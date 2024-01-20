import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from .factory import UserFactory

User = get_user_model()


@pytest.mark.django_db
class TestUser:
    """
    Tests the overriden User Model.
    """

    def test_user_factory(self):
        user = UserFactory()

        assert isinstance(user, User)

    def test_user_str(self):
        user = UserFactory(username="testuser")

        assert str(user) == "testuser"

    def test_user_is_not_anonymous(self):
        user = UserFactory()

        assert not user.is_anonymous

    def test_user_is_authenticated(self):
        user = UserFactory()

        assert user.is_authenticated

    def test_user_get_full_name(self):
        user = UserFactory()

        assert user.get_full_name() == f"{user.first_name} {user.last_name}"

    def test_user_get_short_name(self):
        user = UserFactory()

        assert user.get_short_name() == user.first_name

    def test_user_password_set_and_check(self):
        user = UserFactory()

        user.set_password("newpassword")

        assert user.check_password("newpassword")

    def test_user_has_perm(self):
        user = UserFactory()

        user.is_superuser = True

        assert user.has_perm("auth.view_user")

    def test_user_has_module_perms(self):
        user = UserFactory()

        user.is_superuser = True

        assert user.has_module_perms("auth")

    def test_duplicate_username(self):
        UserFactory(username="testuser")

        with pytest.raises(IntegrityError):
            UserFactory(username="testuser")

    def test_superuser_and_staff_properties(self):
        user = UserFactory(is_superuser=True, is_staff=True)

        assert user.is_superuser
        assert user.is_staff

    def test_email_field(self):
        user = UserFactory(email="test@example.com")

        assert user.email == "test@example.com"

    def test_missing_email(self):
        with pytest.raises(
            IntegrityError,
            match=(
                'null value in column "email" of relation "users_user" violates not-null constraint'
            ),
        ):
            UserFactory(email=None)

    def test_missing_username(self):
        with pytest.raises(
            IntegrityError,
            match=(
                'null value in column "username" of relation "users_user" '
                "violates not-null constraint"
            ),
        ):
            UserFactory(username=None)

    def test_get_username(self):
        user = UserFactory(username="testuser")

        assert user.get_username() == "testuser"

    def test_is_active(self):
        user = UserFactory(is_active=True)

        assert user.is_active

    def test_is_not_staff(self):
        user = UserFactory(is_staff=False)

        assert not user.is_staff

    def test_is_not_superuser(self):
        user = UserFactory(is_superuser=False)

        assert not user.is_superuser

    def test_set_unusable_password(self):
        user = UserFactory()

        user.set_unusable_password()

        assert not user.has_usable_password()
