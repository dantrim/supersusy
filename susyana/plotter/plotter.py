#!/usr/bin/env python


from optparse import OptionParser
import os

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True # don't let root steal cmd-line options
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(False)
import sys
sys.path.append(os.environ['SUSYDIR'])
#sys.path.append('../../../')
#sys.dont_write_bytecode = True

r.TEventList.__init__._creates = False
r.TH1F.__init__._creates = False
r.TGraphErrors.__init__._creates = False
r.TGraphAsymmErrors.__init__._creates = False


import supersusy.utils.plot_utils as pu
import supersusy.utils.utils as utils
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region
import supersusy.utils.plot as plot

def get_plotConfig(conf) :
    configuration_file = ""
    configuration_file = "./" + indir + "/" + conf + ".py"
    if os.path.isfile(configuration_file) :
        return configuration_file
    else :
        print 'get_plotConfig ERROR    Input plotConfig ("%s") is not found in the directory/path (%s). Does it exist? Exitting.'%(conf, configuration_file)
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
        print 'check_for_consistency ERROR    You have configured a plot for a region that is not defined. Here is the list of "bad regions":'
        for x in bad_regions :
            print x.simplename
        print 'check_for_consistency ERROR    The regions that are defined in the configuration ("%s") are:'%plotConfig
        print configured_regions
        print "check_for_consistency ERROR    Exitting."
        sys.exit()
    else :
        print "check_for_consistency    Plots and regions consistent."

def getSystHists(plot, reg, b, nom_yield) :
    for s in b.systList :
        hist_name = ""
        if "abs" in plot.variable :
            replace_var = plot.variable.replace("abs(","")
            replace_var = replace_var.replace(")","")
            hist_name = replace_var
        else : hist_name = plot.variable
        h_up = pu.th1f("h_"+b.treename+"_"+hist_name+"_"+s.name+"_up", "", int(plot.nbins), plot.x_range_min, plot.x_range_max, plot.x_label, plot.y_label)
        h_dn = pu.th1f("h_"+b.treename+"_"+hist_name+"_"+s.name+"_dn", "", int(plot.nbins), plot.x_range_min, plot.x_range_max, plot.x_label, plot.y_label)

        if s.isWeightSys() :
            cut_up = "(" + reg.tcut + ") * eventweight * " + str(s.up_name) + " * " + str(b.scale_factor)
            cut_dn = "(" + reg.tcut + ") * eventweight * " + str(s.down_name) + " * " + str(b.scale_factor)

            cut_up = r.TCut(cut_up)
            cut_dn = r.TCut(cut_dn)
            sel = r.TCut("1")

            cmd_up = "%s>>%s"%(plot.variable, h_up.GetName())
            cmd_dn = "%s>>%s"%(plot.variable, h_dn.GetName()) 

            s.tree.Draw(cmd_up, cut_up * sel)
            s.tree.Draw(cmd_dn, cut_dn * sel)

            # add overflow to these guys' last bins
            pu.add_overflow_to_lastbin(h_up)
            pu.add_overflow_to_lastbin(h_dn)

            print "    %s   (+%.2f, -%.2f)"%(s.name, h_up.Integral(0,-1)-nom_yield, nom_yield-h_dn.Integral(0,-1))

            s.up_histo = h_up
            s.down_histo = h_dn

        elif s.isKinSys() :
            cut = "(" + reg.tcut + ") * eventweight * " + str(b.scale_factor)
            cut = r.TCut(cut)
            self = r.TCut("1")
            cmd_up = "%s>>%s"%(plot.variable, h_up.GetName())
            cmd_dn = "%s>>%s"%(plot.variable, h_dn.GetName())

            s.tree_up.Draw(cmd_up, cut * sel)
            s.tree_down.Draw(cmd_dn, cut * sel)

            pu.add_overflow_to_lastbin(h_up)
            pu.add_overflow_to_lastbin(h_dn)

            s.up_histo = h_up
            s.down_histo = h_dn

