# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def compute_due_amount(self):
        for rec in self:
            if not rec.id:
                continue
            debit_amount = rec.debit
            credit_amount = rec.credit
            rec.due_amount = credit_amount - debit_amount

    warning_stage = fields.Float(string='Monto Aviso', required=True,
                                 help="Mostrará un mensaje una vez el cliente haya alcanzado este monto."
                                      "Colocar el monto en 0.00 para deshabilitar esta función.")
    blocking_stage = fields.Float(string='Límite de Crédito', required=True,
                                  help="Se bloquearán las ventas a este cliente al llegar a este monto."
                                       "Colocar el monto en 0.00 para deshabilitar esta función.")
    due_amount = fields.Float(string="Total a Crédito", compute="compute_due_amount")
    active_limit = fields.Boolean("Habilitar Crédito", default=False)

    @api.constrains('warning_stage', 'blocking_stage')
    def constrains_warning_stage(self):
        if self.active_limit:
            if self.blocking_stage and self.warning_stage:
                if self.warning_stage >= self.blocking_stage:
                    raise UserError(_("El monto del Aviso debe ser menos al Límite de Crédito"))
            else:
                raise UserError(_("El monto del Aviso y Límite de Crédito deben ser mayores a 0."))


class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    is_cash = fields.Boolean(string="Es Contado", default=False, required=True)
    is_immediate = fields.Boolean("Es Inmediato", default=False)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    has_due = fields.Boolean()
    is_warning = fields.Boolean()
    partner_has_credit = fields.Boolean(related='partner_id.active_limit')
    due_amount = fields.Float(related='partner_id.due_amount')
    credit_limit = fields.Float(related='partner_id.blocking_stage')

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            if rec.partner_has_credit:
                return {'domain': {'payment_term_id': [(1, '=', 1)]}}
            else:
                return {'domain': {'payment_term_id': [('is_immediate', '=', True)]}}

    @api.model
    def _action_confirm(self):
        """To check the selected customers due amount is exceed than blocking stage"""
        if not self.payment_term_id.is_immediate and self.partner_id.active_limit:
            new_credit = self.due_amount + self.amount_total  #considera el monto del pedido actual para ver no sobrepase su crédito.
            if new_credit >= self.partner_id.blocking_stage:
                raise UserError(f"Este cliente ha alcanzado su límite de Crédito. "
                                f"Tiene {self.due_amount} a pagar")
            else:
                res = super(SaleOrder, self)._action_confirm()
                return res
        else:
            res = super(SaleOrder, self)._action_confirm()
            return res

    @api.onchange('partner_id')
    def check_due(self):
        """To show the due amount and warning stage"""
        if self.partner_id and self.partner_id.due_amount > 0:
            self.has_due = True
        else:
            self.has_due = False
        if self.partner_id and self.partner_id.active_limit:
            if self.due_amount >= self.partner_id.warning_stage:
                if self.partner_id.warning_stage != 0:
                    self.is_warning = True
        else:
            self.is_warning = False
