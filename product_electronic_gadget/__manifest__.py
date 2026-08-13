{
    "name": "Product Electronic Gadget",
    "version": "19.0.1.0.0",
    "category": "Inventory/Product",
    'author': 'Coder4Web, Odoo Community Association (OCA)',
    "website": "https://github.com/coder4web-ind",
    "license": "LGPL-3",
    "development_status": "Beta",  # Alpha, Beta, Production/Stable
    "maintainers": ["coder4web-ind"],
    "depends": ["product"],
    "data": [
        "security/ir.model.access.csv",
        "views/electronic_product_brand.xml",
        "views/electronic_product_category.xml",
        "views/electronic_product_device.xml"
    ],
    "installable": True,
} 