def make_plotsRatio(plot, reg, data, backgrounds) :

    print "make_plotsRatio    Plotting %s"%plot.name

    # get the canvases
    rcan = plot.ratioCanvas
    rcan.canvas.cd()
    rcan.upper_pad.cd()

    if plot.isLog() : rcan.upper_pad.SetLogy(True)
    rcan.upper_pad.Update()

    # stack for MC
    hax = r.TH1F("axes", "", int(plot.nbins), plot.x_range_min, plot.x_range_max)
    hax.SetMinimum(plot.y_range_min)
    hax.SetMaximum(plot.y_range_max)
    hax.GetXaxis().SetTitle(plot.x_label)
    hax.GetXaxis().SetTitleFont(42)
    hax.GetXaxis().SetLabelFont(42)
    hax.GetXaxis().SetLabelSize(0.035)
    hax.GetXaxis().SetTitleSize(0.048 * 0.85)
    hax.GetXaxis().SetTitleOffset(-999)
    hax.GetXaxis().SetLabelOffset(-999)

    hax.GetYaxis().SetTitle(plot.y_label)
    hax.GetYaxis().SetTitleFont(42)
    hax.GetYaxis().SetLabelFont(42)
    hax.GetYaxis().SetTitleOffset(1.4)
    hax.GetYaxis().SetLabelOffset(0.013)
    hax.GetYaxis().SetLabelSize(1.2 * 0.035)
    hax.GetYaxis().SetTitleSize(0.055 * 0.85)
    hax.Draw()
    rcan.upper_pad.Update()

    stack = r.THStack("stack_"+plot.name, "")
    # legend
    leg = pu.default_legend(xl=0.65,yl=0.72,xh=0.93,yh=0.90)
    leg.SetNColumns(2)

    # loop through the background MC and add to stack
    histos = []
    for b in backgrounds :
        hist_name = ""
        if "abs" in plot.variable :
            replace_var = plot.variable.replace("abs(","")
            replace_var = replace_var.replace(")","")
            hist_name = replace_var
        elif "ptvarcone" and "pt" in plot.variable :
            r_ = plot.variable.split("/")[0][-5:-3]
            no_ = plot.variable.split("/")[0][-2:]
            hist_name = "R_ptvarcone%s_%s"%(str(r_), str(no_))
        elif "etconetopo" and "pt" in plot.variable :
            r_ = plot.variable.split("/")[0][-5:-3]
            no_ = plot.variable.split("/")[0][-2:]
            hist_name = "R_etconetopo%s_%s"%(str(r_), str(no_))
        else : hist_name = plot.variable
        h = pu.th1f("h_"+b.treename+"_"+hist_name, "", int(plot.nbins), plot.x_range_min, plot.x_range_max, plot.x_label, plot.y_label)
        h.SetLineColor(r.kBlack)
        h.GetXaxis().SetLabelOffset(-999)
        h.SetFillColor(b.color)
        h.SetFillStyle(1001)
        h.Sumw2

        # cut and make the sample weighted, applying the scale_factor
        cut = "(" + reg.tcut + ") * eventweight * " + str(b.scale_factor)
        cut = r.TCut(cut)
        sel = r.TCut("1")
        cmd = "%s>>+%s"%(plot.variable, h.GetName())
        b.tree.Draw(cmd, cut * sel, "goff")

        # print the yield +/- stat error
        stat_err = r.Double(0.0)
        integral = h.IntegralAndError(0,-1,stat_err)
        print "%s: %.2f +/- %.2f"%(b.name, integral, stat_err)

        # get the variation histos if plotting syst band
        if doSys : getSystHists(plot, reg, b, integral)
        
        # add overflow
        pu.add_overflow_to_lastbin(h)
        leg.AddEntry(h, b.displayname, "fl")
        histos.append(h)
        rcan.upper_pad.Update()

    # order the histos
    histos = sorted(histos, key=lambda h: h.Integral(), reverse=False)
    for h in histos :
        stack.Add(h)
    rcan.upper_pad.Update()

    # now get the data points
    hd = pu.th1f("h_data_"+reg.simplename, "", int(plot.nbins), plot.x_range_min, plot.x_range_max, plot.x_label, plot.y_label)
    hd.Sumw2
    cut = "(" + reg.tcut + ")"
    cut = r.TCut(cut)
    sel = r.TCut("1")
    cmd = "%s>>+%s"%(plot.variable, hd.GetName())
    data.tree.Draw(cmd, cut * sel, "goff")
    hd.GetXaxis().SetLabelOffset(-999)

    # print the yield +/- stat error
    stat_err = r.Double(0.0)
    integral = hd.IntegralAndError(0,-1,stat_err)
    print "Data: %.2f +/- %.2f"%(integral, stat_err)
    # add overflow
    pu.add_overflow_to_lastbin(hd)
    gdata = pu.convert_errors_to_poisson(hd)
    gdata.SetLineWidth(2)
    gdata.SetMarkerStyle(20)
    gdata.SetMarkerSize(1.1)
    gdata.SetLineColor(1)
    leg.AddEntry(gdata, "Data", "p")
    rcan.upper_pad.Update()

    #############################
    # systematics loop
    r.gStyle.SetHatchesSpacing(0.9)

    # dummy histo for legend
    mcError = r.TH1F("mcError", "mcError", 2,0,2)
    mcError.SetFillStyle(3354)
    mcError.SetFillColor(r.kBlack)
    mcError.SetLineColor(r.TColor.GetColor("#FC0F1D"))
    leg.AddEntry(mcError, "Total SM", "fl")

    # histogram for total stack
    totalSM = stack.GetStack().Last().Clone("totalSM")
    nominalAsymErrors = pu.th1_to_tgraph(totalSM)
    nominalAsymErrors.SetMarkerSize(0)
    nominalAsymErrors.SetLineWidth(0)
    nominalAsymErrors.SetFillStyle(3354)
    nominalAsymErrors.SetFillColor(r.kGray + 3)
   # leg.AddEntry(nominalAsymErrors, "Bkg. Uncert.", "f")

    if doSys :
        # totalSystHisto will hold each samples'
        # variation
        totalSysHisto = totalSM.Clone()
        totalSysHisto.Reset()
        transient = r.TGraphAsymmErrors()

        # add to the error band the contribution from the up-variations 
        systematics_up = [s.up_name for s in backgrounds[0].systList]
        for up_sys in systematics_up :
            transient = r.TGraphAsymmErrors()
            transient.Clear()
            for b in backgrounds :
                for syst in b.systList :
                    if syst.up_name != up_sys : continue
                    totalSysHisto.Add(syst.up_histo)
            transient = pu.th1_to_tgraph(totalSysHisto)
            pu.add_to_band(transient, nominalAsymErrors)
            totalSysHisto.Reset()

        # add to the error band the contribution from the down-variations
        systematics_down = [s.down_name for s in backgrounds[0].systList]
        for dn_sys in systematics_down :
            transient = r.TGraphAsymmErrors()
            transient.Clear()
            for b in backgrounds :
                for syst in b.systList :
                    if syst.down_name != dn_sys : continue
                    totalSysHisto.Add(syst.down_histo)
            transient = pu.th1_to_tgraph(totalSysHisto)
            pu.add_to_band(transient, nominalAsymErrors)
            totalSysHisto.Reset()


    # draw the MC stack and do cosmetcis
    stack.Draw("HIST SAME")
 #   stack.GetXaxis().SetTitle(plot.x_label)
 #   stack.GetYaxis().SetTitle(plot.y_label)
 #   stack.GetXaxis().SetTitleFont(42)
 #   stack.GetYaxis().SetTitleFont(42)
 #   stack.GetXaxis().SetLabelFont(42)
 #   stack.GetYaxis().SetLabelFont(42)
 #   stack.GetYaxis().SetTitleOffset(1.4)
 #   stack.GetYaxis().SetLabelOffset(0.013)
    stack.SetMinimum(plot.y_range_min)
    stack.SetMaximum(plot.y_range_max)
 #   stack.GetXaxis().SetLabelSize(0.035)
 #   stack.GetYaxis().SetLabelSize(1.2 * 0.035)
 #   stack.GetXaxis().SetTitleSize(0.048 * 0.85)
 #   stack.GetYaxis().SetTitleSize(0.055 * 0.85)
 #   #throw away x-axis labels from the upper-canvas
 #   stack.GetXaxis().SetTitleOffset(-999)
 #   stack.GetXaxis().SetLabelOffset(-999)
    rcan.upper_pad.Update()

    # draw the error band
    nominalAsymErrors.Draw("same && E2")

    # draw the total bkg line
    hist_sm = stack.GetStack().Last().Clone("hist_sm")
    hist_sm.SetLineColor(r.TColor.GetColor("#FC0F1D"))
    hist_sm.SetLineWidth(1)
    hist_sm.SetLineStyle(1)
    hist_sm.SetFillStyle(0)
    hist_sm.Draw("hist same")

    # draw the data graph
    gdata.Draw("option same pz")
    # draw the legend
    leg.Draw()
    r.gPad.RedrawAxis()

    # add some text/labels
    pu.draw_text_on_top(text=plot.name)
    pu.draw_text(text="#it{ATLAS} Work in Progress",x=0.18,y=0.85)
    pu.draw_text(text="13 TeV, 3.3 fb^{-1}",x=0.18,y=0.8)
    pu.draw_text(text=reg.displayname, x=0.18,y=0.75)

    r.gPad.SetTickx()
    r.gPad.SetTicky()

    rcan.upper_pad.Update()

    #### Lower Pad
    rcan.lower_pad.cd()

    # get the total SM histo
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

    # get the ratio-error band
    ratioBand = r.TGraphAsymmErrors(nominalAsymErrors)
    pu.buildRatioErrorBand(nominalAsymErrors, ratioBand)

    # draw lines
    pu.draw_line(plot.x_range_min, 1.0, plot.x_range_max, 1.0,color=r.kRed,style=2,width=1)
    pu.draw_line(plot.x_range_min, 0.5, plot.x_range_max, 0.5,style=3,width=1)
    pu.draw_line(plot.x_range_min, 1.5, plot.x_range_max, 1.5,style=3,width=1)

    # convert to tgraphs to get the ratio
    g_data = pu.th1_to_tgraph(hd)
    g_sm = pu.th1_to_tgraph(h_sm)
    g_ratio = pu.tgraphErrors_divide(g_data, g_sm)

    # For Data/MC only use the statistical error for data
    # since we explicity draw the MC error band
    nominalAsymErrorsNoSys = r.TGraphAsymmErrors(nominalAsymErrors)
    for i in xrange(nominalAsymErrorsNoSys.GetN()) :
        nominalAsymErrorsNoSys.SetPointError(i-1,0,0,0,0)
    ratio_raw = pu.tgraphErrors_divide(g_data, nominalAsymErrorsNoSys)
    ratio = r.TGraphAsymmErrors() 

    x1, y1 = r.Double(0.0), r.Double(0.0)
    index = 0
    for i in xrange(ratio_raw.GetN()) :
        ratio_raw.GetPoint(i, x1, y1)
        if y1 > 0. :
            ratio.SetPoint(index, x1, y1)
            ratio.SetPointError(index, ratio_raw.GetErrorXlow(i), ratio_raw.GetErrorXhigh(i), ratio_raw.GetErrorYlow(i), ratio_raw.GetErrorYhigh(i))
            index+=1
    ratio.SetLineWidth(1)
    ratio.SetMarkerStyle(20)
    ratio.SetMarkerSize(1.1)
    ratio.SetLineColor(1)
    ratio.SetMarkerSize(1.1)
    ratio.Draw("option pz")
    rcan.lower_pad.Update()
    
    ratioBand.Draw("same && E2")
    rcan.lower_pad.Update()

