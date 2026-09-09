"""
CRUD Genérico - API REST com Flask + SQLite (SQL puro)
--------------------------------------------------------
Projeto de portfólio: sistema CRUD (Create, Read, Update, Delete)
genérico de "Itens", pensado para ser facilmente adaptado para
qualquer outra entidade (produtos, clientes, tarefas, etc).

Usa sqlite3 (biblioteca padrão do Python) com SQL puro, sem ORM,
para deixar explícito o funcionamento das queries.

Autor: Jadinei G. Xavier
"""

import os
import sqlite3
from datetime import datetime, timezone

from flask import Flask, request, jsonify, render_template, g

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")

app = Flask(__name__)


# ------------------------------------------------------------------
# Conexão com o banco de dados
# ------------------------------------------------------------------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def fechar_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def criar_banco():
    with app.app_context():
        db = get_db()
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS itens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                quantidade INTEGER NOT NULL DEFAULT 0,
                criado_em TEXT NOT NULL,
                atualizado_em TEXT NOT NULL
            )
            """
        )
        db.commit()


def agora_iso():
    return datetime.now(timezone.utc).isoformat()


def item_para_dict(row):
    return {
        "id": row["id"],
        "nome": row["nome"],
        "descricao": row["descricao"],
        "quantidade": row["quantidade"],
        "criado_em": row["criado_em"],
        "atualizado_em": row["atualizado_em"],
    }


# ------------------------------------------------------------------
# Rota da interface (frontend simples)
# ------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# ------------------------------------------------------------------
# API REST - CRUD de Itens
# ------------------------------------------------------------------

@app.route("/api/itens", methods=["GET"])
def listar_itens():
    """Lista todos os itens. Suporta busca opcional via ?q=texto"""
    query = request.args.get("q", "").strip()
    db = get_db()

    if query:
        linhas = db.execute(
            "SELECT * FROM itens WHERE nome LIKE ? ORDER BY id DESC",
            (f"%{query}%",),
        ).fetchall()
    else:
        linhas = db.execute("SELECT * FROM itens ORDER BY id DESC").fetchall()

    return jsonify([item_para_dict(linha) for linha in linhas]), 200


@app.route("/api/itens/<int:item_id>", methods=["GET"])
def obter_item(item_id):
    """Retorna um único item pelo ID."""
    db = get_db()
    linha = db.execute("SELECT * FROM itens WHERE id = ?", (item_id,)).fetchone()
    if not linha:
        return jsonify({"erro": "Item não encontrado"}), 404
    return jsonify(item_para_dict(linha)), 200


@app.route("/api/itens", methods=["POST"])
def criar_item():
    """Cria um novo item."""
    dados = request.get_json(silent=True) or {}

    nome = (dados.get("nome") or "").strip()
    if not nome:
        return jsonify({"erro": "O campo 'nome' é obrigatório"}), 400

    try:
        quantidade = int(dados.get("quantidade", 0))
    except (ValueError, TypeError):
        return jsonify({"erro": "Valor inválido para 'quantidade'"}), 400

    descricao = (dados.get("descricao") or "").strip() or None
    agora = agora_iso()

    db = get_db()
    try:
        cursor = db.execute(
            """
            INSERT INTO itens (nome, descricao, quantidade, criado_em, atualizado_em)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nome, descricao, quantidade, agora, agora),
        )
        db.commit()
        novo_id = cursor.lastrowid
    except sqlite3.Error:
        db.rollback()
        return jsonify({"erro": "Erro ao salvar no banco de dados"}), 500

    linha = db.execute("SELECT * FROM itens WHERE id = ?", (novo_id,)).fetchone()
    return jsonify(item_para_dict(linha)), 201


@app.route("/api/itens/<int:item_id>", methods=["PUT"])
def atualizar_item(item_id):
    """Atualiza um item existente (atualização total/parcial)."""
    db = get_db()
    linha = db.execute("SELECT * FROM itens WHERE id = ?", (item_id,)).fetchone()
    if not linha:
        return jsonify({"erro": "Item não encontrado"}), 404

    dados = request.get_json(silent=True) or {}

    nome = linha["nome"]
    descricao = linha["descricao"]
    quantidade = linha["quantidade"]

    if "nome" in dados:
        novo_nome = (dados["nome"] or "").strip()
        if not novo_nome:
            return jsonify({"erro": "O campo 'nome' não pode ficar vazio"}), 400
        nome = novo_nome

    if "descricao" in dados:
        descricao = (dados["descricao"] or "").strip() or None

    if "quantidade" in dados:
        try:
            quantidade = int(dados["quantidade"])
        except (ValueError, TypeError):
            return jsonify({"erro": "Valor inválido para 'quantidade'"}), 400

    try:
        db.execute(
            """
            UPDATE itens
            SET nome = ?, descricao = ?, quantidade = ?, atualizado_em = ?
            WHERE id = ?
            """,
            (nome, descricao, quantidade, agora_iso(), item_id),
        )
        db.commit()
    except sqlite3.Error:
        db.rollback()
        return jsonify({"erro": "Erro ao atualizar no banco de dados"}), 500

    linha_atualizada = db.execute(
        "SELECT * FROM itens WHERE id = ?", (item_id,)
    ).fetchone()
    return jsonify(item_para_dict(linha_atualizada)), 200


@app.route("/api/itens/<int:item_id>", methods=["DELETE"])
def deletar_item(item_id):
    """Remove um item pelo ID."""
    db = get_db()
    linha = db.execute("SELECT * FROM itens WHERE id = ?", (item_id,)).fetchone()
    if not linha:
        return jsonify({"erro": "Item não encontrado"}), 404

    try:
        db.execute("DELETE FROM itens WHERE id = ?", (item_id,))
        db.commit()
    except sqlite3.Error:
        db.rollback()
        return jsonify({"erro": "Erro ao remover do banco de dados"}), 500

    return jsonify({"mensagem": "Item removido com sucesso"}), 200


# ------------------------------------------------------------------
# Tratamento de erros genéricos
# ------------------------------------------------------------------
@app.errorhandler(404)
def rota_nao_encontrada(e):
    if request.path.startswith("/api/"):
        return jsonify({"erro": "Rota não encontrada"}), 404
    return e


# ------------------------------------------------------------------
# Inicialização
# ------------------------------------------------------------------
if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)
