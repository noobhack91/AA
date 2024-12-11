from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestBinLocations(TransactionCase):
    def setUp(self):
        super().setUp()
        self.cold_store = self.env['warehouse.cold.store'].create({
            'rack_count': 2,
            'column_count': 3,
            'row_count': 4,
            'height': 5.0,
            'width': 10.0,
            'length': 15.0,
        })
        
        self.fridge = self.env['warehouse.fridge'].create({
            'height': 2.0,
            'width': 1.0,
            'length': 1.5,
        })
        
        self.rack = self.env['warehouse.rack'].create({
            'column_count': 3,
            'row_count': 4,
            'height': 4.0,
            'width': 8.0,
            'length': 12.0,
        })

    def test_cold_store_creation(self):
        self.assertTrue(self.cold_store.name.startswith('CS'))
        self.assertEqual(len(self.cold_store.rack_ids), self.cold_store.rack_count)

    def test_fridge_creation(self):
        self.assertTrue(self.fridge.name.startswith('F'))

    def test_rack_creation(self):
        self.assertTrue(self.rack.name.startswith('R'))
        self.assertEqual(
            len(self.rack.section_ids),
            self.rack.column_count * self.rack.row_count
        )

    def test_rack_section_naming(self):
        section = self.rack.section_ids[0]
        expected_format = f"{self.rack.name}_C{str(section.column_number).zfill(2)}_L{str(section.row_number).zfill(2)}"
        self.assertEqual(section.name, expected_format)

    def test_negative_dimensions(self):
        with self.assertRaises(ValidationError):
            self.env['warehouse.cold.store'].create({
                'rack_count': 2,
                'column_count': 3,
                'row_count': 4,
                'height': -5.0,
                'width': 10.0,
                'length': 15.0,
            })

    def test_negative_counts(self):
        with self.assertRaises(ValidationError):
            self.env['warehouse.cold.store'].create({
                'rack_count': -2,
                'column_count': 3,
                'row_count': 4,
                'height': 5.0,
                'width': 10.0,
                'length': 15.0,
            })