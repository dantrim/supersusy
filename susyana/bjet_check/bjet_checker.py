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
    def __init__(self, name_ = "", displayname_ = "") :
        self.name = name_
        self.displayname = displayname_
        self.tree = None

        self.color = None

    def load_chain(self, file = "") :
        chain = r.TChain("superNt")
        chain.Add(file)
        self.tree = chain

def set_eventlists(sample, region) :
    cut = reg.tcut
    cut = r.TCut(cut)
    sel = r.TCut("1")

    list_name = "list_" + region.name + "_" + sample.name
    save_name = "./lists/" + list_name + ".root"
    print "EvnetList %s"%list_name
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


#########################################################################
def make_wp_comparison_plot(variable, sample, reg) :

    print 50*"-"
    print "Plotting WP comparison : %s"%variable


    nice_names = {}
    nice_names["bjets_n"] = "b-jet Multiplicity"
    nice_names["sjets_n"] = "Non b-tagged jet Multiplicity"
    nice_names["bjets_pt0"] = "Lead b-jet p_{T} [GeV]"
    nice_names["bjets_pt1"] = "2nd b-jet p_{T} [GeV]"
    nice_names["bjets_pt2"] = "3rd b-jet p_{T} [GeV]"
    nice_names["bjets_pt3"] = "4th b-jet p_{T} [GeV]"
    nice_names["bjets_nTrk0"] = "Lead b-jet # tracks"
    nice_names["bjets_nTrk1"] = "2nd b-jet # tracks"
    nice_names["bjets_nTrk2"] = "3rd b-jet # tracks"
    nice_names["bjets_nTrk3"] = "4th b-jet # Ttracks"
    nice_names["bjets_jvt0"] = "Lead b-jet JVT"
    nice_names["bjets_jvt1"] = "2nd b-jet JVT"
    nice_names["bjets_jvt2"] = "3rd b-jet JVT"
    nice_names["bjets_jvt3"] = "4th b-jet JVT"
    nice_names["bjets_eta0"] = "Lead b-jet #eta"
    nice_names["bjets_eta1"] = "2nd b-jet #eta"
    nice_names["bjets_eta2"] = "3rd b-jet #eta"
    nice_names["bjets_eta3"] = "4th b-jet #eta"
    nice_names["mt2"] = "m_{t2} [GeV]"
    nice_names["MDR"] = "M_{#Delta}^{R} [GeV]"
    nice_names["DPB_vSS"] = "#Delta#phi_{#beta}^{R}"

    bounds = {}
    bounds["bjets_n"] = [1,0,10,1e9]
    bounds["sjets_n"] = [1,0,10,1e9]
    bounds["bjets_pt0"] = [10, 0, 350,1e9]
    bounds["bjets_pt1"] = [10, 0, 350,1e9]
    bounds["bjets_pt2"] = [10, 0, 200,1e9]
    bounds["bjets_pt3"] = [10, 0, 200,1e9]
    bounds["bjets_nTrk0"] = [1, 0, 30, 1e9]
    bounds["bjets_nTrk1"] = [1, 0, 30, 1e9]
    bounds["bjets_nTrk2"] = [1, 0, 30, 1e9]
    bounds["bjets_nTrk3"] = [1, 0, 30, 1e9]
    bounds["bjets_jvt0"] = [0.02, 0, 1, 1e9]
    bounds["bjets_jvt1"] = [0.02, 0, 1, 1e9]
    bounds["bjets_jvt2"] = [0.02, 0, 1, 1e9]
    bounds["bjets_jvt3"] = [0.02, 0, 1, 1e9]
    bounds["bjets_eta0"] = [0.2, -3, 3, 1e9]
    bounds["bjets_eta1"] = [0.2, -3, 3, 1e9]
    bounds["bjets_eta2"] = [0.2, -3, 3, 1e9]
    bounds["bjets_eta3"] = [0.2, -3, 3, 1e9]
    bounds["mt2"] = [10, 0, 300, 1e9]
    bounds["MDR"] = [10, 0, 300, 1e9]
    bounds["DPB_vSS"] = [0.1, 0, 3.2, 1e9]

    variables = {}
    variables["bjets_n"] =     { 70 : "nBJets70", 77 : "nBJets", 85 : "nBJets85" , 0 : "nBJetsMatched"}
    variables["sjets_n"] =     { 70 : "nSJets70", 77 : "nSJets", 85 : "nSJets85" , 0 : "nSJetsMatched"}
    variables["bjets_pt0"] =   { 70 : "bj70_pt[0]", 77 : "bj_pt[0]", 85 : "bj85_pt[0]", 0 : "bjMatched_pt[0]"}
    variables["bjets_pt1"] =   { 70 : "bj70_pt[1]", 77 : "bj_pt[1]", 85 : "bj85_pt[1]", 0 : "bjMatched_pt[1]" }
    variables["bjets_pt2"] =   { 70 : "bj70_pt[2]", 77 : "bj_pt[2]", 85 : "bj85_pt[2]", 0 : "bjMatched_pt[2]" }
    variables["bjets_pt3"] =   { 70 : "bj70_pt[3]", 77 : "bj_pt[3]", 85 : "bj85_pt[3]", 0 : "bjMatched_pt[3]" }
    variables["bjets_nTrk0"] = { 70 : "bj70_nTrk[0]", 77 : "bj_nTrk[0]", 85 : "bj85_nTrk[0]", 0 : "bjMatched_nTrk[0]" }
    variables["bjets_nTrk1"] = { 70 : "bj70_nTrk[1]", 77 : "bj_nTrk[1]", 85 : "bj85_nTrk[1]", 0 : "bjMatched_nTrk[1]" }
    variables["bjets_nTrk2"] = { 70 : "bj70_nTrk[2]", 77 : "bj_nTrk[2]", 85 : "bj85_nTrk[2]", 0 : "bjMatched_nTrk[2]" }
    variables["bjets_nTrk3"] = { 70 : "bj70_nTrk[3]", 77 : "bj_nTrk[3]", 85 : "bj85_nTrk[3]", 0 : "bjMatched_nTrk[3]" }
    variables["bjets_jvt0"] =  { 70 : "bj70_jvt[0]", 77 : "bj_jvt[0]", 85 : "bj85_jvt[0]" , 0 : "bjMatched_jvt[0]"}
    variables["bjets_jvt1"] =  { 70 : "bj70_jvt[1]", 77 : "bj_jvt[1]", 85 : "bj85_jvt[1]" , 0 : "bjMatched_jvt[1]"}
    variables["bjets_jvt2"] =  { 70 : "bj70_jvt[2]", 77 : "bj_jvt[2]", 85 : "bj85_jvt[2]" , 0 : "bjMatched_jvt[2]"}
    variables["bjets_jvt3"] =  { 70 : "bj70_jvt[3]", 77 : "bj_jvt[3]", 85 : "bj85_jvt[3]" , 0 : "bjMatched_jvt[3]"}
    variables["bjets_eta0"] =  { 70 : "bj70_eta[0]", 77 : "bj_eta[0]", 85 : "bj85_eta[0]", 0 : "bjMatched_eta[0]" }
    variables["bjets_eta1"] =  { 70 : "bj70_eta[1]", 77 : "bj_eta[1]", 85 : "bj85_eta[1]", 0 : "bjMatched_eta[1]" }
    variables["bjets_eta2"] =  { 70 : "bj70_eta[2]", 77 : "bj_eta[2]", 85 : "bj85_eta[2]", 0 : "bjMatched_eta[2]" }
    variables["bjets_eta3"] =  { 70 : "bj70_eta[3]", 77 : "bj_eta[3]", 85 : "bj85_eta[3]", 0 : "bjMatched_eta[3]" }
    variables["mt2"] = { 70 : "mt2", 77 : "mt2", 85 : "mt2", 0 : "mt2" }
    variables["MDR"] = { 70 : "MDR", 77 : "MDR", 85 : "MDR", 0 : "MDR" }
    variables["DPB_vSS"] = { 70 : "DPB_vSS", 77 : "DPB_vSS", 85 : "DPB_vSS", 0 : "DPB_vSS" }

    colors = {}
    colors[70] = 30
    colors[77] = 38
    colors[85] = 46
    colors[0] = r.kBlack

    
    p = plot.Plot1D()
    p.initialize("%s"%str(reg.name), variable, "wp_comp_%s_%s"%(reg.name, variable))
    p.labels(x=nice_names[variable], y = "Events")
    p.xax(bounds[variable][0], bounds[variable][1], bounds[variable][2])
    p.yax(0.1, bounds[variable][3])
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
    hax.SetMaximum(1e9)
    hax.GetXaxis().SetTitle(p.x_label)
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

    # hists for different WP
    histos = {}

    working_points = [70, 77, 85, 0]
    for wp in working_points :
        if ("data" in sample.name or "run" in sample.name) and wp==0 : continue
        h = pu.th1f("h_" + variable + "_" + str(wp), "", int(p.nbins), p.x_range_min, p.x_range_max, p.x_label, p.y_label)
        h.SetLineColor(colors[wp])
        if wp == 0 :
            h.SetLineStyle(2)
        h.SetFillStyle(0)
        h.SetLineWidth(2)
        h.GetXaxis().SetLabelOffset(-999)
        h.SetMaximum(1e9)
        h.Sumw2

        weight_str = "eventweight"
        cut = ""

        if wp == 70 :
            reg.tcut += " && nBJets70>0"
        elif wp == 77 :
            reg.tcut += " && nBJets>0"
        elif wp == 85 :
            reg.tcut += " && nBJets85>0"
        elif wp == 0 :
            reg.tcut += " && nBJetsMatched>0"

        if "data" not in sample.name or "run" not in sample.name :
            cut = "(" + reg.tcut + ") * %s * %s"%(weight_str, str(8.42))
        else :
            cut = "(" + reg.tcut + ")"
        cut = r.TCut(cut)
        sel = r.TCut("1")
        cmd = "%s>>+%s"%(variables[variable][wp], h.GetName()) 
        sample.tree.Draw(cmd, cut * sel, "goff")

        # print the yield +/- stat error

        stat_err = r.Double(0.0)
        integral = h.IntegralAndError(0,-1, stat_err)
        print "%s : %.2f +/- %.2f"%(str(wp), integral, stat_err)

        # add overflow
        pu.add_overflow_to_lastbin(h)

        if wp != 0 :
            leg.AddEntry(h, "%s %s%% MV2c10 WP"%(sample.displayname, str(wp)), "l")
        elif wp==0 and ("data" not in sample.name or "run" not in sample.name) :
            leg.AddEntry(h, "%s 77%% MV2c10 + Truth Match"%sample.displayname, "l")

        histos[wp] = h
        rcan.upper_pad.Update()

     
    r.gPad.SetGrid()
    histos[70].Draw("hist")
    histos[77].Draw("hist same")
    histos[85].Draw("hist same")
    if len(histos)==4 :
        histos[0].Draw("hist same")
    rcan.upper_pad.Update()

    #draw the legend
    leg.Draw()

    # text
    pu.draw_text(text="ATLAS", x=0.18, y =0.85, size=0.06, font=72) 
    pu.draw_text(text="Internal", x=0.325, y =0.85, size =0.06, font=42)
    if not ("run" in sample.name.lower() or "data" in sample.name.lower()) :
        pu.draw_text(text="L = ~27 fb^{-1}, #sqrt{s} = 13 TeV", x=0.18, y=0.79, size=0.04)
    else :
        pu.draw_text(text="L = ~200 pb^{-1}, #sqrt{s} = 13 TeV", x=0.18, y =0.79, size=0.04)
    pu.draw_text(text=reg.displayname, x=0.18, y=0.74, size=0.04)


    r.gPad.SetTickx()
    r.gPad.SetTicky()


    ######## Lower Pad
    rcan.lower_pad.cd()

    #h_den = histos[77].Clone("h_den")

    ## y-axis
    #yax = h_den.GetYaxis()
    #yax.SetRangeUser(0,2)
    #yax.SetTitle("WP X / WP 77%")
    #yax.SetTitleSize(0.1 * 0.83)
    #yax.SetLabelSize(0.1 * 0.81)
    #yax.SetLabelOffset(0.98 * 0.013 * 1.08)
    #yax.SetTitleOffset(0.45*1.2)
    #yax.SetLabelFont(42)
    #yax.SetTitleFont(42)
    #yax.SetNdivisions(5)

    ## x-axis
    #xax = h_den.GetXaxis()
    #xax.SetTitleSize(1.1 * 0.14)
    #xax.SetLabelSize(yax.GetLabelSize())
    #xax.SetLabelOffset(1.15*0.02)
    #xax.SetTitleOffset(0.85*xax.GetTitleOffset())
    #xax.SetLabelFont(42)
    #xax.SetTitleFont(42)

    #h_den.SetTickLength(0.06)
    #h_den.Draw("axis")
    #rcan.lower_pad.Update()


    # 70
    h_70 = histos[70].Clone("h70")
    # y-axis
    yax = h_70.GetYaxis()
    #yax.SetRangeUser(0,2)
    yax.SetTitle("WP X / WP 77%")
    yax.SetTitleSize(0.1 * 0.83)
    yax.SetLabelSize(0.1 * 0.81)
    yax.SetLabelOffset(0.98 * 0.013 * 1.08)
    yax.SetTitleOffset(0.45*1.2)
    yax.SetLabelFont(42)
    yax.SetTitleFont(42)
    yax.SetNdivisions(5)

    # x-axis
    xax = h_70.GetXaxis()
    xax.SetTitleSize(1.0 * 0.14)
    xax.SetLabelSize(yax.GetLabelSize())
    xax.SetLabelOffset(1.15*0.02)
    xax.SetTitleOffset(0.85*xax.GetTitleOffset())
    xax.SetLabelFont(42)
    xax.SetTitleFont(42)


    h_77 = histos[77].Clone("h77")
    h_85 = histos[85].Clone("h85")

    h_70.GetYaxis().SetRangeUser(0,5)
    h_77.GetYaxis().SetRangeUser(0,5)
    h_85.GetYaxis().SetRangeUser(0,5)
    h_70.SetNdivisions(5)
    h_77.SetNdivisions(5)
    h_85.SetNdivisions(5)

    h_70.Divide(h_77)
    h_85.Divide(h_77)

    h_70.Draw("hist")
    h_85.Draw("hist same")

    if len(histos) == 4 :
        h_0 = histos[0].Clone("h0")
        h_0.GetYaxis().SetRangeUser(0,5)
        h_0.SetNdivisions(5)
        h_0.Divide(h_77)
        h_0.Draw("hist same")
    rcan.lower_pad.Update()

    # lines
    pu.draw_line(p.x_range_min, 1.0, p.x_range_max, 1.0, color=r.kRed, style=2, width=1)

    # save
    outname = p.name + "_" + sample.name + ".eps"
    rcan.canvas.SaveAs(outname)
    out = "./bjet_check_plots/"
    utils.mv_file_to_dir(outname, out, True)
    fullname = out + "/" + outname
    print "%s saved to : %s"%(outname, os.path.abspath(fullname))
        

    