#    g_ratio.SetLineWidth(1)
#    g_ratio.SetMarkerStyle(20)
#    g_ratio.SetMarkerSize(1.1)
#    g_ratio.SetLineColor(1)
#    g_ratio.Draw("option pz")
#    rcan.lower_pad.Update()

    rcan.canvas.Update()

    outname = plot.name + ".eps"
    rcan.canvas.SaveAs(outname)
    out = indir + "/plots/" + outdir
    utils.mv_file_to_dir(outname, out, True)
    fullname = out + "/" + outname
    print "%s saved to : %s"%(outname, os.path.abspath(fullname)) 

def make_plotsComparison(plot, reg, data, backgrounds) :
    print "make_plotsComparison    Plotting %s"%plot.name

    c = plot.canvas
    c.cd()
    c.SetFrameFillColor(0)
    c.SetFillColor(0)
    c.SetLeftMargin(0.14)
    c.SetRightMargin(0.05)
    c.SetBottomMargin(1.3*c.GetBottomMargin())

    if plot.isLog() : c.SetLogy(True)
    c.Update()

    leg = None
    if plot.leg_is_left : leg = pu.default_legend(xl=0.2,yl=0.7,xh=0.47, yh=0.87)
    elif plot.leg_is_bottom_right : leg = pu.default_legend(xl=0.7, yl=0.2,xh=0.97,yh=0.37)
    elif plot.leg_is_bottom_left : leg = pu.default_legend(xl=0.2,yl=0.2,xh=0.47,yh=0.37)
    else : leg = pu.default_legend(xl=0.7,yl=0.7,xh=0.97,yh=0.87)

    histos = []
    maxy = []

