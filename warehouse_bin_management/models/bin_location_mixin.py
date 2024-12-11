from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BinLocationMixin(models.AbstractModel):
    _name = 'bin.location.mixin'
    _description = 'Bin Location Mixin'

    name = fields.Char('Name', required=True, readonly=True)
    height = fields.Float('Height (m)', required=True)
    width = fields.Float('Width (m)', required=True)
    length = fields.Float('Length (m)', required=True)
    active = fields.Boolean(default=True)

    @api.constrains('height', 'width', 'length')
    def _check_dimensions(self):
        for record in self:
            if any(dim <= 0 for dim in [record.height, record.width, record.length]):
                raise ValidationError('All dimensions must be positive numbers.')