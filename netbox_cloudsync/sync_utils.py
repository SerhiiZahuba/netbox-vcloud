import base64


def build_basic_auth_header(username, password):
    token = base64.b64encode(f"{username}:{password}".encode()).decode()
    return f"Basic {token}"


def extract_primary_connection(details):
    for section in details.get("section", []):
        if section.get("_type") != "NetworkConnectionSectionType":
            continue

        connections = section.get("networkConnection") or []
        if not connections:
            return None, None

        connection = connections[0]
        return connection.get("ipAddress"), connection.get("macAddress")

    return None, None


def should_sync_vm(vm, cfg):
    status = (vm.get("status") or "").upper()
    if not cfg.sync_poweroff and status != "POWERED_ON":
        return False

    is_template = vm.get("isVAppTemplate") in (True, "true", "True")
    if is_template and not cfg.sync_templates:
        return False

    return True


def normalize_vm_status(status):
    return "active" if (status or "").upper() == "POWERED_ON" else "offline"
