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
r.TCanvas.__init__._creates = False
r.TPad.__init__._creates = False
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

def get_histogram(plot, sig, reg, variation="") :
    """
    Make the histogram for a given selection
    for the signal point 'sig' for a given
    variation

        variation  : weighting
        ----------- -----------
        right      : susy3BodyRightPol
        left       : susy3BodyLeftPol
        mass       : susy3BodyOnlyMass
    """

    final_weight = ""
    if variation == "nom" :
        final_weight = "eventweightNOPUPW"
    elif variation == "right" :
        final_weight = "eventweightNOPUPW * susy3BodyRightPol"
    elif variation == "left" :
        final_weight = "eventweightNOPUPW * susy3BodyLeftPol"
    elif variation == "mass" :
        final_weight = "eventweightNOPUPW * susy3BodyOnlyMass" 
    else :
        print "get_histogram    ERROR Unhandled variation \"" + variation + "\"! Exitting."
        sys.exit()

    cut = "(" + reg.tcut + ") * " + final_weight 
    print "cut: ", cut
    cut = r.TCut(cut)
    sel = r.TCut("1")
    h = pu.th1f("h_" + variation + "_" + sig.name, "", int(plot.nbins), plot.x_range_min, plot.x_range_max, plot.x_label, plot.y_label)
    h.SetMinimum(plot.y_range_min)
    h.SetMaximum(plot.y_range_max)
    h.GetXaxis().SetTitleOffset(-999)
    h.GetXaxis().SetLabelOffset(-999)
    h.Sumw2()
    cmd = "%s>>%s"%(plot.variable, h.GetName()) 
    sig.tree.Draw(cmd, cut * sel, "goff")

    return h

def get_color_from_name(hist) :

    colors = {}
    colors["nom"] = r.kBlack
    colors["right"] = 38
    colors["left"] = 46
    colors["mass"] = 30

    names = {}
    names["nom"] = "Nominal"
    names["right"] = "Polarized Right"
    names["left"] = "Polarized Left"
    names["mass"] = "Mass-only"

    for variation in colors.keys() :
        if variation in hist.GetName() :
            return colors[variation], names[variation]

