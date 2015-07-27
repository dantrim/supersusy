#!/usr/bin/env python

import ROOT as r
r.gROOT.SetBatch(False)
r.gStyle.SetOptStat(False)
import sys
sys.path.append('../../..')
#sys.dont_write_bytecode = True

r.TEventList.__init__._creates = False
r.TH1F.__init__._creates = False


import argparse
import os

import supersusy.utils.plot_utils as pu
import supersusy.utils.utils as utils
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region
import supersusy.utils.plot as plot

def get_plotConfig(conf) :
    configuration_file = ""
    configuration_file = "./plotConfig/" + conf + ".py"
    if os.path.isfile(configuration_file) :
        return configuration_file
    else :
        print 'get_plotConfig ERROR    Input plotConfig ("%s") is not found in the plotConfig/ directory. Does it exist? Exitting.'%conf
        sys.exit()

def check_for_consistency(plots, regions) :
    '''
    Make sure that the plots are not asking for a region that
    has not been loaded in the config
    '''
    bad_regions = []
    configured_regions = []
    for r in regions :
        configured_regions.append(r.simplename)
    for p in plots :
        current_region = p.region
        if current_region not in configured_regions :
            bad_regions.append(current_region)
    if len(bad_regions) > 0 :
        print 'check_for_consistency ERROR    You have configured a plot for a region that has not also been configured:'
        print bad_regions
        print 'check_for_consistency ERROR    The regions set-up in the configuration ("%s") are:'%plotConfig
        for r in configured_regions :
            print "check_for_consistency ERROR     > '%s'"%(r)
        print "check_for_consistency ERROR    Exitting."
        sys.exit()
    else :
        print "check_for_consistency    Plots and regions consistent."

