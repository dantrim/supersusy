#!/usr/bin/env python

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(1)
r.gStyle.SetOptStat(0)

import sys
import os

from optparse import OptionParser

from math import sqrt

filedir = "/data/uclhc/uci/user/dantrim/ntuples/n0232/c_apr27/mc/Raw/"
signal_filedir = "/data/uclhc/uci/user/dantrim/ntuples/n0232/d_may15/mc/Raw/"
ttbar_file = "%sCENTRAL_410009.root"%filedir
x1000_file = "%sCENTRAL_343777.root"%signal_filedir
x800_file = "%sCENTRAL_343775.root"%signal_filedir
x600_file = "%sCENTRAL_343772.root"%signal_filedir
x400_file = "%sCENTRAL_343769.root"%signal_filedir
hh_file = "%sCENTRAL_342053.root"%signal_filedir

list_made = False

class Sample() :
    def __init__(self, filename, name, displayname, color, is_signal, scale_factor) :
        self.filename = filename
        self.name = name
        self.displayname = displayname
        self.color = color
        self.signal = is_signal

        self.tree = None
        self.get_tree(filename)

        self.scale_factor = scale_factor

        print "Sample %s : %d entries"%(name, self.tree.GetEntries())

    def get_tree(self, filename) :
        tree_name = "superNt"
        chain = r.TChain(tree_name)
        chain.Add(filename)
        self.tree = chain

def get_variables() :

    variables = {}

    """
    variables["mt2_bvis"] = [80, 0, 600]
    variables["l_pt[0]"] = [10, 0, 300]
    variables["l_pt[1]"] = [10, 0, 300]
    variables["l_eta[0]"] = [0.2, -3, 3]
    variables["l_eta[1]"] = [0.2, -3, 3]
    variables["abs(dphi_ll)"] = [0.1, 0, 3.2]
    variables["pTll"] = [20, 0, 600]
    variables["dRll"] = [0.2, 0, 6]
    variables["abs(cosThetaB)"] = [0.05, 0, 1]
    variables["abs(cosTheta1)"] = [0.05, 0, 1]
    variables["abs(cosTheta2)"] = [0.05, 0, 1]
    variables["abs(dphi_boost_ll)"] = [0.1, 0, 3.2]
    variables["nJets"] = [1, 0, 12]
    variables["nSJets"] = [1, 0, 12]
    variables["nBJets"] = [1, 0, 12]
    for i in xrange(3) :
        name = "j_pt[%d]"%i
        variables[name] = [20,0,500]
        name = "j_eta[%d]"%i
        variables[name] = [0.5, -5,5]
    
        name = "sj_pt[%d]"%i
        variables[name] = [10,0,500]
        name = "sj_eta[%d]"%i
        variables[name] = [0.5, -5,5]
    
        name = "bj_pt[%d]"%i
        variables[name] = [20,0,600]
        name = "bj_eta[%d]"%i
        variables[name] = [0.5, -5,5]
    
    variables["dRbb"] = [0.2, 0, 6]
    variables["abs(dphi_bb)"] = [0.1, 0, 3.2]
    variables["abs(dphi_ll_bb)"] = [0.1, 0, 3.2]
    variables["dR_ll_bb"] = [0.2, 0, 6]
    variables["abs(dphi_WW_bb)"] = [0.1, 0, 3.2]
    variables["mass_X"] = [40, 100, 1300]
    variables["mass_X_scaled"] = [40, 100, 1300]
    variables["met"] = [10, 0, 500]
    variables["abs(metPhi)"] = [0.1, 0, 3.2]
    variables["abs(dphi_met_ll)"] = [0.1, 0, 3.2]
    variables["mass_met_ll"] = [10, 0, 400]
    variables["met_pTll"] = [30, 0, 620]
    
    variables["HT2"] = [40, 0, 1200]
    variables["HT2Ratio"] = [0.05, 0, 1]
    variables["MT_HWW"] = [10, 0, 300]
    variables["MT_1"] = [20,180,1200]
    variables["MT_1_scaled"] = [20,180,1200]
    variables["mll"] = [10,0,400]
    variables["mt2"] = [5, 0, 140]
    variables["mt2_00"] = [20, 0, 1000]
    variables["mt2_01"] = [10, 0, 650]
    variables["mt2_10"] = [20, 0, 600]
    variables["mt2_llbb"] = [2, 0, 300]
    variables["mbb"] = [10,0,350]
    variables["mt2_bb"] = [20,0,450]
    variables["mt2_bvis"] = [20,0,600]
    variables["mt2_lvis"] = [20, 0, 600]
    variables["mT_llmet"] = [20,0,800]
    variables["mT_bb"] = [10, 0, 500]
    variables["min_mT_llmet_bb"] = [15,0,500]
    variables["max_mT_llmet_bb"] = [20,0,1200]
    
    variables["mt2_llbb"] = [10, 0, 350]
    variables["abs(cosTheta2)"] = [0.05, 0, 1]
    """
    variables["abs(cosThetaB)"] = [0.05, 0, 1]
    
    return variables

