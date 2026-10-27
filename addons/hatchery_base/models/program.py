# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import api, fields, models


class HatcheryProgram(models.Model):
    _name = "hatchery.program"
    _description = "Programa de incubación"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "species_id, id"

    species_id = fields.Many2one(
        "hatchery.species",
        string="Especie",
        required=True,
        ondelete="restrict",
        tracking=True,
    )
    days_setter = fields.Integer(string="Días en incubadora", default=18, required=True)
    days_hatcher = fields.Integer(string="Días en nacedora", default=3, required=True)
    step_ids = fields.One2many("hatchery.program.step", "program_id", string="Pasos")

    @api.depends("species_id.name", "days_setter", "days_hatcher")
    def _compute_display_name(self):
        for program in self:
            species = program.species_id.name or self.env._("Programa")
            program.display_name = f"{species} ({program.days_setter}+{program.days_hatcher})"


class HatcheryProgramStep(models.Model):
    _name = "hatchery.program.step"
    _description = "Paso de programa"
    _order = "program_id, day_from, day_to, id"
    _rec_name = "day_from"

    program_id = fields.Many2one(
        "hatchery.program",
        string="Programa",
        required=True,
        ondelete="cascade",
        index=True,
    )
    day_from = fields.Integer(string="Día desde", required=True)
    day_to = fields.Integer(string="Día hasta", required=True)
    temp_sp = fields.Float(string="Temperatura de consigna")
    rh_sp = fields.Float(string="Humedad relativa de consigna")
    co2_max = fields.Float(string="CO₂ máximo")

    @api.depends("program_id.display_name", "day_from", "day_to")
    def _compute_display_name(self):
        for step in self:
            step.display_name = self.env._(
                "%(program)s · días %(day_from)s–%(day_to)s",
                program=step.program_id.display_name or self.env._("Programa"),
                day_from=step.day_from,
                day_to=step.day_to,
            )