def make_plotsRatio(plot, reg, data, backgrounds) :
    print "make_plotsRatio    Plotting %s"%plot.name

    rcan = plot.ratioCanvas
    rcan.canvas.cd()
    rcan.upper_pad.cd()

    if plot.isLog() : rcan.upper_pad.SetLogy(True)
    rcan.upper_pad.Update()

    stack = r.THStack("stack_"+plot.name, "")
    leg = pu.default_legend()
    leg.SetNColumns(2)


    histos = []
    for b in backgrounds :
        h = pu.th1f("h_"+b.treename+"_"+plot.variable, "", int(plot.nbins), plot.x_range_min, plot.x_range_max, plot.x_label, plot.y_label)
        h.SetLineColor(r.kBlack)
        h.SetFillColor(b.color)
        h.SetFillStyle(1001)
        h.Sumw2

        cut = "(" + reg.tcut + ") * eventweight * " + str(b.scale_factor)
        cut = r.TCut(cut)
        sel = r.TCut("1")
        #var = "l_q[0]*l_d0sigBSCorr[0]"
        #cmd = "%s>>+%s"%(var, h.GetName())
        cmd = "%s>>+%s"%(plot.variable, h.GetName())
        b.tree.Draw(cmd, cut * sel)
        print "%s: %.2f"%(b.displayname, h.Integral(0,-1))
        #stack.Add(h)
        leg.AddEntry(h, b.displayname, "fl")
        histos.append(h)
        rcan.upper_pad.Update()

    #order the histos
    histos = sorted(histos, key=lambda h: h.Integral(), reverse=False)
    for h in histos :
        stack.Add(h)
    rcan.upper_pad.Update()

    #### DATA
    hd = pu.th1f("h_data_"+reg.simplename, "", int(plot.nbins), plot.x_range_min, plot.x_range_max, plot.x_label, plot.y_label)
    hd.Sumw2
    cut = "(" + reg.tcut + ")"
    cut = r.TCut(cut)
    sel = r.TCut("1")
    #var = "l_q[0]*l_d0sigBSCorr[0]"
    #cmd = "%s>>+%s"%(var, hd.GetName())
    cmd = "%s>>+%s"%(plot.variable, hd.GetName())
    data.tree.Draw(cmd, cut * sel)
    print "Data: %.2f"%(hd.Integral(0,-1))
    #g = pu.th1_to_tgraph(hd)
    g = pu.convert_errors_to_poisson(hd)
    g.SetLineWidth(2)
    g.SetMarkerStyle(20)
    g.SetMarkerSize(1.1)
    g.SetLineColor(1)
    leg.AddEntry(g, "Data", "p")
    rcan.upper_pad.Update()

        
    stack.Draw("HIST")
    stack.GetXaxis().SetTitle(plot.x_label)
    stack.GetYaxis().SetTitle(plot.y_label)
    stack.GetXaxis().SetTitleFont(42)
    stack.GetYaxis().SetTitleFont(42)
    stack.GetXaxis().SetLabelFont(42)
    stack.GetYaxis().SetLabelFont(42)
    stack.GetYaxis().SetTitleOffset(1.4)
    stack.GetYaxis().SetLabelOffset(0.013)
    stack.SetMinimum(plot.y_range_min)
    stack.SetMaximum(plot.y_range_max)
    #stack.GetXaxis().SetLabelSize(0.046)
    stack.GetXaxis().SetLabelSize(0.035)
    #stack.GetYaxis().SetLabelSize(0.05)
    stack.GetYaxis().SetLabelSize(1.2 * 0.035)
    stack.GetXaxis().SetTitleSize(0.048 * 0.85)
    stack.GetYaxis().SetTitleSize(0.055 * 0.85)

    #throw away x-axis labels
    stack.GetXaxis().SetTitleOffset(-999)
    stack.GetXaxis().SetLabelOffset(-999)
    rcan.upper_pad.Update()

    g.Draw("option same pz")
    leg.Draw()
    r.gPad.RedrawAxis()
    pu.draw_text_on_top(text=plot.name)
    pu.draw_text(text="#it{ATLAS} Simulation",x=0.18,y=0.85)
    pu.draw_text(text="13 TeV, ~50 pb^{-1} (period C)",x=0.18, y=0.8)
    pu.draw_text(text=reg.displayname, x=0.18,y=0.75)

    r.gPad.SetTickx()
    r.gPad.SetTicky()

    rcan.upper_pad.Update()

    #### Lower Pad

    rcan.lower_pad.cd()
    h_sm = stack.GetStack().Last().Clone("h_sm")
    
    # yaxis
    yax = h_sm.GetYaxis()
    yax.SetRangeUser(0,2)
    yax.SetTitle("Data/SM")
    yax.SetTitleSize(0.14)
    yax.SetLabelSize(0.13)
    yax.SetLabelOffset(0.98 * 0.013)
    yax.SetTitleOffset(0.45)
    yax.SetLabelFont(42)
    yax.SetTitleFont(42)
    yax.SetNdivisions(5) 
    # xaxis
    xax = h_sm.GetXaxis()
    xax.SetTitleSize(1.2 * 0.14)
    xax.SetLabelSize(0.13)
    xax.SetLabelOffset(1.15*0.02)
    xax.SetTitleOffset(0.85 * xax.GetTitleOffset())
    xax.SetLabelFont(42)
    xax.SetTitleFont(42)
   
    h_sm.SetTickLength(0.06)
    h_sm.Draw("AXIS")
    rcan.lower_pad.Update()

    # draw lines
    pu.draw_line(plot.x_range_min, 1.0, plot.x_range_max, 1.0,color=r.kRed,style=2,width=1)
    pu.draw_line(plot.x_range_min, 0.5, plot.x_range_max, 0.5,style=3,width=1)
    pu.draw_line(plot.x_range_min, 1.5, plot.x_range_max, 1.5,style=3,width=1)

    g_ratio = pu.divide_histograms(hd, h_sm, plot.x_label, "Data/SM")
    g_ratio.SetLineWidth(1)
    g_ratio.SetMarkerStyle(20)
    g_ratio.SetMarkerSize(1.1)
    g_ratio.SetLineColor(1)
    g_ratio.Draw("option pz")
    rcan.lower_pad.Update()

    rcan.canvas.Update()


    outname = plot.name + ".eps"
    rcan.canvas.SaveAs(outname)
    utils.mv_file_to_dir(outname, outdir, True)
    

    


