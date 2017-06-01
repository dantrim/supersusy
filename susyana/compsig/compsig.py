#!/usr/bin/env python

from optparse import OptionParser
import os

import glob

import array

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(False)
import sys
sys.path.append(os.environ['SUSYDIR'])

r.TH1F.__init__._creates = False

import supersusy.utils.plot_utils as pu
import supersusy.utils.utils as utils
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region
import supersusy.utils.plot as plot

from math import sqrt

signal_filedir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/a_jan16/mc/Raw/" 
signal_filelists = "/data/uclhc/uci/user/dantrim/n0231val/filelists/bwn/"

isSFOS = "(( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && abs(mll-91.2)>10 && (l_q[0]*l_q[1])<0)"
isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<0"
trigger = "((year==2015 && trig_pass2015==1) || (year==2016 && trig_pass2016update==1))"
regions = []

reg0 = region.Region()
reg0.name = "dfprebv"
reg0.displayname = "DF Preselection + b-veto"
reg0.tcut = "nLeptons==2 && " + isDFOS + " && nBJets==0 && mll>20 && " + trigger
regions.append(reg0)

reg1 = region.Region()
reg1.name = "dfpreb"
reg1.displayname = "DF Preselection + >0 b-jets"
reg1.tcut = "nLeptons==2 && " + isDFOS + " && nBJets>0 && mll>20  && " + trigger
regions.append(reg1)

reg2 = region.Region()
reg2.name = "sfprebv"
reg2.displayname = "SF Preselection + b-veto"
reg2.tcut = "nLeptons==2 && " + isSFOS + " && nBJets==0 && mll>20 && " + trigger
regions.append(reg2)

reg3 = region.Region()
reg3.name = "sfpreb"
reg3.displayname = "SF Preselection + >0 b-jets"
reg3.tcut = "nLeptons==2 && " + isSFOS + " && nBJets>0 && mll>20 && " + trigger
regions.append(reg3)

reg4 = region.Region()
reg4.name = "pre"
reg4.displayname = "Basic Preselection"
reg4.tcut = "nLeptons==2 && mll>20 && l_pt[0]>25 && l_pt[1]>20 &&  " + trigger
regions.append(reg4)


class Signal :
    def __init__(self, old_or_new = "") :
        self.kind = old_or_new
        self.tree = None
        self.filename = ""
        self.dsid = -1
        self.mX = -1
        self.mY = -1

    def fill(self, dsid_, mx, my) :
        self.dsid = dsid_
        self.mX = mx
        self.mY = my

    def Print(self) :
        print "Signal (%s, %s) [%s] > %s"%(self.mX, self.mY, self.dsid, self.filename)

    def set_tree(self, filename) :
        if not os.path.isfile(filename) :
            print "set_tree    ERROR Input file (%s) is not found!"%filename
            print "set_tree    ERROR  > Exiting."
            sys.exit()
        self.filename = filename
        chain = r.TChain("superNt")
        chain.Add(filename)
        self.tree = chain


def get_dsid(sample) :
    """
    looks for mc15_13TeV. and grabs the dsid after that
    """
    dsid = sample.split("mc15_13TeV.")[1]
    dsid = dsid.split(".")[0]
    return str(dsid)

def build_signals(files, old_or_new) :
    file_to_check = ""
    if old_or_new == "old" :
        file_to_check = "bwn_masses_old.txt"
    elif old_or_new == "new" :
        file_to_check = "bwn_masses_new.txt"
    else :
        print "build_signals    Unhandled input: %s, expect either 'old' or 'new'"%old_or_new
        sys.exit()

    lines = open(file_to_check).readlines()

    out_signals = []
    for line in lines :
        if not line : continue
        line = line.strip()
        if line.startswith("#") : continue
        line = line.split()
        dsid = str(line[0])
        mx = str(line[1])
        my = str(line[2])

        s = Signal(old_or_new)
        s.fill(dsid, mx, my)
        # grab the associated file
        for f in files :
            if dsid in f :
                s.set_tree(f)
                out_signals.append(s)

    return out_signals

def load_signals() :

    lists = glob.glob(signal_filelists + "*.txt")
    print len(lists)

    dsids = []
    for l in lists :
        dsids.append(str(get_dsid(l)))

    files = glob.glob(signal_filedir + "CENTRAL_*.root")
    signal_files = []
    for dsid in dsids :
        for f in files :
            if dsid in f :
                signal_files.append(f)

    old_signals = build_signals(signal_files, "old")
    new_signals = build_signals(signal_files, "new")

    return old_signals, new_signals

