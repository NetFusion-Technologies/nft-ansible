#!/usr/bin/env python3
import ipaddress
import json
import os
import re
import sys
import time
from typing import Any, Dict, Optional

import yaml
from proxmoxer import ProxmoxAPI

CONFIG_PATH = os.path.expanduser("~/.pve_api.yml")
CACHE_PATH = "/tmp/proxmox_inventory_cache.json"
CACHE_TTL = 60


def debug(msg: str) -> None:
    if os.environ.get("PROXMOX_INVENTORY_DEBUG", "").lower() in {"1", "true", "yes"}:
        print(f"[proxmox_inventory] {msg}", file=sys.stderr)


def parse_bool(value: Any, default: bool = True) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def sanitize(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", name)


def load_conf() -> Dict[str, Any]:
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(CONFIG_PATH)

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    cfg["verify_ssl"] = parse_bool(cfg.get("verify_ssl", True))
    return cfg


def load_cache() -> Optional[Dict[str, Any]]:
    if os.environ.get("PROXMOX_INVENTORY_NO_CACHE", "").lower() in {"1", "true", "yes"}:
        return None

    if not os.path.exists(CACHE_PATH):
        return None

    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if time.time() - data["timestamp"] < CACHE_TTL:
            debug("Using cached inventory")
            return data["inventory"]
    except Exception:
        return None

    return None


def save_cache(inventory: Dict[str, Any]) -> None:
    try:
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump({"timestamp": time.time(), "inventory": inventory}, f)
    except Exception:
        pass


def connect(cfg: Dict[str, Any]) -> ProxmoxAPI:
    return ProxmoxAPI(
        cfg["api_host"],
        user=cfg["api_user"],
        token_name=cfg["api_token_name"],
        token_value=cfg["api_token_value"],
        verify_ssl=cfg["verify_ssl"],
    )


def base_inventory():
    return {
        "_meta": {"hostvars": {}},
        "all": {"children": ["qemu", "qemu_linux", "lxc", "proxmox_guests", "ssh_ready"]},
        "qemu": {"hosts": []},
        "qemu_linux": {"hosts": []},
        "lxc": {"hosts": []},
        "ssh_ready": {"hosts": []},
        "proxmox_guests": {"children": ["qemu", "lxc"]},
    }

def ensure_group(inv: Dict[str, Any], name: str) -> None:
    if name not in inv:
        inv[name] = {"hosts": []}


def add_host(inv: Dict[str, Any], group: str, host: str) -> None:
    ensure_group(inv, group)
    inv[group]["hosts"].append(host)


def is_good_ip(ip: str) -> bool:
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False

    if addr.is_loopback:
        return False
    if addr.is_link_local:
        return False
    if addr.is_multicast:
        return False
    if addr.is_unspecified:
        return False

    return True


def ip_score(ip: str) -> int:
    addr = ipaddress.ip_address(ip)

    if addr.version == 4:
        s = str(addr)
        if s.startswith("192.168."):
            return 100
        if s.startswith("10."):
            return 90
        if s.startswith("172."):
            return 80
        return 50

    return 40


def get_ip(proxmox: ProxmoxAPI, node: str, vmid: str, vmtype: str) -> Optional[str]:
    candidates = []

    try:
        if vmtype == "qemu":
            res = proxmox.nodes(node).qemu(vmid).agent("network-get-interfaces").get()
            for iface in res.get("result", []):
                for addr in iface.get("ip-addresses", []):
                    ip = addr.get("ip-address")
                    if ip and is_good_ip(ip):
                        candidates.append(ip)

        elif vmtype == "lxc":
            res = proxmox.nodes(node).lxc(vmid).interfaces.get()
            for iface in res:
                inet = iface.get("inet")
                inet6 = iface.get("inet6")

                if inet:
                    ip = inet.split("/")[0]
                    if is_good_ip(ip):
                        candidates.append(ip)

                if inet6:
                    ip = inet6.split("/")[0]
                    if is_good_ip(ip):
                        candidates.append(ip)
    except Exception:
        return None

    if not candidates:
        return None

    candidates = sorted(set(candidates), key=ip_score, reverse=True)
    return candidates[0]


def build() -> Dict[str, Any]:
    cached = load_cache()
    if cached:
        return cached

    cfg = load_conf()
    proxmox = connect(cfg)

    inv = base_inventory()
    resources = proxmox.cluster.resources.get()

    debug(f"Resources: {len(resources)}")

    for r in resources:
        if r.get("type") not in ("qemu", "lxc"):
            continue

        if r.get("status") != "running":
            continue

        name = r.get("name") or f'{r["type"]}-{r["vmid"]}'
        node = r["node"]
        vmid = str(r["vmid"])
        rtype = r["type"]

        hostvars = {
            "pve_type": rtype,
            "pve_node": node,
            "pve_vmid": vmid,
            "pve_tags": r.get("tags"),
        }

        ip = get_ip(proxmox, node, vmid, rtype)
        if ip:
            hostvars["ansible_host"] = ip
            add_host(inv, "ssh_ready", name)
        else:
            hostvars["ansible_skip_reason"] = "no_usable_ip"

        inv["_meta"]["hostvars"][name] = hostvars

        WINDOWS_OR_SPECIAL = {"ViewPower", "MacOS", "OPNsense", "haos"}

        if rtype == "qemu":
            add_host(inv, "qemu", name)
            if name not in WINDOWS_OR_SPECIAL:
                add_host(inv, "qemu_linux", name)
        elif rtype == "lxc":
            add_host(inv, "lxc", name)

        node_group = f"node_{sanitize(node)}"
        type_group = f"{node_group}_{rtype}"
        add_host(inv, node_group, name)
        add_host(inv, type_group, name)

        tags = r.get("tags")
        if tags:
            for tag in tags.split(";"):
                add_host(inv, f"tag_{sanitize(tag)}", name)

    for group_data in inv.values():
        if isinstance(group_data, dict) and "hosts" in group_data:
            group_data["hosts"] = sorted(set(group_data["hosts"]))

    save_cache(inv)
    return inv


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--host":
        print("{}")
        return

    print(json.dumps(build(), indent=2))


if __name__ == "__main__":
    main()

