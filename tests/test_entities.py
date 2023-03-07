

from configparser import ConfigParser
from unittest import TestCase
import unittest
import pyeti

class TestEntities(TestCase):
    """Tests for Yeti API."""
    def setUp(self):
            config = ConfigParser()
            config.read("pyeti.conf")
            url = config.get('yeti', 'url')
            api_key = config.get('yeti', 'api_key')
            self.api = pyeti.YetiApi(url=url, api_key= api_key)
    
    def test_add_malware(self):
        """Adds a malware with tags and tests for that value and tags match."""
        malware_name = "test_malware"
        self.api.add_malware(name=malware_name, tags=['asd'])
        malware=self.api.entity_search(name=malware_name)
        self.assertEqual(malware[0]['name'], malware_name)

    
    def test_add_campaign(self):
        """Adds a campaign with tags and tests for that value and tags match."""
        campaign_name = "test_campaign"
        self.api.add_campaign(name=campaign_name, tags=['asd'])
        campaign=self.api.entity_search(name=campaign_name)
        self.assertEqual(campaign[0]['name'], campaign_name)

    
    def test_add_actor(self):
        """Adds an actor with tags and tests for that value and tags match."""
        actor_name = "test_actor"
        self.api.add_actor(name=actor_name, tags=['asd'])
        actor=self.api.entity_search(name=actor_name)
        self.assertEqual(actor[0]['name'], actor_name)
      
    def test_add_ttp(self):
        """Adds a ttp with tags and tests for that value and tags match."""
        ttp_name = "test_ttp"
        self.api.add_ttp(name=ttp_name,killchain="toto", tags=['asd'])
        ttp=self.api.entity_search(name=ttp_name)
        self.assertEqual(ttp[0]['name'], ttp_name)
       
    
    def test_add_exploit(self):
        """Adds an exploit with tags and tests for that value and tags match."""
        exploit_name = "test_exploit"
        self.api.add_exploit(name=exploit_name, tags=['asd'])
        exploit=self.api.entity_search(name=exploit_name)
        self.assertEqual(exploit[0]['name'], exploit_name)
    
    def test_add_compagny(self):
        """Adds a compagny with tags and tests for that value and tags match."""
        compagny_name = "test_compagny"
        self.api.add_company(name=compagny_name, tags=['asd'])
        compagny=self.api.entity_search(name=compagny_name)
        self.assertEqual(compagny[0]['name'], compagny_name)


        
if __name__ == '__main__':
    unittest.main()