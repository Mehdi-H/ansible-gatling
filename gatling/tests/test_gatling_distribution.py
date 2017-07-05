import testinfra
# import testinfra.utils.ansible_runner
import unittest

# testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
# '.molecule/ansible_inventory').get_hosts('all')


class TestGatlingDistribution(unittest.TestCase):

    def setUp(self):
        self.host = testinfra.get_backend(
            "ansible://gatling?ansible_inventory=.molecule/ansible_inventory"
        )
        self.file = self.host.get_module("File")
        self.user = "root"
        self.gatling = {
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

    def test_hosts_file(self):
        f = self.file('/etc/hosts')
        self.assertTrue(f.exists)
        self.assertTrue(f.user == 'root')
        self.assertTrue(f.group == 'root')

    def test_gatling_distribution_is_present_as_a_directory(self):

        # Given f as a Gatling distribution resource
        f = self.file('/' + self.user + '/' + self.gatling.get("package")())

        # Then f should be a directory
        self.assertTrue(f.is_directory)

    def test_gatling_distribution_has_the_expected_content_in_it(self):

        # Given f as a Gatling distribution resource
        f = self.file(
            '/' + self.user + '/' +
            self.gatling.get("zip").get("name")()
        )
        # and knowing f's md5 hash
        gatling_distribution_md5_hash = self.gatling.get("zip").get("md5sum")

        # Then f should not be empty
        self.assertTrue(f.size > 0)
        # and f's hash should be as expected
        self.assertTrue(f.md5sum == gatling_distribution_md5_hash)


if __name__ == '__main__':
    unittest.main()
