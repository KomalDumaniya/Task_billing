from odoo import api, _, fields, models 
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

class AccountMove(models.Model):
    _inherit = 'account.move'

    task_id = fields.Many2one('project.task', string='Task')

class ProjectTask(models.Model):
    _inherit = 'project.task'

    invoice_date = fields.Date(string='Bill Date')
    vendor_id = fields.Many2one('res.partner', string='Vendor')
    bill_line_ids = fields.One2many('bill_line', 'bill_id', string="Ticket Lines")
    bill_created = fields.Boolean(string='Bill Created', default=False)
    created_bill_id = fields.Many2one('account.move', string='Created Bill')
    bill_refund = fields.Boolean(string='Bill Refunded', default=False)
    bill_count = fields.Integer(string='Bill', compute='_compute_bill_count')
    status = fields.Selection(
        selection = [('To Do','To Do'),
                     ('In Progress','In Progress'),
                     ('Canceled','Canceled'),
                     ('Done','Done')], 
        string ="status",default = 'To Do') 

    def _compute_bill_count(self):
        for task in self:
            task.bill_count = self.env['account.move'].search_count([('task_id', '=', task.id),('state', '!=', 'cancel')])

    def action_view_bills(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bills',
            'res_model': 'account.move',
            'view_mode': 'form',  
            'domain': [
                    ('task_id', '=', self.id),
                    ('state', '!=', 'cancel')
                ],
            'res_id': self.created_bill_id.id, 
            'context': {'form_view_initial_mode': 'edit'}, 
        }

    def action_cancel_bill(self):
        self.ensure_one()
        if self.created_bill_id.payment_state == 'paid':
            self.bill_refund = True
        else:
            self.created_bill_id.button_cancel()
            self.bill_created = False
            self.bill_refund = False

            return {
                'type': 'ir.actions.act_window',
            }

    @api.onchange('status')
    def _onchange_status(self):
        if self.status == 'Canceled':
            self.action_cancel_bill()

    def action_refund_bills(self):
        self.ensure_one()
        if self.created_bill_id.state != 'posted':
            raise UserError('Cannot refund the bill because it is not posted.')

        refund_move = self.created_bill_id._reverse_moves([{'move_type': 'in_refund'}])
        self.bill_refund = True  

        return {
            'type': 'ir.actions.act_window',
            'name': 'Refund Bill',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': refund_move.id,
            'target': 'new',
        }

    def action_create_bill(self):
        self.ensure_one()
        if not self.invoice_date:
            raise UserError('Please set the bill date.')
        if not self.vendor_id:
            raise UserError('Please set the vendor.')
        if not self.bill_line_ids:
            raise UserError('Please add invoice line.')

        move_vals = {
            'move_type': 'in_invoice',
            'invoice_date': self.invoice_date,
            'partner_id': self.vendor_id.id,
            'task_id': self.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'price_unit': line.price_unit,
                }) for line in self.bill_line_ids],
        }
        move = self.env['account.move'].create(move_vals)
        
        move.action_post()
        self.bill_created = True
        self.created_bill_id = move.id

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'info',
                'title': _('Bill Created'),
                'message': _('Your bill has been created and confirmed successfully.'),
                'next': {'type': 'ir.actions.act_window_close'},
            },
        }

