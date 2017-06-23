#!/usr/bin/env python

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(1)
r.gStyle.SetOptStat(0)

import sys
import os

from optparse import OptionParser

import glob

filedir = "/data/uclhc/uci/user/dantrim/ntuples/n0232/f_jun5/mc/Raw/"

wt_dsids = [410015, 410016]
tt_dsids = [410009]
hh_dsids = [342053]

class Sample :
    def __init__(self, filedir, dsid_list, name, displayname) :
        self.filedir = filedir
        self.dsid_list = dsid_list
        self.name = name
        self.displayname = displayname

        self.tree = self.get_chain(filedir, dsid_list)

    def get_chain(self, filedir, dsids) :

        all_files = glob.glob(filedir + "*.root")
        sample_files = []
        for f in all_files :
            for ds in dsids :
                if str(ds) in f :
                    sample_files.append(f)
                    break

        print "%d files found for %s"%(len(sample_files), self.name)

        c = r.TChain("superNt")
        for f in sample_files :
            c.AddFile(f)

        return c

class RatioCanvas :
    def __init__(self, name) :
        self.name = "c_" + name
        self.canvas = r.TCanvas(self.name,self.name, 768, 768)
        self.upper_pad = r.TPad("upper", "upper", 0.0, 0.0, 1.0, 1.0)
        self.lower_pad = r.TPad("lower", "lower", 0.0, 0.0, 1.0, 1.0)
        self.set_pad_dimensions()

    def set_pad_dimensions(self) :
        can = self.canvas
        up  = self.upper_pad
        dn  = self.lower_pad

        can.cd()
        up_height = 0.75
        dn_height = 0.30
        up.SetPad(0.0, 1.0-up_height, 1.0, 1.0)
        dn.SetPad(0.0, 0.0, 1.0, dn_height)

        up.SetTickx(0)
        dn.SetGrid(0)
        dn.SetTicky(0)

        up.SetFrameFillColor(0)
        up.SetFillColor(0)

        # set right margins
        up.SetRightMargin(0.05)
        dn.SetRightMargin(0.05)

        # set left margins
        up.SetLeftMargin(0.14)
        dn.SetLeftMargin(0.14)

        # set top margins
        up.SetTopMargin(0.7 * up.GetTopMargin())

        # set bottom margins
        up.SetBottomMargin(0.09)
        dn.SetBottomMargin(0.4)

        up.Draw()
        dn.Draw()
        can.Update()

        self.canvas = can
        self.upper_pad = up
        self.lower_pad = dn

def get_variables() :

    variables = {}

    # jets
    variables["nBJets"] = [1,0,10]
    variables["nSJets"] = [1, 0, 15]
    variables["bj_pt[0]"] = [10, 0, 350]
    variables["bj_pt[1]"] = [5, 0, 160]
    variables["bj_pt[2]"] = [5, 0, 120]
    variables["bj_eta[0]"] = [0.1, -2.5, 2.5]
    variables["bj_eta[1]"] = [0.1, -2.5, 2.5]
    variables["bj_eta[2]"] = [0.1, -2.5, 2.5]
    variables["mbb"] = [10, 0, 400]
    variables["dRbb"] = [0.2, 0, 6]

    # jets + leptons
    variables["abs(dphi_j0_ll)"] = [0.1, 0, 3.2]
    variables["abs(dphi_j0_l0)"] = [0.1, 0, 3.2]
    variables["abs(dphi_sj0_ll)"] = [0.1, 0, 3.2]
    variables["abs(dphi_sj0_l0)"] = [0.1, 0, 3.2]
    variables["abs(dphi_bj0_ll)"] = [0.1, 0, 3.2]
    variables["abs(dphi_bj0_l0)"] = [0.1, 0, 3.2]
    variables["dR_ll_bb"] = [0.2, 0, 6]
    variables["abs(dphi_ll_bb)"] = [0.1, 0, 3.2]

    # met
    variables["met"] = [10, 0, 300]

    # leptons
    variables["l_pt[0]"] = [5, 0, 300]
    variables["l_pt[1]"] = [5, 0, 180]
    variables["l_eta[0]"] = [0.1, -2.5, 2.5]
    variables["l_eta[1]"] = [0.1, -2.5, 2.5]
    variables["mll"] = [10, 0, 400]
    variables["pTll"] = [10, 0, 400]
    variables["dRll"] = [0.2, 0, 6]
    variables["abs(dphi_ll)"] = [0.1, 0, 3.2]

    # sr-like
    variables["HT2Ratio"] = [0.05, 0, 1]
    variables["meff"] = [20,0,1000]
    variables["met_pTll"] = [20, 0, 800]
    variables["mt2_bb"] = [10, 0, 300]
    variables["mt2_bvis"] = [10,0,400]
    variables["mt2_lvis"] = [10,0,400]

    return variables

