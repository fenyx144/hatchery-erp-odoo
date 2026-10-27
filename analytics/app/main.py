import os

from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Hatchery API",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json",
    docs_url=None,
    redoc_url=None,
)


@app.get("/api/v1/health", summary="Estado de servicios")
def health() -> dict[str, str]:
    """Comprueba que este proceso tiene el secreto y la URL de Odoo.

    El cuerpo detallado por servicio no está definido en la ficha (sección 2.4).
    """
    dsn_file = os.environ.get("TSDB_DSN_FILE", "")
    if not dsn_file or not os.path.isfile(dsn_file) or os.path.getsize(dsn_file) == 0:
        raise HTTPException(status_code=503, detail="missing_secret")
    if not os.environ.get("ODOO_URL"):
        raise HTTPException(status_code=503, detail="missing_odoo_url")
    return {"status": "ok"}