##########################################################################
if __name__ == "__main__" :
    
    filename = "/data/uclhc/uci/user/dantrim/ntuples/n0228/b_oct5/mc/Raw/CENTRAL_410009.root"
    sample = Sample("ttbar", "t#bar{t}")

    #filename = "/data/uclhc/uci/user/dantrim/ntuples/n0228/b_oct5/data/Raw/CENTRAL_physics_Main_307514.root"
    #sample = Sample("run307514", "Run 307514")
    sample.load_chain(filename)
    print sample.tree.GetEntries()

    reg = region.Region()
    reg.name = "dfpreb"
    reg.displayname = "DF Preselection + >0 b-jets"
    isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<0" 
    reg.tcut = "nLeptons==2 && " + isDFOS + " && mll>20"

    set_eventlists(sample, reg)
    
    variables_to_plot = []
    #variables_to_plot+= ["bjets_n", "bjets_pt0", "bjets_pt1", "bjets_pt2", "bjets_pt3"]
    #variables_to_plot+= ["bjets_nTrk0", "bjets_nTrk1", "bjets_nTrk2", "bjets_nTrk3"]
    #variables_to_plot+= ["bjets_jvt0", "bjets_jvt1", "bjets_jvt2", "bjets_jvt3"]
    #variables_to_plot+= ["bjets_eta0", "bjets_eta1", "bjets_eta2", "bjets_eta3"]
    #variables_to_plot+= ["sjets_n"]
    variables_to_plot+= ["mt2", "MDR", "DPB_vSS"]
    
    for v in variables_to_plot :
        make_wp_comparison_plot(v, sample, reg)

