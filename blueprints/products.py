from flask import Blueprint, render_template, request
import mysql.connector

# Blueprint名はproducts
products_bp = Blueprint('products',__name__)


# ==============================
# 商品一覧処理('/products')
# ==============================
@products_bp.route('/products')
def products():
    
    #SQL作成
    sql = """
        SELECT p.id, p.price, s.series, c.color, p.color_detail, p.stock, p.image_path
        FROM t_product p
        INNER JOIN t_series s
        ON p.series_id = s.id
        INNER JOIN t_color c
        ON p.color_id = c.id
        WHERE p.is_active = 1;
    """

    con = connect_db()#コネクション
    cur = con.cursor(dictionary=True)
    cur.execute(sql)
    products=cur.fetchall()#検索結果を取得
    cur.close()
    con.close()#コネクション

    # if products is None:
    if not products:
        #エラーメッセージ
        err_msg = "商品情報が存在しません"
        return render_template('pages/error.html',err_msg=err_msg)
    
    #結果出力処理
    return render_template('products/products.html',products=products)

# ==============================
# 商品詳細取得処理('/products/<product_id>')
# ==============================
@products_bp.route('/products/<int:product_id>')
def product_detail(product_id):

    sql = """
        SELECT p.id, p.price, s.series, c.color, p.color_detail, p.caption, p.stock, p.image_path
        FROM t_product p
        INNER JOIN t_series s
        ON p.series_id = s.id
        INNER JOIN t_color c
        ON p.color_id = c.id
        WHERE p.id = %s;
    """

    con = connect_db()#コネクション
    cur = con.cursor(dictionary=True)
    cur.execute(sql, (product_id,))
    product=cur.fetchone()  #検索結果を取得
    cur.close()
    con.close()     #コネクション

    if product is None:
        err_msg = "商品情報が存在しません"
        return render_template('pages/error.html',err_msg=err_msg)

    return render_template('products/product_detail.html',product=product)


# ==============================
# DB接続
# ==============================
def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        db='db_mini_wallet_lab'
    )