from modules.core.permission.models import Permission
import pytest
from modules.core.permission.repository import PermissionRepository
from .setup import register_test_db, register_test_injections, \
                   teardown, load_permissions, drop_all_collections

_perm_repo = PermissionRepository()


@pytest.fixture(autouse=True)
def setup():
    register_test_db()
    register_test_injections()
    load_permissions()


def test_can_get_a_list_of_all_permissions():
    permissions = _perm_repo.get_all_permissions()

    assert len(permissions) > 0


def test_can_create_new_permission():
    permission = _perm_repo.create_new_permission(
                    route="test:test_new_perm",
                    description="Just a test permissions.")

    result = Permission.objects(route=permission.route).first()

    assert result is not None


def tests_teardown():
    drop_all_collections()
    teardown()
