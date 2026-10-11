from types import SimpleNamespace
import unittest
from unittest.mock import patch

from programmes import ProgrammeHandler


class ProgrammeMetricsTests(unittest.TestCase):
    def test_metrics_are_aggregate_and_have_no_domain_labels(self):
        fake_store = SimpleNamespace(
            items={
                "private-programme-slug": {
                    "entityTypeCodes": ["POTA", "SOTA"],
                },
                "another-private-slug": {
                    "entityTypeCodes": ["POTA"],
                },
            },
            data={"entityTypeCatalog": {"POTA": {}, "SOTA": {}}},
        )

        with patch.object(ProgrammeHandler, "store", fake_store):
            output = ProgrammeHandler.metrics_text()

        self.assertIn("myota_programmes 2", output)
        self.assertIn("myota_programme_entity_type_catalog_items 2", output)
        self.assertIn("myota_programme_category_assignments 3", output)
        self.assertNotIn("private-programme-slug", output)
        self.assertNotIn("POTA", output)


if __name__ == "__main__":
    unittest.main()
