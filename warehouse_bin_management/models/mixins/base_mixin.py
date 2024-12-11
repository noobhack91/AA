from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BaseMixin(models.AbstractModel):
    _name = 'base.mixin'
    _description = 'Base Mixin'

    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    created_date = fields.Datetime('Created Date', default=fields.Datetime.now, readonly=True)
    updated_date = fields.Datetime('Updated Date', default=fields.Datetime.now, readonly=True)

    def write(self, vals):
        vals['updated_date'] = fields.Datetime.now()
        return super().write(vals)