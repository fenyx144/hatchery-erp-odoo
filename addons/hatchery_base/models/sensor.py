# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HatcherySensor(models.Model):
    _name = "hatchery.sensor"
    _description = "Sensor"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "machine_id, variable_id, id"
    _rec_name = "scada_tag"

    machine_id = fields.Many2one(
        "hatchery.machine",
        string="Máquina",
        required=True,
        ondelete="cascade",
        index=True,
        tracking=True,
    )
    variable_id = fields.Many2one(
        "hatchery.variable",
        string="Variable",
        required=True,
        ondelete="restrict",
        tracking=True,
    )
    scada_tag = fields.Char(
        string="Tag SCADA",
        tracking=True,
        help="Tag de solo lectura. El ERP no escribe en el SCADA.",
    )
    unit = fields.Char(string="Unidad")
    scale = fields.Float(string="Escala", default=1.0)
    offset = fields.Float(string="Desplazamiento", default=0.0)
    min_ok = fields.Float(string="Mínimo aceptable", required=True)
    max_ok = fields.Float(string="Máximo aceptable", required=True)
    min_alarm = fields.Float(string="Alarma mínima", required=True)
    max_alarm = fields.Float(string="Alarma máxima", required=True)

    @api.depends("scada_tag", "variable_id", "machine_id.code")
    def _compute_display_name(self):
        for sensor in self:
            sensor.display_name = sensor.scada_tag or " · ".join(
                part
                for part in (sensor.machine_id.code, sensor.variable_id.display_name)
                if part
            ) or self.env._("Sensor")

    @api.constrains("min_alarm", "min_ok", "max_ok", "max_alarm")
    def _check_thresholds(self):
        for sensor in self:
            if not (
                sensor.min_alarm < sensor.min_ok < sensor.max_ok < sensor.max_alarm
            ):
                raise ValidationError(
                    _(
                        "Los umbrales deben cumplir: alarma mínima < mínimo aceptable "
                        "< máximo aceptable < alarma máxima."
                    )
                )
