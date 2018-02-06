library(RPostgreSQL)
library(dplyr)
# データベースアクセス
con <- dbConnect(PostgreSQL(), host="192.168.11.16", 
                 port=5432, 
                 dbname="datacom2017", 
                 user="postgres", 
                 password="postgres")
#データ読み込み
dbGetQuery(con,"SET CLIENT_ENCODING TO 'shift-jis';")
store <- dbGetQuery(con,"SELECT * FROM store_1") %>% as.tbl()
staff <- dbGetQuery(con,"SELECT * FROM staff_1") %>% as.tbl()
line <- dbGetQuery(con,"SELECT * FROM line_henpin_syori_fin") %>% as.tbl()
receipt <- dbGetQuery(con,"SELECT * FROM receipt_henpin_syori_fin") %>% as.tbl()
customer <- dbGetQuery(con,"SELECT * FROM customer_3") %>% as.tbl()
ziocode <- dbGetQuery(con,"SELECT * FROM zip_geocodes") %>% as.tbl()

#データ読み込み productのみ別用
dbGetQuery(con,"SET CLIENT_ENCODING TO 'utf-8';")
product <- dbGetQuery(con,"SELECT * FROM product_2") %>% as.tbl()
product$product_category <- iconv(product$product_category,from = "utf-8",to="cp932")
product$category_1 <- iconv(product$category_1,from = "utf-8",to="cp932")
product$category_2 <- iconv(product$category_2,from = "utf-8",to="cp932")
product$product_name<- iconv(product$product_name,from = "utf-8",to="cp932")

# 期間内で初回来店が2017年02月30日以降の人間は3000名程度いる
# リピーター判定で取り除く必要ある,リピーター判定
customer<- receipt %>%
  filter(customer_id != -1) %>%
  group_by(year=year(dt), month=month(dt), customer_id) %>%
  summarise() %>%
  ungroup() %>%
  group_by(customer_id) %>%
  summarise(count = n()) %>%
  filter(count > 1) %>%
  select(-count) %>%
  mutate(repeater = TRUE) %>%
  right_join(customer, by="customer_id") %>%
  replace_na(list(repeater=FALSE))

# 店舗データに最寄駅を追加
store_names <- c("表参道","銀座","池袋","新宿","目黒","駒沢","二子玉川","みなとみらい","中野","上大岡","横浜","吉祥寺","不明")
store <- store %>% 
  mutate(station = store_names)

# 会計明細に必要な情報を集約
line <- line %>% 
  mutate(product_id = as.character(product_id)) %>% 
  left_join(receipt %>% select(dt,receipt_id, customer_id, regi_staff), 
            by="receipt_id") %>% 
  left_join(customer %>% select(customer_id, repeater, comment),
            by="customer_id") %>% 
  left_join(product %>% select(product_id, product_name),
            by="product_id")

# フリー女性, フリー男性, 顧客情報なしのデータを消去する.
# お気にいり店舗

customer %>%
  filter(is.na(comment) == TRUE) %>% 
  #filter(is.na(visit_interval) == FALSE) %>% 
  left_join(receipt, by="customer_id") %>%
  group_by(customer_id, dt, store_id) %>%
  summarise() %>%
  ungroup() %>%
  select(customer_id, store_id) %>%
  group_by(customer_id) %>%
  nest() %>%
  mutate(mode = map(data, ~modeest::mfv(.$store_id))) %>%
  select(-data) %>%
  unnest() %>% 
  inner_join(customer,by="customer_id") -> customer
