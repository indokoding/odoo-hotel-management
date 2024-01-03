{
  'name': 'Hotel Management System',
  'version': '1.0.1',
  'summary': 'Manage rental products in the sales module',
  'description': 'This module allows you to manage rental products within the sales module of Odoo.',
  'category': 'Sales',
  'author': 'Your Name',
  'website': 'https://www.example.com',
  'license': 'LGPL-3',
  'depends': [
    "mail", 
    "sale",
    "purchase", 
    "account", 
    "website", 
    "website_sale"
  ],
  'sequence': 0,
  'data': [
    'data/sequence.xml',
    'data/hotel_room_data.xml',
    
    'security/ir.model.access.csv',
    
    'wizard/checkout_room_booking.xml',
    'wizard/checkin_room_booking.xml',
    'wizard/create_room_booking.xml',
    
    'views/room_views.xml',
    'views/product_views.xml',
    'views/amenity_views.xml',
    'views/book_history_views.xml',
    'views/dashboard_views.xml',
    'views/menu_views.xml',
    
  ],
  'installable': True,
  'auto_install': False,
  'application': True,
}
