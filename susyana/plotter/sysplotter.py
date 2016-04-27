
from optparse import OptionParser
import os

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(False)
import sys
sys.path.append(os.environ['SUSYDIR'])

r.TEventList.__init__._creates = False
r.TH1F.__init__._creates = False
r.TGraphErrors.__init__._creates = False
r.TGraphAsymmErrors.__init__._creates = False
r.TCanvas.__init__._creates = False


import supersusy.utils.plot_utils as pu
import supersusy.utils.utils as utils
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
        for blah in bad_regions :
            print blah.simplename
        print 'check_for_consistency ERROR    The regions that are defined in the configuration ("%s") are:'%plotConfig
        print configured_regions
        print "check_for_consistency ERROR    Exitting."
        sys.exit()
    else :
        print "check_for_consistency    Plots and regions consistent."

################################################################
def getSystHistos(plot_, reg, bkg, syst, histname) :

    var_yields = []

    h_up = pu.th1f("h_"+bkg.treename+"_"+histname+"_"+syst.name+"_up","", int(plot_.nbins), plot_.x_range_min, plot_.x_range_max, plot_.x_label, plot_.y_label)
    h_up.SetFillStyle(0)
    h_up.SetLineColor(46)
    h_dn = pu.th1f("h_"+bkg.treename+"_"+histname+"_"+syst.name+"_dn","", int(plot_.nbins), plot_.x_range_min, plot_.x_range_max, plot_.x_label, plot_.y_label)
    h_dn.SetFillStyle(0)
    h_dn.SetLineColor(38)
        

    if syst.isWeightSys() :
        #weight_up = "eventweight * pupw_up"
        #weight_dn = "eventweight * pupw_down"
        #weight_up = "eventweight * pupw * syst_PILEUPUP"
        #weight_dn = "eventweight * pupw * syst_PILEUPDOWN"
        #cut_up = "(" + reg.tcut + ") * " + weight_up + " * " + str(bkg.scale_factor)
        #cut_dn = "(" + reg.tcut + ") * " + weight_dn + " * " + str(bkg.scale_factor)

        cut_up = "(" + reg.tcut + ") * eventweight * " + str(syst.up_name) + " * " + str(bkg.scale_factor)
        cut_dn = "(" + reg.tcut + ") * eventweight * " + str(syst.down_name) + " * " + str(bkg.scale_factor)
        cut_up = r.TCut(cut_up)
        cut_dn = r.TCut(cut_dn)
        sel = r.TCut("1")

        cmd_up = "%s>>%s"%(plot_.variable, h_up.GetName())
        cmd_dn = "%s>>%s"%(plot_.variable, h_dn.GetName())

        syst.tree.Draw(cmd_up, cut_up * sel)
        syst.tree.Draw(cmd_dn, cut_dn * sel)

        ## overflow
        pu.add_overflow_to_lastbin(h_up)
        pu.add_overflow_to_lastbin(h_dn)


        var_yields.append(h_up.Integral(0,-1))
        var_yields.append(h_dn.Integral(0,-1))

        syst.up_histo = h_up
        syst.down_histo = h_dn

    elif syst.isKinSys() :
        cut = "(" + reg.tcut + ") * eventweight * " + str(bkg.scale_factor)
        cut = r.TCut(cut)
        sel = r.TCut("1")
        cmd_up = "%s>>%s"%(plot_.variable, h_up.GetName())
        cmd_dn = "%s>>%s"%(plot_.variable, h_dn.GetName())

        syst.tree_up.Draw(cmd_up, cut*sel)
        pu.add_overflow_to_lastbin(h_up)
        syst.up_histo = h_up
        var_yields.append(h_up.Integral(0,-1))
        if "JER" not in syst.name :
       # if not syst.isOneSided() or "JER" in syst.name :
            syst.tree_down.Draw(cmd_dn, cut*sel)
            pu.add_overflow_to_lastbin(h_dn)
            syst.down_histo = h_dn
            var_yields.append(h_dn.Integral(0,-1))

    return var_yields




