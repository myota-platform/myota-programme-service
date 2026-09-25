import unittest

from programmes import ProgrammeHandler


class EntityTypeManagementTests(unittest.TestCase):
    def setUp(self):
        self.previous_items = ProgrammeHandler.store.items
        self.previous_events = ProgrammeHandler.store.events
        ProgrammeHandler.store.items = {
            "demo": {"id": "programme-1", "entityTypes": [{"code": "MUNICIPAL_PARK", "label": "Municipal park", "geometry": "MULTIPOLYGON"}], "policyVersion": 1}
        }
        ProgrammeHandler.store.events = []

    def tearDown(self):
        ProgrammeHandler.store.items = self.previous_items
        ProgrammeHandler.store.events = self.previous_events

    def test_creates_and_updates_programme_category(self):
        result = ProgrammeHandler.save_entity_type(None, {"slug": "demo", "_body": {
            "code": "TRAIL", "label": "Trail", "geometry": "LINESTRING", "description": "A walkable route"
        }})
        self.assertEqual(result["entityType"]["code"], "TRAIL")
        self.assertTrue(result["entityType"]["active"])

        result = ProgrammeHandler.save_entity_type(None, {"slug": "demo", "_body": {
            "code": "TRAIL", "originalCode": "TRAIL", "label": "Hiking trail", "geometry": "LINESTRING", "active": False
        }})
        self.assertEqual(result["entityType"]["label"], "Hiking trail")
        self.assertFalse(result["entityType"]["active"])

    def test_category_codes_cannot_be_renamed(self):
        with self.assertRaisesRegex(ValueError, "cannot be renamed"):
            ProgrammeHandler.save_entity_type(None, {"slug": "demo", "_body": {
                "code": "CITY_PARK", "originalCode": "MUNICIPAL_PARK", "label": "City park", "geometry": "POLYGON"
            }})


if __name__ == "__main__":
    unittest.main()
