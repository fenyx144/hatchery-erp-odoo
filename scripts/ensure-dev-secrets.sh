#!/usr/bin/env bash
# Genera secretos locales y una CA de desarrollo. No imprime los secretos.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"
mkdir -p secrets
umask 077

if [[ ! -s secrets/db_pw ]]; then
  openssl rand -hex 24 > secrets/db_pw
fi
if [[ ! -s secrets/ts_pw ]]; then
  openssl rand -hex 24 > secrets/ts_pw
fi
if [[ ! -s secrets/ts_ro_dsn ]]; then
  # Formato no definido en la ficha. URI libpq; el rol ts_ro no se crea en WP-01.
  ro_pw="$(openssl rand -hex 24)"
  printf 'postgresql://ts_ro:%s@tsdb:5432/telemetry\n' "$ro_pw" > secrets/ts_ro_dsn
fi

if [[ ! -s secrets/dev-ca.key || ! -s secrets/dev-ca.crt ]]; then
  openssl req -x509 -newkey rsa:2048 -nodes \
    -keyout secrets/dev-ca.key \
    -out secrets/dev-ca.crt \
    -days 825 \
    -subj "/CN=Hatchery Dev CA"
fi

if [[ ! -s secrets/nginx.key || ! -s secrets/nginx.crt ]]; then
  openssl req -newkey rsa:2048 -nodes \
    -keyout secrets/nginx.key \
    -out secrets/nginx.csr \
    -subj "/CN=localhost"
  cat > secrets/nginx.ext <<'EOF'
subjectAltName=DNS:localhost,IP:127.0.0.1
extendedKeyUsage=serverAuth
keyUsage=digitalSignature,keyEncipherment
EOF
  openssl x509 -req \
    -in secrets/nginx.csr \
    -CA secrets/dev-ca.crt \
    -CAkey secrets/dev-ca.key \
    -CAcreateserial \
    -out secrets/nginx.crt \
    -days 825 \
    -extfile secrets/nginx.ext
  rm -f secrets/nginx.csr secrets/nginx.ext
fi

if [[ ! -f .env ]]; then
  cp .env.example .env
fi

# Postgres arranca como root y puede leer 0600. Odoo y analytics no: el secreto
# se monta con el modo del archivo del host.
chmod 644 secrets/db_pw secrets/ts_pw secrets/ts_ro_dsn secrets/nginx.crt secrets/dev-ca.crt
chmod 600 secrets/nginx.key secrets/dev-ca.key

if command -v sudo >/dev/null 2>&1; then
  sudo cp secrets/dev-ca.crt /usr/local/share/ca-certificates/hatchery-dev-ca.crt
  sudo update-ca-certificates >/dev/null
else
  echo "sudo no está disponible; curl no confiará en la CA de desarrollo" >&2
  exit 1
fi