def make_1d_plot(var, bounds, ttbar, wt, selection, hh = None) :

    selection_to_use = selection
    #if "nBJets" in var :
    #    selection_to_use = selection.replace("&& nBJets>=2","")

    ok_name = var.replace("(","").replace(")","").replace("[","").replace("]","").replace("abs","")

    c = RatioCanvas(ok_name)
    c.canvas.cd()
    c.upper_pad.cd()
    c.upper_pad.SetGrid(1,1)
    c.upper_pad.SetTickx(1)
    c.upper_pad.SetTicky(1)
    c.upper_pad.Update()

    ## plots
    n_bins = bounds[2] - bounds[1]
    n_bins = n_bins / bounds[0]

    htt = r.TH1F("htt_%s_tt"%ok_name, "", int(n_bins), bounds[1], bounds[2]) 

    initial_title_offset = htt.GetXaxis().GetTitleOffset()
    initial_label_offset = htt.GetXaxis().GetLabelOffset()

    htt.GetXaxis().SetTitle(var)
    htt.GetYaxis().SetTitle("arb. units")
    htt.GetYaxis().SetTitleOffset(1.2*htt.GetYaxis().GetTitleOffset())
    htt.GetXaxis().SetTitleFont(42)
    htt.GetXaxis().SetLabelFont(42)
    htt.GetXaxis().SetLabelOffset(-999)
    htt.SetLineColor(r.kBlue)
    htt.SetLineWidth(2)
    htt.Sumw2()

    hwt = r.TH1F("hwt_%s_wt"%ok_name, "", int(n_bins), bounds[1], bounds[2])
    hwt.SetLineColor(r.kRed)
    hwt.SetLineWidth(2)
    hwt.GetXaxis().SetTitle(var)
    hwt.GetYaxis().SetTitle("arb. units")
    hwt.GetYaxis().SetTitleOffset(1.5*hwt.GetYaxis().GetTitleOffset())
    hwt.GetXaxis().SetTitleFont(42)
    hwt.GetXaxis().SetLabelFont(42)
    hwt.GetXaxis().SetLabelOffset(-999)
    hwt.Sumw2()

    hhh = None
    if hh :
        hhh = r.TH1F("hwt_%s_hh"%ok_name, "", int(n_bins), bounds[1], bounds[2])
        hhh.SetLineColor(r.kBlack)
        hhh.SetLineWidth(2)
        hhh.SetLineStyle(2)
        hhh.GetXaxis().SetTitle(var)
        hhh.GetYaxis().SetTitle("arb. units")
        hhh.GetYaxis().SetTitleOffset(1.5*hhh.GetYaxis().GetTitleOffset())
        hhh.GetXaxis().SetTitleFont(42)
        hhh.GetXaxis().SetLabelFont(42)
        hhh.GetXaxis().SetLabelOffset(-999)
        hhh.Sumw2()

    ## draw
    cmd = "%s>>%s"%(var, htt.GetName())
    cut = r.TCut(selection_to_use)
    sel = r.TCut("1")
    ttbar.tree.Draw(cmd, cut * sel, "goff")

    cmd = "%s>>%s"%(var, hwt.GetName())
    wt.tree.Draw(cmd, cut * sel, "goff")

    if hh :
        cmd = "%s>>%s"%(var, hhh.GetName())
        hh.tree.Draw(cmd, cut * sel, "goff")

    tt_integral = htt.Integral()
    wt_integral = hwt.Integral()
    hh_integral = 0
    if hh :
        hh_integral = hhh.Integral()
    tt_scaled = False
    wt_scaled = False
    hh_scaled = False
    if tt_integral != 0 :
        htt.Scale(1/tt_integral)
        tt_scaled = True
    if wt_integral != 0 :
        hwt.Scale(1/wt_integral)
        wt_scaled = True
    if hh_integral != 0 :
        hhh.Scale(1/hh_integral)
        hh_scaled= True
    all_scaled = (tt_scaled and wt_scaled)
    if hh :
        all_scaled = (all_scaled and hh_scaled)
    if not all_scaled :
        print "Could not normalize all histograms!"
        return

    maxy = htt.GetMaximum()
    if hwt.GetMaximum() > maxy : maxy = hwt.GetMaximum()
    if hh :
        if hhh.GetMaximum() > maxy : maxy = hhh.GetMaximum()
    maxy = 1.5*maxy
    htt.SetMaximum(maxy)
    hwt.SetMaximum(maxy)
    hhh.SetMaximum(maxy)

    leg = r.TLegend(0.8, 0.8, 0.92, 0.9)
    leg.AddEntry(htt, ttbar.displayname, "l")
    leg.AddEntry(hwt, wt.displayname, "l")
    if hh :
        leg.AddEntry(hhh, hh.displayname, "l")

    htt.Draw("hist")
    c.upper_pad.Update()
    hwt.Draw("hist same")
    c.upper_pad.Update()
    if hh :
        hhh.Draw("hist same")
        c.upper_pad.Update()
    leg.Draw()
    c.upper_pad.Update()

    ########################################
    # lower pad
    c.lower_pad.cd()
    c.lower_pad.SetGrid(1,1)
    c.lower_pad.SetTickx(1)
    c.lower_pad.SetTicky(1)

    h_ratio = htt.Clone("ratio")
    h_ratio.Divide(hwt)
    h_ratio.SetLineColor(r.kBlue)
    h_ratio.SetLineWidth(2)
    yax = h_ratio.GetYaxis()
    xax = h_ratio.GetXaxis()
    h_ratio.GetYaxis().SetTitleSize(2.7*yax.GetTitleSize())
    h_ratio.GetYaxis().SetLabelSize(2.7*yax.GetLabelSize())
    h_ratio.GetXaxis().SetTitleSize(2.7*xax.GetTitleSize())
    h_ratio.GetXaxis().SetLabelSize(2.7*xax.GetLabelSize())
    h_ratio.GetXaxis().SetLabelFont(42)
    h_ratio.GetXaxis().SetTitleFont(42)
    h_ratio.GetYaxis().SetTitleFont(42)
    h_ratio.GetYaxis().SetLabelFont(42)

    h_ratio.SetMinimum(0)
    h_ratio.SetMaximum(2)
    h_ratio.GetYaxis().SetTitle("X/Wt")
    yax.SetTitleOffset(0.5*yax.GetTitleOffset())
    yax.SetLabelSize(0.6*yax.GetLabelSize())
    h_ratio.GetXaxis().SetLabelOffset(initial_label_offset)
    h_ratio.GetXaxis().SetTitleOffset(initial_title_offset)

    hh_ratio = None
    if hh :
        hh_ratio = hhh.Clone("ratio")
        hh_ratio.Divide(hwt)
        hh_ratio.SetLineColor(r.kBlack)
        hh_ratio.SetLineWidth(2)
        yax = hh_ratio.GetYaxis()
        xax = hh_ratio.GetXaxis()
        hh_ratio.GetYaxis().SetTitleSize(2.7*yax.GetTitleSize())
        hh_ratio.GetYaxis().SetLabelSize(2.7*yax.GetLabelSize())
        hh_ratio.GetXaxis().SetTitleSize(2.7*xax.GetTitleSize())
        hh_ratio.GetXaxis().SetLabelSize(2.7*xax.GetLabelSize())
        hh_ratio.GetXaxis().SetLabelFont(42)
        hh_ratio.GetXaxis().SetTitleFont(42)
        hh_ratio.GetYaxis().SetTitleFont(42)
        hh_ratio.GetYaxis().SetLabelFont(42)

        hh_ratio.SetMinimum(0)
        hh_ratio.SetMaximum(2)
        hh_ratio.GetYaxis().SetTitle("X/Wt")
        yax.SetTitleOffset(0.5*yax.GetTitleOffset())
        yax.SetLabelSize(0.6*yax.GetLabelSize())
        hh_ratio.GetXaxis().SetLabelOffset(initial_label_offset)
        hh_ratio.GetXaxis().SetTitleOffset(initial_title_offset)

    line = r.TLine(bounds[1], 1, bounds[2], 1)
    line.SetLineStyle(2)
    line.SetLineWidth(2)
    line.SetLineColor(r.kRed)

    h_ratio.Draw("hist")
    if hh :
        hh_ratio.Draw("hist same")
    line.Draw()
    c.lower_pad.Update()

    save_name = "./plots_singletop/st_wt_%s.eps"%ok_name
    c.canvas.SaveAs(save_name)


