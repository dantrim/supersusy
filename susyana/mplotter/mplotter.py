#!/usr/bin/env python

from optparse import OptionParser
import os

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(False)
import sys
sys.path.append(os.environ['SUSYDIR'])

# root preventions
r.TEventList.__init__._creates = False
r.TH1F.__init__._creates = False
r.TGraphErrors.__init__._creates = False
r.TGraphAsymmErrors.__init__._creates = False

# supersusy
import supersusy.utils.plot_utils as pu
import supersusy.utils.utils as utils
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region
import supersusy.utils.mplot as mplot

# cool stuff
from root_numpy import tree2rec
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import numpy as np
#from scipy.stats import kendalltau
import seaborn as sns
sns.set(style="ticks")

def msg(msg="") :
    print "mplotter    %s"%msg

def main() :
    global indir, plotConfig, requestReqegion, outdir, dbg
    parser = OptionParser()
    parser.add_option("-c", "--plotConfig", dest = "plotConfig", default = "")
    parser.add_option("-i", "--indir", dest = "indir", default = "")
    parser.add_option("-r", "--requestRegion", dest = "requestRegion", default = "")
    parser.add_option("-o", "--outdir", dest = "outdir", default = "./")
    parser.add_option("-d", "--dbg", action = "store_true", dest = "dbg", default = False)
    (options, args) = parser.parse_args()
    indir           = options.indir
    plotConfig      = options.plotConfig
    requestRegion   = options.requestRegion
    outdir          = options.outdir
    dbg             = options.dbg

    inputs_bad = False
    if indir == "" :
        msg('ERROR You have not provided an input directory ("-i" / "--indir").')
        inputs_bad = True
    if plotConfig == "" :
        msg('ERROR You have not provided a plot configuration file ("-c" / "--plotConfig").')
        inputs_bad = True
    if inputs_bad :
        sys.exit()

    print " ++ ------------------------------------------ ++ "
    print "      m-plotter"
    print ""
    print "     config directory    : %s                     "%indir
    print "     plot config         : %s                     "%plotConfig
    print "     requested region    : %s                     "%requestRegion
    print "     output directory    : %s                     "%outdir
    print "     debug               : %s                     "%dbg
    print ""
    print " ++ ------------------------------------------ ++ "

    # get the config
   # plots = []
   # data = None
   # backgrounds = []
   # regions = []
   # conf_file = "./stop2L/stop2L.py"
   # execfile(str(conf_file), locals())

   # print conf_file
    print plots
    print data
    print backgrounds
    print regions

    msg("ADD CHECK FOR CONSISTENCY")

    if dbg :
        for p in plots :
            p.Print()
    print " ++ ------------------------------------------ ++ "
    print "     Loaded backgrounds :"
    for b in backgrounds :
        b.Print()
    if data :
        print "     Loaded data sample :"
        data.Print()
    print " ++ ------------------------------------------ ++ "

    # make the plots
    if requestRegion != "" :
        requested_plots = []
        for p in plots :
            if p.region == requestRegion : 
                requested_plots.append(p)
        make_plots(requested_plots, regions, data, backgrounds)
    else :
        make_plots(plots, regions, data, backgrounds)


###############################
def get_plotConfig(conf) :
    global indir
    conf_file = "./" + indir + "/" + conf + ".py"
    if os.path.isfile(conf_file) :
        msg("    Found the configuration file: %s"%conf_file)
        return conf_file
    else :
        msg("ERROR Input plot configuration ('%s') is not found in the directory/path provided ('%s'). Does it exist?"%(conf, conf_file))
        sys.exit()

###############################
def set_eventlists(bkgs, reg) :
    cut = reg.tcut
    cut = r.TCut(cut)
    sel = r.TCut("1")
    for bk in bkgs :
        if bk :
            list_name = "list_" + reg.simplename + "_" + bk.treename
            save_name = "./" + indir + "/lists/" + list_name + ".root"

            # check if the list already exists
            if os.path.isfile(save_name) :
                rfile = r.TFile.Open(save_name)
                list = rfile.Get(list_name)
                msg("%s : EventList found at %s"%(bk.name, os.path.abspath(save_name)))
                if dbg : list.Print()
                bk.tree.SetEventList(list)
            else :
                draw_list = ">> " + list_name
                bk.tree.Draw(draw_list, sel * cut)
                list = r.gROOT.FindObject(list_name)
                bk.tree.SetEventList(list)
                list.SaveAs(save_name)