################################################################
##
def make_sys_plot(plot_, region, bkg_list, sys_list) :

    # canvases
    rcan = plot_.ratioCanvas
    rcan.canvas.cd()
    rcan.upper_pad.cd()

    if plot_.isLog() : rcan.upper_pad.SetLogy(True)
    rcan.upper_pad.Update()

    # stack for MC
    hax = r.TH1F("axes", "", int(plot_.nbins), plot_.x_range_min, plot_.x_range_max)
    hax.SetMinimum(plot_.y_range_min)
    hax.SetMaximum(plot_.y_range_max)
    hax.GetXaxis().SetTitle(plot_.x_label)
    hax.GetXaxis().SetTitleFont(42)
    hax.GetXaxis().SetLabelFont(42)
    hax.GetXaxis().SetLabelSize(0.035)
    hax.GetXaxis().SetTitleSize(0.048 * 0.85)
    hax.GetXaxis().SetTitleOffset(-999)
    hax.GetXaxis().SetLabelOffset(-999)

    hax.GetYaxis().SetTitle(plot_.y_label)
    hax.GetYaxis().SetTitleFont(42)
    hax.GetYaxis().SetLabelFont(42)
    hax.GetYaxis().SetTitleOffset(1.4)
    hax.GetYaxis().SetLabelOffset(0.013)
    hax.GetYaxis().SetLabelSize(1.2 * 0.035)
    hax.GetYaxis().SetTitleSize(0.055 * 0.85)
    hax.Draw()
    rcan.upper_pad.Update()

    nom_stack = r.THStack("stack_" + plot_.name + "_nom", "")
    up_stack  = r.THStack("stack_" + plot_.name + "_up", "")
    down_stack = r.THStack("stack_" + plot_.name + "_down", "")

    # legend
    leg = pu.default_legend(xl=0.62, yl=0.68, xh=0.93, yh=0.90)

    if len(sys_list) > 1 :
        print "ERROR you should only provide this method one systematic"
        sys.exit()

    # loop through background MC and add to stack
    nom_histos = []
    up_histos = []
    down_histos = []

    syst = sys_list[0]

    for b in bkg_list :

        #######################################
        ## nominal
        hist_name = ""
        if "abs" in plot_.variable :
            replace_var = plot_.variable.replace("abs(","")
            replace_var = replace_var.replace(")","")
            hist_name = replace_var
        else :
            hist_name = plot_.variable

        h = pu.th1f("h_" + b.treename + "_" + hist_name + "_nom", "",
                    int(plot_.nbins), plot_.x_range_min, plot_.x_range_max,
                    plot_.x_label, plot_.y_label)
        h.SetLineColor(r.kBlack)
        h.SetLineWidth(2*h.GetLineWidth())
        h.SetFillStyle(0)
        h.GetXaxis().SetLabelOffset(-999)

        # cut and make the sample wait
        cut = "(" + region.tcut + ") * eventweight * " + str(b.scale_factor)
        cut = r.TCut(cut)
        sel = r.TCut("1")
        cmd = "%s>>+%s"%(plot_.variable, h.GetName())
        b.tree.Draw(cmd, cut * sel, "goff")

        stat_err = r.Double(0.0)
        nom_integral = h.IntegralAndError(0,-1,stat_err)

        # add overflow
        pu.add_overflow_to_lastbin(h)
        nom_histos.append(h)
        rcan.upper_pad.Update()
        
        ##############################
        # fill variation histos
        for x in b.systList :
            if x.name == syst.name :
                syst = x
        sys_yields = getSystHistos(plot_, region, b, syst, hist_name)

        syst.up_histo.SetLineColor(46)
        syst.up_histo.SetFillStyle(0)
        up_histos.append(syst.up_histo)

        if "JER" not in syst.name :
        #if not syst.isOneSided() :
            syst.down_histo.SetFillStyle(0)
            syst.down_histo.SetLineColor(38)
            down_histos.append(syst.down_histo)

    ## order the histos (not really necessary for this)
    nom_histos = sorted(nom_histos, key=lambda h: h.Integral(), reverse=False)
    up_histos = sorted(up_histos, key=lambda h: h.Integral(), reverse=False)
    if not syst.isOneSided() :
        down_histos = sorted(down_histos, key=lambda h: h.Integral(), reverse=False)
    for h in nom_histos :
        nom_stack.Add(h)
    for h in up_histos :
        up_stack.Add(h)
    #if not syst.isOneSided() :
    if "JER" not in syst.name :
        for h in down_histos :
            down_stack.Add(h)


    ############################ get the envelopes
    nom_total = nom_stack.GetStack().Last().Clone("nom_total")
    nom_total.SetMaximum(plot_.y_range_max)
    nom_total.SetMinimum(plot_.y_range_min)
    nom_total.SetLineColor(r.kBlack)
    nom_total.SetLineWidth(1*nom_total.GetLineWidth())
    nom_total.SetFillStyle(0)
    leg.AddEntry(nom_total, "Nominal", "l")

    up_total = up_stack.GetStack().Last().Clone("up_total")
    up_total.SetMaximum(plot_.y_range_max)
    up_total.SetMinimum(plot_.y_range_min)
    up_total.SetLineColor(46)
    up_total.SetLineWidth(1*up_total.GetLineWidth())
    up_total.SetFillStyle(0)
    var_up = ""
    if "JER" in syst.name :
        var_up = "Variation"
    else :
        var_up = "Up-Variation"
    leg.AddEntry(up_total, var_up, "l")

    if "JER" not in syst.name :
        down_total = down_stack.GetStack().Last().Clone("down_total")
        down_total.SetMaximum(plot_.y_range_max)
        down_total.SetMinimum(plot_.y_range_min)
        down_total.SetLineColor(38)
        down_total.SetLineWidth(1*down_total.GetLineWidth())
        down_total.SetFillStyle(0)
        leg.AddEntry(down_total, "Down-Variation", "l")

    ############################# draw!
    nom_total.Draw("hist")
    up_total.Draw("hist same")
    if "JER" not in syst.name :
        down_total.Draw("hist same")
    rcan.upper_pad.Update()

    r.gPad.SetTickx()
    r.gPad.SetTicky()
    rcan.upper_pad.Update()

    ############################ words
    pu.draw_text(text="#it{ATLAS} Preliminary", x= 0.18, y = 0.85)
    pu.draw_text(text="13 TeV, 3.2/fb", x=0.18,y=0.8)
    pu.draw_text(text=region.displayname, x=0.18,y=0.75)
    pu.draw_text(text=syst.name,x=0.18,y=0.7)
    rcan.upper_pad.Update()


    ############################# ratios
    rcan.lower_pad.cd()

    up_ratio = up_total.Clone("up_ratio")
    up_ratio.Divide(nom_total)

    down_ratio = down_total.Clone("down_ratio")
    down_ratio.Divide(nom_total)

    ## axis for lower pad
    yax = up_ratio.GetYaxis()
    yax.SetRangeUser(0,2)
    yax.SetTitle("Variation/Nominal")
    yax.SetTitleSize(nom_total.GetYaxis().GetTitleSize())
 #   yax.SetTitleSize(0.14 * 0.5)
    yax.SetLabelSize(nom_total.GetYaxis().GetLabelSize())
 #   yax.SetLabelSize(0.13)
    yax.SetLabelOffset(1.2 * nom_total.GetYaxis().GetLabelOffset())
 #   yax.SetLabelOffset(0.98 * 0.013)
