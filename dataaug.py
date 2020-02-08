from mcmtools import *
import time

t = time.time()


data_g = read_file("./data/gps_13", "rb", "g", max_lines=1000)
data_o = read_file("./data/order_13", "rb", "o", max_lines=1000)

data_o.loc[data_o.orderid == " ", 'driverid'] = "kkk"
data_o['driverid'].astype("object")


data_g.drop_duplicates(subset=["orderid"])
data_g.sort_values(by=['orderid'])
data_o.sort_values(by=['orderid'])


print("sorted successfully, time:", time.time() - t)


i = 0
j = 0
len1 = data_o.shape[0]
len2 = data_g.shape[0]


while i < len1 and j < len2:
    ord = data_o.iloc[i, 0][2:]
    ord_ = data_g.iloc[i, 1]
    if ord == ord_:
        data_o.iloc[i, 7] = data_g.iloc[j, 0]
        i, j = i + 1, j + 1
    if ord > ord_:
        j += 1
    if ord < ord_:
        i += 1

data_o.to_csv("./g_13_aug.csv")