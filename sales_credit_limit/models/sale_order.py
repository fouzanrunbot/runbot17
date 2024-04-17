from odoo import _, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    """to include a blocking order error upon order confirmation"""
    _inherit = 'sale.order'

    def action_confirm(self):
        """Block the order if the selected customer's due amount exceeds
         the blocking limit."""
        partner = self.partner_id.parent_id if self.partner_id.parent_id else\
            self.partner_id
        if partner.credit_amount > \
                partner.blocking_credit_limit != 0:
            raise UserError(_("%s has reached the maximum allowed Credit Limit."
                              , self.partner_id.name))
        return super().action_confirm()
