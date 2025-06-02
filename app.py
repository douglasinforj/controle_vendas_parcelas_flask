from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

def conectar():
    return sqlite3.connect("database/vendas.db")

@app.route("/")
def index():
    return render_template("index.html")


#-------------------------Clientes---------------------------#

@app.route("/clientes")
def clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    lista = cursor.fetchall()
    conn.close()
    return render_template("clientes.html", clientes=lista)



@app.route("/clientes/novo", methods=["POST"])
def novo_cliente():
    nome = request.form["nome"]
    email = request.form["email"]
    telefone = request.form["telefone"]

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
                   (nome, email, telefone))
    conn.commit()
    conn.close()
    return redirect(url_for("clientes"))


@app.route("/clientes/<int:cliente_id>")
def cliente_detalhes(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()
    conn.close()
    return render_template("cliente_detalhes.html", cliente=cliente)


@app.route('/clientes/<int:id>/editar', methods=['GET', 'POST'])
def editar_cliente(id):
    conn = conectar()
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        cursor.execute("UPDATE clientes SET nome = ?, email = ?, telefone = ? WHERE id = ?", (nome, email, telefone, id))
        conn.commit()
        conn.close()
        return redirect('/clientes')
    
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (id,))
    cliente = cursor.fetchone()
    conn.close()
    return render_template('editar_cliente.html', cliente=cliente)


@app.route('/clientes/<int:id>/excluir')
def excluir_cliente(id):
    conn = sqlite3.connect('database/vendas.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/clientes')




if __name__ == '__main__':
    app.run(debug=True)

