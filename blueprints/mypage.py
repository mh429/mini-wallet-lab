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
    return render_template("mypage/mypage.html", user_info=[], orders=[])

  # ユーザ情報のSQL
  sqlUser = """
    SELECT
      id,
      name,
      birthday,
      gender,
      tel,
      zip,
      address1,
      address2,
      address3,
      m_flag
    FROM t_member
    WHERE id = %s;
    """

  # 注文情報のSQL
  sqlOrder = """
    SELECT
      id,
      order_date,
      processing
    FROM t_order
    WHERE member_id = %s
    ORDER BY id DESC;
    """

  # DB接続処理
  con = connect_db()  # コネクション
  cur = con.cursor(dictionary=True)

  # ユーザ情報を取得
  cur.execute(sqlUser, (user_id,))
  user_info = cur.fetchone()
  # 生年月日
  user_info["birthday_str"] = user_info["birthday"].strftime("%Y年%#m月%#d日")
  # 性別
  gender_map = {1: "男性", 2: "女性", 3: "その他"}
  user_info["gender_str"] = gender_map.get(user_info["gender"], "未設定")
  # メルマガ
  m_flag_map = {0: "受信しない", 1: "受信する"}
  user_info["m_flag_str"] = m_flag_map.get(user_info["m_flag"], "未設定")

  # 注文情報を取得
  cur.execute(sqlOrder, (user_id,))
  orders = cur.fetchall()
  # 変換
  for order in orders:
    # 注文日
    order["order_date_str"] = order["order_date"].strftime("%Y年%#m月%#d日")
    # 注文ステータス
    processing_map = {1: "受注処理待ち", 2: "発送待ち", 3: "発送済み", 0: "キャンセル"}
    order["processing"] = processing_map.get(order["processing"], "未設定")

  cur.close()
  con.close()  # コネクション

  # 画面を表示
  return render_template(
      "mypage/mypage.html", user_info=user_info, orders=orders
  )

# ================================================
# 注文詳細情報画面表示('/mypage_order_detail')
# ================================================
@mypage_bp.route("/mypage_order_detail/<int:order_id>")
def mypage_order_detail(order_id):

  # 注文情報
  sql = """
    SELECT *
    FROM t_order
    WHERE id = %s;
  """

  # 注文明細
  sqlDetail = """
    SELECT
      od.product_id,
      od.quantity,
      p.name,
      p.price
    FROM t_order_detail od
    INNER JOIN t_product p
      ON od.product_id = p.id
    WHERE od.order_id = %s;
    """

  con = connect_db()  # コネクション
  cur = con.cursor(dictionary=True)

  cur.execute(sql, (order_id,))
  order = cur.fetchone() # 注文情報を取得

  cur.execute(sqlDetail, (order_id,))
  order_detail = cur.fetchall() # 注文明細を取得

  cur.close()
  con.close()  # コネクション  

  print(order_detail)

  # 支払い方法
  payment_map = {1: "クレジットカード", 2: "電子決済", 3: "銀行振込"}
  order["payment_str"] = payment_map.get(order["payment"], "未設定")
  # 注文日
  order["order_date"] = order["order_date"].strftime("%Y年%#m月%#d日")

  # 小計と合計
  total = 0
  for item in order_detail:
    item["subtotal"] = item["price"] * item["quantity"]
    total += item["subtotal"]

  # 注文情報をテンプレートに渡す
  return render_template(
    "mypage/mypage_order_detail.html", 
    order=order,
    order_detail=order_detail,
    total=total
  )

# ==============================
# DB接続
# ==============================
def connect_db():
  return mysql.connector.connect(
    host="localhost", user="root", passwd="", db="db_mini_wallet_lab"
  )
