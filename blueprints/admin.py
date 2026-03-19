from flask import Blueprint, render_template, request, make_response, redirect
from datetime import datetime
import mysql.connector
import os
import glob
from flask import flash

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

# ================================================
# 注文ステータス更新('/admin_update_processing')
# ================================================
@admin_bp.route("/admin_update_processing", methods=["POST"])
def admin_update_processing():

  # フォームから取得
  order_id = request.form.get("order_id")
  processing = request.form.get("processing")

  # SQL作成
  sql = """
    UPDATE t_order
    SET processing = %s
    WHERE id = %s;
  """
  con = connect_db()  # コネクション
  cur = con.cursor(dictionary=True)
  cur.execute(sql, (processing, order_id))
  con.commit()
  cur.close()
  con.close()  # コネクション  

  response = make_response(redirect("/admin_order"))
  return response

# ================================================
# 会員情報画面表示('/admin_member_info')
# ================================================
@admin_bp.route("/admin_member_info")
def admin_member_info():

  # SQL作成
  sql = """
    SELECT *
    FROM t_member
  """
  con = connect_db()  # コネクション
  cur = con.cursor(dictionary=True)
  cur.execute(sql)
  member_info = cur.fetchall()
  cur.close()
  con.close()  # コネクション  

  for member in member_info:
    # 生年月日
    member["birthday_str"] = member["birthday"].strftime("%Y年%#m月%#d日")
    # 性別
    gender_map = {1: "男性", 2: "女性", 3: "その他"}
    member["gender_str"] = gender_map.get(member["gender"], "未設定")
    # メルマガ
    m_flag_map = {0: "受信しない", 1: "受信する"}
    member["m_flag_str"] = m_flag_map.get(member["m_flag"], "未設定")

  # 会員情報をテンプレートに渡す
  return render_template(
    "admin/admin_member_info.html", 
    member_info=member_info
  )

# ================================================
# 管理者情報画面表示('/admin_staff_info')
# ================================================
@admin_bp.route("/admin_staff_info")
def admin_staff_info():

  # SQL作成
  sql = """
    SELECT id,name
    FROM t_admin
  """
  con = connect_db()  # コネクション
  cur = con.cursor(dictionary=True)
  cur.execute(sql)
  staff_info = cur.fetchall()
  cur.close()
  con.close()  # コネクション  

  # 会員情報をテンプレートに渡す
  return render_template(
    "admin/admin_staff_info.html", 
    staff_info=staff_info
  )

# ================================================
# 新規管理者登録('/admin_add_staff')
# ================================================
@admin_bp.route("/admin_add_staff", methods=["POST"])
def admin_add_staff():

  # フォームから取得
  staff_name = request.form.get("staff_name")
  staff_id = request.form.get("staff_id")
  password = request.form.get("pass")
  pass_confirm = request.form.get("pass_confirm")

  # pass一致チェック
  if password != pass_confirm:
      err_msg = "パスワードが一致しません"
      return render_template('pages/error.html',err_msg = err_msg)

  # SQL作成
  sql = """
    INSERT INTO t_admin(id, pass, name, authority)
    VALUES (%s, %s, %s, %s);
  """

  con = connect_db()  # コネクション
  cur = con.cursor(dictionary=True)
  cur.execute(sql,(staff_id,password,staff_name,1))
  con.commit()  # コネクション
  cur.close()
  con.close()  # コネクション  

  response = make_response(redirect("/admin_staff_info"))
  return response

# ================================================
# 商品情報画面表示('/admin_products')
# ================================================
@admin_bp.route("/admin_products")
def admin_products():

  # SQL作成
  sql = """
    SELECT *
    FROM t_product
    ORDER BY id DESC
  """
  con = connect_db()  # コネクション
  cur = con.cursor(dictionary=True)
  cur.execute(sql)
  products = cur.fetchall()
  cur.close()
  con.close()  # コネクション  

  for product in products:
    # 状態
    is_active_map = {1: "公開", 0: "非公開"}
    product["is_active_str"] = is_active_map.get(product["is_active"], "未設定")


  # 会員情報をテンプレートに渡す
  return render_template(
    "admin/admin_products.html", 
    products=products
  )

# ================================================
# 商品登録画面表示('/admin_product_add')
# ================================================
@admin_bp.route("/admin_product_add")
def admin_product_add():

  # ページを表示
  return render_template(
    "admin/admin_product_add.html"
  )

