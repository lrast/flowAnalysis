# does the full fit.


# fits GMM models

import numpy as np
import pymc as pm
import scipy.stats as stats

import matplotlib as mpl
import matplotlib.pyplot as plt

import copy

import pymc as pm
import scipy.stats as stats

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

toFit = [ np.log10(entry.data[['M Cherry-A', 'SSC-A']]).dropna().as_matrix() for entry in timecourse.gated ]

# fit the control
controlFit = mixture.GMM( n_components=1, covariance_type='full')
controlFit.fit(noTag)

ctlCovars = controlFit.covars_[0]
ctlMean = controlFit.means_[0]

ctlTaus = np.linalg.inv( ctlCovars)

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


# wee need a more complecated fit for the mixtures;
# very ugly
def makeModel(data, tau_post_mean, covType='fixed'):
    # Assignment to a cloud
    p = pm.Uniform("p", 0, 1) #prior

    assignment = pm.Categorical("assignment", [p, 1 - p], size=data.shape[0])

    if covType == 'fixed':
        fitTau = ctlTaus
        #mean prior
        center_0 = pm.MvNormal('center_0', np.array([2.5, 5]), fitTau )
        center_1 = pm.MvNormal('center_1', np.array([3, 5]), fitTau ) 

        
        # while the most one dimensional distributions are comfortable generating multiple samples,
        # the MvNormal is not. As a result, we must make a multi-MvNormal variable
        @pm.stochastic(observed=True)
        def empirical(value=data, center_0=center_0, center_1=center_1, tau=fitTau, assignment=assignment):
            # assume that the data is IID.
            running = 0
            # do each of the the subpopulations independently
            pop_0 = data[assignment == 0]
            pop_1 = data[assignment == 1]


            prob_0 = pm.mv_normal_like(pop_0, center_0, tau)
            prob_1 = pm.mv_normal_like(pop_1, center_1, tau)
            return prob_0 + prob_1
        
        
    elif covType == 'diag':
        #diagonally shaped covariance matrix.

        # This keeps the distribution the same shape, while changing size
        
        #a = pm.Uniform('a', 0.1, 1.99999999)
        a0 = pm.TruncatedNormal('a0', 0.4, 5, 0.1, 0.8)
        a1 = pm.TruncatedNormal('a1', 0.4, 5, 0.1, 0.8)
        
        @pm.deterministic(name='fitTau_0')
        def fitTau_0(a=a0):
            eigs = np.linalg.eig(ctlTaus)
            D = np.diag( eigs[0] * [a, 1/a])
            P = eigs[1]

            return np.dot(P, np.dot( D, np.linalg.inv( P) ) )
        
        @pm.deterministic(name='fitTau_1')
        def fitTau_1(a=a1):
            eigs = np.linalg.eig(ctlTaus)
            D = np.diag( eigs[0] * [a, 1/a])
            P = eigs[1]

            return np.dot(P, np.dot( D, np.linalg.inv( P) ) )
        
        #mean prior
        center_0 = pm.MvNormal('center_0', np.array([2.5, 5]), fitTau_0 )
        center_1 = pm.MvNormal('center_1', np.array([3, 5]), fitTau_1 ) 
        
        # while the most one dimensional distributions are comfortable generating multiple samples,
        # the MvNormal is not. As a result, we must make a multi-MvNormal variable
        @pm.stochastic(observed=True)
        def empirical(value=data, center_0=center_0, center_1=center_1, tau0=fitTau_0, tau1=fitTau_1, assignment=assignment):
            # assume that the data is IID.
            running = 0
            # do each of the the subpopulations independently
            pop_0 = data[assignment == 0]
            pop_1 = data[assignment == 1]


            prob_0 = pm.mv_normal_like(pop_0, center_0, tau0)
            prob_1 = pm.mv_normal_like(pop_1, center_1, tau1)
            return prob_0 + prob_1
        
    else:
        nCTLs = noTag.shape[0]
        fitTau = pm.Wishart('fitTau', nCTLs,  tau_post_mean)
    
        #mean prior
        center_0 = pm.MvNormal('center_0', np.array([2.5, 5]), fitTau )
        center_1 = pm.MvNormal('center_1', np.array([3, 5]), fitTau ) 


        # while the most one dimensional distributions are comfortable generating multiple samples,
        # the MvNormal is not. As a result, we must make a multi-MvNormal variable
        @pm.stochastic(observed=True)
        def empirical(value=data, center_0=center_0, center_1=center_1, tau=fitTau, assignment=assignment):
            # assume that the data is IID.
            running = 0
            # do each of the the subpopulations independently
            pop_0 = data[assignment == 0]
            pop_1 = data[assignment == 1]


            prob_0 = pm.mv_normal_like(pop_0, center_0, tau)
            prob_1 = pm.mv_normal_like(pop_1, center_1, tau)
            return prob_0 + prob_1

    if covType == 'diag':
        expModel = pm.Model( [p, assignment, a0, a1, fitTau_0, fitTau_1, center_0, center_1, empirical])
    else:
        expModel = pm.Model( [p, assignment, fitTau, center_0, center_1, empirical])

    return expModel


# fitting the mixtures

# take samples of the distributions
toFitIndices = [np.random.choice(range(entry.shape[0]), size=(2000,1)) for entry in toFit]
toFitSamples = [ toFit[index][toFitIndices[index], :].squeeze() for index in range(len(toFit)) ]

# make the models
fullModels = [ makeModel(entry, ctlTaus, covType='fixed') for entry in toFitSamples]
fullMCMCs = [ pm.MCMC(entry) for entry in fullModels ]

# fit the models
nSamp = 12000
burn= 2000
times = np.array( range(nSamp-burn) )

i = 0
for entry in fullMCMCs:
    print i
    entry.sample(nSamp, burn)
    
    i += 1



def makePlots():
    plt.subplots(4, 4, sharex='col', sharey='row')

    for index in range(len(fullMCMCs)):
        currModel = fullMCMCs[index]
        currSamples = toFitSamples[index]
        
        a = currModel.trace('assignment')
        assOut = a[-1]
        
        plt.subplot(4, 4, index)
        plt.scatter( currSamples[assOut==0,0],  currSamples[assOut==0,1], 0.5, color='b');
        plt.scatter( currSamples[assOut==1,0],  currSamples[assOut==1,1], 0.5, color='g');
        
        plt.xlim([1,5])
        plt.ylim([4, 5.6])



# various plotting functions
def traceHist(mcmc):
    #plots a histogram of 
    cen0Trace = mcmc.trace('center_0')
    plt.subplot(1,3,1)
    plt.hist( cen0Trace[:], bins=20 );

    cen1Trace = mcmc.trace('center_1')
    plt.subplot(1,3,2)
    plt.hist( cen1Trace[:], bins=20 );

    pTrace = mcmc.trace('p')
    plt.subplot(1,3,2)
    plt.hist( pTrace[:], bins=20 );

    plt.show()







