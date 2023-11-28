import factory
from pytest_factoryboy import register


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: "user%d" % n)
    first_name = factory.Sequence(lambda n: "first_name%d" % n)
    last_name = factory.Sequence(lambda n: "last_name%d" % n)
    email = factory.Sequence(lambda n: "email%d@hotosm.com" % n)
    password = factory.PostGenerationMethodCall("set_password", "password")

    class Meta:
        model = "users.User"
        skip_postgeneration_save = True


register(UserFactory)
