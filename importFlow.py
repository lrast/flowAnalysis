#imports flow data
import FlowCytometryTools
import os

from FlowCytometryTools import FCMeasurement



directory = './titration'


toImport = os.listdir(directory)


samples = [FCMeasurement(ID=entry, datafile=directory+'/'+entry) for entry in toImport]
