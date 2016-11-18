#!/usr/bin/env python

from optparse import OptionParser
import os

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(False)
r.gROOT.ProcessLine("gErrorIgnoreLevel=3001;")

import sys
sys.path.append(os.environ['SUSYDIR'])

import supersusy.utils.plot_utils as pu
import supersusy.utils.utils as utils
import supersusy.utils.region as region
import supersusy.utils.plot as plot


################################
# files
file_dir = "/data/uclhc/uci/user/dantrim/ntuples/n0228/g_nov14/mc/Raw/"
zjets_file = file_dir + "zjets_mumu_ee.root" 
vbf_higgs_file = file_dir + "CENTRAL_341080.root"

class Sample :
    def __init__(self, name_ = "", displayname_="", color_ = 1) :
        self.name = name_
        self.displayname = displayname_
        self.color = color_
        self.tree = None

    def load_chain(self, file_="") :
        chain = r.TChain("superNt")
        chain.Add(file_)
        self.tree = chain


def get_samples() :

    # zjets
    zjets_sample = Sample("zjets", "Z+jets (ee+#mu#mu)", r.kBlack)
    zjets_sample.load_chain(zjets_file)

    # higgs
    higgs_sample = Sample("higgs", "VBF Higgs", r.kRed)
    higgs_sample.load_chain(vbf_higgs_file)

    return higgs_sample, zjets_sample

def get_pre_regions() :

    isSFOS = "nLeptons==2 && (nElectrons==2 || nMuons==2) && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"
    isSFOS = isSFOS + " && abs(mll-91.2)>25."
    isDilepton = "nLeptons==2 && (((nElectrons==2 || nMuons==2) && abs(mll-91.2)>25.) || (nElectrons==1 && nMuons==1)) && l_pt[0]>25 && l_pt[1]>20"
    reg_pre = isDilepton + " && mll>40 && met>45"
    #reg_pre = isSFOS + " && mll>40 && met>35"

    reg_pre_fjvt = reg_pre + " && nSJets>=2 && deta_sj>4.4 && mjj_sj>700 && sj_pt[0]>40 && sj_pt[1]>20 && lep_centrality_sjet>2"
    reg_pre_nfjvt = reg_pre + " && nSNPJets>=2 && deta_snpj>4.4 && mjj_snpj>700 && snpj_pt[0]>40 && snpj_pt[1]>20 && lep_centrality_snpjet>2"

    # fJVT pre-region
    reg_fjvt = region.Region()
    reg_fjvt.name = "pre_fjvt"
    reg_fjvt.displayname = "VBF Pre-Selection (w/ fJVT)"
    reg_fjvt.tcut = reg_pre_fjvt

    # no-fJVT pre-region
    reg_no_fjvt = region.Region()
    reg_no_fjvt.name = "pre_nfjvt"
    reg_no_fjvt.displayname = "VBF Pre-Selection (w/out fJVT)"
    reg_no_fjvt.tcut = reg_pre_nfjvt

    return reg_fjvt, reg_no_fjvt


