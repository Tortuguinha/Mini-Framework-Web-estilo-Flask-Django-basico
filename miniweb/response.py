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

        # Header padrão se não for definido
        if "Content-Type" not in self.headers:
            self.headers["Content-Type"] = "text/html; charset=utf-8"

    def set_header(self, key: str, value: str):
        """Define ou sobrescreve um header."""
        self.headers[key] = value

    def set_status(self, code: int, message: str = None):
        """Define o código de status da resposta."""
        self.status = code
        if message:
            self._status_message_override = message
        else:
            self._status_message_override = None

    def _get_status_message(self):
        """Retorna a mensagem textual para o código HTTP."""
        status_messages = {
            200: "OK",
            201: "Created",
            204: "No Content",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
        }
        return (
            self._status_message_override
            if hasattr(self, "_status_message_override") and self._status_message_override
            else status_messages.get(self.status, "Unknown Status")
        )

    def to_wsgi(self):
        """
        Retorna no formato esperado por servidores WSGI.
        Exemplo: ("200 OK", [("Content-Type", "text/html")], [b"<h1>Hello</h1>"])
        """
        status_str = f"{self.status} {self._get_status_message()}"
        headers_list = [(key, value) for key, value in self.headers.items()]
        return status_str, headers_list, [self.body.encode("utf-8")]

    def build(self) -> str:
        """
        Constrói a resposta HTTP bruta (string) para enviar via socket.
        """
        status_line = f"HTTP/1.1 {self.status} {self._get_status_message()}"
        headers_str = "\r\n".join(f"{k}: {v}" for k, v in self.headers.items())
        return f"{status_line}\r\n{headers_str}\r\n\r\n{self.body}"

    # ---------- Helpers ----------
    @staticmethod
    def json(data, status: int = 200):
        """Cria uma resposta JSON."""
        body = json.dumps(data, ensure_ascii=False)
        response = Response(body=body, status=status)
        response.set_header("Content-Type", "application/json; charset=utf-8")
        return response

    @staticmethod
    def html(content: str, status: int = 200):
        """Cria uma resposta HTML."""
        response = Response(body=content, status=status)
        response.set_header("Content-Type", "text/html; charset=utf-8")
        return response

    @staticmethod
    def text(content: str, status: int = 200):
        """Cria uma resposta de texto puro."""
        response = Response(body=content, status=status)
        response.set_header("Content-Type", "text/plain; charset=utf-8")
        return response
