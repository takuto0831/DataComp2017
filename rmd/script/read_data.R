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

#データ読み込み productのみ別用
dbGetQuery(con,"SET CLIENT_ENCODING TO 'utf-8';")
product <- dbGetQuery(con,"SELECT * FROM product_2") %>% as.tbl()
product$product_category <- iconv(product$product_category,from = "utf-8",to="cp932")
product$category_1 <- iconv(product$category_1,from = "utf-8",to="cp932")
product$category_2 <- iconv(product$category_2,from = "utf-8",to="cp932")
product$product_name<- iconv(product$product_name,from = "utf-8",to="cp932")