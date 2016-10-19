#!/usr/bin/env python

from optparse import OptionParser
import os

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(False)
r.gROOT.ProcessLine("gErrorIgnoreLevel=3001;") # ignore ROOT info messages

import sys
sys.path.append(os.environ['SUSYDIR'])

import glob

import supersusy.utils.plot_utils as pu
import supersusy.utils.utils as utils
import supersusy.utils.region as region
import supersusy.utils.plot as plot

class Sample :
    def __init__(self, name_="", displayname_="") :
        self.name = name_
        self.displayname = displayname_
        self.tree = None

        self.color = None

    def load_chain(self, file_="") :
        chain = r.TChain("superNt")
        chain.Add(file_)
        self.tree = chain

class Variable :
    def __init__(self, name_="", nicename_="", gev_=False, bounds_=None) :
        self.name = name_
        self.nice_name = nicename_
        if(gev_) :
            self.nice_name = self.nice_name + " [GeV]"
        self.bounds = bounds_

def set_eventlists(sample, region) :
    cut = reg.tcut
    cut = r.TCut(cut)
    sel = r.TCut("1")

    list_name = "list_" + region.name + "_" + sample.name
    save_name = "./lists/" + list_name + ".root"
    print "EventList %s"%list_name
    if os.path.isfile(save_name) :
        rfile = r.TFile.Open(save_name)
        list = rfile.Get(list_name)
        print "%s : EventList found at %s"%(sample.name, os.path.abspath(save_name))
        sample.tree.SetEventList(list)
    else :
        draw_list = ">> " + list_name
        sample.tree.Draw(draw_list, sel*cut)
        list = r.gROOT.FindObject(list_name)
        sample.tree.SetEventList(list)
        list.SaveAs(save_name)

def get_variables() :
    out = []

    names = []
    names += ["mt2"]
    names += ["met"]
    names += ["meff"]
    names += ["bj_pt[0]"]
    names += ["bj_pt[1]"]
    names += ["bj_pt[2]"]
    names += ["sj_pt[0]"]
    names += ["sj_pt[1]"]
    names += ["sj_pt[2]"]
    names += ["nBJets"]
    names += ["nSJets"]
    names += ["nJets"]
    names += ["bj_eta[0]"]
    names += ["bj_eta[1]"]
    names += ["pTll"]
    names += ["dphi_ll"]
    names += ["l_pt[0]"]
    names += ["l_pt[1]"]


    nice_names = {}
    nice_names["mt2"]  = "m_{t2}"
    nice_names["met"]  = "Missing E_{T}"
    nice_names["meff"]  = "m_{eff}"
    nice_names["bj_pt[0]"] = "Lead b-jet p_{T}"
    nice_names["bj_pt[1]"] = "2nd b-jet p_{T}"
    nice_names["bj_pt[2]"] = "3rd b-jet p_{T}"
    nice_names["sj_pt[0]"] = "Lead signal, non b-jet p_{T}"
    nice_names["sj_pt[1]"] = "2nd signal, non b-jet p_{T}"
    nice_names["sj_pt[2]"] = "3rd signal, non b-jet p_{T}"
    nice_names["nBJets"] = "b-tagged jet multiplicity"
    nice_names["nSJets"] = "non-b, signal jet multiplicity"
    nice_names["nJets"] = "signal jet multiplicity"
    nice_names["bj_eta[0]"] = "Lead b-jet #eta"
    nice_names["bj_eta[1]"] = "2nd b-jet #eta"
    nice_names["pTll"] = "Dilepton Transverse Momentum"
    nice_names["dphi_ll"] = "#Delta#phi_{ll}"
    nice_names["l_pt[0]"] = "Lead lepton p_{T}"
    nice_names["l_pt[1]"] = "Sub-lead lepton p_{T}"

    do_gev = {}
    do_gev["mt2"] = True
    do_gev["met"] = True
    do_gev["meff"] = True
    do_gev["bj_pt[0]"] = True
    do_gev["bj_pt[1]"] = True
    do_gev["bj_pt[2]"] = True
    do_gev["sj_pt[0]"] = True
    do_gev["sj_pt[1]"] = True
    do_gev["sj_pt[2]"] = True
    do_gev["nBJets"] = False
    do_gev["nSJets"] = False
    do_gev["nJets"] = False
    do_gev["bj_eta[0]"] = False
    do_gev["bj_eta[1]"] = False
    do_gev["pTll"] = True
    do_gev["dphi_ll"] = False
    do_gev["l_pt[0]"] = True
    do_gev["l_pt[1]"] = True

    bounds = {}
    bounds["mt2"]      = { "test" : [10, 0, 250, 1e9] }
    bounds["met"]      = { "test" : [10, 0, 300, 1e9] }
    bounds["meff"]      = { "test" : [80, 0, 2000, 1e9] }
    bounds["bj_pt[0]"] = { "test" : [10, 0, 300, 1e9] }
    bounds["bj_pt[1]"] = { "test" : [10, 0, 250, 1e9] }
    bounds["bj_pt[2]"] = { "test" : [10, 0, 250, 1e9] }
    bounds["sj_pt[0]"] = { "test" : [10, 0, 300, 1e9] }
    bounds["sj_pt[1]"] = { "test" : [10, 0, 250, 1e9] }
    bounds["sj_pt[2]"] = { "test" : [10, 0, 250, 1e9] }
    bounds["nBJets"] =   { "test" : [1, 0, 7, 1e9] }
    bounds["nSJets"] =   { "test" : [1, 0, 10, 1e9] }
    bounds["nJets"] =    { "test" : [1, 0, 15, 1e9] }
    bounds["bj_eta[0]"]= { "test" : [0.2, -2.5, 2.5, 1e9] }
    bounds["bj_eta[1]"]= { "test" : [0.2, -2.5, 2.5, 1e9] }
    bounds["pTll"] =     { "test" : [10, 0, 300, 1e9] }
    bounds["dphi_ll"] =  { "test" : [0.2, -3, 3, 1e9] }
    bounds["l_pt[0]"] =  { "test" : [10, 0, 250, 1e9] }
    bounds["l_pt[1]"] =  { "test" : [10, 0, 200, 1e9] }

    for var in names :
        if "sj_pt" not in var : continue
        v = Variable(var, nice_names[var], do_gev[var], bounds[var])
        out.append(v)

    return out

