#imports flow data
import FlowCytometryTools
import os
import numpy as np

from FlowCytometryTools import FCMeasurement, FCPlate
from pylab import *


def importFlow(directory):
    toImport = os.listdir(directory)
    toImport = [entry for entry in toImport if entry[-4:] == '.fcs']

    samples = [FCMeasurement(ID=entry, datafile=directory+'/'+entry) for entry in toImport]
    return samples


def filterBubbles(cutoff, data):
    #remove the bubles from bubbly samples
    #the bubbles start after time cutoff
    filtered = data[ data['Time'] < cutoff ]
    return filtered



