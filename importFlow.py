#imports flow data
import FlowCytometryTools
import os
import numpy as np

from FlowCytometryTools import FCMeasurement, FCPlate
from pylab import *


directory = './titration'

def importFlow(directory):
    toImport = os.listdir(directory)
    toImport = [entry for entry in toImport if entry[-4:] == '.fcs']

    samples = [FCMeasurement(ID=entry, datafile=directory+'/'+entry) for entry in toImport]
    return samples

samples = importFlow(directory)


def filterBubbles(cutoff, data):
    #remove the bubles from the bubbly sample.
    #the bubbles start after time 18000
    filtered = data[ data['Time'] < cutoff ]
    return filtered

samples[6].data = filterBubbles(18000, samples[6].data)

def gainCorrection():
    #corrects for differences in gains between runs
    pass




nameMap = {'par-1':samples[1], 'par-2': samples[3], 'par-4': samples[4], 'par-8': samples[5], 'par-16':samples[2], 'par-ctl': samples[6], 'par-ctl-plate': samples[7],
	'tag-1': samples[8], 'tag-2': samples[10], 'tag-4': samples[12], 'tag-8': samples[13], 'tag-16': samples[9], 'tag-32': samples[11], 'tag-ctl': samples[14],
	'tag-rep-2': samples[16], 'tag-rep-4': samples[17], 'tag-rep-8': samples[18], 'tag-rep-16': samples[15]}


plateMap = {'par-1': ('A', 1), 'par-2': ('A', 2), 'par-4': ('A', 3), 'par-8': ('A', 4), 'par-16': ('A', 5), 'par-ctl': ('A', 6), 'par-ctl-plate': ('A', 7),
    'tag-1': ('B', 1), 'tag-2': ('B', 2), 'tag-4': ('B', 3), 'tag-8': ('B', 4), 'tag-16': ('B', 5), 'tag-32': ('B', 6), 'tag-ctl': ('B', 7),
	'tag-rep-2': ('C', 2), 'tag-rep-4': ('C', 3), 'tag-rep-8': ('C', 4), 'tag-rep-16': ('C', 5),
}


plateView = FCPlate('aggregated',nameMap, None, shape=(3,7), positions=plateMap)



figure(1); plateView.plot(['FSC-A', 'SSC-A'], kind='scatter',  hide_tick_lines=False, s=1)
figure(2); mChSCCaxis = plateView.plot(['M Cherry-A', 'SSC-A'], kind='scatter', hide_tick_lines=False, s=1, xlim=(10**2,10**6))
figure(3); histxis = plateView.plot(['M Cherry-A'], bins=np.logspace(1, 6, 500), hide_tick_lines=False, xlim=(10**2,10**6))


# make the axes log again
for entry in np.ndenumerate(mChSCCaxis[1]):
    entry[1].set_xscale('log')

for entry in np.ndenumerate(histxis[1]):
    entry[1].set_xscale('log')



plt.show()



def makeLotsPlots():
    i = 1
    for entry in samples:
        fig = figure(i)
        ax = fig.add_subplot(1,1,1)
        #entry.plot(['FSC-A', 'SSC-A'], kind='scatter');
        entry.plot( ['M Cherry-A'], bins=np.logspace(1, 6, 500) )
        ax.set_xscale('log')

        i+= 1

    plt.show()



