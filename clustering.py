# clustering analysis of the data

import matplotlib.pyplot as plt
import matplotlib as mpl

import pymc
import sklearn.mixture as mixture
import numpy as np

import makeGates
reload(makeGates)
from makeGates import liveSamples, singletSamples

import seaborn as sns




model = mixture.GMM(n_components=2)
rawData = singletSamples[2].data[['M Cherry-A', 'SSC-A']] 
#toFit = np.nan_to_num( np.log10( rawData) )
#model.fit( toFit)
#means = [ model.means_[0,i] for i in [0,1]]
#covars = model._get_covars()

fig = plt.figure()
ax = plt.gca()
#ax.scatter( singletSamples[0]['M Cherry-A'], singletSamples[0]['SSC-A'], s=1, alpha=0.3, color='blue')
#ax.scatter( singletSamples[-1]['M Cherry-A'], singletSamples[-1]['SSC-A'], s=0.2, alpha=0.3, color='green')
#ax.scatter( singletSamples[-5]['M Cherry-A'], singletSamples[-5]['SSC-A'], s=1, alpha=0.4, color='red')

ax.scatter( singletSamples[2]['M Cherry-A'], singletSamples[2]['SSC-A'], s=0.2, alpha=0.3, color='green')
ax.scatter( singletSamples[1]['M Cherry-A'], singletSamples[1]['SSC-A'], s=1, alpha=0.4, color='red')

#norm = singletSamples[1]['M Cherry-A'] / singletSamples[1]['SSC-A']
#plt.hist( norm, bins=np.logspace(-3, 0, 300))
#ax.set_xlim([10**-3,10**0])

ax.set_xlim([0,8000])
#ax.set_yscale('log')
#ax.set_xscale('log')

plt.show()



