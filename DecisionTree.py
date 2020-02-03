import pandas as pd
import os
import math

'''
   ID3:  使用信息熵的差 (IG)
   CART: 使用基尼指数（Gini Index）
   C4.5:  使用信息增益率 (IG Ratio)
'''


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


def CalInformationGain(data, dfeature, ent_method='entropy'):
    '''
    :param data: 全部的数据表格
    :param dfeature: 作为划分依据的特征
    :return: 信息增益
    '''

    num = data.shape[0]
    groups = data.groupby(dfeature)
    ent_new = 0.0

    assert ent_method in ['entropy', 'gini']

    if ent_method == 'entropy':
        for name, group in groups:
            v = group.shape[0]
            ent_v = CalEntropy(group.iloc[:, -1])
            ent_new += (v / num) * ent_v
        return CalEntropy(data.iloc[:, -1]) - ent_new

    if ent_method == 'gini':
        for name, group in groups:
            v = group.shape[0]
            ent_v = CalIGini(group.iloc[:, -1])
            ent_new += (v / num) * ent_v
        return CalEntropy(data.iloc[:, -1]) - ent_new


def CalIGRate(data, dfeature, ent_method='entropy'):
    '''
    :param data: same as CalInformationGain
    :param dfeature:  same as CalInformationGain
    :return: 信息增益率
    '''
    IG = CalInformationGain(data, dfeature, ent_method)
    iv = 0.0
    num = data.shape[0]
    g = data.groupby(dfeature)
    for name, group in g:
        v = group.shape[0]
        iv -= math.log(v / num, 2) * (v / num)

    return IG / iv


def CalIGini(data):
    '''
    :param data: same as CalEnt
    :param dfeature:  same as CalEnt
    :return: CART决策树中的Gini指数  sum()
    '''
    # to do


def get_best_dividing_feature(data, method='entropy', using_ratio=False):
    """
    :param data: 划分使用到的数据
    :param method: 划分评价指数
    :param using_ratio: 是否使用增益率
    :return: 最优的划分特征
    """
    best_feature = " "
    max_ent = - 100000
    for feature in data.columns.values[:-1]:   # [:-1]把label信息排除在外
        ent_ = 0
        if using_ratio == True:
            ent_ = CalIGRate(data, feature, method)
        else:
            ent_ = CalInformationGain(data, feature, method)
            print(ent_)
        if ent_ > max_ent:
            max_ent = ent_
            best_feature = feature

    return best_feature, max_ent


def CreateDecicisonTree(data, TreeType='ID3'):
    # return a tree in in a dir type
    assert TreeType in ['C4.5', 'ID3', 'CART']
    root = {}
    if data.shape[0] == 0:
        return

    dfeature = " "

    if TreeType == 'ID3':
        dfeature = get_best_dividing_feature(data, method='entropy', using_ratio=False)

    if TreeType == 'C4.5':
        dfeature = get_best_dividing_feature(data, method='entropy', using_ratio=True)

    if TreeType == 'CART':
        dfeature = get_best_dividing_feature(data, method='gini')

    # 找出数量最多的label(salient feature)备用
    label = data[data.columns.values[-1]]
    label = list(label)
    salient_feature = max(label, key=label.count)

    for df in list(set(label)):      #list(set(*)) is used to remove same units
        







def MakeDecision(data, root):
    """
    :param data: DataFrame
    :return: a list of decision
    """
    # {'f1':{'f11':{'f21':{a}}, 'f12'"{b}, 'f13':{c}}}
    num = data.shape[0]
    ans_list = []

    for i in range(num):
        while type(root) == 'dict':
            KEY = list(root.keys())[0]
            root = root[data[KEY][i]]
        ans_list.append(root)

    return ans_list


if __name__ == '__main__':
    # test data:
    data = read_data('./data1.csv')
    data = data.iloc[:, [1, 2, 3, 4, 5, 6, 9]]
    print("column size:", data.iloc[:, -1].shape[0])
    ent = CalEntropy(data.iloc[:, -1])
    print("Entropy of data:", ent)

    for name in data.columns.values:
        eg = CalInformationGain(data, name)
        print("EGain divided by {}:".format(name), eg)
        egr = CalIGRate(data, name)
        print("EGainRatio divided by {}:".format(name), egr)
        print("-" * 50)

    print(get_best_dividing_feature(data))



