# router.py

class Router:
    """
    Classe responsável por gerenciar todas as rotas da aplicação.
    - Permite registrar rotas para múltiplos métodos HTTP (GET, POST, etc.)
    - Resolve a função correta baseada no path e método da requisição.
    """

    def __init__(self):
        # Estrutura de dados:
        # {"path": {"GET": func, "POST": func, ...}}
        self.routes = {}

    def add_route(self, path, func, methods=None):
        """
        Registra uma rota.
        - path: URL da rota (ex: "/about")
        - func: função que será executada quando a rota for chamada
        - methods: lista de métodos HTTP permitidos (GET, POST, etc.)
        """
        methods = methods or ["GET"]  # Se não for especificado, assume GET

        if path not in self.routes:
            self.routes[path] = {}

        # Associa cada método à função da rota
        for method in methods:
            self.routes[path][method.upper()] = func

    def resolve(self, path, method):
        """
        Retorna a função registrada para a rota e método.
        - path: caminho da URL
        - method: método HTTP (GET, POST, etc.)
        Retorna None se a rota ou método não existir.
        """
        route_methods = self.routes.get(path)
        if route_methods:
            return route_methods.get(method.upper())
        return None
