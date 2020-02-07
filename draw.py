import matplotlib.pylab as plt
from matplotlib.patches import Ellipse
from mcmtools import *
from matplotlib import font_manager as fm, rcParams


plt.rcParams['savefig.dpi'] = 500
plt.rcParams['figure.dpi'] = 500
plt.style.use('ggplot')

odata = read_file("./data/order_1", "rb", "o")
a = plt.subplot(111, aspect='equal')
alpha = 4.24 * 2

(lop, lap), (lod, lad) = MC(odata)
(t1, e11, e12), (t2, e21, e22) = SDE(odata)
(t1, e11, e12), (t2, e21, e22) = (t1, alpha * e11, alpha * e12), (t2, alpha * e21, alpha * e22)


ec1 = Ellipse(xy=(lod, lad), width=e21, height=e22, angle=t1 * 180 / 3.1415926)
ec1.set_facecolor("yellow")
ec1.set_alpha(0.25)

print((t1, e11, e12), (t2, e21, e22))

ec2 = Ellipse(xy=(lop, lap), width=e11, height=e12, angle=t2 * 180 / 3.1415926)
ec2.set_facecolor("blue")
ec2.set_alpha(0.25)

a.add_artist(ec1)
a.add_artist(ec2)


a.grid(True)
a.scatter(-1, -1, c="blue", marker="s", alpha=0.25)
a.scatter(-1, -1, c="yellow", marker="s", alpha=0.25)
for i in range(0, odata.shape[0], 200):
    #pick
    lon_p = odata['lon_pick'][i]
    lat_p = odata['lat_pick'][i]
    a.scatter(lon_p, lat_p, c="red", marker="o", s=3)
    #drop
    lon_d = odata['lon_drop'][i]
    lat_d = odata['lat_drop'][i]
    a.scatter(lon_d, lat_d, c="green", marker="o", s=1)

    #print("draw:[{}/{}]".format(i / 100, odata.shape[0] / 100))



a.scatter(lop, lap, c="blue", marker="*", s=120)
a.scatter(lod, lad, c="yellow", marker="*", s=95)

plt.legend(["SDE_pick", "SDE_drop", "Pick-Up position", "Drop-off position"])


plt.xlim(103.8, 104.4)
plt.ylim(30.50, 30.90)

font1 = {'family': 'Times New Roman',
'weight': 'heavy',
'size' : 15,
}

a.set_title('SDE of Pick-Drop position distribution', font1)
plt.savefig("./pic/scat1_new.png")


"""
-1.4492233403374253, 0.03945852567274138, 0.04237395693061733),  #78 degree
(1.284535692192403, 0.04209841723485832, 0.47816252099699214))   #-81 degree
"""