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

r.TH1F.__init__._creates = False
r.TGraph2D.__init__._creates = False
r.TLatex.__init__._creates = False
r.THStack.__init__._creates = False

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

################################################################################### Zn-Ratio
### ZN-RATIO

##########################
### Get the Zn for the section
def get_zn_for_selection(h_sig, h_sm) :
    '''
    Provide the histogram for the signal assumption and the
    total expected background yield and calculate the
    Zn value for the applied selection. Calculate The Zn
    for the inclusive yield with a 30% systematic error
    assumption on top of the statistical uncertainty
    '''
    nSig = h_sig.Integral(0,-1)
    stat_err = r.Double(0.0)
    nBkg = h_sm.IntegralAndError(0, -1, stat_err)

    zn = r.Double(0.0)
    if nBkg > 0 and nSig > 0 :
        total_error = sqrt( (stat_err/nBkg)**2 + (0.30)**2)
        zn = r.RooStats.NumberCountingUtils.BinomialExpZ(nSig, nBkg, total_error)
    if zn < 0 : zn = 0.001

    return zn


##########################
### Zn per bin, up and down
def get_zn_per_bin(h_sig, h_sm) :
    '''
    Loop over the bins of the histogram, getting the totol signal
    yield up to that bin (nSig) and the expected background up to that bin (nBkg)
    and calculate the Zn for the inclusive yield with a 30% systematic error
    assumption on top of the statistical uncertainty
    '''
    zn_low_to_high = []
    zn_high_to_low = []

    zn_include_right = []
    zn_include_left = []

    for bin in range(h_sm.GetNbinsX()+1) :

        # integral low -> high
        nBkg, nSig = r.Double(0.0), r.Double(0.0)
        stat_err = r.Double(0.0)

        # take counts from the left side of the cut value at bin (i.e. Zn for upper-cut)
        nBkg = h_sm.IntegralAndError(0, bin, stat_err)
        nSig = h_sig.Integral(0, bin)

        zn_up = r.Double(0.0)
        if nBkg > 0 and nSig > 0 :
            total_err = sqrt( (stat_err/nBkg)**2 + (0.30)**2)
            zn_up = r.RooStats.NumberCountingUtils.BinomialExpZ(nSig, nBkg, total_err)
            if zn_up < 0 : zn_up = 0.001
            #zn_up = 1.5
        zn_include_left.append(zn_up)
        
        # integral high -> low
        nBkg, nSig = r.Double(0.0), r.Double(0.0)
        stat_err = r.Double(0.0)

        # take counts from the right side of the cut value at bin (i.e. Zn for lower-cut)
        nBkg = h_sm.IntegralAndError(bin,-1, stat_err)
        nSig = h_sig.Integral(bin,-1)

        zn_down = r.Double(0.0)
        if nBkg > 0 and nSig > 0 :
            total_err = sqrt( (stat_err/nBkg)**2 + (0.30)**2)
            zn_down = r.RooStats.NumberCountingUtils.BinomialExpZ(nSig, nBkg, total_err)
            if zn_down < 0 : zn_down = 0.001
            #zn_down = 0.8
        zn_include_right.append(zn_down)

    return zn_include_right, zn_include_left
        
            
