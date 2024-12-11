from odoo import models, fields, api
from odoo.exceptions import ValidationError

class StorageLocation(models.Model):
    _name = 'warehouse.storage.location'
    _inherit = ['sequence.mixin']
    _description = 'Storage Location'

    location_type_id = fields.Many2one('warehouse.location.type', string='Location Type', required=True)
    height = fields.Float('Height (m)', required=True)
    width = fields.Float('Width (m)', required=True)
    length = fields.Float('Length (m)', required=True)
    active = fields.Boolean('Active', default=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    notes = fields.Text('Notes')

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Storage location name must be unique!')
    ]

    @api.constrains('height', 'width', 'length')
    def _check_dimensions(self):
        for record in self:
            if any(dim <= 0 for dim in [record.height, record.width, record.length]):
                raise ValidationError('All dimensions must be positive numbers.')

    def _get_sequence_code(self):
        self.ensure_one()
        return f"{self.location_type_id.code}.sequence"

    def _format_name(self, sequence):
        self.ensure_one()
        return f"{self.location_type_id.code}{sequence}"