#######################################################
def make_fjvt_plots(higgs, zjets) :

    # pre-selection regions
    reg_pre_fjvt, reg_pre_nfjvt = get_pre_regions()
    regions = [reg_pre_fjvt, reg_pre_nfjvt]

    # variables
    nice_names = {}
    nice_names["mjj"] = "m_{jj} [GeV]"
    nice_names["deta"] = "|#Delta#eta|"
    nice_names["centrality"] = "Lepton centrality"
    nice_names["recoil"] = "f_{recoil}"
    nice_names["nsjets"] = "Number of jets"
    nice_names["jpt0"] = "Lead jet p_{T} [GeV]"
    nice_names["jpt1"] = "Sub-lead jet p_{T} [GeV]"

    bounds = {}
    bounds["mjj"] = [100, 0, 3000,1e10]
    bounds["deta"] = [0.4,0,8,1e10]
    bounds["centrality"] = [0.4, -2,5,1e10]
    bounds["recoil"] = [0.1, 0, 5,1e10]
    bounds["nsjets"] = [1,2,6,1e10]
    bounds["jpt0"] = [20, 0, 300,1e10]
    bounds["jpt1"] = [20, 0, 300,1e10] 

    variables = {}
    variables["mjj"] = { "fjvt" : "mjj_sj", "nfjvt" : "mjj_snpj" }
    variables["deta"] = { "fjvt" : "deta_sj", "nfjvt" : "deta_snpj" }
    variables["centrality"] = { "fjvt" : "lep_centrality_sjet", "nfjvt" : "lep_centrality_snpjet" }
    variables["recoil"] = { "fjvt" : "f_recoil_sjet", "nfjvt" : "f_recoil_snpjet" }
    variables["nsjets"] = { "fjvt" : "nSJets", "nfjvt" : "nSNPJets" }
    variables["jpt0"] = { "fjvt" : "sj_pt[0]", "nfjvt" : "snpj_pt[0]" }
    variables["jpt1"] = { "fjvt" : "sj_pt[1]", "nfjvt" : "snpj_pt[1]" }

    line_styles = {}
    line_styles["fjvt"] = 1
    line_styles["nfjvt"] = 2

    for var in variables.keys() :
        print "Plotting %s"%var

        p = plot.Plot1D()
        p.initialize("fjvt_check_%s"%str(var), str(var), "fjvt_check_%s"%str(var))
        p.labels(x=nice_names[var], y = "Arb. Units")
        p.xax(bounds[var][0], bounds[var][1], bounds[var][2])
        p.setRatioCanvas(p.name)

        # canvas
        rcan = p.ratioCanvas
        rcan.upper_pad.cd()

        # axis
        hax = r.TH1F("axis", "", int(p.nbins), p.x_range_min, p.x_range_max)
        hax.SetMinimum(10)
        hax.GetXaxis().SetTitle(nice_names[var])
        hax.Draw()
        rcan.upper_pad.Update()

        histos = []
        maxy_ = -1
        for reg in regions :
            print " > Region %s"%reg.name
            if "nfjvt" in reg.name :
                key = "nfjvt"
            else :
                key = "fjvt"
            for proc in [higgs, zjets] :
                print " >> %s"%proc.name
                h = pu.th1f("h_" + var + "_" + str(key) + "_" + proc.name, "", int(p.nbins),
                                        p.x_range_min, p.x_range_max, p.x_label, p.y_label)
                h.SetLineColor(proc.color)
                h.SetLineStyle(line_styles[key])
                h.SetFillStyle(0)
                h.SetLineWidth(2)
                h.GetXaxis().SetLabelOffset(-999)
                h.Sumw2

                weight_str = "eventweight"
                if "higgs" in proc.name :
                    weight_str += " * 1e5"
                cut = "(" + reg.tcut + ") * " + weight_str
                cut = r.TCut(cut)
                sel = r.TCut("1")
                cmd = "%s>>%s"%(variables[var][key], h.GetName())
                proc.tree.Draw(cmd, cut * sel, "goff")

                pu.add_overflow_to_lastbin(h) 


                stat_err = r.Double(0.0)
                integral = h.IntegralAndError(0,-1,stat_err)
                print "%s (%s) : %.2f +/- %.2f"%(str(proc.name), key, integral, stat_err)


                # normalize
                #h.Scale(1/h.Integral())
                if h.GetMaximum() > maxy_ :
                    maxy_ = 1.2 * h.GetMaximum()

                histos.append(h)
                rcan.upper_pad.Update()

        r.gPad.SetGrid()

        for h in histos :
            h.SetMaximum(maxy_)

        # legend
        leg = pu.default_legend(xl=0.55, yl=0.71, xh=0.93, yh=0.90)
        h_higgs_fjvt = None
        h_higgs_nfjvt = None
        h_zjets_fjvt = None
        h_zjets_nfjvt = None
        for h in histos :
            if "nfjvt" in h.GetName() :
                if "higgs" in h.GetName() :
                    h_higgs_nfjvt = h
                else :
                    h_zjets_nfjvt = h
            else :
                if "higgs" in h.GetName() :
                    h_higgs_fjvt = h
                else :
                    h_zjets_fjvt = h
        #h_higgs_nfjvt.Scale(h_zjets_nfjvt.Integral())
        #h_higgs_fjvt.Scale(h_zjets_fjvt.Integral())
        #h_higgs_nfjvt.Scale(h_zjets_nfjvt.Integral()/h_higgs_nfjvt.Integral())
        #h_higgs_fjvt.Scale(h_zjets_fjvt.Integral()/h_zjets_fjvt.Integral())

        leg.AddEntry(h_higgs_fjvt, "VBF Higgs x1e5 (w/ fJVT)", "l")
        leg.AddEntry(h_higgs_nfjvt, "VBF Higgs x1e5 (w/out fJVT)", "l")
        leg.AddEntry(h_zjets_fjvt, "Z+jets (w/ fJVT)", "l")
        leg.AddEntry(h_zjets_nfjvt, "Z+jets (w/out fJVT)", "l")

        ## draw
        h_higgs_fjvt.Draw("hist")
        h_higgs_nfjvt.Draw("hist same")
        h_zjets_fjvt.Draw("hist same")
        h_zjets_nfjvt.Draw("hist same")

        ## draw legend
        leg.Draw()

        r.gPad.SetTickx()
        r.gPad.SetTicky()


        ######################## LOWER PAD
        rcan.lower_pad.cd()

        # higgses
        h_h_nfjvt  = h_higgs_nfjvt.Clone("higgs_nofjvt")
        h_h_ratio  = h_higgs_fjvt.Clone("higgs_fjvt")
        h_h_ratio.Divide(h_h_nfjvt)
        h_h_ratio.GetYaxis().SetRangeUser(0,5)

        # zjetses
        h_z_nfjvt = h_zjets_nfjvt.Clone("zjets_nofjvt")
        h_z_ratio = h_zjets_fjvt.Clone("zjets_fjvt")
        h_z_ratio.Divide(h_z_nfjvt)
        h_z_ratio.GetYaxis().SetRangeUser(0,5)

        # axes
        haxis = [h_h_ratio, h_z_ratio]
        for hax in haxis :
            yax = hax.GetYaxis()
            yax.SetTitle("fJVT / no fJVT")
            yax.SetTitleSize(0.1 * 0.83)
            yax.SetLabelSize(0.1 * 0.81)
            yax.SetLabelOffset(0.98 * 0.013 * 1.08)
            yax.SetTitleOffset(0.45 * 1.2)
            yax.SetLabelFont(42)
            yax.SetTitleFont(42)
            yax.SetNdivisions(5)

            xax = hax.GetXaxis()
            xax.SetTitleSize(1.0 * 0.14)
            xax.SetLabelSize(yax.GetLabelSize())
            xax.SetLabelOffset(1.15 * 0.02)
            xax.SetTitleOffset(0.85 * xax.GetTitleOffset())
            xax.SetLabelFont(42)
            xax.SetTitleFont(42)


        h_h_ratio.Draw("hist")
        h_z_ratio.Draw("hist same")



        # save
        outname = p.name + ".eps"
        rcan.canvas.SaveAs(outname)
        out = "./fjvtcheck/"
        utils.mv_file_to_dir(outname, out, True)
        fullname = out + outname
        print "%s saved to : %s"%(outname, os.path.abspath(fullname))

        



#_____________________________________________________________________________
if __name__ == "__main__" :
    parser = OptionParser()
    parser.add_option("-p", "--plots", action="store_true", default=False)
    parser.add_option("-e", "--eff", action="store_true", default=False)
    (options, args) = parser.parse_args()
    do_plots = options.plots
    do_eff = options.eff

    print 50*"-"
    print " fJVT "
    print "   plots      : %s"%do_plots
    print "   efficiency : %s"%do_eff
    print 50*"-"

    # get the trees/samples
    higgs, zjets = get_samples()

    if do_plots :
        make_fjvt_plots(higgs, zjets)
