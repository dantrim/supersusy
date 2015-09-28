#!/usr/bin python

import ROOT as r
r.gROOT.SetBatch(True)
import array
import collections

r.TGraph.__init__._creates = False
r.TCanvas.__init__._creates = False
r.TH1F.__init__._creates = False

if __name__ == "__main__" :

    ######### PROJECTSION FROM SEPTEMBER 15
    # lumi projectsionf ro (250, 160)
    x0 = collections.OrderedDict()
    x0[1]  = 1.4
    x0[2]  = 1.83
    x0[4]  = 2.23
    x0[6]  = 2.42
    x0[10] = 2.62
    

    # lumi projections for (300, 180)
    x1 = collections.OrderedDict()
    x1[1]  = 0.37 
    x1[2]  = 0.57
    x1[4]  = 0.74
    x1[6]  = 0.83
    x1[10] = 0.92

    # lumi projections for (300, 150)
    x2 = collections.OrderedDict()
    x2[1]  = 0.0 
    x2[2]  = 0.0
    x2[4]  = 0.05
    x2[6]  = 0.08
    x2[10] = 0.11

    ######### PROJECTSION FROM SEPTEMBER 22
    ## "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && DPB_vTT_0 > 2. && RPT_0 > 0.60 && nBJets==0 && mt2>90"

    # lumi projectsionf ro (250, 160)
    x0 = collections.OrderedDict()
    x0[1]  = 1.40 
    x0[2]  = 1.93
    x0[4]  = 2.47
    x0[6]  = 2.75
    x0[10] = 3.05
    

    # lumi projections for (300, 180)
    x1 = collections.OrderedDict()
    x1[1]  = 0.6 
    x1[2]  = 0.91
    x1[4]  = 1.23
    x1[6]  = 1.40
    x1[10] = 1.6

    # lumi projections for (300, 150)
    x2 = collections.OrderedDict()
    x2[1]  = 0.06 
    x2[2]  = 0.24
    x2[4]  = 0.41
    x2[6]  = 0.49
    x2[10] = 0.6



    c = r.TCanvas("c1", "", 600, 700)
    c.cd()

    graphs = []
    for i, dic in enumerate([x0, x1, x2]) :
        name = ""
        color = None
        if i == 0 : 
            name = "(250, 160)"
            color = r.TColor.GetColor("#315E88")
        elif i == 1 : 
            name = "(300, 180)"
            color = r.TColor.GetColor("#FC0D1B")
        elif i == 2 : 
            name = "(300, 150)"
            color = r.TColor.GetColor("#41C1FC")

        g = r.TGraph()
        g.SetTitle("")
        g.SetName(name)
        g.SetMinimum(0.0)
        g.SetMaximum(5.0)
        g.GetXaxis().SetTitle("Integrated Lumi [fb^{-1}]")
        g.GetYaxis().SetTitle("Significance")
        g.SetLineWidth(2)
        g.SetLineColor(color)
        g.SetLineStyle(1)
        for xval, yval in dic.iteritems() :
            g.SetPoint(g.GetN(), float(xval), float(yval))
        graphs.append(g)

    leg = r.TLegend(0.15, 0.72, 0.53, 0.90)
    leg.SetFillStyle(0)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetTextFont(42)

    is_first = True
    for graph in graphs :
        leg.AddEntry(graph, graph.GetName(), "l")
        if is_first :
            is_first = False
            graph.Draw("AC")
            graph.GetXaxis().SetTitle("Integrated Lumi [fb^{-1}]")
            graph.GetYaxis().SetTitle("Significance")
            c.Update()
        else :
            graph.Draw("C")
            graph.GetXaxis().SetTitle("Integrated Lumi [fb^{-1}]")
            graph.GetYaxis().SetTitle("Significance")
            c.Update()

    leg.Draw()
    c.Update()

    c.SaveAs("testLumi.eps")
    

