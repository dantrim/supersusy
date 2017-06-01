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
r.TH2F.__init__._creates = False
r.TCanvas.__init__._creates = False
r.TGraph.__init__._creates = False
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
    cut_raw = "(" + tcut + ")"
    cut = r.TCut(cut)
    cut_raw = r.TCut(cut_raw)
    sel = r.TCut("1")
    h = pu.th1f("h_" + bkg_.name + "_yield_" + region_name, "", 4, 0, 4, "", "")
    h_raw = pu.th1f("h_" + bkg_.name + "_rawyield_" + region_name, "", 4, 0, 4, "", "")
    cmd = "%s>>%s"%("isMC", h.GetName())
    cmd_raw = "%s>>%s"%("isMC", h_raw.GetName())
    bkg_.tree.Draw(cmd, cut * sel, "goff") 
    bkg_.tree.Draw(cmd_raw, cut_raw * sel, "goff")

    err = r.Double(0.0)
    integral = h.IntegralAndError(0, -1, err)

    err_raw = r.Double(0.0)
    int_raw = h_raw.IntegralAndError(0,-1, err_raw)

    #print "BKG RAW YIELD %s (%s)> %.2f +/- %.2f (%.2f)"%(region_name, bkg_.name, int_raw, err_raw, sqrt(int_raw))
    print "BKG YIELD %s (%s)> %.2f +/- %.2f (%.2f)"%(region_name, bkg_.name, integral, err, sqrt(integral))

    h.Delete()
    return integral, err

#def get_signal_yield(sig_, tcut, region_name, extra_weight = "") :
#    extra_ = ""
#    cut = ""
#    cut_raw = ""
#    if not extra_weight == "" :
#        cut = "(" + tcut + ") * eventweight * " + str(sig_.scale_factor) + " * " + str(extra_weight)
#        cut_raw = "(" + tcut + ")"# * " + str(sig_.scale_factor) + " * " + str(extra_weight)
#    else :
#        cut = "(" + tcut + ") * eventweight * " + str(sig_.scale_factor) 
#        cut_raw = "(" + tcut + ")"# * " + str(sig_.scale_factor) 
#    cut = r.TCut(cut) 
#    cut_raw = r.TCut(cut_raw)
#    sel = r.TCut("1")
#    hname = "%.0f_%.0f"%(sig_.mx, sig_.my)
#    h = pu.th1f("h_" + hname + "_yield_" + region_name, "", 4, 0, 4, "", "")
#    h_raw = pu.th1f("h_" + hname + "_raw_" + region_name, "", 4,0,4,"","")
#    cmd = "%s>>%s"%("isMC", h.GetName())
#    cmd_raw = "%s>>%s"%("isMC", h_raw.GetName())
#    sig_.tree.Draw(cmd, cut * sel, "goff")
#    sig_.tree.Draw(cmd_raw, cut_raw * sel, "goff")
#
#    err = r.Double(0.0)
#    integral = h.IntegralAndError(0, -1, err)
#
#    err_raw = r.Double(0.0)
#    int_raw = h_raw.IntegralAndError(0,-1,err_raw)
#    
#    #print " SIGNAL Yield (%s)> %s : %.2f +/- %.2f (%.2f)"%(region_name, sig_.getName(), integral, err, sqrt(integral))
#    print " SIGNAL RAW Yield (%s)> %s : %.2f +/- %.2f (%.2f)"%(region_name, sig_.getName(), int_raw, err_raw, sqrt(int_raw))
#    #integral = integral - err
#    h.Delete()
#    return integral

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
    for sig in sigs_ :

        significance = 0

        integral = get_signal_yield(sig, reg_.getTcut(), reg_.name, "1")
        #integral = get_signal_yield(sig, reg_.getTcut(), reg_.name, "susy3BodyRightPol")
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

        s.best_region = best_region
        print "best region for %s : %s (%.2f)"%(s.getName(), best_region, significances[best_region])
        s.best_significance = significances[best_region]


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
    frame = r.TH2F("frame", "", n_bins, 100, 450, 93, 0, 425)

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

