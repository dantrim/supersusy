#!/usr/bin/env python


from optparse import OptionParser
import os

import glob

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

from math import sqrt

###############################
## handler class for data lumi
## normalized yields
###############################
class lumiData :
    def __init__(self, filename_ = "") :
        self.filename = filename_
        self.tree = self.get_tree(filename_) # must be absolute path
        self.run_number = self.get_runNumber(filename_)

        self.init_print()

        self.lumi = 0.0
        self.yields = {} # { region : yield }
        self.errors = {} # { region : error } 

    def get_tree(self, fname_="" ) :
        if not os.path.isfile(fname_) :
            print "lumiData::get_tree()    ERROR Input file (%s) is not found!"%fname_
            print "lumiData::get_tree()    ERROR  > Exiting."
            sys.exit()

        chain = r.TChain('superNt')
        chain.Add(fname_)
        #self.tree = chain
        return chain

    def get_runNumber(self, fname_="") :
        number = fname_.split("/")[-1].split("_")[-1].replace(".root","")
        return number

    def init_print(self) :
        print "lumiData::init_print()    %d : %d entries"%(int(self.run_number), int(self.tree.GetEntries()))
        



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
        configured_regions.append(r.name)
    for p in plots :
        current_region = p.region
        if current_region not in configured_regions :
            bad_regions.append(current_region)
    if len(bad_regions) > 0 :
        print 'check_for_consistency ERROR    You have configured a plot for a region that is not defined. Here is the list of "bad regions":'
        for blah in bad_regions :
            print blah.name
        print 'check_for_consistency ERROR    The regions that are defined in the configuration ("%s") are:'%plotConfig
        print configured_regions
        print "check_for_consistency ERROR    Exitting."
        sys.exit()
    else :
        print "check_for_consistency    Plots and regions consistent."

def make_eventlists(regs_, plts_, data_, bkgs_) :
    for reg in regs_ :
        plots_with_region = []
        for p in plts_ :
            if p.region == reg.name : plots_with_region.append(p)

        if len(plots_with_region) == 0 : continue
        print "Setting EventLists for %s"%erg.name
        cut = reg.tcut
        cut = r.TCut(cut)
        sel = r.TCut("1")
        for b in backgrounds :
            list_name = "list_" + reg.name + "_" + b.treename
            save_name = "./" + indir + "/lists/" + list_name + ".root"
            if os.path.isfile(save_name) :
                rfile = r.TFile.Open(save_name)
                list = rfile.Get(list_name)
                print "%s : EventList found at %s"%(b.name, os.path.abspath(save_name))
                list.Print()
                b.tree.SetEventList(list)
            else :
                draw_list = ">> " + list_name
                b.tree.Draw(draw_list, sel*cut)
                list = r.gROOT.FindObject(list_name)
                b.tree.SetEventList(list)
                list.SaveAs(save_name)

        if data_ :
            data_list_name = "list_" + reg.anem + "_" + data.treename
            data_save_name = "./" + indir + "/lists/" + data_list_name + ".root"
            if os.path.isfile(data_save_name) :
                rfile = r.TFile.Open(data_save_name)
                data_list = rfile.Get(data_list_name)
                print "Data: EventList found at %s"%(os.path.abspath(data_save_name))
                data_list.Print()
                data_.tree.SetEventList(data_list)
            else :
                draw_list = ">> " + data_list_name
                data_.tree.Draw(draw_list, sel * cut)
                data_list = r.gROOT.FindObject(data_list_name)
                data_.tree.SetEventList(data_list)
                data_list.SaveAs(data_save_name)

