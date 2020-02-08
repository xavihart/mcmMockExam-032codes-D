from mcmtools import *
import numpy as np



def random_change(x, max_):
    #1
    while True:
        t = np.random.randint(max_)
        if t not in x:
            break
    ex = np.random.randint(len(x))
    x[ex] = t
    #2
    i, j = np.random.randint(len(x)), np.random.randint(len(x))
    x[i], x[j] = x[j], x[i]
    return x



def cal_cost(Cost, x, status="r"):
    tot = 0.0
    assert status in ["r", "c"]
    if status == "r":
        for i in range(len(x)):
            tot += Cost[i][x[i]]
        return tot
    else:
        for i in range(len(x)):
            tot += Cost[x[i]][i]
        return tot



def SA(cost, init_T = 1000, end_T = 10, iter = 300):
    """
     use simulate annealing algorithm
    :param Cost: the cost matrix , its a numpy array
    :return: the best matching matrix in numpy [0, 1] (request * car number)
    """
    r_num = cost.shape[0]
    r_car = cost.shape[1]
    miner = min(r_car, r_num)
    maxer = max(r_car, r_num)
    x = np.random.permutation(range(maxer))[:miner]
    T = init_T

    q = 1 - 5 / iter

    if miner == r_num:
        state = "r"
    else:
        state= "c"

    cost_now = cal_cost(cost, x, state)
    time= 0
    while T > end_T:
        for i in range(iter):
            x_new = random_change(x, maxer)
            cost_new = cal_cost(cost, x_new, state)
            dt = cost_new - cost_now
            if dt < 0:
                cost_now = cost_new
                x = x_new
            else:
                e = np.exp(-dt / T)
                ran = np.random.uniform(0, 1)
                if ran < e:
                    x = x_new
                    cost_now = cost_new

        time += 1
        T *= q
        #print("time", time, "x:", x, "cost:", cost_now)
    return x