##########################
### set the labels, etc.. for the ratio pads
def set_ratio_style(histo, where="mid", xlabel="") :
   
    if where=="mid" : 
        # x-axis
        histo.GetXaxis().SetTitleOffset(-999)
        histo.GetXaxis().SetLabelOffset(-999)

        # y-axis
        histo.GetYaxis().SetTitle("Z_{n} #downarrow")
        histo.GetYaxis().SetTitleOffset(0.3 * histo.GetYaxis().GetTitleOffset())
        histo.GetYaxis().SetTitleSize(4.0 * histo.GetYaxis().GetTitleSize())
        histo.GetYaxis().SetTitleFont(42)
        histo.GetYaxis().SetLabelFont(42)
        histo.GetYaxis().SetLabelSize(2.0 * histo.GetYaxis().GetLabelSize())
        histo.GetYaxis().SetNdivisions(5)

    if where=="low" :
        # x-axis
        histo.GetXaxis().SetTitle(xlabel)
        histo.GetXaxis().SetTitleSize(2.75 * histo.GetXaxis().GetTitleSize())
        histo.GetXaxis().SetTitleFont(42)
        histo.GetXaxis().SetTitleOffset(1.65 * histo.GetXaxis().GetTitleOffset())
        histo.GetXaxis().SetLabelFont(42)
        histo.GetXaxis().SetLabelSize(2.5 * histo.GetXaxis().GetLabelSize())
        histo.GetXaxis().SetLabelOffset(8 * histo.GetXaxis().GetLabelOffset())

        # y-axis
        histo.GetYaxis().SetTitle("Z_{n} #uparrow")
        histo.GetYaxis().SetTitleSize(2.2 * histo.GetYaxis().GetTitleSize())
        histo.GetYaxis().SetTitleOffset(0.355 * histo.GetYaxis().GetTitleOffset())
        histo.GetYaxis().SetTitleFont(42)
        histo.GetYaxis().SetLabelFont(42)
        histo.GetYaxis().SetLabelSize(0.035)
        histo.GetYaxis().SetNdivisions(5)