def make_nVtxEffPlot(plt, reg, data, bkgs) :

    print "make_nVtxEffPlot..."

    if plt.variable != "nVtx" :
        print "make_nVtxEffPlot ERROR    You may only provide plots setup to plot nVtx!"
        print "make_nVtxEffPlot ERROR    This plot is configured to plot %s"%plt.variable
        sys.exit()

    r.gStyle.SetOptStat(0000)
    r.gStyle.SetOptFit(0111);


    # get the canvas
    c = plt.canvas
    c.cd()
    c.SetFrameFillColor(0)
    c.SetFillColor(0)
    c.SetLeftMargin(0.14)
    c.SetRightMargin(0.05)
    c.SetBottomMargin(1.3*c.GetBottomMargin())

    c.Update()

    ## stack for MC with selection
    stack = r.THStack("stack_" + plt.name, "")

    ## get MC histos with region selection applied 
    histos = []

    print "make_nVtxEffPlot    Getting histograms with selection applied (%s)"%reg.name
    for b in bkgs :
        print "    > %s"%b.name
        hist_name = plt.variable

        h = pu.th1f("h_"+b.treename+"_"+hist_name, "", int(plt.nbins), plt.x_range_min, plt.x_range_max, plt.x_label, plt.y_label) 
        h.SetLineColor(b.color)
        h.SetLineColor(r.kBlack)
        h.SetMarkerSize(1.2*h.GetMarkerSize())
        h.SetMarkerStyle(20)
        h.SetLineWidth(2)
        h.SetLineStyle(b.line_style)
        h.SetFillColor(0)
        h.Sumw2


        weight_str = ""
        if b.isSignal() :
            weight_str = "eventweightNOPUPW * susy3BodyRightPol"
        else :
            print " **** NOT APPLYING PRW TO MC ***** "
            weight_str = "eventweightNOPUPW"
        cut = "(" + reg.tcut + ") * %s *"%weight_str + str(b.scale_factor)
        cut = r.TCut(cut)
        sel = r.TCut("1")
        cmd = "%s>>+%s"%(plt.variable, h.GetName())
        b.tree.Draw(cmd, cut * sel)

        pu.add_overflow_to_lastbin(h)

        histos.append(h)
        c.Update()

    histos = sorted(histos, key=lambda h: h.Integral(), reverse=False)
    for h in histos :
        stack.Add(h)


    ## stack for MC withi NO selection
    stack_nosel = r.THStack("stack_" + plt.name + "_nosel", "")

    ## get the MC histos with no selection applied
    histos_nosel = []
    
    print "make_nVtxEffPlot    Getting histograms with NO selection applied (%s)"%reg.name
    for b in bkgs :
        print "    > %s"%b.name
        hist_name = plt.variable

        h = pu.th1f("h_"+b.treename+"_"+hist_name + "_nosel", "", int(plt.nbins), plt.x_range_min, plt.x_range_max, plt.x_label, plt.y_label) 
        h.SetLineColor(b.color)
        h.SetMarkerStyle(20)
        h.SetMarkerSize(1.2*h.GetMarkerSize())
        h.SetLineColor(r.kBlack)
        h.SetLineWidth(2)
        h.SetLineStyle(b.line_style)
        h.SetFillColor(0)
        h.Sumw2


        weight_str = ""
        if b.isSignal() :
            weight_str = "eventweightNOPUPW * susy3BodyRightPol"
        else :
            print " **** NOT APPLYING PRW TO MC ***** "
            weight_str = "eventweightNOPUPW"
        #cut = "(" + reg.tcut + ") * %s *"%weight_str + str(b.scale_factor)
        cut = "1"
        cut = r.TCut(cut)
        sel = r.TCut("1")
        cmd = "%s>>+%s"%(plt.variable, h.GetName())
        b.tree.Draw(cmd, cut * sel)

        pu.add_overflow_to_lastbin(h)

        histos_nosel.append(h)
        c.Update()

    histos_nosel = sorted(histos_nosel, key=lambda h: h.Integral(), reverse=False)
    for h in histos_nosel :
        stack_nosel.Add(h)


    ### total MC with selection
    totalSM = stack.GetStack().Last().Clone("totalSM")
    ### total MC with no selection
    totalSM_nosel = stack_nosel.GetStack().Last().Clone("totalSM_nosel")

    #c.SetMaximum(5)
    #c.SetMinimum(0)
    #c.Update()

    h_den = totalSM_nosel.Clone("h_den")
    h_num = totalSM.Clone("h_num") 

    h_num.Divide(h_den)

    # axes
    hax = r.TH1F("axes","", int(plt.nbins), plt.x_range_min, plt.x_range_max)
    hax.SetMinimum(0)
    hax.SetMaximum(1.2*h_num.GetMaximum())
    hax.GetXaxis().SetTitle("Number of Primary Vertices")
    hax.GetXaxis().SetTitleFont(42)
    hax.GetXaxis().SetLabelFont(42)
    hax.GetXaxis().SetLabelSize(0.035)
    hax.GetXaxis().SetTitleSize(0.048 * 0.85)

    hax.GetYaxis().SetTitle("%s Selection Efficiency"%reg.displayname)
    hax.GetYaxis().SetTitleFont(42)
    hax.GetYaxis().SetLabelFont(42)
    hax.GetYaxis().SetTitleOffset(1.4)
    hax.GetYaxis().SetLabelOffset(0.013)
    hax.GetYaxis().SetLabelSize(1.2*0.035)
    hax.GetYaxis().SetTitleSize(0.055*0.85)
    hax.Draw("axis")


    c.Update()

    h_num.Draw("p0 e same")
    h_num.GetXaxis().SetTitle("Number of Primary Vertices")
    h_num.GetXaxis().SetTitleFont(42)
    h_num.GetXaxis().SetLabelFont(42)
    h_num.GetXaxis().SetLabelSize(0.035)
    h_num.GetXaxis().SetTitleSize(0.048 * 0.85)
    h_num.GetYaxis().SetTitle("%s Selection Efficiency"%reg.displayname)
    h_num.GetYaxis().SetTitleFont(42)
    h_num.GetYaxis().SetLabelFont(42)
    h_num.GetYaxis().SetTitleOffset(1.35)
    h_num.GetYaxis().SetLabelOffset(0.013)
    h_num.GetYaxis().SetLabelSize(1.2*0.035)
    h_num.GetYaxis().SetTitleSize(0.055*0.85)
    c.Update()
    h_num.Fit("pol1")
    r.gStyle.SetOptFit(0111);
    c.Update()
    h_num.Draw()
    #ps = r.gStyle.GetListOfFunctions().FindObject("stats");
    #ps.SetX1NDC(0.15);
    #ps.SetX2NDC(0.6);
    #c.Modified();
    #c.Update();
    r.gStyle.SetStatX(0.58)
    r.gStyle.SetStatY(0.85)
    c.Update()

    c.SaveAs("eff_nVtx_%s.eps"%reg.name)


