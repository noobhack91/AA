from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ColdStore(models.Model):
    _name = 'warehouse.cold.store'
    _inherit = ['base.mixin', 'dimension.mixin', 'naming.mixin']
    _description = 'Cold Store'
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Cold Store name must be unique!')
    ]

    rack_count = fields.Integer('Number of Racks', required=True)
    column_count = fields.Integer('Columns per Rack', required=True)
    row_count = fields.Integer('Rows per Rack', required=True)
    rack_ids = fields.One2many('warehouse.rack', 'cold_store_id', string='Racks')
    temperature = fields.Float('Temperature (°C)', required=True)
    humidity = fields.Float('Humidity (%)', required=True)

    def _generate_name(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('cold.store.sequence')
        return f'CS{sequence}'

    @api.constrains('rack_count', 'column_count', 'row_count')
    def _check_counts(self):
        for record in self:
            if any(count <= 0 for count in [record.rack_count, record.column_count, record.row_count]):
                raise ValidationError('Rack count, column count, and row count must be positive numbers.')

    @api.constrains('temperature', 'humidity')
    def _check_environment(self):
        for record in self:
            if not -30 <= record.temperature <= 30:
                raise ValidationError('Temperature must be between -30°C and 30°C')
            if not 0 <= record.humidity <= 100:
                raise ValidationError('Humidity must be between 0% and 100%')

    @api.model
    def create(self, vals):
        # Create the cold store
        cold_store = super().create(vals)
        
        # Create associated racks
        for i in range(cold_store.rack_count):
            self.env['warehouse.rack'].create({
                'cold_store_id': cold_store.id,
                'column_count': cold_store.column_count,
                'row_count': cold_store.row_count,
                'height': cold_store.height / cold_store.row_count,
                'width': cold_store.width / cold_store.column_count,
                'length': cold_store.length,
                'material': 'steel',  # Default material
                'max_weight_capacity': 1000.0,  # Default capacity
            })
        
        return cold_store