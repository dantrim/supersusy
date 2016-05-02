#!/usr/bin/env python

from optparse import OptionParser
from math import sqrt
import os

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(False)

import sys
sys.path.append(os.environ['SUSYDIR'])

from glob import glob

r.TH1F.__init__._creates = False
r.TGraph2D.__init__._creates = False
r.TLatex.__init__._creates = False


import supersusy.utils.plot_utils as pu
import supersusy.utils.utils as utils
import supersusy.utils.plot as plot

import supersusy.utils.background as background
import supersusy.susyana.znplotter.znregion as znregion
import supersusy.susyana.znplotter.znsignal as znsignal


def get_optConfig(conf_) :
    configuration_file = ""
    configuration_file = "./" + indir + "/" + conf_ + ".py"
    if os.path.isfile(configuration_file) :
        return configuration_file
    else :
        print "znplotter::get_optConfig    ERROR Input config ('%s') is not found in the directory and/or"
        print "znplotter::get_optConfig    ERROR path ('%s')."%(conf_, configuration_file)
        sys.exit()

def get_grid_file(gridname) :

    fname = os.environ['SUSYDIR']
    spacer = ""
    if not fname.endswith("/") :
        spacer = "/"
    fname += spacer + "supersusy/susyinfo/%s/masses_%s.txt"%(gridname,gridname)
    if not os.path.isfile(fname) :
        print "znplotter::get_grid_file    ERROR SUSY info file for grid %s not found in"%gridname
        print "znplotter::get_grid_file    ERROR expected location: %s"%fname 
        sys.exit()

    print "znplotter::get_grid_file    SUSY info file found: %s"%fname
    return fname
    

def get_signal_grid(file_rawdir, grid_name) :

    grid_configuration_file = get_grid_file(grid_name)

    sig_list = []
    lines = open(grid_configuration_file).readlines()

    header_line = lines[0]
    header_line = header_line.strip().split()
    print header_line
    if not header_line[0] == "DSID" or not len(header_line) > 1:
        print "znplotter::get_signal_grid    ERROR SUSY info file ('%s') expected to have first"%grid_configuration_file
        print "znplotter::get_signal_grid    ERROR line be of format:"
        print "znplotter::get_signal_grid           DSID mX[GeV] mY[GeV] ..."
        sys.exit()


    spacer = ""
    if not file_rawdir.endswith("/") :
        spacer = "/"
    raw_files = glob(file_rawdir + spacer + "CENTRAL_*.root")

    n_masses = -1
    if len(header_line)==3 :
        n_masses = 2
    elif len(header_line)==4 :
        n_masses = 3

    n_ok = 0
    n_expected = 0

    for line in lines[1:] :
        if not line : continue
        if line.startswith("#") : continue
        line = line.strip()
        dsid_ = int(line.split()[0])
        mX_ = float(line.split()[1])
        mY_ = float(line.split()[2])
        mZ_ = -1
        if n_masses > 2 :
            mZ_ = float(line.split()[3])

        sigpoint = znsignal.ZnSignal(dsid_, mX_, mY_, mZ_)

        n_expected += 1

        files_for_this_point = []
        for rf_ in raw_files :
            if "entrylist_" in rf_ : continue
            if str(dsid_) in rf_ :
                files_for_this_point.append(rf_)

        fileOK = True
        if len(files_for_this_point) == 0 :
            print "znplotter::get_signal_grid    WARNING No files found for signal point DSID %d (%.1f,%.1f,%.1f)"%(dsid_, mX_, mY_, mZ_)
            fileOK = False
         #   sys.exit()
        if len(files_for_this_point) > 1 :
            print "znplotter::get_signal_grid    WARNING More than 1 file found for signal point DSID %d (%.1f,%.1f,%.1f)"%(dsid_, mX_, mY_, mZ_)
            sys.exit()

        file_for_this_point = ""
        if fileOK :
            n_ok += 1
            file_for_this_point = files_for_this_point[0]
            print file_for_this_point

            sigpoint.setFile(file_for_this_point)
            sigpoint.setTree()

            sig_list.append(sigpoint)

    print "znplotter::get_signal_grid    INFO Found %d/%d of the signal points from the input"%(n_ok,n_expected)
    print "znplotter::get_signal_grid    INFO grid file ('%s') and directory ('%s')"%(grid_configuration_file, file_rawdir)

    return sig_list

def get_yield(bkg_, tcut, region_name) :
    cut = "(" + tcut + ") * eventweight * " + str(bkg_.scale_factor)
    cut = r.TCut(cut)
    sel = r.TCut("1")
    h = pu.th1f("h_" + bkg_.name + "_yield_" + region_name, "", 4, 0, 1, "", "")
    cmd = "%s>>%s"%("isMC", h.GetName())
    bkg_.tree.Draw(cmd, cut * sel, "goff") 

    err = r.Double(0.0)
    integral = h.IntegralAndError(0, -1, err)
    h.Delete()
    return integral, err

