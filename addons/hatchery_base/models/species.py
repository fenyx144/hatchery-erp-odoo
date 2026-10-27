# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import fields, models


class HatcherySpecies(models.Model):
    _name = "hatchery.species"
    _description = "Especie"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name, id"

    name = fields.Char(string="Nombre", required=True, tracking=True)
    incubation_days = fields.Integer(string="Días de incubación", default=21, required=True)
    candling_days = fields.Char(string="Días de ovoscopia", default="10,18", required=True)
    program_ids = fields.One2many("hatchery.program", "species_id", string="Programas")
