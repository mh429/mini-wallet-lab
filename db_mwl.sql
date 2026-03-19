-- [コマンドプロンプトに以下を入力し、MySQLの存在する場所に移動する]
cd \
cd \xampp\mysql\bin

-- [MySQLを起動する方法]
mysql -u root -p


-- [データベースの一覧を確認する]
SHOW DATABASES;


-- [データベースを作成する]
-- [データベースの文字コードを設定]mb4は絵文字使わなかったらなくてもOK
CREATE DATABASE db_mini_wallet_lab
DEFAULT CHARACTER SET utf8mb4;

-- [データベースを指定する]
USE db_mini_wallet_lab;

-- 何かあったときにDB削除
-- 使用中なら、先にDB切り替えてから削除
USE mysql;
drop database db_mini_wallet_lab;
-- テーブル削除
DROP TABLE テーブル名;


-- [テーブルの一覧を確認する]
SHOW TABLES;





--------------------------ユーザ側-----------------------------------

-- 現在公開中の商品情報を取得
SELECT p.id, p.price, s.series, c.color, p.caption, p.stock, p.image_path
FROM t_product p
INNER JOIN t_series s
ON p.series_id = s.id
INNER JOIN t_color c
ON p.color_id = c.id
WHERE p.is_active = 1;

SELECT *
FROM t_product
WHERE is_active = 1;


-- メールアドレスとPWに一致する会員情報を取得
SELECT *
FROM t_member
WHERE mail = "";


--IDに一致する商品情報
SELECT *
FROM products
WHERE id IN (1,2);

-- 在庫数を変更
-- →足りなかったらエラー
UPDATE t_product
SET stock = stock - i
WHERE id =  ;

-- 注文情報を注文Tに追加
INSERT INTO t_order
(order_date, orderer, mail, tel, zip, address1, address2, address3, recipient, member_id, processing)
VALUES
('', '', '', '', '', '', '', '', '', , 1);

('2026-02-09', '畑中 萌', 'ccc@mail.com', '0000-44-5555', '444-4444', '大阪府大阪市中央区', '1-4-5', 'ハイツ101', '畑中 萌', NULL, 1);

-- 注文情報を注文明細Tに追加
INSERT INTO t_order_detail (order_id, product_id, quantity)
VALUES
(, , ),
(, , );

(5, 2, 3),
(5, 4, 1);

-- 会員情報を会員Tに追加
INSERT INTO t_member
(mail, pass, name, birthday, gender, tel, zip, address1, address2, address3, m_flag)
VALUES
('', '', '', '', , '', '', '', '', '', );

('ccc@mail.com', 'pass5555', '畑中 萌', '1990-01-01', 2, '0000-44-5555', '444-4444', '大阪府大阪市中央区', '1-4-5', 'ハイツ101', 1);



---------------------------管理者側----------------------------------

-- 管理者IDとPWに一致する管理者情報を取得
SELECT *
FROM t_admin
WHERE id = ;

-- 管理者情報を管理者Tに追加
INSERT INTO t_admin (pass, name, authority) VALUES
('', '', );

('admin333', '畑中', 3);

-- 注文情報を取得
SELECT *
FROM t_order;

SELECT *
FROM t_order_detail;

-- 処理状況を更新
UPDATE t_order
SET processing = 
WHERE id =  ;

-- 商品情報を登録
INSERT INTO t_product
(name, price, series_id, color_id, caption, stock, image_path, is_active)
VALUES
('', , , , '', , '', );

('Someday Bloom', 18900, 2, 1, 'テスト用', 10, '', 0);

-- 商品情報を編集