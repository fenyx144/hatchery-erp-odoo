# hatchery-erp-odoo

ERP de planta de incubación sobre Odoo 18 Community. La especificación está en `docs/ficha_tecnica.md`.

## WP-01

```bash
make up
curl -f --cacert secrets/dev-ca.crt https://localhost/api/v1/health
```

En Windows (Docker Desktop + WSL2): `scripts/start.ps1`, y el mismo `curl`.

Los secretos se generan en `secrets/` y no se versionan. La plantilla de entorno es `.env.example`. Las decisiones que la ficha deja abiertas están en `docs/PREGUNTAS.md`.

## WP-02

Módulo `addons/hatchery_base`: plantas, granjas, máquinas, sensores y programas. Con el stack de WP-01 en marcha, la prueba del módulo es:

```bash
docker compose run --rm --no-deps --entrypoint /entrypoint.sh \
  -e HOST=db -e USER=odoo -e PASSWORD_FILE=/run/secrets/db_pw \
  odoo odoo -d test --test-enable --stop-after-init -i hatchery_base --test-tags /hatchery_base
```

El comando de la tabla 11.1 no lleva `--test-tags`. La CI usa la etiqueta para no ejecutar las pruebas de Odoo que piden Chrome.
