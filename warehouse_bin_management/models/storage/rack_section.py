from odoo import models, fields, api

class RackSection(models.Model):
    _name = 'warehouse.rack.section'
    _inherit = ['base.mixin', 'dimension.mixin', 'naming.mixin']
    _description = 'Rack Section'
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Rack Section name must be unique!')
    ]

    rack_id = fields.Many2one('warehouse.rack', string='Rack', required=True, ondelete='cascade')
    column_number = fields.Integer('Column Number', required=True)
    row_number = fields.Integer('Row Number', required=True)
    current_weight = fields.Float('Current Weight (kg)', default=0.0)
    is_occupied = fields.Boolean('Is Occupied', default=False)
    last_inventory_date = fields.Date('Last Inventory Date')
    status = fields.Selection([
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('maintenance', 'Under Maintenance')
    ], string='Status', default='available', required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self._generate_name(vals['rack_id'], vals['column_number'], vals['row_number'])
            vals['code'] = vals['name']
        return super().create(vals)

    def _generate_name(self, rack_id, column_number, row_number):
        rack = self.env['warehouse.rack'].browse(rack_id)
        return f'{rack.name}_C{str(column_number).zfill(2)}_L{str(row_number).zfill(2)}'

    @api.constrains('current_weight')
    def _check_weight(self):
        for record in self:
            max_weight = record.rack_id.max_weight_capacity / (record.rack_id.column_count * record.rack_id.row_count)
            if record.current_weight > max_weight:
                raise ValidationError(f'Current weight exceeds maximum capacity of {max_weight} kg for this section.')