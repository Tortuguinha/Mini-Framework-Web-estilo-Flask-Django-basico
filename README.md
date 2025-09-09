project:
  name: "MiniWeb"
  description: >
    Um framework web minimalista em Python puro, inspirado em Flask e Django,
    criado do zero para aprendizado e portfólio.
  features:
    - Sistema de rotas (/home, /about, /user/<id>)
    - Objetos Request e Response
    - Suporte a middlewares
    - Renderização de templates HTML
    - Servidor HTTP básico em Python puro
  structure:
    - miniweb/
    - miniweb/__init__.py
    - miniweb/app.py         # Classe principal App
    - miniweb/router.py      # Sistema de rotas
    - miniweb/request.py     # Objeto Request
    - miniweb/response.py    # Objeto Response
    - miniweb/middleware.py  # Middlewares
    - miniweb/templates.py   # Engine de templates
    - examples/hello_world.py
    - tests/
    - README.md
    - setup.py
  installation:
    steps:
      - git clone https://github.com/seu-usuario/miniweb.git
      - cd miniweb
      - python -m venv venv
      - source venv/bin/activate   # Linux/Mac
      - venv\Scripts\activate      # Windows
      - python examples/hello_world.py
  usage_example: |
    from miniweb import App

    app = App()

    @app.route("/")
    def home(req, res):
        res.text = "Bem-vindo ao MiniWeb!"

    @app.route("/about")
    def about(req, res):
        res.html = app.render("about.html", {"name": "Tortuga"})

    if __name__ == "__main__":
        app.run()
  goals:
    - Exercício prático de arquitetura de software
    - Entender conceitos por trás de frameworks web modernos
  roadmap:
    - Suporte a rotas dinâmicas (/user/<id>)
    - Middleware de autenticação
    - Templates mais avançados
    - Tratamento de erros (404, 500)
    - Publicação no PyPI
  author:
    name: "Tortuga"
    github: "https://github.com/Tortuguinha"
