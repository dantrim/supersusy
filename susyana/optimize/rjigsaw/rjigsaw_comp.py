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
backgrounds = []

#### MC

### ttbar
ttbar = background.Background("ttbar", "ttbar")
ttbar.scale_factor = 1
ttbar.set_fillStyle(0)
ttbar.setLineStyle(1)
ttbar.set_color(r.TColor.GetColor("#FC0D1B"))
ttbar.set_treename("ttbar")
ttbar.set_chain_from_list_CONDOR(filelist_dir + "ttbar/", rawdir)
backgrounds.append(ttbar)

### zjets
zjets = background.Background("zjets", "Z+jets (PowHeg)")
zjets.set_debug()
zjets.scale_factor = 1
zjets.set_color(r.TColor.GetColor("#82DE68"))
zjets.set_treename("zjets")
zjets.set_chain_from_list_CONDOR(filelist_dir + "zjets/", rawdir)
backgrounds.append(zjets)


### singletop
stop = background.Background("st", "ST")
stop.scale_factor = 2.4
stop.set_color(r.TColor.GetColor("#DE080C"))
stop.set_treename("ST")
stop.set_chain_from_list_CONDOR(filelist_dir + "singletop/", rawdir)
backgrounds.append(stop)

### wjets
wjets = background.Background("wjets", "Wjets (PowHeg)")
wjets.scale_factor = 2.4
wjets.set_color(r.TColor.GetColor("#5E9AD6"))
wjets.set_treename("wjets")
wjets.set_chain_from_list_CONDOR(filelist_dir + "wjets/", rawdir)
backgrounds.append(wjets)

### ww
ww = background.Background("vv", "vv")
ww.scale_factor = 2.4
ww.set_color(r.TColor.GetColor("#41C1FC"))
ww.set_treename("vv")
ww.set_chain_from_list_CONDOR(filelist_dir + "sherpaVV/", rawdir)
backgrounds.append(ww)

### bwn -- (250, 160)
bwn0 = background.Background("bwn250_160", "(250,160)")
bwn0.setSignal()
bwn0.scale_factor = 2.4
bwn0.set_fillStyle(0)
bwn0.setLineStyle(2)
bwn0.set_color(r.kBlue)
bwn0.set_treename("sig1")
bwn0.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "406009")
backgrounds.append(bwn0)

### bwn -- (300, 150)
bwn1 = background.Background("bwn300_150", "(350,150)")
bwn1.setSignal()
bwn1.scale_factor = 2.4
bwn1.set_fillStyle(0)
bwn1.setLineStyle(2)
bwn1.set_color(r.kGreen)
bwn1.set_treename("sig2")
bwn1.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "406010")
backgrounds.append(bwn1)

### bwn -- (300, 180)
bwn2 = background.Background("bwn300_180", "(300,180)")
bwn2.setSignal()
bwn2.scale_factor = 2.4
bwn2.set_fillStyle(0)
bwn2.setLineStyle(2)
bwn2.set_color(r.kRed)
bwn2.set_treename("sig3")
bwn2.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "406011")
backgrounds.append(bwn2)


#### DATA
data = background.Data()
data.set_color(r.kBlack)
data.set_treename("Data")
data.set_chain_from_list_CONDOR(filelist_dir + "data/", data_rawdir)


#############################################
# Set up the regions
#############################################
regions = []

reg = region.Region("rjr", "Stop2l-RJR")
reg.tcut = "nLeptons==2 && abs(mll-91.2)>12 &&  (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && nSJets==1 && j_pt[0] > 100"
regions.append(reg)


#############################################
# Set up the plots
#############################################

plots = []

yy = 100000

## mt2
p = plot.Plot1D()
p.initialize("rjr", "mt2", "rjr_mt2")
p.labels(x="mt2", y = "")
p.xax(10, 0, 220)
p.doLogY = True
p.yax(0.1, yy)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## MDR
p = plot.Plot1D()
p.initialize("rjr", "MDR", "rjr_MDR")
p.labels(x="MDR", y = "")
p.xax(10, 0, 220)
p.doLogY = True
p.yax(0.1, yy)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## DPB
p = plot.Plot1D()
p.initialize("rjr", "DPB_vSS", "rjr_DPB")
p.labels(x="DPB", y = "")
p.xax(0.1, 0, 3.2)
p.doLogY = True
p.yax(0.1, yy)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## R1
p = plot.Plot1D()
p.initialize("rjr", "R1", "rjr_R1")
p.labels(x="R1", y ="")
p.xax(0.05, 0, 1)
p.doLogY = True
p.yax(0.1, yy)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## R2
p = plot.Plot1D()
p.initialize("rjr", "R2", "rjr_R2")
p.labels(x="R2", y = "")
p.xax(0.05, 0, 1)
p.doLogY = True
p.leg_is_bottom_left = True
p.yax(0.1, yy)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## H_11_SS
p = plot.Plot1D()
p.initialize("rjr", "H_11_SS", "rjr_H11SS")
p.labels(x="H_{11}^{SS} [GeV]", y = "")
p.xax(10, 0, 400)
p.doLogY = True
p.yax(0.1, yy)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## H_21_SS
p = plot.Plot1D()

