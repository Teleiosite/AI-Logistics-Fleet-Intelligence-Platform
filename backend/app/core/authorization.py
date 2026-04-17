from dataclasses import dataclass


@dataclass(frozen=True)
class Permission:
    resource: str
    action: str


ROLE_POLICY: dict[str, set[Permission]] = {
    "super_admin": {Permission("*", "*")},
    "company_admin": {Permission("*", "*")},
    "transport_admin": {
        Permission("shipments", "read"),
        Permission("shipments", "write"),
        Permission("fleet", "read"),
        Permission("fleet", "write"),
        Permission("fuel", "read"),
        Permission("fuel", "write"),
        Permission("invoices", "approve"),
        Permission("analytics", "read"),
        Permission("notifications", "read"),
        Permission("notifications", "write"),
    },
    "logistics_manager": {
        Permission("shipments", "read"),
        Permission("shipments", "write"),
        Permission("fleet", "read"),
        Permission("dvr", "read"),
        Permission("dvr", "write"),
        Permission("analytics", "read"),
        Permission("notifications", "read"),
    },
    "finance_officer": {
        Permission("invoices", "read"),
        Permission("invoices", "write"),
        Permission("invoices", "approve"),
        Permission("fuel", "read"),
        Permission("analytics", "read"),
        Permission("notifications", "read"),
    },
    "driver": {
        Permission("shipments", "read"),
        Permission("shipments", "write_own"),
        Permission("fuel", "write_own"),
        Permission("dvr", "write_own"),
        Permission("notifications", "read"),
    },
    "auditor": {
        Permission("shipments", "read"),
        Permission("fleet", "read"),
        Permission("fuel", "read"),
        Permission("invoices", "read"),
        Permission("analytics", "read"),
        Permission("notifications", "read"),
    },
}


def has_permission(role: str, resource: str, action: str) -> bool:
    permissions = ROLE_POLICY.get(role, set())
    return (
        Permission("*", "*") in permissions
        or Permission(resource, action) in permissions
        or Permission(resource, "*") in permissions
    )