# ================================================
# 商品登録処理('/admin_product_insert')
# ================================================
@admin_bp.route("/admin_product_insert", methods=["POST"])
def admin_product_insert():

  name = request.form.get("name")
  price = request.form.get("price")
  series_id = request.form.get("series_id")
  color_id = request.form.get("color_id")
  color_detail = request.form.get("color_detail")
  caption = request.form.get("caption")
  stock = request.form.get("stock")
  img_file = request.files['img_file']
  image_path = ""
  search_key = request.form.get("search_key")
  is_active = request.form.get("is_active")

  # SELECTを作成
  sql = """
  INSERT INTO t_product(
    name,
    price,
    series_id,
    color_id,
    color_detail,
    caption,
    stock,
    image_path,
    search_key,
    is_active
  )
  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
  """

  data = (
    name,
    price,
    series_id,
    color_id,
    color_detail,
    caption,
    stock,
    image_path,
    search_key,
    is_active
  )

  # DB接続からSQL文の発行、commit処理、DB切断
  con = connect_db()  # コネクション
  cur = con.cursor()
  cur.execute(sql, data)

  # 画像の登録
  UPLOAD_FOLDER = 'static/images/products'
  product_id = cur.lastrowid #直前のINSERT操作で生成された主キーの値を返すカーソルのプロパティ
  ext = os.path.splitext(img_file.filename)[1].lower() # 拡張子を取得
  filename = str(product_id) + ext
  path = os.path.join(UPLOAD_FOLDER, filename) # OSによるpathの区切り文字の違いを補完
  img_file.save(path)
  image_path = "images/products/" + filename

  sql = """
  UPDATE t_product
  SET image_path=%s
  WHERE id=%s
  """
  cur.execute(sql,(image_path,product_id))

  con.commit()  # コネクション
  cur.close()
  con.close()  # コネクション

  # 次のページ専用の一時メッセージ
  flash("商品を登録しました")
  # リダイレクト
  response = make_response(redirect("/admin_products"))
  return response

# ================================================
# 商品編集画面表示('/admin_product_edit')
# ================================================
@admin_bp.route("/admin_product_edit/<int:product_id>")
def admin_product_edit(product_id):

  # SQL作成
  sql = """
    SELECT *
    FROM t_product
    WHERE id = %s;
  """
  con = connect_db()  # コネクション
  cur = con.cursor(dictionary=True)
  cur.execute(sql, (product_id,))
  product = cur.fetchone()
  cur.close()
  con.close()  # コネクション  

  product["series_id"] = int(product["series_id"])
  product["color_id"] = int(product["color_id"])
  product["is_active"] = int(product["is_active"])

  # ページを表示
  return render_template(
    "admin/admin_product_edit.html", 
    product=product
  )

# ================================================
# 商品登録処理('/admin_product_update')
# ================================================
@admin_bp.route("/admin_product_update", methods=["POST"])
def admin_product_update():

  product_id = request.form.get("product_id")
  name = request.form.get("name")
  price = request.form.get("price")
  series_id = request.form.get("series_id")
  color_id = request.form.get("color_id")
  color_detail = request.form.get("color_detail")
  caption = request.form.get("caption")
  stock = request.form.get("stock")
  img_file = request.files['img_file']
  search_key = request.form.get("search_key")
  is_active = request.form.get("is_active")

  # SELECTを作成
  sql = """
  UPDATE t_product
  SET
    name=%s,
    price=%s,
    series_id=%s,
    color_id=%s,
    color_detail=%s,
    caption=%s,
    stock=%s,
    search_key=%s,
    is_active=%s
  WHERE id=%s
  """

  data = (
    name,
    price,
    series_id,
    color_id,
    color_detail,
    caption,
    stock,
    search_key,
    is_active,
    product_id
  )

  # DB接続からSQL文の発行、commit処理、DB切断
  con = connect_db()  # コネクション
  cur = con.cursor()
  cur.execute(sql, data)

  # 画像が選択された場合のみ更新
  # and以下でファイルが未選択でもtrueになるのを防いでいる
  if img_file and img_file.filename != "":
    UPLOAD_FOLDER = 'static/images/products'

    # 既存画像削除
    # globはファイル検索するPythonの標準機能
    # glob.glob(検索条件)
    old_files = glob.glob(os.path.join(UPLOAD_FOLDER, str(product_id) + ".*"))
    for file in old_files:
      os.remove(file)

    # 差替え画像登録
    ext = os.path.splitext(img_file.filename)[1].lower() # 拡張子を取得
    filename = str(product_id) + ext
    path = os.path.join(UPLOAD_FOLDER, filename)
    img_file.save(path)
    image_path = "images/products/" + filename

    sql = """
    UPDATE t_product
    SET image_path=%s
    WHERE id=%s
    """
    cur.execute(sql,(image_path,product_id))

  con.commit()  # コネクション
  cur.close()
  con.close()  # コネクション

  # 次のページ専用の一時メッセージ
  flash("商品情報を更新しました")
  # リダイレクト
  response = make_response(redirect("/admin_products"))
  return response

# ==============================
# DB接続
# ==============================
def connect_db():
  return mysql.connector.connect(
    host="localhost", user="root", passwd="", db="db_mini_wallet_lab"
  )
