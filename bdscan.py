import numpy as np
import sklearn.cluster as skc
from sklearn import metrics
import matplotlib.pyplot as plt  
from mcmtools import *

data = read_file("./data/order_1", "rb", "o", list=True)
X = []


for i in range(len(data)):
    a = []
    a.append(data[i][3])
    a.append(data[i][4])
    X.append(a)


X = np.array(X)

X = X[:1000]

print(X[0])

db = skc.DBSCAN(eps=0.005, min_samples=3).fit(X) #DBSCAN聚类方法 还有参数，matric = ""距离计算方法
labels = db.labels_  #和X同一个维度，labels对应索引序号的值 为她所在簇的序号。若簇编号为-1，表示为噪声

print('每个样本的簇标号:')
print(labels)

raito = len(labels[labels[:] == -1]) / len(labels)  #计算噪声点个数占总数的比例
print('噪声比:', format(raito, '.2%'))

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)  # 获取分簇的数目

print('分簇的数目: %d' % n_clusters_)

for i in range(n_clusters_):
    print('簇 ', i, '的所有样本:')
    one_cluster = X[labels == i]
    print(one_cluster)
    plt.plot(one_cluster[:,0],one_cluster[:,1],'o')

plt.savefig("./pic/dbscan.png")
