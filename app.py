from flask import Flask
from flask_cors import CORS
from app.routes import routes_bp

app = Flask(__name__)
CORS(app)

# Rota de boas-vindas / checagem de status
@app.route('/', methods=['GET'])
def home():
    return {"status": "sucesso", "mensagem": "Backend rodando com sucesso!"}, 200

app.register_blueprint(routes_bp)

if __name__ == '__main__':
    print("\n==========================================")
    print("      BACKEND RODANDO COM SUCESSO!       ")
    print("==========================================\n")
    app.run(debug=True)
