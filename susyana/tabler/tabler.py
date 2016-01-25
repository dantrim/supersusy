#!/usr/bin/env python

from tabulate import tabulate

from optparse import OptionParser
import os

from math import sqrt

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(False)
import sys
sys.path.append(os.environ['SUSYDIR'])

r.TEventList.__init__._creates = False
r.TH1F.__init__._creates = False

import supersusy.utils.utils as utils
import supersusy.utils.plot_utils as pu
import supersusy.utils.background as background
import supersusy.utils.region as region

################################################
## print the usage
def print_usage() :
    print "+ ----------------------------- +"
    print "   tabler                        "
    print "         usage                   "
    print " "
    print "   not sure yet                  "
    print "+ ----------------------------- +"
    sys.exit()
    
################################################
## grab the config file
def get_config() :
    configuration_file = "./" + indir + "/" + config + ".py"
    if os.path.isfile(configuration_file) :
        return configuration_file
    else :
        print 'get_config ERROR    Input config ("%s") is not found in the directory/path: %s. Exitting.'%(config, configuration_file)
        sys.exit()

################################################
## set the event lists
def set_eventlists(regions, backgrounds, data) :

    for reg in regions :
        # set event lists, if they already exist then load them
        print "Setting EventLists for %s"%reg.simplename
        cut = ""
        if reg.isCutFlow() :
            print "Not setting event list for region (%s) marked as a cutflow!"%(reg.simplename)
            continue 
        else :
            cut = reg.tcut

        cut = r.TCut(cut)
        sel = r.TCut("1")
        for b in backgrounds :
            list_name = "list_" + reg.simplename + "_" + b.treename
            save_name = "./" + indir + "/lists/" + list_name + ".root"

            # check if the list exists
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

        if data :
            data_list_name = "list_" + reg.simplename + "_" + data.treename
            data_save_name = "./" + indir + "/lists/" + data_list_name + ".root"
            if os.path.isfile(data_save_name) :
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
                data_list.SaveAs(data_save_name)

################################################
## get the yield for a bkg provided a specific cut
def getCutYield(tcut, bkg, cutNumber) :
    # create a canvas to prevent ROOT from telling us its doing things
    c = r.TCanvas("c_"+b.treename+"_cutflow_"+str(cutNumber), "", 800, 600)
    c.cd()

    h = pu.th1f("h_"+b.treename+"_cutflow_"+str(cutNumber), "", 4, 0, 1,"","")
    cut = "(" + tcut + ") * eventweight * " + str(b.scale_factor)
    cut = r.TCut(cut)
    sel = r.TCut("1")
    cmd = "isMC>>%s"%h.GetName()
    bkg.tree.Draw(cmd, cut * sel)

    stat_err = r.Double(0.0)
    integral = h.IntegralAndError(0,-1,stat_err)

    h.Delete() 
    c.Close() # prevent annoying canvas warnings

    return integral

################################################
## make cutflow table
def make_cutflow(reg, data, backgrounds) :
    print "make_cutflow    region: %s (%s)"%(reg.name,reg.displayname)
    print "                cut   : %s"%(reg.cutFlow[0])

    headers = ['Cut']
    for bkg in backgrounds :
        headers.append(bkg.displayname) 
    # table as a list for tabulate module
    #  > each entry is a list and corresponds to a single row in the table (not including header)
    #  > for each list (row), each entry is a table value at coordinate (row, column) <==> table[iRow][iColumn]
    table = []

    # tables for efficiencies
    #   > each entry will be a list holding the efficiencies for each cut
    #   > e.g. [ [cut1 efficiency bkg1, cut1 efficiency bkg2], [cut2 efficiency bkg1, cut2 efficiency bkg2], ... ]
    efficiencies = []

    for icut, cut in enumerate(reg.getCutFlowDict().keys()) :
        line = []
        line.append(cut) # first entry in the row is the name of the cut

        # make a list of cut efficiencies for each background, for each cut
        # eff_list : indices correspond to the background, values = eff. for that bkg.
        eff_list = []

        for ib, bkg in enumerate(backgrounds) :
            # get the yield for the bkg for the cutflow up to this point
            bkgYield = getCutYield(reg.getCutFlowList()[icut], bkg, icut)

            # get the background yield from the previous cut to calculate the efficiency
            # of the current cut
            efficiency = ""
            if icut == 0 : efficiency = "1.00"
            elif icut != 0 and float(table[icut-1][ib+1]) > 0: efficiency = "%.2f"%(bkgYield / float(table[icut-1][ib+1]) * 1.0)
            eff_list.append(efficiency)

            # add an entry to this row
            line.append("%.2f"%bkgYield)

        # add the efficiencies for this cut
        efficiencies.append(eff_list)
        print cut
        table.append(line)

    # add the efficiencies to the row values by editting the current table
    new_table = []
    for icut, line in enumerate(table) :
        new_line = []
        new_line.append(line[0])
        for iB, bkg in enumerate(backgrounds) :
            bline = line[iB+1] 
            bline += " (%s)"%(efficiencies[icut][iB])
            new_line.append(bline)
        new_table.append(new_line)
    table = new_table
            
    print tabulate(table, headers, tablefmt="rst", numalign="right", stralign="left", floatfmt=".2f")