def make_event_list(samples, selection) :

    cut = r.TCut(selection)
    sel = r.TCut("1")

    for s in samples :
        list_name = "list_%s_selection"%s.name
        save_name = "./lists/" + list_name + ".root"
        if os.path.isfile(save_name) :
            rfile = r.TFile.Open(save_name)
            list = rfile.Get(list_name)
            s.tree.SetEventList(list)
        else :
            draw_list = ">> " + list_name
            s.tree.Draw(draw_list, sel*cut)
            list = r.gROOT.FindObject(list_name)
            s.tree.SetEventList(list)
            list.SaveAs(save_name)

def make_plot(samples, selection, var, bounds) :

    global list_made


    ok_name = make_name_ok(var)
    c = r.TCanvas("c_%s"%ok_name, "", 800, 600)
    c.cd()

    n_bins = bounds[2] - bounds[1]
    n_bins = n_bins / bounds[0]

    axis = r.TH1F("axis_%s"%ok_name, "", int(n_bins), bounds[1], bounds[2])
    axis.GetXaxis().SetTitle(var)
    axis.GetXaxis().SetTitleFont(42)
    axis.GetXaxis().SetLabelFont(42)

    axis.GetYaxis().SetTitle("Arb. Units")
    axis.GetYaxis().SetTitleFont(42)
    axis.GetYaxis().SetLabelFont(42)

    c.SetGrid(1,1)


    if not list_made :
        make_event_list(samples, selection)
        list_made = True

    weight = "eventweight"

    leg = r.TLegend(0.7, 0.72, 0.93, 0.93)
    maxy = []

    r.gStyle.SetPalette(r.kRainBow)

    histos = []
    for isample, s in enumerate(samples) :
        h = r.TH1F("h_%s_%s"%(ok_name, s.name), "", int(n_bins), bounds[1], bounds[2])
        h.SetLineColor(s.color)
        h.SetLineColor(r.gStyle.GetColorPalette(60*isample))
        if "x" not in s.name :
            h.SetLineColor(r.kRed)
        h.SetFillColor(0)
        h.SetLineWidth(2)
        if not s.signal and s.name == "ttbar" :
            h.SetLineColor(r.kBlack)
            #h.SetFillColorAlpha(r.gStyle.GetColorPalette(60*isample), 0.2)
            h.SetFillColorAlpha(2, 0.3)
        h.Sumw2()

        cut = "( %s ) * %s * %s"%(selection, weight, s.scale_factor)
        cut = r.TCut(cut)
        sel = r.TCut("1")

        cmd = "%s>>%s"%(var, h.GetName())
        s.tree.Draw(cmd, cut * sel, "goff")

        err = r.Double(0.0)
        integral = h.IntegralAndError(0,-1,err)
        if integral != 0 : h.Scale(1/integral)

        print "%s : %.2f +/- %.2f"%(s.name, integral, err)

        leg.AddEntry(h, s.displayname, "l")
        histos.append(h)
        maxy.append(h.GetMaximum())

    maxy = 1.25 * max(maxy)

    c.cd()
    axis.SetMaximum(maxy)
    axis.Draw("axis")
    c.Update()

    for h in histos :
        h.SetMaximum(maxy)
        h.Draw("hist same")

    leg.Draw()

    text = r.TLatex()
    text.SetNDC()
    text.SetTextFont(42)
    text.DrawLatex(0.15, 0.83, "#bf{#it{ATLAS}} Simulation")
    text.DrawLatex(0.15, 0.78, "pp #rightarrow hh #rightarrow WWbb")
    c.Update()

    outname = "./WWBBRECO/" + ok_name + ".pdf"
    c.SaveAs(outname)
    


def make_plots(samples, selection) :

    print "make_plots"
    variables = get_variables()
    n_total = len(variables)
    n_current = 1
    for var, bounds, in variables.iteritems() :
        print " > [%d/%d] %s"%(n_current, n_total, var)
        make_plot(samples, selection, var, bounds)
        n_current += 1