def make_plots1D(plot, reg, data, backgrounds) :

    if plot.ratioCanvas : make_plotsRatio(plot, reg, data, backgrounds)
    else :
        print "make_plots1D    Plotting %s"%plot.name 
        c = plot.canvas
        c.cd()
        c.SetFrameFillColor(0)
        c.SetFillColor(0)
        c.SetLeftMargin(0.14)
        c.SetRightMargin(0.05)
        c.SetBottomMargin(1.3*c.GetBottomMargin())


        if plot.isLog() : c.SetLogy(True)
        c.Update()
        
        stack = r.THStack("stack_"+plot.name, "")

        leg = pu.default_legend()
        leg.SetNColumns(2)

        # order the backgrounds by integral
        histos = []
        for b in backgrounds :
            h = pu.th1f("h_"+b.treename+"_"+plot.variable, "", int(plot.nbins), plot.x_range_min, plot.x_range_max, plot.x_label, plot.y_label)
            h.SetLineColor(r.kBlack)
            h.SetLineWidth(1)
            h.SetFillColor(b.color)
            h.SetFillStyle(b.fillStyle)
            h.Sumw2

            cut = "(" + reg.tcut + ") * eventweight * " + str(b.scale_factor)
            cut = r.TCut(cut)
            sel = r.TCut("1")
            cmd = "%s>>+%s"%(plot.variable, h.GetName())
            b.tree.Draw(cmd, cut * sel)
            print "%s: %.2f"%(b.displayname, h.Integral(0,-1))
            #stack.Add(h)
            leg.AddEntry(h, b.displayname, "f")
            histos.append(h)
            c.Update()

        #order the histos
        histos = sorted(histos, key=lambda h: h.Integral(), reverse=False)
        for h in histos :
            stack.Add(h)
        c.Update()

        #### DATA
        hd = pu.th1f("h_data_"+reg.simplename, "", int(plot.nbins), plot.x_range_min, plot.x_range_max, plot.x_label, plot.y_label)
        hd.Sumw2
        cut = "(" + reg.tcut + ")"
        cut = r.TCut(cut)
        sel = r.TCut("1")
        cmd = "%s>>+%s"%(plot.variable, hd.GetName())
        data.tree.Draw(cmd, cut * sel)
        print "Data: %.2f"%(hd.Integral(0,-1))
        #g = pu.th1_to_tgraph(hd)
        g = pu.convert_errors_to_poisson(hd)
        g.SetLineWidth(2)
        g.SetMarkerStyle(20)
        g.SetMarkerSize(1.1)
        g.SetLineColor(1)
        leg.AddEntry(g, "Data", "p")


        
        stack.Draw("HIST")
        stack.GetXaxis().SetTitle(plot.x_label)
        stack.GetYaxis().SetTitle(plot.y_label)
        stack.GetXaxis().SetTitleFont(42)
        stack.GetYaxis().SetTitleFont(42)
        stack.GetXaxis().SetLabelFont(42)
        stack.GetYaxis().SetLabelFont(42)
        stack.GetYaxis().SetTitleOffset(1.4)
        stack.GetYaxis().SetLabelOffset(0.013)
        stack.SetMinimum(plot.y_range_min)
        stack.SetMaximum(plot.y_range_max)
        #stack.GetXaxis().SetLabelSize(0.046)
        stack.GetXaxis().SetLabelSize(0.035)
        #stack.GetYaxis().SetLabelSize(0.05)
        stack.GetYaxis().SetLabelSize(0.035)
        stack.GetXaxis().SetTitleSize(0.048 * 0.85)
        stack.GetYaxis().SetTitleSize(0.055 * 0.85)


        g.Draw("option same pz")
        leg.Draw()

        pu.draw_text_on_top(text=plot.name)
        pu.draw_text(text="#it{ATLAS} Simulation",x=0.18,y=0.85)
        pu.draw_text(text="13 TeV, ~6 pb^{-1}",x=0.18, y=0.8)
        pu.draw_text(text=reg.displayname, x=0.18,y=0.75)
        c.Update()
        r.gPad.RedrawAxis()
        outname = plot.name + ".eps"
        c.SaveAs(outname)
        utils.mv_file_to_dir(outname, outdir, True)

def check_2d_consistency(plot, data, backgrounds) :

    if plot.sample == "Data" and data.treename == "":
        print 'check_2d_consistency ERROR    Requested sample is ("Data") and the data sample is empty. Exitting.'
        sys.exit()
    sample_in_backgrounds = False
    for b in backgrounds :
        if plot.sample == b.name and plot.sample != "Data" : sample_in_backgrounds = True
    if not sample_in_backgrounds and plot.sample != "Data" :
        print 'check_2d_consistency ERROR    Requested sample ("%s") is not in the backgrounds list:'%plot.sample
        print backgrounds
        print 'check_2d_consistency ERROR    Exitting.'
        sys.exit()

    print 'check_2d_consistency    Samples consistent with plot.'

