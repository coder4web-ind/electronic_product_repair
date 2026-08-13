# For my own shop and farm
{
    'name': 'Electroincs Gadget Repair',
    'summary': (
        'Streamlined device repair tracking compliant with EU Directive '
        '2024/1799 framework rules.'
    ),
    'version': '19.0.1.0.0',
    'category': 'Services',
    'author': 'Coder4Web, Odoo Community Association (OCA)',
    'website': 'https://github.com/coder4web-ind',  # Replace with the target OCA repo URL once agreed
    'description': """
Repair Clinics: Mobile & Cell Phone Repair Shop Management
==========================================================
A lightweight, fast, and mobile-responsive module built to manage independent device repair workflows.

Key Features & Keyword Indexing:
---------------------------------
* Mobile Repair & Cell Phone Repair Shop Optimization: Tailored for quick retail check-ins.
* Device Service Ticket Lifecycle: Seamless status updates for technicians on the shop floor.
* Hardware & IMEI Tracking: Log unique device identifiers effortlessly.
* Compliant with EU Directive 2024/1799 framework rules for consumer right-to-repair standards.
    """,
    'license': 'LGPL-3',
    'depends': [        
        'product_electronic_gadget',
        'repair'
        
    ],
    'data': [
        "security/ir.model.access.csv",
        "views/menu/disable_menu.xml",        
        "views/menu/repair_order_menu.xml"
    ],
    'demo': [],
    'images': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}