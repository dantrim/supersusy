#!/usr/bin/env python


from optparse import OptionParser
import os

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True # don't let root steal cmd-line options
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(False)
import sys
sys.path.append(os.environ['SUSYDIR'])
#sys.path.append('../../../')
#sys.dont_write_bytecode = True

r.TEventList.__init__._creates = False
r.TH1F.__init__._creates = False
r.TGraphErrors.__init__._creates = False
r.TGraphAsymmErrors.__init__._creates = False


import supersusy.utils.plot_utils as pu
import supersusy.utils.utils as utils
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region
import supersusy.utils.plot as plot

def get_plotConfig(conf) :
    configuration_file = ""
    configuration_file = "./" + indir + "/" + conf + ".py"
    if os.path.isfile(configuration_file) :
        return configuration_file
    else :
        print 'get_plotConfig ERROR    Input plotConfig ("%s") is not found in the directory/path (%s). Does it exist? Exitting.'%(conf, configuration_file)
        sys.exit()


def make_threebody_plots(plt, reg, sig) :

    print "not yet finished!"


if __name__ == "__main__" :
    global indir, plotConfig, outdir, dbg
    parser = OptionParser()
    parser.add_option("-c", "--plotConfig", dest="plotConfig", default="")
    parser.add_option("-i", "--indir", dest="indir", default="")
    parser.add_option("-o", "--outdir", dest="outdir", default="./")
    parser.add_option("-d", "--dbg", action="store_true", dest="dbg", default=False)
    (options, args) = parser.parse_args()
    indir           = options.indir
    plotConfig      = options.plotConfig
    outdir          = options.outdir
    dbg             = options.dbg


    print " ++ ------------------------- ++ "
    print "     3-body "
    print ""
    print "    config dir:      %s"%indir
    print "    config:          %s"%plotConfig
    print "    output dir:      %s"%outdir
    print "    debug:           %s"%dbg
    print " ++ ------------------------- ++ "

    conf_file = get_plotConfig(plotConfig)
    print "Found the configuration file: %s"%conf_file

    plots_ = []
    region_ = None
    signal_ = None

    execfile(conf_file)

    if region_.name == "" :
        print "ERROR    Region name is empty!"
        sys.exit()
    if signal_.name == "" :
        print "ERROR    Signal name is empty!"
        sys.exit()

    for pl in plots_ :
        make_threebody_plots(pl, region_, signal_)
