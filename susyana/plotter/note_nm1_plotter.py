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

from array import array


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

def set_event_lists(reg, backgrounds, data) :
    # set event lists, if they already exist load it. otherwise make it and save
    print "Setting EventLists for %s"%reg.name
    cut = reg.tcut
    cut = r.TCut(cut)
    sel = r.TCut("1")
    for b in backgrounds :
        list_name = "list_" + reg.name + "_" + b.treename
        save_name = "./" + indir + "/lists/" + list_name + ".root"
        print list_name
    
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
    
    # systematics trees
    if doSys :
        cut = reg.tcut
        cut = r.TCut(cut)
        sel = r.TCut("1")
        for b in backgrounds :
            if 'fakes' in b.name : continue
            for s in b.systList :
                if not s.isKinSys() : continue
    
                # up variation
                list_name_up = "list_" + reg.name + "_" + b.treename + "_" + s.name + "_UP"
                save_name_up = "./" + indir + "/lists/" + list_name_up + ".root"
    
                if os.path.isfile(save_name_up) :
                    rfile = r.TFile.Open(save_name_up)
                    list = rfile.Get(list_name_up)
                    print "%s : EventList found at %s"%(b.name, os.path.abspath(save_name_up))
                    if dbg : list.Print()
                    s.tree_up.SetEventList(list)
                else :
                    draw_list = ">> " + list_name_up
                    s.tree_up.Draw(draw_list, sel*cut)
                    list = r.gROOT.FindObject(list_name_up)
                    s.tree_up.SetEventList(list)
                    list.SaveAs(save_name_up)
    
                # down variation
                    
                list_name_dn = "list_" + reg.name + "_" + b.treename + "_" + s.name + "_DN"
                save_name_dn = "./" + indir + "/lists/" + list_name_dn + ".root"
    
                if not s.isOneSided() :
                    if os.path.isfile(save_name_dn) :
                        rfile = r.TFile.Open(save_name_dn)
                        list = rfile.Get(list_name_dn)
                        print "%s : EventList found at %s"%(b.name, os.path.abspath(save_name_dn))
                        if dbg : list.Print()
                        s.tree_down.SetEventList(list)
                    else :
                        draw_list = ">> " + list_name_dn
                        s.tree_down.Draw(draw_list, sel*cut)
                        list = r.gROOT.FindObject(list_name_dn)
                        s.tree_down.SetEventList(list)
                        list.SaveAs(save_name_dn)
    
    # do data
    
    if data :
        data_list_name = "list_" + reg.name + "_" + data.treename
        data_save_name = "./" + indir + "/lists/" + data_list_name + ".root"
        if os.path.isfile(data_save_name) :
            #rfile = r.TFile.Open(data_list_name+".root")
            rfile = r.TFile.Open(data_save_name)
            data_list = rfile.Get(data_list_name)

