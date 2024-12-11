from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestColdStore(TransactionCase):
    def setUp(self):
        super().setUp()
        self.cold_store = self.env['warehouse.cold.store'].create({
            'rack_count': 2,
            'column_count': 3,
            'row_count': 4,
            'height': 5.0,
            'width': 10.0,
            'length': 15.0,
            'temperature': -5.0,
            'humidity': 60.0,
        })

    def test_name_generation(self):
        self.assertTrue(self.cold_store.name.startswith('CS'))
        self.assertEqual(len(self.cold_store.name), 5)  # CS + 3 digits

    def test_invalid_temperature(self):
        with self.assertRaises(ValidationError):
            self.env['warehouse.cold.store'].create({
                'rack_count': 2,
                'column_count': 3,
                'row_count': 4,
                'height': 5.0,
                'width': 10.0,
                'length': 15.0,
                'temperature': -35.0,  # Invalid temperature
                'humidity': 60.0,
            })

    def test_invalid_humidity(self):
        with self.assertRaises(ValidationError):
            self.env['warehouse.cold.store'].create({
                'rack_count': 2,
                'column_count': 3,
                'row_count': 4,
                'height': 5.0,
                'width': 10.0,
                'length': 15.0,
                'temperature': -5.0,
                'humidity': 101.0,  # Invalid humidity
            })