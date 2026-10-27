"""Puerto 8090 reservado para la UI del simulador (WP-04). Sin Modbus (WP-03)."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PAGE = """<!DOCTYPE html>
<html lang="es-PE">
<head>
  <meta charset="utf-8">
  <title>Simulador</title>
</head>
<body>
  <p>Simulador de planta. La configuración gráfica todavía no está disponible.</p>
</body>
</html>
""".encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path.split("?", 1)[0] == "/health":
            body = b"ok"
            content_type = "text/plain; charset=utf-8"
        elif self.path.split("?", 1)[0] == "/":
            body = PAGE
            content_type = "text/html; charset=utf-8"
        else:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: object) -> None:
        return


def main() -> None:
    server = ThreadingHTTPServer(("0.0.0.0", 8090), Handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
