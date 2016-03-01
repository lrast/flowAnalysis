#imports flow data
import FlowCytometryTools
import os
import numpy as np

from FlowCytometryTools import FCMeasurement, FCPlate
from pylab import *

from settings import directory, toFilter


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

for entry in toFilter:
    samples[entry].data = filterBubbles(18000, samples[entry].data)

