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

import array


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
    h = pu.th1f("h_" + bkg_.name + "_yield_" + region_name, "", 4, 0, 4, "", "")
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
    hname = "%.0f_%.0f"%(sig_.mx, sig_.my)
    h = pu.th1f("h_" + hname + "_yield_" + region_name, "", 4, 0, 4, "", "")
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

    if n_bkg > 0 :
        total_rel_error = sqrt( (n_bkg_err/n_bkg)**2 + (rel_uncer)**2)
    else :
        total_rel_error = rel_uncer

    ########################
    ## get the signal yields
    print "adding 3body right polarization weight"
    for sig in sigs_ :

        significance = 0

        #integral = get_signal_yield(sig, reg_.getTcut(), reg_.name, "1")
        integral = get_signal_yield(sig, reg_.getTcut(), reg_.name, "susy3BodyRightPol")
        sig.yields[reg_.name] = integral

        if metric == "Zn" :
            zn = r.RooStats.NumberCountingUtils.BinomialExpZ(integral, n_bkg, total_rel_error)
           # print "%s : %s : %.2f"%(reg_.name, sig.getName(), zn)
            if zn < 0 : zn = 0.001
            significance = zn

        else :
            print "get_significance    ERROR Unhandled significance metric provided ('%s')"%metric
            sys.exit()

        sig.significance_dict[reg_.name] = significance

    
def combine_subregion_significance(reg_, sigs_) :

    parent_region_name = reg_.name
    child_region_names = []
    for ch in reg_.get_subregions() :
        child_region_names.append(ch.name)

    # now add in quad the sign for each signal point
    # and store it
    for s in sigs_ :
        zn_comb = 0.0
        for ch in child_region_names :
            zn_ = s.significance_dict[ch]
            zn_comb += zn_ * zn_
        zn_comb = sqrt(zn_comb)

        s.significance_dict[parent_region_name] = zn_comb

def do_pwc_combination(region_names_, sigs_) :
    """
    pick the region from the list of parent regions
    'region_names_' that gives the largest
    significance for a given point
    """

    for s in sigs_ :
        significances = {}
        for reg_name in region_names_ :
            significances[reg_name] = s.significance_dict[reg_name]

        # get the region name associated with the largest
        # significance
        best_region = max(significances, key = lambda i: significances[i])

        self.best_region = best_region
        self.best_significance = significances[best_region]


def do_quad_combination(region_names_, sigs_) :
    """
    add in quadrature the significances for each
    of the parent regions whose names are provided
    in 'region_names_'
    """

    for s in sigs_ :
        s.best_region = "COMB"
        zn_comb = 0.0
        significances = []
        for reg_name in region_names_ :
            significances.append(s.significance_dict[reg_name])
        for signif_ in significances :
            zn_comb += signif_ * signif_
        zn_comb = sqrt(zn_comb)
        s.best_significance = zn_comb

def get_best_significance(regs_, sigs_) :

    parent_region_names = []
    region_ids = []
    for reg_ in regs_ :
        if not reg_.isParent() : continue
        if reg_.getId() not in region_ids :
            region_ids.append(reg_.getId())
        parent_region_names.append(reg_.getName())

    if len(region_ids) < len(parent_region_names) :
        print "znplotter::get_best_significance    INFO Treating regions as non-orthogonal"
        print "znplotter::get_best_significance    INFO  -> Will do PWC to combine significances between regions"
        do_pwc_combination(parent_region_names, sigs_)

    elif len(region_ids) == len(parent_region_names) :
        print "znplotter::get_best_significance    INFO Treating regions as orthogonal"
        print "znplotter::get_best_significance    INFO  -> Will add in quadrature the significance of parent regions for the combination"
        do_quad_combination(parent_region_names, sigs_)

    else :
        print "znplotter::get_best_significance    ERROR Unhandled situation!"
        sys.exit()


################################################################
## PLOTTING
################################################################

# set color palette to please your eyes
def set_palette(name='', ncontours=999) :
    if name == "gray" or name == "grayscale" :
        stops = [0.00, 0.34, 0.61, 0.84, 1.00]
        red   = [1.00, 0.84, 0.61, 0.34, 0.00]
        green = [1.00, 0.84, 0.61, 0.34, 0.00]
        blue  = [1.00, 0.84, 0.61, 0.34, 0.00] 
    else :
        stops = [0.00, 0.34, 0.61, 0.84, 1.00]
        red   = [0.00, 0.00, 0.87, 1.00, 0.51]
        green = [0.00, 0.81, 1.00, 0.20, 0.00]
        blue  = [0.51, 1.00, 0.12, 0.00, 0.00] 

    s = array.array('d', stops)
    R = array.array('d', red)
    g = array.array('d', green)
    b = array.array('d', blue)
    
    npoints = len(s)
    r.TColor.CreateGradientColorTable(npoints, s, R, g, b, ncontours)
    r.gStyle.SetNumberContours(ncontours)

