import sympy
import numpy as np
import math
from matplotlib.pyplot import plot
from matplotlib.pyplot import show
import matplotlib.pyplot as plt
import matplotlib

fig = plt.figure()
#提前知道三个AP的大概位置坐标
maxy = 20
maxx = 20
cx=[5,8,9]
cy=[5,15,17]
dot1 = plot(cx,cy,'k^')

# A为距离设备1米时的rssi绝对值,n为环境衰减因子
# dBm = (quality / 2) - 100
def rssiRange(rssi):
    A = -145.657
    n = 6.39
    iRssi = -rssi
    power = float((iRssi - A ) / ( 10 * n ))
    print("power = %f" %power)
    result = pow(10, power)
    return result

#生成盲节点，以及其与参考节点欧式距离
mtx = 10
mty = 14
# plt.hold('on')
dot2 = plot(mtx,mty,'go')
da = rssiRange(81)
db = rssiRange(87)
dc = rssiRange(99)
dis = [da,db,dc]
print("da = %d" %da)
print("db = %d" %db)
print("dc = %d" %dc)

for i in range(3):
    theta = np.arange(0, 2*np.pi, 0.01)
    x = cx[i] + dis[i] * np.cos(theta)
    y = cy[i] + dis[i] * np.sin(theta)
    axes = fig.add_subplot(111)
    axes.plot(x, y)
    axes.axis('equal')

CrossPointx = []
CrossPointy = []
#计算定位坐标
def threePoints():
    px = 0
    py = 0
    for i in range(3):
        for j in range(3):
            if j <= i:
                continue
            # 圆心距离PQ
            p2p = float(np.sqrt((cx[i] - cx[j])*(cx[i] - cx[j]) + (cy[i] - cy[j])*(cy[i] - cy[j])))
            # 判断两圆是否相交
            if dis[i] + dis[j] <= p2p:
                # 不相交，按比例求
                CrossPointx.append(cx[i] + (cx[j] - cx[i])*dis[i] / (dis[i] + dis[j]))
                CrossPointy.append(cy[i] + (cy[j] - cy[i])*dis[i] / (dis[i] + dis[j]))
                # plt.plot(cx[i] + (cx[j] - cx[i])*dis[i] / (dis[i] + dis[j]), cy[i] + (cy[j] - cy[i])*dis[i] / (dis[i] + dis[j]), 'om')  # 绘制紫红色的圆形的点
                px += cx[i] + (cx[j] - cx[i])*dis[i] / (dis[i] + dis[j])
                py += cy[i] + (cy[j] - cy[i])*dis[i] / (dis[i] + dis[j])
            elif p2p <= abs(dis[i] - dis[j]):
                px += (cx[j] + cx[i])/2
                py += (cy[j] + cy[i])/2
                CrossPointx.append((cx[j] + cx[i])/2)
                CrossPointy.append((cy[j] + cy[i])/2)
                # plt.plot((cx[j] + cx[i])/2, (cy[j] + cy[i])/2, 'r*')  # 绘制紫红色的圆形的点
            else:
                dr = p2p / 2 + (dis[i] * dis[i] - dis[j] * dis[j]) / (2 * p2p)
                CrossPointx.append(cx[i] + (cx[j] - cx[i])*dr / p2p)
                CrossPointy.append(cy[i] + (cy[j] - cy[i])*dr / p2p)
                # plt.plot(cx[i] + (cx[j] - cx[i])*dr / p2p, cy[i] + (cy[j] - cy[i])*dr / p2p, 'r*')  # 绘制紫红色的圆形的点
                px += cx[i] + (cx[j] - cx[i])*dr / p2p
                py += cy[i] + (cy[j] - cy[i])*dr / p2p
    # 三个圆两两求点，最终得到三个点，求其均值
    px /= 3
    py /= 3
    return px, py



locx,locy = threePoints()
dot3 = plot(locx,locy,'om')

dot4 = plot(CrossPointx,CrossPointy,'r*')

#显示脚注
x = [[locx,cx[0]],[locx,cx[1]],[locx,cx[2]]]
y = [[locy,cy[0]],[locy,cy[1]],[locy,cy[2]]]
for i in range(len(x)):
    plt.plot(x[i],y[i],linestyle = '--',color ='g' )
plt.title('Trilateration')
plt.legend(['AP','Blind','Range1','Range2','Range3','Result','Cross Point'], loc='lower right')
show()
