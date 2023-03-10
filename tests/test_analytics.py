from configparser import ConfigParser
from unittest import TestCase
from pyeti import YetiApi


class TestAnalytics(TestCase):
    def setUp(self) -> None:
        self.config = ConfigParser()
        self.config.read("pyeti.conf")
        self.url = self.config.get("yeti", "url")
        self.api_key = self.config.get("yeti", "api_key")
        self.settings = self.config["settings"]
        self.api = YetiApi(url=self.url, api_key=self.api_key)

        return super().setUp()

    def test_onyphe(self):
        settings = {"onyphe_api_key": self.settings["onyphe_api_key"]}
        res = self.api.add_analytics_settings(settings)
        if not res:
            raise Exception("Failed to add settings")

        oneshot = self.api.get_analytic_oneshot("Onyphe")
        if not oneshot:
            raise Exception("Failed to get oneshot")
        obs = self.api.add_ipadress("8.8.8.8")
        res = self.api.analytics_oneshot_run(oneshot, obs)
        if not res:
            raise Exception("Failed to run oneshot")

    def test_shodan(self):
        settings = {"shodan_api_key": self.settings["shodan_api_key"]}
        res = self.api.add_analytics_settings(settings)
        if not res:
            raise Exception("Failed to add settings")
        oneshot = self.api.get_analytic_oneshot("Shodan")
        if not oneshot:
            raise Exception("Failed to get oneshot")
        obs = self.api.add_ipadress("8.8.8.8")
        res = self.api.analytics_oneshot_run(oneshot, obs)
        if not res:
            raise Exception("Failed to run oneshot")

    def test_passivetotaldns(self):
        settings = {
            "passivetotal_api_username": self.settings["passivetotal_api_username"],
            "passivetotal_api_key": self.settings["passivetotal_api_key"],
        }
        res = self.api.add_analytics_settings(settings)
        if not res:
            raise Exception("Failed to add settings")
        oneshot = self.api.get_analytic_oneshot("PassiveTotal Passive DNS")
        if not oneshot:
            raise Exception("Failed to get oneshot")
        obs = self.api.add_ipadress("8.8.8.8")
        res = self.api.analytics_oneshot_run(oneshot, obs)
        if not res:
            raise Exception("Failed to run oneshot")
    

    def test_passivetotalmalware(self):
        settings = {
            "passivetotal_api_username": self.settings["passivetotal_api_username"],
            "passivetotal_api_key": self.settings["passivetotal_api_key"],
        }
        res = self.api.add_analytics_settings(settings)
        if not res:
            raise Exception("Failed to add settings")
        oneshot = self.api.get_analytic_oneshot("Get Malware")
        if not oneshot:
            raise Exception("Failed to get oneshot")
        obs = self.api.add_ipadress("8.8.8.8")
        res = self.api.analytics_oneshot_run(oneshot, obs)
        if not res:
            raise Exception("Failed to run oneshot")
    
    def test_passivetotalsubdomains(self):
        settings = {
            "passivetotal_api_username": self.settings["passivetotal_api_username"],
            "passivetotal_api_key": self.settings["passivetotal_api_key"],
        }
        res = self.api.add_analytics_settings(settings)
        if not res:
            raise Exception("Failed to add settings")
        oneshot = self.api.get_analytic_oneshot("Get Subdomains")
        if not oneshot:
            raise Exception("Failed to get oneshot")
        obs = self.api.add_hostname("google.com")
        res = self.api.analytics_oneshot_run(oneshot, obs)
        if not res:
            raise Exception("Failed to run oneshot")
    
    def test_passivetotalwhois(self):
        settings = {
            "passivetotal_api_username": self.settings["passivetotal_api_username"],
            "passivetotal_api_key": self.settings["passivetotal_api_key"],
        }
        res = self.api.add_analytics_settings(settings)
        if not res:
            raise Exception("Failed to add settings")
        oneshot = self.api.get_analytic_oneshot("PassiveTotal Whois")
        if not oneshot:
            raise Exception("Failed to get oneshot")
        obs = self.api.add_hostname("google.com")
        res = self.api.analytics_oneshot_run(oneshot, obs)
        if not res:
            raise Exception("Failed to run oneshot")
        
    def test_urlscanio_hostname(self):            
        oneshot = self.api.get_analytic_oneshot("UrlScanIo")
        if not oneshot:
            raise Exception("Failed to get oneshot")
        obs = self.api.add_hostname("joyfulkayy.wixsite.com")
        
        res = self.api.analytics_oneshot_run(oneshot, obs)
        if not res:
            raise Exception("Failed to run oneshot")
        
    def test_urlscanio_ip(self):            
        oneshot = self.api.get_analytic_oneshot("UrlScanIo")
        if not oneshot:
            raise Exception("Failed to get oneshot")
        obs = self.api.add_ipadress("35.242.251.130")
        if not obs:
            raise Exception("Failed to add IP")
        res = self.api.analytics_oneshot_run(oneshot, obs)
        if not res:
            raise Exception("Failed to run oneshot")
    
    def test_urlscanio_hash(self):
        oneshot = self.api.get_analytic_oneshot("UrlScanIo")
        if not oneshot:
            raise Exception("Failed to get oneshot")
        obs = self.api.add_hash("d23633501bdcbc8d5572aa7e61b69fb39fabb4656dcc9e4bfb665d5d112da13f")
        if not obs:
            raise Exception("Failed to add Hash")
        res = self.api.analytics_oneshot_run(oneshot, obs)
        if not res:
            raise Exception("Failed to run oneshot")

    def test_malshare_hash(self):
        settings = {"malshare_api_key": self.settings["malshare_api_key"]}
        res = self.api.add_analytics_settings(settings)
        if not res:
            raise Exception("Failed to add settings")
        oneshot = self.api.get_analytic_oneshot("MalShare")
        if not oneshot:
            raise Exception("Failed to get oneshot")
        obs = self.api.add_hash("d2c1ac8249f477f7f00b95938a708cc3b9581ee2e20d622993efe9a14f8ce8dd")
        if not obs:
            raise Exception("Failed to add Hash")
        res = self.api.analytics_oneshot_run(oneshot, obs)
        if not res:
            raise Exception("Failed to run oneshot")