p.initialize("rjr", "H_21_SS", "rjr_H21SS")
p.labels(x="H_{21}^{SS} [GeV]", y = "")
p.xax(10, 0, 600)
p.doLogY = True
p.yax(0.1, yy)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## H_22_SS
p = plot.Plot1D()

p.initialize("rjr", "H_22_SS", "rjr_H22SS")
p.labels(x="H_{22}^{SS} [GeV]", y = "")
p.xax(10, 0, 800)
p.doLogY = True
p.yax(0.1, yy)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## H_11_S1
p = plot.Plot1D()

p.initialize("rjr", "H_11_S1", "rjr_H11S1")
p.labels(x="H_{11}^{S1} [GeV]", y = "")
p.xax(10, 0, 300)
p.doLogY = True
p.yax(0.1, yy)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## H_11_SS / H_21_SS
p = plot.Plot1D()

p.initialize("rjr", "H_11_SS/H_21_SS", "rjr_RH11SSH21SS")
p.labels(x="H_{11}^{SS}/H_{21}^{SS}", y = "")
p.xax(0.05, 0, 1)
p.doLogY = True
p.yax(0.1, yy)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## H_11_SS / H_11_S1
p = plot.Plot1D()

p.initialize("rjr", "H_11_SS/H_11_S1", "rjr_RH11SSH11S1")
p.labels(x="H_{11}^{SS}/H_{11}^{S1}", y = "")
p.xax(0.5, 0, 20)
p.doLogY = True
p.yax(0.1, yy)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## H_11_S1 / H_22_SS
p = plot.Plot1D()

p.initialize("rjr", "H_11_S1/H_22_SS", "rjr_RH11S1H22SS")
p.labels(x="H_{11}^{S1}/H_{22}^{SS}", y = "")
p.xax(0.02, 0, 0.5)
p.doLogY = True
p.yax(0.1, yy)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## shat
p = plot.Plot1D()

p.initialize("rjr", "shat", "rjr_shat")
p.labels(x="shat [GeV]", y = "")
p.xax(10, 0, 500)
p.doLogY =True
p.yax(0.1, yy)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## pTT_T
p = plot.Plot1D()

p.initialize("rjr", "pTT_T", "rjr_pTT_T")
p.labels(x="p_{TT}^{T} [GeV]", y = "")
p.xax(10, 0, 500)
p.doLogY = True
p.yax(0.1, yy)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## pTT_T / H_22_SS
p = plot.Plot1D()

p.initialize("rjr", "pTT_T/H_22_SS", "rjr_RpTT_T_H_22_SS")
p.labels(x="p_{TT}^{T}/H_{22}^{SS}", y = "")
p.xax(0.05, 0, 2)
p.doLogY = True
p.yax(0.1, yy)
p.setDoubleRatioCanvas(p.name)
plots.append(p)


## pTT_Z
p = plot.Plot1D()

p.initialize("rjr", "pTT_Z", "rjr_pTT_Z")
p.labels(x="p_{TT}^{Z} [GeV]", y = "")
p.xax(10, 0, 500)
p.doLogY = True
p.yax(0.1, yy)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## RPT
p = plot.Plot1D()

p.initialize("rjr", "RPT", "rjr_RPT")
p.labels(x="RPT", y = "")
p.xax(0.05, 0, 1)
p.doLogY = True
p.yax(0.1, yy)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## RPZ
p = plot.Plot1D()

p.initialize("rjr", "RPZ", "rjr_RPZ")
p.labels(x="RPZ", y = "")
p.xax(0.05, 0, 1)
p.doLogY = True
p.yax(0.1, yy)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## gamInvRp1
p = plot.Plot1D()

p.initialize("rjr", "gamInvRp1", "rjr_gamInvRp1")
p.labels(x="1/#gamma_{R+1}", y = "")
p.xax(0.05, 0, 1)
p.doLogY = True
p.yax(0.1, yy)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## costheta_SS
p = plot.Plot1D()

p.initialize("rjr", "costheta_SS", "rjr_costheta_SS")
p.labels(x="cos#theta_{SS}", y = "")
p.xax(0.1, -1, 1)
p.doLogY = True
p.yax(0.1, yy)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## dphi_v_SS
p = plot.Plot1D()

p.initialize("rjr", "dphi_v_SS", "rjr_dphi_v_SS")
p.labels(x="#Delta#phi_{vis}^{SS}", y = "")
p.xax(0.1, 0, 3.2)
p.doLogY = True
p.yax(0.1, yy)
p.setDoubleRatioCanvas(p.name)
plots.append(p)
