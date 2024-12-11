from odoo import models, fields, api

class RackSection(models.Model):
    _name = 'warehouse.rack.section'
    _inherit = ['bin.location.mixin']
    _description = 'Rack Section'
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Rack Section name must be unique!')
    ]

    rack_id = fields.Many2one('warehouse.rack', string='Rack', required=True, ondelete='cascade')
    column_number = fields.Integer('Column Number', required=True)
    row_number = fields.Integer('Row Number', required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self._generate_name(vals['rack_id'], vals['column_number'], vals['row_number'])
        return super().create(vals)

    def _generate_name(self, rack_id, column_number, row_number):
        rack = self.env['warehouse.rack'].browse(rack_id)
        return f'{rack.name}_C{str(column_number).zfill(2)}_L{str(row_number).zfill(2)}'