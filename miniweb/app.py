import socket  # Biblioteca padrão do Python para comunicação de rede (TCP/UDP)
from .response import Response  # Classe para facilitar a criação de respostas HTTP
from .request import Request    # Classe para facilitar o parsing de requisições HTTP


class App:
    def __init__(self, host="localhost", port=8000):
        """
        Classe principal do nosso mini framework web.
        - host: endereço onde o servidor vai rodar (padrão localhost)
        - port: porta do servidor (padrão 8000)
        """
        self.host = host
        self.port = port
        self.routes = {}  # Dicionário que guarda as rotas registradas (ex.: "/" -> função)

    # =========================
    # 🎯 Decorador de rotas
    # =========================
    def route(self, path):
        """
        Decorador para registrar uma rota.
        Exemplo de uso:
            @app.route("/")
            def home(req, res):
                res.body = "Hello!"
                # ou return Response.text("Hello")
        """
        def decorator(func):
            self.routes[path] = func  # Salva a função associada ao caminho
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

        # Cria o socket do servidor
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))  # Liga o socket ao host e porta
            server_socket.listen(5)  # Permite até 5 conexões pendentes
            try:
                while True:  # Loop infinito para manter o servidor ativo
                    client_socket, addr = server_socket.accept()  # Aceita uma conexão
                    with client_socket:  # Garante fechamento do socket do cliente
                        request = client_socket.recv(1024).decode("utf-8")  # Recebe a requisição HTTP
                        print(f"📩 Request from {addr}:\n{request}")

                        # Gera a resposta baseada na rota
                        response = self.handle_request(request)

                        # Envia a resposta de volta ao cliente (navegador)
                        client_socket.sendall(response.encode("utf-8"))
            except KeyboardInterrupt:
                # Permite parar o servidor com CTRL+C de forma amigável
                print("\n🛑 Server stopped.")

    def run(self):
        """Alias para start() - para manter sintaxe parecida com Flask/Django."""
        self.start()

    # =========================
    # 🔎 Parsing de rota
    # =========================
    def _parse_path(self, request):
        """
        Extrai o caminho da URL (path) da requisição HTTP.
        Exemplo: 'GET /about HTTP/1.1' -> '/about'
        """
        try:
            first_line = request.split("\n")[0]  # Pega a primeira linha da requisição
            path = first_line.split(" ")[1]  # Extrai o caminho da URL
            return path
        except IndexError:
            return "/"  # Se não conseguir extrair, retorna "/"

    # =========================
    # ⚙️ Processamento de requisições
    # =========================
    def handle_request(self, request_text):
        """
        Processa a requisição e devolve uma resposta HTTP.
        Agora suporta dois estilos:
        1) Função de rota modifica o `res` recebido
        2) Função de rota retorna um `Response`
        """
        req = Request(request_text)   # Cria o objeto de requisição
        res = Response()              # Cria o objeto de resposta "em branco"
        path = req.path

        if path in self.routes:
            # Executa a função da rota
            result = self.routes[path](req, res)

            if isinstance(result, Response):
                # Caso 1: a função retornou diretamente um Response
                res = result
            else:
                # Caso 2: a função apenas modificou o res existente
                pass
        else:
            # Rota não encontrada -> 404
            res = Response(body="<h1>404 - Page Not Found</h1>", status=404)

        # Constrói a resposta HTTP final
        status_str, headers_list, body_bytes = res.to_wsgi()
        headers_str = "\r\n".join(f"{key}: {value}" for key, value in headers_list)
        return f"HTTP/1.1 {status_str}\r\n{headers_str}\r\n\r\n{body_bytes[0].decode('utf-8')}"
