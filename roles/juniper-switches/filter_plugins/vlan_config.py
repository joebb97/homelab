from typing import Any


def generate_vlan_config(
    current_vlans: list[dict[str, Any]],
    desired_vlans: list[dict[str, Any]],
    l2_interfaces: list[dict[str, Any]],
    current_irbs: list[dict[str, Any]],
    desired_irbs: list[dict[str, Any]],
) -> list[str]:
    current_vlans_by_name = {v["name"]: v for v in current_vlans}
    current_vlans_by_id = {v["vlan_id"]: v for v in current_vlans}
    desired_vlans_by_name = {v["name"]: v for v in desired_vlans}
    desired_vlans_by_id = {v["vlan_id"]: v for v in desired_vlans}
    desired_irbs_by_unit = {v["unit"]: v for v in desired_irbs}

    lines: list[str] = []
    for current in current_vlans:
        name = current["name"]
        vid = current["vlan_id"]

        if name not in desired_vlans_by_name and vid not in desired_vlans_by_id:
            if name != "default":
                lines.append(f"delete vlans {name}")
                lines.append(f"delete interfaces irb unit {vid}")
            continue

        desired_vlan = desired_vlans_by_id.get(vid)
        if desired_vlan and name != desired_vlan["name"]:
            lines.append(f"rename vlans {name} to {desired_vlan['name']}")
            lines.extend(_generate_l2_rename_lines(l2_interfaces, name, desired_vlan["name"]))

        desired_vlan = desired_vlans_by_name.get(name)
        if desired_vlan and vid != desired_vlan["vlan_id"]:
            lines.append(f"set vlans {name} vlan-id {desired_vlan['vlan_id']}")
            lines.append(f"delete interfaces irb unit {vid}")

    for desired_vlan in desired_vlans:
        name = desired_vlan["name"]
        vid = desired_vlan["vlan_id"]
        if name not in current_vlans_by_name and vid not in current_vlans_by_id:
            lines.append(f"set vlans {name} vlan-id {vid}")
            desired_irb = desired_irbs_by_unit.get(vid)
            if desired_irb:
                lines.append(f"set vlans {name} l3-interface irb.{vid}")

    for current in current_irbs:
        unit = int(current["unit"])
        if unit not in desired_irbs_by_unit and unit != 0:
            lines.append(f"delete interfaces irb unit {unit}")

    return lines


def _generate_l2_rename_lines(
    interfaces: list[dict[str, Any]],
    old_name: str,
    new_name: str,
) -> list[str]:
    lines: list[str] = []
    for iface in interfaces:
        access_vlan = iface.get("access", {}).get("vlan")
        trunk_vlans = iface.get("trunk", {}).get("allowed_vlans", [])

        if access_vlan == old_name or old_name in trunk_vlans:
            lines.append(
                f"delete interfaces {iface['name']} unit 0 "
                f"family ethernet-switching vlan members {old_name}"
            )
            lines.append(
                f"set interfaces {iface['name']} unit 0 "
                f"family ethernet-switching vlan members {new_name}"
            )

    return lines


class FilterModule:
    def filters(self):
        return {
            "generate_vlan_config": generate_vlan_config,
        }
