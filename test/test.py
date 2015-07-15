#!/usr/bin/env python

import ROOT as r
r.gROOT.SetBatch(False)
r.gStyle.SetOptStat(False)
import sys
sys.path.append('../..')
sys.dont_write_bytecode = True

import supersusy.utils.plot_utils as pu
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region


if __name__=="__main__" :
    s = signal.Signal()
    s.set_debug()
    s.set_file("/afs/cern.ch/work/d/dantrim/public/SusyAna/Super/CENTRAL_406002.root")
    s.set_grid("tN1")
    s.set_dsid_from_file(s.file)
    s.set_tree()
    s.set_mass_info()
    s.set_displayname_from_masses()

    b = background.Background("ttbar")
    b.set_debug()
    b.set_file("/afs/cern.ch/work/d/dantrim/public/SusyAna/Super/CENTRAL_410000.root")
    b.set_dsid_from_file(b.file)
    b.set_tree()
    b.Print()

    tcuts = {}
    displaynames = {}
    tcuts["test"] = "l_pt[0]>35"
    displaynames["test"] = "Dummy Region"
    testregion = region.Region()
    testregion.tcut = tcuts["test"]
    testregion.displayname = displaynames["test"]
    testregion.Print()

    c = pu.basic_canvas()
    c.cd()

    h1 = pu.th1f("test", "", 25, 0, 200, "p_{T} [GeV]", "Entries")
    h1.SetLineColor(b.color)
    h2 = pu.th1f("test2", "", 25, 0, 200, "p_{T} [GeV]", "Entries")
    h2.SetLineColor(s.color)
    cmd1 = "l_pt[0]>>%s"%h1.GetName()
    cmd2 = "l_pt[0]>>%s"%h2.GetName()
    print "background : %s"%str(b.tree.GetEntries())
    print "signal     : %s"%str(s.tree.GetEntries())
    b.tree.Draw(cmd1, testregion.tcut)
    s.tree.Draw(cmd2, testregion.tcut)
    h1.Draw("hist")
    h2.Draw("hist same")

    leg = pu.default_legend()
    leg.AddEntry(h1, b.displayname, "l")
    leg.AddEntry(h2, s.displayname, "l")
    leg.Draw("same")
    c.Update()

    pu.draw_text_on_top(text="%s: %s"%(testregion.displayname, testregion.tcut), size=0.03)
    c.Update()

    c.Print("test.eps")
    


