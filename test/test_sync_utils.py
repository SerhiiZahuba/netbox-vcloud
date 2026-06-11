from types import SimpleNamespace

from netbox_vcloud.sync_utils import (
    build_basic_auth_header,
    extract_primary_connection,
    normalize_vm_status,
    should_sync_vm,
)


def test_build_basic_auth_header_encodes_credentials():
    assert build_basic_auth_header("user", "pass") == "Basic dXNlcjpwYXNz"


def test_extract_primary_connection_returns_first_network_values():
    ip, mac = extract_primary_connection(
        {
            "section": [
                {
                    "_type": "NetworkConnectionSectionType",
                    "networkConnection": [
                        {"ipAddress": "10.0.0.5", "macAddress": "00:11:22:33:44:55"}
                    ],
                }
            ]
        }
    )

    assert ip == "10.0.0.5"
    assert mac == "00:11:22:33:44:55"


def test_extract_primary_connection_returns_empty_values_when_missing():
    assert extract_primary_connection({"section": []}) == (None, None)


def test_should_sync_vm_respects_power_and_template_flags():
    cfg = SimpleNamespace(sync_poweroff=False, sync_templates=False)

    assert should_sync_vm({"status": "POWERED_ON"}, cfg) is True
    assert should_sync_vm({"status": "POWERED_OFF"}, cfg) is False
    assert should_sync_vm({"status": "POWERED_ON", "isVAppTemplate": True}, cfg) is False


def test_normalize_vm_status_maps_power_state():
    assert normalize_vm_status("POWERED_ON") == "active"
    assert normalize_vm_status("POWERED_OFF") == "offline"
