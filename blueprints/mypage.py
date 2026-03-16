from flask import Blueprint, render_template, request
import mysql.connector

# Blueprint名はsearch
mypage_bp = Blueprint("mypage", __name__)


# ==============================
# mypage画面表示処理('/mypage')
# ==============================
@mypage_bp.route("/mypage")
def mypage():

    # クッキーからユーザ情報を取得
    user_id = request.cookies.get("user_id")
    print(user_id)

    # ログインしてない場合
    if user_id is None:
        return render_template("mypage/mypage.html", user_info=[], history_info=[])

    # SELECTを作成
    sqlUser = "SELECT id,name,birthday,gender,tel,zip,address1,address2,address3,m_flag FROM t_member"
    sqlUser = (
        sqlUser + " WHERE id = '" + str(user_id) + "';"
    )  # WHERE等の予約文字の前には半角スペースをつける癖をつける
    print(sqlUser)

    # SELECTを作成
    sqlOrder = "SELECT id, order_date, member_id, orderer, mail, tel, zip, address1, address2, address3, recipient, payment, processing FROM t_order"
    sqlOrder = (
        sqlOrder + " WHERE member_id = '" + str(user_id) + "' ORDER BY id DESC;"
    )  # WHERE等の予約文字の前には半角スペースをつける癖をつける
    print(sqlOrder)

    sqlDetail = """
        SELECT
            od.order_id,
            p.name,
            od.quantity
        FROM t_order_detail od
        INNER JOIN t_product p
            ON od.product_id = p.id
        WHERE od.order_id = %s;
        """

    # DB接続処理
    con = connect_db()  # コネクション
    cur = con.cursor(dictionary=True)

    cur.execute(sqlUser)
    user_info = cur.fetchone()  # 検索結果を取得
    # 生年月日
    user_info["birthday_str"] = user_info["birthday"].strftime("%Y年%#m月%#d日")
    # 性別
    gender_map = {1: "男性", 2: "女性", 3: "その他"}
    user_info["gender_str"] = gender_map.get(user_info["gender"], "未設定")
    # メルマガ
    m_flag_map = {0: "受信しない", 1: "受信する"}
    user_info["m_flag_str"] = m_flag_map.get(user_info["m_flag"], "未設定")

    cur.execute(sqlOrder)
    orders = cur.fetchall()  # 検索結果を取得

    # 注文明細を取得
    order_history = []

    # if orders is None:
    #     order_history=[]
    # else:
    #     for order in orders:
    #         cur.execute(sqlDetail, (order["id"],))
    #         details = cur.fetchall()
    #         order_history.append({
    #             "order_id": order["id"],
    #             "order_date": order["order_date"],
    #             "items": details
    #         })

    for order in orders:
        cur.execute(sqlDetail, (order["id"],))
        details = cur.fetchall()
        order_history.append(
            {
                "order_id": order["id"],
                "order_date": order["order_date"],
                "order_items": details,
            }
        )

    # # 返り値
    # order_history = [
    # {
    #     "order_id": 3,
    #     "order_date": "2026-02-02",
    #     "items": [
    #         {"order_id": 3, "name": "Someday / Black", "quantity": 1},
    #         {"order_id": 3, "name": "Memory / Blue", "quantity": 2}
    #     ]
    # },
    # {
    #     "order_id": 1,
    #     "order_date": "2026-01-01",
    #     "items": [
    #         {"order_id": 1, "name": "Just Day / Brown", "quantity": 1}
    #     ]
    # }
    # ]

    cur.close()
    con.close()  # コネクション

    # 画面を表示
    return render_template(
        "mypage/mypage.html", user_info=user_info, order_history=order_history
    )


# ==============================
# DB接続
# ==============================
def connect_db():
    return mysql.connector.connect(
        host="localhost", user="root", passwd="", db="db_mini_wallet_lab"
    )
