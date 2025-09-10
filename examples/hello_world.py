# hello_world.py
from miniweb.app import App
from miniweb.response import Response
import sys, os

# Ajusta path para garantir que o pacote "miniweb" seja encontrado
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ==============================
# 🚀 Criação da aplicação
# ==============================
app = App()

# ==============================
# 🟢 Estilo 1: modificando `res` diretamente
# ==============================
@app.route("/", methods=["GET"])
def home(req, res):
    """
    Página inicial (GET)
    Modifica o objeto `res` diretamente.
    """
    res.body = """
    <html>
    <head>
        <title>MiniWeb Home</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f0f0f0; color: #333; text-align: center; }
            h1 { color: #4CAF50; margin-top: 50px; }
            p { font-size: 1.2em; }
            a { color: #2196F3; text-decoration: none; margin: 0 10px; }
            a:hover { text-decoration: underline; }
            .nav { margin-top: 20px; }
        </style>
    </head>
    <body>
        <h1>Bem-vindo ao MiniWeb!</h1>
        <p>Framework leve e rápido em Python 🚀</p>
        <div class="nav">
            <a href="/">Home</a>
            <a href="/about">Sobre</a>
            <a href="/html">HTML</a>
            <a href="/json">JSON</a>
            <a href="/plaintext">Texto</a>
        </div>
    </body>
    </html>
    """
    res.set_header("Content-Type", "text/html")


@app.route("/about", methods=["GET"])
def about(req, res):
    """
    Página sobre (GET)
    Também altera `res`.
    """
    res.body = """
    <html>
    <head>
        <meta charset="UTF-8">  <!-- Adicione esta linha -->
        <title>MiniWeb Home</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f0f0f0; color: #333; text-align: center; }
            h1 { color: #4CAF50; margin-top: 50px; }
            p { font-size: 1.2em; }
            a { color: #2196F3; text-decoration: none; margin: 0 10px; }
            a:hover { text-decoration: underline; }
            .nav { margin-top: 20px; }
        </style>
    </head>
    <body>
        <h1>Bem-vindo ao MiniWeb!</h1>
        <p>Framework leve e rápido em Python 🚀</p>
        <div class="nav">
            <a href="/">Home</a>
            <a href="/about">Sobre</a>
            <a href="/html">HTML</a>
            <a href="/json">JSON</a>
            <a href="/plaintext">Texto</a>
        </div>
    </body>
    </html>
    """
    res.set_header("Content-Type", "text/html; charset=utf-8")  # Certifique-se de manter UTF-8


# ==============================
# 🔵 Estilo 2: retornando Response
# ==============================
@app.route("/json", methods=["GET"])
def api(req, res):
    """
    Retorna JSON diretamente usando Response.json()
    """
    return Response.json({"message": "Hello API!", "ok": True})


@app.route("/plaintext", methods=["GET"])
def plaintext(req, res):
    """
    Retorna texto puro
    """
    return Response.text("MiniWeb rodando em modo texto simples ✅")


@app.route("/html", methods=["GET"])
def custom_html(req, res):
    """
    Retorna HTML usando helper Response.html()
    """
    content = """
    <html>
    <head>
        <title>Página HTML</title>
        <style>
            body { font-family: 'Courier New', monospace; background: #e0f7fa; color: #00796B; text-align: center; }
            h2 { margin-top: 50px; }
            p { font-size: 1.1em; }
        </style>
    </head>
    <body>
        <h2>Página gerada com Response.html()</h2>
        <p>Exemplo de HTML estilizado inline</p>
        <a href="/">Voltar</a>
    </body>
    </html>
    """
    return Response.html(content)


# ==============================
# 📬 Exemplo POST e form data
# ==============================
@app.route("/submit", methods=["POST"])
def submit_form(req, res):
    """
    Recebe dados de formulário via POST e retorna JSON
    """
    # Captura valores do formulário (POST) ou query string (GET)
    name = req.form.get("name") or req.query.get("name") or "Visitante"
    return Response.json({"message": f"Olá, {name}!", "status": "sucesso"})


# ==============================
# 📬 Exemplo múltiplos métodos
# ==============================
@app.route("/multi", methods=["GET", "POST"])
def multi_method(req, res):
    """
    Demonstra suporte a múltiplos métodos HTTP
    """
    if req.method == "GET":
        return Response.text("Você fez um GET nesta rota!")
    elif req.method == "POST":
        data = req.form.get("data", "nenhum dado")
        return Response.json({"mensagem": f"POST recebido: {data}"})


# ==============================
# ▶️ Inicialização do servidor
# ==============================
if __name__ == "__main__":
    app.run()
