from SAplanning import *
from mcmtools import *
import numpy as np
import heapq
import time
# [path]:
file_path = "./data/order_1"

# 数据列表
# status
driver_number = 30000
driver_position = np.zeros((driver_time), 2)  # (lon, lat) 需要初始化！
driver_time = np.zeros((driver_number, 2))   # (start, end)
driver_used = np.zeros(driver_number)  # 0, 1

# measure list
driver_order_list = []  # (order_number, start_time, end_time, start_position, end_position)

for i in range(driver_number):
    driver_order_list.append([])


Nfree_list = []
PT = 0.0


data = read_file(file_path, "rb", "o")
data.sort_values("begintime", inplace=True)
data = data.iloc[:, [1, 2, 3, 4, 5, 6]]
data = np.array(data)
data_size = data.shape[0]
print("data downloaded!------size:", data.shape)


# DATA type : np.float64
#  Function to be tested!
def generate_data_blocks(data, uniform=False, time_step=30.0, block_number=10):
    ans = []
    s = data[0][1]
    if uniform:
        for i in range(int(data.shape[0] / block_number)):
            tmp = []
            tmp.append(i * 10)
            tmp.append(i * 10 + 9)
            ans.append(tmp)
    # make assumption that i % 10 != 0

    s_index = 0

    for j in range(data.shape[0]):
        if data[0][j] > data[s_index][j] + time_step:
            tmp = []
            tmp.append(s_index)
            tmp.append(j - 1)
            ans.append(tmp)
            s_index = j

        else:
            continue
    return ans

def init_car_position():
    # to do
    return


req_index = generate_data_blocks(data)
actual_begin_time_for_blocks = []


#Pending section:
for i in range(len(req_index)):

    istart = req_index[i][0]
    iend = req_index[i][1]
    block_size = iend - istart + 1

    # block 里面的订单都视为同一个起始时间stime
    stime = data[0][istart]

    # update这一时间点出租车的used状态
    for i in range(driver_number):
        if used[i] == 0:
            continue
        else:
            if driver_time[i][1] < stime:
                used[i] = 0

    availiable_index = np.argwhere(np.array(driver_used) != 0)
    availiable_number = len(availiable_index)

    # 如果车子数量不够，填补优先结束的车子
    Nfree_list.append(availiable_number)

    if availiable_number <= block_size:

        iloc = driver_time[:, 1]
        iloc = stime - iloc
        iloc[np.argwhere(iloc >= 0)] = -1e6

        index = heapq.nlargest(block_size, range(len(iloc)), iloc.take)

        # update PT and stime:
        newtime = driver_time[index[0]][1]
        PT += (newtime - stime)
        stime = newtime

        # update ava list:
        availiable_index += index


    # generate cost matrix
    cost = np.zeros((block_size, availiable_number))
    for i in range(block_size):
        for j in range(availiable_number):
            cost[i][j] = dis_earth(driver_position[availiable_index[j]][0], \
                                   driver_position[availiable_index[j]][1], \
                                   data[istart + i][2], data[istart + i][3] )

    ti = time.time()
    #  --- Simulating Annealing ---
    solution = SA(cost)

    PT += ti -time.time()

    # update status of cars :
    for i in range(len(solution)):
        order_number = istart + i
        # cid for Car ID

        cid = solution[i]
        driver_used[cid] = 1
        driver_order_list[cid].append((order_number, data[order_number][1], data[order_number][2] \
                                 , data[order_number][3], data[order_number][4], data[order_number][5] \
                                 , data[order_number][6]))

        driver_time[cid][0] = data[order_number][1]
        driver_time[cid][1] = data[order_number][2]

        driver_position[cid][0] = data[order_number][4]
        driver_position[cid][1] = data[order_number][5]






# measurement part:
# using order_list to calculate

cw = 0.0
st = 0.0

for i in range(driver_number):
    # order_list[i]
    if i == 0:
        continue
    cw += driver_order_list[i][0] - driver_order_list[i - 1][1]
    st += dis_earth(driver_order_list[i][3], driver_order_list[i][4], \
                    driver_order_list[i - 1][5], driver_order_list[i - 1][6])
cw /= driver_number
st /= driver_number





avg_nfree = np.array(Nfree_list).mean()

f = open("./result/PendResult.txt", "w")
f.write("File_path:{}\n".format(file_path))
f.write("PT: averge pending time{}(s)\n".format(PT / data_size ))
f.write("Nfree: average vacant cars for each orders: {}\n".format(avg_nfree))
f.write("CW:avg car waiting time: {}(s)\n".format(cw))
f.write("SD: avg (total distance) a driver takes to pick up passeangers: {}(km)\n".format(st))
