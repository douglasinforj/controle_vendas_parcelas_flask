import sqlite3

caminho_banco = 'database/vendas.db'

caminho_schema = 'schema.sql'

def inicializar_banco():
    with open(caminho_schema, 'r', encoding='utf-8') as f:
        schema = f.read()
    
    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    conn.close()
    print("Banco de dados criado com sucesso!")

if __name__ == '__main__':
    inicializar_banco()