def getSystHists(plot, reg, b, nom_yield, nom_hist) :
    for s in b.systList :
        hist_name = "MDR"
        h_up = nom_hist.Clone("h_"+b.treename+"_"+hist_name+"_"+s.name+"_up")
        h_dn = nom_hist.Clone("h_"+b.treename+"_"+hist_name+"_"+s.name+"_dn")

        h_up.SetMinimum(plot.y_range_min)
        h_up.SetMaximum(plot.y_range_max)
        h_up.GetXaxis().SetLabelOffset(-999)
        h_up.GetXaxis().SetTitleOffset(-999)
        h_dn.SetMinimum(plot.y_range_min)
        h_dn.SetMaximum(plot.y_range_max)
        h_dn.GetXaxis().SetLabelOffset(-999)
        h_dn.GetXaxis().SetTitleOffset(-999)

        for hsys in [h_up, h_dn] :
            yax = hsys.GetYaxis()
            xax = hsys.GetXaxis()

            yax.SetTitleSize(0.05)
            yax.SetLabelSize(0.045)
            yax.SetLabelOffset(0.008)
            yax.SetTitleOffset(1.2)
            yax.SetLabelFont(42)
            yax.SetTitleFont(42)
            yax.SetNdivisions(5) 
        
        if s.isWeightSys() :
            name_up = s.up_name
            name_up = "syst_" + name_up.replace('syst_', "")
            name_dn = s.down_name
            name_dn = "syst_" + name_dn.replace('syst_', "")
            weight_up = ""
            weight_dn = ""
            if "PILEUPUP" in name_up :
                weight_up = " eventweightNOPUPW * pupw_up "
            else :
                weight_up = " eventweight * %s"%(str(name_up))
            if "PILEUPDOWN" in name_dn :
                weight_dn = " eventweightNOPUPW * pupw_down "
            else :
                weight_dn = " eventweight * %s"%(str(name_dn))

            norm_factor = "1"
            if "ttbar" in b.name :
                norm_factor = "0.99"
            elif "vv" in b.name  and "SF" in reg.name :
                norm_factor = "1.27"
            elif "vv" in b.name and "SF" not in reg.name :
                norm_factor = "1.23"

            cut_up = "(" + reg.tcut + ") * %s * %s *%s"%(weight_up, str(b.scale_factor), norm_factor)
            cut_dn = "(" + reg.tcut + ") * %s * %s *%s"%(weight_dn, str(b.scale_factor), norm_factor)
            #cut_up = "(" + reg.tcut + ") * eventweight * " + str(name_up) + " * " + str(b.scale_factor)
            #cut_dn = "(" + reg.tcut + ") * eventweight * " + str(name_dn) + " * " + str(b.scale_factor)

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

            norm_factor = "1"
            if "ttbar" in b.name :
                norm_factor = "0.99"
            elif "vv" in b.name  and "SF" in reg.name :
                norm_factor = "1.27"
            elif "vv" in b.name and "SF" not in reg.name :
                norm_factor = "1.23"

            cut = "(" + reg.tcut + ") * eventweight * %s * %s"%(str(b.scale_factor), norm_factor)
            cut = r.TCut(cut)
            sel = r.TCut("1")
            cmd_up = "%s>>%s"%(plot.variable, h_up.GetName())
            cmd_dn = "%s>>%s"%(plot.variable, h_dn.GetName())

            s.tree_up.Draw(cmd_up, cut * sel)
            pu.add_overflow_to_lastbin(h_up)
            s.up_histo = h_up

            is_one_side = False
            if "JER" in syst.name : is_one_side = True
            if "ResoPerp" in syst.name or "ResoPara" in syst.name : is_one_side = True
            if not s.isOneSided() :
            #if not is_one_side :
                s.tree_down.Draw(cmd_dn, cut * sel)
                pu.add_overflow_to_lastbin(h_dn)
                s.down_histo = h_dn
            else :
                s.down_histo = nom_hist.Clone("%s_down_hist"%s.name)
                h_dn = s.down_histo

            if s.isOneSided() :
                print "    %s (+%.2f, -%.2f)"%(s.name, h_up.Integral(0,-1)-nom_yield, nom_yield-h_dn.Integral(0,-1))
            else :
                print "    %s  (+%.2f, -%.2f)"%(s.name, h_up.Integral(0,-1)-nom_yield, nom_yield-h_dn.Integral(0,-1))