################################################
## get the yield for a background given a tcut
def get_yield(background, tcut, isData) :

    cut = ""
    if not isData :
        cut = "(" + tcut + ") * eventweight * " + str(b.scale_factor)
    else :
        cut = "(" + tcut + ")"

    cut = r.TCut(cut)
    sel = r.TCut("1")
    h = pu.th1f("h_"+b.treename+"_yield_", "", 4, 0, 1,"","")
    cmd = "%s>>%s"%("isMC", h.GetName())
    background.tree.Draw(cmd, cut * sel, "goff") 

    err = r.Double(0.0)
    integral = h.IntegralAndError(0, -1, err)
    h.Delete()
    return integral, err
    

################################################
## make yields tables
def make_yieldsTable(reg_, data, backgrounds) :
    print "make_yieldsTable    region    : %s (%s)"%(reg_.name, reg_.displayname)
    print "                    selection : %s"%(reg_.tcut)

    headers = ["Region"]
    for bkg in backgrounds :
        headers.append(bkg.displayname)
    headers.append("Total SM")
    if data :
        headers.append("Data")
    # table as a list for tabulate module
    #  > each entry is a list and corresponds to a single row in the table (not including header)
    #  > for each list (row), each entry is a table value at coordinate (row, column) <==> table[iRow][iColumn]
    table = []

    row = []
    row.append(reg_.displayname)

    total_MC_yield = 0.0
    total_MC_stat_err = 0.0
    for bkg in backgrounds :
        # grab the yield and error
        yld, stat_err = get_yield(bkg, reg_.tcut, False)
        yld_str = "%.2f +/- %.2f"%(yld, stat_err)
        row.append(yld_str)

        total_MC_yield += yld
        total_MC_stat_err += stat_err * stat_err

    # get the yield for total MC
    total_MC_stat_err = sqrt(total_MC_stat_err)
    total_MC_str = "%.2f +/- %.2f"%(total_MC_yield, total_MC_stat_err)
    row.append(total_MC_str)
    
    # get the data yield
    if data : 
        data_yld, data_stat_err = get_yield(data, reg_.tcut, True)
        data_yld_str = "%.2f +/- %.2f"%(data_yld, data_stat_err)
        row.append(data_yld_str)

    table.append(row)

    print tabulate(table, headers, tablefmt="rst", numalign="right", stralign="left", floatfmt=".2f")

################################################
## make the tables
def make_tables(regions_, data, backgrounds) :

    # put signal samples at the end
    ordered_backgrounds = []
    for b in backgrounds :
        if not b.isSignal() : ordered_backgrounds.append(b)
    for b in backgrounds :
        if b.isSignal() : ordered_backgrounds.append(b)
    backgrounds = ordered_backgrounds

    for reg_ in regions_ :
        if reg.isCutFlow() :
            make_cutflow(reg_, data, backgrounds)
        else :
            #set_eventlists([reg], backgrounds, data) 
            make_yieldsTable(reg_, data, backgrounds)

################################################
## main
if __name__=="__main__" :

    # just make these global so we don't have to move them around everywhere
    global indir, config, doSys, dbg

    parser = OptionParser()
    parser.add_option("-i", "--indir",  dest="indir", default="") 
    parser.add_option("-c", "--config", dest="config", default="")
    parser.add_option("-s", "--doSys",  action="store_true", dest="doSys", default=False)
    parser.add_option("-d", "--dbg",    action="store_true", dest="dbg", default=False)
    parser.add_option("-u", "--usage",  action="store_true", dest="usage", default=False)
    (options, args) = parser.parse_args()
    indir  = options.indir
    config = options.config
    doSys  = options.doSys
    dbg    = options.dbg
    usage  = options.usage
    if usage : print_usage()

    print "+ ----------------------------- +"
    print "   tabler                        "
    print "         input options           "
    print "   input directory : %s          "%indir
    print "   config          : %s          "%config
    print "   systematics     : %s          "%doSys
    print "   debug           : %s          "%dbg
    print "+ ----------------------------- +"

    # get the config file
    conf_file = get_config() 

    # container for the regions
    regions = []
    # container for the backgrounds/samples
    backgrounds = []
    data = None

    # container for systematics (if any)
    systematics = []

    # load the config
    execfile(conf_file) 

    # print out the loaded backgrounds
    print "+ ----------------------------- +"
    print "   Loaded backgrounds:           "
    for b in backgrounds :
        b.Print()
    if data :
        print "   Loaded data sample:       "
        print data.Print()    
    print "+ ----------------------------- +"
    if doSys :
        print "+ ----------------------------- +"
        print "   Loaded systematics:           "
        for s in systematics :
            s.check()
            s.Print()
            for b in backgrounds :
                b.addSys(s)
                if dbg :
                    for s in b.systList :
                        print s.tree
        print "+ ----------------------------- +"

    # set event lists
    #set_eventlists(regions, backgrounds, data)
    # make tables
    make_tables(regions, data, backgrounds)

 