#    for b in backgrounds :
#        nbjets = ["==0", "==1", "==2", "==3"]
#        colors = { "==0" : r.kBlue, "==1" : r.kRed, "==2" : r.kMagenta, "==3" : r.kCyan }
#        for i, nbj in enumerate(nbjets) :
#            h = pu.th1f("h_" + nbj, "", int(plot.nbins), plot.x_range_min, plot.x_range_max, plot.x_label, plot.y_label)
#            h.SetLineColor(colors[nbj])
#            h.SetLineWidth(2)
#            h.SetLineStyle(1)
#            h.SetFillColor(0)
#            h.Sumw2
#
#            if i==1 :
#                cut = "(" + reg.tcut + " && nBJets%s && bj_pt[0]>80"%nbj + ") * " + str(b.scale_factor)
#            elif i==2 :
#                cut = "(" + reg.tcut + " && nBJets%s && bj_pt[0]>80 && bj_pt[1]>80"%nbj + ") * " + str(b.scale_factor)
#            
#            else :
#                cut = "(" + reg.tcut + " && nBJets%s"%nbj + ") * " + str(b.scale_factor)
#            cut = r.TCut(cut)
#            cut.Print()
#            sel = r.TCut("1")
#            cmd = "%s>>+%s"%(plot.variable, h.GetName())
#            b.tree.Draw(cmd, cut * sel)
#
#            print "%s : %.2f"%(nbj, h.Integral())
#            h.Scale(1/h.Integral())
#            
#            # setup the axes
#            x = h.GetXaxis()
#            x.SetTitle(plot.x_label)
#            x.SetTitleSize(0.048 * 0.85)
#            x.SetLabelSize(0.035)
#            x.SetLabelOffset(1.15 * 0.02)
#            x.SetTitleOffset(0.95 * x.GetTitleOffset())
#            x.SetLabelFont(42)
#            x.SetTitleFont(42)
#
#            y = h.GetYaxis()
#            y.SetTitle("Arb. units")
#            y.SetTitleSize(0.055 * 0.85)
#            y.SetLabelSize(1.2 * 0.035)
#            y.SetLabelOffset(0.013)
#            y.SetTitleOffset(1.4)
#            y.SetLabelFont(42)
#            y.SetTitleFont(42)
#
#            leg.AddEntry(h, nbj, "l")
#            histos.append(h)
#            c.Update()
#            maxy.append(h.GetMaximum())
#    maxy_ = 1.25* max(maxy)

        


    for b in backgrounds :
        hist_name = ""
        if "abs" in plot.variable :
            replace_var = plot.variable.replace("abs(","")
            replace_var = replace_var.replace(")","")
            hist_name = replace_var
        elif "RPT_0/RPZ_0" in plot.variable :
            hist_name = "RPTZratio"
        elif "pTT_t_0 / (pTT_t_0 + MDR_v1_t1_0)" :
            hist_name = "RPT2"
        else : hist_name = plot.variable
        h = pu.th1f("h_"+b.treename+"_"+hist_name, "", int(plot.nbins), plot.x_range_min, plot.x_range_max, plot.x_label, plot.y_label)
        h.SetLineColor(b.color)
        h.SetLineWidth(2)
        h.SetLineStyle(b.line_style)
        h.SetFillColor(0)
        h.Sumw2

        # cut and make the sample weighted, applying any scale_factor
        cut = "(" + reg.tcut + ") * " + str(b.scale_factor)
        cut = r.TCut(cut)
        sel = r.TCut("1")
        cmd = "%s>>+%s"%(plot.variable, h.GetName())
        b.tree.Draw(cmd, cut * sel)

        # print the yield +/- stat error
        stat_err = r.Double(0.0)
        integral = h.IntegralAndError(0,-1, stat_err)
        print "%s: %.2f +/- %.2f"%(b.name, integral, stat_err)

        # normalize since we only care about shapes
        if integral != 0 : h.Scale(1/integral)

        # add overflow
        pu.add_overflow_to_lastbin(h)

        # setup the axes
        x = h.GetXaxis()
        x.SetTitle(plot.x_label)
        x.SetTitleSize(0.048 * 0.85)
        x.SetLabelSize(0.035)
        x.SetLabelOffset(1.15 * 0.02)
        x.SetTitleOffset(0.95 * x.GetTitleOffset())
        x.SetLabelFont(42)
        x.SetTitleFont(42)

        y = h.GetYaxis()
        y.SetTitle("Arb. units")
        y.SetTitleSize(0.055 * 0.85)
        y.SetLabelSize(1.2 * 0.035)
        y.SetLabelOffset(0.013)
        y.SetTitleOffset(1.4)
        y.SetLabelFont(42)
        y.SetTitleFont(42)

        leg.AddEntry(h, b.displayname, "l")
        histos.append(h)
        c.Update()
        maxy.append(h.GetMaximum())

    maxy_ = 1.25*max(maxy)

    is_first = True
    for hist in histos :
        if is_first :
            is_first = False
            hist.SetMaximum(maxy_)
            hist.Draw("hist")
        hist.Draw("hist same")
        hist.SetMaximum(maxy_)

    # legend
    leg.Draw()

    pu.draw_text_on_top(text=plot.name)

    outname = plot.name + ".eps"
    c.SaveAs(outname)
    out = indir + "/plots/" + outdir
    utils.mv_file_to_dir(outname, out, True)
    fullname = out + "/" + outname
    print "%s saved to : %s"%(outname, os.path.abspath(fullname))