def make_MDR_nm1_plot(reg, backgrounds, data) :

    print "make_MDR_nm1_plot    %s"%reg.name

    #mdr_nice = "E_{V}^{P} [GeV]"
    mdr_nice = "M_{#Delta}^{R} [GeV]"

    p = plot.Plot1D()
    p.initialize(reg.name, "MDR", "%s_MDR"%(reg.name))
    p.labels(x=mdr_nice, y = "Entries")
    if reg.name == "srwNM1" :
        p.yax(0.1, 10000)
    elif reg.name == "srwNM1SF" :
        p.yax(0.1, 20000)
    elif reg.name == "srtNM1" :
        p.yax(0.1, 50000)
    elif reg.name == "srtNM1SF" :
        p.yax(0.1, 50000)
    p.doLogY = True
    p.setRatioCanvas(p.name)

    ### canvas get
    rcan = p.ratioCanvas
    rcan.canvas.cd()
    rcan.upper_pad.cd()

    if p.isLog() : rcan.upper_pad.SetLogy(True)
    rcan.upper_pad.Update()

    binlow = []
    if reg.name == "srwNM1":
        binlow = [80,95,110,130,150,180]#100,140]#,130]#,130]#75,90,110,130,160]
    elif reg.name == "srwNM1SF" :
        binlow = [80,95,110,130,150,180]
        #binlow = [80,95,110,130,150,180,200]
    elif reg.name == "srtNM1" :
        binlow = [70,80,95,110,130,150,180]#100,140]#,130]#,130]#75,90,110,130,160]
    elif reg.name == "srtNM1SF" :
        binlow = [70,80,95,110,130,150,180]
        #binlow = [70,80,95,110,130,150,180,200]
        #binlow = [70,80,90,100,110,120,130,140,150,160,170,180,200]

    hax = r.TH1F("axes", "", len(binlow)-1, array('d',binlow))
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

    stack = r.THStack("stack_"+p.name,"")

    # legend
    leg = pu.default_legend(xl=0.55,yl=0.71,xh=0.93,yh=0.90)
    #leg = pu.default_legend(xl=0.55,yl=0.65,xh=0.93,yh=0.90)
    leg.SetNColumns(2)

    # histos
    histos = []
    h_nom_fake = None

    n_total_sm_yield = 0.
    for b in backgrounds :
        if b.isSignal() : continue
        if "data" in b.name.lower() : continue
        hist_name = "MDR"
        h = r.TH1F("h_" + b.treename+"_"+hist_name, "", len(binlow)-1, array('d',binlow))
        font = 42
        h.SetTitleFont(font)

        #x-axis
        xx = h.GetXaxis()
        xx.SetTitle(p.x_label)
        xx.SetTitleOffset(1.2*xx.GetTitleOffset())
        xx.SetTitleFont(font)
        xx.SetLabelFont(font)

        #y-axis
        yy = h.GetYaxis()
        yy.SetTitle(p.y_label)
        yy.SetTitleOffset(1.2*yy.GetTitleOffset())
        yy.SetTitleFont(font)
        yy.SetLabelFont(font)

        h.Sumw2()

        h.SetLineColor(b.color) # stop2L people have no sense
        #h.SetLineColor(r.kBlack)
        h.GetXaxis().SetLabelOffset(-999)
        h.SetFillColor(b.color)
        h.SetFillStyle(1001)

        # cuts
        weight_str = ""
        if "fakes" in b.name :
            weight_str = "FakeWeight"
        else :
            weight_str = "eventweight"

        norm_factor = "1"
        if "ttbar" in b.name :
            norm_factor = "0.99"
        elif "vv" in b.name  and "SF" in reg.name :
            norm_factor = "1.23"
        elif "vv" in b.name and "SF" not in reg.name :
            norm_factor = "1.27"
        cut = "(" + reg.tcut + ") * %s * %s * %s"%(weight_str, str(b.scale_factor), norm_factor)
        cut = r.TCut(cut)
        sel = r.TCut("1")
        cmd = "%s>>+%s"%(p.variable, h.GetName())
        blah = b.tree.Draw(cmd, cut * sel, "goff")

        # print yields
        stat_err = r.Double(0.0)
        integral = h.IntegralAndError(0,-1,stat_err)
        n_total_sm_yield += float(integral)
        print "%s: %.2f +/- %.2f"%(b.name, integral, stat_err)

        # get variation histos
        if doSys and 'fakes' not in b.name and (integral>0)  : getSystHists(p, reg, b, integral, h)
        #if doSys and 'fakes' not in b.name and (integral>0) and "zjets" not in b.name : getSystHists(p, reg, b, integral, h)

        # add overflow
        pu.add_overflow_to_lastbin(h)

        # set negative bin yields to 0
        for ibin in xrange(h.GetXaxis().GetNbins()) :
            if h.GetBinContent(ibin+1) < 0. :
                print "Setting bin %d for %s to 0"%(ibin, b.name)
                h.SetBinContent(ibin+1, 0)
                h.SetBinError(ibin+1,0)

        if "fakes" in b.name :
            h_nom_fake = h.Clone("fakes_nominal_histo")

        leg.AddEntry(h, b.displayname, "f")
        if integral > 0 :
            histos.append(h)
        rcan.upper_pad.Update()


    # order the histos
    histos = sorted(histos, key=lambda h: h.Integral(), reverse=False)
    for h in histos :
        stack.Add(h)
    rcan.upper_pad.Update()
    #hist_sm = stack.GetStack().Last().Clone("hist_sm")
        

    # now get the data points
    hd = r.TH1F("h_data_"+reg.name,"", len(binlow)-1, array('d',binlow))
    hd.Sumw2()
    cut = "(" + reg.tcut + ")"
    cut = r.TCut(cut)
    sel = r.TCut("1")
    cmd = "%s>>+%s"%(p.variable, hd.GetName()) 
    data.tree.Draw(cmd, cut * sel, "goff")
    hd.GetXaxis().SetLabelOffset(-999)

    print "Total SM: %.2f"%(n_total_sm_yield)

    # print yeild +/- stat err
    stat_err = r.Double(0.0)
    integral = hd.IntegralAndError(0,-1,stat_err)
    print "Data: %.2f +/- %.2f"%(integral, stat_err)
    pu.add_overflow_to_lastbin(hd)

    gdata = pu.convert_errors_to_poisson(hd)
    gdata.SetLineWidth(2)
    gdata.SetMarkerStyle(20)
    gdata.SetMarkerSize(1.5)
    #gdata.SetMarkerSize(1.1)
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
    mcError.SetLineWidth(3)
    leg.AddEntry(mcError, "Total SM", "fl")

    # histogram for total stack
    totalSM = stack.GetStack().Last().Clone("totalSM")
    nominalAsymErrors = pu.th1_to_tgraph(totalSM)
    nominalAsymErrors.SetMarkerSize(0)
    nominalAsymErrors.SetLineWidth(0)
    nominalAsymErrors.SetFillStyle(3354)
    nominalAsymErrors.SetFillColor(r.kGray + 3)
   # leg.AddEntry(nominalAsymErrors, "Bkg. Uncert.", "f")


    tmp = []
    backgrounds_original = backgrounds
    for b in backgrounds :
        if "bwn" in b.name : continue
        if "fakes" in b.name : continue
        #if "zjets" in b.name : continue
        tmp.append(b)
    backgrounds = tmp
    if doSys :
        # totalSystHisto will hold each samples'
        # variation
        totalSysHisto = totalSM.Clone()
        totalSysHisto.Reset("ICE")
        transient = r.TGraphAsymmErrors()

        # add to the error band the contribution from the up-variations 
        systematics_up = [s.up_name for s in backgrounds[0].systList]
        for up_sys in systematics_up :

            new_name = ""
            if "syst_" in up_sys :
                new_name = "syst_" + up_sys.replace("syst_","")
            else :
                new_name = up_sys
            up_sys = new_name

            transient = r.TGraphAsymmErrors()
            transient.Clear()
            for b in backgrounds :
                #if b.name in avoid_bkg : continue
                #if "zjets" in b.name : continue
                if "bwn" in b.name : continue
                if b.isSignal() : continue
                if 'fakes' in b.name : continue
                for syst in b.systList :
                    if "EG_SCALE_ALL" in syst.up_name  and "zjets" in b.name : continue

                    new_name = ""
                    if "syst_" in syst.up_name :
                        new_name = "syst_" + syst.up_name.replace("syst_","")
                    else :
                        new_name = syst.up_name
                    syst.up_name = new_name

                    if syst.up_name != up_sys : continue
                    #print "[%s] adding %s to up histo : %.2f (%.2f)"%(up_sys, b.name, syst.up_histo.Integral(), totalSM.Integral())
                    totalSysHisto.Add(syst.up_histo)
            if h_nom_fake :
                totalSysHisto.Add(h_nom_fake)
            transient = pu.th1_to_tgraph(totalSysHisto)
            #print " > %s: %s"%(b.name, up_sys)
            pu.add_to_band(transient, nominalAsymErrors)#, up_sys)
            totalSysHisto.Reset()

        # add to the error band the contribution from the down-variations
        systematics_down = [s.down_name for s in backgrounds[0].systList]
        for dn_sys in systematics_down :

            new_name = ""
            if "syst_" in dn_sys :
                new_name = "syst_" + dn_sys.replace("syst_","")
            else :
                new_name = dn_sys
            dn_sys = new_name

            transient = r.TGraphAsymmErrors()
            transient.Clear()
            for b in backgrounds :
                #if "zjets" in b.name : continue
                if "bwn" in b.name : continue
                #if b.name in avoid_bkg : continue
                if b.isSignal() : continue
                if 'fakes' in b.name : continue
                for syst in b.systList :
                    if "EG_SCALE_ALL" in syst.down_name  and "zjets" in b.name : continue

                    new_name = ""
                    if "syst_" in syst.down_name :
                        new_name = "syst_" + syst.down_name.replace("syst_","")
                    else :
                        new_name = syst.down_name
                    syst.down_name = new_name

                    if syst.down_name != dn_sys : continue
                    #print "[%s] adding %s to down histo : %.2f"%(dn_sys, b.name, syst.down_histo.Integral())
                   # if syst.isOneSided() : continue

                   # if "JER" in syst.name : continue
                   # if "ResoPerp" in syst.name or "ResoPara" in syst.name : continue
                    totalSysHisto.Add(syst.down_histo)
            if h_nom_fake :
                totalSysHisto.Add(h_nom_fake)
            transient = pu.th1_to_tgraph(totalSysHisto)
            #print " > %s: %s"%(b.name, dn_sys)
            pu.add_to_band(transient, nominalAsymErrors)#, dn_sys)
            totalSysHisto.Reset()

    # draw mc stack
    stack.Draw("HIST SAME")
    stack.SetMinimum(p.y_range_min)
    stack.SetMaximum(p.y_range_max)
    rcan.upper_pad.Update()

    # draw the error band
    nominalAsymErrors.Draw("same && E2")
    
    # draw the total bkg line
    hist_sm = stack.GetStack().Last().Clone("hist_sm")
    hist_sm.SetLineColor(r.TColor.GetColor("#FC0F1D"))
    hist_sm.SetLineWidth(mcError.GetLineWidth())
    hist_sm.SetLineStyle(1)
    hist_sm.SetFillStyle(0)
    hist_sm.Draw("hist same")


    ####################################
    # plot signal
    leg_sig = pu.default_legend(xl=0.55,yl=0.56,xh=0.91,yh=0.71)
    #leg_sig = pu.default_legend(xl=0.55,yl=0.35,xh=0.93,yh=0.60)
    leg_sig.SetNColumns(1)
    sig_histos = []
    for s in backgrounds_original :
        if not s.isSignal() : continue
        hist_name = "MDR"
        h = r.TH1F("h_" + b.treename+"_"+hist_name, "", len(binlow)-1, array('d',binlow))
        h.SetLineWidth(2)
        h.SetLineStyle(2)
        h.SetLineColor(s.color)
        h.GetXaxis().SetLabelOffset(-999)
        h.SetFillStyle(0)
        h.Sumw2()

        # cut and make the sample weighted, applying the scale_factor
        cut = "(" + reg.tcut + ") * eventweightNOPUPW * susy3BodyRightPol *" + str(s.scale_factor)
        cut = r.TCut(cut)
        sel = r.TCut("1")
        cmd = "%s>>+%s"%(p.variable, h.GetName())
        s.tree.Draw(cmd, cut * sel, "goff")

        # print the yield +/- stat error
        stat_err = r.Double(0.0)
        integral = h.IntegralAndError(0,-1,stat_err)
        print "%s: %.2f +/- %.2f"%(s.name, integral, stat_err)
        
        # add overflow
        pu.add_overflow_to_lastbin(h)

        #h_dummy = r.TH1F("dummy","",2,0,2)
        #h_dummy.SetFillStyle(1001)
        #h_dummy.SetFillColor(r.kWhite)
        #h_dummy.SetLineColor(r.kWhite)

        leg_sig.AddEntry(h, s.displayname, "l")
        #leg_sig.AddEntry(h_dummy, "", "fl")
        sig_histos.append(h)
        rcan.upper_pad.Update()

    # draw the signals
    for hsig in sig_histos :
        hsig.Draw("hist same")

    # draw the dta graph
    gdata.Draw("option same pz 0")
    leg.Draw()
    leg_sig.Draw()
    r.gPad.RedrawAxis()

    # add some text/labels
    #pu.draw_text(text="#it{ATLAS} Preliminary",x=0.18,y=0.85, size=0.06)
    pu.draw_text(text="ATLAS",x=0.18,y=0.85,size=0.06,font=72)
    pu.draw_text(text="Preliminary",x=0.325,y=0.85,size=0.06,font=42)
    pu.draw_text(text="L = 13.3 fb^{-1}, #sqrt{s} = 13 TeV",x=0.18,y=0.79, size=0.04)
    pu.draw_text(text=reg.displayname,      x=0.18,y=0.74, size=0.04)

    r.gPad.SetTickx()
    r.gPad.SetTicky()

    rcan.canvas.Update()

    ########################################
    # lower pad
    ########################################
    rcan.lower_pad.cd()

    # get the total SM histo
    h_sm = stack.GetStack().Last().Clone("h_sm")

    # yaxis
    yax = h_sm.GetYaxis()
    yax.SetRangeUser(0,2)
    yax.SetTitle("Data/SM")
    
    yax.SetTitleSize(0.14 * 0.83)
    yax.SetLabelSize(0.13 * 0.81)
    yax.SetLabelOffset(0.98 * 0.013 * 1.08)
    yax.SetTitleOffset(0.45 * 1.2)
    yax.SetLabelFont(42)
    yax.SetTitleFont(42)
    yax.SetNdivisions(5) 