def look_for_signal(mx, my, signals, old_or_new) :

    found_masses = False

    list_with_mstops = []
    for s in signals :
        if str(s.mX) == str(mx) :
            list_with_mstops.append(s)

    list_with_both = []
    for s in list_with_mstops :
        if str(s.mY) == str(my) :
            list_with_both.append(s)

    if len(list_with_both) == 0 :
        found_masses = False
    elif len(list_with_both) == 1 :
        found_masses = True
    else :
        print "look_for_signals()    ERROR Found more than one signal point at (%s,%s) in %s signals"%(mx,my,old_or_new)
        found_masses = False

    return found_masses, list_with_both[0]

def make_comparison_plots(signew, sigold, reg_request) :
    print "make_comparison_plots"
    global regions

    region = None
    for reg in regions :
        if reg.name == reg_request :
            region = reg 

    print " > %s"%region.name

    # variables
    variables = []
    # basic kinematic
    variables.append("l_pt[0]")
    variables.append("l_pt[1]")
    variables.append("l_eta[0]")
    variables.append("l_eta[1]")
    variables.append("pTll")
    variables.append("met")
    variables.append("nSJets")
    variables.append("sj_pt[0]")
    variables.append("sj_pt[1]")
    variables.append("nBJets")
    variables.append("bj_pt[0]")
    variables.append("bj_pt[1]")

    # signal region variables
    variables.append("MDR")
    variables.append("DPB_vSS")
    variables.append("gamInvRp1")
    variables.append("cosThetaB")
    variables.append("RPT")


    nice_names = {}
    nice_names["l_pt[0]"] = "Lead lepton p_{T} [GeV]"
    nice_names["l_pt[1]"] = "Sub-lead lepton p_{T} [GeV]"
    nice_names["l_eta[0]"] = "Lead lepton #eta"
    nice_names["l_eta[1]"] = "Sub-lead lepton #eta"
    nice_names["pTll"] = "p_{T}^{ll} [GeV]"
    nice_names["met"] = "Missing Transverse Momentum [GeV]"
    nice_names["nSJets"] = "Number of non-b-tagged jets"
    nice_names["sj_pt[0]"] = "Lead non-b-jet p_{T} [GeV]"
    nice_names["sj_pt[1]"] = "Sub-lead non-b-jet p_{T} [GeV]"
    nice_names["nBJets"] = "Number of b-tagged jets"
    nice_names["bj_pt[0]"] = "Lead b-jet p_{T} [GeV]"
    nice_names["bj_pt[1]"] = "Sub-lead b-jet p_{T} [GeV]"
    nice_names["MDR"] = "M_{#Delta}^{R} [GeV]"
    nice_names["DPB_vSS"] = "#Delta#phi_{#beta}^{R}"
    nice_names["gamInvRp1"] = "1/#gamma_{R+1}"
    nice_names["cosThetaB"] = "cos#theta_{b}"
    nice_names["RPT"] = "R_{p_{T}}"

    bounds = {}
    bounds["l_pt[0]"] = [10, 20, 150]
    bounds["l_pt[1]"] = [10, 20, 150]
    bounds["l_eta[0]"] = [0.1,0,3]
    bounds["l_eta[1]"] = [0.1,0,3]
    bounds["pTll"] = [10,0,250]
    bounds["met"] = [10,0,350]
    bounds["nSJets"] = [1,0,15]
    bounds["sj_pt[0]"] = [10,0,250]
    bounds["sj_pt[1]"] = [10,0,200]
    bounds["nBJets"] = [1,0,10]
    bounds["bj_pt[0]"] = [10,0,250]
    bounds["bj_pt[1]"] = [10,0,250]
    bounds["MDR"] = [10,0,180]
    bounds["DPB_vSS"] = [0.1,0,3.2]
    bounds["gamInvRp1"] = [0.05,0,1]
    bounds["cosThetaB"] = [0.05,-1,1]
    bounds["RPT"] = [0.05,0,1]

    hist_names = {}
    hist_names["l_pt[0]"] = "lpt0"
    hist_names["l_pt[1]"] = "lpt1"
    hist_names["l_eta[0]"] = "leta0"
    hist_names["l_eta[1]"] = "leta1"
    hist_names["pTll"] = "pTll"
    hist_names["met"] = "met"
    hist_names["nSJets"] = "nSJets"
    hist_names["sj_pt[0]"] = "sjpt0"
    hist_names["sj_pt[1]"] = "sjpt1"
    hist_names["nBJets"] = "nBJets"
    hist_names["bj_pt[0]"] = "bjpt0"
    hist_names["bj_pt[1]"] = "bjpt1"
    hist_names["MDR"] = "MDR"
    hist_names["DPB_vSS"] = "DPB"
    hist_names["gamInvRp1"] = "gamInvRp1"
    hist_names["cosThetaB"] = "cosThetaB"
    hist_names["RPT"] = "RPT"

    for variable in variables :
        print " > Plottings %s"%variable
        p = plot.Plot1D()
        p.initialize(hist_names[variable], variable, "%s_%s_%s_%s"%(hist_names[variable], region.name, str(signew.mX), str(signew.mY)))
        p.labels(x=nice_names[variable], y="Arb. Units")
        p.xax(bounds[variable][0], bounds[variable][1], bounds[variable][2])
        p.setRatioCanvas(p.name)

        rcan = p.ratioCanvas
        rcan.canvas.cd()
        rcan.upper_pad.cd()

        r.gPad.SetGrid()

        hax = r.TH1F("axes", "", int(p.nbins), p.x_range_min, p.x_range_max)
        hax.SetMinimum(p.y_range_min)
        hax.SetMaximum(p.y_range_max)
        hax.GetXaxis().SetTitle(p.x_label)
        hax.GetXaxis().SetTitleFont(42)
        hax.GetXaxis().SetLabelFont(42)
        hax.GetXaxis().SetLabelSize(0.035)
        hax.GetXaxis().SetTitleSize(0.048 * 0.85)
        hax.GetXaxis().SetTitleOffset(-999)
        hax.GetXaxis().SetLabelOffset(-999) 

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

        samples = [signew, sigold]

        line_colors = {}
        line_colors["old"] = 46
        line_colors["new"] = 38

        leg_names = {}
        leg_names["old"] = "(%s,%s) w/ Reweighting"%(str(samples[0].mX), str(samples[0].mY))
        leg_names["new"] = "(%s,%s) w/ MadSpin"%(str(samples[0].mX), str(samples[0].mY))

        histos = []
        maxy = []
        for s in samples :
            h = pu.th1f("h_" + s.kind + "_" + hist_names[variable],"", int(p.nbins), p.x_range_min, p.x_range_max, p.x_label, p.y_label)
            old_or_new = s.kind
            h.SetLineColor(line_colors[old_or_new])
            h.GetXaxis().SetLabelOffset(-999)
            h.SetFillColor(0)
            h.SetLineWidth(2)
            h.Sumw2

            weight_str = ""
            if old_or_new == "old" :
                weight_str = "eventweight * susy3BodyRightPol"
                #weight_str = "eventweightNOPUPW * susy3BodyRightPol"
            else :
                #s.tree.Scan("mcid:susy3BodyRightPol")
                weight_str = "eventweight"
                #weight_str = "eventweightNOPUPW"

            cut = "(" + region.tcut + ") * %s"%weight_str
            cut = r.TCut(cut)
            sel = r.TCut("1")
            cmd = "%s>>+%s"%(p.variable, h.GetName())
            s.tree.Draw(cmd, cut * sel, "goff")

            print "%s : %.2f"%(old_or_new, h.GetMean())

            pu.add_overflow_to_lastbin(h)

            stat_err = r.Double(0.0)
            integral = h.IntegralAndError(0,-1,stat_err)
            print "[%s] %.2f +/- %.2f"%(old_or_new, float(integral), float(stat_err))
            if integral != 0 : h.Scale(1/integral)


            leg.AddEntry(h, leg_names[old_or_new], "l")
            histos.append(h)
            rcan.canvas.Update()
            maxy.append(h.GetMaximum())

        maxy = 1.25*max(maxy)

        is_first = True
        for hist in histos :
            if is_first :
                is_first = False
                hist.SetMaximum(maxy)
                hist.Draw("hist e")
            hist.SetMaximum(maxy)
            hist.Draw("hist e same")

        leg.Draw()
        pu.draw_text_on_top(text=region.displayname)

        

        ################ hey, baby, let's move to the lower pad
        rcan.lower_pad.cd()

        h_new = None
        h_old = None
 
        for h in histos :
            if "old" in h.GetName() :
                h_old = h
            elif "new" in h.GetName() :
                h_new = h

        h_n = h_new.Clone("new_hist")
        h_o = h_old.Clone("old_hist")
        h_n.Divide(h_o)
        h_n.GetYaxis().SetRangeUser(0,2)

        hr = h_n

        hr.SetLineColor(r.kBlack)

        yax = hr.GetYaxis()
        yax.SetTitle("MadSpin/Reweight")
        yax.SetTitleSize(0.1 * 0.83)
        yax.SetLabelSize(0.1 * 0.81)
        yax.SetLabelOffset(0.98 * 0.013 * 1.08)
        yax.SetTitleOffset(0.45 * 1.2)
        yax.SetLabelFont(42)
        yax.SetTitleFont(42)
        yax.SetNdivisions(5)

        xax = hr.GetXaxis()
        xax.SetTitleSize(1.0 * 0.14)
        xax.SetLabelSize(yax.GetLabelSize())
        xax.SetLabelOffset(1.15 * 0.02)
        xax.SetTitleOffset(0.85 * xax.GetTitleOffset())
        xax.SetLabelFont(42)
        xax.SetTitleFont(42)
    
        hr.Draw("hist e")
        outname = p.variable + "_%s_%s"%(str(samples[0].mX), str(samples[0].mY)) + "_" + region.name + ".eps"
        rcan.canvas.SaveAs(outname)
        out = "./plots/"
        utils.mv_file_to_dir(outname, out, True)
        fullname = out + "/" + outname
        print "%s saved to  : %s"%(outname, os.path.abspath(fullname))

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
    frame = r.TH2F("frame", "", n_bins, 100, 500, 93, 0, 425)

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

