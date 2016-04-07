# fits GMM models

import numpy as np
import pymc as pm
import scipy.stats as stats

import matplotlib as mpl
import matplotlib.pyplot as plt

import copy

from getProcessed import getProcessed
from sklearn import mixture
from fitGMMModel import plotModel
from scipy import stats


# the data
titrD2 = getProcessed('titrationD2')
titrD4 = getProcessed('titrationD4')
timecourse = getProcessed('finalRun')

noTag = np.log10( titrD4.gated[2].data[['M Cherry-A', 'SSC-A']]).dropna().as_matrix()
negTag = np.log10( titrD4.gated[-1].data[['M Cherry-A', 'SSC-A']]).dropna().as_matrix()

# fit the control
controlFit = mixture.GMM( n_components=1, covariance_type='full')
controlFit.fit(noTag)

ctlCovars = controlFit.covars_[0]
ctlMean = controlFit.means_[0]


#plot the control fit.
xs = np.linspace(1, 5, 200)
ys = np.linspace(4, 5.6, 200)

X, Y = np.meshgrid(xs, ys)
position = np.dstack((X, Y))

full_posterior = stats.multivariate_normal(ctlMean, ctlCovars)

plt.contourf( X, Y, full_posterior.pdf(position), cmap="Blues")
plt.scatter(noTag[:,0], noTag[:,1], 0.3, color='g', alpha=0.4);
plt.xlim([1,5])
plt.ylim([4, 5.6]);
plt.show()

#Try using a Gaussian mixture model
models = []
for entry in timecourse.gated:
    currModel = copy.deepcopy( controlFit )
    currModel.set_params(n_components=2, covariance_type='tied')
    models.append( currModel)


toFit = [ np.log10(entry.data[['M Cherry-A', 'SSC-A']]).dropna().as_matrix() for entry in timecourse.gated ]

for index in range(len(toFit)):
    models[index].fit( toFit[index] )


plt.subplots(4, 4, sharex='col', sharey='row')

for index in range(len( timecourse.gated)):
    models[index].fit( toFit[index] )

    plotModel( models[index], toFit[index], plotnum=index, covariance_type='tied')
    plt.autoscale(tight=True)
    plt.xlim([1,5])
    plt.ylim([4, 5.6])
    #print index



