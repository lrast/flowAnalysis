from FlowCytometryTools import PolyGate

import settings
reload(settings)
from settings import makePlate, liveGate, singletGate

import importFlow
reload(importFlow)
from importFlow import *


def applyGates(data, gates):
    # gates the samples (in order) 
    for currGate in gates:
        currData = [ entry.gate(currGate) for entry in data]
        data = currData
    return currData



# plot the live gate
makePlots = 0
if makePlots == 1:
    ungatedPlate = makePlate(samples)
    figure(1); 
    ungatedPlate.plot(['FSC-A', 'SSC-A'], gates=[liveGate], gate_colors='red',
        kind='scatter', hide_tick_lines=False, s=1, alpha=0.3)


    liveSamples = applyGates( samples, [liveGate])
    figure(2);
    livePlate = makePlate( liveSamples )
    livePlate.plot(['FSC-A', 'FSC-H'], gates=[singletGate], gate_colors='red',
        kind='scatter', hide_tick_lines=False, s=1, alpha=0.3)


    singletSamples = applyGates( liveSamples, [ singletGate ])
    singletPlate = makePlate( singletSamples )

    figure(3); mChSCCaxis = singletPlate.plot(['M Cherry-A', 'SSC-A'], kind='scatter', hide_tick_lines=False, s=1, alpha=0.3, xlim=(10**1,10**6))
    figure(4); histxis = singletPlate.plot(['M Cherry-A'], bins=np.logspace(1, 6, 300), hide_tick_lines=False, xlim=(10**1,10**6))


    # make the axes log again
    for entry in np.ndenumerate(mChSCCaxis[1]):
        entry[1].set_xscale('log')
        entry[1].set_yscale('log')

    for entry in np.ndenumerate(histxis[1]):
        entry[1].set_xscale('log')


    plt.show()

else:
    liveSamples = applyGates( samples, [liveGate])
    singletSamples = applyGates( liveSamples, [ singletGate ])


def makeLotsPlots():
    i = 1
    for entry in singletSamples:
        print i, entry.ID
        fig = figure(i)
        ax = fig.add_subplot(1,1,1)
        entry.plot(['M Cherry-A', 'SSC-A'], kind='scatter', s=1, alpha=0.3);
        #entry.plot( ['M Cherry-A'], bins=np.logspace(1, 6, 500) )
        xlim(10**0,10**6)
        ax.set_xscale('log')
        ax.set_yscale('log')

        i+= 1

    plt.show()
