from flask import Flask, render_template, redirect, url_for, request, jsonify
import sqlite3
import os
from extrair import ExtrairArquivofuncao

app = Flask(__name__)



@app.route('/')
def index():
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'NF.db')

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS dados (
                    N INTEGER,
                    Campo TEXT,
                    Descricao TEXT,
                    Tipo TEXT,
                    Tam TEXT,
                    Dec TEXT,
                    Entr TEXT,
                    Saida TEXT
                )
            ''')
        cursor.execute('SELECT * FROM dados')
        rows = cursor.fetchall()
        conn.close()

        return render_template('index.html', rows=rows)

    except Exception as e:
        return f"Erro: {str(e)}"

@app.route('/atualizar-dados-da-tabela', methods=['POST'])
def AtualizarDados():
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'NF.db')

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM dados')
        conn.commit()
        conn.close()

        ExtrairArquivofuncao()

        return redirect(url_for('index'))

    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/deletar-dados-da-tabela', methods=['POST'])
def DeletarDadosTabela():
    try:
        selected_ids = request.json.get('selected_ids')
        db_path = os.path.join(os.path.dirname(__file__), 'NF.db')
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            for selected_id in selected_ids:
                cursor.execute('DELETE FROM dados WHERE N = ?', (selected_id,))

            conn.commit()

        return jsonify({"success": True}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)