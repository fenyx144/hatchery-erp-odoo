# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

import pytz

from odoo import api, fields, models


class HatcheryPlant(models.Model):
    _name = "hatchery.plant"
    _description = "Planta de incubación"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name, id"

    name = fields.Char(string="Nombre", required=True, tracking=True)
    company_id = fields.Many2one(
        "res.company",
        string="Compañía",
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )
    tz = fields.Selection(
        selection="_selection_tz",
        string="Zona horaria",
        required=True,
        default="America/Lima",
        tracking=True,
    )
    machine_ids = fields.One2many("hatchery.machine", "plant_id", string="Máquinas")
    machine_count = fields.Integer(string="Máquinas", compute="_compute_kpis")
    machine_free_count = fields.Integer(string="Libres", compute="_compute_kpis")
    machine_loaded_count = fields.Integer(string="Cargadas", compute="_compute_kpis")
    machine_cleaning_count = fields.Integer(string="En limpieza", compute="_compute_kpis")
    machine_maintenance_count = fields.Integer(
        string="En mantenimiento",
        compute="_compute_kpis",
    )
    installed_capacity_eggs = fields.Integer(
        string="Capacidad instalada (huevos)",
        compute="_compute_kpis",
        help="Suma de la capacidad en huevos del modelo de cada máquina de la planta.",
    )

    @api.model
    def _selection_tz(self):
        return [
            (name, name)
            for name in sorted(
                pytz.all_timezones,
                key=lambda item: item if not item.startswith("Etc/") else "_",
            )
        ]

    @api.depends("machine_ids.state", "machine_ids.model_id.capacity_eggs")
    def _compute_kpis(self):
        for plant in self:
            machines = plant.machine_ids
            plant.machine_count = len(machines)
            plant.machine_free_count = len(
                machines.filtered(lambda machine: machine.state == "free")
            )
            plant.machine_loaded_count = len(
                machines.filtered(lambda machine: machine.state == "loaded")
            )
            plant.machine_cleaning_count = len(
                machines.filtered(lambda machine: machine.state == "cleaning")
            )
            plant.machine_maintenance_count = len(
                machines.filtered(lambda machine: machine.state == "maintenance")
            )
            plant.installed_capacity_eggs = sum(machines.mapped("model_id.capacity_eggs"))
