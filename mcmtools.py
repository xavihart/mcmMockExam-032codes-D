import os
import time
import numpy as np
import pandas as pd



def read_file(file_path, read_method, og, splitby=",", max_lines=1e9):
    """

    :param file_path:
    :param read_method: advice "rb"
    :param og: "o" for order data, "g" for gps data
    :param splitby: "," [default]
    :param max_lines: to control the max size
    :return: a DataFrame
    """
    f = open(file_path, read_method)
    s = []
    for i, lines in enumerate(f):
        if i > max_lines:
            break
        lines = str(lines)
        l = lines.split(splitby)
        l[-1] = l[-1][:-3]
        for i in range(len(l)):
            if i == 0:
                continue
            if "." not in l[i]:
                l[i] = int(l[i])
            else:
                l[i] = float(l[i])

        s.append(l)
    f.close()
    data = pd.DataFrame(s)

    assert og in ["o", "g"]

    if og == "o":
        assert data.shape[1] == 7
        data.rename(columns={0: "orderid", 1: "begintime", 2: "endtime", 3: "lon_pick", 4: "lat_pick",\
                              5: "lon_drop", 6: "lat_drop"}, inplace=True)

    if og == "g":
        assert data.shape[1] == 5
        data.rename(columns={0: "driverid", 1: "orderid", 2: "time", 3: "lon", 4: "lat", }, inplace=True)

    print("file type:{}, read successfully!".format(og) + "-" * 10)

    return data


def dis_earth(lat1, long1, lat2, long2):
    tmp = np.sin(lat1 / 180 * np.pi) * np.sin(lat2 / 180 * np.pi) + \
          np.cos(lat1 / 180 * np.pi) * np.cos(lat2 / 180 * np.pi) * np.cos((long1 - long2) / 180 * np.pi)
    return 6371 * np.arccos(tmp)



def MC(data):
    # data: DataFrame , orderdata
    # return :  pickup(lon, lat), drop(lon, lat)
    mc_lon_pick = data['lon_pick'].mean()
    mc_lat_pick = data['lat_pick'].mean()
    mc_lon_drop = data['lon_drop'].mean()
    mc_lat_drop = data['lat_drop'].mean()
    return (mc_lon_pick, mc_lat_pick), (mc_lon_drop, mc_lat_drop)


def SDD(data):
    # datatype : DataFrame
    # return (pickSDD, dropSDD)
    size = data.shape[0]
    v = size - 1   # n-1
    var_lon_pick = data['lon_pick'].var()
    var_lat_pick = data['lat_pick'].var()
    var_lon_drop = data['lon_drop'].var()
    var_lat_drop = data['lat_drop'].var()


    tmp = (var_lat_pick + var_lon_pick) * v / size
    SDD_pick = np.sqrt(tmp)

    tmp = (var_lat_drop + var_lon_drop) * v / size
    SDD_drop = np.sqrt(tmp)

    return (SDD_pick, SDD_drop)




def SDE(data):
    len = data.shape[0]
    v = len - 1
    # pickup:

    varx = data['lon_pick'].var() * v
    vary = data['lat_pick'].var() * v
    cor = data['lon_pick'].corr(data['lat_pick']) * v

    theta_pick = np.arctan(((varx - vary) + np.sqrt((varx-vary)**2 + 4 * (cor ** 2))) * 1 / (2 * cor))

    cos = np.cos(theta_pick)

    sin = np.sin(theta_pick)
    k1 = 0.0
    k2 = 0.0
    (lop, lap), (lod, lad) = MC(data)
    for i in range(len):
        k1 += (cos * (data['lon_pick'][i] - lop) - sin * (data['lat_pick'][i] - lap)) ** 2
        k2 += (sin * (data['lon_pick'][i] - lop) - cos * (data['lat_pick'][i] - lap)) ** 2

    #k1 = cos * cos * varx + sin * sin * vary - 2 * sin * cos * cor
    #k2 = sin * sin * varx + cos * cos * vary - 2 * sin * cos * cor
    #print(v, varx, vary, theta_pick, cor)
    e1_pick = np.sqrt((k1) / (v - 1))
    e2_pick = np.sqrt((k2) / (v - 1))

    #dropoff:

    varx = data['lon_drop'].var() * v
    vary = data['lat_drop'].var() * v
    cor = data['lon_drop'].corr(data['lat_drop']) * v

    theta_drop = np.arctan(((varx - vary) + np.sqrt((varx-vary)**2 + 4 * (cor ** 2))) * 1 / (2 * cor))

    cos = np.cos(theta_drop)
    sin = np.sin(theta_drop)
    #k1 = cos * cos * varx + sin * sin * vary - 2 * sin * cos * cor
    #k2 = sin * sin * varx + cos * cos * vary - 2 * sin * cos * cor
    k1 = 0.0
    k2 = 0.0
    for i in range(len):
        k1 += (cos * (data['lon_drop'][i] - lod) - sin * (data['lat_drop'][i] - lad)) ** 2
        k2 += (sin * (data['lon_drop'][i] - lod) - cos * (data['lat_drop'][i] - lad)) ** 2

    e1_drop = np.sqrt((k1) / (v - 1))
    e2_drop = np.sqrt((k2) / (v - 1))

    return (theta_pick, e1_pick, e2_pick), (theta_drop, e1_drop, e2_drop)
