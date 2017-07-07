import testinfra
import unittest


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
            "home": (
                lambda: "/" + self.gatling.get("user") + "/" +
                self.gatling.get("distribution") +
                self.gatling.get("version") + "/"
            ),
            "version": "2.2.5",
            "package": (
                lambda: self.gatling.get("distribution") +
                self.gatling.get("version")
            ),
            "zip": {
                "name": (
                    lambda: self.gatling['package']() + '-bundle.zip'
                ),
                "md5sum": "b2f3448466b815c29d2d81fe2335503e"
            },
            "simulation": {
                "name": "write.streaming.StaresRamp",
                "directory": "/user-files/simulations",
                "runner_script": "/bin/gatling.sh",
                "report_directory": "/results/",
                "reports_directory": "/results/merged_reports/"
            }
        }

    def test_gatling_distribution_has_the_expected_digest(self):
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

    def test_gatling_distribution_has_a_simulation_directory(self):

        for host in self.gatling.get("hosts"):

            # Given the path to gatling simulation folder
            simulation_directory = host.file(
                self.gatling.get("home")() +
                self.gatling.get("simulation").get("directory")
             )

            # Then the simulation folder exists and it is a directory
            self.assertTrue(simulation_directory.is_directory)

    def test_gatling_distribution_has_a_runner_script(self):

        for host in self.gatling.get("hosts"):

            # Given the path to gatling runner script
            runner_script = host.file(
                self.gatling.get("home")() +
                self.gatling.get("simulation").get("runner_script")
             )

            # Then the simulation folder exists and it is a directory
            self.assertTrue(runner_script.is_file)

    def test_g_d_has_a_report_directory_for_the_hosted_simulations(self):

        for host in self.gatling.get("hosts"):

            # Given the path to gatling runner script
            report_directory = host.file(
                self.gatling.get("home")() +
                self.gatling.get("simulation").get("report_directory")
             )

            # Then the simulation folder exists and it is a directory
            self.assertTrue(report_directory.is_directory)

    def test_g_d_has_a_report_directory_for_the_merged_simulations(self):

        for host in self.gatling.get("hosts"):

            # Given the path to gatling runner script
            reports_directory = host.file(
                self.gatling.get("home")() +
                self.gatling.get("simulation").get("reports_directory")
             )

            # Then the simulation folder exists and it is a directory
            self.assertTrue(reports_directory.is_directory)

    def test_g_d_has_all_the_simulation_files(self):

        # Given a list of simulation files
        simulation_file_names = [
            "AbstractTranquility", "DataGenerator",
            "DruidSineSignalSimulation", "MeasureFeeder",
            "StaresRamp", "TranquilityInstance"
        ]

        for host in self.gatling.get("hosts"):

            for simulation_file_name in simulation_file_names:
                # Then, each of these simulation files exists
                simulation_file = host.file(
                    self.gatling.get("home")() +
                    self.gatling.get("simulation").get("directory") +
                    "/" + simulation_file_name + ".scala"
                )

                self.assertTrue(simulation_file.size > 0)
                self.assertTrue(simulation_file.is_file)


if __name__ == '__main__':
    unittest.main()
