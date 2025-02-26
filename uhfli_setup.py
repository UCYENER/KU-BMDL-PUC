def set_uhfli_tabs_and_settings(START, STOP, NUMBER_OF_POINTS):
    import time
    import zhinst.core

    daq = zhinst.core.ziDAQServer('127.0.0.1', 8004, 6)

    # Starting module scopeModule
    scope = daq.scopeModule()
    scope.set('lastreplace', 1)
    scope.subscribe('/dev2566/scopes/0/wave')
    scope.set('historylength', 100)
    scope.execute()
    scope.set('averager/weight', 10)
    scope.set('averager/restart', 0)
    scope.set('averager/weight', 10)
    scope.set('averager/restart', 0)
    scope.set('fft/power', 0)
    scope.set('mode', 1)
    scope.set('fft/spectraldensity', 0)
    scope.set('fft/window', 1)
    scope.set('save/directory', r'C:\Users\user\Documents\Zurich Instruments\LabOne\WebServer')

    # Starting module dataAcquisitionModule
    daq_module = daq.dataAcquisitionModule()
    daq_module.set('triggernode', '/dev2566/demods/0/sample.R')
    daq_module.set('preview', 1)
    daq_module.set('device', 'dev2566')
    daq_module.set('historylength', 100)
    daq_module.set('count', 1)
    daq_module.set('type', 6)
    daq_module.set('edge', 1)
    daq_module.set('bits', 1)
    daq_module.set('bitmask', 1)
    daq_module.set('eventcount/mode', 1)
    daq_module.set('delay', -0.00000500)
    daq_module.set('grid/mode', 4)
    daq_module.set('grid/cols', 20)
    daq_module.set('duration', 0.00004551)
    daq_module.set('bandwidth', 0.00000000)
    daq_module.set('pulse/min', 0.00000000)
    daq_module.set('pulse/max', 0.00100000)
    daq_module.set('holdoff/time', 0.00000000)
    daq_module.set('holdoff/count', 0)
    daq_module.set('grid/rows', 100)
    daq_module.set('grid/repetitions', 1)
    daq_module.set('grid/rowrepetition', 0)
    daq_module.set('grid/direction', 0)
    daq_module.set('grid/waterfall', 0)
    daq_module.set('grid/overwrite', 0)
    daq_module.set('fft/window', 1)
    daq_module.set('refreshrate', 5.00000000)
    daq_module.set('awgcontrol', 0)
    daq_module.set('historylength', 51)
    daq_module.set('bandwidth', 0.00000000)
    daq_module.set('hysteresis', 0.01000000)
    daq_module.set('level', 0.10000000)
    daq_module.set('triggernode', '/dev2566/demods/0/sample.TrigAWGTrig1')
    daq_module.set('save/directory', r'C:\Users\user\Documents\Zurich Instruments\LabOne\WebServer')
    daq_module.set('clearhistory', 1)
    daq_module.set('clearhistory', 1)
    daq_module.set('bandwidth', 0.00000000)
    daq_module.set('clearhistory', 1)

    # Starting module sweep
    sweeper = daq.sweep()
    sweeper.set('device', 'dev2566')
    sweeper.set('xmapping', 1)
    sweeper.set('historylength', 100)
    sweeper.set('scan', 0)
    sweeper.set('xmapping', 0)
    sweeper.set('loopcount', 1)
    sweeper.set('gridnode', '/dev2566/oscs/0/freq')
    sweeper.set('bandwidth', 112849.89695476)
    sweeper.set('order', 4)
    sweeper.set('settling/inaccuracy', 0.10000000)
    sweeper.set('settling/time', 0.00000000)
    sweeper.set('averaging/tc', 0.00000000)
    sweeper.set('averaging/sample', 13)
    sweeper.set('averaging/time', 0.00000000)
    sweeper.set('filtermode', 1)
    sweeper.set('maxbandwidth', 100000.00000000)
    sweeper.set('bandwidthoverlap', 1)
    sweeper.set('omegasuppression', 40.00000000)
    sweeper.set('phaseunwrap', 0)
    sweeper.set('sincfilter', 0)
    sweeper.set('awgcontrol', 1)
    sweeper.set('historylength', 51)
    sweeper.set('bandwidthcontrol', 1)
    sweeper.set('save/directory', r"C:\Users\user\Documents\Umut\20240506 UCY UScomm uhfli python real-time automation\deneme 1\data")

    # Starting module awgModule
    awg = daq.awgModule()
    awg.set('device', 'dev2566')
    sweeper.set('samplecount', NUMBER_OF_POINTS)
    sweeper.set('start', START)
    sweeper.set('stop', STOP)
    awg.set('index', 0)
    awg.execute()
    awg.set('compiler/sourcefile', 'awg sequencer code real time.seqc')
    awg.set('compiler/start', 1)

    sweeper.set('endless', 0)
    sweeper.set('device', 'dev2566')
    sweeper.subscribe('/dev2566/demods/0/sample')
    sweeper.set("loopcount", 1)
    sweeper.set("save/fileformat", "hdf5")


    return daq, scope, daq_module, sweeper, awg