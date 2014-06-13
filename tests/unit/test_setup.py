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
                if package_from_directory not in directories_that_dont_have_packages and subdirname != '__pycache__':
                    packages_from_directories.append(package_from_directory)

        mismatch_message = "List of packages in setup.py doesn't match subdirectories of 'braintree' - " \
                + "add your new directory to 'packages, or if none, `git clean -df` to remove a stale directory"
        self.assertEquals(sorted(packages_from_directories), sorted(packages_from_setup), mismatch_message)
