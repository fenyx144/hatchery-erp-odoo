# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import api, fields, models


class HatcheryBreederFlock(models.Model):
    _name = "hatchery.breeder.flock"
    _description = "Lote reproductor"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "hatch_date desc, id"
    _rec_name = "house"

    farm_id = fields.Many2one(
        "hatchery.farm",
        string="Granja",
        required=True,
        ondelete="restrict",
        index=True,
        tracking=True,
    )
    house = fields.Char(string="Galpón", tracking=True)
    genetic_line = fields.Char(string="Línea genética", tracking=True)
    hatch_date = fields.Date(string="Fecha de nacimiento", tracking=True)
    age_weeks = fields.Integer(
        string="Edad (semanas)",
        compute="_compute_age_weeks",
        help="Semanas enteras entre la fecha de nacimiento y la fecha actual.",
    )
    health_status = fields.Char(string="Estado sanitario", tracking=True)

    @api.depends("farm_id.name", "house", "genetic_line")
    def _compute_display_name(self):
        for flock in self:
            parts = [flock.farm_id.name, flock.house, flock.genetic_line]
            flock.display_name = " · ".join(part for part in parts if part) or self.env._(
                "Lote reproductor"
            )

    @api.depends("hatch_date")
    @api.depends_context("tz")
    def _compute_age_weeks(self):
        today = fields.Date.context_today(self)
        for flock in self:
            if flock.hatch_date:
                flock.age_weeks = (today - flock.hatch_date).days // 7
            else:
                flock.age_weeks = 0
