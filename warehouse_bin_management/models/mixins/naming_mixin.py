from odoo import models, fields, api

class NamingMixin(models.AbstractModel):
    _name = 'naming.mixin'
    _description = 'Naming Mixin'

    name = fields.Char('Name', readonly=True, copy=False)
    code = fields.Char('Code', readonly=True, copy=False)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self._generate_name(vals)
            vals['code'] = vals['name']
        return super().create(vals)

    def _generate_name(self, vals):
        """To be implemented by inheriting models"""
        return False