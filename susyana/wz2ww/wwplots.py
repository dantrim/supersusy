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

import supersusy.utils.plot_utils as pu
import supersusy.utils.utils as utils
import supersusy.utils.background as background
import supersusy.utils.region as region
import supersusy.utils.plot as plot


def get_xsec(name="") :
    xsec_map = {}
    xsec_map["WW"] = 14.02 * 0.91
    xsec_map["WZ"] = 4.46 * 1.0 #* 6.4#3.2

    return xsec_map[name]

def get_sumw(name="") :
    sumw_map = {}
    sumw_map["WW"] = 13351.5 #20k raw events
    sumw_map["WZ"] = 263363  #60k raw events
    #sumw_map["WZ"] = 86645.4

    return sumw_map[name]

def get_plotConfig(conf) :
    global indir
    conf_file = "./" + indir + "/" + conf + ".py"
    if os.path.isfile(conf_file) :
        print "Found the configuration file: %s"%conf_file
        return conf_file
    else :
        print "ERROR Input plot configuration ('%s') is not found in the directory.path provided ('%s'). Does it exist?"%(conf, conf_file)
        sys.exit()


def make_plotsRatio(plot, region, backgrounds) :

    print "make_plotsRatio    Plotting %s"%plot.name

    # get the canvases
    rcan = plot.ratioCanvas
    rcan.canvas.cd()
    rcan.upper_pad.cd()

    if plot.isLog() : rcan.upper_pad.SetLogy(True)
    rcan.upper_pad.Update()

    # set up the frame
    hax = r.TH1F("axes", "", int(plot.nbins), plot.x_range_min, plot.x_range_max)
    hax.SetMinimum(plot.y_range_min)
    hax.SetMaximum(plot.y_range_max)
    xax = hax.GetXaxis()
    xax.SetTitle(plot.x_label)
    xax.SetTitleFont(42)
    xax.SetLabelFont(42)
    xax.SetLabelSize(0.035)
    xax.SetTitleSize(0.048 * 0.85)
    xax.SetTitleOffset(-999)
    xax.SetLabelOffset(-999)

    yax = hax.GetYaxis()
    yax.SetTitle(plot.y_label)
    yax.SetTitleFont(42)
    yax.SetLabelFont(42)
    yax.SetTitleOffset(1.4)
    yax.SetLabelOffset(0.013)
    yax.SetLabelSize(1.2 * 0.035)
    yax.SetTitleSize(0.055 * 0.85)

    hax.Draw()
    rcan.upper_pad.Update()

    # legend
    leg = pu.default_legend(xl=0.65, yl=0.72, xh=0.93, yh=0.90)

    histos = [] 
    n_drawn = 0
    for b in backgrounds :
        hist_name = ""
        if "abs" in plot.variable :
            replace_var = plot.variable.replace("abs(", "")
            replace_var = replace_var.replace(")", "")
            hist_name = replace_var
        else : hist_name = plot.variable
        h = None
        h = pu.th1f("h_"+b.treename+"_"+b.name+"_"+hist_name, "", int(plot.nbins), plot.x_range_min, plot.x_range_max, plot.x_label, plot.y_label)
        h.SetMinimum(0.1)
        h.SetLineColor(b.color)
        h.GetXaxis().SetLabelOffset(-999)
        h.SetLineWidth(2)
        h.SetFillStyle(0)
        h.Sumw2()

        idx = ""
        if "WW" in b.name or "ww" in b.name :
            idx = "WW"
        elif "WZ" in b.name or "wz" in b.name :
            idx = "WZ"

        sumw = get_sumw(idx)
        xsec = get_xsec(idx)
        lumi = 3300.0 # 3.3/fb

        weight_str = "eventweight * %s * %s / %s"%(str(xsec), str(lumi), str(sumw))
        print "weight = %s"%weight_str

        cut = "(" + reg.tcut + ") * %s "%weight_str
        #cut = "(" + reg.tcut + ") * eventweight * " + str(b.scale_factor)
        cut = r.TCut(cut)
        sel = r.TCut("1")
        cmd = "%s>>%s"%(plot.variable, h.GetName())
        b.tree.Draw(cmd, cut * sel, "goff")

        # yield
        stat_err = r.Double(0.0)
        integral = h.IntegralAndError(0,-1,stat_err)
        print "%s: %.2f +/- %.2f"%(b.name, integral, stat_err)

        # add overflow
        pu.add_overflow_to_lastbin(h)
        leg.AddEntry(h, b.displayname, "l")
        histos.append(h)
        #rcan.upper_pad.Update()
        #rcan.canvas.Update()

    h_WW = None
    h_WZ = None
    for h in histos :
        if "WW" in h.GetName() or "ww" in h.GetName() :
            h_WW = h
            rcan.upper_pad.Update()
        elif "WZ" in h.GetName() or "wz" in h.GetName() :
            h_WZ = h
            rcan.upper_pad.Update()
        else :
            print "Expecting a  histogram with name that has 'WZ/wz' or 'WW/ww' in it"
            sys.exit()
    h_WW.Draw()
    h_WZ.Draw("same")
 
  h_WZ.Scale(1/h_WZ.Integral())
    h_WW.Scale(1/h_WW.Integral())

    leg.Draw()
    r.gPad.RedrawAxis()


    ##########################
    # Lower Pad
    ##########################
    rcan.lower_pad.cd()