def make_1d_plots(ttbar, wt, specific_variable, hh = None) :

    variables = get_variables()
    to_use = {}

    if specific_variable != "" :
        for v in variables.keys() :
            if v != specific_variable : continue
            to_use[v] = variables[v]
    else :
        to_use = variables

    n_total = len(to_use)

    selection = "(nLeptons==2 && l_pt[0]>25 && l_pt[1]>20 && mll>20 && nBJets>=2 && HT2Ratio>=0.8) * eventweight"

    n_current = 1
    for var, bounds in to_use.iteritems() :
        print "make_1d_plots    [%d/%d] %s"%(n_current, n_total, var)
        n_current += 1
        make_1d_plot(var, bounds, ttbar, wt, selection, hh)

def main() :

    parser = OptionParser()
    parser.add_option("--one", default="1", help="Do 1d plots")
    parser.add_option("--two", default="0", help="Do 2d plots")
    parser.add_option("--var", default="", help="Plot specific variable")
    parser.add_option("--sig", action="store_true", default=False)
    (options, args) = parser.parse_args()
    do_1d = bool(int(options.one))
    do_2d = bool(int(options.two))
    specific_variable = options.var
    do_signal = options.sig

    if do_2d :
        print "\n2d plotting is not supported (yet)"
        do_2d = False

    if not do_1d and not do_1d :
        print "\nNothing to plot!"
        sys.exit()

    
    ttbar = Sample(filedir, tt_dsids, "ttbar", "t#bar{t}") 
    wt = Sample(filedir, wt_dsids, "wt", "Wt")
    hh = None
    if do_signal :
        hh = Sample(filedir, hh_dsids, "hh", "hh")

    if do_1d :
        make_1d_plots(ttbar, wt, specific_variable, hh)


#___________________________________________________________________________
if __name__ == "__main__" :
    main()
