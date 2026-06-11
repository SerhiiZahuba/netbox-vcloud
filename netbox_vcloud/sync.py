import requests
from django.utils import timezone
from virtualization.models import VirtualMachine, Cluster, VMInterface
from tenancy.models import Tenant
from dcim.models import Site, DeviceRole
from ipam.models import IPAddress

from .sync_utils import (
    build_basic_auth_header,
    extract_primary_connection,
    normalize_vm_status,
    should_sync_vm,
)

REQUEST_TIMEOUT = 30


def run_sync(cfg):
    headers = {
        "Authorization": build_basic_auth_header(cfg.vcloud_user, cfg.vcloud_password),
        "Accept": "application/*;version=38.1",
    }

    response = requests.post(
        f"{cfg.vcloud_url}/cloudapi/1.0.0/sessions",
        headers=headers,
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()

    token = response.headers.get("X-VMWARE-VCLOUD-ACCESS-TOKEN")
    if not token:
        raise RuntimeError("vCloud auth failed: missing access token")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/*+json;version=38.1",
    }

    vms_response = requests.get(
        f"{cfg.vcloud_url}/api/query?type=vm&page=1&pageSize=100&format=records",
        headers=headers,
        timeout=REQUEST_TIMEOUT,
    )
    vms_response.raise_for_status()

    vms = vms_response.json().get("record", [])
    if isinstance(vms, dict):
        vms = [vms]

    cluster = cfg.netbox_cluster or Cluster.objects.first()
    site = cfg.netbox_site or Site.objects.first()
    role = cfg.netbox_role or DeviceRole.objects.first()
    tenant = cfg.netbox_tenant or Tenant.objects.first()

    for vm in vms:
        if not should_sync_vm(vm, cfg):
            continue

        name = vm.get("name")
        href = vm.get("href")
        if not name or not href:
            continue

        details_response = requests.get(href, headers=headers, timeout=REQUEST_TIMEOUT)
        details_response.raise_for_status()

        ip, mac = extract_primary_connection(details_response.json())

        vm_obj, _ = VirtualMachine.objects.update_or_create(
            name=name,
            defaults={
                "status": normalize_vm_status(vm.get("status", "POWERED_ON")),
                "vcpus": vm.get("numberOfCpus", 0),
                "memory": vm.get("memoryMB", 0),
                "disk": vm.get("totalStorageAllocatedMb", 0),
                "cluster": cluster,
                "site": site,
                "tenant": tenant,
                "role": role,
                "comments": f"Synced {timezone.now().strftime('%F %T')}",
            },
        )

        iface_defaults = {"enabled": True}
        if mac:
            iface_defaults["mac_address"] = mac

        iface, _ = VMInterface.objects.get_or_create(
            virtual_machine=vm_obj,
            name="eth0",
            defaults=iface_defaults,
        )

        if ip:
            ip_obj, _ = IPAddress.objects.get_or_create(address=f"{ip}/24")
            ip_obj.assigned_object = iface
            ip_obj.status = "active"
            ip_obj.save()

    cfg.last_sync = timezone.now()
    cfg.save()
