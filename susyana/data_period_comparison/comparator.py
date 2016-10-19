#!/usr/bin/env python

from optparse import OptionParser
import os

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(False)

import sys
sys.path.append(os.environ['SUSYDIR'])

import glob

r.TH1F.__init__._creates = False


import supersusy.utils.plot_utils as pu
import supersusy.utils.utils as utils
import supersusy.utils.background as background
import supersusy.utils.region as region
import supersusy.utils.plot as plot


class DataSample :
    def __init__(self, name_ = "", txtfilename_ = "") :
        self.name = name_
        self.displayname = ""
        self.txtfilename = txtfilename_
        self.tree = None

        self.color = None

        self.runs = []
        self.run_min = -1
        self.run_max = -1

    def Print(self) :
        print "DataSample %s"%self.name
        for r in self.runs :
            print "   > %s"%str(r)

    def load_chain(self, file_dir = "") :
        runs = []
        lines = open(self.txtfilename).readlines()
        for line in lines :
            if not line : continue
            line = line.strip()
            runs.append(int(line))

        runs = sorted(runs)
        self.runs = runs
        self.run_min = min(runs)
        self.run_max = max(runs)

        if not file_dir.endswith("/") :
            file_dir = file_dir + "/"
        files = glob.glob(file_dir + "CENTRAL*.root")
        files_runs = []
        for run in runs :
            for f in files :
                if str(run) in f :
                    files_runs.append(f)
                    break

        chain = r.TChain("superNt")
        for f in files_runs :
            chain.Add(f)
        self.tree = chain

def get_lists() :
    out = {}

    colors = [38, 46, 30, 9, 2]

    dir_2015 = "/data/uclhc/uci/user/dantrim/ntuples/n0228/a_sep21/data15/Raw/"
    dir_2016_preIchep = "/data/uclhc/uci/user/dantrim/ntuples/n0228/a_sep21/data16/Raw/"
    dir_2016_postIchep = "/data/uclhc/uci/user/dantrim/ntuples/n0228/a_sep21/data16/Raw/"
    dir_allIchep = "/data/uclhc/uci/user/dantrim/ntuples/n0228/a_sep21/all_data/"
    dir_allRuns = "/data/uclhc/uci/user/dantrim/ntuples/n0228/a_sep21/all_data/"

    list_2015 = "runs_2015.txt" 
    list_2016_preIchep = "runs_2016ichep.txt"
    list_2016_postIchep = "runs_2016postichep.txt"
    list_allIchep = "runs_ichep.txt"
    list_allRuns = "runs_all.txt"

    out["2015"] = { "list" : list_2015, "dir" : dir_2015, "color" : colors[0], "nice" : "2015" }
    out["2016pre"] = { "list" : list_2016_preIchep, "dir" : dir_2016_preIchep, "color" : colors[1], "nice" : "2016 (ICHEP)" }
    out["2016post"] = { "list" : list_2016_postIchep, "dir" : dir_2016_postIchep, "color" : colors[2], "nice" : "2016 (post-ICHEP)" }
    out["allIchep"] = { "list" : list_allIchep, "dir" : dir_allIchep, "color" : colors[3], "nice" : "2015+2016 (ICHEP)" }
    out["allRuns"] = { "list" : list_allRuns, "dir" : dir_allRuns, "color" : colors[4], "nice" : "2015+2016" }

    return out

def order_samples(samples) :
    out = []

    order = ["2015", "2016pre", "allIchep", "2016post", "allRuns"]
    for x in order :
        for s in samples :
            if x in s.name :
                out.append(s)
    return out

