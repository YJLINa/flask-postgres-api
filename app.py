from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# PostgreSQL 設定（Render 從環境變數注入）
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "port": os.getenv("DB_PORT", 5432)
}

def query_postgres(sql_query):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(sql_query)
    colnames = [desc[0] for desc in cur.description]
    rows = [dict(zip(colnames, row)) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return rows

@app.route("/query", methods=["GET"])
def query():
    sql = request.args.get("q")
    if not sql:
        return jsonify({"error": "請提供查詢參數 ?q=SQL 語句"}), 400

    # 簡單限制：不允許動詞（防刪表、改表）
    blocked = ["drop", "update", "delete", "insert", "alter"]
    if any(word in sql.lower() for word in blocked):
        return jsonify({"error": "不允許修改資料的 SQL"}), 400

    # 限定只能查某一張表
    if "from nj_asm_rawdata" not in sql.lower():
        return jsonify({"error": "僅允許查詢 nj_asm_rawdata 資料表"}), 400

    try:
        data = query_postgres(sql)
        return jsonify({
            "query": sql,
            "result_count": len(data),
            "result": data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "PostgreSQL Copilot API is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