def make_ttbar_comp_plots(var, region, samples) :
    print 50*"-"
    print "Making ttbar comparison plots, variable: %s"%var.name


    p = plot.Plot1D()
    p.initialize("%s"%str(region.name), var.name, "ttbar_comp_%s_%s"%(region.name, var.name))
    p.labels(x=var.nice_name, y = "Arb. Units")
    p.xax(var.bounds[reg.name][0], var.bounds[reg.name][1], var.bounds[reg.name][2])
    p.yax(0.1, var.bounds[reg.name][3])
    p.doLogY = True
    p.setRatioCanvas(p.name)

    # canvas
    rcan = p.ratioCanvas
    rcan.canvas.cd()
    rcan.upper_pad.cd()

    if p.isLog() : rcan.upper_pad.SetLogy(True)
    rcan.upper_pad.Update()

    # axes
    hax = r.TH1F("axis", "", int(p.nbins), p.x_range_min, p.x_range_max)
    hax.SetMinimum(p.y_range_min)
    hax.SetMaximum(10000)
    hax.GetXaxis().SetTitle(var.nice_name)
    hax.GetXaxis().SetTitleFont(42)
    hax.GetXaxis().SetLabelFont(42)
    hax.GetXaxis().SetLabelSize(0.035)
    hax.GetXaxis().SetTitleOffset(-999)

    hax.GetYaxis().SetTitle(p.y_label)
    hax.GetYaxis().SetTitleFont(42)
    hax.GetYaxis().SetLabelFont(42)
    hax.GetYaxis().SetTitleOffset(1.4)
    hax.GetYaxis().SetLabelOffset(0.013)
    hax.GetYaxis().SetLabelSize(1.2 * 0.035)
    hax.GetYaxis().SetTitleSize(0.055 * 0.85)
    hax.Draw()
    rcan.upper_pad.Update()

    # legend
    leg = pu.default_legend(xl=0.55, yl=0.71, xh=0.93, yh=0.90)

    # histos
    histos_tmp = {}
    display_names = {}
    samples_for_order = ["nominal", "sherpa", "mgp"]
    colors = {}
    for s in samples :
        h = pu.th1f("h_" + var.name + "_" + str(s.name), "", int(p.nbins), p.x_range_min, p.x_range_max, p.x_label, p.y_label)
        h.SetLineColor(s.color)
        h.SetFillStyle(0)
        h.SetLineWidth(2)
        h.GetXaxis().SetLabelOffset(-999)
        h.SetMaximum(10000)
        h.Sumw2

        display_names[s.name] = s.displayname
        colors[s.name] = s.color

        lumi_scale = 8.42 # not neeed for normalized distributions
        weight_str = "eventweight * %s"%lumi_scale

        cut = "(" + region.tcut + ") * %s"%weight_str
        cut = r.TCut(cut)
        sel = r.TCut("1")
        cmd = "%s>>+%s"%(var.name, h.GetName())
        s.tree.Draw(cmd, cut * sel, "goff") 

        #print yield stuffs
        stat_err = r.Double(0.0)
        integral = h.IntegralAndError(0,-1,stat_err)
        print "%s : %.2f +/- %.2f"%(s.name, integral, stat_err) 


        # add overflow
        pu.add_overflow_to_lastbin(h)

        # norm to unity
        h.Scale(1/h.Integral())

        histos_tmp[s.name] = h
        rcan.upper_pad.Update()

    r.gPad.SetGrid()

    histos = {}
    for sname in samples_for_order :
        for sn, hist in histos_tmp.iteritems() :
            if sn == sname :
                histos[sname] = hist 
                leg.AddEntry(hist, display_names[sname], "l")

    histos["nominal"].Draw("hist")
    histos["sherpa"].Draw("hist same")
    histos["mgp"].Draw("hist same")

    # draw the legend
    leg.Draw()


    ############### lower pad
    rcan.lower_pad.cd()

    # nom
    h_nom = histos["nominal"].Clone("nominal")
    # sherpa
    h_sherpa = histos["sherpa"].Clone("sherpa")
    # mgpythia
    h_mgp = histos["mgp"].Clone("mgp")

    # y-axis
    yax = h_sherpa.GetYaxis()
    yax.SetTitle("Other/Nominal")
    yax.SetTitleSize(0.1 * 0.83)
    yax.SetLabelSize(0.1 * 0.81)
    yax.SetLabelOffset(0.98 * 0.013 * 1.08)
    yax.SetTitleOffset(0.45 * 1.2)
    yax.SetLabelFont(42)
    yax.SetTitleFont(42)
    yax.SetNdivisions(5)

    # x-axis
    xax = h_sherpa.GetXaxis()
    xax.SetTitleSize(1.0 * 0.14)
    xax.SetLabelSize(yax.GetLabelSize())
    xax.SetLabelOffset(1.15 * 0.02)
    xax.SetTitleOffset(0.85 * xax.GetTitleOffset())
    xax.SetLabelFont(42)
    xax.SetTitleFont(42)

    h_nom.GetYaxis().SetRangeUser(0,5)
    h_sherpa.GetYaxis().SetRangeUser(0,5)
    h_mgp.GetYaxis().SetRangeUser(0,5)
    h_nom.SetNdivisions(5)
    h_sherpa.SetNdivisions(5)
    h_mgp.SetNdivisions(5)

    h_sherpa.Divide(h_nom)
    h_mgp.Divide(h_nom)

    maxy_ = 5
    if "bj_pt[0]" in var.name or "bj_pt[1]" in var.name:
        maxy_ = 2
    elif "bj_pt[2]" in var.name :
        maxy_ = 3
    elif "nBJets" in var.name :
        maxy_ = 2
    elif "nSJets" in var.name :
        maxy_ = 3
    elif "eta" in var.name :
        maxy_ = 2
    elif "dphi_ll" in var.name or "pTll" in var.name :
        maxy_ = 2
    elif "l_pt" in var.name :
        maxy_ = 2
    elif "meff" in var.name or "met" in var.name :
        maxy_ = 2
    elif "sj_pt" in var.name :
        maxy_ = 2

    h_sherpa.GetYaxis().SetRangeUser(0,maxy_)
    h_mgp.GetYaxis().SetRangeUser(0,maxy_)

    h_sherpa.SetMarkerStyle(20)
    h_sherpa.SetMarkerColor(colors["sherpa"])
    h_mgp.SetMarkerStyle(20)
    h_mgp.SetMarkerColor(colors["mgp"])

    h_sherpa.Draw("pe")
    h_mgp.Draw("pe same")

    rcan.lower_pad.Update()

    # lines
    pu.draw_line(p.x_range_min, 1.0, p.x_range_max, 1.0, color=r.kRed, style=2, width=1)


    # save
    outname = p.name + ".eps"
    rcan.canvas.SaveAs(outname)
    out = "./ttbar_comp_plots/"
    utils.mv_file_to_dir(outname, out, True)
    fullname = out + "/" + outname
    print "%s saved to : %s"%(outname, os.path.abspath(fullname))