def get_averages(signals, variable) :

    bins = {}
    bins["nBJets"] = [1, 0, 20]
    bins["MDR"] = [10, 0, 1000]
    bins["RPT"] = [100, 0, 1]
    bins["gamInvRp1"] = [100, 0, 1]
    bins["met"] = [200,0,500]
    bins["DPB_vSS"] = [100,0,3.2]
    bins["l_pt[0]"] = [100,0,300]
    bins["l_pt[1]"] = [100,0,300]
    bins["bj_pt[0]"] = [100,0,300]

    n_bins = bins[variable][0]
    x_low = bins[variable][1]
    x_high = bins[variable][2]

    tcut = "(nLeptons==2 && mll>20 && l_pt[0]>25 && l_pt[1]>20 && %s) * eventweight"%trigger
    

    for s in signals :
        h_avg = r.TH1F("h_avg_%s_%s_%s"%(str(s.kind),str(s.mX), str(s.mY)),"", n_bins, x_low, x_high)
        cmd = "%s>>+%s"%(variable, h_avg.GetName())
        if s.kind == "old" :
            tcut = tcut# + " * susy3BodyRightPol"
        cut = r.TCut(tcut)
        sel = r.TCut("1")
        s.tree.Draw(cmd, cut * sel, "goff") 

        h_avg.Scale(1/h_avg.Integral())

        average = h_avg.GetMean()
        s.average = average

