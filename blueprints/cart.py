from flask import Blueprint, render_template, request, make_response, redirect
from datetime import datetime
import mysql.connector

# Blueprint名はcart
cart_bp = Blueprint("cart", __name__)


# ==============================
# カート追加処理('/add_to_cart')
# ==============================
@cart_bp.route("/add_to_cart")
def add_to_cart():

    # cookieからカート情報を取得。存在しない場合はNoneが格納される
    cart_item = request.cookies.get("cart_item")

    # 商品情報を取得
    product_id = request.args.get("product_id")
    quantity = int(request.args.get("quantity", 1))

    cart_dict = {}

    # カートが既にある場合
    if cart_item:
        items = cart_item.split(",")
        for item in items:
            pid, qty = item.split(":")
            cart_dict[pid] = int(qty)

    # 新しい商品を追加
    if product_id:
        if product_id in cart_dict:
            cart_dict[product_id] += int(quantity)
        else:
            cart_dict[product_id] = int(quantity)

    # 文字列に戻す
    new_cart = ",".join([f"{pid}:{qty}" for pid, qty in cart_dict.items()])

    # レスポンスオブジェクトを作成し、商品情報をテンプレートに渡す
    response = make_response(redirect("/cart"))
    # 商品情報をCookieに保存
    response.set_cookie("cart_item", new_cart, max_age=60 * 60 * 24 * 1)  # 1日間有効
    # レスポンスオブジェクトを返す
    return response


# ==============================
# カート表示処理('/cart')
# ==============================
@cart_bp.route("/cart")
def cart():

    # クッキーからユーザ情報を取得
    user_id = request.cookies.get("user_id")

    # cookieからカート情報を取得。存在しない場合はNoneが格納される
    cart_item = request.cookies.get("cart_item")

    cart_dict = {}

    # カートがある場合
    if cart_item:
        items = cart_item.split(",")
        for item in items:
            pid, qty = item.split(":")
            cart_dict[pid] = int(qty)

    # print(cart_dict)
    # こんな形{'1': 1, '4': 4, '3': 2}
    ids = cart_dict.keys()
    ids = ",".join(ids)
    print(ids)

    # カートが空の場合
    if not ids:
        return render_template("cart/cart.html", cart_items=[], user_id=user_id)

    # idに一致する商品情報を取得
    sql = f"""
        SELECT id, price, name, stock
        FROM t_product
        WHERE id IN ({ids});
    """
    con = connect_db()  # コネクション
    cur = con.cursor(dictionary=True)
    cur.execute(sql)
    cart_products = cur.fetchall()  # 検索結果を取得
    cur.close()
    con.close()  # コネクション

    if cart_products is None:
        err_msg = "商品情報が存在しません"
        return render_template("pages/error.html", err_msg=err_msg)

    # cart_products を ID をキーにした辞書に変換
    cart_products_dict = {p["id"]: p for p in cart_products}
    # cart_dict と結合して “カート商品リスト” を作る
    cart_items = []
    for pid_str, qty in cart_dict.items():
        pid = int(pid_str)  # cart_dict のキーは文字列なので int に変換
        product = cart_products_dict.get(pid)

        if product:
            cart_items.append(
                {
                    "id": pid,
                    "name": product["name"],
                    "price": product["price"],
                    "qty": qty,
                    "subtotal": product["price"] * qty,
                }
            )

    total = sum(item["subtotal"] for item in cart_items)

    # 商品情報をテンプレートに渡す
    return render_template(
        "cart/cart.html", cart_items=cart_items, total=total, user_id=user_id
    )

    # #レスポンスオブジェクトを作成し、商品情報をテンプレートに渡す
    # response = make_response(render_template('cart/cart.html',cart_items=cart_items,total=total,user_id=user_id))
    # #レスポンスオブジェクトを返す
    # return response


# ==============================
# カート削除('/remove_from_cart')
# ==============================
@cart_bp.route("/remove_from_cart")
def remove_from_cart():

    # cookieからカート情報を取得。存在しない場合はNoneが格納される
    cart_item = request.cookies.get("cart_item")

    print(cart_item)

    # 商品情報を取得
    product_id = request.args.get("product_id")
    print(product_id)

    cart_dict = {}

    # カートが既にある場合
    if cart_item:
        items = cart_item.split(",")
        for item in items:
            pid, qty = item.split(":")
            cart_dict[pid] = int(qty)

    print(cart_dict)

    # カートから削除
    if product_id in cart_dict:
        del cart_dict[product_id]

    # 文字列に戻す
    new_cart = ",".join([f"{pid}:{qty}" for pid, qty in cart_dict.items()])

    # レスポンスオブジェクトを作成し、商品情報をテンプレートに渡す
    response = make_response(redirect("/cart"))
    # 商品情報をCookieに保存
    response.set_cookie("cart_item", new_cart, max_age=60 * 60 * 24 * 1)  # 1日間有効
    # レスポンスオブジェクトを返す
    return response