def get_contour(sigs_, sigma_ = 2, frame_hist = None) :
    '''
    Make a contour for the provided sigma value
    '''

    if not frame_hist :
        print "znplotter::get_contour    ERROR Provided frame histogram is empty!"
        sys.exit()

    pval_ = -1
    if sigma_ == 2 :
        # draw a 2 sigma contour (e.g. exclusion)
        pval_ = 0.05 
    elif sigma_ == 3 :
        # draw a 3 sigma contour
        pval_ = 0.003
    elif sigma_ == 5 :
        # draw a 5 sigma contour
        pval_ = 3e-7
    else :
        print "znplotter::get_contour    ERROR Requested sigma value (%.2f) is not handled!"%(sigma_)
        sys.exit()

    print "znplotter::get_contour    INFO Creating contour for %.2f-sigma"%sigma_

    gr = r.TGraph2D()
    gr.SetName("g_%dsigma"%sigma_)
    gr.Clear()
    #print "SIGS SIZE: ",len(sigs_)
    for s in sigs_ :
        significance = s.best_significance
        if significance < 0.0 : significance = 0.0
        x = float(s.mx)
        y = float(s.my)
        #print "setting contour point graph: (%.2f, %.2f, %.2f)"%(x, y, significance)
        gr.SetPoint(gr.GetN(), x, y, float(significance))

    #print "GR GET N: ", gr.GetN()

    nbinsX = frame_hist.GetXaxis().GetNbins()
    nbinsY = frame_hist.GetYaxis().GetNbins()
    x_min = frame_hist.GetXaxis().GetXmin()
    x_max = frame_hist.GetXaxis().GetXmax()
    y_min = frame_hist.GetYaxis().GetXmin()
    y_max = frame_hist.GetYaxis().GetXmax()

    #print "nx: %d  ny: %d  xmin: %d  xmax: %d  ymin: %d  ymax: %d"%(nbinsX, nbinsY, x_min, x_max, y_min, y_max)

    hist = None
    hist = r.TH2F("tmp_hist_" + gr.GetName(), "", nbinsX, x_min, x_max, nbinsY, y_min, y_max)
    hist.SetDirectory(0)
    gr.SetHistogram(hist)
    level = r.TMath.NormQuantile(1.0-pval_)
    if gr.GetZmax() < level : return
    h = gr.GetHistogram().Clone("tmp_hist_" + gr.GetName())
    h.SetDirectory(0)
    nPointsExcluded = len([1 for i in range(gr.GetN()) if gr.GetZ()[i] > level])
    if nPointsExcluded < 3 :
        print "znplotter::get_contour    WARNING Less than three points satisfy the contour for %.2f-sigma!"%sigma_
        print "znplotter::get_contour    WARNING  > Will not draw contour for this level."
        return None

    c_ = r.TCanvas("tmp_can_" + gr.GetName(), "")
    c_.cd()
    #h.Smooth()
    h.SetContour(1)
    h.SetContourLevel(0, level)
    h.Draw("CONT LIST")
    r.gPad.Update()
    c_.Draw()
    contours = r.gROOT.GetListOfSpecials().FindObject("contours")
    if contours.GetEntries() :
        cont = contours.At(0).First()
        contours.Delete()
        h.Delete()
        return cont

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
    gr.SetMaximum(5.0)

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
    tex.SetTextSize(1.2*0.3*tex.GetTextSize())
    for s in sigs_ :
        significance = s.best_significance
        if significance < 0.0 : significance = 0.0
        tex.DrawLatex(float(s.mx), float(s.my), "%.2f"%significance)

    forbidden_lines = get_forbidden_lines(grid_name)
    for line_ in forbidden_lines :
        line_.Draw()
        canvas.Update()

    ###### get the contour
    g_exc = None
    g_3sig = None
    g_5sig = None

    g_exc =  get_contour(sigs_, sigma_ = 2, frame_hist = frame)
    g_3sig = get_contour(sigs_, sigma_ = 3, frame_hist = frame)
    g_5sig = get_contour(sigs_, sigma_ = 5, frame_hist = frame)

    canvas.cd()
    if g_exc :
        g_exc.SetName("2-#sigma")
        g_exc.SetLineWidth(2)
        g_exc.SetLineStyle(2)
        g_exc.SetLineColor(r.kRed)
        g_exc.Draw("l same")
    else :
        g_exc = r.TGraph()
        g_exc.SetName("2-#sigma")
        g_exc.SetLineWidth(2)
        g_exc.SetLineStyle(2)
        g_exc.SetLineColor(r.kRed)
    canvas.Update()

    if g_3sig :
        g_3sig.SetName("3-#sigma")
        g_3sig.SetLineWidth(2)
        g_3sig.SetLineStyle(1)
        g_3sig.SetLineColor(r.kBlue)
        g_3sig.Draw("l same")
    else :
        g_3sig = r.TGraph()
        g_3sig.SetName("3-#sigma")
        g_3sig.SetLineWidth(2)
        g_3sig.SetLineStyle(1)
        g_3sig.SetLineColor(r.kBlue)
    canvas.Update()

    if g_5sig :
        g_5sig.SetName("5-#sigma")
        g_5sig.SetLineWidth(2)
        g_5sig.SetLineStyle(1)
        g_5sig.SetLineColor(r.kBlack)
        g_5sig.Draw("l same")
    else :
        g_5sig = r.TGraph()
        g_5sig.SetName("5-#sigma")
        g_5sig.SetLineWidth(2)
        g_5sig.SetLineStyle(1)
        g_5sig.SetLineColor(r.kBlack)
    canvas.Update()


    ################################
    # legend
    leg = pu.default_legend(xl=0.19,yl=0.65,xh=0.45,yh=0.74)
    if g_exc :
        leg.AddEntry(g_exc, "2#sigma (exclusion)", "l")
    if g_3sig :
        leg.AddEntry(g_3sig, "3#sigma", "l")
    if g_5sig :
        leg.AddEntry(g_5sig, "5#sigma", "l")
    leg.Draw()
    canvas.Update()

    ##################################
    # atlas
    pu.draw_text(text="#bf{#it{ATLAS}} Internal",x=0.2, y = 0.87, size = 0.05)
    pu.draw_text(text="13 TeV, 10/fb",x=0.2,y=0.82,size=0.04)
    print 45*"*"
    print "Hardcoding process formula onto canvas"
    print 45*"*"
    formula = "#tilde{t} #rightarrow bW#tilde{#chi}_{0}"
    pu.draw_text(text=formula,x=0.21,y=0.77,size=0.03)
    canvas.Update()

    #################################
    # z-axis
    z_title = "Significance"
    pu.draw_text(text=z_title,x=0.98,y=0.66,size=0.035, angle=90.0)

    #################################
    # save

    canvas.SaveAs("test.eps")



