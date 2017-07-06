import testinfra
# import testinfra.utils.ansible_runner
import unittest

# testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
# '.molecule/ansible_inventory').get_hosts('all')


class TestGatlingDistribution(unittest.TestCase):

    def setUp(self):
        """
        Some initializations are made.
        * We fetch the gatling host from testinfra + Ansible inventory,
        * We set the user,
        * We set some information about the gatling distribution
            * distribution name,
            * version,
            * package name (=distribution + version),
            * zip name
        """

        # We get every hosts that fit in the gatling group in a list
        gatling_hosts = testinfra.get_hosts([
            "ansible://gatling?ansible_inventory=.molecule/ansible_inventory"
            ]
        )
        # We set some information on the remote environment
        self.gatling = {
            "hosts": gatling_hosts,
            "user": "root",
            "distribution": "gatling-charts-highcharts-bundle-",
            "version": "2.2.5",
            "package": (
                lambda: self.gatling['distribution'] + self.gatling["version"]
            ),
            "zip": {
                "name": (
                    lambda: self.gatling['package']() + '-bundle.zip'
                ),
                "md5sum": "b2f3448466b815c29d2d81fe2335503e"
            }
        }

    def test_gatling_distribution_has_the_expected_content_in_it(self):
        """
        We test that the gatling .zip distribution is present,
            And that its md5 digest is as expected.
        """

        for host in self.gatling.get("hosts"):

            # Given f as a Gatling distribution resource
            f = host.file(
                '/' + self.gatling.get("user") + '/' +
                self.gatling.get("zip").get("name")()
            )
            # and knowing f's md5 hash
            gatling_distribution_md5_hash = \
                self.gatling.get("zip").get("md5sum")

            # Then f should not be empty
            self.assertTrue(f.size > 0)
            # and f's hash should be as expected
            self.assertTrue(f.md5sum == gatling_distribution_md5_hash)

    def test_gatling_distribution_is_present_as_a_directory(self):
        """
        We test that the gatling .zip distribution was unarchived,
            And that it is now present as a directory.
        """

        for host in self.gatling.get("hosts"):

            # Given f as a Gatling distribution resource
            f = host.file(
                '/' + self.gatling.get("user") + '/' +
                self.gatling.get("package")()
            )

            # Then f should be a directory
            self.assertTrue(f.is_directory)


if __name__ == '__main__':
    unittest.main()
