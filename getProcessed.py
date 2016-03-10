#imports and gates flow data
import flowSettings
reload(flowSettings)
from flowSettings import makeSettings

import importFlow
reload(importFlow)
from importFlow import importFlow, filterBubbles

import makeGates
reload(makeGates)
from makeGates import applyGates, plotGates


class flowRun(object):
    """docstring for flowRun"""
    def __init__(self, raw, gated, plotGates):
        self.raw = raw
        self.gated = gated
        self.plotGates = plotGates

#run = 'timecourse4Gy'
#run = 'finalRun'
#run = 'titrationD4'

def getProcessed(run):
    # get the settings
    settings = makeSettings( run )

    #get the data
    samples = importFlow(settings.directory)

    for entry in settings.toFilter:
        samples[entry].data = filterBubbles(18000, samples[entry].data)

    # apply gates 
    liveSamples = applyGates( samples, [settings.liveGate])
    singletSamples = applyGates( liveSamples, [ settings.singletGate ])

    return flowRun( samples, singletSamples, lambda: plotGates(samples, settings) )

