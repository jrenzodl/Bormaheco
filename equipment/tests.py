from django.test import TestCase


class ExampleTestCase(TestCase):
    def setUp(self):
        self.maven = Dog(name="Maven", breed="corgi")
        self.maven.save()

    def test_save(self):
        self.assertEquals(self.maven.name, "Maven")
        # You can mix in pytest's `assert` approach!
        assert self.maven.breed == "corgi
