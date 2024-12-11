{
    'name': 'Warehouse Bin Management',
    'version': '17.0.1.0.0',
    'category': 'Warehouse',
    'summary': 'Manage warehouse bin locations including Cold Stores, Fridges, and Racks',
    'description': """
        This module provides functionality to manage warehouse bin locations:
        * Cold Store management
        * Fridge management
        * Rack and Rack Section management
        * Automated naming conventions
        * Input validation
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'stock'],
    'data': [
        'security/warehouse_security.xml',
        'security/ir.model.access.csv',
        'data/ir.sequence.xml',
        'views/cold_store_views.xml',
        'views/fridge_views.xml',
        'views/rack_views.xml',
        'views/rack_section_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}