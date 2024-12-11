from odoo import models, fields, api

class SequenceMixin(models.AbstractModel):
    _name = 'sequence.mixin'
    _description = 'Sequence Generation Mixin'

    name = fields.Char('Name', required=True, readonly=True, copy=False)
    sequence_number = fields.Integer('Sequence Number', readonly=True, copy=False)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            sequence_code = self._get_sequence_code()
            sequence = self.env['ir.sequence'].next_by_code(sequence_code)
            vals['name'] = self._format_name(sequence)
            vals['sequence_number'] = int(sequence)
        return super().create(vals)

    def _get_sequence_code(self):
        """To be implemented by inheriting models"""
        return False

    def _format_name(self, sequence):
        """To be implemented by inheriting models"""
        return sequence