import testinfra
import unittest


class TestGatlingDependencies(unittest.TestCase):

    def setUp(self):
        # We get every hosts that fit in the gatling group in a list
        self.gatling_hosts = testinfra.get_hosts([
            "ansible://gatling?ansible_inventory=.molecule/ansible_inventory"
        ])

    def test_unarchive_dependency_is_installed(self):
        """
        We test that a dependency is available on the machine,
         so that we can unarchive the gatling distribution.
        """

        # Given
        unarchive_package = "unzip"

        # Then, unzip is installed on the machine
        for host in self.gatling_hosts:
            self.assertTrue(host.package(unarchive_package).is_installed)

    def test_debconf_package_is_installed(self):
        """
        We test that the debconf & debconf-utils packages are installed,
        so that we can automatize the installation of java,
        without any user-input, through Ansible.
        """

        # Given
        java_package = "oracle-java8-installer"

        # Then, java is installed on the machine
        for host in self.gatling_hosts:
            self.assertTrue(host.package(java_package).is_installed)

    def test_java_package_is_installed(self):
        """
        We test that java is installed on the machine,
        so that we can launch the Gatling load testing tool.
        """
        debconf_packages = ["debconf", "debconf-utils"]
        print(zip(self.gatling_hosts, debconf_packages))
        for host, debconf_package in zip(self.gatling_hosts, debconf_packages):
            self.assertTrue(host.package(debconf_package).is_installed)


if __name__ == '__main__':
    unittest.main()
