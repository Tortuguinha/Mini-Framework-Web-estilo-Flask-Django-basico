import json
from urllib.parse import urlparse, parse_qs

class Request:
    def __init__(self, request_text: str):
        """
        Representa uma requisição HTTP recebida pelo servidor.
        - request_text: texto bruto da requisição recebida pelo socket
        """
        self.request_text = request_text
        
        # Atributos principais da requisição
        self.method = None          # Método HTTP (GET, POST, etc.)
        self.path = None            # Caminho da rota (/about, /api, etc.)
        self.http_version = None    # Versão do protocolo HTTP
        self.headers = {}           # Dicionário de cabeçalhos
        self.body = None            # Corpo cru da requisição
        self.query_params = {}      # Parâmetros da URL (ex.: ?foo=bar)
        self.cookies = {}           # Cookies enviados pelo cliente
        
        # Processa a requisição
        self.parse_request()

    def parse_request(self):
        """Faz o parsing da requisição HTTP bruta"""
        # Divide a requisição em linhas
        lines = self.request_text.split("\r\n")

        # Primeira linha: método, path e versão do HTTP
        request_line = lines[0].split(" ")
        if len(request_line) == 3:
            self.method, raw_path, self.http_version = request_line
        else:
            # fallback se versão não foi enviada
            self.method, raw_path = request_line[0], request_line[1]
            self.http_version = "HTTP/1.1"

        self.method = self.method.upper()  # Normaliza o método (GET, POST, ...)

        # Processa query params (ex.: /about?lang=pt&foo=bar)
        parsed = urlparse(raw_path)
        self.path = parsed.path  # só o caminho puro (/about)
        self.query_params = {k: v[0] for k, v in parse_qs(parsed.query).items()}

        # Separa cabeçalhos e corpo
        header_lines = []
        body_lines = []
        is_body = False
        for line in lines[1:]:
            if line == "":
                is_body = True
                continue
            if is_body:
                body_lines.append(line)
            else:
                header_lines.append(line)

        # Converte headers para dicionário
        for header in header_lines:
            if ":" in header:
                key, value = header.split(":", 1)
                self.headers[key.strip()] = value.strip()

        # Junta corpo em string (pode ser JSON ou outro formato)
        self.body = "\n".join(body_lines)

        # Processa cookies, se existirem
        if "Cookie" in self.headers:
            self.cookies = self._parse_cookies(self.headers["Cookie"])

    def _parse_cookies(self, cookie_header: str):
        """Transforma o header Cookie em dicionário"""
        cookies = {}
        parts = cookie_header.split(";")
        for part in parts:
            if "=" in part:
                key, value = part.strip().split("=", 1)
                cookies[key] = value
        return cookies

    def json(self):
        """
        Tenta converter o corpo da requisição em JSON.
        Retorna {} se não for possível.
        """
        try:
            return json.loads(self.body) if self.body else {}
        except json.JSONDecodeError:
            return {}
