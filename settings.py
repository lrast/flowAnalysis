# settings for various experiments

from FlowCytometryTools import FCMeasurement, FCPlate, PolyGate

run = 'titrationD4'

if run == 'titrationD2':
    # NCS titration day1
    directory = './titration'
    toFilter = [6]

    liveGate = PolyGate([(8.924e+04, 2.587e+05), (2.844e+04, 3.233e+04), (4.515e+04, 1.601e+04), (2.601e+05, 1.241e+05), (2.605e+05, 2.608e+05), (8.924e+04, 2.587e+05)],('FSC-A', 'SSC-A'), region='in', name='gate1')
    singletGate = PolyGate([(3.139e+04, 3.590e+04), (1.941e+05, 1.726e+05), (2.481e+05, 1.733e+05), (3.139e+04, 2.3e+04), (3.139e+04, 3.590e+04)], ('FSC-A', 'FSC-H'), region='in', name='gate1')

    def makePlate(data):
        ## makes the plate layout with the current data
        nameMap = {'par-1': data[1], 'par-2': data[3], 'par-4': data[4], 'par-8': data[5], 'par-16':data[2], 'par-ctl': data[6], 'par-ctl-plate': data[7],
            'tag-1': data[8], 'tag-2': data[10], 'tag-4': data[12], 'tag-8': data[13], 'tag-16': data[9], 'tag-32': data[11], 'tag-ctl': data[14],
            'tag-rep-2': data[16], 'tag-rep-4': data[17], 'tag-rep-8': data[18], 'tag-rep-16': data[15]}

        plateMap = {'par-1': ('A', 1), 'par-2': ('A', 2), 'par-4': ('A', 3), 'par-8': ('A', 4), 'par-16': ('A', 5), 'par-ctl': ('A', 6), 'par-ctl-plate': ('A', 7),
            'tag-1': ('B', 1), 'tag-2': ('B', 2), 'tag-4': ('B', 3), 'tag-8': ('B', 4), 'tag-16': ('B', 5), 'tag-32': ('B', 6), 'tag-ctl': ('B', 7),
            'tag-rep-2': ('C', 2), 'tag-rep-4': ('C', 3), 'tag-rep-8': ('C', 4), 'tag-rep-16': ('C', 5)
        }

        plateView = FCPlate('aggregated',nameMap, None, shape=(3,7), positions=plateMap)

        return plateView


if run == 'titrationD4':
    #NCS titration day 2
    directory = './titrationD4'
    toFilter = []

    liveGate = PolyGate([(1.501e+04, 2.513e+04), (8.787e+04, 2.615e+05), (2.605e+05, 2.615e+05), (2.619e+05, 1.593e+05), (5.074e+04, 7.421e+03), (2.754e+04, 8.102e+03), (1.547e+04, 2.445e+04)], ('FSC-A', 'SSC-A'), region='in', name='gate1')
    singletGate = PolyGate([(1.645e+04, 1.105e+04), (1.733e+04, 2.295e+04), (1.621e+05, 1.481e+05), (2.158e+05, 1.481e+05), (2.393e+04, 1.069e+04), (1.733e+04, 1.069e+04)], ('FSC-A', 'FSC-H'), region='in', name='gate1')

    def makePlate(data):
        ## makes the plate layout with the current data
        nameMap = {'par-1': data[0], 'par-2': data[2], 'par-4': data[4], 'par-8': data[5], 'par-16':data[1], 'par-32':data[3], 'par-ctl': data[6],
            'tag-1': data[7], 'tag-2': data[9], 'tag-4': data[11], 'tag-8': data[12], 'tag-16': data[8], 'tag-32': data[10], 'tag-ctl': data[13] }

        plateMap = {'par-1': ('A', 1), 'par-2': ('A', 2), 'par-4': ('A', 3), 'par-8': ('A', 4), 'par-16': ('A', 5), 'par-32': ('A', 6), 'par-ctl': ('A', 7),
            'tag-1': ('B', 1), 'tag-2': ('B', 2), 'tag-4': ('B', 3), 'tag-8': ('B', 4), 'tag-16': ('B', 5), 'tag-32': ('B', 6), 'tag-ctl': ('B', 7),
        }

        plateView = FCPlate('aggregated',nameMap, None, shape=(2,7), positions=plateMap)

        return plateView




