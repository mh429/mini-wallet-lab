-- テーブル作成とデータ注入

-- ① シリーズテーブル t_series
CREATE TABLE t_series (
  id INT AUTO_INCREMENT PRIMARY KEY,
  series VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO t_series (series) VALUES
('Just Day'),
('Someday');

-- ② 色テーブル t_color
CREATE TABLE t_color (
  id INT AUTO_INCREMENT PRIMARY KEY,
  color VARCHAR(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO t_color (color) VALUES
('Yellow'),
('Pink'),
('Blue'),
('Purple'),
('Green'),
('Black'),
('Brown');

-- ③ 商品テーブル t_product
CREATE TABLE t_product (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  price INT NOT NULL,
  series_id INT NOT NULL,
  color_id INT NOT NULL,
  color_detail VARCHAR(100) NOT NULL,
  caption VARCHAR(500),
  stock INT NOT NULL,
  image_path VARCHAR(255),
  search_key VARCHAR(255),
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  FOREIGN KEY (series_id) REFERENCES t_series(id),
  FOREIGN KEY (color_id) REFERENCES t_color(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO t_product
(name, price, series_id, color_id, color_detail, caption, stock, image_path, search_key, is_active)
VALUES
('Just Day / Black', 18500, 1, 6, 'Black', '丁寧な暮らしにそっと寄り添いたいという想いを込めて、手に馴染み長く使って頂けるデザインを目指しました。当店のこだわりの詰まった一品です。', 10, '/images/products/1.jpg', '三つ折り,justday,黒,ブラック,モノトーン', 1),
('Just Day / Yellow', 18500, 1, 1, 'Yellow', '丁寧な暮らしにそっと寄り添いたいという想いを込めて、手に馴染み長く使って頂けるデザインを目指しました。当店のこだわりの詰まった一品です。', 10, '/images/products/2.jpg', '三つ折り,justday,黃,黄色,イエロー', 1),
('Just Day / Brown', 18500, 1, 7, 'Brown', '丁寧な暮らしにそっと寄り添いたいという想いを込めて、手に馴染み長く使って頂けるデザインを目指しました。当店のこだわりの詰まった一品です。', 10, '/images/products/3.jpg', '三つ折り,justday,茶,茶色', 1),
('Someday / Lime Green', 16900, 2, 5, 'Lime Green', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/4.jpg', '二つ折り,ボタン,緑,グリーン,ライム,黄緑,ライムグリーン', 1),
('Someday / Magenta', 16900, 2, 2, 'Magenta', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/5.jpg', '二つ折り,ボタン,マゼンタ,ピンク', 1),
('Someday / Cafe Brown', 16900, 2, 7,'Cafe Brown', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/6.jpg', '二つ折り,ボタン,ブラウン,茶,茶色', 1),
('Someday / Purple', 16900, 2, 4, 'Purple', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/7.jpg', '二つ折り,ボタン,パープル,紫', 1),
('Someday / Wine', 16900, 2, 4, 'Wine', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/8.jpg', '二つ折り,ボタン,赤,レッド,ワイン,ワインレッド,紫,パープル,赤紫', 1),
('Someday / Pastel Blue', 16900, 2, 3, 'Pastel Blue', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/9.jpg', '二つ折り,ボタン,ブルー,水色,パステルカラー,青', 1),
('Someday / Pink', 16900, 2, 2, 'Pink', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/10.jpg', '二つ折り,ボタン,ピンク', 1),
('Someday / Beige', 16900, 2, 1, 'Beige', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/11.jpg', '二つ折り,ボタン,ベージュ,ブラウン,茶色,アイボリー', 1),
('Someday / Cyan', 16900, 2, 3, 'Cyan', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/12.jpg', '二つ折り,ボタン,ブルー,水色,青,シアン', 1),
('Someday / Gray', 16900, 2, 6, 'Gray', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/13.jpg', '二つ折り,ボタン,グレー,灰色,モノトーン', 1),
('Someday / Green', 16900, 2, 5, 'Green', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/14.jpg', '二つ折り,ボタン,グリーン,緑', 1),
('Someday / Pastel Pink', 16900, 2, 2, 'Pastel Pink', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/15.jpg', '二つ折り,ボタン,ピンク,パステルカラー', 1),
('Someday / Brown', 16900, 2, 7, 'Brown', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/16.jpg', '二つ折り,ボタン,茶色,赤茶,ブラウン', 1),
('Someday / Red', 16900, 2, 2, 'Red', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/17.jpg', '二つ折り,ボタン,赤,レッド', 1),
('Someday / Matt Black', 16900, 2, 6, 'Matt Black', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/18.jpg', '二つ折り,ボタン,黒,ブラック,モノトーン', 1),
('Someday / Sky Blue', 16900, 2, 3, 'Sky Blue', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/19.jpg', '二つ折り,ボタン,シアン,水色,青,ブルー', 1),
('Someday / Salmon Pink', 16900, 2, 2, 'Salmon Pink', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/20.jpg', '二つ折り,ボタン,サーモン,ピンク', 1),
('Someday / Camel', 16900, 2, 7, 'Camel', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/21.jpg', '二つ折り,ボタン,ベージュ,茶色,ブラウン', 1),
('Someday / Blue', 16900, 2, 3, 'Blue', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/22.jpg', '二つ折り,ボタン,青,ブルー,ネイビー,紺色', 1),
('Someday / Black', 16900, 2, 6, 'Black', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/23.jpg', '二つ折り,ボタン,ブラック,黒,モノトーン', 1);

-- INSERT INTO t_product
-- (name, price, series_id, color_id, color_detail, caption, stock, image_path, search_key, is_active)
-- VALUES
-- ('Just Day / Black', 18500, 1, 6, 'Black', '丁寧な暮らしにそっと寄り添いたいという想いを込めて、手に馴染み長く使って頂けるデザインを目指しました。当店のこだわりの詰まった一品です。', 10, '/images/products/justday_black.jpg', '三つ折り,justday,黒,ブラック,モノトーン', 1),
-- ('Just Day / Yellow', 18500, 1, 1, 'Yellow', '丁寧な暮らしにそっと寄り添いたいという想いを込めて、手に馴染み長く使って頂けるデザインを目指しました。当店のこだわりの詰まった一品です。', 10, '/images/products/justday_yellow.jpg', '三つ折り,justday,黃,黄色,イエロー', 1),
-- ('Just Day / Brown', 18500, 1, 7, 'Brown', '丁寧な暮らしにそっと寄り添いたいという想いを込めて、手に馴染み長く使って頂けるデザインを目指しました。当店のこだわりの詰まった一品です。', 10, '/images/products/justday_brown.jpg', '三つ折り,justday,茶,茶色', 1),
-- ('Someday / Lime Green', 16900, 2, 5, 'Lime Green', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/someday_limegreen.jpg', '二つ折り,ボタン,緑,グリーン,ライム,黄緑,ライムグリーン', 1),
-- ('Someday / Magenta', 16900, 2, 2, 'Magenta', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/someday_magenta.jpg', '二つ折り,ボタン,マゼンタ,ピンク', 1),
-- ('Someday / Cafe Brown', 16900, 2, 7,'Cafe Brown', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/someday_cafebrown.jpg', '二つ折り,ボタン,ブラウン,茶,茶色', 1),
-- ('Someday / Purple', 16900, 2, 4, 'Purple', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/someday_purple.jpg', '二つ折り,ボタン,パープル,紫', 1),
-- ('Someday / Wine', 16900, 2, 4, 'Wine', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/someday_wine.jpg', '二つ折り,ボタン,赤,レッド,ワイン,ワインレッド,紫,パープル,赤紫', 1),
-- ('Someday / Pastel Blue', 16900, 2, 3, 'Pastel Blue', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/someday_pastelblue.jpg', '二つ折り,ボタン,ブルー,水色,パステルカラー,青', 1),
-- ('Someday / Pink', 16900, 2, 2, 'Pink', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/someday_pink.jpg', '二つ折り,ボタン,ピンク', 1),
-- ('Someday / Beige', 16900, 2, 1, 'Beige', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/someday_beige.jpg', '二つ折り,ボタン,ベージュ,ブラウン,茶色,アイボリー', 1),
-- ('Someday / Cyan', 16900, 2, 3, 'Cyan', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/someday_cyan.jpg', '二つ折り,ボタン,ブルー,水色,青,シアン', 1),
-- ('Someday / Gray', 16900, 2, 6, 'Gray', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/someday_gray.jpg', '二つ折り,ボタン,グレー,灰色,モノトーン', 1),
-- ('Someday / Green', 16900, 2, 5, 'Green', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/someday_green.jpg', '二つ折り,ボタン,グリーン,緑', 1),
-- ('Someday / Pastel Pink', 16900, 2, 2, 'Pastel Pink', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/someday_pastelpink.jpg', '二つ折り,ボタン,ピンク,パステルカラー', 1),
-- ('Someday / Brown', 16900, 2, 7, 'Brown', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/someday_brown.jpg', '二つ折り,ボタン,茶色,赤茶,ブラウン', 1),
-- ('Someday / Red', 16900, 2, 2, 'Red', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/someday_red.jpg', '二つ折り,ボタン,赤,レッド', 1),
-- ('Someday / Matt Black', 16900, 2, 6, 'Matt Black', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/someday_mattblack.jpg', '二つ折り,ボタン,黒,ブラック,モノトーン', 1),
-- ('Someday / Sky Blue', 16900, 2, 3, 'Sky Blue', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/someday_skyblue.jpg', '二つ折り,ボタン,シアン,水色,青,ブルー', 1),
-- ('Someday / Salmon Pink', 16900, 2, 2, 'Salmon Pink', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/someday_salmonpink.jpg', '二つ折り,ボタン,サーモン,ピンク', 1),
-- ('Someday / Camel', 16900, 2, 7, 'Camel', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/someday_camel.jpg', '二つ折り,ボタン,ベージュ,茶色,ブラウン', 1),
-- ('Someday / Blue', 16900, 2, 3, 'Blue', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/someday_blue.jpg', '二つ折り,ボタン,青,ブルー,ネイビー,紺色', 1),
-- ('Someday / Black', 16900, 2, 6, 'Black', '機能は賢く最小限でも、暮らしに色を添える存在でありたい。そんな願いから生まれました。', 5, '/images/products/someday_black.jpg', '二つ折り,ボタン,ブラック,黒,モノトーン', 1);

-- ④ 会員テーブル t_member
CREATE TABLE t_member (
  id VARCHAR(255) PRIMARY KEY,
  pass VARCHAR(100) NOT NULL,
  name VARCHAR(50) NOT NULL,
  birthday DATE NOT NULL,
  gender TINYINT NOT NULL,
  tel VARCHAR(20) NOT NULL,
  zip VARCHAR(10) NOT NULL,
  address1 VARCHAR(100) NOT NULL,
  address2 VARCHAR(100),
  address3 VARCHAR(100),
  m_flag TINYINT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO t_member
(id, pass, name, birthday, gender, tel, zip, address1, address2, address3, m_flag)
VALUES
('demo@demo.com', 'portfolio2026', '田中 太郎', '1990-01-01', 1, '0000-11-1111', '530-0001', '大阪府大阪市北区', '梅田3丁目3-1', '大阪ハイツ101', 1);

-- ⑤ 注文テーブル t_order
CREATE TABLE t_order (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_date DATE NOT NULL,
  member_id VARCHAR(50) ,
  orderer VARCHAR(50) NOT NULL,
  mail VARCHAR(255) NOT NULL,
  tel VARCHAR(20) NOT NULL,
  zip VARCHAR(10) NOT NULL,
  address1 VARCHAR(100) NOT NULL,
  address2 VARCHAR(100) NOT NULL,
  address3 VARCHAR(100),
  recipient VARCHAR(50) NOT NULL,
  payment TINYINT NOT NULL,
  processing TINYINT NOT NULL,
  FOREIGN KEY (member_id) REFERENCES t_member(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO t_order
(order_date, member_id, orderer, mail, tel, zip, address1, address2, address3, recipient, payment, processing)
VALUES
('2026-01-01', 'demo@demo.com', '田中 太郎', 'demo@demo.com', '0000-11-1111', '530-0001', '大阪府大阪市北区梅田', '3丁目3-1', '大阪ハイツ101', '田中 太郎', 1, 3),
('2026-01-02', NULL, '山田 花子', 'demo2@demo.com', '000-2222-2222', '160-0023', '東京都新宿区西新宿', '1丁目7-3', NULL, '山田 花子', 2, 3),
('2026-02-02', 'demo@demo.com', '田中 太郎', 'demo@demo.com', '0000-11-1111', '530-0001', '大阪府大阪市北区梅田', '3丁目3-1', '大阪ハイツ101', '田中 太郎', 1, 2),
('2026-03-03', NULL, '鈴木 一郎', 'demo3@demo.com', '000-3333-3333', '450-0002', '愛知県名古屋市中村区名駅', '4丁目27-1', NULL, '鈴木 一郎', 3, 1);

-- ⑥ 注文明細テーブル t_order_detail
CREATE TABLE t_order_detail (
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL,
  PRIMARY KEY (order_id, product_id),
  FOREIGN KEY (order_id) REFERENCES t_order(id),
  FOREIGN KEY (product_id) REFERENCES t_product(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO t_order_detail (order_id, product_id, quantity) VALUES
(1, 3, 1),
(2, 2, 1),
(3, 23, 1),
(4, 8, 2),
(4, 1, 2),
(4, 14, 3);

-- ⑦ 管理者テーブル t_admin
CREATE TABLE t_admin (
  id VARCHAR(255) PRIMARY KEY,
  pass VARCHAR(100) NOT NULL,
  name VARCHAR(50) NOT NULL,
  authority TINYINT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO t_admin (id, pass, name, authority) VALUES
('staff@demo.com','portfolio2026', '財田 布太郎', 1);

