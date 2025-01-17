import Simulação1 as Sm
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

Tn = []
vald = []
valv = []
for i in range(100):
    Sim, val1, val2 = Sm.Main(100, 1000000, 2)
    vald += [val1]
    valv += [val2]
    Tn += [Sim]
    print(Tn)
res = stats.ecdf(Tn)
ax = plt.subplot()
res.cdf.plot(ax)
m = np.mean(Tn)
x = np.linspace(stats.expon.ppf(0.01, 0, m), stats.expon.ppf(0.99, 0, m), 100)
cdf = stats.expon.cdf(x, 0, m)
plt.plot(x, cdf)
print(stats.kstest(Tn, 'expon', args=(0, m)))
print(vald, "\n", valv)
print(all(vald))
print(all(valv))
plt.show()