def make_name_ok(var) :
    name = var.replace("abs(","").replace(")","")
    name = name.replace("/", "_over_")
    name = name.replace("[","").replace("]","")
    return name

def get_sob(samples, selection) :

    print " * getting SOB * "
    print " SELECTION: %s"%selection
    split_sel = selection.split("&&")
    for isel, sel in enumerate(split_sel) :
        print " SEL [%d] : %s"%(isel, sel)

    global list_made

    if not list_made :
        make_event_list(samples, selection)
        list_made = True

    # group backgrounds and signal
    backgrounds = []
    signals = []

    for s in samples :
        if s.signal :
            signals.append(s)
        else :
            backgrounds.append(s)

    weight = "eventweight"


    # get total background yield
    bkg_yield = 0.0
    bkg_err = 0.0
    for ibkg, bkg in enumerate(backgrounds) :
        h = r.TH1F("h_bkg_%d"%ibkg, "", 4, 0, 4)
        h.Sumw2()

        cut = "( %s ) * %s * %s"%(selection, weight, bkg.scale_factor)
        cut = r.TCut(cut)
        sel = r.TCut("1")

        cmd = "%s>>%s"%("isMC", h.GetName())
        bkg.tree.Draw(cmd, cut * sel, "goff")

        err = r.Double(0.0)
        integral = h.IntegralAndError(0,-1,err)
        bkg_yield += integral
        bkg_err += err * err

    bkg_err = sqrt(bkg_err)

    signal_yields = {}
    for isig, sig in enumerate(signals) :
        h = r.TH1F("h_sig_%d"%isig, "", 4, 0, 4)
        h.Sumw2()

        cut = "( %s ) * %s * %s"%(selection, weight, sig.scale_factor)
        cut = r.TCut(cut)
        sel = r.TCut("1")

        cmd = "%s>>%s"%("isMC", h.GetName())
        sig.tree.Draw(cmd, cut * sel, "goff")

        err = r.Double(0.0)
        integral = h.IntegralAndError(0,-1,err)

        yield_list = []
        yield_list.append(integral)
        yield_list.append(err)

        signal_yields[sig.name] = yield_list

    print 50*"-"
    print " Total background yield : %.2f +/- %.2f"%(bkg_yield, bkg_err)
    print 25*"- "
    for isig, sig in enumerate(signals) :
        sig_yield = signal_yields[sig.name][0]
        sig_err = signal_yields[sig.name][1]
        print " Signal yield %s : %.2f +/- %.2f"%(sig.name, sig_yield, sig_err)
    print 50*"-"
    print "\n"
    print " SOB for luminosity estimate %.2f fb-1"%samples[0].scale_factor
    for isig, sig in enumerate(signals) :
        sig_yield = signal_yields[sig.name][0]
        denom = bkg_yield**2 + bkg_err**2
        s_over_b = sig_yield / sqrt( denom )
        print "  [%d] %s : %.5f"%(isig, sig.name, float(s_over_b))
    print 50*"-"

    print "\n"
    print " Zn for luminosity estimate %.2f fb-1"%samples[0].scale_factor
    for isig, sig in enumerate(signals) :
        sig_yield = signal_yields[sig.name][0]
        total_err = sqrt( (bkg_err/bkg_yield)**2 + (0.3)**2 )
        zn = r.RooStats.NumberCountingUtils.BinomialExpZ(sig_yield, bkg_yield, total_err)
        print "   [%d] %s : %.3f"%(isig, sig.name, float(zn))
    print 50*"-"

def get_pad_number(n_vars, ix, iy) :

    #print "n_vars %d  ix %d   iy %d "%(n_vars, ix, iy)

    return ix + n_vars * iy