def make_frame(grid_name) :
    n_bins = 100
    frame = r.TH2F("frame", "#scale[0.8]{%s}"%grid_name, n_bins, 100, 450, n_bins, 0, 425)

    frame.SetLabelOffset( 0.012, "X" )
    frame.SetLabelOffset( 0.012, "Y" )

    frame.GetXaxis().SetTitleOffset( 1.33 )
    frame.GetYaxis().SetTitleOffset( 1.47 )

    frame.GetXaxis().SetLabelSize( 0.035 )
    frame.GetYaxis().SetLabelSize( 0.035 )
    frame.GetXaxis().SetTitleSize( 0.04 )
    frame.GetYaxis().SetTitleSize( 0.04 )

    frame.GetXaxis().SetTitleFont( 42 )
    frame.GetYaxis().SetTitleFont( 42 )
    frame.GetXaxis().SetLabelFont( 42 )
    frame.GetYaxis().SetLabelFont( 42 )

    r.gPad.SetTicks()
    r.gPad.SetLeftMargin( 1.2*0.13 )
    r.gPad.SetRightMargin( 2*0.08 )
    r.gPad.SetBottomMargin( 1.2*0.120 )
    r.gPad.SetTopMargin( 1.1*0.060 )

    return frame

def get_forbidden_lines(grid_name) :

    out_lines = []
    if grid_name == "bWN" or grid_name == "bWNnew" :

        x_low = 100.0
        y_low = 0.0

        # delta m = m_w + m_b line
        y_high_w = 350
        slope = 1.0
        y_w = slope * x_low - 84.8
        beginx = x_low
        endx_w = 1.2*365 

        line_w = r.TLine(beginx, y_w, endx_w, endx_w * slope - 84.8)
        line_w.SetLineStyle(9)
        line_w.SetLineWidth(2)
        line_w.SetLineColor(r.kGray+2)
        out_lines.append(line_w)

        # delta m = m_t line
        beginx = 172.5
        #y_t = slope * x_low - 172.5
        y_t = 0.0
        endx_t = 450

        line_t = r.TLine(beginx, y_t, endx_t, endx_t * slope - 172.5)
        #line_t = r.TLine(beginx, y_t, endx_t, endx_t * slope - 172.5)
        line_t.SetLineStyle(9)
        line_t.SetLineWidth(2)
        line_t.SetLineColor(r.kGray+2)
        out_lines.append(line_t)
        
    else :
        print "znplotter::get_forbidden_lines    WARNING Unhandled grid provided ('%s')"%grid_name
        print "znplotter::get_forbidden_lines    WARNING  > Will not provide kinematic boundary lines"

    return out_lines


def make_sensitivity_plot(sigs_, regs_, grid_name) :

    set_palette()

    canvas = r.TCanvas("c_sensitivity", "", 768, 768) 
    canvas.cd()

    frame = make_frame(grid_name)
    frame.Draw("axis")
    frame.GetXaxis().SetTitle("m_{#tilde{t}} [GeV]")
    frame.GetYaxis().SetTitle("m_{#tilde{#chi_{0}}} [GeV]")
    canvas.Update()

    gr = r.TGraph2D(1)
    gr.Clear()
    #gr.SetTitle("g_sensitivity")
    #gr.SetMarginBinsContent(0)
    #gr.SetMaxIter(500000);
    #gr.SetNpx(120)
    #gr.SetNpy(120)
    gr.SetMarkerStyle(r.kFullSquare)
    gr.SetMarkerSize(2*gr.GetMarkerSize())

    for s in sigs_ :
        significance, x, y = 0.0, 0.0, 0.0
        significance = s.best_significance
        x = s.mx
        y = s.my
        if significance < 0.0 : significance = 0.0
      #  if float(x) < 200 :
      #      print "blah : ", float(x)
      #      continue
        gr.SetPoint(gr.GetN(), float(x), float(y), significance)

    if gr.GetN() :
        gr.Draw("colz same")
    canvas.Update()

    # for some reason have to do this after drawing the graph
    tex = r.TLatex(0.0, 0.0, '')
    tex.SetTextFont(42)
    tex.SetTextSize(0.3*tex.GetTextSize())
    for s in sigs_ :
        significance = s.best_significance
        if significance < 0.0 : significance = 0.0
        tex.DrawLatex(float(s.mx), float(s.my), "%.2f"%significance)

    forbidden_lines = get_forbidden_lines(grid_name)
    for line_ in forbidden_lines :
        line_.Draw()
        canvas.Update()



    #################################
    # save

    canvas.SaveAs("test.eps")



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

    ## let's first combine any subregions
    for reg in regions :
        if reg.isParent() :
            combine_subregion_significance(reg, signals)

    for s in signals :
        print s.significance_dict

    ## now we have the significance for each sub-region and the 
    ## significance for the combination of each sub-region

    ## now find the best significance for a given point
    ## > if the regions are orthogonal this will just
    ## > combine them. if not, it will perform the PWC 
    get_best_significance(regions, signals)

    ## OK now we can start plotting
    make_sensitivity_plot(signals, regions, signal_grid)

