# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from .selection import MACHINE_KINDS, MACHINE_STATES


class HatcheryMachine(models.Model):
    _name = "hatchery.machine"
    _description = "Máquina"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "plant_id, code, id"
    _rec_name = "code"

    code = fields.Char(string="Código", required=True, tracking=True)
    model_id = fields.Many2one(
        "hatchery.machine.model",
        string="Modelo",
        required=True,
        ondelete="restrict",
        tracking=True,
    )
    kind = fields.Selection(
        MACHINE_KINDS,
        string="Tipo",
        related="model_id.kind",
        store=True,
    )
    plant_id = fields.Many2one(
        "hatchery.plant",
        string="Planta",
        required=True,
        ondelete="restrict",
        index=True,
        tracking=True,
    )
    scada_id = fields.Char(
        string="Identificador SCADA",
        copy=False,
        tracking=True,
        help="Identificador de solo lectura. El ERP no escribe en el SCADA ni en la máquina.",
    )
    state = fields.Selection(
        MACHINE_STATES,
        string="Estado",
        required=True,
        default="free",
        tracking=True,
        index=True,
    )
    x_pos = fields.Float(
        string="Posición X",
        help="Posición horizontal en el mapa de planta. El mapa la lee como porcentaje del ancho.",
    )
    y_pos = fields.Float(
        string="Posición Y",
        help="Posición vertical en el mapa de planta. El mapa la lee como porcentaje del alto.",
    )
    sensor_ids = fields.One2many("hatchery.sensor", "machine_id", string="Sensores")

    _sql_constraints = [
        (
            "scada_id_plant_uniq",
            "unique(plant_id, scada_id)",
            "El identificador SCADA ya existe en esta planta.",
        ),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        self._check_scada_vals(vals_list)
        return super().create(vals_list)

    def write(self, vals):
        if "scada_id" in vals or "plant_id" in vals:
            self._check_scada_write(vals)
        return super().write(vals)

    @api.model
    def _check_scada_vals(self, vals_list):
        seen = set()
        for vals in vals_list:
            scada_id = vals.get("scada_id")
            plant_id = vals.get("plant_id")
            if not scada_id:
                continue
            key = (plant_id, scada_id)
            if key in seen or self.search_count(
                [("plant_id", "=", plant_id), ("scada_id", "=", scada_id)]
            ):
                raise ValidationError(_("El identificador SCADA ya existe en esta planta."))
            seen.add(key)

    def _check_scada_write(self, vals):
        for machine in self:
            scada_id = vals.get("scada_id", machine.scada_id)
            plant_id = vals.get("plant_id", machine.plant_id.id)
            if not scada_id:
                continue
            duplicate = self.search_count(
                [
                    ("id", "not in", self.ids),
                    ("plant_id", "=", plant_id),
                    ("scada_id", "=", scada_id),
                ]
            )
            if duplicate:
                raise ValidationError(_("El identificador SCADA ya existe en esta planta."))
