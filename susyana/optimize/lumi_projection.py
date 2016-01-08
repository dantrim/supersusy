#!/usr/bin python

import ROOT as r
r.gROOT.SetBatch(True)
import array
import collections

r.TGraph.__init__._creates = False
r.TCanvas.__init__._creates = False
r.TH1F.__init__._creates = False

if __name__ == "__main__" :

#    ######### PROJECTSION FROM SEPTEMBER 22
#    ## "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && DPB_vTT_0 > 2. && RPT_0 > 0.60 && nBJets==0 && mt2>90"
#
#    # lumi projectsionf ro (250, 160)
#    x0 = collections.OrderedDict()
#    x0[1]  = 1.40 
#    x0[2]  = 1.93
#    x0[4]  = 2.47
#    x0[6]  = 2.75
#    x0[10] = 3.05
#    
#
#    # lumi projections for (300, 180)
#    x1 = collections.OrderedDict()
#    x1[1]  = 0.6 
#    x1[2]  = 0.91
#    x1[4]  = 1.23
#    x1[6]  = 1.40
#    x1[10] = 1.6
#
#    # lumi projections for (300, 150)
#    x2 = collections.OrderedDict()
#    x2[1]  = 0.06 
#    x2[2]  = 0.24
#    x2[4]  = 0.41
#    x2[6]  = 0.49
#    x2[10] = 0.6

#    ################### 20 %
#
#    # lumi (250,160) 20%
#    x0 = collections.OrderedDict()
#    x0[3.34] = 2.90
#    x0[6.0] = 3.58
#    x0[8.0] = 3.91
#    x0[10.0] = 4.15
#
#    # lumi (300,180) 20%
#    x1 = collections.OrderedDict()
#    x1[3.34] = 1.22
#    x1[6.0]  = 1.57
#    x1[8.0]  = 1.75
#    x1[10.0] = 1.88
#
#    # lumi (300,150) 20%
#    x2 = collections.OrderedDict()
#    x2[3.34] = 0.39
#    x2[6.0]  = 0.58
#    x2[8.0]  = 0.67
#    x2[10.0] = 0.73

#    ################### 30 %
#
#    # lumi (250,160) 30%
#    x0 = collections.OrderedDict()
#    x0[3.34] = 2.68
#    x0[6.0]  = 3.22
#    x0[8.0]  = 3.46
#    x0[10.0] = 3.64
#
#    # lumi (300,180) 30%
#    x1 = collections.OrderedDict()
#    x1[3.34] = 1.11
#    x1[6.0]  = 1.40
#    x1[8.0]  = 1.53
#    x1[10.0] = 1.63
#
#    # lumi (300,150) 30%
#    x2 = collections.OrderedDict()
#    x2[3.34] = 0.33
#    x2[6.0]  = 0.48
#    x2[8.0]  = 0.55
#    x2[10.0] = 0.60

    ################### 40 %

    # lumi (250,160) 40%
    x0 = collections.OrderedDict()
    x0[3.34] = 2.42
    x0[6.0]  = 2.84
    x0[8.0]  = 3.02
    x0[10.0] = 3.14

    # lumi (300,180) 40%
    x1 = collections.OrderedDict()
    x1[3.34] = 0.98
    x1[6.0]  = 1.21
    x1[8.0]  = 1.31
    x1[10.0] = 1.38

    # lumi (300,150) 40%
    x2 = collections.OrderedDict()
    x2[3.34] = 0.26
    x2[6.0]  = 0.38
    x2[8.0]  = 0.43
    x2[10.0] = 0.47

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
        g.GetXaxis().SetTitle("Integrated Lumi [fb^{-1}] (#sigma_{sys} = 20 %%)")
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
    

