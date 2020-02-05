from mcmtools import *

data = read_file("./data/order_13", "rb", "o")

print(SDE(data))