def make_plots1D(plot, reg, data, backgrounds) :

    if plot.ratioCanvas : make_plotsRatio(plot, reg, data, backgrounds)
    elif plot.is_comparison : make_plotsComparison(plot, reg, data, backgrounds)
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

            # print the integral +/- stat_error
            stat_err = r.Double(0.0)
            integral = h.IntegralAndError(0,-1,stat_err)
            print "%s: %.2f +/- %.2f"%(b.name, integral, stat_err)

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

        # print the integral and +/- stat error
        stat_err = r.Double(0.0)
        integral = hd.IntegralAndError(0,-1,stat_err)
        print "Data: %.2f +/- %.2f"%(integral, stat_err)

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
        pu.draw_text(text="#it{ATLAS} Work in Progress",x=0.18,y=0.85)
        pu.draw_text(text="13 TeV, 78.3 pb^{-1}",x=0.18, y=0.8)
        pu.draw_text(text=reg.displayname, x=0.18,y=0.75)
        c.Update()
        r.gPad.RedrawAxis()

        outname = plot.name + ".eps"
        c.SaveAs(outname)
        out = indir + "/plots/" + outdir
        utils.mv_file_to_dir(outname, out, True)
        fullname = out + "/" + outname
        print "%s saved to : %s"%(outname, os.path.abspath(fullname)) 

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

    # get the stats box back to show the mean and err
    r.gStyle.SetOptStat(1100)

    # grab the plot's canvas and pretty up
    c = plot.canvas
    c.cd()
    c.SetGridx(1)
    c.SetGridy(1)
    c.SetFrameFillColor(0)
    c.SetFillColor(0)
    c.SetLeftMargin(0.13)
    c.SetRightMargin(0.14)
    c.SetBottomMargin(1.3*c.GetBottomMargin())

    # name_on_plot : text to put on top of the plot pad in addition to the region name so that
    # we know which sample is being plotted on the profile
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

    # move the stats box so it does not block the text on top
    st = h.FindObject("stats")
    st.SetY1NDC(0.93 * st.GetY1NDC())
    st.SetY2NDC(0.93 * st.GetY2NDC())

    # draw
    h.Draw()

    # draw descriptive text on top
  #  pu.draw_text_on_top(text="%s : #bf{%s}"%(plot.name, name_on_plot),pushup=1.035)
    pu.draw_text_on_top(text="%s : #bf{%s}"%(plot.name, name_on_plot))
    c.Update()

    r.gPad.RedrawAxis()

    # set output
    outname =  plot.name + ".eps"
    out = indir + "/plots/" + outdir
    c.SaveAs(outname)
    utils.mv_file_to_dir(outname, out, True)
    fullname = out + "/" + outname
    print "%s saved to : %s"%(outname, os.path.abspath(fullname)) 

