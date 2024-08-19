from flask import Flask, request, redirect
import string
import random
from pymongo import MongoClient


app = Flask(__name__)


cliente = MongoClient('mongodb://localhost:27017/')
banco_de_dados = cliente['encurtador_url']
colecao_urls = banco_de_dados['urls']


def gerar_codigo_curto():
    caracteres = string.ascii_letters + string.digits
    return '' .join(random.choice(caracteres) for _ in range(6))



@app.route('/', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        url_original = request.form['url']
        if not url_original:
            return 'URL inválida', 400
        
        codigo_curto = gerar_codigo_curto()
        colecao_urls.insert_one({'original': url_original, 'curto': codigo_curto})
        
        url_curta = request.host_url +codigo_curto
        return f"URL encurtada: {url_curta}"
    return '''
        <form method='post'>
            URL: <input type='text' name='url'>
            <input type='submit' value='Encurtar'>
        </form>
    '''

@app.route('/<codigo_curto>')
def redirecionar_para_url( codigo_curto):
    documento_url = colecao_urls.find_one({'curto': codigo_curto})
    if documento_url:
        return redirect(documento_url['original'])
    return'URL não encontrada', 404


if __name__ == '__main__':
    app.run(debug=True)