def make_average_plot(signals_old, signals_new, average_plot) :
    set_palette()

    samples = [signals_old, signals_new]

    variables = {}
    variables["nBJets"] = "nBJets"
    variables["MDR"] = "MDR"
    variables["RPT"] = "RPT"
    variables["gamInvRp1"] = "gamInvRp1"
    variables["met"] = "met"
    variables["DPB_vSS"] = "DPB_vSS"
    variables["l_pt[0]"] = "lpt0"
    variables["l_pt[1]"] = "lpt1"
    variables["bj_pt[0]"] = "bjpt0"
    variable = variables[average_plot]

    maxima = {}
    maxima["nBJets"] = 3.5
    maxima["MDR"] = 1.15
    maxima["RPT"] = 1.1
    maxima["gamInvRp1"] = 1.2
    maxima["met"] = 1.5
    maxima["DPB_vSS"] = 1.5
    maxima["l_pt[0]"] = 1.2
    maxima["l_pt[1]"] = 1.2
    maxima["bj_pt[0]"] = 1.2

    minima = {}
    minima["nBJets"] = 0.5
    minima["MDR"] = 0.85
    minima["RPT"] = 0.9
    minima["gamInvRp1"] = 0.8
    minima["met"] = 0.8
    minima["DPB_vSS"] = 0.8
    minima["l_pt[0]"] = 0.8
    minima["l_pt[1]"] = 0.8
    minima["bj_pt[0]"] = 0.8

    get_averages(signals_old, average_plot)
    get_averages(signals_new, average_plot)

    samples = [signals_new, signals_old]

    for sn in signals_new :
        for so in signals_old :
            if sn.mX==so.mX and sn.mY==so.mY :
                sn.average = sn.average / so.average

    for i, sample in enumerate(samples) :
        kind = ""
        if i == 0 : kind = "new"
        else : kind = "old"

        canvas = r.TCanvas("c_average_%s_%s"%(variable, kind), "", 768, 768)
        canvas.cd()

        frame = make_frame("average_%s_%s"%(variable,kind))
        frame.Draw("axis")
        frame.GetXaxis().SetTitle("m_{#tilde{t}} [GeV]")
        frame.GetYaxis().SetTitle("m_{#tilde{#chi_{0}}} [GeV]")
        canvas.Update()

        gr = r.TGraph2D(1)
        gr.Clear()
        gr.SetMarkerStyle(r.kFullSquare)
        gr.SetMarkerSize(2*gr.GetMarkerSize())
        gr.SetMaximum(maxima[average_plot])
        gr.SetMinimum(minima[average_plot])

        for s in sample :
            average = s.average
            x = float(s.mX)
            y = float(s.mY)
            available_in_both = False
            new_avail = False
            old_avail = False
            for sn in signals_new :
                if float(sn.mX)==x and float(sn.mY)==y :
                    new_avail = True
            for sn in signals_old :
                if float(sn.mX)==x and float(sn.mY)==y :
                    old_avail = True
            available_in_both = new_avail and old_avail
                
            if not available_in_both :
                continue
            gr.SetPoint(gr.GetN(), x, y, float(average))

        # put text yo
        tex = r.TLatex(0.0,0.0,'')
        tex.SetTextFont(42)
        tex.SetTextSize(1.2*0.3*tex.GetTextSize())

        if gr.GetN() :
            gr.Draw("colz same")
        canvas.Update()

        for s in sample :
            average = s.average
            x = float(s.mX)
            y = float(s.mY)
            available_in_both = False
            new_avail = False
            old_avail = False
            for sn in signals_new :
                if float(sn.mX)==x and float(sn.mY)==y :
                    new_avail = True
            for sn in signals_old :
                if float(sn.mX)==x and float(sn.mY)==y :
                    old_avail = True
            available_in_both = new_avail and old_avail

            if not available_in_both : continue
            tex.DrawLatex(x,y,"%.2f"%float(average))



        # z-axis
        z_title = "%s Avg. MadSpin/Reweighting"%variable
        pu.draw_text(text=z_title, x = 0.97, y = 0.3, size=0.035, angle=90.0)

        ########################
        # save
        canvas.SaveAs("avg_plot_%s_ratio.eps"%(variable))
        break
    

