from flask import Blueprint, render_template, request
import mysql.connector

# Blueprint名はsearch
search_bp = Blueprint("search", __name__)


# ==============================
# search画面表示処理('/search')
# ==============================
@search_bp.route("/search")
def search():

    search_text = request.args.get("search_text")

    # SQL作成
    sql = """
        SELECT p.id, p.price, s.series, c.color, p.color_detail, p.stock, p.image_path
        FROM t_product p
        INNER JOIN t_series s
        ON p.series_id = s.id
        INNER JOIN t_color c
        ON p.color_id = c.id
        WHERE p.is_active = 1
        AND (
            p.name LIKE %s
            OR s.series LIKE %s
            OR c.color LIKE %s
            OR p.color_detail LIKE %s
            OR p.search_key LIKE %s
        );
    """

    param = (
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%",
    )

    con = connect_db()  # コネクション
    cur = con.cursor(dictionary=True)
    cur.execute(sql, param)
    products = cur.fetchall()  # 検索結果を取得
    cur.close()
    con.close()  # コネクション

    # 画面を表示
    return render_template(
        "search/search.html", products=products, search_text=search_text
    )


# ==============================
# DB接続
# ==============================
def connect_db():
    return mysql.connector.connect(
        host="localhost", user="root", passwd="", db="db_mini_wallet_lab"
    )