##################################################
##################################################
##################################################
# lumi normalized data plotting stuff
##################################################
##################################################
##################################################

class lumiCanvas :
    '''
    Class to hold the canvases for the pads n stuff
    '''
    def __init__(self, name) :
        self.name = name
        self.canvas = r.TCanvas(name,name,1200,600)
        self.pad = r.TPad("pad","pad",0.0,0.0,1.0,1.0)
        self.set_pad_dimensions()

    def set_pad_dimensions(self) :
        can = self.canvas
        pad = self.pad

        can.cd()
        up_height = 0.10
        dn_height = 0.50
        pad.SetPad(0.0,up_height,1.0,1.0)
        
        pad.SetTickx(1)
        pad.SetTicky(0)

        pad.SetFrameFillColor(0)
        pad.SetFillColor(0)
        pad.SetLeftMargin(0.07)
        pad.SetRightMargin(0.025)
        pad.SetBottomMargin(0.2)
        pad.SetTopMargin(0.2)

        pad.Draw()
        can.Update()

        self.canvas = can
        self.pad = pad

        


def run_ARQ(list_of_runs = []) :

    import subprocess

    if len(list_of_runs) == 0 :
        print "run_ARQ()    ERROR list of runs provided is empty!"
        print "run_ARQ()     > Exiting."
        sys.exit()

    # run the query - all of the retrieved data is stored in a pickle file on disk
    cmd = "AtlRunQuery.py \"find run %s and ready and st %s 100k+ / show lumi\"" % (list_of_runs, "physics_Main")
    print "Executing the following ARQ query:"
    print " > %s" % cmd
    env = os.environ.copy()
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    for line in output.stdout.readlines() :
        print " > %s" % line.rstrip()
    print 45*"-"
    print "  Retrieved ARQ results "
    print 45*"-"