#__________________________________________________
if __name__ == "__main__" :
    global outdir, dbg, request_region
    parser = OptionParser()
    parser.add_option("-o", "--outdir", default="./")
    parser.add_option("-d", "--dbg", action="store_true", default=False)
    parser.add_option("-r", "--region", default="")
    parser.add_option("-x", "--mx", default="250")
    parser.add_option("-y", "--my", default="160")
    parser.add_option("--avg", default="")
    (options,args) = parser.parse_args()
    outdir = options.outdir
    dbg = options.dbg
    request_region = options.region
    m_stop = options.mx
    m_lsp = options.my
    average_plot = options.avg

    if request_region == "" and average_plot == "":
        print "ERROR You must provide a region to plot (-r/--region input)"
        print "ERROR  > Exiting"
        sys.exit()

    #########
    print 75*"-"
    print "Compsig"
    print 75*"-"

    signals_old, signals_new = load_signals()
    print ""
    print "Loaded %d new signals"%len(signals_new)
    print "Loaded %d old signals"%len(signals_old)
    print ""

    if average_plot == "" :
        found_masses_new, signal_new = look_for_signal(m_stop, m_lsp, signals_new, "new")
        found_masses_old, signal_old = look_for_signal(m_stop, m_lsp, signals_old, "old")
        if not found_masses_new or not found_masses_old :
            print " > Exiting"
            sys.exit()
        make_comparison_plots(signal_new, signal_old, request_region)
    elif average_plot != "" :
        make_average_plot(signals_old, signals_new, average_plot)


