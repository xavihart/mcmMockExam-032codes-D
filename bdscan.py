import numpy as np
import sklearn.cluster as skc
from sklearn import metrics
import matplotlib.pyplot as plt  
from mcmtools import *

plt.rcParams['savefig.dpi'] = 500
plt.rcParams['figure.dpi'] = 500
plt.style.use('seaborn-dark')

day = 1



data = read_file("./data/order_{}".format(str(day)), "rb", "o", list=True)
X = []


for i in range(len(data)):
    a = []
    a.append(data[i][3])
    a.append(data[i][4])
    X.append(a)


X = np.array(X)

X = X[0:200000:10]

print(X[0])

db = skc.DBSCAN(eps=0.003, min_samples=20).fit(X) #DBSCAN聚类方法 还有参数，matric = ""距离计算方法
labels = db.labels_  #和X同一个维度，labels对应索引序号的值 为她所在簇的序号。若簇编号为-1，表示为噪声

print('每个样本的簇标号:')
print(labels)

raito = len(labels[labels[:] == -1]) / len(labels)  #计算噪声点个数占总数的比例
print('噪声比:', format(raito, '.2%'))

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)  # 获取分簇的数目

print('分簇的数目: %d' % n_clusters_)


list = []



for i in range(n_clusters_):
    print('簇 ', i, '的所有样本:')
    one_cluster = X[labels == i]
    list.append((one_cluster.shape[0], one_cluster[:, 0].mean(), one_cluster[:, 1].mean()))
    print(one_cluster)
    plt.scatter(one_cluster[:,0], one_cluster[:,1], s=7)


plt.grid(True)

font1 = {'family': 'Times New Roman',
'weight': 'heavy',
'size' : 12,
}

if day == 13:
    plt.title('Clusters for pick-up position in weekdend', font1)
else:
    plt.title('Clusters for pick-up position in weekday', font1)



list = np.array(list)

print(list)

plt.savefig("./pic/dbscan_{}.png".format(day))