def get_signal_yield(sig_, tcut, region_name, extra_weight = "") :
    extra_ = ""
    cut = ""
    if not extra_weight == "" :
        cut = "(" + tcut + ") * eventweight * " + str(sig_.scale_factor) + " * " + str(extra_weight)
    else :
        cut = "(" + tcut + ") * eventweight * " + str(sig_.scale_factor) 
    cut = r.TCut(cut) 
    sel = r.TCut("1")
    h = pu.th1f("h_" + sig_.name + "_yield_" + region_name, "", 4, 0, 1, "", "")
    cmd = "%s>>%s"%("isMC", h.GetName())
    sig_.tree.Draw(cmd, cut * sel, "goff")

    err = r.Double(0.0)
    integral = h.IntegralAndError(0, -1, err)
    h.Delete()
    return integral
    
        

    
            
def get_significance(bkgs_, sigs_, reg_, metric = "", rel_uncer = 0.0) :

    ###########################
    ## get the total bkg yield
    n_bkg = 0.0
    n_bkg_err = 0.0
    for bkg in bkgs_ :
        integral, stat_err = get_yield(bkg, reg_.getTcut(), reg_.name)
        n_bkg += integral
        n_bkg_err += stat_err * stat_err
    n_bkg_err = sqrt(n_bkg_err)

    total_rel_error = sqrt( (n_bkg_err/n_bkg)**2 + (rel_uncer)**2)

    ########################
    ## get the signal yields
    print "adding 3body right polarization weight"
    for sig in sigs_ :

        significance = 0

        integral = get_signal_yield(sig, reg_.getTcut(), reg_.name, "susy3BodyRightPol")
        sig.yields[reg_.name] = integral

        if metric == "Zn" :
            zn = r.RooStats.NumberCountingUtils.BinomialExpZ(integral, n_bkg, total_rel_error)
            if zn < 0 : zn = 0.001
            significance = zn

        else :
            print "get_significance    ERROR Unhandled significance metric provided ('%s')"%metric
            sys.exit()

        sig.significance_dict[reg_.name] = significance

    



################################################################
#### MAIN
################################################################
if __name__ == "__main__" :

    # print out Kirkby
    r.RooStats.NumberCountingUtils.BinomialExpZ(4, 4, 0.3)

    global optConfig, indir, requestRegion, outdir, dbg


    parser = OptionParser()
    parser.add_option("-c", "--optConfig", dest="optConfig", default="")
    parser.add_option("-i", "--indir", dest="indir", default="")
    parser.add_option("-r", "--requestRegion", dest="requestRegion", default="")
    parser.add_option("-o", "--outdir", dest="outdir", default="./")
    parser.add_option("-d", "--dbg", action="store_true", dest="dbg", default=False)
    (options, args) = parser.parse_args()
    optConfig       = options.optConfig
    indir           = options.indir
    outdir          = options.outdir
    requestRegion   = options.requestRegion
    dbg             = options.dbg



    print " ++ ----------------------------- ++ " 
    print "     znplotter "
    print ""
    print "  config directory      : %s"%indir
    print "  config                : %s"%optConfig
    print "  output directory      : %s"%outdir
    print "  requested region      : %s"%requestRegion
    print "  debug                 : %s"%dbg
    print ""
    print " ++ ----------------------------- ++ "


    ######################################
    ## grab the config file
    config = get_optConfig(optConfig)
    print "znplotter    Found configuration file: %s"%config

    #####################################
    ## containers for backrounds, ZnRegions, ZnSignals
    backgrounds = []
    regions = []

    signal_file_rawdir = ""
    signal_grid = ""
    signal_scale_factor = 1.0
    signals = []

    significance_metric = ""

    bkg_uncertainty = 0.0 #fractional


    #######################################
    ## fill the containers and signal info
    execfile(config)

    if signal_file_rawdir == "" :
        print "znplotter    ERROR signal_file_rawdir is empty!"
        sys.exit()
    if signal_grid == "" :
        print "znplotter    ERROR signal_grid is empty!"
        sys.exit()
    if not os.path.isdir(signal_file_rawdir) :
        print "znplotter    ERROR signal_file_rawdir ('%s') is not found!"%signal_file_rawdir
        sys.exit()


    # check regions loaded
    for reg in regions :
        reg.Print()

    # check backgrounds loaded
    for bkg in backgrounds :
        bkg.Print()
        print bkg.tree.GetEntries()

    # get the signal grid
    signals = get_signal_grid(signal_file_rawdir, signal_grid)
    for s in signals :
        s.scale_factor = signal_scale_factor
    print "signal scale factor = ", signal_scale_factor

    #####################################
    ## get the significance for each region
    for reg in regions :
        if reg.isParent() :
            for ch_reg in reg.orthogonal_subregions :
                get_significance(backgrounds, signals, ch_reg, significance_metric, bkg_uncertainty)
        else :
            get_significance(backgrounds, signals, reg, significance_metric, bkg_uncertainty)

    ## at this point we have the significance evaluated at each
    ## point of the grid --> just need to start plotting now
