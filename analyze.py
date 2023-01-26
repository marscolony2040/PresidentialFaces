import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import random as rd
import time, datetime
from matplotlib import rcParams

rcParams['figure.autolayout'] = True


def clean_gdp(x):
    years = x['Year'].values.tolist()
    nominal = [float(p.replace('$','').replace(',','.')) for p in x['Nominal GDP (trillions)']]
    del years[0]
    rates = np.array(nominal[1:])/np.array(nominal[:-1]) - 1
    return years, rates.tolist()

def clean_sp(z):
    dates, nums = z['Date'].values.tolist(), z['Price'].values.tolist()
    h = [[i, float(j.replace(',',''))] for i, j in zip(dates, nums) if float(i.split(' ')[-1]) >= 1929 and float(i.split(' ')[-1]) <= 2021]
    x, y = np.array(h).T
    y = np.array([float(k) for k in y])
    y = y[:-1]/y[1:] - 1
    return x.tolist()[::-1], y.tolist()[::-1]

def gatherPresidents():
    names = ('HerbertHoover', 'FDR', 'HarryTruman', 'DwightEisenhower', 'JFK', 'LBJ', 'RichardNixon',
                         'GeraldFord', 'JimmyCarter', 'RonaldReagan', 'GHWB', 'BillClinton', 'GWB', 'Obama', 'DT')
    imgs = [plt.imread('Presidents/{}.png'.format(n)) for n in names]
    scld = [OffsetImage(ii, zoom=0.27) for ii in imgs]
    return scld

def getPres(cp, ps, mb):
    terms = ((1930, 1933), (1933, 1945), (1945, 1953), (1953, 1961), (1961, 1963), (1964, 1969),
                         (1969, 1974), (1974, 1977), (1977, 1981), (1981, 1989), (1989, 1993), (1993, 2001),
                         (2001, 2009), (2009, 2017), (2017, 2021))

    goat = ('Herbert Hoover', 'Franklin D. Roosevelt', 'Harry Truman', 'Dwight Eisenhower',
                     'John F. Kennedy', 'Lyndon Johnson', 'Richard Nixon', 'Gerald Ford', 'Jimmy Carter', 'Ronald Reagan',
                     'George H.W. Bush', 'Bill Clinton', 'George W. Bush', 'Barack Obama', 'Donald Trump')

    for ii, (t0, t1) in enumerate(terms):
        if ps >= t0 and ps < t1:
            return (t0, t1), cp[ps], mb[ii], ii, goat[ii]
  
gdp = pd.read_csv('GDP.csv')
sp = pd.read_csv('SP500.csv')

years, rates = clean_gdp(gdp)
sdates, returns = clean_sp(sp)


pres = gatherPresidents()
cmps = {i:np.sum([l for k, l in zip(sdates, returns) if str(i) in k]) for i in years}

fig = plt.figure(figsize=(9,6))
ax = fig.add_subplot(111)
fig.tight_layout()

xx, yy = [], []

prez = {}
kly = {}

bLine = lambda a, b, n: np.array([a + i * (b - a)/(n - 1) for i in range(n)])


for y, r, rt in zip(years, rates, returns):
    king = getPres(cmps, y, pres)
    if king:
        rtn = king[1]
        pic = king[2]
        ax.cla()
        ax.set_title('Year: {} | President: {}'.format(y, king[4]), color='blue')
        xx.append(r); yy.append(rt)
        #ax.scatter(xx, yy)
        
        ax.scatter(-0.17, -0.66, color='white')
        xMax, yMax = 0.25, 0.6

        bX, bY = bLine(0, xMax, 20), bLine(0, yMax, 20)

        ax.plot(np.zeros(len(bY)), bY, color='limegreen', linewidth=0.9)
        ax.plot(bX, np.zeros(len(bX)), color='limegreen', linewidth=0.9)

        ax.plot(xx, yy, color='red', linewidth=1.9, alpha=0.5)
        ax.plot(xx, yy, color='white', linewidth=1.2, alpha=0.5)
        ax.plot(xx, yy, color='blue', linewidth=0.5, alpha=0.5)

        aus = AnnotationBbox(pic, (r, rt), xycoords='data', frameon=False)
        prez[king[3]] = aus
        for goo, gow in prez.items():
            ax.add_artist(gow)

        ax.set_xlabel("Nominal GDP Yearly Percent Change", color='blue')
        ax.set_ylabel("S&P 500 Yearly Return", color='blue')
        ax.set_xticklabels(['{0:.2f}%'.format(jo*100) for jo in ax.get_xticks()])
        ax.set_yticklabels(['{0:.2f}%'.format(jo*100) for jo in ax.get_yticks()])
        plt.pause(0.001)









plt.show()
