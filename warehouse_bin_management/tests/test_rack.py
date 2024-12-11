from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestRack(TransactionCase):
    def setUp(self):
        super().setUp()
        self.rack = self.env['warehouse.rack'].create({
            'column_count': 3,
            'row_count': 4,
            'height': 4.0,
            'width': 8.0,
            'length': 12.0,
            'material': 'steel',
            'max_weight_capacity': 1000.0,
        })

    def test_name_generation(self):
        self.assertTrue(self.rack.name.startswith('R'))
        
        # Test rack in cold store
        cold_store = self.env['warehouse.cold.store'].create({
            'rack_count': 1,
            'column_count': 3,
            'row_count': 4,
            'height': 5.0,
            'width': 10.0,
            'length': 15.0,
            'temperature': -5.0,
            'humidity': 60.0,
        })
        
        rack_in_store = self.env['warehouse.rack'].create({
            'cold_store_id': cold_store.id,
            'column_count': 3,
            'row_count': 4,
            'height': 4.0,
            'width': 8.0,
            'length': 12.0,
            'material': 'steel',
            'max_weight_capacity': 1000.0,
        })
        self.assertTrue('_R' in rack_in_store.name)

    def test_section_creation(self):
        self.assertEqual(
            len(self.rack.section_ids),
            self.rack.column_count * self.rack.row_count
        )

    def test_invalid_weight_capacity(self):
        with self.assertRaises(ValidationError):
            self.env['warehouse.rack'].create({
                'column_count': 3,
                'row_count': 4,
                'height': 4.0,
                'width': 8.0,
                'length': 12.0,
                'material': 'steel',
                'max_weight_capacity': -100.0,  # Invalid weight capacity
            })