def make_1dprofileRMS(plot, reg, data, backgrounds ) :
    print "make_1dprofileRMS    Plotting %s"%plot.name

    r.gStyle.SetOptStat(1100)

    # grab the plot's canvas and pretty up
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

            hist_name_x = ""
            hist_name_y = ""
            if "abs" in plot.xVariable :
                x_repl = plot.xVariable.replace("abs(","")
                x_repl = x_repl.replace(")","")
                hist_name_x = x_repl
            else : hist_name_x = plot.xVariable

            if "abs" in plot.yVariable :
                y_repl = plot.yVariable.replace("abs(","")
                y_repl = y_repl.replace(")","")
                hist_name_y = y_repl
            else : hist_name_y = plot.yVariable

            hx = pu.th1f("h_"+b.treename+"_"+hist_name_x, "", int(plot.n_binsX), plot.x_range_min, plot.x_range_max, plot.x_label, plot.y_label)
            hx.Sumw2
            cut = "(" + reg.tcut + ") * eventweight * " + str(b.scale_factor)
            cut = r.TCut(cut)
            sel = r.TCut("1")
            cmd = "%s>>+%s"%(plot.xVariable, hx.GetName())
            b.tree.Draw(cmd, cut * sel)

            g = r.TGraphErrors()

            for i in range(hx.GetNbinsX()) :
                hy = pu.th1f("h_" + b.treename + "_" + hist_name_y, "", 100, -200, 200,  plot.y_label, "")
                cut_up = hx.GetBinLowEdge(i+1) + hx.GetBinWidth(i+1)
                cut_down = hx.GetBinLowEdge(i+1) 
                cut = "(" + reg.tcut + " && ( %s >= %s && %s <= %s)"%(plot.xVariable, cut_down, plot.xVariable, cut_up)  + ") * eventweight * " + str(b.scale_factor) 
                cut = r.TCut(cut)
                sel = r.TCut("1")
                cmd = "%s>>%s"%(plot.yVariable, hy.GetName())
                b.tree.Draw(cmd, cut * sel)
                rms = hy.GetRMS()
                rms_err = hy.GetRMSError()
                g.SetPoint(i, hx.GetBinCenter(i+1), rms)
                g.SetPointError(i, 0.5*hx.GetBinWidth(i+1), rms_err)
                hy.Delete()
   
            g.SetMarkerStyle(8)
            g.SetMarkerSize(1.15 * g.GetMarkerSize())
            g.SetMarkerColor(r.TColor.GetColor("#E67067"))
            g.GetYaxis().SetRangeUser(plot.y_range_min, plot.y_range_max)

            g.Draw("ap")
            r.gPad.Update()
            g.Draw("ap") 
            g.GetYaxis().SetTitle(plot.y_label)
            g.GetXaxis().SetTitle(plot.x_label)
            

    if plot.sample == "Data" :
        name_on_plot = "Data"
        hist_name_x = ""
        hist_name_y = ""
        if "abs" in plot.xVariable :
            x_repl = plot.xVariable.replace("abs(","")
            x_repl = x_repl.replace(")","")
            hist_name_x = x_repl
        else : hist_name_x = plot.xVariable

        if "abs" in plot.yVariable :
            y_repl = plot.yVariable.replace("abs(","")
            y_repl = y_repl.replace(")","")
            hist_name_y = y_repl
        else : hist_name_y = plot.yVariable

        hx = pu.th1f("h_data_"+hist_name_x, "", int(plot.n_binsX), plot.x_range_min, plot.x_range_max, plot.x_label, plot.y_label)
        hx.Sumw2
        cut = "(" + reg.tcut + ") * eventweight"
        cut = r.TCut(cut)
        sel = r.TCut("1")
        cmd = "%s>>+%s"%(plot.xVariable, hx.GetName())
        data.tree.Draw(cmd, cut * sel)

        g = r.TGraphErrors()

        for i in range(hx.GetNbinsX()) :
            hy = pu.th1f("h_data_" + hist_name_y, "", 100, -200, 200,  plot.y_label, "")
            cut_up = hx.GetBinLowEdge(i+1) + hx.GetBinWidth(i+1)
            cut_down = hx.GetBinLowEdge(i+1) 
            cut = "(" + reg.tcut + " && ( %s >= %s && %s <= %s)"%(plot.xVariable, cut_down, plot.xVariable, cut_up)  + ") * eventweight" 
            cut = r.TCut(cut)
            sel = r.TCut("1")
            cmd = "%s>>%s"%(plot.yVariable, hy.GetName())
            data.tree.Draw(cmd, cut * sel)
            rms = hy.GetRMS()
            rms_err = hy.GetRMSError()
            g.SetPoint(i, hx.GetBinCenter(i+1), rms)
            g.SetPointError(i, 0.5*hx.GetBinWidth(i+1), rms_err)
            hy.Delete()

        g.SetMarkerStyle(8)
        g.SetMarkerSize(1.15 * g.GetMarkerSize())
        g.SetMarkerColor(r.TColor.GetColor("#5E9AD6"))
        g.GetYaxis().SetRangeUser(plot.y_range_min, plot.y_range_max)

        g.Draw("ap")
        r.gPad.Update()
        g.Draw("ap") 
        g.GetYaxis().SetTitle(plot.y_label)
        g.GetXaxis().SetTitle(plot.x_label)



    pu.draw_text_on_top(text="%s : #bf{%s}"%(plot.name, name_on_plot))
    c.Update()
    r.gPad.RedrawAxis()

    # set output
    outname = plot.name + ".eps"
    out = indir + "/plots/" + outdir
    c.SaveAs(outname)
    utils.mv_file_to_dir(outname, out, True)
    fullname = out + "/" + outname
    print "%s saved to : %s"%(outname, os.path.abspath(fullname))


