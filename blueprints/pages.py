from flask import Blueprint,render_template

# Blueprint名はabout
pages_bp = Blueprint('pages',__name__)

# ==============================
# about画面表示処理('/about')
# ==============================
@pages_bp.route('/about')
def about():
    #画面を表示
    return render_template('pages/about.html')

# ==============================
# news画面表示処理('/news')
# ==============================
@pages_bp.route('/news')
def news():
    # ダミーニュース
    news_list = [
        {
            "id": 1,
            "title": "新色「Lime Green」「Magenta」追加のお知らせ",
            "date": "2026-01-25",
            "content": "「Someday」シリーズに新色「Lime Green」と「Magenta」が加わりました。鮮やかな色合いで日常の差し色になってほしいという願いを込めました。オンラインストアおよび一部取扱店舗にて順次販売開始予定です。"
        },
        {
            "id": 2,
            "title": "POP-UP STORE開催のお知らせ",
            "date": "2026-02-18",
            "content": "期間限定でPOP-UP STOREを開催いたします。人気の定番シリーズから最新アイテムまで実際に手に取ってご覧いただけます。会場限定のカラーアイテムもご用意しておりますので、ぜひこの機会にお立ち寄りください。"
        },
        {
            "id": 3,
            "title": "新色「Brown」追加のお知らせ",
            "date": "2026-01-25",
            "content": "「Just Day」シリーズに新色「Brown」が加わりました。深みのある落ち着いたカラーで、使い込むほどにレザーの風合いが増していきます。オンラインストアおよび一部取扱店舗にて順次販売開始予定です。"
        },
        {
            "id": 4,
            "title": "年末年始休業のお知らせ",
            "date": "2025-12-20",
            "content": "誠に勝手ながら、下記の期間は年末年始休業とさせていただきます。休業期間中もオンラインストアでのご注文は可能ですが、商品の発送およびお問い合わせ対応は営業開始日より順次対応いたします。"
        },
        {
            "id": 5,
            "title": "オンラインストア リニューアルのお知らせ",
            "date": "2025-11-12",
            "content": "このたびオンラインストアをリニューアルいたしました。商品ページのデザイン改善や検索機能の強化など、より快適にお買い物いただけるようになりました。今後も新商品や限定アイテムを随時追加予定です。"
        }
    ]

    #画面を表示
    return render_template('pages/news.html', news_list=news_list)

# ==============================
# store画面表示処理('/store')
# ==============================
@pages_bp.route('/store')
def store():
    # ダミー店舗
    stores = [
        {
            "name": "STYLE HUB 札幌店",
            "address": "北海道札幌市中央区北1条西 xxxx-xx-xx",
            "tel": "011-123-xxxx",
            "hours": "10:00〜20:00"
        },
        {
            "name": "URBAN SELECT 仙台店",
            "address": "宮城県仙台市青葉区中央 xxxx-xx-xx",
            "tel": "022-234-xxxx",
            "hours": "10:00〜20:00"
        },
        {
            "name": "CITY DESIGN SHOP 新潟店",
            "address": "新潟県新潟市中央区万代 xxxx-xx-xx",
            "tel": "025-345-xxxx",
            "hours": "10:00〜19:30"
        },
        {
            "name": "MODERN LIFESTYLE 金沢店",
            "address": "石川県金沢市香林坊 xxxx-xx-xx",
            "tel": "076-456-xxxx",
            "hours": "11:00〜20:00"
        },
        {
            "name": "URBAN CRAFT 名古屋店",
            "address": "愛知県名古屋市中区栄 xxxx-xx-xx",
            "tel": "052-567-xxxx",
            "hours": "10:00〜21:00"
        },
        {
            "name": "DESIGN MARKET 京都店",
            "address": "京都府京都市下京区四条通 xxxx-xx-xx",
            "tel": "075-678-xxxx",
            "hours": "11:00〜20:00"
        },
        {
            "name": "LIFESTYLE BASE 大阪店",
            "address": "大阪府大阪市北区梅田 xxxx-xx-xx",
            "tel": "06-789-xxxx",
            "hours": "10:00〜21:00"
        },
        {
            "name": "CREATIVE SELECT 神戸店",
            "address": "兵庫県神戸市中央区三宮町 xxxx-xx-xx",
            "tel": "078-890-xxxx",
            "hours": "11:00〜20:00"
        },
        {
            "name": "DESIGN STATION 広島店",
            "address": "広島県広島市中区紙屋町 xxxx-xx-xx",
            "tel": "082-901-xxxx",
            "hours": "10:00〜20:00"
        },
        {
            "name": "URBAN STYLE 福岡店",
            "address": "福岡県福岡市中央区天神 xxxx-xx-xx",
            "tel": "092-012-xxxx",
            "hours": "10:00〜21:00"
        }
    ]

    #画面を表示
    return render_template('pages/store.html', stores=stores)
