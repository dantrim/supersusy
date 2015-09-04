#!/usr/bin/env python

from optparse import OptionParser
import os

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(False)
import sys
sys.path.append(os.environ['SUSYDIR'])

r.TH1F.__init__._creates = False
r.TGraph2D.__init__._creates = False
r.TLatex.__init__._creates = False

import supersusy.utils.plot_utils as pu
import supersusy.utils.utils as utils
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region
import supersusy.utils.plot as plot

def get_optConfig(conf) :
    configuration_file = ""
    configuration_file = "./" + indir + "/" + conf + ".py"
    if os.path.isfile(configuration_file) :
        return configuration_file
    else :
        print 'optimizer get_optConfig ERROR    Input optConfig ("%s") is not found in the directory/path ("%s"). Does it exist?'%(conf, configuration_file)
        print 'optimizer get_optConfig ERROR    >>> Exiting.'
        sys.exit()



if __name__=="__main__" :

    # make these blogal
    global optConfig, indir, requestRegion, outdir, dbg

    parser = OptionParser()
    parser.add_option("-c", "--optConfig", dest="optConfig", default="")
    parser.add_option("-m", "--method", dest="method", default="zn")
    parser.add_option("-i", "--indir", dest="indir", default="")
    parser.add_option("-r", "--requestRegion", dest="requestRegion", default="")
    parser.add_option("-o", "--outdir", dest="outdir", default="./")
    parser.add_option("-d", "--dbg", action="store_true", dest="dbg", default=False)
    (options, args) = parser.parse_args()
    optConfig     = options.optConfig
    method        = options.method
    indir         = options.indir
    requestRegion = options.requestRegion
    outdir        = options.outdir
    dbg           = options.dbg


    if method != "zn" :
        print 'optimizer ERROR    You have requested an optimization method that is not yet supported ("%s").'%method
        print 'optimizer ERROR    Currently we only support Zn (BinomialExp) - based optimization routines'
        print 'optimizer ERROR    selected with the "-m" ("--method") option "zn".'
        print 'optimizer ERROR    >>> Exiting.'
        sys.exit()

    print " ++ ----------------------------- ++ "
    print "      optmizer                       "
    print ""
    print "    config directory  :  %s          "%indir
    print "    method            :  %s          "%method
    print "    config            :  %s          "%optConfig
    print "    requested region  :  %s          "%requestRegion
    print "    output directory  :  %s          "%outdir
    print "    debug             :  %s          "%dbg
    print ""
    print " ++ ----------------------------- ++ "

    #########################################
    ## grab the config file
    config = get_optConfig(optConfig)
    print 'optimizer    Found configuration file: %s'%config

    #########################################
    ## grab the backgrounds and regions
    ## from the configuration file
    backgrounds = []
    regions = []
    execfile(config)

    #### parse out the signals
    signals = []
    for background_sample in backgrounds :
        if background_sample.isSignal() : 
            signals.append(background_sample)
            print "optimizer    Found signal sample", background_sample.Print()
