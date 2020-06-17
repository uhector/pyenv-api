import random
import unittest

from pyenv_api import PyenvAPI


class TestBase(unittest.TestCase):
    """Base class for test cases."""

    def setUp(self):
        self.api_object = PyenvAPI()

    def tearDown(self):
        del self.api_object.global_version


class InstallationTestCase(TestBase):
    """Test case for install/uninstall operations."""

    def test_install(self):
        # Someday Travis, someday...
        pass

    def test_uninstall(self):
        version = random.choice(self.api_object.installed_versions)
        ps = self.api_object.uninstall(version)

        self.assertEqual(ps.returncode, 0)
        self.assertNotIn(version, self.api_object.installed_versions)


class GlobalTestCase(TestBase):
    """Test case for `global_version` setter and deleter."""

    def test_global_setter(self):
        version = [random.choice(self.api_object.installed_versions)]
        self.api_object.global_version = version
        
        self.assertEqual(self.api_object.global_version, version)

    def test_global_deleter(self):
        version = [random.choice(self.api_object.installed_versions)]
        self.api_object.global_version = version

        del self.api_object.global_version

        self.assertNotEqual(self.api_object.global_version, version)


if __name__ == '__main__':
    unittest.main()