def make_2d_plot(sample, var_list, selection) :

    global list_made

    r.gStyle.SetPalette(r.kBird)
    #r.gStyle.SetPalette(r.kRainBow)
    #r.gStyle.SetPalette(r.kInvertedDarkBodyRadiator)

    n_vars = len(var_list)
    n_vars += 1 # for the board row on LHS/Bottom
    c = r.TCanvas("c_2d_%s"%sample.name, "", 800, 800)
    #c.Divide(n_vars, n_vars, 0., 0.)
    c.Divide(n_vars, n_vars, 0.0002, 0.0002)

    all_variables = get_variables()
    variables = {}
    for var, bounds in all_variables.iteritems() :
        if var in var_list :
            variables[var] = bounds

    #weight = "eventweight"
    weight = "1"

    histos = []
    histo_coords = []

    x_vars = {}
    y_vars = {}

    for ix, xvar in enumerate(variables.keys()) :
        for iy, yvar in enumerate(variables.keys()) :
            if iy < ix : continue

            print " > 2d [%d,%d] (%s,%s)"%(ix, iy, xvar, yvar)

            if not list_made :
                make_event_list([sample], selection)

            x_vars[ix] = xvar
            y_vars[iy] = yvar

            pad_number = get_pad_number(n_vars, ix, iy)
            #print "pad %d"%pad_number

            #c.cd(pad_number)

            xbounds = variables[xvar]
            ybounds = variables[yvar]

            n_x_bins = xbounds[2] - xbounds[1]
            n_x_bins = n_x_bins / xbounds[0]

            n_y_bins = ybounds[2] - ybounds[1]
            n_y_bins = n_y_bins / ybounds[0]

            h = r.TH2F("h_2d_%s_%d_%d"%(sample.name, ix, iy), "", int(n_x_bins), xbounds[1], xbounds[2],
                                                                    int(n_y_bins), ybounds[1], ybounds[2])

            yaxis = h.GetYaxis()
            yaxis.SetLabelFont(42)
            yaxis.SetLabelSize(1.8*yaxis.GetLabelSize())
            #yaxis.CenterTitle(True)
            #yaxis.SetTitleFont(42)
            #yaxis.SetTitleSize(2*yaxis.GetTitleSize())
            #yaxis.SetTitle(yvar)

            xaxis = h.GetXaxis()
            xaxis.SetLabelFont(42)
            xaxis.SetLabelSize(1.3*xaxis.GetLabelSize())
            #xaxis.CenterTitle(True)
            #xaxis.SetTitleFont(42)
            #xaxis.SetTitleSize(2*yaxis.GetTitleSize())
            #xaxis.SetTitle(xvar)

            cut = "( %s ) * %s * %s"%(selection, weight, sample.scale_factor)
            cut = r.TCut(cut)
            sel = r.TCut("1")

            cmd = "%s:%s>>%s"%(yvar, xvar, h.GetName())
            sample.tree.Draw(cmd, cut * sel, "goff")

            #print "blah  %d"%h.GetEntries()

            integral = h.Integral()
            if integral != 0 : h.Scale(1/h.Integral())

            h.SetMinimum(1.02 * h.GetMinimum())

            histos.append(h)
            histo_coords.append([ix, iy])

    for ihisto, histo in enumerate(histos) :
        coords = histo_coords[ihisto]
        ix = coords[0]
        ix += 1
        iy = coords[1]
        if iy == (n_vars - 1) :
            iy += 1
        pad = get_pad_number(n_vars, ix, iy)
        c.cd(pad + 1)

        histo.Draw("same col")
        c.Update()

    for x in xrange(n_vars-1) :
        #pad = get_pad_number(n_vars, x, 0)
        c.cd(x*n_vars + 1)
        text = r.TLatex()
        text.SetTextSize(2.2*text.GetTextSize())
        text.SetNDC()
        text.DrawLatex(0.1, 0.5, y_vars[x])
        c.Update()

    for x in xrange(n_vars-1) :
        pad = (n_vars-1)*n_vars + x + 2
        c.cd(pad)
        text = r.TLatex()
        text.SetTextSize(2.2*text.GetTextSize())
        text.SetNDC()
        text.DrawLatex(0.1, 0.5, x_vars[x])
        c.Update()
        

    save_name = "%s_2d_scatter.pdf"%sample.name
    save_name = "./WWBB2D/%s"%save_name
    c.SaveAs(save_name)


def make_2d_plots(samples, signame, selection) :

    vars_for_2D = ["mbb",
                    "mt2_llbb",
                    "dR_ll_bb",
                    "abs(dphi_met_ll)",
                    "abs(dphi_ll)",
                    "dRbb",
                    "HT2Ratio",
                    "abs(cosThetaB)"]

    background = None
    signal = None

    for s in samples :
        if s.signal and s.name == signame :
            signal = s
        elif s.signal :
            continue
        elif s.name == "ttbar" :
            background = s
        else :
            print "make_2d_plots   Whoops, no samples satisfy you. Exiting."
            sys.exit()

    samples = [signal, background]
    for s in samples :
        make_2d_plot(s, vars_for_2D, selection)

    