#    h_ratio = h_WW.Clone("h_ratio")
    h_ratio = pu.th1f("h_ratio_"+plot.name, "", int(plot.nbins), plot.x_range_min, plot.x_range_max, "", "") 

    # y-axis
    axy = h_ratio.GetYaxis()
    axy.SetRangeUser(0,2)
    axy.SetTitle("WZ' / WW")
    axy.SetTitleSize(0.14)
    axy.SetLabelSize(0.13)
    axy.SetLabelOffset(0.98 * 0.013)
    axy.SetTitleOffset(0.45)
    axy.SetLabelFont(42)
    axy.SetTitleFont(42)
    axy.SetNdivisions(5)
    # x-axis
    axx = h_ratio.GetXaxis()
    axx.SetTitle(plot.x_label)
    axx.SetTitleSize(1.2 * 0.14)
    axx.SetLabelSize(0.13)
#    axx.SetLabelOffset(1.15 * 0.02)
    axx.SetTitleOffset(0.85 * axx.GetTitleOffset())
    axx.SetLabelFont(42)
    axx.SetTitleFont(42)

    h_ratio.SetTickLength(0.06)
    h_ratio.Draw("AXIS")
    rcan.lower_pad.Update()

    # draw lines
    pu.draw_line(plot.x_range_min, 1.0, plot.x_range_max, 1.0, color=r.kRed, style=2, width=1)
    pu.draw_line(plot.x_range_min, 0.5, plot.x_range_max, 0.5, style=3, width=1)
    pu.draw_line(plot.x_range_min, 1.5, plot.x_range_max, 1.5, style=3, width=1)
    
    h_WWr = h_WW.Clone("ww_rat")
    h_WZr = h_WZ.Clone("wz_rat")

    h_WZr.Divide(h_WWr)
    h_WZr.SetMarkerStyle(20)
    h_WZr.SetLineColor(r.kBlack)
    h_WZr.Draw("same")
    rcan.lower_pad.Update()

    outname = plot.name + ".eps"
    rcan.canvas.SaveAs(outname)
    out = indir + "/plots/" + outdir
    utils.mv_file_to_dir(outname, out, True)
    fullname = out + "/" + outname
    print "%s saved to : %s"%(outname, os.path.abspath(fullname))

    
        
    
    
    

    

def make_plots1D(plot, region, backgrounds) :
    if plot.ratioCanvas : make_plotsRatio(plot, region, backgrounds)
    else :
        print "make_plots1D ERROR    only ratio plots supported!"
        sys.exit() 

def make_plots(plots, regions, backgrounds) :
    for reg in regions :
        plots_with_region = []
        for p in plots :
            if p.region == reg.simplename : plots_with_region.append(p)
        if len(plots_with_region)==0 : continue
        
        for p in plots_with_region :
            if not p.is2D : make_plots1D(p, reg, backgrounds)
            elif p.is2D :
                print "make_plots ERROR 2D plotting not supported!"
                sys.exit()


if __name__=="__main__" :
    global indir, plotConfig, outdir, requestPlot, requestRegion


    parser = OptionParser()
    parser.add_option("-c", "--plotConfig", dest="plotConfig", default="")
    parser.add_option("-i", "--indir", dest="indir", default="")
    parser.add_option("-r", "--requestRegion", dest="requestRegion", default="")
    parser.add_option("-p", "--requestPlot", dest="requestPlot", default="")
    parser.add_option("-o", "--outdir", dest="outdir", default="./")
    (options, args) = parser.parse_args()
    indir = options.indir
    plotConfig = options.plotConfig
    requestRegion = options.requestRegion
    requestPlot = options.requestPlot
    outdir = options.outdir

    print " ++ --------------------------------- ++ "
    print "      wz-to-ww                           "
    print ""
    print "     config directory : %s               "%indir
    print "     plot config      : %s               "%plotConfig
    print "     requested plot   : %s               "%requestPlot
    print "     requested region : %s               "%requestRegion
    print "     output directory : %s               "%outdir
    print ""
    print " ++ --------------------------------- ++ "

    conf_file = get_plotConfig(plotConfig)

    plots = []
    backgrounds = []
    regions = []
    execfile(conf_file)

    if requestRegion != "" :
        requested_plots = []
        for p in plots :
            if p.region == requestRegion : requested_plots.append(p)
        make_plots(requested_plots, regions, backgrounds)
    elif requestPlot != "" :
        requested_plots = []
        for p in plots :
            if p.name == requestPlot : requested_plots.append(p)
        make_plots(requested_plots, regions, backgrounds)
    else :
        make_plots(plots, regions, backgrounds)


    