##########################
### Zn ratio plots
def make_znRatioPlots(backgrounds, signals, region, plot) :
    print "make_znRatioPlots    Plottings %s"%plot.name

    # get canvases
    ratiocan = plot.getCanvas()
    ratiocan.canvas.cd()

    # go to the upper-pad
    ratiocan.upper_pad.cd()
    ratiocan.upper_pad.Draw()
    ratiocan.middle_pad.cd()
    ratiocan.middle_pad.Draw()
    ratiocan.lower_pad.cd()
    ratiocan.lower_pad.Draw()

    ratiocan.canvas.cd()
    ratiocan.upper_pad.cd()

    if plot.isLog() : ratiocan.upper_pad.SetLogy(True)
    ratiocan.upper_pad.Update()

    # stack for MC backgrounds

    ratiocan.upper_pad.cd()
    hax = r.TH1F("axes", "", int(plot.nbins), plot.x_range_min, plot.x_range_max)
    hax.SetMinimum(plot.y_range_min)
    hax.SetMaximum(plot.y_range_max)
    hax.GetXaxis().SetTitle(plot.x_label)
    hax.GetXaxis().SetTitleFont(42)
    hax.GetXaxis().SetLabelFont(42)
    hax.GetXaxis().SetLabelSize(0.035)
    hax.GetXaxis().SetTitleSize(0.048 * 0.85)
    hax.GetXaxis().SetTitleOffset(-999)
    hax.GetXaxis().SetLabelOffset(-999)

    hax.GetYaxis().SetTitle(plot.y_label)
    hax.GetYaxis().SetTitleFont(42)
    hax.GetYaxis().SetLabelFont(42)
    hax.GetYaxis().SetTitleOffset(1.4)
    hax.GetYaxis().SetLabelOffset(0.013)
    hax.GetYaxis().SetLabelSize(1.2 * 0.035)
    hax.GetYaxis().SetTitleSize(0.055 * 0.85)
    hax.Draw()
    ratiocan.upper_pad.Update()
    
    stack = r.THStack("stack_"+plot.name, "")

    # legend
    leg = pu.default_legend(xl=0.65, yl=0.72, xh=0.93, yh=0.90)
    leg.SetNColumns(2)

    ### loop through the background MC and add to stack
    histos = []
    hist_dict = {} # associate the background with its histogram name

    hist_name = ""
    if "abs" in plot.variable :
        replace_var = plot.variable.replace("abs(","")
        replace_var = replace_var.replace(")","")
        hist_name = replace_var
    else : hist_name = plot.variable

    for b in backgrounds :
        h = pu.th1f("h_"+b.treename+"_"+hist_name, "", int(plot.nbins), plot.x_range_min, plot.x_range_max, plot.x_label, plot.y_label)
        h.SetLineColor(r.kBlack)
        h.SetFillColor(b.color)
        h.SetFillStyle(1001)
        h.Sumw2

        # cut and make the sample weighted, applying the scale_factor
        cut = "(" + reg.tcut + ") * eventweight * " + str(b.scale_factor)
        cut = r.TCut(cut)
        sel = r.TCut("1")
        cmd = "%s>>%s"%(plot.variable, h.GetName())
        b.tree.Draw(cmd, cut * sel, "goff")
        
        # print the yield +/- stat error
        stat_error = r.Double(0.0)
        integral = h.IntegralAndError(0, -1, stat_error)
        print "%s: %.2f +/- %.2f"%(b.name, integral, stat_error)

        # add overflow
        pu.add_overflow_to_lastbin(h)

        # add to group
        histos.append(h)
        hist_dict[h.GetName()] = b.displayname
     #   ratiocan.upper_pad.Update()

    # order the histograms and add to legend
    histos = sorted(histos, key = lambda h: h.Integral(), reverse = False)
    for his in histos :
        stack.Add(his)
    
    histos_leg = sorted(histos, key = lambda h: h.Integral(), reverse = True)
    for hl in histos_leg :
        leg.AddEntry(hl, hist_dict[hl.GetName()], "fl")
    ### total SM histo
    totalSM = stack.GetStack().Last().Clone("totalSM")

    ### container for zn pads
    zn_values = {}

    ### now plot the signal points

    sig_histos = []
    for s in signals :

        zn_values[s.name] = {} # { up : [], down : [] }

        hs = pu.th1f("h_"+s.treename+"_"+hist_name, "", int(plot.nbins), plot.x_range_min, plot.x_range_max, plot.x_label, plot.y_label)
        hs.SetLineColor(s.color)
        hs.SetLineStyle(2)
        hs.SetLineWidth(2) 
        hs.SetFillStyle(0)
        hs.Sumw2

        # cut and make sample weighted, applying the scale_factor
        cut = "(" + reg.tcut + ") * eventweight *" + str(s.scale_factor)
        cut = r.TCut(cut)
        sel = r.TCut("1")
        cmd = "%s>>%s"%(plot.variable, hs.GetName())
        s.tree.Draw(cmd, cut * sel, "goff")

        # print the yield +/- stat error
        stat_error = r.Double(0.0)
        integral = hs.IntegralAndError(0, -1, stat_error)
        print "%s: %.2f +/- %.2f"%(s.name, integral, stat_error)

        # add overflow
        pu.add_overflow_to_lastbin(hs)

        # add to legend
        leg.AddEntry(hs, s.displayname, "l")

        hs.SetMaximum(plot.y_range_max)
        hs.SetMinimum(plot.y_range_min)

        sig_histos.append(hs)
      #  ratiocan.upper_pad.Update()

        # get the zn-per-bin values
        # "up" : Zn values for lower-cuts (i.e. SR includes everything to the right of the cut)
        # "down" : Zn values for upper-cuts (i.e. SR includes everything to the left of the cut)
        zn_values[s.name]['up'], zn_values[s.name]['down'] = get_zn_per_bin(hs, totalSM)

        # get the total zn for this selection
        # and attach the the signal point
        zn = get_zn_for_selection(hs, totalSM)
        s.zn_val = zn

    print " ++ ----------------------------- ++ "
    print "     Z_n for selection %s            "%reg.displayname
    print ""
    for sigpoint in signals :
        print "   Zn %s : %.2f"%(sigpoint.displayname, sigpoint.zn_val)
    print " ++ ----------------------------- ++ "


    ### draw MC backgrounds
    ratiocan.upper_pad.Update()
    
    # now draw the stack without the axis
    stack.Draw("HIST same")

    ### draw signals
    for h_sig in sig_histos :
        h_sig.Draw("same")
    ratiocan.canvas.Update()

    leg.Draw()
    ratiocan.canvas.Update()
    r.gPad.RedrawAxis()

    #########################
    ## now draw zn

    ### up
    zn_up_histos = []
    zn_down_histos = []
    for sig in signals :
        updown = ['up', 'down']
        for dir in updown :
            zns = zn_values[sig.name][dir]
            hz = pu.th1f("h_zn_"+dir+"_" + sig.name, "", int(plot.nbins), plot.x_range_min, plot.x_range_max, "","")
            hz.SetMarkerStyle(20)
            hz.SetMarkerColor(sig.color)
            hz.SetMarkerSize(0.3 * hz.GetMarkerSize())
            hz.SetMaximum(2.5)
            hz.SetMinimum(0.0)
            for ibin, zn in enumerate(zns) :
                hz.SetBinContent(ibin, r.Double(zn))
            if 'up' in dir : zn_up_histos.append(hz)
            elif 'down' in dir : zn_down_histos.append(hz)

    ratiocan.middle_pad.cd()
    is_first = True
    for hzn in zn_up_histos :
        if is_first : 
            hzn.Draw("p")
            set_ratio_style(hzn, "mid", "")
            is_first = False
        else :
            hzn.Draw("same p")
    ratiocan.middle_pad.Update()

    ratiocan.lower_pad.cd()
    is_first = True
    for hzn in zn_down_histos :
        if is_first : 
            hzn.Draw("p")
            is_first = False
            set_ratio_style(hzn, "low", plot.x_label)
        else :
            hzn.Draw("same p")
    ratiocan.lower_pad.Update()

    #### save
    outname = plot.name + ".eps"
    ratiocan.canvas.SaveAs(outname)
    out = indir + "/plots/" + outdir
    utils.mv_file_to_dir(outname, out, True)
    fullname = out + "/" + outname
    print "%s saved to : %s"%(outname, os.path.abspath(fullname))



    
