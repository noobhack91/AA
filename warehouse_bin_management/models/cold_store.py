from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ColdStore(models.Model):
    _name = 'warehouse.cold.store'
    _inherit = ['bin.location.mixin']
    _description = 'Cold Store'
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Cold Store name must be unique!')
    ]

    rack_count = fields.Integer('Number of Racks', required=True)
    column_count = fields.Integer('Columns per Rack', required=True)
    row_count = fields.Integer('Rows per Rack', required=True)
    rack_ids = fields.One2many('warehouse.rack', 'cold_store_id', string='Racks')

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self._generate_name()
        return super().create(vals)

    def _generate_name(self):
        sequence = self.env['ir.sequence'].next_by_code('cold.store.sequence')
        return f'CS{sequence}'

    @api.constrains('rack_count', 'column_count', 'row_count')
    def _check_counts(self):
        for record in self:
            if any(count <= 0 for count in [record.rack_count, record.column_count, record.row_count]):
                raise ValidationError('Rack count, column count, and row count must be positive numbers.')