from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DimensionMixin(models.AbstractModel):
    _name = 'dimension.mixin'
    _description = 'Dimension Mixin'

    height = fields.Float('Height (m)', required=True)
    width = fields.Float('Width (m)', required=True)
    length = fields.Float('Length (m)', required=True)

    @api.constrains('height', 'width', 'length')
    def _check_dimensions(self):
        for record in self:
            if any(dim <= 0 for dim in [record.height, record.width, record.length]):
                raise ValidationError('All dimensions must be positive numbers.')