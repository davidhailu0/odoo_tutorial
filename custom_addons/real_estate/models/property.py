from odoo import fields, models, api


class Property(models.Model):
    _name = "property.estate"
    _description = "Module that helps with advertising real states"

    name = fields.Char("Name", required=True)
    tag_ids = fields.Many2many("property.tag", string="Property Tag")
    description = fields.Text("Description")
    type_id = fields.Many2one("property.type", string="Property Type")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From")
    expected_price = fields.Float("Expected Price")
    best_offer = fields.Float("Best Offer")
    selling_price = fields.Float("Selling Price")
    bedrooms = fields.Integer("Bedrooms")
    living_area = fields.Integer("Living Area (sqm)")
    facade = fields.Integer("Facade")
    garage = fields.Integer("Garage", default=True)
    garden = fields.Boolean("Garden", default=False)
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')], "Garden Orientation",
        default='north')
    offer_ids = fields.One2many("property.offer", "property_id")
    sales_id = fields.Many2one("res.users", string="Salesman")
    buyer_id = fields.Many2one("res.partner", string="Buyer")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    total_area = fields.Integer("Total Area", compute=_compute_total_area)


class PropertyType(models.Model):
    _name = "property.type"
    _description = "The Type of Property to be added"

    name = fields.Char("Name", required=True)


class PropertyTag(models.Model):
    _name = "property.tag"
    _description = "Added another model for tag"

    name = fields.Char("Name", required=True)
