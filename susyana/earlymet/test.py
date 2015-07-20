#!/usr/bin/env python

import ROOT as r
r.gROOT.SetBatch(False)
r.gStyle.SetOptStat(False)
import sys
sys.path.append('../../..')
sys.dont_write_bytecode = True

import argparse
import os

import supersusy.utils.plot_utils as pu
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

def make_plotsRatio(plot, regions, data, backgrounds) :
    print "make_plotsRatio not defined"

def make_plots1D(plot, reg, data, backgrounds) :
    print "make_plots1D    Plotting %s"%plot.name 

    if plot.ratioCanvas : make_plotsRatio(plot, reg, data, backgrounds)
    else :
        c = plot.canvas
        c.cd()
        c.SetFrameFillColor(0)
        c.SetFillColor(0)
        c.SetLeftMargin(0.14)
        c.SetRightMargin(0.05)
        c.SetBottomMargin(1.3*c.GetBottomMargin())

        if p.doLogY : c.SetLogy(True)
        
        stack = r.THStack("stack_"+plot.name, "")
     #   reg = region.Region()
     #   for regi in regions :
     #       if regi.simplename == plot.region :
     #           reg.simplename = regi.simplename
     #           reg.tcut = regi.tcut
     #           reg.displayname = regi.displayname

        leg = pu.default_legend()

        for b in backgrounds :
            h = pu.th1f("h_"+b.treename, "", int(plot.nbins), plot.x_range_min, plot.x_range_max, plot.x_label, plot.y_label)
            h.SetLineColor(b.color)
            h.SetFillColor(b.color)
            h.SetFillStyle(1001)
            h.Sumw2

            cut = "(" + reg.tcut + ") * eventweight * " + str(b.scale_factor)
            cut = r.TCut(cut)
            sel = r.TCut("1")
            cmd = "%s>>%s"%(plot.variable, h.GetName())
            b.tree.Draw(cmd, cut * sel)
            print "%s: %.2f"%(b.displayname, h.Integral(0,-1))
            stack.Add(h)
            leg.AddEntry(h, b.displayname, "fl")
            c.Update()

        #### DATA
        hd = pu.th1f("h_data_"+reg.simplename, "", int(plot.nbins), plot.x_range_min, plot.x_range_max, plot.x_label, plot.y_label)
        hd.Sumw2
        cut = "(" + reg.tcut + ")"
        cut = r.TCut(cut)
        sel = r.TCut("1")
        cmd = "%s>>%s"%(plot.variable, hd.GetName())
        data.tree.Draw(cmd, cut * sel)
        print "Data: %.2f"%(hd.Integral(0,-1))
        g = pu.th1_to_tgraph(hd)
        g.SetLineWidth(2)
        g.SetMarkerStyle(20)
        g.SetMarkerSize(1.1)
        g.SetLineColor(1)

        c.Update()

        
        stack.Draw("HIST")
        stack.GetXaxis().SetTitle(plot.x_label)
        stack.GetYaxis().SetTitle(plot.y_label)
        stack.GetXaxis().SetTitleFont(42)
        stack.GetYaxis().SetTitleFont(42)
        stack.GetXaxis().SetLabelFont(42)
        stack.GetYaxis().SetLabelFont(42)
        stack.GetYaxis().SetTitleOffset(0.95 * 1.28)
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

        r.gPad.RedrawAxis()
        outname = plot.name + ".eps"
        c.SaveAs(outname)
        

def make_plots2D(plot, regions, data, backgrounds) :
    print "make_plots2D not defined"

def make_plots(plots, regions, data, backgrounds) :
    for reg in regions:
        plots_with_region = []
        for p in plots :
            print p.name
            if p.region == reg.simplename : plots_with_region.append(p)
        if len(plots_with_region)==0 : continue
        print "Setting EventLists for %s"%reg.simplename
        cut = reg.tcut
        cut = r.TCut(cut)
        sel = r.TCut("1")
        for b in backgrounds :
            list_name = "list_" + reg.simplename + "_" + b.treename
            list = r.TEventList(list_name)
            draw_list = ">> " + list_name
            b.tree.Draw(draw_list, sel*cut)
            
            this_list = r.gDirectory.Get(list_name)
            b.tree.SetEventList(this_list)

        # do data
        data_list_name = "list_" + reg.simplename + "_data"
        data_list = r.TEventList(data_list_name)
        draw_list = ">> " + data_list_name
        data.tree.Draw(draw_list, sel*cut)
        data.tree.SetEventList(r.gDirectory.Get(data_list_name))

        for p in plots_with_region :
            if not p.is2D : make_plots1D(p, reg, data, backgrounds) 
            elif p.is2D : make_plots2D(p, reg, data, backgrounds)


  #  for p in plots :
  #      if not p.is2D : make_plots1D(p, regions, data, backgrounds)
  #      elif p.is2D : make_plots2D(p, regions, data, backgrounds)


if __name__=="__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--plotConfig")
    args = parser.parse_args()
    global plotConfig
    plotConfig = args.plotConfig

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

    make_plots(plots, regions, data, backgrounds)
