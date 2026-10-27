#!/bin/bash
# Copia odoo.conf y añade admin_passwd desde el secreto. No imprime la clave.
set -euo pipefail

secret=/run/secrets/odoo_admin_passwd
if [[ ! -s "$secret" ]]; then
  echo "falta el secreto odoo_admin_passwd" >&2
  exit 1
fi

umask 077
install -d -m 700 /tmp/odoo
grep -v -E '^[[:space:]]*admin_passwd[[:space:]]*=' /etc/odoo/odoo.conf > /tmp/odoo/odoo.conf
printf 'admin_passwd = %s\n' "$(<"$secret")" >> /tmp/odoo/odoo.conf
chmod 600 /tmp/odoo/odoo.conf
export ODOO_RC=/tmp/odoo/odoo.conf
exec /entrypoint.sh odoo
