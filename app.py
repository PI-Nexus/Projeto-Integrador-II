import os
from flask import Flask, render_template
from flask_cors import CORS
from app.routes import routes_bp

# Mapeia os caminhos absolutos para as pastas frontend
base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'frontend', 'templates')
static_dir = os.path.join(base_dir, 'frontend', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
CORS(app)

# Rota principal para carregar o index.html
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Registra as demais rotas do projeto
app.register_blueprint(routes_bp)

if __name__ == '__main__':
    print("\n=============================================")
    print("      BACKEND RODANDO COM SUCESSO!           ")
    print("=============================================\n")
    app.run(debug=True, port=5000)