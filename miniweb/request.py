import json
from urllib.parse import urlparse, parse_qs
import re

class Request:
    def __init__(self, request_text: str):
        """
        Representa uma requisição HTTP recebida pelo servidor.
        """
        self.request_text = request_text
        self.method = None          # Método HTTP (GET, POST, etc.)
        self.path = None            # Caminho da rota (/about, /api, etc.)
        self.http_version = None    # Versão do protocolo HTTP
        self.headers = {}           # Dicionário de cabeçalhos
        self.body = None            # Corpo cru da requisição
        self.query_params = {}      # Parâmetros da URL (ex.: ?foo=bar)
        self.form = {}              # Parâmetros enviados via form POST
        self.files = {}             # Arquivos enviados via form multipart
        self.cookies = {}           # Cookies enviados pelo cliente

        # Processa a requisição
        self.parse_request()

    def parse_request(self):
        """Faz o parsing da requisição HTTP bruta"""
        lines = self.request_text.split("\r\n")

        # Primeira linha: método, path e versão do HTTP
        request_line = lines[0].split(" ")
        if len(request_line) == 3:
            self.method, raw_path, self.http_version = request_line
        else:
            self.method, raw_path = request_line[0], request_line[1]
            self.http_version = "HTTP/1.1"
        self.method = self.method.upper()

        # Processa query params
        parsed = urlparse(raw_path)
        self.path = parsed.path
        self.query_params = self._parse_query(parsed.query)

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

        # Corpo cru
        self.body = "\n".join(body_lines)

        # Cookies
        if "Cookie" in self.headers:
            self.cookies = self._parse_cookies(self.headers["Cookie"])

        # ================================
        # Processa form data e arquivos
        # ================================
        content_type = self.headers.get("Content-Type", "")
        if self.method == "POST":
            if "application/x-www-form-urlencoded" in content_type:
                self.form = self._parse_form(self.body)
            elif "multipart/form-data" in content_type:
                self._parse_multipart(self.body, content_type)

    # =========================
    # 🔹 Multipart parser simples
    # =========================
    def _parse_multipart(self, body: str, content_type: str):
        """Parse multipart/form-data sem usar cgi"""
        # Extrai boundary
        m = re.search(r'boundary=(.+)', content_type)
        if not m:
            return
        boundary = "--" + m.group(1)
        parts = body.split(boundary)
        for part in parts:
            part = part.strip()
            if not part or part == "--":
                continue
            headers, _, content = part.partition("\r\n\r\n")
            content = content.rstrip("\r\n")
            header_lines = headers.split("\r\n")
            disposition = {}
            for h in header_lines:
                if h.lower().startswith("content-disposition"):
                    m = re.findall(r'(\w+)="([^"]+)"', h)
                    for k, v in m:
                        disposition[k] = v
            name = disposition.get("name")
            filename = disposition.get("filename")
            if filename:
                self.files[name] = {
                    "filename": filename,
                    "content": content.encode("utf-8")
                }
            elif name:
                self.form[name] = content

    # =========================
    # 🔹 Helpers privados
    # =========================
    def _parse_cookies(self, cookie_header: str):
        cookies = {}
        parts = cookie_header.split(";")
        for part in parts:
            if "=" in part:
                key, value = part.strip().split("=", 1)
                cookies[key] = value
        return cookies

    def _parse_query(self, query_string: str):
        return {k: v[0] if len(v) == 1 else v for k, v in parse_qs(query_string).items()}

    def _parse_form(self, body: str):
        return {k: v[0] if len(v) == 1 else v for k, v in parse_qs(body).items()}

    # =========================
    # 🔹 JSON helper público
    # =========================
    def json(self):
        try:
            return json.loads(self.body) if self.body else {}
        except json.JSONDecodeError:
            return {}
