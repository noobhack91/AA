from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Fridge(models.Model):
    _name = 'warehouse.fridge'
    _inherit = ['base.mixin', 'dimension.mixin', 'naming.mixin']
    _description = 'Fridge'
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Fridge name must be unique!')
    ]

    temperature = fields.Float('Temperature (°C)', required=True)
    power_rating = fields.Float('Power Rating (kW)', required=True)
    has_display = fields.Boolean('Has Display', default=False)
    display_type = fields.Selection([
        ('lcd', 'LCD'),
        ('led', 'LED'),
        ('digital', 'Digital')
    ], string='Display Type')

    def _generate_name(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('fridge.sequence')
        return f'F{sequence}'

    @api.constrains('temperature')
    def _check_temperature(self):
        for record in self:
            if not -30 <= record.temperature <= 10:
                raise ValidationError('Fridge temperature must be between -30°C and 10°C')