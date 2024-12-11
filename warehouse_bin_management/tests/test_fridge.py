from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestFridge(TransactionCase):
    def setUp(self):
        super().setUp()
        self.fridge = self.env['warehouse.fridge'].create({
            'height': 2.0,
            'width': 1.0,
            'length': 1.5,
            'temperature': 4.0,
            'power_rating': 0.75,
            'has_display': True,
            'display_type': 'lcd',
        })

    def test_name_generation(self):
        self.assertTrue(self.fridge.name.startswith('F'))
        self.assertEqual(len(self.fridge.name), 4)  # F + 3 digits

    def test_invalid_temperature(self):
        with self.assertRaises(ValidationError):
            self.env['warehouse.fridge'].create({
                'height': 2.0,
                'width': 1.0,
                'length': 1.5,
                'temperature': 15.0,  # Invalid temperature
                'power_rating': 0.75,
            })

    def test_display_type_constraint(self):
        fridge = self.env['warehouse.fridge'].create({
            'height': 2.0,
            'width': 1.0,
            'length': 1.5,
            'temperature': 4.0,
            'power_rating': 0.75,
            'has_display': False,
        })
        self.assertFalse(fridge.display_type, "Display type should be empty when has_display is False")