################################################################################### Main
### MAIN
if __name__=="__main__" :

    # some dummy stuff to have the RooStats banner print at beginning of output
    # instead of middle of our own
    dummy = r.TH1F("dummy", "dummy", 1, 0, 1)
    dummy.Fill(0,10)
    dummy2 = r.TH1F("dummy2", "dumm2", 1, 0 , 1)
    dummy2.Fill(0,10)
    get_zn_for_selection(dummy, dummy2)

    # make these blogal
    global optConfig, indir, requestRegion, outdir, dbg

    parser = OptionParser()
    parser.add_option("-c", "--optConfig", dest="optConfig", default="")
    parser.add_option("-m", "--method", dest="method", default="zn_ratio")
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

    acceptable_methods = ["zn", "zn_ratio"]
    if method not in acceptable_methods :
        print 'optimizer ERROR    You have requested an optimization method that is not yet supported ("%s").'%method
        print 'optimizer ERROR    Currently we only support Zn (BinomialExp) - based optimization routines'
        print 'optimizer ERROR    selected with the "-m" ("--method") option "zn" or "zn_ratio".'
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

    #########################################
    ## if doing zn-ratio plots
    plots = []

    execfile(config)

    #### parse out the signals
    signals = []
    backgrounds_new = []
    for background_sample in backgrounds :
        if background_sample.isSignal() : 
            signals.append(background_sample)
            print "optimizer    Found signal sample", background_sample.Print()
        else : backgrounds_new.append(background_sample)
    if len(signals) == 0 :
        print "optmizer ERROR    No signal samples configured."
        print "optmizer ERROR    >>> Exiting."
        sys.exit()

    backgrounds = backgrounds_new

    ### go over methods
    if method == "zn_ratio" :
        if len(plots) == 0 :
            print "optimizer ERROR    Attempting to make the zn_ratio plots without having configured any plots!"
            print "optimizer ERROR    >>> Exiting."
            sys.exit()
        region_names = [x.name for x in regions]
        if requestRegion not in region_names :
            print "optmizer ERROR    The requested region ('%s') is not in the configured regions"%requestRegion
            print "optmizer ERROR    To make the zn-ratio plots a requested region is required."
            print "optmizer ERROR    >>> Exiting."
            sys.exit()
        for configured_plot in plots :
            if not configured_plot.doubleRatioCanvas :
                print "optmizer ERROR    Attempting to make the zn_ratio plot %s without the required 'double ratio canvas'"%configured_plot.name
                print "optmizer ERROR    >>> Exiting."
                sys.exit()
            for possible_regions in regions :
                if configured_plot.region != requestRegion : continue 
            make_znRatioPlots(backgrounds, signals, requestRegion, configured_plot) 