from odoo.exceptions import ValidationError

def validate_positive_number(value, field_name):
    """Validate that a number is positive."""
    if value <= 0:
        raise ValidationError(f'{field_name} must be a positive number.')

def validate_range(value, min_val, max_val, field_name):
    """Validate that a number is within a specified range."""
    if not min_val <= value <= max_val:
        raise ValidationError(f'{field_name} must be between {min_val} and {max_val}.')