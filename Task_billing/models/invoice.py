from odoo import fields, models, api

class BillLine(models.Model):
    _name = "bill_line"
    _description = "Bill Line"

    bill_id = fields.Many2one('project.task', string="bill")
    product_id = fields.Many2one("product.product", string = "Product")
    quantity = fields.Float(string= "Quantity", default = "1.0")
    price_unit = fields.Float(string="Price")
    name = fields.Char(string='Label', compute='_compute_name', store=True)
    tax_ids = fields.Many2many("account.tax" , string="Taxes")
    price_subtotal = fields.Float(string="Tax excl.", compute="_compute_price_subtotal", store=True)

    @api.depends('product_id')
    def _compute_name(self):
        for line in self:
            line.name = line.product_id.name        

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:                     
            self.price_unit = self.product_id.list_price
            self.tax_ids = self.product_id.taxes_id
    
    @api.depends('quantity', 'price_unit')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.quantity * line.price_unit

class BillProdcut(models.Model):
    _inherit = "product.product"
