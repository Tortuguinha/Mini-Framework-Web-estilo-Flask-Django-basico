from miniweb.app import App
from miniweb.response import Response  # ✅ Import necessário para retornar Response direto
import sys, os

# Ajuste do path para garantir que "miniweb" seja encontrado
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ==============================
# 🚀 Criação da aplicação
# ==============================
app = App()

# ==============================
# 🟢 Estilo 1: modificando `res`
# ==============================
@app.route("/")
def home(req, res):
    """
    Exemplo de rota que **modifica o objeto `res` diretamente**.
    """
    res.body = "<h1>Bem-vindo ao MiniWeb!</h1>"
    res.set_header("Content-Type", "text/html")


@app.route("/about")
def about(req, res):
    """
    Outra rota no estilo clássico: apenas ajusta `res`.
    """
    res.body = "<h1>Sobre</h1><p>Mini framework em Python puro 🚀</p>"
    res.set_header("Content-Type", "text/html")


# ==============================
# 🔵 Estilo 2: retornando Response
# ==============================
@app.route("/json")
def api(req, res):
    """
    Exemplo de rota que retorna um `Response` JSON diretamente.
    """
    return Response.json({"message": "Hello API!", "ok": True})


@app.route("/plaintext")
def plaintext(req, res):
    """
    Exemplo de rota que retorna texto puro direto.
    """
    return Response.text("MiniWeb rodando em modo texto simples ✅")


@app.route("/html")
def custom_html(req, res):
    """
    Exemplo de rota que retorna HTML direto via helper.
    """
    return Response.html("<h2>Página gerada com Response.html()</h2>")


# ==============================
# ▶️ Inicialização do servidor
# ==============================
if __name__ == "__main__":
    app.run()
