from django.contrib.auth.models import User
import factory
from faker import Faker
from private_files.tests.testapp.models import Document


class UserFactory(factory.DjangoModelFactory):

    class Meta:
        model = User

    first_name = factory.Faker('first_name_male')
    last_name = factory.Faker('last_name')
    username = 'basic'
    email = 'basic@tnot_admin.com'
    password = factory.PostGenerationMethodCall('set_password', 'thepassword')
    is_active = True

class DocumentFactory(factory.DjangoModelFactory):
    class Meta:
        model = Document

    title = "The title"
    owner = factory.SubFactory(UserFactory)
    attachment = factory.django.FileField(filename='the_file.dat')