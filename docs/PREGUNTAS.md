# Preguntas abiertas

Fuente: `docs/ficha_tecnica.md` versión 1.3. Aquí solo entra lo que este paquete no pudo cerrar sin inventar un requisito.

## Afectan a WP-01

1. **Despliegue (sección 2.2 y pregunta 15 de la sección 12.2).** Sigue [POR CONFIRMAR] si el servidor está en la planta o en un VPS. El compose es el entorno autoalojado de desarrollo. No se eligió un destino de producción.

2. **Proveedor de LLM (pregunta 11).** `LLM_PROVIDER` queda vacío. No hay modelo configurado.

3. **Cuerpo de `GET /api/v1/health` (sección 2.4).** La ficha solo dice «Estado de servicios». La respuesta de este paquete es `{"status":"ok"}` con HTTP 200 si el proceso ve el secreto `ts_ro_dsn` y `ODOO_URL`. No hay un esquema de detalle por servicio.

4. **Formato de `secrets/ts_ro_dsn`.** No está definido. En desarrollo el archivo es una URI libpq: `postgresql://ts_ro:<secreto>@tsdb:5432/telemetry`. El rol `ts_ro` no se crea: el esquema de la sección 5.3 y los usuarios de la sección 2.3 corresponden a WP-05. Analytics no abre esa conexión en WP-01.

5. **Secreto de `ts_writer`.** La sección 2.3 pide ese usuario de solo INSERT. La sección 2.2 no declara un archivo de secreto. No se creó el rol ni una contraseña.

6. **Certificado TLS de producción.** No está definido. `make up` genera una CA local, no versionada. Instalarla en el almacén del sistema es opcional y puede fallar; la prueba usa `curl -f --cacert secrets/dev-ca.crt https://localhost/api/v1/health`. No es el certificado de la planta.

7. **Límite de 20 req/s por token (sección 2.3).** `hatchery.device.token` todavía no existe. Nginx aplica 20 req/s por dirección IP, con una ráfaga de 5. Falta confirmar si ese sustituto sirve hasta que existan los tokens.

8. **Clave maestra de Odoo (`admin_passwd`).** En desarrollo la genera `scripts/ensure-dev-secrets.sh` en `secrets/odoo_admin_passwd` y el arranque la inyecta. No se usa la clave por defecto de la imagen ni se versiona. Sigue abierto cómo custodiarla y rotarla en la planta.

9. **Nombre de la base de la aplicación Odoo.** La ficha fija `POSTGRES_DB=postgres` para el motor. No dice qué base debe crear Odoo. WP-01 no inicializa una base de aplicación.

10. **CI de la sección 10.** Pide pylint-odoo, pruebas Odoo, pytest de cada servicio y una carga de 5 minutos. Esos artefactos llegan en paquetes posteriores. El workflow de WP-01 ejecuta ruff sobre los servicios mínimos y el comando de la tabla 11.1.

## Afectan a WP-02

11. **Valores de `health_status`.** La sección 3.1 no define una lista. Quedó como texto libre, no como selección.

12. **Unidad de `receiving_capacity_day`.** No dice si son huevos, pollitos u otra medida. La etiqueta es «Capacidad de recepción por día», sin unidad.

13. **Unidad de `x_pos` y `y_pos`.** No está definida. El mapa las interpreta como porcentaje del plano (0 a 100) desde la esquina superior izquierda. No se rechazan otros números. Es una suposición para poder dibujar, no un dato de la planta.

14. **`company_id` y `plant_id` en todos los modelos (sección 10) frente a la sección 3.1.** La sección 3.1 solo pone `company_id` en `hatchery.plant` y `plant_id` en `hatchery.machine`. No se añadieron esos campos al resto: la sección 10 corresponde a WP-18. Hay regla de registro por compañía en la planta y, a través de esa relación, en la máquina y el sensor. Granjas, lotes, modelos, variables, especies y programas quedan compartidos entre compañías.

15. **Aparición en el simulador.** La aceptación de 3.1 dice que la máquina nueva aparece en el mapa y en el simulador. Exportar e importar con el simulador es WP-04. Este paquete guarda `x_pos`, `y_pos`, sensores y `scada_id` para que ese paquete los lea. No hay escritura al simulador ni al SCADA.

16. **Matriz de 7 roles (sección 6.3).** Es WP-15 (`hatchery_security`). Aquí solo hay dos grupos del módulo: Usuario (lectura) y Responsable (alta, baja y modificación).

17. **Modelos reales de máquina (sección 1.4).** Siguen [POR CONFIRMAR]. El demo no usa HatchTech ni otra marca real: «Marca de demostración» y capacidades ficticias.

18. **Umbrales del sensor.** La regla `min_alarm < min_ok < max_ok < max_alarm` se exige siempre. Un Float de Odoo vale 0 si nadie lo llena, y 0 no cumple la desigualdad salvo que el resto de límites la respete (por ejemplo 0 < 10 < 20 < 30). No hay un valor «vacío». La ficha no dice si los cuatro límites son obligatorios ni su unidad.

19. **`scale` y `offset`.** La ficha no da valores por defecto. Quedaron en 1 y 0 para no transformar la lectura hasta que alguien los cambie.

20. **Código de `hatchery.variable` único.** La ficha enumera temp, rh, co2, turn, fan y valve, y no dice si pueden repetirse. Se impidió repetir el código. La unidad de fan y valve no aparece en la ficha: el demo las deja vacías. °C, %, ppm y grados del demo salen de la física descrita en la sección 4.2, como datos de ejemplo.

21. **Coherencia numérica no exigida.** No se exige que `capacity_eggs` sea igual a carros × bandejas × huevos por bandeja, ni que `days_setter + days_hatcher` sea igual a `incubation_days`.

22. **`age_weeks`.** Semanas enteras entre `hatch_date` y la fecha del contexto (`días // 7`). Si no hay fecha, el valor es 0. Una fecha futura da un número negativo. La ficha no lo prohíbe.

23. **Tipo en `hatchery.machine`.** El campo `kind` es el tipo del modelo (`model_id.kind`), almacenado para filtrar y agrupar. No es un segundo catálogo.

24. **Dirección de la granja.** Quedó como texto. La ficha no dice si debe ser un contacto con calle, distrito y ubigeo.

25. **Datos de la sección 10 y almacenes.** El demo de este paquete es un juego pequeño (una planta, un ejemplo de cada tipo de granja, pocos equipos). Las 25 máquinas, 60 días y 3 clientes son WP-18. Los almacenes (`WH/Huevo-Frio` y el resto) son de `hatchery_stock` (WP-07); aquí no se crean.

26. **Traducciones `.po` y `auditlog`.** Son WP-18. Las etiquetas están escritas en español en el módulo. Los modelos principales heredan `mail.thread` porque la dependencia declarada es `mail`; no se instaló `auditlog`.

27. **Unicidad del código de máquina.** La ficha solo exige `scada_id` único por planta. El código de la máquina puede repetirse. Varios `scada_id` vacíos se permiten.

28. **Consignas del programa demo.** 37,7 °C y el resto de pasos son cifras de ejemplo para ver la ficha, no el programa de la planta. La curva real no está en la sección 3.1.

## El resto de la ficha

Las preguntas 1 a 10, 12 y 14 de la sección 12.2 no cambian estos paquetes. Siguen abiertas allí.
