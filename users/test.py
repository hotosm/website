import pytest
from django.contrib.auth import get_user_model

from .factory import UserFactory

User = get_user_model()


@pytest.mark.django_db
class TestUser:
    def test_user_factory(self):
        user = UserFactory()
        assert isinstance(user, User)

    def test_user_model(self):
        user1 = UserFactory()
        user2 = UserFactory()

        assert user1.username == "user1"
        assert user1.first_name == "first_name1"
        assert user1.last_name == "last_name1"
        assert user1.email == "email1@hotosm.com"
        assert user1.check_password("password")

        assert user2.username == "user2"
        assert user2.first_name == "first_name2"
        assert user2.last_name == "last_name2"
        assert user2.email == "email2@hotosm.com"
        assert user2.check_password("password")