def make_threebody_plots(plt, reg, sig) :

    # get the canvases
    rcan = plt.ratioCanvas
    rcan.canvas.cd()
    rcan.upper_pad.cd()

    if plt.isLog() : rcan.upper_pad.SetLogy(True)

    # draw the frame
    hax = r.TH1F("axes","", int(plt.nbins), plt.x_range_min, plt.x_range_max)
    hax.SetMinimum(plt.y_range_min)
    hax.SetMaximum(plt.y_range_max)
    hax.GetXaxis().SetTitle(plt.x_label)
    hax.GetXaxis().SetTitleFont(42)
    hax.GetXaxis().SetLabelFont(42)
    hax.GetXaxis().SetLabelSize(0.035)
    hax.GetXaxis().SetTitleSize(0.048*0.85)
    hax.GetXaxis().SetTitleOffset(-999)
    hax.GetXaxis().SetLabelOffset(-999)

    hax.GetYaxis().SetTitle(plt.y_label)
    hax.GetYaxis().SetTitleFont(42)
    hax.GetYaxis().SetLabelFont(42)
    hax.GetYaxis().SetTitleOffset(1.4)
    hax.GetYaxis().SetLabelOffset(0.013)
    hax.GetYaxis().SetLabelSize(1.2*0.035)
    hax.GetYaxis().SetTitleSize(0.055*0.85)
    hax.Draw("axis")
    rcan.upper_pad.Update()

    # legend
    leg = pu.default_legend(xl=0.6, yl=0.65, xh=0.97, yh=0.90)
    leg.SetHeader("%s"%sig.displayname)
    leg.SetNColumns(1)
    
    #############################################################
    # get histogram for nom, 3-body (Right, Left, Mass-only)
    ############################################################
    h_nom = get_histogram(plt, sig, reg, "nom")
    h_r = get_histogram(plt, sig, reg, "right")
    h_l = get_histogram(plt, sig, reg, "left")
    h_m = get_histogram(plt, sig, reg, "mass") 

    #filetest = r.TFile.Open("/data/uclhc/uci/user/dantrim/ntuples/n0222/may23/mc/Raw/CENTRAL_387947.root")
    #treetest = filetest.Get("superNt")
    #c = r.TCanvas("c", "", 768, 768)
    #c.cd()
    #htest = r.TH1F("h","", 32, 0, 250)
    #cut = "(" + reg.tcut + ") * " + "eventweightNOPUPW" 
    #cut = r.TCut(cut)
    #sel = r.TCut("1")
    #cmd = "%s>>%s"%("MDR", htest.GetName()) 
    #treetest.Draw(cmd, cut*sel)
    #c.SaveAs("testing.eps")
    


    ############
    # hergiw
    #hf = r.TFile.Open("/data/uclhc/uci/user/dantrim/ntuples/n0222/apr17/mc/Raw/CENTRAL_406010.root")
    hf = r.TFile.Open("/data/uclhc/uci/user/dantrim/ntuples/n0222/may23/mc/Raw/CENTRAL_406010.root")
    herwig_250_160_tree = hf.Get("superNt")
    
    print "blah ", reg.tcut
    cut = "(" + reg.tcut + ") * " + "eventweightNOPUPW" 
    cut = r.TCut(cut)
    sel = r.TCut("1")
    hh = pu.th1f("h_herwig_" + "_" + sig.name + "_herwig", "", int(plt.nbins), plt.x_range_min, plt.x_range_max, plt.x_label, plt.y_label)
    hh.SetMinimum(plt.y_range_min)
    hh.SetMaximum(plt.y_range_max)
    hh.GetXaxis().SetTitleOffset(-999)
    hh.GetXaxis().SetLabelOffset(-999)
    hh.SetLineColor(r.kBlack)
    hh.SetLineWidth(2)
    hh.SetLineStyle(2)
    hh.SetFillStyle(0)
    cmd = "%s>>%s"%(plt.variable, hh.GetName()) 
    herwig_250_160_tree.Draw(cmd, cut * sel, "goff")


    histos = [h_nom, h_r, h_l, h_m]

    # overflows
    for h in histos:
        pu.add_overflow_to_lastbin(h)

    # colors
    for h in histos :
        color, name = get_color_from_name(h)
        h.SetLineColor(color)
        h.SetLineWidth(2)
        h.SetFillStyle(0)
        leg.AddEntry(h, name, "l") 

    # draw
    histos.append(hh)
    is_first = True
    for h in histos :
        if is_first :
            is_first = False
            rcan.upper_pad.cd()
            
            h.Draw("hist e")
            rcan.upper_pad.Update()
        else :
            rcan.upper_pad.cd()
            h.Draw("hist e same")
            rcan.upper_pad.Update()

    #hwerwig
    hh.SetLineColor(r.kRed)
    hh.SetFillStyle(0)
    hh.Draw("hist same")
    leg.AddEntry(hh, "Herwig++", "l")

    rcan.upper_pad.SetGridx(True)
    rcan.upper_pad.SetGridy(True)

    # draw the legend
    leg.Draw()


    ################################################
    ## ratio
    ################################################
    rcan.lower_pad.cd()

    h_den = h_nom.Clone("h_den")
    # y-axis
    yax = h_den.GetYaxis()
    yax.SetRangeUser(0,2)
    yax.SetTitle("Variation/Nominal")
    yax.SetTitleSize(0.14 * 0.75)
    yax.SetLabelSize(0.13)
    yax.SetLabelOffset(0.98 * 0.013)
    yax.SetTitleOffset(0.48)
    yax.SetLabelFont(42)
    yax.SetTitleFont(42)
    yax.SetNdivisions(5)
    # x-axis
    xax = h_den.GetXaxis()
    xax.SetTitleSize(1.0 * 0.14)
    xax.SetLabelSize(0.13)
    xax.SetLabelOffset(1.15*0.02)
    xax.SetTitleOffset(1.1)#0.2*2)
    #xax.SetTitleOffset(0.1 * xax.GetTitleOffset())
    xax.SetLabelFont(42)
    xax.SetTitleFont(42) 

    h_den.SetTickLength(0.06)
    h_den.Draw("AXIS")
    h_den.SetTitle(plt.x_label)

    # unity line
    pu.draw_line(plt.x_range_min, 1.0, plt.x_range_max, 1.0, color=r.kRed, style=2, width=1)

    # right
    h_rl = h_r.Clone("h_rl")
    h_rl.Divide(h_den)
    h_rl.Draw("hist e same")
    rcan.lower_pad.Update()

    # left
    h_ll = h_l.Clone("h_ll")
    h_ll.Divide(h_den)
    h_ll.Draw("hist e same")
    rcan.lower_pad.Update()

    # mass
    h_ml = h_m.Clone("h_ml")
    h_ml.Divide(h_den)
    h_ml.Draw("hist e same")
    rcan.lower_pad.Update()


    rcan.canvas.SaveAs("test_%s.eps"%plt.variable)
    
        

    



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
