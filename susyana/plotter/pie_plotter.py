#!/usr/bin/env python

from optparse import OptionParser
import os

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(False)
import sys
sys.path.append(os.environ['SUSYDIR'])

# keep root from owning things
r.TH1F.__init__._creates = False

# supersusy 
import supersusy.utils.plot_utils as pu
import supersusy.utils.utils as utils
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region
import supersusy.utils.plot as plot

# matplotlib goo
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
plt.rc('font', family = 'serif')

def get_plotConfig(conf) :
    configuration_file = "./" + indir + "/" + conf + ".py"
    if os.path.isfile(configuration_file) :
        print "[get_plotConfig]    Found the configuration file: %s"%configuration_file
        return configuration_file
    else :
        print '[get_plotConfig]    ERROR Input plot configuration ("%s") is not found in the directory/path provided ("%s"). Does it exist? Exitting.'%(conf, configuration_file)
        sys.exit()

def get_yield(region, bkg) :
    h_yld = r.TH1F("h_%s_%s"%(region.simplename, bkg.name), "h_%s_%s"%(region.simplename, bkg.name), 3, 0, 3)
    cut = "(" + region.tcut + ") * eventweight *" + str(bkg.scale_factor)
    cut = r.TCut(cut)
    sel = r.TCut("1")
    cmd = "%s>>%s"%("isMC", h_yld.GetName()) 
    bkg.tree.Draw(cmd, cut * sel, "goff")
    yield_ = h_yld.Integral()
    h_yld.Delete()
    return yield_

def make_piePlots(region, backgrounds) :
    print "[make_piePlots]    Baking region %s"%region.simplename

    yields = {}
    total_yield = 0.0
    for bkg in backgrounds :
        yld = get_yield(region, bkg)
        yields[bkg.displayname] = yld
        total_yield += yld
        print "[make_piePlots]    %s   :    %.2f"%(bkg.name, yld)
    print "[make_piePlots]    Total :    %.2f"%total_yield
    labels = yields.keys()
    labels2 = []
    fractions = []
    colors = []
    for l in labels :
        fractions.append("%.1f"%(float(yields[l]) / total_yield * 100.0))
        labe = l
        labels2.append( l + " (%s %%)"%fractions[-1])
        for b_ in backgrounds :
            if b_.displayname == l :
                colors.append(b_.color)
    labels = labels2
    #patches, texts = plt.pie(fractions, colors = colors, shadow=True, startangle=90)
    #plt.pie(fractions, colors = colors, autopct='%1.1f%%', shadow=True, startangle=90)
    patches, texts = plt.pie(fractions, colors = colors, shadow=True, startangle=90)
    #patches, texts, blah = plt.pie(fractions, labels = labels, colors = colors, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    #plt.tight_layout()
    outname = "%s_pie.eps"%region.simplename
    out = indir + "/plots/" + outdir
    plt.savefig(outname)
    utils.mv_file_to_dir(outname, out, True)
    fullname = out + "/" + outname
    print "[make_piePlots]    %s saved to : %s"%(outname, os.path.abspath(fullname))

    # clear plot
    plt.clf()

if __name__ == "__main__" :
    global indir, plotConfig, requestedRegion, outdir, dbg
    parser = OptionParser()
    parser.add_option("-c", "--plotConfig", dest="plotConfig", default = "")
    parser.add_option("-i", "--indir", dest = "indir", default = "")
    parser.add_option("-r", "--requestedRegion", dest = "requestedRegion", default = "")
    parser.add_option("-o", "--outdir", dest = "outdir", default = "./")
    parser.add_option("-d", "--dbg", action = "store_true", dest = "dbg", default = False)
    (options, args) = parser.parse_args()
    indir = options.indir
    plotConfig = options.plotConfig
    requestedRegion = options.requestedRegion
    outdir = options.outdir
    dbg = options.dbg

    inputs_bad = False
    if indir == "" :
        print 'ERROR    You have not provided an input directory ("-i" / "--indir").'
        inputs_bad = True
    if plotConfig == "" :
        print 'ERROR    You have not provided a plot configuration ("-c" / "--plotConfig").'
        inputs_bad = True
    if inputs_bad :
        sys.exit()

    print " ++ -------------------------- ++ "
    print "      pie-plotter                 "
    print "                                  "
    print "     config directory : %s        "%indir
    print "     plot config      : %s        "%plotConfig
    print "     requested region : %s        "%requestedRegion
    print "     output directory : %s        "%outdir
    print "     debug            : %s        "%dbg
    print ""
    print " ++ -------------------------- ++\n"

    # get the config
    conf_file = get_plotConfig(plotConfig)
    backgrounds = []
    regions = []
    execfile(conf_file)

    # print out loaded business
    print " ++ -------------------------- ++ "
    print "     Loaded backgrounds :   "
    for b in backgrounds :
        b.Print()
    print " ++ -------------------------- ++ "
    

    if requestedRegion != "" :
        for region_ in regions :
            if region_.simplename == requestedRegion :
                make_piePlots(region_, backgrounds)
    else :
        for region_ in regions :
            make_piePlots(region_, backgrounds)
