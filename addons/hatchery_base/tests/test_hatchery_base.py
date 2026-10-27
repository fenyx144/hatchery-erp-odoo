# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from datetime import timedelta

from odoo.exceptions import AccessError, ValidationError
from odoo.fields import Date
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestHatcheryBase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.plant = cls.env["hatchery.plant"].create({
            "name": "Planta de prueba",
            "tz": "America/Lima",
        })
        cls.farm = cls.env["hatchery.farm"].create({
            "name": "Granja de prueba",
            "kind": "breeder",
            "code": "GRA-PRUEBA",
        })
        cls.variables = {}
        for code, unit in (("temp", "°C"), ("rh", "%"), ("co2", "ppm")):
            variable = cls.env["hatchery.variable"].search([("code", "=", code)], limit=1)
            if not variable:
                variable = cls.env["hatchery.variable"].create({"code": code, "unit": unit})
            cls.variables[code] = variable

    def _sensor_vals(self, machine, variable, tag):
        return {
            "machine_id": machine.id,
            "variable_id": variable.id,
            "scada_tag": tag,
            "unit": variable.unit,
            "scale": 1,
            "offset": 0,
            "min_alarm": 0,
            "min_ok": 10,
            "max_ok": 20,
            "max_alarm": 30,
        }

    def test_crear_modelo_y_tres_sensores(self):
        model = self.env["hatchery.machine.model"].create({
            "brand": "Marca de prueba",
            "model": "Incubadora de prueba",
            "kind": "setter",
            "capacity_eggs": 1500,
            "trolleys": 2,
            "trays_per_trolley": 10,
            "eggs_per_tray": 75,
        })
        machine = self.env["hatchery.machine"].create({
            "code": "INC-PRUEBA-01",
            "model_id": model.id,
            "plant_id": self.plant.id,
            "scada_id": "SCADA-PRUEBA-01",
            "state": "free",
            "x_pos": 25,
            "y_pos": 40,
        })
        sensors = self.env["hatchery.sensor"]
        for index, code in enumerate(("temp", "rh", "co2"), start=1):
            sensors |= self.env["hatchery.sensor"].create(
                self._sensor_vals(machine, self.variables[code], f"TAG-PRUEBA-{index}")
            )
        self.assertEqual(len(sensors), 3)
        self.assertEqual(machine.sensor_ids, sensors)
        self.assertEqual(machine.x_pos, 25)
        self.assertEqual(machine.y_pos, 40)
        action = self.env.ref("hatchery_base.action_hatchery_plant_map")
        self.assertEqual(action.tag, "hatchery_base.plant_map")
        self.assertEqual(self.plant.machine_free_count, 1)
        self.assertEqual(self.plant.installed_capacity_eggs, 1500)

    def test_capacidad_debe_ser_positiva(self):
        with self.assertRaises(ValidationError):
            self.env["hatchery.machine.model"].create({
                "model": "Sin capacidad",
                "kind": "setter",
                "capacity_eggs": 0,
            })

    def test_scada_unico_por_planta(self):
        model = self.env["hatchery.machine.model"].create({
            "model": "Modelo SCADA",
            "kind": "hatcher",
            "capacity_eggs": 100,
        })
        vals = {
            "model_id": model.id,
            "plant_id": self.plant.id,
            "scada_id": "SCADA-DUP",
        }
        self.env["hatchery.machine"].create({**vals, "code": "M-1"})
        with self.assertRaises(ValidationError):
            self.env["hatchery.machine"].create({**vals, "code": "M-2"})
        other = self.env["hatchery.plant"].create({"name": "Otra planta de prueba"})
        self.env["hatchery.machine"].create({
            **vals,
            "code": "M-3",
            "plant_id": other.id,
        })
        self.env["hatchery.machine"].create({
            "code": "M-4",
            "model_id": model.id,
            "plant_id": self.plant.id,
        })
        self.env["hatchery.machine"].create({
            "code": "M-5",
            "model_id": model.id,
            "plant_id": self.plant.id,
        })

    def test_umbrales(self):
        model = self.env["hatchery.machine.model"].create({
            "model": "Modelo umbral",
            "kind": "chamber",
            "capacity_eggs": 10,
        })
        machine = self.env["hatchery.machine"].create({
            "code": "CAM-PRUEBA",
            "model_id": model.id,
            "plant_id": self.plant.id,
        })
        vals = self._sensor_vals(machine, self.variables["temp"], "TAG-MAL")
        vals["max_ok"] = vals["min_ok"]
        with self.assertRaises(ValidationError):
            self.env["hatchery.sensor"].create(vals)

    def test_edad_en_semanas(self):
        today = Date.context_today(self.env.user)
        flock = self.env["hatchery.breeder.flock"].create({
            "farm_id": self.farm.id,
            "house": "Galpón 1",
            "hatch_date": today - timedelta(days=20),
        })
        self.assertEqual(flock.age_weeks, 2)
        empty = self.env["hatchery.breeder.flock"].create({"farm_id": self.farm.id})
        self.assertEqual(empty.age_weeks, 0)

    def test_usuario_solo_lee(self):
        user = self.env["res.users"].with_context(no_reset_password=True).create({
            "name": "Usuario de lectura",
            "login": "hatchery_lectura",
            "groups_id": [(6, 0, [
                self.env.ref("base.group_user").id,
                self.env.ref("hatchery_base.group_hatchery_user").id,
            ])],
        })
        plants = self.env["hatchery.plant"].with_user(user).search([("id", "=", self.plant.id)])
        self.assertEqual(plants, self.plant)
        with self.assertRaises(AccessError):
            self.env["hatchery.plant"].with_user(user).create({"name": "No permitida"})

    def test_regla_de_compania(self):
        company = self.env["res.company"].create({"name": "Compañía de prueba"})
        hidden = self.env["hatchery.plant"].sudo().create({
            "name": "Planta de otra compañía",
            "company_id": company.id,
        })
        user = self.env["res.users"].with_context(no_reset_password=True).create({
            "name": "Usuario de compañía",
            "login": "hatchery_compania",
            "company_id": self.env.company.id,
            "company_ids": [(6, 0, [self.env.company.id])],
            "groups_id": [(6, 0, [
                self.env.ref("base.group_user").id,
                self.env.ref("hatchery_base.group_hatchery_user").id,
            ])],
        })
        visible = self.env["hatchery.plant"].with_user(user).search([("id", "=", hidden.id)])
        self.assertFalse(visible)
        own = self.env["hatchery.plant"].with_user(user).search([("id", "=", self.plant.id)])
        self.assertEqual(own, self.plant)

    def test_demo_en_el_mapa(self):
        machine = self.env.ref("hatchery_base.machine_demo_setter", raise_if_not_found=False)
        if not machine:
            self.skipTest("sin datos demo")
        self.assertTrue(machine.x_pos or machine.y_pos)
        self.assertEqual(len(machine.sensor_ids), 3)
        self.assertTrue(machine.scada_id)
