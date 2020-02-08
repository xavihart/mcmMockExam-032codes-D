from SAplanning import *
from mcmtools import *
import numpy as np
import heapq
import time
# [path]:
file_path = "./data/order_1"

# 数据列表
# status
driver_number = 200
number_ord = 10
driver_position = np.zeros((driver_number, 2)) # (lon, lat) 需要初始化！
driver_position[:, 0] = 104.071
driver_position[:, 1] = 30.173
driver_time = np.zeros((driver_number, 2))   # (start, end)
driver_used = np.zeros(driver_number)  # 0, 1



# measure list
driver_order_list = []  # (order_number, start_time, end_time, start_position, end_position)

for i in range(driver_number):
    driver_order_list.append([])


Nfree_list = []
PT = 0.0


data = read_file(file_path, "rb", "o")
data = data.iloc[100000:(100000 + number_ord), ]
data.sort_values("begintime", inplace=True)
data = data.iloc[:, [1, 2, 3, 4, 5, 6]]
data = np.array(data)
data_size = data.shape[0]
print("data downloaded!------size:", data.shape)


# DATA type : np.float64
#  Function to be tested!
def generate_data_blocks(data, uniform=False, time_step=100.0, block_number=10):
    ans = []
    s = data[0][1]
    if uniform:
        for i in range(int(data.shape[0] / block_number)):
            tmp = []
            tmp.append(i * block_number)
            tmp.append(i * block_number + block_number)
            ans.append(tmp)
        return ans
    # make assumption that i % 10 == 0

    s_index = 0

    for j in range(data.shape[0]):
        if data[j][0] > data[s_index][0] + time_step:
            tmp = []
            tmp.append(s_index)
            tmp.append(j - 1)
            ans.append(tmp)
            s_index = j

        else:
            continue
    return ans

def init_car_position(hisinfo=False):
    if not hisinfo:
        for i in range(driver_number):
            driver_position[i][0] = np.random.uniform(103.9, 104.2)
            driver_position[i][1] = np.random.uniform(30.55, 30.80)




    return




req_index = generate_data_blocks(data, uniform=False,time_step=300,  block_number=5)
#print("req index", req_index)


actual_begin_time_for_blocks = []
print(req_index)
l_req = len(req_index)

#Pending section:
for i in range(len(req_index)):

    print("[{}/{}]".format(i, l_req))
    istart = req_index[i][0]
    iend = req_index[i][1]

    block_size = iend - istart + 1

    # block 里面的订单都视为同一个起始时间stime
    stime = data[istart][0]
    print("start time", stime)
    # update这一时间点出租车的used状态
    t = time.time()

    for i in range(driver_number):
        if driver_used[i] == 0:
            continue
        else:
            if driver_time[i][1] < stime:
                driver_used[i] = 0
                print(i, "back!")
    #print("time for update cars 1", time.time() - t)

    availiable_index = np.argwhere(np.array(driver_used) == 0)
    availiable_index = availiable_index.squeeze(1)
    availiable_number = len(availiable_index)
    #print(availiable_index.shape)
    #print(block_size)
    # 如果车子数量不够，填补优先结束的车子
    Nfree_list.append(availiable_number)             # needed to be changed

    if availiable_number <= block_size:
        print("not enough")
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
    # print("driver pos", driver_position.shape)

    #t = time.time()
    print("ava index", availiable_index)

    for i in range(block_size):
        for j in range(availiable_number):
            cost[i][j] = dis_earth(driver_position[availiable_index[j]][0], \
                                   driver_position[availiable_index[j]][1], \
                                   data[istart + i][2], data[istart + i][3] )

    #print("time for generate cost mat", time.time() - t)


    ti = time.time()
    #  --- Simulating Annealing ---
    solution = SA(cost)

    PT += time.time() - ti

    #print("time for SA", time() - ti)

    # update status of cars :
    print("solution", solution)
    for i in range(len(solution)):
        order_number = istart + i
        # cid for Car ID

        cid = solution[i]
        driver_used[cid] = 1
        driver_order_list[cid].append((order_number, data[order_number][0], data[order_number][1] \
                                 , data[order_number][2], data[order_number][3], data[order_number][4] \
                                 , data[order_number][5]))

        driver_time[cid][0] = data[order_number][0]
        driver_time[cid][1] = data[order_number][1]

        driver_position[cid][0] = data[order_number][4]
        driver_position[cid][1] = data[order_number][5]

    print(" time:[{}]".format(i, time.time() - t))




# measurement part:
# using order_list to calculate

cw = 0.0
st = 0.0

print("pending done!------")


for j in range(driver_number):
    # order_list[i]
    for i in range(len(driver_order_list[j])):

        if i == 0:
            continue
        cw += driver_order_list[j][i][1] - driver_order_list[j][i - 1][2]
        st += dis_earth(driver_order_list[j][i][3], driver_order_list[j][i][4], \
                        driver_order_list[j][i][5], driver_order_list[j][i][6])
cw /= driver_number
st /= driver_number





avg_nfree = np.array(Nfree_list).mean()

f = open("./result/PendResult_ordernumber{}.txt".format(order_number), "w")
f.write("order_size:[{}], car_number:[{}]".format(data.shape[0], driver_number))
f.write("File_path: {}\n".format(file_path))
f.write("PT: averge pending time {}(s)\n".format(PT / data_size ))
f.write("Nfree: average vacant cars for each orders: {}\n".format(avg_nfree))
f.write("CW:avg car waiting time: {}(s)\n".format(cw))
f.write("SD: avg (total distance) a driver takes to pick up passeangers: {}(km)\n".format(st))
