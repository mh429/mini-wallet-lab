from flask import Blueprint, render_template, request, make_response
import mysql.connector

# Blueprint名はmember_registration
member_registration_bp = Blueprint("member_registration", __name__)


# ================================================
# 会員登録画面出力処理('/member_registration')
# ================================================
@member_registration_bp.route("/member_registration", methods=["GET"])
def member_registration():
    # 会員登録画面出力処理
    return render_template("member_registration/member_registration.html")


# ================================================
# 会員登録成功画面出力処理('/member_registration_success')
# ================================================
@member_registration_bp.route("/member_registration_success", methods=["POST"])
def member_registration_success():
    # フォームからユーザー名を取得
    user_id = request.form.get("mail")
    password = request.form.get("pass")
    name = request.form.get("name")
    birthday = request.form.get("birthday")
    gender = request.form.get("gender")
    tel = request.form.get("tel")
    zip = request.form.get("zip")
    address1 = request.form.get("address1")
    address2 = request.form.get("address2")
    address3 = request.form.get("address3")
    m_flag = request.form.get("m_flag")

    # 未入力チェック
    # if user_id == "" or password == "":
    #     err_msg = "ユーザID　または　パスワードが未入力です"
    #     return render_template('pages/error.html',err_msg = err_msg)

    # SELECTを作成
    sql = "INSERT INTO t_member(id, pass, name, birthday, gender, tel, zip, address1, address2, address3, m_flag) VALUES ('"
    sql = (
        sql
        + str(user_id)
        + "', '"
        + str(password)
        + "', '"
        + str(name)
        + "', '"
        + str(birthday)
        + "', "
        + str(gender)
        + ", '"
        + str(tel)
        + "', '"
        + str(zip)
        + "', '"
        + str(address1)
        + "', '"
        + str(address2)
        + "', '"
        + str(address3)
        + "', "
        + str(m_flag)
        + ");"
    )
    print(sql)

    # DB接続からSQL文の発行、commit処理、DB切断
    con = connect_db()  # コネクション
    cur = con.cursor()
    cur.execute(sql)
    con.commit()  # コネクション
    cur.close()
    con.close()  # コネクション

    # レスポンスオブジェクトを作成し、ユーザ名をテンプレートに渡す(テンプレートで表示可能になる)
    response = make_response(
        render_template(
            "member_registration/member_registration_success.html", user_name=name
        )
    )
    # ユーザ名をCookieに保存
    response.set_cookie("user_name", name, max_age=60 * 60 * 24 * 1)  # 1日間有効
    response.set_cookie("user_id", user_id, max_age=60 * 60 * 24 * 1)
    # レスポンスオブジェクトを返す
    return response


# ==============================
# DB接続
# ==============================
def connect_db():
    return mysql.connector.connect(
        host="localhost", user="root", passwd="", db="db_mini_wallet_lab"
    )
