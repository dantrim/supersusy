#!/usr/bin/env python

import ROOT as r
r.gROOT.SetBatch(False)
r.gStyle.SetOptStat(False)
import sys
sys.path.append('../../..')
sys.dont_write_bytecode = True

import argparse
import os

import supersusy.utils.plot_utils as pu
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region
import supersusy.utils.plot as plot

def get_plotConfig(conf) :
    configuration_file = ""
    configuration_file = "./plotConfig/" + conf + ".py"
    if os.path.isfile(configuration_file) :
        return configuration_file
    else :
        print 'get_plotConfig ERROR    Input plotConfig ("%s") is not found in the plotConfig/ directory. Does it exist? Exitting.'%conf
        sys.exit()

def check_for_consistency(plots, regions) :
    '''
    Make sure that the plots are not asking for a region that
    has not been loaded in the config
    '''
    bad_regions = []
    configured_regions = []
    for r in regions :
        configured_regions.append(r.simplename)
    for p in plots :
        current_region = p.region
        if current_region not in configured_regions :
            bad_regions.append(current_region)
    if len(bad_regions) > 0 :
        print 'check_for_consistency ERROR    You have configured a plot for a region that has not also been configured:'
        print bad_regions
        print 'check_for_consistency ERROR    The regions set-up in the configuration ("%s") are:'%plotConfig
        for r in configured_regions :
            print "check_for_consistency ERROR     > '%s'"%(r)
        print "check_for_consistency ERROR    Exitting."
        sys.exit()
    else :
        print "check_for_consistency    Plots and regions consistent."

if __name__=="__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--plotConfig")
    args = parser.parse_args()
    global plotConfig
    plotConfig = args.plotConfig

    conf_file = get_plotConfig(plotConfig)
    print conf_file

    plots = []
    data = None
    backgrounds = []
    regions = []
    execfile(conf_file)
    for p in plots :
        p.Print()
        print p
        print "    nbins: %s"%str(p.nbins)
        if p.ratioCanvas :
            print "    rcan: %s"%str(p.ratioCanvas.canvas.GetName())
            print p.ratioCanvas.upper_pad
            print p.ratioCanvas.lower_pad
    print ""
    for b in backgrounds :
        b.Print()
    print ""
    for r in regions :
        r.Print()
    print ""
    data.Print()

    check_for_consistency(plots, regions)
