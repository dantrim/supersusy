#!/bin/env python

import sys
sys.path.append('../../../../../')
import supersusy.utils.plot as plot
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region


#############################################
# Set up the samples
#############################################
rawdir = "/data/uclhc/uci/user/dantrim/ntuples/rjigsaw/mc/Raw/"
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/rjigsaw/data/Raw/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0216val/filelists/"

truth_dir = "/data/uclhc/uci/user/dantrim/TruthAna/superTruth/"
diboson_file = truth_dir + "superTruth_361068_WWlvlv.root"
ttbar_file   = truth_dir + "superTruth_410000_ttbar_nonAllHad.root"
sig250_file  = truth_dir + "superTruth_406009_250_160.root"
sig300_file  = truth_dir + "superTruth_406011_300_180.root"

backgrounds = []

#### MC

## ttbar
ttbar = background.Background("ttbar", "t#bar{t}")
ttbar.scale_factor = 1
ttbar.set_color(r.TColor.GetColor("#FC0D1B"))
ttbar.set_treename("superTruth")
ttbar.set_file(ttbar_file)
ttbar.set_tree()
backgrounds.append(ttbar)

## diboson
diboson = background.Background("vv", "VV")
diboson.scale_factor = 1.0
diboson.set_color(r.TColor.GetColor("#41C1FC"))
diboson.set_treename("superTruth")
diboson.set_file(diboson_file)
diboson.set_tree()
backgrounds.append(diboson)

sig250 = background.Background("sig250", "(250,160)")
sig250.line_style = 2
sig250.scale_factor = 1.0
sig250.set_color(38)
sig250.set_treename("superTruth")
sig250.set_file(sig250_file)
sig250.set_tree()
backgrounds.append(sig250)

sig300 = background.Background("sig300", "(300,180)")
sig300.line_style = 2
sig300.scale_factor = 1.0
sig300.set_color(46)
sig300.set_treename("superTruth")
sig300.set_file(sig300_file)
sig300.set_tree()
backgrounds.append(sig300)


#############################################
# Set up the regions
#############################################
regions = []

reg = region.Region()
reg.simplename = "wwpre"
reg.displayname = "WW-pre (DFOS-20)"
reg.tcut = "nLeptons==2 && isDF==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"
regions.append(reg)


#############################################
# Set up the plots
#############################################

plots = []