def make_1dprofile(plot, reg, data, backgrounds) :
    print "make_1dprofile    Plotting %s"%plot.name

    r.gStyle.SetOptStat(1100)
    c = plot.canvas
    c.cd()
    c.SetGridx(1)
    c.SetGridy(1)
    c.SetFrameFillColor(0)
    c.SetFillColor(0)
    c.SetLeftMargin(0.13)
    c.SetRightMargin(0.14)
    c.SetBottomMargin(1.3*c.GetBottomMargin())

    name_on_plot = ""

    if plot.sample != "Data" :
        for b in backgrounds :
            if b.name != plot.sample : continue
            name_on_plot += b.displayname
            h = r.TProfile("hprof_"+b.name+"_"+plot.xVariable+"_"+plot.yVariable,";%s;%s"%(plot.x_label,plot.y_label), int(plot.n_binsX), plot.x_range_min, plot.x_range_max, plot.y_range_min, plot.y_range_max)

            cut = "(" + reg.tcut + ") * eventweight * " + str(b.scale_factor)
            cut = r.TCut(cut)
            sel = r.TCut("1")
            cmd = "%s:%s>>+%s"%(plot.yVariable, plot.xVariable, h.GetName())
            b.tree.Draw(cmd, cut * sel, "prof")
            h.SetMarkerColor(r.TColor.GetColor("#E67067"))

    if plot.sample == "Data" :
        name_on_plot = "Data"
        h = r.TProfile("hprof_Data_"+plot.xVariable+"_"+plot.yVariable,";%s;%s"%(plot.x_label,plot.y_label), int(plot.n_binsX), plot.x_range_min, plot.x_range_max, plot.y_range_min, plot.y_range_max)

        cut = "(" + reg.tcut + ")"
        cut = r.TCut(cut)
        sel = r.TCut("1")
        cmd = "%s:%s>>+%s"%(plot.yVariable, plot.xVariable, h.GetName())
        data.tree.Draw(cmd, cut * sel, "prof")
        h.SetMarkerColor(r.TColor.GetColor("#5E9AD6"))

  #  r.TGaxis.SetMaxDigits(2)
    h.GetYaxis().SetTitleOffset(1.6 * h.GetYaxis().GetTitleOffset())
    h.GetXaxis().SetTitleOffset(1.2 * h.GetXaxis().GetTitleOffset())
    h.SetMarkerStyle(8)
    h.SetLineColor(r.kBlack)
    h.SetMarkerSize(1.15*h.GetMarkerSize())
    h.GetYaxis().SetRangeUser(plot.y_range_min,plot.y_range_max)

    h.Draw()
    r.gPad.Update()

    st = h.FindObject("stats")
    st.SetY1NDC(0.93 * st.GetY1NDC())
    st.SetY2NDC(0.93 * st.GetY2NDC())

    h.Draw()

  #  pu.draw_text_on_top(text="%s : #bf{%s}"%(plot.name, name_on_plot),pushup=1.035)
    pu.draw_text_on_top(text="%s : #bf{%s}"%(plot.name, name_on_plot))

    c.Update()
    r.gPad.RedrawAxis()
    outname = "periodC/" + plot.name + ".eps"
    c.SaveAs(outname)
    utils.mv_file_to_dir(outname, outdir, True)

def make_plots2D(plot, reg, data, backgrounds) :

    check_2d_consistency(plot, data, backgrounds)

    if plot.do_profile : 
        make_1dprofile(plot, reg, data, backgrounds)
        return
    print "make_plots2D    Plotting %s"%plot.name 
    
    pu.set_palette(name="redbluevector")

    c = plot.canvas
    c.cd()
    # these should be int he default cavnas setting in utils/plot.py
    c.SetFrameFillColor(0)
    c.SetFillColor(0)
    c.SetLeftMargin(0.13)
    c.SetRightMargin(0.14)
    c.SetBottomMargin(1.3*c.GetBottomMargin())

    name_on_plot = ""

    if plot.sample != "Data" :
        for b in backgrounds :
            if b.name != plot.sample : continue
            name_on_plot = b.displayname
            h = pu.th2f("h_"+b.name+"_"+plot.xVariable+"_"+plot.yVariable, "", int(plot.n_binsX), plot.x_range_min, plot.x_range_max, int(plot.n_binsY), plot.y_range_min, plot.y_range_max, plot.x_label, plot.y_label)
            
            cut = "(" + reg.tcut + ") * eventweight * " + str(b.scale_factor)
            cut = r.TCut(cut)
            sel = r.TCut("1")
            cmd = "%s:%s>>+%s"%(plot.yVariable,plot.xVariable,h.GetName())
            b.tree.Draw(cmd, cut * sel)


    if plot.sample == "Data" :
        name_on_plot = "Data"
        h = pu.th2f("h_"+data.name+"_"+plot.xVariable+"_"+plot.yVariable, "", int(plot.n_binsX), plot.x_range_min, plot.x_range_max, int(plot.n_binsY), plot.y_range_min, plot.y_range_max, plot.x_label, plot.y_label)

        cut = "(" + reg.tcut + ")"
        cut = r.TCut(cut)
        sel = r.TCut("1")
        cmd = "%s:%s>>+%s"%(plot.yVariable,plot.xVariable,h.GetName())
        data.tree.Draw(cmd, cut * sel)


    if h.Integral()!=0 : h.Scale(1/h.Integral())
    h.Smooth()
    h.GetYaxis().SetTitleOffset(1.52 * h.GetYaxis().GetTitleOffset())
    h.GetXaxis().SetTitleOffset(1.2 * h.GetXaxis().GetTitleOffset())
    #r.TGaxis.SetMaxDigits(2)
    #h.GetZaxis().SetLabelSize(0.75 * h.GetLabelSize())
 
    g = r.TGraph2D(1)
    g.SetMarkerStyle(r.kFullSquare)
    g.SetMarkerSize(2.0 * g.GetMarkerSize())
    g.SetHistogram(h)
    g.Draw(plot.style)