def main() :

    parser = OptionParser()
    parser.add_option("--sob", default=False, action="store_true")
    parser.add_option("--plots", default=False, action="store_true")
    parser.add_option("--plots2D", default=False, action="store_true")
    parser.add_option("--sig42D",default="hh")
    (options, args) = parser.parse_args()

    do_sob = options.sob
    do_plots = options.plots
    do_plots2D = options.plots2D
    sig_for2D_plot = options.sig42D

    if not do_sob and not do_plots and not do_plots2D :
        print "You have not provided any input, exiting"
        sys.exit()


    lumi_weight = 40.0
    ttbar = Sample(ttbar_file, "ttbar", "t#bar{t}", 1, False, lumi_weight)
    x1000 = Sample(x1000_file, "x1000", "X (1000 GeV)", 3, True, lumi_weight)
    x800 = Sample(x800_file, "x800", "X (800 GeV)", 4, True, lumi_weight)
    x600 = Sample(x600_file, "x600", "X (600 GeV)", r.kMagenta+2, True, lumi_weight)
    x400 = Sample(x400_file, "x400", "X (400 GeV)", r.kCyan+2, True, lumi_weight)
    hh = Sample(hh_file, "hh", "HH", 2, True, lumi_weight)

    samples = [ttbar, x1000, x800, x600, x400, hh]

    if do_plots2D :
        found_it = False
        for s in samples :
            if s.name == sig_for2D_plot :
                found_it = True

        if not found_it :
            print "Did not find requested signal %s in loaded samples, exiting"%sig_for2D_plot
            sys.exit()

    # define here the selection
    isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<0"
    isSFOS = "(( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && abs(mll-91.2)>10 && (l_q[0]*l_q[1])<0)"
    two_leptons = "( (%s) || (%s) )"%(isDFOS, isSFOS)
    #two_leptons = "nLeptons==2 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<0"
    trigger = "((year==2015 && trig_pass2015==1) || (year==2016 && trig_pass2016update==1))"
    selection = "%s && %s && nBJets==2 && nSJets>0 && mll>20"%(two_leptons, trigger)
    #selection = "%s && nBJets==2 && %s && mll>20 && l_pt[0]>25 && l_pt[1]>20 && mll<80 && HT2Ratio>0.8 && mT_bb>100 && dRbb<1.8 && MT_1_scaled>400"%(two_leptons, trigger) 
    #selection = "%s && nBJets==2 && nSJets>0 && %s && mll>20 && HT2Ratio>0.85 && abs(dphi_ll)<1 && mbb>80 && mbb<140 && dR_ll_bb>2.2 && dRbb<1.25 && mt2_llbb>100 && mt2_llbb<150 && abs(dphi_met_ll)<1"%(two_leptons, trigger) 
    # this is a good selection May 9 2017
    #selection = "%s && nBJets==2 && nSJets>0 && %s && mll>20 && HT2Ratio>0.85 && abs(dphi_ll)<1 && mbb>80 && mbb<140 && dR_ll_bb>2.2 && dRbb<1.25 && mt2_llbb>100 && mt2_llbb<150 && abs(dphi_met_ll)<1 && abs(cosThetaB)<0.7"%(two_leptons, trigger) 

    dphi_met_ll = "abs(dphi_met_ll)<1"
    dphi_met_ll = "1"

    base_selection = "%s && %s && nBJets==2 && nSJets>0 && mll>20"%(two_leptons, trigger)
    mbb_window = "mbb > 80 && mbb < 140"
    mt2_ll_bb_window = "mt2_llbb>100 && mt2_llbb<150"
    dRllbb = "dR_ll_bb>2.2"
    dphi_ll = "abs(dphi_ll)<1"
    dRbb = "dRbb<1.25"
    HT2Ratio = "HT2Ratio>0.85"
    cosThetaB = "abs(cosThetaB)<0.7"
    #cosThetaB = "1"

    sel0 = base_selection
    sel1 = sel0 + " && " + mbb_window
    sel2 = sel1 + " && " + mt2_ll_bb_window
    sel3 = sel2 + " && " + dRllbb
    sel4 = sel3 + " && " + dphi_met_ll
    sel5 = sel4 + " && " + dphi_ll
    sel6 = sel5 + " && " + dRbb
    sel7 = sel6 + " && " + HT2Ratio
    sel8 = sel7 + " && " + cosThetaB

    selection = sel8


    if do_plots :
        make_plots(samples, selection)    

    if do_sob or do_plots :
        x = r.RooStats
        get_sob(samples, selection)

    selection_for_2d = "nBJets==2 && nSJets>0 && mll>20"
    #selection_for_2d = "%s && %s && nBJets==2 && nSJets>0 && mll>20"%(two_leptons, trigger)

    if do_plots2D :
        make_2d_plots(samples, sig_for2D_plot, selection_for_2d)

#_________________________________________________________________
if __name__ == "__main__" :
    main()
