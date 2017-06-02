#!/usr/bin/env python

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(1)
r.gStyle.SetOptStat(0)

import sys
import os

import array

from optparse import OptionParser

# files
filedir = "/data/uclhc/uci/user/dantrim/ntuples/n0232/e_may31/mc/Raw/"
hh_file = "%sCENTRAL_342053.root"%filedir
x1000_file = "%sCENTRAL_343777.root"%filedir

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

def get_efficiencies(sample, lower_pt, upper_pt, pt_step, trigger="") :

    # get pt cut boundaries
    pt_cuts = []
    n_steps = upper_pt - lower_pt
    n_steps = n_steps / pt_step 
    current = lower_pt
    for i in xrange(n_steps+1) :
        pt_cuts.append(current)
        current += pt_step

    sel = r.TCut("1")

    #test_cut = "l_pt[0]>120 && ((year==2015 && (trig_e24_lhmedium_L1EM20VHI==1 || trig_mu26_imedium==1)) || (year==2016 && (trig_e26_lhtight_ivarloose==1 || trig_mu20_iloose_L1MU15==1)))"
    eff_dict = {}
    for icut, pt_cut in enumerate(pt_cuts) :

        sub_lead_cut = 0.8*float(pt_cut)

        cut = "l_pt[0]>%s && l_pt[1]>%s && mll>20"%(pt_cut, str(sub_lead_cut))
        if trigger!="" :
            cut = cut + " && " + trigger
        
       # cut = cut + "l_pt[0]>%s"%pt_cut
        #print cut
        cut = "(" + cut + ")"# * eventweight * %s"%sample.scale_factor
        #print cut
        #print test_cut
        cut = r.TCut(cut)

        h = r.TH1F("h_%d_%s"%(icut, sample.name), "", 4, 0, 4)
        #h.Sumw2()

        cmd = "%s>>%s"%("isMC", h.GetName())
        sample.tree.Draw(cmd, cut, "goff")

        stat_err = r.Double(0.0)
        integral = h.IntegralAndError(0,-1, stat_err)
        #print "%s pt>%s : %.2f +/- %.2f"%(sample.name, pt_cut, integral, stat_err)

        eff_dict[pt_cut] = integral

        #sys.exit()

    return eff_dict

def get_efficiencies_2d(sample, lower_pt, upper_pt, pt_step, trigger="") :

    # get pt cut boundaries
    pt_cuts = []
    n_steps = upper_pt - lower_pt
    n_steps = n_steps / pt_step
    current = lower_pt
    for i in xrange(n_steps+1) :
        pt_cuts.append(current)
        current += pt_step


    sel = r.TCut("1")

    eff_dict = {}
    # lead lepton
    for icut, ipt in enumerate(pt_cuts) :
        # sub-lead lepton
        for jcut, jpt in enumerate(pt_cuts) :
            if not ipt > jpt : continue # require sub-lead lepton to have lower pt

            cut = "l_pt[0]>%s && l_pt[1]>%s && mll>20"%(ipt, jpt)

            if trigger != "" :
                cut = cut + " && " + trigger

            cut = "(" + cut + ")"
            cut = r.TCut(cut)

            h = r.TH1F("h_%d_%d_%s"%(ipt, jpt, sample.name), "", 4, 0, 4)

            cmd = "%s>>%s"%("isMC", h.GetName())
            sample.tree.Draw(cmd, cut, "goff")

            stat_err = r.Double(0.0)
            integral = h.IntegralAndError(0,-1, stat_err)
            key = (ipt, jpt)
            eff_dict[key] = integral

    return eff_dict, pt_cuts

def make_eff(eff_none, eff_trig, trig_name, sample) :

    # get the bounds
    pt_cuts = eff_none.keys() 
    lower_pt_cut = pt_cuts[0]
    upper_pt_cut = pt_cuts[-1]
    n_bins = len(pt_cuts)

    c = r.TCanvas("c_%s_%s"%(sample.name, trig_name), "", 800, 600)
    c.cd()

    hden = r.TH1F("hden_%s_%s"%(sample.name, trig_name), "", n_bins, lower_pt_cut, upper_pt_cut)
    hden.SetTitle("%s #epsilon")

    x = hden.GetXaxis()
    x.SetTitleFont(42)
    x.SetTitle("Leading lepton p_{T} [GeV]")
    x.SetLabelFont(42)

    y = hden.GetYaxis()
    y.SetTitleFont(42)
    y.SetTitle("#epsilon")
    y.SetLabelFont(42)

    miny = 2

    #for pt, yld in eff_none.iteritems() :
    for ipt, pt_cut in enumerate(eff_none.keys()) :
        hden.SetBinContent(ipt, int(eff_none[pt_cut]))
        #hden.Fill(pt, int(yld))
        #if float(yld) < miny : miny = yld

    hnum= r.TH1F("hnum_%s_%s"%(sample.name, trig_name), "", n_bins, lower_pt_cut, upper_pt_cut)
    hnum.SetTitle("%s #epsilon")

    x = hnum.GetXaxis()
    x.SetTitleFont(42)
    x.SetTitle("Leading lepton p_{T} [GeV]")
    x.SetLabelFont(42)

    y = hnum.GetYaxis()
    y.SetTitleFont(42)
    y.SetTitle("#epsilon")
    y.SetLabelFont(42)

    #for pt, yld in eff_trig.iteritems() :
    for ipt, pt_cut in enumerate(eff_trig.keys()) :
        hnum.SetBinContent(ipt, int(eff_trig[pt_cut]))
        #hnum.Fill(pt, int(yld))
        #if float(yld) < miny : miny = yld

    #hnum.SetMinimum(0.95*miny)
    #hden.SetMinimum(0.95*miny)

    eff = r.TEfficiency(hnum, hden)
    c.cd()
    eff.Draw("AP")
    #hnum.Divide(hden)
    #hnum.Draw("P")
    c.Update()

    c.SaveAs("./test_plots/test_eff.eps")