for rs in ["wwpre"] :

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "l_pt[0]", rs + "_lpt0")
    p.labels(x="lpt0 [Gev]", y ="")
    p.xax(10, 0, 200)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "l_pt[1]", rs + "_lpt1")
    p.labels(x="lpt1 [Gev]", y ="")
    p.xax(10, 0, 200)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "l_type[0]", rs + "_type0")
    p.labels(x="lead lep mcType", y = "")
    p.xax(1, 0, 40)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "l_type[1]", rs + "_type1")
    p.labels(x="sub-lead lep mcType", y = "")
    p.xax(1, 0, 40)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "l_origin[0]", rs + "_origin0")
    p.labels(x="lead lep mcOrigin", y = "")
    p.xax(1, 0, 40)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "l_origin[1]", rs + "_origin1")
    p.labels(x="sub-lead lep mcOrigin", y = "")
    p.xax(1, 0, 40)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "j_n", rs + "_jn")
    p.labels(x="j_n")
    p.xax(1, 0, 10)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "j_pt[0]", rs + "_jpt0")
    p.labels(x="jpt0 [GeV]")
    p.xax(10, 0, 200)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "lj_n", rs + "_ljn")
    p.labels(x="lj_n")
    p.xax(1, 0, 10)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "lj_pt[0]", rs + "_ljpt0")
    p.labels(x="ljpt0 [GeV]")
    p.xax(10, 0, 200)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "bj_n", rs + "_bjn")
    p.labels(x="bj_n")
    p.xax(1, 0, 10)
    p.doLogY = True
    p.yax(0.1, 100) 
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "bj_pt[0]", rs + "_bjpt0")
    p.labels(x="bjpt0 [GeV]")
    p.xax(10, 0, 200)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "met_et", rs + "_met_et")
    p.labels(x="met_et [GeV]")
    p.xax(10, 0, 200)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "mt2", rs + "_mt2")
    p.labels(x="mt2 [GeV]")
    p.xax(10, 0, 200)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "meff", rs + "_meff")
    p.labels(x="meff [GeV]")
    p.xax(10, 0, 500)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "meff_S2L", rs + "_meff_S2L")
    p.labels(x="meff S2L [GeV]")
    p.xax(10, 0, 500)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "dphiLL", rs + "_dphiLL")
    p.labels(x="dphiLL")
    p.xax(0.2, -3.2, 3.2)
    p.doLogY = True
    p.yax(0.1, 100) 
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "ptLL", rs + "_ptLL")
    p.labels(x="ptLL [GeV]")
    p.xax(10, 0, 200)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "drLL", rs + "_drLL")
    p.labels(x="drLL")
    p.xax(0.1, 0, 5)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "pbLL", rs + "_pbLL")
    p.labels(x="pbLL [GeV]")
    p.xax(10, 0, 200)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "dphi_met_pbLL", rs + "_dphi_met_pbLL")
    p.labels(x="dphi_met_pbLL")
    p.xax(0.2, -3.2, 3.2)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "r1", rs + "_r1")
    p.labels(x="r1")
    p.xax(0.05, 0, 1)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "r2", rs + "_r2")
    p.labels(x="r2")
    p.xax(0.05, 0, 1)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "r1_S2L", rs + "_r1_S2L")
    p.labels(x="r1 S2L")
    p.xax(0.05, 0, 1)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name) 
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "dr_l0_j0", rs + "_dr_l0_j0")
    p.labels(x="dr l0 j0")
    p.xax(0.1, 0, 5)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "dr_l1_j0", rs + "_dr_l1_j0")
    p.labels(x="dr l1 j0")
    p.xax(0.1, 0, 5)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "dr_l0_bj0", rs + "_dr_l0_bj0")
    p.labels(x="dr l0 bj0")
    p.xax(0.1, 0, 5)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "dr_l0_lj0", rs + "_dr_l0_lj0")
    p.labels(x="dr l0 lj0")
    p.xax(0.1, 0, 5)
    p.doLogY = True
    p.yax(0.1, 100) 
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "dphi_l0_j0", rs + "_dphi_l0_j0")
    p.labels(x="dphi l0 j0")
    p.xax(0.2, -3.2, 3.2)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "dphi_l1_j0", rs + "_dphi_l1_j0")
    p.labels(x="dphi l1 j0")
    p.xax(0.2, -3.2, 3.2)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "dphi_l0_bj0", rs + "_dphi_l0_bj0")
    p.labels(x="dphi l0 bj0")
    p.xax(0.2, -3.2, 3.2)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "dphi_ptLL_j0", rs + "_dphi_ptLL_j0")
    p.labels(x="dphi ptLL j0")
    p.xax(0.2, -3.2, 3.2)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)


    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "dphi_ptLL_bj0", rs + "_dphi_ptLL_bj0")
    p.labels(x="dphi ptLL bj0")
    p.xax(0.2, -3.2, 3.2)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "dphi_ptLL_lj0", rs + "_dphi_ptLL_lj0")
    p.labels(x="dphi ptLL lj0")
    p.xax(0.2, -3.2, 3.2)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "dphi_l0_met", rs + "_dphi_l0_met")
    p.labels(x="dphi l0 met")
    p.xax(0.2, -3.2, 3.2)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "dphi_l1_met", rs + "_dphi_l1_met")
    p.labels(x="dphi l1 met")
    p.xax(0.2, -3.2, 3.2)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "dphi_ptLL_met", rs + "_dphi_ptLL_met")
    p.labels(x="dphi ptLL met")
    p.xax(0.2, -3.2, 3.2)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "Rsib", rs + "_Rsib")
    p.labels(x="Rsib")
    p.xax(40, -200, 200)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "dphi_met_j0", rs + "_dphi_met_j0")
    p.labels(x="dphi met j0")
    p.xax(0.2, -3.2, 3.2)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "dphi_met_bj0", rs + "_dphi_met_bj0")
    p.labels(x="dphi met bj0")
    p.xax(0.2, -3.2, 3.2)
    p.doLogY = True
    p.yax(0.1, 100) 
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "dphi_met_lj0", rs + "_dphi_met_lj0")
    p.labels(x="dphi met lj0")
    p.xax(0.2, -3.2, 3.2)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "deltaX", rs + "_deltaX")
    p.labels(x="deltaX")
    p.xax(0.005, 0, 0.1)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "cosThetaB", rs + "_cosThetaB")
    p.labels(x="cosThetaB")
    p.xax(0.1, -1, 1)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "shatr", rs + "_shatr")
    p.labels(x="shatr [GeV]")
    p.xax(40, 0, 800)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "DPB", rs + "_DPB")    
    p.labels(x="DPB")
    p.xax(0.1, 0, 3.2)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "dphi_l1_l2", rs + "_dphi_l1_l2")
    p.labels(x="dphi_l1_l2")
    p.xax(0.1, 0, 3.2)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "MDR", rs + "_MDR")
    p.labels(x="MDR [Gev]")
    p.xax(10, 0, 200)  
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.setComparison()
    p.initialize(rs, "cosThetaRp1", rs + "_cosThetaRp1")
    p.labels(x="cosThetaRp1")
    p.xax(0.05, -1, 1)
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)
    