#############################################################################
if __name__=="__main__" :

    # nominal ttbar sample
    file_nominal = "/data/uclhc/uci/user/dantrim/ntuples/n0228/a_sep21/mc/Raw/CENTRAL_410009.root"
    # sherpa 2.2.1 ttbar (dilepton) sample
    file_sherpa = "/data/uclhc/uci/user/dantrim/ntuples/n0228/e_oct19/mc/Raw/ttbar_dilepton_sherpa221_410252.root"
    # MGPythia + up to 2 jets
    file_mgp = "/data/uclhc/uci/user/dantrim/ntuples/n0228/e_oct19/mc/Raw/ttbar_mgp_407.root"
    

    nom_sample = Sample("nominal", "Nominal (410009)")
    nom_sample.load_chain(file_nominal)
    nom_sample.color = 12

    sherpa_sample = Sample("sherpa", "Sherpa 2.2.1 (DiLepton)")
    sherpa_sample.load_chain(file_sherpa)
    sherpa_sample.color = 46

    mgp_sample = Sample("mgp", "MGPythia")
    mgp_sample.load_chain(file_mgp)
    mgp_sample.color = 38

    samples = [nom_sample, sherpa_sample, mgp_sample]

    print "Loaded ttbar samples:"
    for s in samples :
        print "  >  %s  [%d entries]"%(s.name, s.tree.GetEntries())

    reg = region.Region()
    reg.name = "test"
    reg.displayname = "Stop-2L (Super-Razor) test"
    isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<0"
    reg.tcut = isDFOS + " && nBJets>=1 && nJets>2  && mll>20"
    #reg.tcut = "nLeptons==2 && " + isDFOS + " && nBJets>0 && MDR>80 && RPT>0.5 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && mll>20"

    for s in samples :
        set_eventlists(s, reg)

    variables_to_plot = get_variables()

    for v in variables_to_plot :
        make_ttbar_comp_plots(v, reg, samples)
