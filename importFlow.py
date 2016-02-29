#imports flow data
import FlowCytometryTools
import os

from FlowCytometryTools import FCMeasurement, FCPlate
from pylab import *


directory = './titration'


toImport = os.listdir(directory)
toImport = [entry for entry in toImport if entry[-4:] == '.fcs']

samples = [FCMeasurement(ID=entry, datafile=directory+'/'+entry) for entry in toImport]


#remove the bubles from the bubbly sample.
#the bubbles start after time 18000
def filterBubbles(cutoff, data):
    #time filter
    filtered = data[ data['Time'] < cutoff ]
    return filtered

samples[7].data = filterBubbles(18000, samples[7].data)


nameMap = {'par-1':samples[1]}
plateMap = {'par-1':('A', 1)}


plateView = FCPlate('aggregated',nameMap, None, shape=(4,3), positions=plateMap)





def makeLotsPlots():
    i = 1
    for entry in samples:
        figure(i)
        entry.plot(['FSC-A', 'SSC-A'], kind='scatter');

        i+= 1

    plt.show()



