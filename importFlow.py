#imports flow data
import FlowCytometryTools
import os
import numpy as np

from FlowCytometryTools import FCMeasurement, FCPlate
from pylab import *

import settings
reload(settings)
from settings import directory, toFilter


def importFlow(directory):
    toImport = os.listdir(directory)
    toImport = [entry for entry in toImport if entry[-4:] == '.fcs']

    samples = [FCMeasurement(ID=entry, datafile=directory+'/'+entry) for entry in toImport]
    return samples

samples = importFlow(directory)


def filterBubbles(cutoff, data):
    #remove the bubles from bubbly samples
    #the bubbles start after time cutoff
    filtered = data[ data['Time'] < cutoff ]
    return filtered

for entry in toFilter:
    samples[entry].data = filterBubbles(18000, samples[entry].data)

