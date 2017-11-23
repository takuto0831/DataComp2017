
#2点間の距離を求める公式
distance_func <- function(lat, long, main_lat, main_long){
  # 軽度の序離を求める
  dis_x = 6378150 * cos(main_lat/180 * pi) * 2 * pi * (long-main_long) / 360 
  # 緯度の距離を求める
  dis_y = 40054782 * (lat-main_lat) / 360
  return(sqrt(dis_x^2 + dis_y^2))
}

distance_func_2 <- function(lat, long, main_lat, main_long){
  r = 6378.137
  dx = long - main_long
  d = acos(sin(main_lat*pi/180) * sin(lat*pi/180) + 
             cos(main_lat*pi/180) * cos(lat*pi/180) * cos(dx*pi/180))
  return(d*r)
}

# 角度を求める関数
# なんか違う
theta_func <- function(lat, long, main_lat, main_long){
  dx = long-main_long
  phi = 90 - atan2(sin(dx),cos(main_lat)*tan(lat) - sin(main_lat)*cos(dx))
  return(d)
}



main_lat =35.67403
main_long = 139.7657
lat = 33.5120
long= 130.4512
