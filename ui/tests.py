from django.test import TestCase
from .views import calculate_statistics


class HomePageTests(TestCase):
    def test_index_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_allerts_page_loads(self):
        response = self.client.get('/allerts/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'EU-recommended thresholds')

class StatisticsFunctionTests(TestCase):
    def test_calculate_statistics(self):
        chart_data = [
            {"name": "Farm1", "values_temp": [1, 3, 5]},
        ]
        stats = calculate_statistics(chart_data)
        self.assertEqual(stats["Farm1"]["values_temp"]["min"], 1)
        self.assertEqual(stats["Farm1"]["values_temp"]["max"], 5)
        self.assertEqual(stats["Farm1"]["values_temp"]["mean"], 3)


class DashboardTests(TestCase):
    def test_dashboard_page_loads(self):
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 200)


class DashLayoutContentTests(TestCase):
    def test_layout_contains_placeholders(self):
        from ui.dashapp import app
        layout_str = str(app.layout)
        self.assertIn("Kazova Farm", layout_str)
        self.assertIn("Uncertainty ranges of sensors", layout_str)
        self.assertIn("Energy consumption", layout_str)
        self.assertIn(
            "In Turkey: Milk data and milk composition (manual entry option).",
            layout_str,
        )
        self.assertIn("General farm location", layout_str)
        self.assertIn("Farm size.", layout_str)
        self.assertIn(
            "In Turkey (manual entry): Annual energy consumption.",
            layout_str,
        )
        self.assertIn("Ventilation specs", layout_str)