# ==============================
# 購入画面表示('/purchase')
# ==============================
@cart_bp.route("/purchase")
def purchase():

    # cookieからカート情報を取得。存在しない場合はNoneが格納される
    cart_item = request.cookies.get("cart_item")
    cart_dict = {}

    # カートが既にある場合
    if cart_item:
        items = cart_item.split(",")
        for item in items:
            pid, qty = item.split(":")
            cart_dict[pid] = int(qty)

    # print(cart_dict)
    # こんな形{'1': 1, '4': 4, '3': 2}
    ids = cart_dict.keys()
    ids = ",".join(ids)
    print(ids)

    # idに一致する商品情報を取得
    sql = f"""
        SELECT id, price, name, stock
        FROM t_product
        WHERE id IN ({ids});
    """
    con = connect_db()  # コネクション
    cur = con.cursor(dictionary=True)
    cur.execute(sql)
    cart_products = cur.fetchall()  # 検索結果を取得
    cur.close()
    con.close()  # コネクション

    if cart_products is None:
        err_msg = "商品情報が存在しません"
        return render_template("pages/error.html", err_msg=err_msg)

    # cart_products を ID をキーにした辞書に変換
    cart_products_dict = {p["id"]: p for p in cart_products}
    # cart_dict と結合して “カート商品リスト” を作る
    cart_items = []
    for pid_str, qty in cart_dict.items():
        pid = int(pid_str)  # cart_dict のキーは文字列なので int に変換
        product = cart_products_dict.get(pid)

        if product:
            cart_items.append(
                {
                    "id": pid,
                    "name": product["name"],
                    "price": product["price"],
                    "qty": qty,
                    "subtotal": product["price"] * qty,
                }
            )

    total = sum(item["subtotal"] for item in cart_items)

    # クッキーからユーザ情報を取得
    user_id = request.cookies.get("user_id")
    print(user_id)

    # ログインしてない場合
    if user_id is None:
        return render_template(
            "cart/purchase.html", cart_items=cart_items, total=total, user_info=[]
        )

    # SELECTを作成
    sql = "SELECT id,name,tel,zip,address1,address2,address3 FROM t_member"
    sql = (
        sql + " WHERE id = '" + str(user_id) + "';"
    )  # WHERE等の予約文字の前には半角スペースをつける癖をつける
    print(sql)

    # DB接続処理
    con = connect_db()  # コネクション
    cur = con.cursor(dictionary=True)
    cur.execute(sql)
    user_info = cur.fetchone()  # 検索結果を取得
    cur.close()
    con.close()  # コネクション

    if user_info is None:
        err_msg = "ユーザIDが存在しません"
        return render_template("pages/error.html", err_msg=err_msg)

    # レスポンスオブジェクトを作成し、商品情報をテンプレートに渡す
    response = make_response(
        render_template(
            "cart/purchase.html",
            cart_items=cart_items,
            total=total,
            user_info=user_info,
        )
    )

    return response


# ==============================
# 購入処理('/add_purchase')
# ==============================
@cart_bp.route("/add_purchase", methods=["POST"])
def add_purchase():

    # フォームから取得
    member_id = request.form.get("member_id")
    orderer = request.form.get("orderer")
    mail = request.form.get("mail")
    tel = request.form.get("tel")
    zip = request.form.get("zip")
    address1 = request.form.get("address1")
    address2 = request.form.get("address2")
    address3 = request.form.get("address3")
    recipient = request.form.get("recipient")
    payment = request.form.get("payment")

    if not member_id:
        member_id = "NULL"
    else:
        member_id = f"'{member_id}'"

    if not address3:
        address3 = "NULL"
    else:
        address3 = f"'{address3}'"

    order_date = datetime.today().strftime("%Y-%m-%d")

    # SELECTを作成
    sql = "INSERT INTO t_order (order_date, member_id, orderer, mail, tel, zip, address1, address2, address3, recipient, payment, processing) VALUES ('"
    sql = (
        sql
        + str(order_date)
        + "', "
        + str(member_id)
        + ", '"
        + str(orderer)
        + "', '"
        + str(mail)
        + "', '"
        + str(tel)
        + "', '"
        + str(zip)
        + "', '"
        + str(address1)
        + "', '"
        + str(address2)
        + "', "
        + str(address3)
        + ", '"
        + str(recipient)
        + "', "
        + str(payment)
        + ", "
        + str(1)
        + ");"
    )
    print(sql)

    # DB接続
    con = connect_db()  # コネクション
    cur = con.cursor()
    # 注文テーブルにINSERT
    cur.execute(sql)

    order_id = cur.lastrowid  # 今作った注文ID

    # hiddenで送られてきた商品ID一覧
    product_ids = request.form.getlist("product_id")

    # 商品IDの数だけ繰り返す
    for pid in product_ids:
        # そのIDの購入数量を取得
        quantity = request.form.get(f"quantity_{pid}")

        # ① 注文明細テーブルにINSERT
        sql_order_detail = f"""
            INSERT INTO t_order_detail (order_id, product_id, quantity)
            VALUES ({order_id}, {pid}, {quantity});
        """
        cur.execute(sql_order_detail)

        # ② 商品テーブルの在庫を減らす
        sql_stock = f"""
            UPDATE t_product
            SET stock = stock - {quantity}
            WHERE id = {pid};
        """
        # sql_stock = f"""
        #     UPDATE t_product
        #     SET stock = stock - {quantity}
        #     WHERE id = {pid}
        #     AND stock >= {quantity};
        # """
        cur.execute(sql_stock)

    con.commit()

    # DB切断
    cur.close()
    con.close()  # コネクション

    # レスポンスオブジェクトを作成し、購入完了画面の表示関数にリダイレクト
    # カートは空にする
    response = make_response(redirect("/purchase_success"))
    response.delete_cookie("cart_item")
    return response


# ==============================
# 購入完了画面表示('/purchase_success')
# ==============================
@cart_bp.route("/purchase_success")
def purchase_success():
    # 購入完了画面を表示
    return render_template("cart/purchase_success.html")


# ==============================
# DB接続
# ==============================
def connect_db():
    return mysql.connector.connect(
        host="localhost", user="root", passwd="", db="db_mini_wallet_lab"
    )