def make_eff_2d(eff_none, eff_trig, pt_cuts, trig_type, trig_name, sample) :

    #r.gStyle.SetPalette(r.kBlackBody)
    r.gStyle.SetPalette(r.kBird)

    # get the bounds
    #pt_cuts = eff_none.keys()
    #pt_cuts_tmp = []
    #for x in pt_cuts :
    #    if x[1] not in pt_cuts_tmp :
    #        pt_cuts_tmp.append(x[0])
    #pt_cuts_tmp = sorted(pt_cuts_tmp)
    lower_pt_cut = pt_cuts[0]
    upper_pt_cut = pt_cuts[-1]
    n_bins = len(pt_cuts)

    #print pt_cuts
    #sys.exit()

    #print pt_cuts_tmp
    #sys.exit()

    c = r.TCanvas("c_%s_%s"%(sample.name, trig_name), "", 800, 600)
    c.SetRightMargin(1.08*c.GetRightMargin())
    c.cd()

    hden = r.TH2F("hden_%s_%s"%(sample.name, trig_name), "", n_bins, lower_pt_cut, upper_pt_cut,
                n_bins, lower_pt_cut, upper_pt_cut)
    hden.SetTitle("%s #epsilon : %s"%(sample.name, trig_name))
    x = hden.GetXaxis()
    x.SetTitleFont(42)
    x.SetTitle("Leading lepton p_{T} [GeV]")
    x.SetLabelFont(42)
    y = hden.GetYaxis()
    y.SetTitleFont(42)
    y.SetTitle("Sub-leading lepton p_{T} [GeV]")
    y.SetLabelFont(42)
    hden.SetMarkerSize(0.35*hden.GetMarkerSize())

    hden.SetMaximum(1.0)

    miny = 2

    for pt_keys in eff_none.keys() :
        x_pt_cut = pt_keys[0]
        y_pt_cut = pt_keys[1]

        x_idx = pt_cuts.index(int(x_pt_cut))
        y_idx = pt_cuts.index(int(y_pt_cut))

        eff = float(eff_trig[pt_keys]) / float(eff_none[pt_keys])

        if eff < miny : miny = eff

        #print "(%.2f, %.2f) pt : %.2f  (%d, %d)"%(float(x_pt_cut), float(y_pt_cut), eff, int(x_idx), int(y_idx))

        #hden.Fill(x_pt_cut, y_pt_cut, eff)
        hden.SetBinContent(x_idx+1, y_idx+1, eff)

    hden.SetMaximum(1.0)
    hden.SetMinimum(0.95*miny)


    c.cd()
    r.gStyle.SetNumberContours(512)

    #hden.Draw("CONT4Z")
    hden.Draw("colz")
    c.Update()

    text = r.TLatex()
    text.SetTextSize(0.35*text.GetTextSize())
    for ipt, ip in enumerate(pt_cuts) :
        for jpt, jp in enumerate(pt_cuts) :
            if not ip > jp : continue
            if ip%5==0 and jp%5==0 :
                x_idx = pt_cuts.index(ip)
                y_idx = pt_cuts.index(jp)

                key = (ip, jp)

                eff = float(eff_trig[key]) / float(eff_none[key])
                text.DrawLatex(ip-1, jp, "%.2f"%eff)
    c.Update()

    #c.SaveAs("./test_plots/test_eff_2d.eps")
    c.SaveAs("./trig_eff_plots/trig_eff_2d_%s_%s.eps"%(sample.name, trig_type))

    


