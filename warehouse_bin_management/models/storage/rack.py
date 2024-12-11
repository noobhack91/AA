from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Rack(models.Model):
    _name = 'warehouse.rack'
    _inherit = ['base.mixin', 'dimension.mixin', 'naming.mixin']
    _description = 'Rack'
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Rack name must be unique!')
    ]

    cold_store_id = fields.Many2one('warehouse.cold.store', string='Cold Store')
    column_count = fields.Integer('Number of Columns', required=True)
    row_count = fields.Integer('Number of Rows', required=True)
    section_ids = fields.One2many('warehouse.rack.section', 'rack_id', string='Sections')
    material = fields.Selection([
        ('steel', 'Steel'),
        ('aluminum', 'Aluminum'),
        ('wood', 'Wood')
    ], string='Material', required=True)
    max_weight_capacity = fields.Float('Maximum Weight Capacity (kg)', required=True)

    def _generate_name(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('rack.sequence')
        if vals.get('cold_store_id'):
            cold_store = self.env['warehouse.cold.store'].browse(vals['cold_store_id'])
            return f'{cold_store.name}_R{sequence}'
        return f'R{sequence}'

    @api.model
    def create(self, vals):
        rack = super().create(vals)
        rack._create_sections()
        return rack

    def _create_sections(self):
        for rack in self:
            section_height = rack.height / rack.row_count
            section_width = rack.width / rack.column_count
            
            for column in range(1, rack.column_count + 1):
                for row in range(1, rack.row_count + 1):
                    self.env['warehouse.rack.section'].create({
                        'rack_id': rack.id,
                        'column_number': column,
                        'row_number': row,
                        'height': section_height,
                        'width': section_width,
                        'length': rack.length,
                    })

    @api.constrains('column_count', 'row_count', 'max_weight_capacity')
    def _check_constraints(self):
        for record in self:
            if any(count <= 0 for count in [record.column_count, record.row_count]):
                raise ValidationError('Column count and row count must be positive numbers.')
            if record.max_weight_capacity <= 0:
                raise ValidationError('Maximum weight capacity must be greater than zero.')