def get_lumi(samples = []) :
    if len(samples) == 0 :
        print "get_lumi()    ERROR list of samples is empty!"
        sys.exit()

    lumidict = {}
    lines = open("lumiinfo.txt").readlines()
    for line in lines :
        if not line : continue
        line = line.strip()
        line = line.split()
        lumidict[str(line[0])] = float(line[1])

    for ds in samples :
        ds.lumi = lumidict[str(ds.run_number)]

def get_yield(sample, region) :

    cut = "(" + region.tcut + ")"
    cut = r.TCut(cut)
    sel = r.TCut("1")
    h = pu.th1f("h_" + str(sample.run_number) + "_%s"%region.name + "_yield","",4,-1,3,"","")
    cmd = "%s>>%s"%("isMC", h.GetName())
    sample.tree.Draw(cmd, cut * sel, "goff")

    err = r.Double(0.0)
    integral = h.IntegralAndError(0,-1,err)
    h.Delete()
    return integral, err

def get_periodlines(samples, height, region_name) :

    periods = {}
    periods["A15"] = [266904, 367639]
    periods["B15"] = [267538, 267599]
    periods["C15"] = [270441, 272531]
    periods["D15"] = [276073, 276954]
    periods["E15"] = [278727, 279928]
    periods["F15"] = [279932, 280422]
    periods["G15"] = [280423, 281075]
    periods["H15"] = [281130, 281411]
    periods["I15"] = [281662, 282482]
    periods["J15"] = [282625, 284484]

    periods["A16"] = [296939, 300287]
    periods["B16"] = [300345, 300908]
    periods["C16"] = [301912, 302393]
    periods["D16"] = [302737, 303059]

    lines = []
    text = []
    last_period = "A15"
    for s in samples :
        run = int(s.run_number)
        for period in periods.keys() :
            if run >= periods[period][0] and run <= periods[period][1] :
                s.period = period
                #if period != last_period :
                #    print "line at run %s, period %s, bin: %d"%(str(run), period, irun)
                #    l = r.TLine(irun, 0.0, irun, height)
                #    l.SetLineColor(r.kBlue)
                #    l.SetLineWidth(2)
                #    l.SetLineStyle(2)
                #    lines.append(l)
                #    last_period = period
                #else :
                #    continue

    colors = [2,3,4,r.kOrange-3,6,7,8,9]

    label_height = {}
    label_height["srtPreselDF"] = 1
    label_height["srtPreselEE"] = 0.5
    label_height["srtPreselMM"] = 0.5
    label_height["srwPreselDF"] = 0.15
    label_height["srwPreselEE"] = 1
    label_height["srwPreselMM"] = 1

    #current_period = samples[0].period
    current_period = "A15"
    change_set = 0
    for ibin, s in enumerate(samples) :
        #print "%s : %s"%(str(s.run_number), s.period)
        if s.period != current_period :
            l = r.TLine(ibin, 0.0, ibin, height)
            l.SetLineColor(colors[change_set])
            l.SetLineWidth(1)
            l.SetLineStyle(1)
            lines.append(l)
            current_period = s.period

            t = r.TLatex()
            t.SetTextSize(0.04)
            t.SetTextFont(42)
            t.SetTextColor(colors[change_set])
            t.SetTextAngle(90)
            t.DrawLatex(ibin+1.5, label_height[region_name], "#bf{%s}"%s.period)

            change_set += 1
        else :
            continue

    return lines

def get_err(hist, lumi) :
    '''
    Provided a histogram, convert the errors
    to Poisson errors
    '''
    # needed variables
    alpha = 0.158655
    beta = 0.158655

    g = r.TGraphAsymmErrors()

    for ibin in xrange(1,hist.GetNbinsX()+1) :
        value = hist.GetBinContent(ibin)
        if value != 0 :
            error_poisson_up = 0.5 * r.TMath.ChisquareQuantile(1-beta,2*(value+1))-value
            error_poisson_down = value - 0.5*r.TMath.ChisquareQuantile(alpha,2*value)
            ex = hist.GetBinWidth(ibin) / 2.0 
            g.SetPoint(ibin-1, hist.GetBinCenter(ibin), value)
            g.SetPointError(ibin-1, ex, ex, error_poisson_down / float(lumi[ibin-1]), error_poisson_up / float(lumi[ibin-1]))
        else :
            g.SetPoint(ibin-1, hist.GetBinCenter(ibin), 0.0)
            g.SetPointError(ibin-1, 0., 0., 0., 0.)

    return g
    

