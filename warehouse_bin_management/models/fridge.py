from odoo import models, fields, api

class Fridge(models.Model):
    _name = 'warehouse.fridge'
    _inherit = ['bin.location.mixin']
    _description = 'Fridge'
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Fridge name must be unique!')
    ]

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self._generate_name()
        return super().create(vals)

    def _generate_name(self):
        sequence = self.env['ir.sequence'].next_by_code('fridge.sequence')
        return f'F{sequence}'