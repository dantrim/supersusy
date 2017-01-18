#!/usr/bin/env python

from optparse import OptionParser
import os

import glob

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

reg = region.Region()
reg.name = "dfprebv"
reg.displayname = "DF Preselection + b-veto"
reg.tcut = "nLeptons==2 && " + isDFOS + " && nBJets==0 && mll>20 && " + trigger
regions.append(reg)


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

    region = None
    for reg in regions :
        if reg.name == reg_request :
            region = reg 

    print " > %s"%region.name

    # variables
    variables = []
    variables.append("l_pt[0]")
    variables.append("MDR")
    variables.append("DPB_vSS")


    nice_names = {}
    nice_names["l_pt[0]"] = "Lead lepton p_{T} [GeV]"
    nice_names["MDR"] = "MDR"
    nice_names["DPB_vSS"] = "DPB"

    bounds = {}
    bounds["l_pt[0]"] = [10, 20, 150]
    bounds["MDR"] = [10,0,300]
    bounds["DPB_vSS"] = [0.1,0,3.2]

    hist_names = {}
    hist_names["l_pt[0]"] = "lpt0"
    hist_names["MDR"] = "MDR"
    hist_names["DPB_vSS"] = "DPB"

    for variable in variables :
        print " > Plottings %s"%variable
        p = plot.Plot1D()
        p.initialize(hist_names[variable], variable, "%s_%s_%s_%s"%(hist_names[variable], reg.name, str(signew.mX), str(signew.mY)))
        p.labels(x=nice_names[variable], y="Arb. Units")
        p.xax(bounds[variable][0], bounds[variable][1], bounds[variable][2])
        p.setRatioCanvas(p.name)

        rcan = p.ratioCanvas
        rcan.canvas.cd()
        rcan.upper_pad.cd()

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
        line_colors["old"] = r.kBlack
        line_colors["new"] = r.kBlue

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
                weight_str = "eventweightNOPUPW"#* susy3BodyLeftPol"
            else :
                weight_str = "eventweightNOPUPW"

            cut = "(" + reg.tcut + ") * %s"%weight_str
            cut = r.TCut(cut)
            sel = r.TCut("1")
            cmd = "%s>>+%s"%(p.variable, h.GetName())
            s.tree.Draw(cmd, cut * sel, "goff")

            pu.add_overflow_to_lastbin(h)

            stat_err = r.Double(0.0)
            integral = h.IntegralAndError(0,-1,stat_err)
            print "%.2f +/- %.2f"%(float(integral), float(stat_err))
            if integral != 0 : h.Scale(1/integral)


            leg_name = old_or_new
            leg.AddEntry(h, leg_name, "l")
            histos.append(h)
            rcan.canvas.Update()
            maxy.append(h.GetMaximum())

        maxy = 1.25*max(maxy)

        is_first = True
        for hist in histos :
            if is_first :
                is_first = False
                hist.SetMaximum(maxy)
                hist.Draw("hist")
            hist.SetMaximum(maxy)
            hist.Draw("hist same")

        leg.Draw()

        outname = p.name + ".eps"
        rcan.canvas.SaveAs(outname)
        out = "./plots/"
        utils.mv_file_to_dir(outname, out, True)
        fullname = out + "/" + outname
        print "%s saved to  : %s"%(outname, os.path.abspath(fullname))

    

    

#__________________________________________________
if __name__ == "__main__" :
    global outdir, dbg, request_region
    parser = OptionParser()
    parser.add_option("-o", "--outdir", default="./")
    parser.add_option("-d", "--dbg", action="store_true", default=False)
    parser.add_option("-r", "--region", default="")
    parser.add_option("-x", "--mx", default="250")
    parser.add_option("-y", "--my", default="160")
    (options,args) = parser.parse_args()
    outdir = options.outdir
    dbg = options.dbg
    request_region = options.region
    m_stop = options.mx
    m_lsp = options.my

    if request_region == "" :
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

    found_masses_new, signal_new = look_for_signal(m_stop, m_lsp, signals_new, "new")
    found_masses_old, signal_old = look_for_signal(m_stop, m_lsp, signals_old, "old")
    if not found_masses_new or not found_masses_old :
        print " > Exiting"
        sys.exit()

    make_comparison_plots(signal_new, signal_old, request_region)


