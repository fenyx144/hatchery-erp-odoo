/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const STATE_LABELS = {
    free: "Libre",
    loaded: "Cargada",
    cleaning: "Limpieza",
    maintenance: "Mantenimiento",
};

export class PlantMap extends Component {
    static template = "hatchery_base.PlantMap";
    static props = ["*"];

    setup() {
        this.orm = useService("orm");
        this.state = useState({
            plants: [],
            plantId: false,
            machines: [],
        });
        onWillStart(async () => {
            this.state.plants = await this.orm.searchRead("hatchery.plant", [], ["name"], {
                order: "name",
            });
            if (this.state.plants.length) {
                this.state.plantId = this.state.plants[0].id;
            }
            await this.loadMachines();
        });
    }

    async loadMachines() {
        const domain = this.state.plantId ? [["plant_id", "=", this.state.plantId]] : [];
        this.state.machines = await this.orm.searchRead(
            "hatchery.machine",
            domain,
            ["code", "state", "x_pos", "y_pos", "scada_id", "kind"],
            { order: "code" }
        );
    }

    async onPlantChange(ev) {
        const value = ev.target.value;
        this.state.plantId = value ? Number(value) : false;
        await this.loadMachines();
    }

    machineStyle(machine) {
        const x = Number.isFinite(machine.x_pos) ? machine.x_pos : 0;
        const y = Number.isFinite(machine.y_pos) ? machine.y_pos : 0;
        return `left: ${x}%; top: ${y}%;`;
    }

    stateLabel(state) {
        return STATE_LABELS[state] || state || "";
    }
}

registry.category("actions").add("hatchery_base.plant_map", PlantMap);
