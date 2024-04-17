# -*- coding: utf-8 -*-
################################################################################

#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Fouzan M(Contact : odoo@cybrosys.com)
#
#    This program is under the terms of the Odoo Proprietary License v1.0
#    (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the
#    Software or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#    OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
#    USE OR OTHER DEALINGS IN THE SOFTWARE.
#
################################################################################
from odoo import _, models
from odoo.tools import formatLang


class AccountMove(models.Model):
    """to add blocking credit limit in credit limit message"""
    _inherit = 'account.move'

    def _build_credit_warning_message(self, record, current_amount=0.0,
                                      exclude_current=False):
        """to add blocking credit limit in credit limit warning message"""

        msg = super()._build_credit_warning_message(record, current_amount=0.0,
                                                    exclude_current=False)
        partner_id = record.partner_id.commercial_partner_id
        credit_to_invoice = max(partner_id.credit_to_invoice - (
            current_amount if exclude_current else 0), 0)
        total_credit = partner_id.credit + credit_to_invoice + current_amount
        partner_id.credit_amount = total_credit
        if msg and 'this document' not in msg and current_amount:
            msg += _('\nTotal amount due (including this document) : %s',
                     formatLang(self.env, total_credit,
                                currency_obj=record.company_id.
                                currency_id))
        if msg and total_credit > partner_id.blocking_credit_limit != 0:
            msg += _('\nThe allowed Credit Limit is : %s',
                     formatLang(self.env, partner_id.blocking_credit_limit,
                                currency_obj=record.company_id.
                                currency_id))
        elif msg and total_credit > partner_id.credit_limit and \
                partner_id.blocking_credit_limit != 0:
            msg += _('\nThe Credit will be blocked at: %s',
                     formatLang(self.env, partner_id.blocking_credit_limit,
                                currency_obj=record.company_id.
                                currency_id))
        return msg
