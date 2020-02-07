from mcmtools import *
import os


data = read_file("./data/gps_1", "rb", "g")
g = data.groupby("driverid")

f = open("./data/DriverID1.txt", "w")

for name, group in g:
    str = name[2:] + ".csv"
    f.write(name + ",\n")
    f1 = open("./data/detailed1/"+str, "w")
    f1.close()
    group.to_csv("./data/detailed1/{}".format(str), columns=data.columns)

f.close()
#print(SDE(data))