"""Conector en espera. WP-05 implementa la captura.

Este proceso no abre sockets: no lee ni escribe Modbus, SQL ni el SCADA.
"""

import pathlib
import time

HEALTH = pathlib.Path("/tmp/healthy")


def main() -> None:
    HEALTH.write_text("ok", encoding="utf-8")
    while True:
        time.sleep(30)


if __name__ == "__main__":
    main()