def make_lumi_plot(samples, region) :
    print "make_lumi_plot()    Making lumi plot for %s"%region.name

    lumican = lumiCanvas("lumican_%s"%region.name)
    lumican.canvas.cd()

    # only plot those runs with >= 10/pb of data
    new_samples = []
    for s in samples :
        if s.lumi >= 10 : new_samples.append(s)
    samples = new_samples


    # only 2015
    #new_samples = []
    #for s in samples :
    #    if int(s.run_number) < 297730 : new_samples.append(s)
    #samples = new_samples


    lumican.pad.cd()
    h = pu.th1f("h_lumi_" + region.name, "",int(len(samples)), 0, int(len(samples)), "Run Number", "Events/pb^{-1}")

    #h.SetBinErrorOption(r.TH1.kPoisson)
    #h.Sumw2()

    samples = sorted(samples, key = lambda x: x.run_number, reverse=False)


    maxy = -1

    sum_ev = 0.0

    lumi_list = []

    for ibin, s_ in enumerate(samples) :
        yld = s_.yields[region.name]
        lumi = s_.lumi
        lumi_list.append(lumi)
        norm = float(yld)/float(lumi)
        sum_ev += norm
        if norm > maxy : maxy = norm
        h.SetBinContent(ibin+1, norm)
        h.SetBinError(ibin+1, sqrt(yld)/float(lumi))
        h.GetXaxis().SetBinLabel(ibin+1, "%s"%str(s_.run_number))

    avg_norm = float(sum_ev)/len(samples)

    maxima = {}
    maxima['srwPreselEE'] = 10.
    maxima['srwPreselMM'] = 10.
    maxima['srwPreselDF'] = 1.8
    maxima['srtPreselEE'] = 5.
    maxima['srtPreselMM'] = 5.
    maxima['srtPreselDF'] = 8.
    
    #h.SetMaximum(maxima[region.name])
    h.SetMaximum(2.15*avg_norm)
    h.SetMarkerColor(r.TColor.GetColor("#386672"))
    h.SetMarkerSize(1.5*h.GetMarkerSize())

    h.SetMinimum(0)

    h.SetFillColor(0)
    h.SetLineColor(r.kBlack)

    ## labels
    h.GetXaxis().LabelsOption("v")
    h.GetXaxis().SetLabelFont(42)
    h.GetXaxis().SetLabelOffset(3.2*h.GetXaxis().GetLabelOffset())
    h.GetXaxis().SetLabelSize(1.2*h.GetXaxis().GetLabelSize())


    ## title
    # x
    h.GetXaxis().SetTitleSize(1.75*h.GetXaxis().GetTitleSize())
    h.GetXaxis().SetTitleOffset(1.5*h.GetXaxis().GetTitleOffset())

    # y
    h.GetYaxis().SetTitleOffset(0.5*h.GetYaxis().GetTitleOffset())
    h.GetYaxis().SetTitleSize(1.25*h.GetYaxis().GetTitleSize())

    # draw average norm lumi line
    pu.draw_line(0, avg_norm, len(samples), avg_norm, color=r.kRed,style=2,width=1)

    h.Draw("hist e")

    h.Fit("pol1")
    lumican.canvas.Update()

    h.Draw()
    pu.draw_line(0, avg_norm, len(samples), avg_norm, color=r.kRed,style=2,width=1)

    ## get periods and lines
  #  period_lines = get_periodlines(samples, h.GetMaximum(), region.name)
  #  for line in period_lines :
  #      line.Draw()

    pu.draw_text_on_top(region.displayname + "  2015 + 2016 (DS1)")

    lumican.canvas.Update()
    lumican.canvas.SaveAs("normlumi_%s.eps"%region.name)
    #lumican.canvas.SaveAs("normlumi_%s_badTrig.eps"%region.name)
        

    

    


