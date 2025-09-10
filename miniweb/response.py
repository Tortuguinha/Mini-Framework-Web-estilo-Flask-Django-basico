import json

class Response:
    def __init__(self, body: str = "", status: int = 200, headers: dict = None):
        """
        Representa uma resposta HTTP.
        - body: conteúdo da resposta (string)
        - status: código de status HTTP (ex.: 200, 404)
        - headers: dicionário de cabeçalhos HTTP
        """
        self.body = body
        self.status = status
        self.headers = headers if headers is not None else {}

        # ✅ Garante que sempre exista um Content-Type (default = HTML)
        if "Content-Type" not in self.headers:
            self.headers["Content-Type"] = "text/html; charset=utf-8"

        # Inicializa override de mensagem de status
        self._status_message_override = None

    # ========================
    # 🔧 Métodos utilitários
    # ========================
    def set_header(self, key: str, value: str):
        """Define ou sobrescreve um header HTTP."""
        self.headers[key] = value

    def set_status(self, code: int, message: str = None):
        """
        Define o código de status HTTP da resposta.
        - code: número (ex.: 200, 404)
        - message: texto opcional (ex.: "All Good")
        """
        self.status = code
        self._status_message_override = message

    # ========================
    # 🔹 Helpers privados
    # ========================
    def _get_status_message(self):
        """
        Retorna a mensagem textual padrão de acordo com o código de status.
        Exemplo: 200 -> "OK"
        """
        status_messages = {
            200: "OK",
            201: "Created",
            204: "No Content",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            405: "Method Not Allowed",
            500: "Internal Server Error",
        }
        return (
            self._status_message_override
            if self._status_message_override
            else status_messages.get(self.status, "Unknown Status")
        )

    def _build_headers(self):
        """Retorna lista de tuplas com headers e string de headers crua."""
        headers_list = [(key, value) for key, value in self.headers.items()]
        headers_str = "\r\n".join(f"{k}: {v}" for k, v in self.headers.items())
        return headers_list, headers_str

    def _build_body(self):
        """Retorna corpo em bytes e string."""
        return [self.body.encode("utf-8")], self.body

    # ========================
    # 🚀 Integração WSGI
    # ========================
    def to_wsgi(self):
        """
        Retorna no formato esperado por servidores WSGI.
        Exemplo: ("200 OK", [("Content-Type", "text/html")], [b"<h1>Hello</h1>"])
        """
        status_str = f"{self.status} {self._get_status_message()}"
        headers_list, _ = self._build_headers()
        body_bytes, _ = self._build_body()
        return status_str, headers_list, body_bytes

    # ========================
    # 📨 Monta resposta crua (sockets)
    # ========================
    def build(self) -> str:
        """
        Constrói a resposta HTTP bruta (string) para enviar via socket.
        """
        status_line = f"HTTP/1.1 {self.status} {self._get_status_message()}"
        _, headers_str = self._build_headers()
        _, body_str = self._build_body()
        return f"{status_line}\r\n{headers_str}\r\n\r\n{body_str}"

    # ========================
    # 🎯 Atalhos helpers
    # ========================
    @staticmethod
    def json(data, status: int = 200):
        """
        Helper para criar resposta JSON.
        - data: dict ou lista (será serializado com json.dumps)
        """
        body = json.dumps(data, ensure_ascii=False)  # suporta acentos
        response = Response(body=body, status=status)
        response.set_header("Content-Type", "application/json; charset=utf-8")
        return response

    @staticmethod
    def html(content: str, status: int = 200):
        """
        Helper para criar resposta HTML.
        """
        response = Response(body=content, status=status)
        response.set_header("Content-Type", "text/html; charset=utf-8")
        return response

    @staticmethod
    def text(content: str, status: int = 200):
        """
        Helper para criar resposta em texto puro.
        """
        response = Response(body=content, status=status)
        response.set_header("Content-Type", "text/plain; charset=utf-8")
        return response