def make_trig_eff_plots(samples, trig_type) :

    # 2015 dilepton
    dielectron_2015 = "trig_2e12_lhloose_L12EM10VH==1"
    dimuon_2015 = "trig_mu18_mu8noL1==1"
    emu_2015 = "trig_e17_lhloose_nod0_mu14==1"

    # 2016 dilepton
    dielectron_2016 = "trig_2e17_lhvloose_nod0==1"
    dimuon_2016 = "trig_mu22_mu8noL1==1"
    emu_2016 = "trig_e17_lhloose_mu14==1"

    # 2015 single lepton
    single_electron_2015 = "trig_e24_lhmedium_L1EM20VHI==1"
    single_muon_2015 = "trig_mu26_imedium==1"

    # 2016 single lepton
    single_electron_2016 = "trig_e26_lhtight_ivarloose==1"
    single_muon_2016 = "trig_mu20_iloose_L1MU15==1"

    # dilepton only
    dilepton_2015 = "year==2015 && (%s || %s || %s)"%(dielectron_2015, dimuon_2015, emu_2015)
    dilepton_2016 = "year==2016 && (%s || %s || %s)"%(dielectron_2016, dimuon_2016, emu_2016)

    # single lepton only
    single_2015 = "year==2015 && (%s || %s)"%(single_electron_2015, single_muon_2015)
    single_2016 = "year==2016 && (%s || %s)"%(single_electron_2016, single_muon_2016)


    # dilepton final
    dilepton_triggers = " %s || %s "%(dilepton_2015, dilepton_2016)
    dilepton_triggers = "((%s) || (%s))"%(dilepton_2015, dilepton_2016)

    # signle lepton final
    #single_lepton_triggers = " (%s) || (%s) "%(single_2015, single_2016)
    single_lepton_triggers = "((%s) || (%s))"%(single_2015, single_2016)

    # dilepton OR'd with single
    di_or_si_triggers = "( ((%s) || (%s)) || ((%s) || (%s)) ) "%(single_2015, single_2016, dilepton_2015, dilepton_2016)

    # dilepton AND with single
    di_and_si_triggers = "( ((%s) || (%s)) && ((%s) || (%s)) ) "%(single_2015, single_2016, dilepton_2015, dilepton_2016)


    single_test = dielectron_2016

    nice_names = {}
    nice_names["single"] = "Single Lepton Triggers"
    nice_names["dilepton"] = "Dilepton Triggers"
    nice_names["di-or-si"] = "Dilepton OR Single"
    nice_names["di-and-si"] = "Dilepton AND Single"

    ##########################################################
    # scan pT ranges 6 to 30 in steps of 2
    efficiencies = []
    min_pt = 1
    max_pt = 45
    pt_step = 1
    for s in samples :

        # denominator
        eff_dict_none, pt_cuts = get_efficiencies_2d(s, min_pt, max_pt, pt_step, trigger="")

        eff_dict_trig = {}
        if trig_type == "single" :
            eff_dict_trig, pt_cuts = get_efficiencies_2d(s, min_pt, max_pt, pt_step, trigger=single_lepton_triggers)
        elif trig_type == "dilepton" :
            eff_dict_trig, pt_cuts = get_efficiencies_2d(s, min_pt, max_pt, pt_step, trigger=dilepton_triggers)
        elif trig_type == "di-or-si" :
            eff_dict_trig, pt_cuts = get_efficiencies_2d(s, min_pt, max_pt, pt_step, trigger=di_or_si_triggers)
        elif trig_type == "di-and-si" :
            eff_dict_trig, pt_cuts = get_efficiencies_2d(s, min_pt, max_pt, pt_step, trigger=di_and_si_triggers)

        #eff_dict_trig = get_efficiencies(s, min_pt, max_pt, pt_step, trigger=single_test)
        #eff_dict_trig = get_efficiencies(s, min_pt, max_pt, pt_step, trigger=single_lepton_triggers)
        #eff_dict_trig = get_efficiencies(s, min_pt, max_pt, pt_step, trigger=dilepton_triggers)
        #eff_dict_trig = get_efficiencies(s, min_pt, max_pt, pt_step, trigger=di_or_si_triggers)
        #eff_dict_trig = get_efficiencies(s, min_pt, max_pt, pt_step, trigger=di_and_si_triggers)

        #for key in eff_dict_none.keys() :
        #    print "%s : %.2f"%(key, float(eff_dict_trig[key])/float(eff_dict_none[key]))


        #make_eff(eff_dict_none, eff_dict_trig, nice_names[trig_type], s)
        make_eff_2d(eff_dict_none, eff_dict_trig, pt_cuts, trig_type, nice_names[trig_type], s)


def main() :

    parser = OptionParser()
    parser.add_option("-t","--type", default="dilepton")
    (options, args) = parser.parse_args()
    trig_type = options.type

    valid_types = ["dilepton", "single", "di-or-si", "di-and-si"]
    if trig_type not in valid_types :
        print "Trigger type '%s' not valid!"%trig_type 
        sys.exit()
    
    
    
    lumi_weight = 40.0
    hh = Sample(hh_file, "hh", "HH", 2, True, lumi_weight)
    x1000 = Sample(x1000_file, "x1000", "X (1 TeV)", 3, True, lumi_weight)
    
    samples = [hh, x1000]
    
    make_trig_eff_plots(samples, trig_type)

#__________________________________________________________
if __name__ == "__main__" :
    main()
