import pandas as pd
import os
import math

def read_data(path):
    data = pd.read_csv(path, encoding='utf-8')
    return data
def CalEntropy(Label_Col):
    '''
    :param Label_Col: 当前数据表格的标签列
    :return: 全体的信息熵
    '''
    d = {}
    num = Label_Col.shape[0]
    for i in Label_Col:
        if i in d.keys():
            d[i] += 1
        else:
            d[i] = 1
    ent = 0.0
    for k in d.keys():
        p_k = d[k] / num
        ent -= p_k * math.log(p_k, 2)
    return ent

def CalInformationGain(data, dfeature):
    '''
    :param data: 全部的数据表格
    :param dfeature: 作为划分依据的特征
    :return: 信息增益
    '''
    num = data.shape[0]
    groups = data.groupby(dfeature)
    ent_new = 0.0
    for name, group in groups:
        v = group.shape[0]
        ent_v = CalEntropy(group.iloc[:, -1])
        ent_new += (v / num) * ent_v
    return CalEntropy(data.iloc[:, -1]) - ent_new

if __name__ == '__main__':
    data = read_data('./data1.csv')
    print(data.iloc[:, -1])
    print(CalEntropy(data.iloc[:, -1]))
    print(CalInformationGain(data, '纹理'))


