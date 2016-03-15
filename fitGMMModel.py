# attempts to fit models to the data

import itertools
import numpy as np

from scipy import linalg
import matplotlib.pyplot as plt
import matplotlib as mpl

from sklearn import mixture

from getProcessed import getProcessed
timecourse = getProcessed('finalRun')


covariance_type='full'

def plotModel(gmm, data):
    # plots an ellipse corresponding to the gmm
    # cribbed from sckit-learn docs: 
    color_iter = itertools.cycle([ 'g', 'b','k', 'r', 'c', 'm', 'y'])
    Ys = gmm.predict(data)

    splot = plt.subplot(1, 1, 1)
    iterateThrough = enumerate(zip(gmm.means_, gmm.covars_, color_iter))

    # this API seems TERRIBLE
    if covariance_type == 'tied':
        covars = np.array([ gmm.covars_, gmm.covars_])
        iterateThrough = enumerate(zip(gmm.means_, covars, color_iter))

    for i, (mean, covar, color) in iterateThrough:

        if not np.any(Ys == i):
            continue
        ax = plt.scatter(data[Ys == i, 0], data[Ys == i, 1], .5, color=color)

        v, w = linalg.eigh(covar)
        # Plot an ellipse to show the Gaussian component
        angle = np.arctan2(w[0][1], w[0][0])
        angle = 180 * angle / np.pi  # convert to degrees
        v *= 4
        ell = mpl.patches.Ellipse(mean, v[0], v[1], 180 + angle, color=color)
        ell.set_clip_box(splot.bbox)
        ell.set_alpha(.6)
        splot.add_artist(ell)

        splot.set_xlim([1, 5])
        splot.set_ylim([4, 5.6])

    plt.show()


#Try using a Gaussian mixture model
models = [ mixture.GMM( n_components=2, covariance_type=covariance_type, n_iter=500, n_init=10) for entry in timecourse.gated]
toFit = [ np.log10(entry.data[['M Cherry-A', 'SSC-A']]).dropna().as_matrix() for entry in timecourse.gated ]

for index in range(len( timecourse.gated)):
    models[index].fit( toFit[index] )

    plotModel( models[index], toFit[index])







