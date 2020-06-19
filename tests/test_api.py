import random
import unittest

from pyenvapi import PyenvAPI


class TestBase(unittest.TestCase):
    """Base class for test cases."""

    def setUp(self):
        self.api_object = PyenvAPI()

    def tearDown(self):
        del self.api_object.global_version


class InstallationTestCase(TestBase):
    """Test case for install/uninstall operations."""

    installed_version = None # Version installed during the test.

    def test_install(self):
        # Someday, Travis, someday...
        pass        

    def test_uninstall(self):
        if self.installed_version != None:
            version = self.installed_version
        else:
            version = random.choice(self.api_object.installed)
        
        ps = self.api_object.uninstall(version)
        returncode, stdour, stderr = ps

        self.assertEqual(returncode, 0)
        self.assertNotIn(version, self.api_object.installed)


class GlobalTestCase(TestBase):
    """Test case for `global_version` setter and deleter."""

    @property
    def random_installed(self):
        version = [random.choice(self.api_object.installed)]
        return tuple(version)

    def test_global_setter(self):
        version = self.random_installed
        self.api_object.global_version = version
        
        self.assertEqual(self.api_object.global_version, version)

    def test_global_deleter(self):
        version = self.random_installed
        self.api_object.global_version = version
        
        del self.api_object.global_version
        
        self.assertNotEqual(self.api_object.global_version, version)


if __name__ == '__main__':
    unittest.main()