#    g.Smooth()

    pu.draw_text_on_top(text="%s : #bf{%s}"%(plot.name,name_on_plot))

 #   h.Draw(plot.style)
    c.Update()
    r.gPad.RedrawAxis()
    outname = plot.name+".eps"
    c.SaveAs(outname)
    utils.mv_file_to_dir(outname, outdir, True)

def make_plots(plots, regions, data, backgrounds) :
    for reg in regions:
        plots_with_region = []
        for p in plots :
            if p.region == reg.simplename : plots_with_region.append(p)
        if len(plots_with_region)==0 : continue
        print "Setting EventLists for %s"%reg.simplename
        cut = reg.tcut
        cut = r.TCut(cut)
        sel = r.TCut("1")
        for b in backgrounds :
            list_name = "list_" + reg.simplename + "_" + b.treename
            #this_list = r.TEventList(list_name)
            if os.path.isfile(list_name + ".root") :
                rfile = r.TFile.Open(list_name+".root")
                list = rfile.Get(list_name) 
              #  thislist = r.gDirectory.Get(list.GetName())
                list.Print()
                b.tree.SetEventList(list)
            else :
                draw_list = ">> " + list_name
                b.tree.Draw(draw_list, sel*cut)
                list = r.gROOT.FindObject(list_name)
                b.tree.SetEventList(list)
                list.SaveAs(list_name + ".root")

        # do data
        data_list_name = "list_" + reg.simplename + "_" + data.treename
        if os.path.isfile(data_list_name + ".root") :
            rfile = r.TFile.Open(data_list_name+".root")
            data_list = rfile.Get(data_list_name)
            data_list.Print()
            data.tree.SetEventList(data_list)
        else :
            draw_list = ">> " + data_list_name
            data.tree.Draw(draw_list, sel * cut)
            data_list = r.gROOT.FindObject(data_list_name)
            data.tree.SetEventList(data_list)
            data_list.SaveAs(data_list_name+".root")

        for p in plots_with_region :
            if not p.is2D : make_plots1D(p, reg, data, backgrounds) 
            elif p.is2D : make_plots2D(p, reg, data, backgrounds)


  #  for p in plots :
  #      if not p.is2D : make_plots1D(p, regions, data, backgrounds)
  #      elif p.is2D : make_plots2D(p, regions, data, backgrounds)


if __name__=="__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--plotConfig")
    parser.add_argument("-r", "--requestRegion", default="")
    parser.add_argument("-p", "--requestPlot", default="")
    parser.add_argument("-o", "--outdir", default="./")
    args = parser.parse_args()
    global plotConfig, requestRegion, requestPlot, outdir
    plotConfig = args.plotConfig
    requestRegion = args.requestRegion
    requestPlot = args.requestPlot
    outdir = args.outdir

    if requestRegion != "" and requestPlot != "" :
        print 'ERROR    You have requested both a reagion ("%s") AND a plot ("%s").'%(requestRegion, requestPlot)
        print 'ERROR    You may only request one at a time. Exitting.'
        sys.exit()

    conf_file = get_plotConfig(plotConfig)
    print conf_file

    plots = []
    data = None
    backgrounds = []
    regions = []
    execfile(conf_file)
    for p in plots :
        p.Print()
    for b in backgrounds :
        b.Print()
    data.Print()

    check_for_consistency(plots, regions)

    if requestRegion != "" :
        requested_plots = []
        for p in plots :
            if p.region == requestRegion : requested_plots.append(p)
        make_plots(requested_plots, regions, data, backgrounds)
    elif requestPlot != "" :
        requested_plots = []
        for p in plots :
            if p.name == requestPlot : requested_plots.append(p)
        make_plots(requested_plots, regions, data, backgrounds)
    else :
        make_plots(plots, regions, data, backgrounds)
            


   # make_plots(plots, regions, data, backgrounds)