#    yax.SetTitleOffset(0.45)
    yax.SetTitleOffset(nom_total.GetYaxis().GetTitleOffset())
    yax.SetLabelFont(42)
    yax.SetTitleFont(42)
    yax.SetNdivisions(5)

    xax = up_ratio.GetXaxis()
    xax.SetTitleSize(1.2 * 0.14)
    xax.SetLabelSize(0.13)
    xax.SetLabelOffset(1.15*0.02)
    xax.SetTitleOffset(0.85 * xax.GetTitleOffset())
    xax.SetLabelFont(42)
    xax.SetTitleFont(42)


    up_ratio.Draw("hist")
    down_ratio.Draw("hist same")
    rcan.lower_pad.Update()
    

    


    ########################### save
    outname = plot_.name + "_" + syst.name + ".eps"
    rcan.canvas.SaveAs(outname)
    out = indir + "/plots/" + outdir
    utils.mv_file_to_dir(outname, out, True)
    fullname = out + "/" + outname
    print "%s saved to : %s"%(outname, os.path.abspath(fullname))

    nom_total.Delete()
    up_total.Delete()
    if "JER" not in syst.name :
        down_total.Delete()
    hax.Delete()

##### [before]
#    bkg = bkg_list[0]
#    syst = sys_list[0]
#   
#    ############################
#    # nominal
#    hist_name = ""
#    if "abs" in plot.variable :
#        replace_var = plot.variable.replace("abs(","")
#        replace_var = replace_var.replace(")","")
#        hist_name = replace_var
#    else :
#        hist_name = plot.variable
#
#    h = pu.th1f("h_" + bkg.treename + "_" + hist_name + "_nom", "", int(plot.nbins), plot.x_range_min, plot.x_range_max, plot.x_label, plot.y_label)
#    h.SetLineColor(r.kBlack)
#    h.SetFillStyle(0)
#    h.GetXaxis().SetLabelOffset(-999)
#    h.Sumw2
#
#    # cut and make the sample weighted, with any scale_factor
#    cut = "(" + reg.tcut + ") * eventweight * " + str(bkg.scale_factor)
#    cut = r.TCut(cut)
#    sel = r.TCut("1")
#    cmd = "%s>>%s"%(plot.variable, h.GetName())
#    bkg.tree.Draw(cmd, cut * sel, "goff")
#
#    # get the yields
#    nom_error = r.Double(0.0)
#    nom_integral = h.IntegralAndError(0,-1,nom_error)
#
#    ###############################
#    # fill variation histos
#    for x in bkg.systList :
#        if x.name == syst.name :
#            syst = x
#
#    sys_yields = getSystHistos(plot, reg, bkg, syst, hist_name)
#
#
#    ###############################
#    # now plot
#    h.Draw("hist")
#    rcan.upper_pad.Update()
#
#    syst.up_histo.SetLineColor(46)
#    syst.up_histo.SetFillStyle(0)
#    syst.up_histo.Draw("hist same")
#    rcan.upper_pad.Update()
#
#
#    if not syst.isOneSided() :
#        syst.down_histo.SetLineColor(38)
#        syst.down_histo.SetLineColor(0)
#        syst.down_histo.Draw("hist same")
#        rcan.upper_pad.Update()
#
#
#    print "%.2f +/- %.2f (+%.2f, -%.2f)"%(nom_integral, nom_error, (sys_yields[0]-nom_integral), (nom_integral-sys_yields[1]))
#
#
#
#    ################################
#    # save
#    outname = plot.name + ".eps"
#    rcan.canvas.SaveAs(outname)
#    out = indir + "/plots/" + outdir
#    utils.mv_file_to_dir(outname, out, True)
#    fullname = out + "/" + outname
#    print "%s saved to : %s"%(outname, os.path.abspath(fullname))
#
#    
#   
#
#    hax.Delete() 

