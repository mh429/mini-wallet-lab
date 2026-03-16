from flask import Blueprint, render_template, request, make_response, redirect
from datetime import datetime
import mysql.connector

# Blueprint名はadmin
admin_bp = Blueprint("admin", __name__)


# ==============================
# admin_login画面表示処理('/admin_login')
# ==============================
@admin_bp.route("/admin_login")
def admin_login():
  # 画面を表示
  return render_template("admin/admin_login.html")


# ================================================
# ログイン処理('/admin_login_process')
# ================================================
@admin_bp.route("/admin_login_process", methods=["POST"])
def admin_login_process():
  # フォームからユーザー名を取得
  print(request.form)
  admin_id = request.form.get("admin_id")
  print(admin_id)
  password = request.form.get("password")

  # 未入力チェック
  if admin_id == "" or password == "":
    err_msg = "管理者ID　または　パスワードが未入力です"
    return render_template("pages/error.html", err_msg=err_msg)

  # SELECTを作成
  sql = "SELECT id,pass,name FROM t_admin"
  sql = (
    sql + " WHERE id = '" + str(admin_id) + "';"
  )
  print(sql)

  # DB接続処理
  con = connect_db()  # コネクション
  cur = con.cursor(dictionary=True)
  cur.execute(sql)
  admin_info = cur.fetchone()  # 検索結果を取得
  cur.close()
  con.close()  # コネクション

  if admin_info is None:
    err_msg = "管理者IDが存在しません"
    return render_template("pages/error.html", err_msg=err_msg)
  elif admin_info["pass"] != password:
    err_msg = "パスワードが違います"
    return render_template("pages/error.html", err_msg=err_msg)
  else:
    # レスポンスオブジェクトを作成
    response = make_response(redirect("/admin_top"))
    # # 管理者名をCookieに保存
    # response.set_cookie(
    #   "admin_name", admin_info["name"], max_age=60 * 60 * 1
    # )  # 1時間有効
    # レスポンスオブジェクトを返す
    return response


# ==============================
# 管理者トップ画面表示処理('/admin_top')
# ==============================
@admin_bp.route("/admin_top")
def admin_top():
  # クッキーからユーザ情報を取得
  admin_name = request.cookies.get("admin_name")

  # 今日の日付取得
  today = datetime.now()
  # 曜日配列
  week = ["月", "火", "水", "木", "金", "土", "日"]
  # 表示用フォーマット作成
  today_str = f"{today.year}年{today.month}月{today.day}日（{week[today.weekday()]}）"

  # SQL作成(受注処理待ち)
  order_processing_pending_sql = """
    SELECT COUNT(*) AS count
    FROM t_order
    WHERE processing = 1;
  """
  # SQL作成(発送待ち)
  waiting_for_shipment_sql = """
    SELECT COUNT(*) AS count
    FROM t_order
    WHERE processing = 2;
  """
  con = connect_db()  # コネクション
  cur = con.cursor(dictionary=True)

  cur.execute(order_processing_pending_sql)
  wait_process = cur.fetchone()["count"]  # 受注処理待ち件数を取得

  cur.execute(waiting_for_shipment_sql)
  wait_send = cur.fetchone()["count"]  # 発送待ち件数を取得

  cur.close()
  con.close()  # コネクション

  # 注文情報をテンプレートに渡す
  return render_template(
    "admin/admin_top.html", 
    wait_process=wait_process, 
    wait_send=wait_send, 
    admin_name=admin_name,
    today=today_str
  )

# ================================================
# 注文情報画面表示('/admin_order')
# ================================================
@admin_bp.route("/admin_order")
def admin_order():
  # SQL作成
  sql = """
    SELECT id,order_date,orderer,payment,processing
    FROM t_order
    ORDER BY id DESC
  """
  con = connect_db()  # コネクション
  cur = con.cursor(dictionary=True)
  cur.execute(sql)
  order = cur.fetchall() # 注文情報を取得
  cur.close()
  con.close()  # コネクション  

  # 支払い方法
  payment_map = {1: "クレジットカード", 2: "電子決済", 3: "銀行振込"}
  # 処理状況
  processing_map = {0: "キャンセル", 1: "受注処理待ち", 2: "発送待ち", 3: "完了"}

  for o in order:
    o["payment_str"] = payment_map.get(o["payment"], "未設定")
    o["processing_str"] = processing_map.get(o["processing"], "未設定")
    o["order_date"] = o["order_date"].strftime("%Y年%#m月%#d日")

  # 注文情報をテンプレートに渡す
  return render_template(
    "admin/admin_order.html", 
    order=order
  )

# ================================================
# 注文詳細情報画面表示('/admin_order_detail')
# ================================================
@admin_bp.route("/admin_order_detail/<int:order_id>")
def admin_order_detail(order_id):

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
    "admin/admin_order_detail.html", 
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
