from odoo import models, fields

class LocationType(models.Model):
    _name = 'warehouse.location.type'
    _description = 'Warehouse Location Type'
    _order = 'sequence'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    sequence = fields.Integer('Sequence', default=10)
    active = fields.Boolean('Active', default=True)
    description = fields.Text('Description')
    
    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Location type code must be unique!')
    ]