################################################################
## main plotting function
def make_sys_plots(plot_list, region_list, bkg_list, sys_list) :

    for reg_ in region_list :
        print "Setting eventlists for %s"%(reg_.name)

        cut = reg_.tcut
        cut = r.TCut(cut)
        sel = r.TCut("1")
        for b in bkg_list :
            list_name = "list_" + reg_.name + "_" + b.treename
            save_name = "./" + indir + "/lists/" + list_name + ".root"

            # check if list already exists
            if os.path.isfile(save_name) :
                rfile = r.TFile.Open(save_name)
                list_ = rfile.Get(list_name)
                print "%s : Eventlist found at %s"%(b.name, os.path.abspath(save_name))
                if dbg : list_.Print()
                b.tree.SetEventList(list_)

                # TODO add event lists for systematics trees
            else :
                draw_list = ">> " + list_name
                b.tree.Draw(draw_list, sel*cut)
                list_ = r.gROOT.FindObject(list_name)
                b.tree.SetEventList(list_)
                list_.SaveAs(save_name)

        for p in plot_list :
            make_sys_plot(p, reg_, bkg_list, sys_list)
        



if __name__=="__main__" :
    global indir, plotConfig, requestRegion, requestBkg, requestSys, outdir, dbg
    parser = OptionParser()
    parser.add_option("-c", "--plotConfig", dest="plotConfig",default="")
    parser.add_option("-i", "--indir", dest="indir", default="")
    parser.add_option("-r", "--requestRegion", dest="requestRegion",default="")
    parser.add_option("-o", "--outdir", dest="outdir", default="./")
    parser.add_option("-d", "--dbg", dest = "dbg", action="store_true", default=False)
    parser.add_option("-b", "--requestBkg", dest="requestBkg", default="")
    parser.add_option("-s", "--requestSys", dest="requestSys", default="")
    (options, args) = parser.parse_args()
    indir           = options.indir
    plotConfig      = options.plotConfig
    requestRegion   = options.requestRegion
    outdir          = options.outdir
    requestBkg      = options.requestBkg
    requestSys      = options.requestSys
    dbg             = options.dbg

    print " ++ ------------------------- ++ "
    print "      sysplotter                 "
    print "                                 "
    print " config directory :  %s          "%indir
    print " plot config      :  %s          "%plotConfig
    print " requested region :  %s          "%requestRegion
    print " output directory :  %s          "%outdir
    print "                                 "
    print " ++ ------------------------- ++ \n"

    # get the config
    conf_file = get_plotConfig(plotConfig)
    print "Found configuration file: %s"%conf_file
    plots = []
    backgrounds = []
    systematics = []
    regions = []
    execfile(conf_file)

    if dbg :
        for p in plots :
            p.Print()

    print 45*"-"
    print " Backgrounds: "
    for b in backgrounds :
        b.Print()
    print 45*"-"
    for s in systematics :
        s.check()
        s.Print()
        for b in backgrounds :
            b.addSys(s)

    # make the plots
    requested_regions = []
    requested_bkg = []
    requested_sys = []
    requested_plots = []

    ############################## build regions to send
    if requestRegion != "" :
        for r_ in regions :
            if r_.name == requestRegion : requested_regions.append(r_)
    else :
        print "ERROR You must request a region with the '-r'/'--requestRegion' option!"
        sys.exit()
    if len(requested_regions)==0 or len(requested_regions)>1 :
        print "ERROR finding requested region. (%d)"%len(requested_bkg)
        sys.exit()

 #   ############################## build backgrounds to send
    requested_bkg = backgrounds
 #   if requestBkg != "" :
 #       for b in backgrounds :
 #           if b.name == requestBkg : requested_bkg.append(b) 
 #   else :
 #       requested_bkg = backgrounds
 #   if len(requested_bkg)==0 :
 #       print "ERROR finding requested background (%d)"%len(requested_bkg)
 #       sys.exit()

    ############################# build the plots to send
    for r_ in requested_regions :
        for p_ in plots :
            if p_.region == r_.name : requested_plots.append(p_)
    if len(requested_plots) == 0 :
        print "ERROR No plots are setup for the requested region (%s)"%(requested_regions[0])
        sys.exit()

    ############################## build systematics to send
    if requestSys != "" :
        for sys_ in systematics :
            if sys_.name == requestSys : requested_sys.append(sys_)
    else :
        print "ERROR You must request a systematic with the '-s'/'--requestSys' option!"
        sys.exit()
    if len(requested_sys) == 0 or len(requested_sys) > 1 :
        print "ERROR Require exactly 1 systematic. You have %d."%len(requested_sys)
        sys.exit()
    for sys_ in requested_sys :
        for b in requested_bkg :
            sys_is_in_this_bkg = False
            for check_sys in b.systList :
                if sys_.name == check_sys.name :
                    sys_is_in_this_bkg = True
                    break
            if not sys_is_in_this_bkg :
                print "ERROR Systematic (%s) is not found in the systematic list of background"%sys_.name
                print "ERROR sample %s"%b.name
                sys.exit()

    # things should be good to go now
    make_sys_plots(requested_plots, requested_regions, requested_bkg, requested_sys)
                 


    