##################### CONTAM
def get_yield(reg_, bkgs_) :
    print "Getting MC yield for %s"%reg_.name

    total_yield = 0.0

    for bkg_ in bkgs_ :
        cut = "(" + reg_.tcut + ") * eventweight * " + str(bkg_.scale_factor)
        cut = r.TCut(cut)
        sel = r.TCut("1")
        h = pu.th1f("h_" + reg_.name + "_" + bkg_.name + "_yieldH", "", 4, 0, 4, "","")
        cmd = "%s>>%s"%("isMC", h.GetName())
        bkg_.tree.Draw(cmd, cut * sel, "goff")
        err = r.Double(0.0)
        total_yield += h.IntegralAndError(0,-1,err)
        h.Delete()
    return total_yield

def get_mc_yields(regions_, bkgs_) :
    mc_yield_dict = {}
    for reg_ in regions_ :
        mc_yield_dict[reg_.name] = get_yield(reg_, bkgs_)
    return mc_yield_dict


def get_signal_yield(reg_, sig_) :
    cut = "(" + reg_.tcut + ") * eventweight * " + str(sig_.scale_factor)
    cut = r.TCut(cut)
    sel = r.TCut("1")
    h = pu.th1f("h_" + reg_.name + "_%d_%d_yieldH"%(sig_.mx,sig_.my), "", 4, 0, 4, "","")
    cmd = "%s>>%s"%("isMC", h.GetName())
    sig_.tree.Draw(cmd, cut * sel, "goff")
    err = r.Double(0.0)
    sig_.region_yield[reg_.name] = h.IntegralAndError(0,-1,err)
    print " >> %.2f"%h.IntegralAndError(0,-1,err)
    h.Delete()

def get_signal_yields(regions_, signals_) :
    for sig_ in signals_ :
        sig_.region_yield = {}
        
    for reg_ in regions_ :
        print "Getting signal yields for region: %s"%reg_.name
        for sig_ in signals_ :
            print " > (%.1f,%.1f)"%(sig_.mx, sig_.my)
            get_signal_yield(reg_, sig_)


