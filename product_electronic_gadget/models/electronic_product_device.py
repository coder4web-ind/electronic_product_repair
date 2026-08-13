from odoo import fields, models

REQUIRE_SELECTION = [
    ("parent", "Use Parent/Brand Default"),
    ("yes", "Required"),
    ("no", "Not Required"),
]


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_brand_id = fields.Many2one(
        comodel_name="electronic.product.brand",
        string="Device Brand",
        index=True,
    )
    main_board_part_no = fields.Char(string="Mainboard Part Number")
    pdf_service_manual = fields.Binary(
        string="Service Manual PDF",
        attachment=True,
    )
    sim_card_type = fields.Selection(
        selection=[
            ("none", "None / N/A"),
            ("standard", "Standard Physical SIM"),
            ("esim", "eSIM Only"),
            ("both", "Physical SIM & eSIM"),
        ],
        string="SIM Card Type",
        default="none",
    )
    required_imei = fields.Selection(
        selection=REQUIRE_SELECTION,
        string="IMEI Required",
        default="parent",
    )
    required_serial_no = fields.Selection(
        selection=REQUIRE_SELECTION,
        string="Serial No Required",
        default="parent",
    )

    serial_format = fields.Char(
        string="Serial No Format",
        help=(
            "Validation mask:\n"
            "A = Uppercase Letters (A-Z)\n"
            "N = Numbers (0-9)\n"
            "X = Alphanumeric (A-Z, 0-9)\n"
            "Example: 'C8QH6T96DPNG' -> 'ANAANANNAAAA'"
        ),
    )

    brand_warranty_months = fields.Integer(
        string="Brand Warranty (Months)",
        help="Leave 0 to inherit from Category / Brand default.",
    )
    carrier_warranty_months = fields.Integer(
        string="Carrier Warranty (Months)",
    )
    accessory_warranty_months = fields.Integer(
        string="Accessory Warranty (Months)",
    )