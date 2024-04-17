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
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    """to add blocking credit limit fields"""
    _inherit = 'res.partner'

    blocking_credit_limit = fields.Float(
        company_dependent=True, copy=False, readonly=False,
        groups='account.group_account_invoice,account.group_account_readonly',
        help="Cannot make sales once the selected customer is crossed blocking "
             "amount. Set it to 0 to disable the feature")
    partner_block_credit = fields.Boolean(
        groups='account.group_account_invoice,account.group_account_readonly',
        string="Partner Blocking Limit",
        help="option to select custom block credit limit",
        compute='_compute_partner_block_credit',
        inverse='_inverse_partner_block_credit')
    credit_amount = fields.Float(string='Partner Credit Amount',
                                 help="partner credit amount")

    @api.depends_context('company')
    def _compute_partner_block_credit(self):
        """to set custom partner credit limit option based on default blocking
        limit and partner credit limit"""
        for partner in self:
            company_limit = self.env['ir.property']._get(
                'blocking_credit_limit', 'res.partner')
            partner.partner_block_credit = partner.blocking_credit_limit != \
                                           company_limit

    def _inverse_partner_block_credit(self):
        """to get custom partner credit limit value"""
        for partner in self:
            if not partner.partner_block_credit:
                partner.blocking_credit_limit = self.env['ir.property']._get(
                    'blocking_credit_limit', 'res.partner')


    @api.model
    def _commercial_fields(self):
        """Overrides base method to include 'blocking_credit_limit'. and it
        returns extended list of commercial fields."""
        return super()._commercial_fields() +\
            ['blocking_credit_limit']

    @api.constrains('blocking_credit_limit', 'credit_limit')
    def validation_blocking_limit(self):
        """to validate blocking credit limit"""
        for partner in self:
            if partner.credit_limit > partner.blocking_credit_limit != 0:
                raise ValidationError(
                    _("Blocking Credit Limit must be greater than Credit Limit "
                      "or set Blocking Credit Limit as 0"))
