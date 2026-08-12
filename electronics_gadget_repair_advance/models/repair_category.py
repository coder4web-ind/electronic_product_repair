from odoo import models,fields,api
from odoo.exceptions import ValidationError,UserError

REQUIRE_SELECTION = [
    ("parent", "Use Parent/Brand Default"),
    ("yes", "Required"),
    ("no", "Not Required"),
]

class ProductCategory(models.Model):
    _inherit = "product.category"

    is_device_category = fields.Boolean(
        string="Is Device Category",
        default=False,
        help="Check this if this category represents repairable hardware/devices.",
    )

    required_imeino = fields.Selection(
           REQUIRE_SELECTION,
           string="IMEI Required",
           default="parent",
       )
    required_serial_no = fields.Selection(
        REQUIRE_SELECTION,
        string="Serial No Required", 
        default="parent",
    )
    require_fault_code = fields.Selection(
        selection=REQUIRE_SELECTION,
        string="Require Fault Code",
        default="parent",
        required=True,
    )

    dop_warranty_months = fields.Integer(
        string="Warranty from DOP (Months)",
        help="Default warranty duration based on Date of Purchase.",
    )
    production_warranty_months = fields.Integer(
        string="Warranty from Production (Months)",
        help="Fallback warranty duration based on Manufacturing Date.",
    )
    default_tat_hours = fields.Integer(
        string="Target SLA (Hours)",
        help="Default Turnaround Time target for repairs in this category.",
    )

    
    @api.constrains("parent_id", "is_device_category")
    def _check_goods_hierarchy(self):
        goods_category = self.env["product.category"].search(
            [("name", "=", "Goods")], limit=1
        )

        if not goods_category:
            return 

        for record in self:            
            if record.id == goods_category.id:
                continue

            
            curr = record.parent_id
            is_under_goods = False
            while curr:
                if curr.id == goods_category.id:
                    is_under_goods = True
                    break
                curr = curr.parent_id

            
            if record.is_device_category and not is_under_goods:
                raise ValidationError(
                    f"Invalid Parent for Device Category '{record.name}'!\n\n"
                    f"Device categories must be nested under 'Goods' "
                    f"(e.g., Goods -> {record.name} OR Goods -> Electronics -> {record.name})."
                )

            
            if not record.is_device_category and is_under_goods:
                raise ValidationError(
                    f"Invalid Parent for Category '{record.name}'!\n\n"
                    f"Standard product or service categories cannot be nested under 'Goods'. "
                    f"Please select a non-Goods parent category (e.g., Services)."
                )