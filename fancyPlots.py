#makes fancy plots

import seaborn as sns
from pylab import *
import numpy as np

import makeGates
reload(makeGates)
from makeGates import singletSamples



def makePlots():
    i = 1
    for entry in singletSamples[6:7]:
        print i, entry.ID
        g = sns.jointplot( x='M Cherry-A', y='SSC-A', data=entry.data, xlim=(10**1, 10**6), ylim=(10**4, 10**6), marginal_kws=dict(bins=np.logspace(0, 6, 300)), joint_kws={"s": 1} )
        g.fig.get_axes()[0].set_xscale('log')
        g.fig.get_axes()[0].set_yscale('log')

        g.fig.get_axes()[1].set_xscale('log')
        g.fig.get_axes()[2].set_yscale('log')

        i += 1

    sns.plt.show()