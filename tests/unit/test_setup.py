from tests.test_helper import *
import os

class TestSetup(unittest.TestCase):
    def test_packages_includes_all_packages(self):
        with open('setup.py', 'r') as f:
            setup_contents = f.read()
        packages_line = re.findall('packages=.*', setup_contents)
        packages_from_setup = re.findall('"(.*?)"', str(packages_line))

        packages_from_directories = ['braintree']
        directories_that_dont_have_packages = ['braintree.ssl']
        for dirname, dirnames, filenames in os.walk('braintree'):
            for subdirname in dirnames:
                package_from_directory = re.sub('/', '.', os.path.join(dirname, subdirname))
                if package_from_directory not in directories_that_dont_have_packages:
                    packages_from_directories.append(package_from_directory)

        self.assertEquals(packages_from_directories, packages_from_setup)
