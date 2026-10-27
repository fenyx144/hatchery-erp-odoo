# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

{
    "name": "Incubación: datos maestros",
    "version": "18.0.1.0.0",
    "category": "Incubación",
    "summary": "Plantas, granjas, máquinas, sensores y programas de incubación",
    "author": "Hatchery ERP",
    "website": "https://github.com/fenyx144/hatchery-erp-odoo",
    "license": "LGPL-3",
    "depends": ["base", "mail"],
    "data": [
        "security/hatchery_security.xml",
        "security/ir.model.access.csv",
        "views/plant_views.xml",
        "views/farm_views.xml",
        "views/flock_views.xml",
        "views/machine_model_views.xml",
        "views/machine_views.xml",
        "views/variable_views.xml",
        "views/sensor_views.xml",
        "views/species_views.xml",
        "views/program_views.xml",
        "views/plant_map_views.xml",
        "views/menus.xml",
    ],
    "demo": [
        "demo/demo.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "hatchery_base/static/src/plant_map/plant_map.scss",
            "hatchery_base/static/src/plant_map/plant_map.xml",
            "hatchery_base/static/src/plant_map/plant_map.js",
        ],
    },
    "application": True,
    "installable": True,
}
