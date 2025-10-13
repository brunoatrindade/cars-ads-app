from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Olá, Render! Meu primeiro app Flask está funcionando 🚀"

if __name__ == '__main__':
    app.run()
