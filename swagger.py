from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_restx import Api, Resource
import sqlite3
import os
from extrair import ExtrairArquivofuncao

app = Flask(__name__)
api = Api(app, version='1.0', title='API de Dados', description='API para gerenciamento de dados')

# Defina o namespace para a API
ns = api.namespace('dados', description='Operações relacionadas aos dados')

@ns.route('/')
class DadosResource(Resource):
    def get(self):
        """
        Retorna todos os dados.
        """
        try:
            db_path = os.path.join(os.path.dirname(__file__), 'NF.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM dados')
            rows = cursor.fetchall()
            conn.close()

            return jsonify(rows)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def post(self):
        """
        Atualiza os dados da tabela.
        """
        try:
            db_path = os.path.join(os.path.dirname(__file__), 'NF.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM dados')
            conn.commit()
            conn.close()

            ExtrairArquivofuncao()

            return redirect(url_for('dadosresource'))

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def delete(self):
        """
        Deleta dados da tabela.
        """
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
