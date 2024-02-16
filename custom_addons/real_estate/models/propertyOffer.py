from odoo import fields, models


class PropertyOffer(models.Model):
    _name = "property.offer"
    _description = "offer for house property"

    price = fields.Float("Price")
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string="Status")
    partner_id = fields.Many2one('res.partner', string="Customer")
    property_id = fields.Many2one('property.estate', string="Property")
    validity = fields.Integer("Validity")
    deadline = fields.Date("Deadline")