###############################
def make_plots(plots, regions, data, backgrounds) :
    for reg in regions :
        # gather all the plots that fall under this region
        plots_with_region = []
        for p in plots :
            if p.region == reg.simplename : plots_with_region.append(p)
        if len(plots_with_region) == 0 : continue

        # set event lists
        msg("Checking eventlists for %s"%reg.simplename)
        set_eventlists(backgrounds, reg)
        set_eventlists([data], reg)

        for p in plots_with_region :
            if p.is2D : make_plots2D(p, reg, data, backgrounds)
            else :
                msg("ERROR 2D plotting is the only supported plotting type. Plot with name %s will be skipped"%p.name)
                continue


###################################################################
#
# 2D plotting
#
###################################################################
def make_plots2D(plot, reg, data, backgrounds) :
    if isinstance(plot, mplot.mJointPlot) :
        make_JointPlot(plot, reg, data, backgrounds)
    else :
        msg("ERROR 2D plotting type is not supported for plot with name %s"%plot.name)

#### JointPlot
def make_JointPlot(plot, region, data, backgrounds) :

    sample_to_plot = []
    if data.name == plot.sample : sample_to_plot.append(data)
    if not len(sample_to_plot) :
        for bk in backgrounds :
            if bk.name == plot.sample : sample_to_plot.append(bk)
    if len(sample_to_plot) == 0 or len(sample_to_plot) > 1 :
        msg('ERROR make_JointPlot received %d samples to plot for plot with name %s'%(len(sample_to_plot), plot.name))
        sys.exit()

    # turn this tree into an array :)
    sample_to_plot = sample_to_plot[0]
    selection_ = '(' + region.tcut + ') * eventweight * ' + str(sample_to_plot.scale_factor)
    tree_array = tree2rec(sample_to_plot.tree, branches=[plot.x_var, plot.y_var],
                            selection=selection_)
    tree_array.dtype.names = (plot.x_var, plot.y_var)
    x_arr = tree_array[plot.x_var]
    y_arr = tree_array[plot.y_var]

    sns.set(style="white")

    # stats?
    stat_func_ = None
    if plot.stat_func == "kendalltau" :
        from scipy.stats import kendalltau
        stat_func_ = kendalltau
    elif plot.stat_func == None :
        from scipy.stats import pearsonr
        stat_func_ = pearsonr

    j_plot_grid = None
    if plot.cmap == None or plot.cmap == "default" :
        j_plot_grid = sns.jointplot(x_arr, y_arr, kind = plot.kind, stat_func=stat_func_, color = plot.color, linewidth = plot.line_width, ylim=[plot.y_range_min,plot.y_range_max], xlim=[plot.x_range_min,plot.x_range_max])
        #j_plot_grid = sns.jointplot(x_arr, y_arr, kind = plot.kind, stat_func=stat_func_, color = plot.color, linewidth = plot.line_width, joint_kws={"n_levels":plot.n_levels, "shade":True}, ylim=[plot.y_range_min,plot.y_range_max], xlim=[plot.x_range_min,plot.x_range_max])

    elif plot.cmap == "cubehelix" :
        cmap_ = sns.cubehelix_palette(as_cmap=True, dark=0, light=1, reverse = True)
        j_plot_grid = sns.jointplot(x_arr, y_arr, kind = plot.kind, stat_func=stat_func_, linewidth = plot.line_width, joint_kws={"cmap":cmap_, "n_levels":plot.n_levels, "shade":True}, ylim=[plot.y_range_min, plot.y_range_max], xlim=[plot.x_range_min,plot.x_range_max])
    elif plot.cmap == "blues" :
        j_plot_grid = sns.jointplot(x_arr, y_arr, kind = plot.kind, stat_func=stat_func_, linewidth = 1.0, joint_kws={"cmap":"Blues", "n_levels":plot.n_levels, "shade":True, "shade_lowest":False}, ylim=[plot.y_range_min, plot.y_range_max], xlim=[plot.x_range_min,plot.x_range_max])
    else :
        msg("cmap attribute of joint plot not yet added")
        sys.exit()

    j_plot_grid.fig.suptitle(plot.title)
    j_plot_grid.fig.subplots_adjust(top=0.935)
    j_plot_grid.set_axis_labels(plot.x_label, plot.y_label)


    # save the plot to file
    outname = plot.name + ".eps"
    j_plot_grid.savefig(outname)
    out = indir + "/plots/" + outdir 
    utils.mv_file_to_dir(outname, out, True)
    fullname = out + "/" + outname
    msg("%s saved to : %s"%(outname, os.path.abspath(fullname)))
    

##################################################################################
if __name__=="__main__" :
    plots = []
    data = None
    backgrounds = []
    regions = []
    #conf_file = get_plotConfig(plotConfig)
    execfile("./rjigsaw/rjigsaw_cos_comp.py")
    #execfile(conf_file)
    main()
