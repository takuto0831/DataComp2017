# 新しいデータ作成
customer_com <- customer

# ランダムフォレストによる情報補完
library(missForest)
library(imputeMissings)
library(doParallel)

# "不明"をnaに置き換え
replace(customer_com$sex, which(customer_com$sex=="不明"),NA) %>% 
  as.factor() -> customer_com$sex
# 誕生年代をfactorに変更
customer_com$birth_age %>% 
  as.factor() -> customer_com$birth_age

#並列処理
cl <- makeCluster(5)
registerDoParallel(cl)
  
customer_com %>% 
  select(sex,birth_age,remake_count,total_item_money,visit_interval,
         morning_count_weekday:night_count_holiday) %>% 
  as.data.frame() %>% 
  missForest(
    variablewise = TRUE,
    ntree = 1200,
    #parallelize = "variables",
    parallelize = "forests",
    verbose = TRUE) -> ans

stopCluster(cl)

# 予測した値を補完する
ans$ximp$sex %>%
  as.character() -> customer_com$sex
ans$ximp$birth_age %>%  
  as.character() %>% 
  as.integer() -> customer_com$birth_age
# 来店間隔に使っていいの??
# ans$ximp$visit_interval -> customer_com$visit_interval