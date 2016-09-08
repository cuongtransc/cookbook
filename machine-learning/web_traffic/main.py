import scipy as sp
import matplotlib.pyplot as plt

# Doc data tu file
data = sp.genfromtxt("./web_traffic.tsv", delimiter="\t")
print(data[:10])
print (data.shape)

# Tao 2 vector
# x la gio y la luu luong truy cap
####
x = data[:,0]
y = data[:,1]

# print(sp.sum(sp.isnan(y)))
# print(sp.isnan(y))

# Loai bo cac vi du NAN
x = x[~sp.isnan(y)]
y = y[~sp.isnan(y)]

# Ve do thi
plt.scatter(x,y)
plt.title("Luu luong truy cap web")
plt.xlabel("Thoi gian")
plt.ylabel("Truy cap/gio")
plt.xticks([w*7*24 for w in range(5)],['Tuan %i'%(w+1) for w in range(5)])
plt.autoscale(tight=True)
plt.grid()
# plt.show()

# Gia su hoc ham ax + b = y
# Trich rut ham bac nhat tu tap hoc
fp1, residuals, rank, sv, rcond = sp.polyfit(x, y, 1, full = True)
# [a, b]
print(fp1)

# Get ham so cua model
f1 = sp.poly1d(fp1)

# Dinh nghia ham error
def error(f, x, y):
	return sp.sum((f(x) - y)**2)

print (error(f1, x, y))

# Ve do thi
fx = sp.linspace(0, x[-1], 1000) # tao cac gia tri tren truc X
plt.plot(fx, f1(fx), linewidth=4)
plt.legend(["Bac = %i" % f1.order], loc = "upper left")
#plt.show()

f2p = sp.polyfit(x, y, 2)
print(f2p)
f2=sp.poly1d(f2p)
print(error(f2, x, y))
plt.plot(fx, f2(fx), 'r--', label = 'Bac = 2', linewidth=4)
plt.show()