def get_plots() :
    plots = []

    vars = {}
    vars["nVtx"] = [1, 0, 30]
    vars["avgMu"] = [1, 5, 40]
    vars["met"] = [20, 0, 400]
    vars["mt2"] = [10, 0, 250]
    vars["l_pt[0]"] = [20, 0, 400]
    vars["l_pt[1]"] = [20, 0, 400]
    vars["j_pt[0]"] = [20, 0, 400]
    vars["j_pt[1]" ] = [20, 0, 400]


    nice_names = {}
    nice_names["nVtx"] = "Number of primary vertices"
    nice_names["avgMu"] = "<#mu>"
    nice_names["met"] = "Missing Transverse Momentum [GeV]"
    nice_names["mt2"] = "m_{t2} [GeV]"
    nice_names["l_pt[0]"] = "Leading lepton p_{T} [GeV]"
    nice_names["l_pt[1]"] = "Sub-leading lepton p_{T} [GeV]"
    nice_names["j_pt[0]"] = "Leading jet p_{T} [GeV]"
    nice_names["j_pt[1]"] = "Sub-leading jet p_{T} [GeV]"

    for var, bounds in vars.iteritems() :
        p = plot.Plot1D()
        name_ = ""
        if "abs(" in var :
            name_ = var.replace("abs(","")
            name_ = name_.replace(")","")
        else :
            name_ = var
        p.initialize("data_comp", var, "data_comp_%s"%name_)
        p.labels(x=nice_names[var], y = "Arb. Units")
        p.xax(bounds[0], bounds[1], bounds[2])
        
        p.setDefaultCanvas(p.name)
        plots.append(p)

    return plots

def make_plot(samples, plot, region) :

    c = plot.canvas
    c.cd()
    c.SetFrameFillColor(0)
    c.SetFillColor(0)
    c.SetLeftMargin(0.14)
    c.SetRightMargin(0.05)
    c.SetBottomMargin(1.3*c.GetBottomMargin())
    c.Update()

    r.gPad.SetGrid()

    #prepare legend
    leg = pu.default_legend(xl=0.6, yl=0.69, xh=0.97, yh=0.88)

    histos = []
    for sample in samples :
        print "\t> %s"%sample.name
        hist_name = ""
        if "abs" in plot.variable :
            replace_var = plot.variable.replace("abs(","")
            replace_var = replace_var.replace(")","")
            hist_name = replace_var
        else :
            hist_name = plot.variable

        h = pu.th1f("h_"+sample.name+"_"+hist_name,"",int(plot.nbins), plot.x_range_min, plot.x_range_max, plot.x_label, plot.y_label)
        h.SetLineColor(sample.color)
        if "allIchep" in sample.name or "allRuns" in sample.name :
            h.SetLineStyle(1)
        else :
            h.SetLineStyle(2)
        h.SetFillStyle(0)
        h.SetLineWidth(3)
        h.GetYaxis().SetTitleOffset(1.17*h.GetYaxis().GetTitleOffset())
        h.Sumw2

        sel = r.TCut("1")
        cut = region.tcut
        cut = r.TCut(cut)
        cmd = "%s>>%s"%(plot.variable, h.GetName()) 
        sample.tree.Draw(cmd, cut*sel, "goff")

        #normalize
        h.Scale(1/h.Integral())

        #add overflow
        pu.add_overflow_to_lastbin(h)

        leg.AddEntry(h, sample.displayname, "l")
        histos.append(h)
        c.Update()

    is_first = True
    for h in histos :
        if is_first :
            h.Draw("hist")
            is_first = False
        else :
            h.Draw("hist same")

    leg.Draw()

    c.Update()


    outname = plot.name + ".eps"
    c.SaveAs(outname)
    out = "./plots/"
    utils.mv_file_to_dir(outname, out, True)
    fullname = out + "/" + outname
    print "%s saved to : %s"%(outname, os.path.abspath(fullname))


def set_eventlists(samples, region) :
    cut = reg.tcut
    cut = r.TCut(cut)
    sel = r.TCut("1")

    for sample in samples :
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
    

    

    

#######################################################################
if __name__=="__main__" :

    lists = get_lists()

    samples = []
    for x in lists :
        s = DataSample(x, lists[x]["list"])
        s.load_chain(lists[x]["dir"])
        s.color = lists[x]["color"]
        s.displayname = lists[x]["nice"]
        samples.append(s)
    samples = order_samples(samples)

    plots = get_plots()

    reg = region.Region()
    reg.name = "data_comp"
    reg.displayname = "Preselection"
    isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<0"
    reg.tcut = "nLeptons==2 && " + isDFOS + " && mll>20" 

    set_eventlists(samples, reg)

    for p in plots :
        print "Plotting %s"%p.variable
        make_plot(samples, p, reg)
        

    

    


    
