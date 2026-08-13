from odoo import models,fields,api
from odoo.exceptions import ValidationError,UserError

class ElectronicProductBrand(models.Model):
    _name = "electronic.product.brand"
    _description = "Table for electronics gadgets brands"

    name = fields.Char("Brand Name", size=64, required=True)
    code = fields.Char("Code", size=64, required=True)
    logo = fields.Binary("Logo")
    partner_id = fields.Many2one('res.partner',string="Manufacturer Partner")
    manufacturer_warranty_months = fields.Integer(
        string="Standard Warranty (Months)",
        default=12,
        help="Standard warranty provided by brand/OEM on devices in months."
    )
    carrier_warranty_months = fields.Integer(
        string="Carrier Warranty (Months)",
        default=0,
        help="Default carrier or network provider warranty period in months."
    )
    accessory_warranty_months = fields.Integer(
        string="Accessory Warranty (Months)",
        default=3,
        help="Warranty duration in months for in-box accessories (e.g., charger, cable, earphones)."
    )
    repair_productivity_minutes = fields.Integer(
        string="Standard Repair Time (Mins)",
        default=60,
        help="Target labor/turnaround time allocated for standard repairs on this category."
    )
    repeat_repair_period_days = fields.Integer(
        string="Repeat Repair Window (Days)",
        default=30,
        help="Time window in days to flag a bounce or repeat repair for the same IMEI/Serial."
    )

    required_imeino = fields.Boolean(        
        string="IMEI Required",
        default=False,
        help="Specify if IMEI entry is mandatory during intake for devices under this brand."
    )
    required_serial_no = fields.Boolean(        
        string="Serial No Required", 
        default=False,  # Fixed: Added missing comma
        help="Mandates entering a device serial number during job intake for tracking and warranty validation."
    )
    required_fault_code = fields.Boolean(        
        string="Fault Code Required", 
        default=False,  # Fixed: Added missing comma
        help="Requires technicians to select a standardized diagnostic fault code before proceeding with repair."
    )
    required_firmware = fields.Boolean(        
        string="Firmware Version Required", 
        default=False,
        help="Mandates recording the current software/firmware version installed on the device at intake."
    )

    # Technical & Component Requirements
    require_part_no = fields.Boolean(
        string='Require Part Number', 
        default=False,
        help="Forces technicians to specify exact spare part numbers used for replacement items."
    )
    require_circuit_ref = fields.Boolean(
        string='Require Circuit Reference', 
        default=False,
        help="Mandates capturing board-level circuit schematic references (e.g., C102, R405) for micro-soldering/motherboard repairs."
    )

    # QA & Intake Workflow
    use_qa = fields.Boolean(
        string='Enable QA Audit Stage', 
        default=False,
        help="Enables a mandatory Quality Assurance audit inspection stage before the repair order can be closed."
    )
    complete_on_qa_pass = fields.Boolean(
        string='Auto-Complete on QA Pass', 
        default=False,
        help="Automatically transitions the repair order status to 'Done' as soon as QA inspection passes."
    )
    force_booking_symptom = fields.Boolean(
        string='Force Booking Symptom', 
        default=False,
        help="Requires intake agents to record at least one customer-reported symptom before creating the job."
    )

    active = fields.Boolean(string="Active", default=True)

    _unique_manufacturer_code = models.UniqueIndex("code",message="The Brand Code must be unique!")
    _index_name_idx = models.Index("name")
    _index_code_idx = models.Index("code")
