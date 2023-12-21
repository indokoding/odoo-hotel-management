{
  'name': 'Hotel Management System',
  'version': '1.0.1',
  'summary': 'Manage rental products in the sales module',
  'description': 'This module allows you to manage rental products within the sales module of Odoo.',
  'category': 'Sales',
  'author': 'Your Name',
  'website': 'https://www.example.com',
  'license': 'LGPL-3',
  'depends': ["mail", "sale", "purchase", "account"],
  'sequence': 0,
  'data': [
    'security/ir.model.access.csv',
    
    'views/room_views.xml',
    'views/product_views.xml',
    'views/amenity_views.xml',
    'views/menu_views.xml',
  ],
  'installable': True,
  'auto_install': False,
  'application': True,
}