def make_plots2D(plot, reg, data, backgrounds) :

    #check_2d_consistency(plot, data, backgrounds)

    # check if we want to do profile vs. TH2F plots
    if plot.do_profile : 
        make_1dprofile(plot, reg, data, backgrounds)
        return
    elif plot.do_profileRMS :
        make_1dprofileRMS(plot, reg, data, backgrounds)
        return
    print "make_plots2D    Plotting %s"%plot.name 

    # set the palette/colors 
    #pu.set_palette(name="redbluevector")
    pu.set_palette(name="")

    # get the canvas from the plot
    c = plot.canvas
    c.cd()
    # these should be in the default cavnas setting in utils/plot.py
    c.SetFrameFillColor(0)
    c.SetFillColor(0)
    c.SetLeftMargin(0.13)
    c.SetRightMargin(0.14)
    c.SetBottomMargin(1.3*c.GetBottomMargin())

    # name_on_plot : text to put on top of the plot pad in addition to the region name so that
    # we know which sample is being plotted on the TH2D
    name_on_plot = ""

    ### MC
    if plot.sample != "Data" :
        for b in backgrounds :
            if b.name != plot.sample : continue
            name_on_plot = b.displayname

            hist_name_x = ""
            hist_name_y = ""
            if "abs" in plot.xVariable :
                x_repl = plot.xVariable.replace("abs(","")
                x_repl = x_repl.replace(")","")
                hist_name_x = x_repl
            else : hist_name_x = plot.xVariable

            if "abs" in plot.yVariable :
                y_repl = plot.yVariable.replace("abs(","")
                y_repl = y_repl.replace(")","")
                hist_name_y = y_repl
            else : hist_name_y = plot.yVariable

            h = pu.th2f("h_"+b.name+"_"+hist_name_x+"_"+hist_name_y, "", int(plot.n_binsX), plot.x_range_min, plot.x_range_max, int(plot.n_binsY), plot.y_range_min, plot.y_range_max, plot.x_label, plot.y_label)

            # get the cut, and weight the sample (for TH2 the scale_factor is not so important if we normalize)     
            cut = "(" + reg.tcut + ") * eventweight * " + str(b.scale_factor)
            cut = r.TCut(cut)
            sel = r.TCut("1")
            cmd = "%s:%s>>+%s"%(plot.yVariable,plot.xVariable,h.GetName())
            b.tree.Draw(cmd, cut * sel)

    ### DATA
    if plot.sample == "Data" :
        name_on_plot = "Data"
        h = pu.th2f("h_"+data.name+"_"+plot.xVariable+"_"+plot.yVariable, "", int(plot.n_binsX), plot.x_range_min, plot.x_range_max, int(plot.n_binsY), plot.y_range_min, plot.y_range_max, plot.x_label, plot.y_label)

        cut = "(" + reg.tcut + ")"
        cut = r.TCut(cut)
        sel = r.TCut("1")
        cmd = "%s:%s>>+%s"%(plot.yVariable,plot.xVariable,h.GetName())
        data.tree.Draw(cmd, cut * sel)

    # normalize the histgrams to unity
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

    # write descriptive text on top of the pad
    pu.draw_text_on_top(text="%s : #bf{%s}"%(plot.name,name_on_plot))

    h.Draw(plot.style)
    pu.draw_text_on_top(text="%s : #bf{%s}"%(plot.name,name_on_plot))

    c.Update()

    # redraw the now-invisible axes ticks
    r.gPad.RedrawAxis()

    outname = plot.name+".eps"
    out = indir + "/plots/" + outdir
    c.SaveAs(outname)
    utils.mv_file_to_dir(outname, out, True)
    fullname = out + "/" + outname
    print "%s saved to : %s"%(outname, os.path.abspath(fullname)) 