#    print "title size: ", yax.GetTitleSize()
#    print "label size : ", yax.GetLabelSize()
#    print "lab off      : ", yax.GetLabelOffset()
#    print "title off        : ", yax.GetTitleOffset()
    
    # xaxis
    xax = h_sm.GetXaxis()
    xax.SetTitleSize(1.1 * 0.14)
    xax.SetLabelSize(yax.GetLabelSize())
    #xax.SetLabelSize(0.13)
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
    pu.draw_line(binlow[0], 1.0, binlow[-1], 1.0,color=r.kRed,style=2,width=1)
    pu.draw_line(binlow[0], 0.5, binlow[-1], 0.5,style=3,width=1)
    pu.draw_line(binlow[0], 1.5, binlow[-1], 1.5,style=3,width=1)

    # convert to tgraphs to get the ratio
    #g_data = pu.th1_to_tgraph(hd)
    g_data = pu.convert_errors_to_poisson(hd)
    #g_data = gdata
    g_sm = pu.th1_to_tgraph(h_sm)
    g_ratio = pu.tgraphAsymmErrors_divide(g_data, g_sm)

    # For Data/MC only use the statistical error for data
    # since we explicity draw the MC error band
    nominalAsymErrorsNoSys = r.TGraphAsymmErrors(nominalAsymErrors)
    for i in xrange(nominalAsymErrorsNoSys.GetN()) :
        nominalAsymErrorsNoSys.SetPointError(i,0,0,0,0)
        #nominalAsymErrorsNoSys.SetPointError(i-1,0,0,0,0)
    ratio_raw = pu.tgraphAsymmErrors_divide(g_data, nominalAsymErrorsNoSys)
    ratio = r.TGraphAsymmErrors() 

    x1, y1 = r.Double(0.0), r.Double(0.0)
    index = 0
    for i in xrange(ratio_raw.GetN()) :
        ratio_raw.GetPoint(i, x1, y1)
       # print "raw: (i, x, y) = (%d, %f, %f)"%(int(i),float(x1),float(y1))
       # xx, yy = r.Double(0.0), r.Double(0.0)
       # xn, yn = r.Double(0.0), r.Double(0.0)
       # xg, yg = r.Double(0.0), r.Double(0.0)
       # g_data.GetPoint(i, xx, yy)
       # nominalAsymErrorsNoSys.GetPoint(i, xn, yn)
       # g_sm.GetPoint(i, xg, yg)
       # print "gdata: (i, x, y) = (%d, %f, %f)"%(int(i),float(xx),float(yy))
       # print "nomAs: (i, x, y) = (%d, %f, %f)"%(int(i),float(xn),float(yn))
       # print "g_sm : (i, x, y) = (%d, %f, %f)"%(int(i),float(xg),float(yg))
        x_, y_ = r.Double(0.0), r.Double(0.0)
        xx, yy = r.Double(0.0), r.Double(0.0)
        xr, yr = r.Double(0.0), r.Double(0.0)
        g_data.GetPoint(i, x_, y_)
        gdata.GetPoint(i, xx, yy)
        g_ratio.GetPoint(i, xr, yr)
        print "gdata   (%f,%f) EYH : %f    EYL: %f"%(xx, yy, gdata.GetErrorYhigh(i), gdata.GetErrorYlow(i))
        print "g_data  (%f,%f) EYH : %f    EYL: %f"%(x_, y_, g_data.GetErrorYhigh(i), g_data.GetErrorYlow(i)) 
        print "g_ratio (%f,%f) EYH: %f    EYL: %f"%(xr, yr, g_ratio.GetErrorYhigh(i), g_ratio.GetErrorYlow(i))
        print 50*"-"
        if y1 > 0. :
            ratio.SetPoint(index, x1, y1)
            ratio.SetPointError(index, ratio_raw.GetErrorXlow(i), ratio_raw.GetErrorXhigh(i), ratio_raw.GetErrorYlow(i), ratio_raw.GetErrorYhigh(i))
            index+=1
    #print "SETTING RATIO_RAW TO RATIO"
    #ratio = ratio_raw
    ratio.SetLineWidth(2)
    ratio.SetMarkerStyle(20)
    ratio.SetMarkerSize(1.5)
    #ratio.SetMarkerSize(1.1)
    ratio.SetLineColor(1)
    ratio.SetMarkerSize(1.5)
    ratio.Draw("option pz 0")
    rcan.lower_pad.Update()

    ratioBand.Draw("same && E2")
    rcan.lower_pad.Update()
    



    #########################################
    # save
    #########################################
    outname = p.name + "_prelim.eps"
    rcan.canvas.SaveAs(outname)
    out = indir + "/plots/" + outdir
    utils.mv_file_to_dir(outname, out, True)
    fullname = out + "/" + outname
    print "%s saved to : %s"%(outname, os.path.abspath(fullname))




