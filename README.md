# hatchery-erp-odoo

ERP de planta de incubación sobre Odoo 18 Community. La especificación está en `docs/ficha_tecnica.md`.

## WP-01

```bash
make up
curl -f --cacert secrets/dev-ca.crt https://localhost/api/v1/health
```

En Windows (Docker Desktop + WSL2): `scripts/start.ps1`, y el mismo `curl`.

Los secretos se generan en `secrets/` y no se versionan. La plantilla de entorno es `.env.example`. Las decisiones que la ficha deja abiertas están en `docs/PREGUNTAS.md`.
