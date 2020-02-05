import matplotlib.pylab as plt
from matplotlib.patches import Ellipse
from mcmtools import *


plt.rcParams['savefig.dpi'] = 1000
plt.rcParams['figure.dpi'] = 1000


odata = read_file("./data/order_13", "rb", "o")

a = plt.subplot(111, aspect='equal')

(lop, lap), (lod, lad) = MC(odata)

(t1, e11, e12), (t2, e21, e22) = SDE(odata)

ec1 = Ellipse(xy=(lod, lad), width=e21, height=e22, angle=t1*180/3.1415926)
ec1.set_facecolor("yellow")
ec1.set_alpha(0.25)
a.add_artist(ec1)
a.grid(True)

for i in range(0, odata.shape[0], 200):
    #pick
    lon_p = odata['lon_pick'][i]
    lat_p = odata['lat_pick'][i]
    a.scatter(lon_p, lat_p, c="red", marker="o", s=1)
    #drop
    lon_d = odata['lon_drop'][i]
    lat_d = odata['lat_drop'][i]
    a.scatter(lon_d, lat_d, c="green", marker="x", s=1)

    #print("draw:[{}/{}]".format(i / 100, odata.shape[0] / 100))


a.scatter(lop, lap, c="yellow", marker="*", s=30)
a.scatter(lod, lad, c="blue", marker="*", s=30)




plt.savefig("./pic/scat.png")

