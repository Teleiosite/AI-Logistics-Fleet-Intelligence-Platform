from app.core.authorization import has_permission


def test_super_admin_has_everything() -> None:
    assert has_permission("super_admin", "invoices", "approve")


def test_driver_cannot_approve_invoice() -> None:
    assert not has_permission("driver", "invoices", "approve")
