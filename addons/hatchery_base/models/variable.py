# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import fields, models

from .selection import VARIABLE_CODES


class HatcheryVariable(models.Model):
    _name = "hatchery.variable"
    _description = "Variable"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "code, id"
    _rec_name = "code"

    code = fields.Selection(VARIABLE_CODES, string="Código", required=True, tracking=True)
    unit = fields.Char(string="Unidad", tracking=True)

    _sql_constraints = [
        (
            "code_uniq",
            "unique(code)",
            "Ya existe una variable con este código.",
        ),
    ]
