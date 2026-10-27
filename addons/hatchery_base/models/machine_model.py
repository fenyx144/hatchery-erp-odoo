# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from .selection import MACHINE_KINDS


class HatcheryMachineModel(models.Model):
    _name = "hatchery.machine.model"
    _description = "Modelo de máquina"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "brand, model, id"
    _rec_name = "model"

    brand = fields.Char(string="Marca", tracking=True)
    model = fields.Char(string="Modelo", required=True, tracking=True)
    kind = fields.Selection(MACHINE_KINDS, string="Tipo", required=True, tracking=True)
    capacity_eggs = fields.Integer(string="Capacidad (huevos)", required=True, tracking=True)
    trolleys = fields.Integer(string="Carros")
    trays_per_trolley = fields.Integer(string="Bandejas por carro")
    eggs_per_tray = fields.Integer(string="Huevos por bandeja")
    cleaning_days = fields.Integer(string="Días de limpieza", default=1)

    @api.depends("brand", "model")
    def _compute_display_name(self):
        for record in self:
            parts = [record.brand, record.model]
            record.display_name = " ".join(part for part in parts if part) or self.env._(
                "Modelo de máquina"
            )

    @api.constrains("capacity_eggs")
    def _check_capacity_eggs(self):
        for record in self:
            if record.capacity_eggs <= 0:
                raise ValidationError(_("La capacidad en huevos debe ser mayor que cero."))
