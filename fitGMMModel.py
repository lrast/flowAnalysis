# attempts to fit models to the data

import itertools
import numpy as np

from scipy import linalg
import matplotlib.pyplot as plt
import matplotlib as mpl

from sklearn import mixture

from getProcessed import getProcessed
timecourse = getProcessed('finalRun')


covariance_type='tied'

def plotModel(gmm, data, plotnum=1, covariance_type=covariance_type):
    # plots an ellipse corresponding to the gmm
    # cribbed from sckit-learn docs: 
    color_iter = itertools.cycle([ 'g', 'b','k', 'r', 'c', 'm', 'y'])
    Ys = gmm.predict(data)

    # this API seems TERRIBLE
    if covariance_type == 'tied':
        covars = np.array([ gmm.covars_, gmm.covars_])
        iterateThrough = enumerate(zip(gmm.means_, covars, color_iter))
    else:   # covariance_type = "full"
        iterateThrough = enumerate(zip(gmm.means_, gmm.covars_, color_iter))

    splot = plt.subplot(4, 4, plotnum)

    for i, (mean, covar, color) in iterateThrough:
        if not np.any(Ys == i):
            continue
        ax = plt.scatter(data[Ys == i, 0], data[Ys == i, 1], .5, color=color)

        v, w = linalg.eigh(covar)
        # Plot an ellipse to show the Gaussian component
        angle = np.arctan2(w[0][1], w[0][0])
        angle = 180 * angle / np.pi  # convert to degrees
        v *= 4
        lighter = {'b':'c', 'g':'y'}
        ell = mpl.patches.Ellipse(mean, v[0], v[1], 180 + angle, color=lighter[color])
        ell.set_clip_box(splot.bbox)
        ell.set_alpha(.6)
        splot.add_artist(ell)


def plotFreqs(fatOn, skinnyOn, dayDict, irDict):
    for day in [0, 2, 4, 6]:
        indices = dayDict[day]
        #plt.subplot(4, 1, day/2+1)

        xline = np.linspace(0,1)
        yline = np.linspace(0, 1)

        for entry in indices:
            marker = '$' + irDict[entry] + '$'
            plt.plot(fatOn[entry], skinnyOn[entry], marker=marker, markersize=18, color='k')
            if day < 6:
                fatNext = fatOn[entry] / ( 2- fatOn[entry] )
                skinnyNext = skinnyOn[entry] / ( 2 - skinnyOn[entry] )
                nextMarker = '$' + irDict[entry] + '-$'
                plt.plot( fatNext, skinnyNext, marker='o', markersize=18, color='c')
                plt.plot( fatNext, skinnyNext, marker=nextMarker, markersize=18, color='k')


        plt.plot( xline, yline, color='red' )
        plt.xlim([0,1])
        plt.ylim([0,1])


def plotTCourse(fatOn, skinnyOn, dayDict, irDict, irDictInv ):
    for day in [0, 2, 4, 6]:
        indices = dayDict[day]

        for entry in indices:
            meanPoint = ( fatOn[entry] + skinnyOn[entry] ) / 2
            pointError = np.abs( fatOn[entry] - skinnyOn[entry] ) / 2

            marker = '$' + irDict[entry] + '$'


            #link to the previous days
            if day == 2:
                prev = 0
                hit = irDict[entry]

            elif day > 2:
                currCondition = irDict[entry]
                parent, hit = currCondition[:-1], currCondition[-1]
                
                prev = irDictInv[ parent]

            if day >= 2:
                prevMean = ( fatOn[prev] + skinnyOn[prev] ) / 2
                if hit == '+':
                    lineColor = 'r'
                elif hit == '-':
                    lineColor = 'b'

                plt.plot( [day-2, day], [prevMean, meanPoint], color=lineColor)



            plt.plot( day, meanPoint, marker=marker, markersize=18, color='k')
            #plt.errorbar(day, meanPoint, yerr=pointError, color='k')

    plt.xlim([0,7])
    plt.ylim([0,1])


def plotDists(gmm, data):
    #plots the on an off distributions as projected to the covariance. 
    pass


#Try using a Gaussian mixture model
if __name__ == '__main__':
    models = [ mixture.GMM( n_components=2, covariance_type=covariance_type, n_iter=500, n_init=10) for entry in timecourse.gated]
    toFit = [ np.log10(entry.data[['M Cherry-A', 'SSC-A']]).dropna().as_matrix() for entry in timecourse.gated ]

    for index in range(len( timecourse.gated)):
        models[index].fit( toFit[index] )

        plotModel( models[index], toFit[index])











