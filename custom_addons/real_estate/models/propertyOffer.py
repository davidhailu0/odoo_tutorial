from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import timedelta

import logging

_logger = logging.getLogger(__name__)

class TransientModel(models.TransientModel):
    _name = "transient.model.offer"
    _description = "This is description"
    _transient_max_count = 0 # 0 means unlimited
    _transient_max_hours = 0 # means unlimited

    @api.autovacuum
    def _transient_vacuum(self):
        pass

class AbstractOffer(models.AbstractModel):
    _name = "abstract.offer.model"
    _description = "This is an abstract model"

    partner_email = fields.Char("Email")
    partner_phone = fields.Char("Phone")


class PropertyOffer(models.Model):
    _name = "property.offer"
    _inherit = ['abstract.offer.model']
    _description = "offer for house property"

    @api.depends("partner_id", "property_id")
    def _compute_name(self):
        for rec in self:
            if rec.partner_id.name and rec.property_id.name:
                rec.name = f"{rec.property_id.name}-{rec.partner_id.name}"
            else:
                rec.name = False

    name = fields.Char("Name", compute="_compute_name")
    status = fields.Selection([('new', 'New'), ('accept', 'Accept'), ('refuse', 'Refuse'), ('cancel', 'Cancel')],
                              string="Status", default="new")
    price = fields.Float("Price")
    # status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string="Status")
    partner_id = fields.Many2one('res.partner', string="Customer")
    property_id = fields.Many2one('property.estate', string="Property")

    @api.model
    def _set_created_date(self):
        return fields.Date.today()

    creation_date = fields.Date("Creation Date")
    deadline3 = fields.Date("Deadline33", compute='_create_deadline', inverse='inverse_deadline')
    validity = fields.Integer("Validity")

    def action_accept_offer(self):
        if self.property_id:
            self.validate_accepted_offer()
            self.property_id.write({
                "selling_price": self.price,
                "status": "accept"
            })
        self.status = "accept"

    def action_refuse_offer(self):
        self.status = "refuse"
        if all(self.property_id.offer_ids.mapped("status")):
            self.property_id.write({
                "status": "refuse",
                "selling_price": 0
            })

    def validate_accepted_offer(self):
        offer_ids = self.env["property.offer"].search(
            [
                ('property_id', '=', self.property_id.id),
                ('status', '=', 'accept')
            ]
        )
        if offer_ids:
            raise ValidationError("You have accepted offer already")

    @api.depends("validity", "creation_date")
    def _create_deadline(self):
        for rec in self:
            if rec.creation_date and rec.validity:
                rec.deadline3 = rec.creation_date + timedelta(days=rec.validity)
            else:
                rec.deadline3 = False

    def accept_offer(self):
        if self.partner_id:
            self.partner_id.write({
                "selling_price": self.price
            })
        self.status = "accept"

    def refuse_offer(self):
        self.status = "refuse"

    def inverse_deadline(self):
        for rec in self:
            if rec.deadline3 and rec.creation_date:
                rec.validity = (rec.deadline3 - rec.creation_date).days
            else:
                rec.validity = False

    # _sql_constraints = [
    #     ("check_validity", "check(validity < 0)", "Deadline can not be before creation")
    # ]

    # @api.constrains("validity")
    # def _check_validity(self):
    #     for rec in self:
    #         if rec.deadline <= rec.creation_date:
    #             raise ValidationError("Deadline can not be before creation date")

    # runs everyday

    @api.autovacuum
    def _clean_offers(self):
        self.search([('status', '=', "refused")]).unlink()

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            if not rec.get("creation_date"):
                rec["creation_date"] = fields.Date.today()
        return super(PropertyOffer, self).create(vals)

    # def write(self,vals):
    #     res_partner_ids = self.env[].search([
    #         ("is_company", "=", True)
    #     ])
    #     res_partner_ids = self.env[].browse([10,14])
    #     print(res_partner_ids.name)
    #     return super(PropertyOffer, self).write(vals)