def get_yields(samples, regions) :

    for reg in regions :
        n_total = len(samples)
        n_now = 1
        total_yield = 0
        print "get_yields()    Getting yield for %s"%reg.name
        for s in samples :
            integral, error = get_yield(s, reg)
            print "[%d/%d] : %s > %.1f"%(n_now, n_total, str(s.run_number), integral)
            n_now += 1
            s.yields[reg.name] = integral
            s.errors[reg.name] = error
            total_yield += integral
        print 45*"-"
        print "Total Yield for %s : %.2f"%(reg.name, total_yield)
        print 45*"-"

if __name__ == "__main__" :
    global indir, plotConfig, requestRegion, outdir, dbg
    parser = OptionParser()
    parser.add_option("-c", "--plotConfig", dest="plotConfig", default="")
    parser.add_option("-i", "--indir", dest="indir", default="")
    parser.add_option("-r", "--requestRegion", dest="requestRegion", default="")
    parser.add_option("-o", "--outdir", dest="outdir", default="./")
    (options, args) = parser.parse_args()
    indir               = options.indir
    plotConfig          = options.plotConfig
    requestRegion       = options.requestRegion
    outdir              = options.outdir


    # these guys are grabbed from the config
    do_eff_nVtx = False
    do_lumi_yields = False




    print " ++ ------------------------- ++ "
    print "      diagnostic plotter         "
    print "                                 "
    print " config directory :  %s          "%indir
    print " plot config      :  %s          "%plotConfig
    print " requested region :  %s          "%requestRegion
    print " output directory :  %s          "%outdir
    print "                                 "
    print " ++ ------------------------- ++ \n"

    dbg = True


    # get the config file
    conf_file = get_plotConfig(plotConfig)
    print "Found the configuration file: %s"%conf_file
    plots = []
    data = None
    backgrounds = []
    systematics = []
    regions = []
    execfile(conf_file)

    which_ = ""
    if do_eff_nVtx and do_lumi_yields :
        print "ERROR In your configuration file you have set to do both the nVtx efficiency plots and lumi yields plots!"
        print "ERROR  >> Exiting."
        sys.exit()
    if do_eff_nVtx :
        which_ = "nVtx efficiency plots"
    elif do_lumi_yields :
        which_ = "lumi normalized data yields plots"
    print 50*"-"
    print " To do: %s"%which_
    print 50*"-"

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

    # make the plots

    #######################################################
    ## nVtx efficiency plotting
    #######################################################
    if do_eff_nVtx :
        if requestRegion != "" :
            requested_plots = []
            for p in plots :
                if p.region == requestRegion : requested_plots.append(p)
            for r_ in regions :
                if r_.name == requestRegion : 
                    for plt_ in requested_plots :
                        make_nVtxEffPlot(plt_, r_, data, backgrounds)
        else :
            print "ERROR You must request a region!"
            sys.exit()

    #######################################################
    ## Data lumi normalized yields per run
    #######################################################
    if do_lumi_yields :
        data_files = glob.glob(data_rawdir + "*CENTRAL*.root")
        data_samples = []
        skip = ['302872', '303421', '302053']
        tmp_files = []
        for blah in data_files :
            for x in skip :
                if x not in blah :
                    if blah in tmp_files : continue
                    tmp_files.append(blah)
        data_files = tmp_files
        for df in data_files :
            ldata = lumiData(df)
            data_samples.append(ldata)
        print 45*"-"
        print " %d Data samples loaded"%len(data_samples)
        print 45*"-"
        #sys.exit()

        ana_regions = ['srwPreselEE','srwPreselMM','srwPreselDF']#,'vrt','crv','crvSF','vrv','vrvSF']
        ana_regions += ['srtPreselEE','srtPreselMM','srtPreselDF']#,'vrt','crv','crvSF','vrv','vrvSF']
        #ana_regions = ['srwPreselEE']
        #ana_regions = ['crt']#,'vrt','crv','crvSF','vrv','vrvSF']
        regions = [r_ for r_ in regions if r_.name in ana_regions]
        for reg_ in regions :
            print "%s : %s"%(reg_.name, reg_.tcut)

        #runs = [ld.run_number for ld in data_samples]
        get_lumi(data_samples)

        get_yields(data_samples, regions)

        for reg in regions :
            make_lumi_plot(data_samples, reg)

        
        
        

    print "+----------------------------+"
    print "  Diagnostic plots done."
    print "+----------------------------+"
