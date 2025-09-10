from miniweb.app import App
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Cria a aplicação
app = App()

# Define uma rota para a página inicial
@app.route("/")
def home(req, res):
    res.body = "<h1>Bem-vindo ao MiniWeb!</h1>"
    res.set_header("Content-Type", "text/html")

@app.route("/about")
def about(req, res):
    res.body = "<h1>Sobre</h1><p>Mini framework em Python puro 🚀</p>"
    res.set_header("Content-Type", "text/html")

# Inicia o servidor
if __name__ == "__main__":
    app.run()
