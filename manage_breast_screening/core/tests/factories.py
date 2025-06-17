from django.contrib.auth.models import User
from factory.declarations import Sequence
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = Sequence(lambda n: "user%d@example.com" % n)
    first_name = "Firstname"
    last_name = "Lastname"
