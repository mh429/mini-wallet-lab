from flask import Blueprint, render_template, request, make_response
import mysql.connector

# Blueprint名はlogin
login_bp = Blueprint("login", __name__)


# ================================================
# ログイン画面出力処理('/login')
# ================================================
@login_bp.route("/login", methods=["GET"])
def login():
    # ログイン画面出力処理
    return render_template("login/login.html")


# ================================================
# ログイン成功画面出力処理('/login_success')
# ================================================
@login_bp.route("/login_success", methods=["POST"])
def login_success():
    # フォームからユーザー名を取得
    user_id = request.form.get("user_id")
    password = request.form.get("password")

    # 未入力チェック
    if user_id == "" or password == "":
        err_msg = "ユーザID　または　パスワードが未入力です"
        return render_template("pages/error.html", err_msg=err_msg)

    # SELECTを作成
    sql = "SELECT id,pass,name FROM t_member"
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
    elif user_info["pass"] != password:
        err_msg = "パスワードが違います"
        return render_template("pages/error.html", err_msg=err_msg)
    else:
        # レスポンスオブジェクトを作成し、ユーザ名をテンプレートに渡す
        response = make_response(
            render_template("login/login_success.html", user_name=user_info["name"])
        )
        # ユーザIDをCookieに保存
        response.set_cookie(
            "user_name", user_info["name"], max_age=60 * 60 * 24 * 1
        )  # 1日間有効
        response.set_cookie("user_id", user_info["id"], max_age=60 * 60 * 24 * 1)
        # レスポンスオブジェクトを返す
        return response


# ================================================
# ログアウト処理('/logout)
# ================================================
@login_bp.route("/logout", methods=["POST"])
def logout():
    # ログアウト処理
    response = make_response(render_template("login/logout.html"))

    # Cookieからユーザ名を削除
    response.delete_cookie("user_id")
    response.delete_cookie("user_name")

    # レスポンスを返す
    return response


# ==============================
# DB接続
# ==============================
def connect_db():
    return mysql.connector.connect(
        host="localhost", user="root", passwd="", db="db_mini_wallet_lab"
    )