if __name__=="__main__" :
    global indir, plotConfig, requestRegion, outdir, dbg
    parser = OptionParser()
    parser.add_option("-c", "--plotConfig", dest="plotConfig",default="")
    parser.add_option("-s", "--doSys", action="store_true", dest="doSys", default=False)
    parser.add_option("-i", "--indir", dest="indir", default="")
    parser.add_option("-r", "--requestRegion", dest="requestRegion", default="")
    parser.add_option("-o", "--outdir", dest="outdir", default="./")
    parser.add_option("-d", "--dbg", action="store_true", dest="dbg", default=False)
    parser.add_option("-u", "--usage", action="store_true", dest="usage", default=False)
    (options, args) = parser.parse_args()
    indir           = options.indir
    plotConfig      = options.plotConfig
    doSys           = options.doSys
    requestRegion   = options.requestRegion
    outdir          = options.outdir
    dbg             = options.dbg
    usage           = options.usage
    if usage : print_usage()


    print " ++ ------------------------- ++ "
    print "      NM1 plotter                "
    print "                                 "
    print " config directory :  %s          "%indir
    print " plot config      :  %s          "%plotConfig
    print " requested region :  %s          "%requestRegion
    print " systematics      :  %s          "%doSys
    print " output directory :  %s          "%outdir
    print " debug            :  %s          "%dbg
    print "                                 "
    print " ++ ------------------------- ++ \n"

    # get the config file
    conf_file = get_plotConfig(plotConfig)
    print "Found the configuration file: %s"%conf_file
    data = None
    backgrounds = []
    systematics = []
    regions = []
    execfile(conf_file)


    # print out the loaded backgrounds and plots
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
                if b.isSignal() : continue
                b.addSys(s)
                if dbg :
                    for s in b.systList :
                        print s.tree
        print "+-----------------------+ "

    # make the plots
    found_request = False
    for r_ in regions :
        if  requestRegion == r_.name : found_request = True
    if not found_request :
        print "did not find requested region"
        sys.exit()

    for r_ in regions :
        if r_.name == requestRegion : 
            set_event_lists(r_, backgrounds, data)
            make_MDR_nm1_plot(r_, backgrounds, data)


#    if requestRegion != "" :
#        requested_plots = []
#        for p in plots :
#            if p.region == requestRegion : requested_plots.append(p)
#        make_plots(requested_plots, regions, data, backgrounds)
#    elif requestPlot != "" :
#        requested_plots = []
#        for p in plots :
#            if p.name == requestPlot : requested_plots.append(p)
#        make_plots(requested_plots, regions, data, backgrounds)
#    else :
#        make_plots(plots, regions, data, backgrounds)
#
