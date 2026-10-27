# Preguntas abiertas (WP-01)

Fuente: `doc/ficha_tecnica.md` versión 1.3. Aquí solo entra lo que este paquete no pudo cerrar sin inventar un requisito.

## Afectan a WP-01

1. **Despliegue (sección 2.2 y pregunta 15 de la sección 12.2).** Sigue [POR CONFIRMAR] si el servidor está en la planta o en un VPS. El compose es el entorno autoalojado de desarrollo. No se eligió un destino de producción.

2. **Proveedor de LLM (pregunta 11).** `LLM_PROVIDER` queda vacío. No hay modelo configurado.

3. **Cuerpo de `GET /api/v1/health` (sección 2.4).** La ficha solo dice «Estado de servicios». La respuesta de este paquete es `{"status":"ok"}` con HTTP 200 si el proceso ve el secreto `ts_ro_dsn` y `ODOO_URL`. No hay un esquema de detalle por servicio.

4. **Formato de `secrets/ts_ro_dsn`.** No está definido. En desarrollo el archivo es una URI libpq: `postgresql://ts_ro:<secreto>@tsdb:5432/telemetry`. El rol `ts_ro` no se crea: el esquema de la sección 5.3 y los usuarios de la sección 2.3 corresponden a WP-05. Analytics no abre esa conexión en WP-01.

5. **Secreto de `ts_writer`.** La sección 2.3 pide ese usuario de solo INSERT. La sección 2.2 no declara un archivo de secreto. No se creó el rol ni una contraseña.

6. **Certificado TLS de producción.** No está definido. `make up` genera una CA local, no versionada, y la instala en el almacén del sistema para que `curl -f https://localhost/api/v1/health` confíe en ella. No es el certificado de la planta.

7. **Límite de 20 req/s por token (sección 2.3).** `hatchery.device.token` todavía no existe. Nginx aplica 20 req/s por dirección IP, con una ráfaga de 5. Falta confirmar si ese sustituto sirve hasta que existan los tokens.

8. **Clave maestra de Odoo (`admin_passwd`).** No está entre los secretos de la sección 2.2. No se escribió una clave en el repositorio. Queda el valor por defecto de la imagen.

9. **Nombre de la base de la aplicación Odoo.** La ficha fija `POSTGRES_DB=postgres` para el motor. No dice qué base debe crear Odoo. WP-01 no inicializa una base de aplicación.

10. **CI de la sección 10.** Pide pylint-odoo, pruebas Odoo, pytest de cada servicio y una carga de 5 minutos. Esos artefactos llegan en paquetes posteriores. El workflow de WP-01 ejecuta ruff sobre los servicios mínimos y el comando de la tabla 11.1.

## El resto de la ficha

Las preguntas 1 a 10, 12 y 14 de la sección 12.2 no cambian este paquete. Siguen abiertas allí.
