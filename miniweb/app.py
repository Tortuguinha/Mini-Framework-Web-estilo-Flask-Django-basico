import socket  # Biblioteca padrão do Python para comunicação de rede (TCP/UDP)
from .response import Response  # Classe para facilitar a criação de respostas HTTP
from .request import Request    # Classe para facilitar o parsing de requisições HTTP
from .router import Router      # Importa o Router modular


class App:
    def __init__(self, host="localhost", port=8000):
        """
        Classe principal do nosso mini framework web.
        - host: endereço onde o servidor vai rodar (padrão localhost)
        - port: porta do servidor (padrão 8000)
        """
        self.host = host
        self.port = port

        # Gerenciador de rotas centralizado
        self.router = Router()

    # =========================
    # 🎯 Decorador de rotas
    # =========================
    def route(self, path, methods=["GET"]):
        """
        Decorador para registrar uma rota com suporte a múltiplos métodos HTTP.
        Exemplo:
            @app.route("/", methods=["GET", "POST"])
            def home(req, res): ...
        """
        def decorator(func):
            # Registra a rota no Router
            self.router.add_route(path, func, methods)
            return func
        return decorator

    # =========================
    # 🚀 Servidor Socket
    # =========================
    def start(self):
        """
        Inicia o servidor web e fica escutando conexões HTTP.
        Usa sockets TCP para receber e responder requisições.
        """
        print(f"🚀 Server running at http://{self.host}:{self.port}")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            try:
                while True:
                    client_socket, addr = server_socket.accept()
                    with client_socket:
                        request_text = client_socket.recv(4096).decode("utf-8")
                        print(f"📩 Request from {addr}:\n{request_text}")

                        # Gera a resposta baseada na rota
                        response = self.handle_request(request_text)

                        # Envia a resposta de volta ao cliente
                        client_socket.sendall(response.encode("utf-8"))
            except KeyboardInterrupt:
                print("\n🛑 Server stopped.")

    def run(self):
        """Alias para start()"""
        self.start()

    # =========================
    # ⚙️ Processamento de requisições
    # =========================
    def handle_request(self, request_text):
        """
        Processa a requisição e devolve uma resposta HTTP.
        Suporta:
        1) Função de rota que modifica o `res`
        2) Função de rota que retorna um `Response`
        Também valida o método HTTP da rota (405) e rota inexistente (404).
        """
        req = Request(request_text)
        res = Response()
        path, method = req.path, req.method.upper()

        # =========================
        # 🔹 Usa o Router para resolver a rota
        # =========================
        route_func = self.router.resolve(path, method)

        if route_func:
            # Executa a função da rota
            result = route_func(req, res)

            if isinstance(result, Response):
                # Caso a função retorne um Response diretamente
                res = result
        else:
            # Verifica se a rota existe mas não suporta o método
            allowed_methods = self.router.allowed_methods(path)
            if allowed_methods:
                res = Response(
                    body=f"<h1>405 - Method {method} Not Allowed</h1>",
                    status=405,
                    headers={"Allow": ", ".join(allowed_methods)}
                )
            else:
                # Rota não encontrada
                res = Response(body="<h1>404 - Page Not Found</h1>", status=404)

        # Constrói a resposta HTTP final
        status_str, headers_list, body_bytes = res.to_wsgi()
        headers_str = "\r\n".join(f"{key}: {value}" for key, value in headers_list)
        return f"HTTP/1.1 {status_str}\r\n{headers_str}\r\n\r\n{body_bytes[0].decode('utf-8')}"
