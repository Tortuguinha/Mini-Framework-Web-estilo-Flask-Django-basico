class Request:
    def __init__(self, request_text):
        self.request_text = request_text
        self.method = None
        self.path = None
        self.http_version = None
        self.headers = {}
        self.body = None
        self.parse_request()

    def parse_request(self):
        # Divide a requisição em linhas
        lines = self.request_text.split("\r\n")
        
        # Primeira linha: método, path e versão do HTTP
        request_line = lines[0].split(" ")
        if len(request_line) == 3:
            self.method, self.path, self.http_version = request_line
        else:
            self.method, self.path = request_line[0], request_line[1]
            self.http_version = "HTTP/1.1"

        # Separa cabeçalhos do corpo
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

        # Transforma headers em dicionário
        for header in header_lines:
            key, value = header.split(":", 1)
            self.headers[key.strip()] = value.strip()

        # Junta corpo em string
        self.body = "\n".join(body_lines)