def make_plots(plots, regions, data, backgrounds) :
    for reg in regions:
        # first check that there are plots for the given region
        plots_with_region = []
        for p in plots :
            if p.region == reg.simplename : plots_with_region.append(p)
        if len(plots_with_region)==0 : continue

        # set event lists, if they already exist load it. otherwise make it and save
        print "Setting EventLists for %s"%reg.simplename
        cut = reg.tcut
        cut = r.TCut(cut)
        sel = r.TCut("1")
        for b in backgrounds :
            list_name = "list_" + reg.simplename + "_" + b.treename
            save_name = "./" + indir + "/lists/" + list_name + ".root"

            # check if the list already exists
            if os.path.isfile(save_name) :
                rfile = r.TFile.Open(save_name)
                list = rfile.Get(list_name) 
                print "%s : EventList found at %s"%(b.name, os.path.abspath(save_name))
                if dbg : list.Print()
                b.tree.SetEventList(list)
            else :
                draw_list = ">> " + list_name
                b.tree.Draw(draw_list, sel*cut)
                list = r.gROOT.FindObject(list_name)
                b.tree.SetEventList(list)
                list.SaveAs(save_name)
                #list.SaveAs(list_name + ".root")
        # do data

        if data :
            data_list_name = "list_" + reg.simplename + "_" + data.treename
            data_save_name = "./" + indir + "/lists/" + data_list_name + ".root"
            if os.path.isfile(data_save_name) :
                #rfile = r.TFile.Open(data_list_name+".root")
                rfile = r.TFile.Open(data_save_name)
                data_list = rfile.Get(data_list_name)
                print "Data : EventList found at %s"%os.path.abspath(data_save_name)
                if dbg : data_list.Print()
                data.tree.SetEventList(data_list)
            else :
                draw_list = ">> " + data_list_name
                data.tree.Draw(draw_list, sel * cut)
                data_list = r.gROOT.FindObject(data_list_name)
                data.tree.SetEventList(data_list)
                #data_list.SaveAs(data_list_name+".root")
                data_list.SaveAs(data_save_name)

        # now check if we want to do a 1D or 2D plot
        for p in plots_with_region :
            if not p.is2D : make_plots1D(p, reg, data, backgrounds) 
            elif p.is2D : make_plots2D(p, reg, data, backgrounds)

def print_usage() :

    print "\nUsage"
    print "     -i (--indir)      : provide the name of the directory containing the config, plots, and lists directories"
    print "     -c (--plotConfig) : provide the name of the config file (without '.py')"
    print "     -r (--requestRegion) : request a region to plot -- will make all plots in the config that are in this region"
    print "     -p (--requestPlot) : request a specific plot -- provide the name of the plot"
    print "     -o (--outdir) : provide the name of the output directory to save the plots "
    print "                      --> will be under 'indir/plots/' "
    print "     -d (--dbg) : set debug/verbosity to True"
    sys.exit()

if __name__=="__main__" :
    global indir, plotConfig, requestRegion, requestPlot, outdir, dbg
    parser = OptionParser()
    parser.add_option("-c", "--plotConfig", dest="plotConfig",default="")
    parser.add_option("-s", "--doSys", action="store_true", dest="doSys", default=False)
    parser.add_option("-i", "--indir", dest="indir", default="")
    parser.add_option("-r", "--requestRegion", dest="requestRegion", default="")
    parser.add_option("-p", "--requestPlot", dest="requestPlot", default="")
    parser.add_option("-o", "--outdir", dest="outdir", default="./")
    parser.add_option("-d", "--dbg", action="store_true", dest="dbg", default=False)
    parser.add_option("-u", "--usage", action="store_true", dest="usage", default=False)
    (options, args) = parser.parse_args()
    indir           = options.indir
    plotConfig      = options.plotConfig
    doSys           = options.doSys
    requestRegion   = options.requestRegion
    requestPlot     = options.requestPlot
    outdir          = options.outdir
    dbg             = options.dbg
    usage           = options.usage
    if usage : print_usage()

    if requestRegion != "" and requestPlot != "" :
        print 'ERROR    You have requested both a reagion ("%s") AND a plot ("%s").'%(requestRegion, requestPlot)
        print 'ERROR    You may only request one at a time. Exitting.'
        sys.exit()

    print " ++ ------------------------- ++ "
    print "      plotter                    "
    print "                                 "
    print " config directory :  %s          "%indir
    print " plot config      :  %s          "%plotConfig
    print " requested region :  %s          "%requestRegion
    print " requested plot   :  %s          "%requestPlot
    print " systematics      :  %s          "%doSys
    print " output directory :  %s          "%outdir
    print " debug            :  %s          "%dbg
    print "                                 "
    print " ++ ------------------------- ++ \n"

    # get the config file
    conf_file = get_plotConfig(plotConfig)
    print "Found the configuration file: %s"%conf_file
    plots = []
    data = None
    backgrounds = []
    systematics = []
    regions = []
    execfile(conf_file)

    check_for_consistency(plots, regions)

    # print out the loaded backgrounds and plots
    if dbg :
        for p in plots :
            p.Print()
    print "+-----------------------+ "
    print "  Loaded backgrounds:    "
    for b in backgrounds :
        b.Print()
    print "  Loaded data sample:    "
    if data : data.Print()
    print "+-----------------------+ "
    if doSys :
        print "+-----------------------+ "
        print "  Loaded systematics:     "
        for s in systematics :
            s.check()
            s.Print()
            for b in backgrounds :
                b.addSys(s)
                if dbg :
                    for s in b.systList :
                        print s.tree
        print "+-----------------------+ "


    # make the plots
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
