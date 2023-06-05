import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import random as rd
import time, datetime
from matplotlib import rcParams

rcParams['figure.autolayout'] = True

bg = 'black'
fg = 'limegreen'
fg2 = 'gray'

def clean_gdp(x):
    years = x['Year'].values.tolist()
    nominal = [float(p.replace('$','').replace(',','')) for p in x['Real GDP (trillions)']]
    del years[0]
    rates = np.array(nominal[1:])/np.array(nominal[:-1]) - 1
    return years, rates.tolist()

def clean_sp(z):
    dates, nums = z['Date'].values.tolist(), z['Price'].values.tolist()
    h = [[i, float(j.replace(',',''))] for i, j in zip(dates, nums) if float(i.split(' ')[-1]) >= 1929 and float(i.split(' ')[-1]) <= 2022]
    x, y = np.array(h).T
    y = np.array([float(k) for k in y])
    y = y[:-1]/y[1:] - 1
    return x.tolist()[::-1], y.tolist()[::-1]

def gatherPresidents():
    names = ('HerbertHoover', 'FDR', 'HarryTruman', 'DwightEisenhower', 'JFK', 'LBJ', 'RichardNixon',
                         'GeraldFord', 'JimmyCarter', 'RonaldReagan', 'GHWB', 'BillClinton', 'GWB', 'Obama', 'DT','Biden')
    imgs = [plt.imread('Presidents/{}.png'.format(n)) for n in names]
    scld = [OffsetImage(ii, zoom=0.27) for ii in imgs]
    return scld

def getPres(cp, ps, mb):
    terms = ((1930, 1934), (1934, 1946), (1946, 1954), (1954, 1962), (1962, 1964), (1964, 1970),
                         (1970, 1975), (1975, 1978), (1978, 1982), (1982, 1990), (1990, 1994), (1994, 2002),
                         (2002, 2010), (2010, 2018), (2018, 2022), (2022, 2024))

    goat = ('Herbert Hoover', 'Franklin D. Roosevelt', 'Harry Truman', 'Dwight Eisenhower',
                     'John F. Kennedy', 'Lyndon Johnson', 'Richard Nixon', 'Gerald Ford', 'Jimmy Carter', 'Ronald Reagan',
                     'George H.W. Bush', 'Bill Clinton', 'George W. Bush', 'Barack Obama', 'Donald Trump','Joe Biden')

    for ii, (t0, t1) in enumerate(terms):
        if ps >= t0 and ps < t1:
            return (t0, t1), cp[ps], mb[ii], ii, goat[ii]
  
gdp = pd.read_csv('GDP3.csv')
sp = pd.read_csv('SP500.csv')


years, rates = clean_gdp(gdp)
sdates, returns = clean_sp(sp)


pres = gatherPresidents()
cmps = {i:np.sum([l for k, l in zip(sdates, returns) if str(i) in k]) for i in years}

fig = plt.figure(figsize=(9,6))
ax = fig.add_subplot(111)
fig.tight_layout()
fig.patch.set_facecolor(bg)
ax.tick_params('x', colors=fg)
ax.tick_params('y', colors=fg)
ax.set_facecolor(fg2)

xx, yy = [], []

prez = {}
kly = {}

bLine = lambda a, b, n: np.array([a + i * (b - a)/(n - 1) for i in range(n)])

plt.pause(4)
for y, r, rt in zip(years, rates, returns):
    king = getPres(cmps, y, pres)
    if king:
        rtn = king[1]
        pic = king[2]
        ax.cla()
        ax.set_title('Year: {} | President: {}'.format(y, king[4]), color=fg)
        xx.append(r); yy.append(rt)
        #ax.scatter(xx, yy)
        
        ax.scatter(-0.17, -0.66, color=fg2)
        xMax, yMax = 0.25, 0.6

        bX, bY = bLine(0, xMax, 20), bLine(0, yMax, 20)

        ax.plot(np.zeros(len(bY)), bY, color=fg, linewidth=2.5)
        ax.plot(bX, np.zeros(len(bX)), color=fg, linewidth=2.5)

        #ax.plot(xx, yy, color='red', linewidth=1.1)

        aus = AnnotationBbox(pic, (r, rt), xycoords='data', frameon=False)
        prez[king[3]] = aus
        for goo, gow in prez.items():
            ax.add_artist(gow)

        ax.set_xlabel("Real GDP Yearly Percent Change", color=fg)
        ax.set_ylabel("S&P 500 Yearly Return", color=fg)
        ax.set_xticklabels(['{0:.2f}%'.format(jo*100) for jo in ax.get_xticks()])
        ax.set_yticklabels(['{0:.2f}%'.format(jo*100) for jo in ax.get_yticks()])
        plt.pause(0.01)









plt.show()

