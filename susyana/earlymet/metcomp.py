#!/usr/bin/env python

import ROOT as r
r.gROOT.SetBatch(False)
r.gStyle.SetOptStat(False)
import sys
sys.path.append('../../..')
sys.dont_write_bytecode = True

import supersusy.utils.plot_utils as pu
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region
import supersuys.utils.plot as plot


def define_regions() :
    '''
    Define here the various regions (as TCuts) that you will need
    '''
    regions = []
    # ----------------------------
    #  Z like 
    # ----------------------------
    reg = region.Region()
    reg.simplename     = "zlike"
    reg.displayname    = "Z-enriched"
    reg.tcut           = "nLeptons==2 && nJets>=0 && l_pt[0]>25 && l_pt[1]>25 && l_d0sigBSCorr[0]<5 && l_d0sigBSCorr[1]<5 && l_eta[0]<2.4 & l_eta[1]<2.4 && l_z0sinTheta[0]<3 && l_z0sinTheta[1]<3"
    regions.append(reg)

    return regions

if __name__ == "__main__" :

    datafile = "/gdata/atlas/dantrim/SusyAna/histoAna/run2early/n0208/data/Processed/data15_13TeV.root"
    data = background.Data()
    data.set_file(datafile)
    data.set_treename("Data_CENTRAL")
    data.set_merged_tree(data.treename)
    data.Print()

    zeefile = "/gdata/atlas/dantrim/SusyAna/histoAna/run2early/n0208/mc/Processed/zee_mc15_13TeV.root"
    zee = background.Background("Zee")
    zee.set_debug()
    zee.set_file(zeefile)
    zee.color = r.kRed
    zee.set_treename("Zee_CENTRAL")
    zee.set_merged_tree(zee.treename)
    zee.Print()

    zmmfile = "/gdata/atlas/dantrim/SusyAna/histoAna/run2early/n0208/mc/Processed/zmm_mc15_13TeV.root"
    zmm = background.Background("Zmm")
    zmm.set_debug()
    zmm.set_file(zmmfile)
    zmm.color = r.kBlue
    zmm.set_treename("Zmm_CENTRAL")
    zmm.set_merged_tree(zmm.treename)
    zmm.Print()

    regions = define_regions()

    c = pu.basic_canvas()
    c.cd()
    histos = []
    maxy = -99
    stack = r.THStack("stack", "stack")
    leg = pu.default_legend()
    for b in [zee, zmm] :
        h = pu.th1f("test", "", 20, 70, 110, "m_{ll} [GeV]", "Entries")
        h.SetLineColor(b.color)
     #   h.SetLineWidth(2)
        h.SetFillColor(b.color)
        h.SetFillStyle(1001)

        region = regions[0]
        cut ="(" + region.tcut + ") * eventweight"
        cut = r.TCut(cut)
        sel = r.TCut("1")
        cmd = "mll>>%s"%h.GetName()
        b.tree.Draw(cmd, cut * sel, "goff")
        stack.Add(h)
        leg.AddEntry(h, b.displayname, "f")
    #    histos.append(h)
    #    if h.GetMaximum() > maxy : maxy = 1.3 * h.GetMaximum()
    #    c.Update()

#    histos[0].SetMaximum(maxy)
#    histos[0].Draw("hist")
#    for hist in histos :
#        hist.SetMaximum(maxy)
#        hist.Draw("hist same")
#    c.Update()
#
    stack.Draw("HIST")
    hd = pu.th1f("data", "", 20, 70, 110, "m_{ll} [GeV]", "Entries")
    hd.Sumw2
    region = regions[0]
    cut ="(" + region.tcut + ") * eventweight"
    cut = r.TCut(cut)
    sel = r.TCut("1")
    cmd = "mll>>%s"%hd.GetName()
    data.tree.Draw(cmd, cut * sel, "goff")
    g = pu.th1_to_tgraph(hd)
    g.SetLineWidth(2)
    g.SetMarkerStyle(20)
    g.SetMarkerSize(1.1)
    g.SetLineColor(1)
    g.Draw("same p0")
    c.Update() 

    leg.AddEntry(g, data.displayname, "p")
    leg.Draw("ap same")
    c.Update()
    

    c.SaveAs("test.eps")
