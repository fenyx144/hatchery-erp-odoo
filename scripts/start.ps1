# Windows: Docker Desktop + WSL2. Equivale a `make up`.
# ensure-dev-secrets.sh no exige sudo: si no puede instalar la CA, avisa y sigue.
# La prueba de salud, después de este script, es:
# curl -f --cacert secrets/dev-ca.crt https://localhost/api/v1/health
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
& bash ./scripts/ensure-dev-secrets.sh
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
docker compose up -d --build --wait --remove-orphans
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
