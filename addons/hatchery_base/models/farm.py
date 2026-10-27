# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import fields, models

from .selection import FARM_KINDS


class HatcheryFarm(models.Model):
    _name = "hatchery.farm"
    _description = "Granja"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name, id"

    name = fields.Char(string="Nombre", required=True, tracking=True)
    code = fields.Char(string="Código", tracking=True)
    kind = fields.Selection(FARM_KINDS, string="Tipo", required=True, tracking=True)
    partner_id = fields.Many2one("res.partner", string="Contacto", tracking=True)
    address = fields.Char(string="Dirección")
    senasa_code = fields.Char(string="Código SENASA", tracking=True)
    receiving_capacity_day = fields.Integer(string="Capacidad de recepción por día")
    active = fields.Boolean(string="Activo", default=True)
    flock_ids = fields.One2many("hatchery.breeder.flock", "farm_id", string="Lotes reproductores")
