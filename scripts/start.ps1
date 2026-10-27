# Windows: Docker Desktop + WSL2. Equivale a `make up`.
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
& bash ./scripts/ensure-dev-secrets.sh
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
docker compose up -d --build --wait --remove-orphans
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
