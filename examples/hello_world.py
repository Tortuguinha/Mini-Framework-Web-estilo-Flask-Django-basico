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
# 🔹 Função auxiliar para templates
# ==============================
def render_template(filename, **context):
    """
    Lê um arquivo HTML da pasta templates e substitui placeholders do tipo {{ var }}
    - filename: nome do arquivo na pasta templates
    - context: dicionário com valores para substituir no template
    """
    path = os.path.join(os.path.dirname(__file__), "..", "templates", filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # Substitui {{ variavel }} pelos valores do contexto
    for key, value in context.items():
        content = content.replace(f"{{{{ {key} }}}}", str(value))
    return content

# ==============================
# 🟢 Estilo 1: modificando `res` diretamente
# ==============================
@app.route("/", methods=["GET"])
def home(req, res):
    """
    Página inicial (GET) usando template
    """
    res.body = render_template("home.html")
    res.set_header("Content-Type", "text/html; charset=utf-8")


@app.route("/about", methods=["GET"])
def about(req, res):
    """
    Página sobre (GET) usando template com placeholders
    """
    res.body = render_template(
        "about.html",
        framework_name="MiniWeb",
        framework_desc="Framework leve e rápido em Python"
    )
    res.set_header("Content-Type", "text/html; charset=utf-8")


# ==============================
# 🔵 Estilo 2: retornando Response
# ==============================
@app.route("/json", methods=["GET"])
def api(req, res):
    return Response.json({"message": "Hello API!", "ok": True})


@app.route("/plaintext", methods=["GET"])
def plaintext(req, res):
    return Response.text("MiniWeb rodando em modo texto simples ✅")


@app.route("/html", methods=["GET"])
def custom_html(req, res):
    """
    Retorna HTML usando template custom.html com placeholders
    """
    content = render_template(
        "custom.html",
        framework_name="MiniWeb",
        framework_desc="Framework leve e rápido em Python"
    )
    return Response.html(content)


# ==============================
# 📬 Exemplo POST e form data
# ==============================
@app.route("/submit", methods=["POST"])
def submit_form(req, res):
    name = req.form.get("name") or req.query.get("name") or "Visitante"
    return Response.json({"message": f"Olá, {name}!", "status": "sucesso"})


# ==============================
# 📬 Exemplo múltiplos métodos
# ==============================
@app.route("/multi", methods=["GET", "POST"])
def multi_method(req, res):
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