def make_contamination_plot(r_, mc_yield_dict, sigs_, grid_name) :
    set_palette()

    canvas = r.TCanvas("c_contamination", "", 768, 768)
    canvas.cd()

    frame = make_frame(grid_name)
    frame.Draw("axis")
    frame.GetXaxis().SetTitle("m_{#tilde{t}} [GeV]")
    frame.GetYaxis().SetTitle("m_{#tilde{#chi_{0}}} [GeV]")
    canvas.Update()

    gr = r.TGraph2D(1)
    gr.Clear()
    gr.SetMarkerStyle(r.kFullSquare)
    gr.SetMarkerSize(2*gr.GetMarkerSize())
    gr.SetMaximum(35)

    mc_yield = float(mc_yield_dict[r_.name])

    max_contam = -1
    for s in sigs_ :
        s_yield = float(s.region_yield[r_.name])
        contamination_ = s_yield / mc_yield
        x = s.mx
        y = s.my
        #make percentage
        contamination_ *= 100.
        if contamination_ > max_contam :
            max_contam = contamination_
        gr.SetPoint(gr.GetN(), float(x), float(y), contamination_)

    if gr.GetN() :
        gr.Draw("colz same")
    canvas.Update()

    gr.SetMaximum(max_contam*1.15)
    canvas.Update()

    tex = r.TLatex(0.0, 0.0, '')
    tex.SetTextFont(42)
    tex.SetTextSize(1.2*0.3*tex.GetTextSize())
    for s in sigs_ :
        contamination_ = float(s.region_yield[r_.name]) / mc_yield
        # make percentage
        contamination_ *= 100.
        #if float(x) > 435. : continue
        #if float(y) > 350. : continue
        x = s.mx
        y = s.my
        if float(x) > 435 : x = -200
        tex.DrawLatex(float(x), float(y), "%.1f"%contamination_)

    forbidden_lines = get_forbidden_lines(grid_name)
    for line_ in forbidden_lines :
        line_.Draw()
        canvas.Update()

    ############################################
    ## atlas
    pu.draw_text(text="#bf{#it{ATLAS}} Internal",x=0.2, y = 0.87, size = 0.05)  
    pu.draw_text(text="13 TeV, Region: #bf{%s}"%r_.displayname,x=0.2,y=0.82,size=0.04)
    formula = "#tilde{t} #rightarrow bW#tilde{#chi}_{0}"
    pu.draw_text(text=formula,x=0.21,y=0.77,size=0.03)
    canvas.Update()

    ##########################################
    ## z-axis
    z_title = "Signal Contamination [%]"
    pu.draw_text(text=z_title,x=0.98,y=0.50,size=0.035, angle=90.0) 


    #######################################
    ## save
    outname = "sigcontam_%s.eps"%r_.name
    canvas.SaveAs(outname)

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
    print "     contamplotter "
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
    print "contamplotter    Found configuration file: %s"%config

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
        print "contamplotter    ERROR signal_file_rawdir is empty!"
        sys.exit()
    if signal_grid == "" :
        print "contamplotter    ERROR signal_grid is empty!"
        sys.exit()
    if not os.path.isdir(signal_file_rawdir) :
        print "contamplotter    ERROR signal_file_rawdir ('%s') is not found!"%signal_file_rawdir
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

    ########################################
    # get the total MC yield in all regions
    # returns: { reg.name : total MC yield }
    mc_yield_dict = get_mc_yields(regions, backgrounds)

    ########################################
    # get the yields in each region for each
    # signal point
    # adds to each signal point object a dict:
    #  sig.region_yield[reg.name] = yield
    get_signal_yields(regions, signals)

    #######################################
    # for each region, make a contamination
    # plot
    for r_ in regions :
        make_contamination_plot(r_, mc_yield_dict, signals, signal_grid)


    

#    #####################################
#    ## get the significance for each region
#    for reg in regions :
#        if reg.isParent() :
#            for ch_reg in reg.orthogonal_subregions :
#                get_significance(backgrounds, signals, ch_reg, significance_metric, bkg_uncertainty)
#        else :
#            get_significance(backgrounds, signals, reg, significance_metric, bkg_uncertainty)
#
#    ## at this point we have the significance evaluated at each
#    ## point of the grid --> just need to start plotting now
#
#    ## let's first combine any subregions
#    for reg in regions :
#        if reg.isParent() :
#            combine_subregion_significance(reg, signals)
#
#    for s in signals :
#        print s.significance_dict
#
#    ## now we have the significance for each sub-region and the 
#    ## significance for the combination of each sub-region
#
#    ## now find the best significance for a given point
#    ## > if the regions are orthogonal this will just
#    ## > combine them. if not, it will perform the PWC 
#    get_best_significance(regions, signals)
#
#    ## OK now we can start plotting
#    make_sensitivity_plot(signals, regions, signal_grid)
#
