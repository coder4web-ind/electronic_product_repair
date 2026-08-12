from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

PRODUCT_CONDITION = [
    ("good", "Good Condition"),
    ("fair", "Little Scratches"),
    ("poor", "Poor Condition"),
    ("extreme", "Extremely Poor"),
    ("dead", "Dead Device (No Power)"),
]


class RepairOrder(models.Model):
    _inherit = "repair.order"

    partner_id = fields.Many2one(
        'res.partner', 'Customer',
        index=True, 
        check_company=True, 
        change_default=True, 
        compute='_compute_partner_id', 
        readonly=False, 
        store=True,
        domain="[('user_ids', '=', False)]",
        help='Choose partner for whom the order will be invoiced and delivered.'
    )

    brand_id = fields.Many2one(
        "repair.device.brand",
        string="Brand",
        help="e.g., Apple, Samsung, Xiaomi",
    )

    allowed_category_ids = fields.Many2many(
        "product.category",
        compute="_compute_allowed_category_ids",
        string="Allowed Unit Types",
    )
    
    category_id = fields.Many2one(
        "product.category",
        string="Device Category",
        domain="[('id', 'in', allowed_category_ids)]",
        help="Select category under Goods (e.g., Smartphones, Tablets, Laptops)",
    )
    
    device_id = fields.Many2one(
        "product.template",
        string="Device",
        domain="[('repair_brand_id', '=', brand_id), ('categ_id', '=', category_id)]",
    )

    job_summary = fields.Text(string="Reported Fault in Device")

    device_condition = fields.Selection(
        selection=PRODUCT_CONDITION,
        string="Device Condition",
    )

    # Computed fields (Unstored)
    required_imei = fields.Boolean(
        compute="_compute_imei_serial_required",
        store=False,
    )

    required_serial = fields.Boolean(
        compute="_compute_imei_serial_required",
        store=False,
    )

    # Computed field (Stored - separate compute method to prevent registry mismatch)
    required_qa = fields.Boolean(
        compute="_compute_required_qa",
        store=True,
    )

    imei = fields.Char("IMEI", size=16, tracking=True)
    serial = fields.Char("Serial No", size=64, tracking=True)

    @staticmethod
    def _imei_luhn_is_valid(value):
        if not value:
            return False

        digits = [int(ch) for ch in value if ch.isdigit()]
        if len(digits) not in (14, 15, 16):
            return False

        checksum = 0
        for idx, digit in enumerate(digits):
            if idx % 2 == 1:
                doubled = digit * 2
                checksum += doubled - 9 if doubled > 9 else doubled
            else:
                checksum += digit

        return checksum % 10 == 0

    @api.depends("brand_id")
    def _compute_allowed_category_ids(self):
        for rec in self:
            if rec.brand_id:
                matching_devices = self.env["product.template"].search(
                    [("repair_brand_id", "=", rec.brand_id.id)]
                )
                rec.allowed_category_ids = matching_devices.mapped("categ_id")
            else:
                goods_cat = self.env["product.category"].search(
                    [("name", "=", "Goods")], limit=1
                )
                if goods_cat:
                    rec.allowed_category_ids = self.env["product.category"].search(
                        [("id", "child_of", goods_cat.id)]
                    )
                else:
                    rec.allowed_category_ids = False

    @api.onchange("brand_id")
    def _onchange_reset_children(self):
        self.category_id = False
        self.device_id = False

    @api.onchange("category_id")
    def _onchange_category_reset_device(self):
        self.device_id = False

    @api.depends('brand_id', 'category_id', 'device_id')
    def _compute_imei_serial_required(self):
        for record in self:
            imei_setting = record.device_id.required_imei if record.device_id else 'parent'
            serial_setting = record.device_id.required_serial_no if record.device_id else 'parent'

            if imei_setting == 'parent' and record.category_id:
                imei_setting = record.category_id.required_imeino 

            if imei_setting == 'parent' and record.brand_id:
                imei_setting = record.brand_id.required_imeino 

            if serial_setting == 'parent' and record.category_id:
                serial_setting = record.category_id.required_serial_no 

            if serial_setting == 'parent' and record.brand_id:
                serial_setting = record.brand_id.required_serial_no 

            record.required_imei = (imei_setting == 'yes')
            record.required_serial = (serial_setting == 'yes')

    @api.depends('brand_id')
    def _compute_required_qa(self):
        for record in self:
            record.required_qa = bool(record.brand_id and record.brand_id.use_qa)

    @api.constrains('imei')
    def _check_imei_luhn(self):
        for record in self:
            if record.imei:
                imei_val = record.imei.strip().replace(' ', '').replace('-', '')
                if not self._imei_luhn_is_valid(imei_val):
                    raise ValidationError(
                        _("The IMEI '%s' is not valid. Please enter a correct IMEI using the Luhn checksum.", record.imei)
                    )