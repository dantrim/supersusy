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
ttbar.set_color(r.TColor.GetColor("#FC0D1B"))
ttbar.set_treename("ttbar")
ttbar.set_chain_from_list_CONDOR(filelist_dir + "ttbar/", rawdir)
backgrounds.append(ttbar)

### ww
ww = background.Background("vv", "vv")
ww.scale_factor = 1.0
ww.set_color(r.TColor.GetColor("#41C1FC"))
ww.set_treename("vv")
ww.set_chain_from_list_CONDOR(filelist_dir + "sherpaVV/", rawdir)
backgrounds.append(ww)

colors = [ 2, 3, 4, 5, 6, 7, 8, 9, 30, 38, 46 ]
points = {}
#points["387266"] = "(550,540,1)"
#points["387267"] = "(550,540,100)"
#points["387268"] = "(550,540,200)"
#points["387269"] = "(550,540,300)"
#points["387270"] = "(550,540,350)"
points["387277"] = "(650,640,1)"
points["387278"] = "(650,640,100)"
points["387279"] = "(650,640,200)"
#points["387280"] = "(650,640,300)"
points["387281"] = "(650,640,400)"
points["387282"] = "(650,640,450)"

for i, p in enumerate(points) :
    s = background.Background("bch_%s"%p, points[p])
    s.setSignal()
    s.scale_factor = 1.0
    s.set_fillStyle(0)
    s.setLineStyle(2)
    s.set_color(colors[i])
    s.set_treename("bch_%s"%p)
    s.set_chain_from_list_CONDOR(filelist_dir + "bchargino/", rawdir, str(p))
    backgrounds.append(s)


#### bwn -- (300, 180)
#bwn2 = background.Background("bwn300_180", "(300,180)")
#bwn2.setSignal()
#bwn2.scale_factor = 1.0
#bwn2.set_fillStyle(0)
#bwn2.setLineStyle(2)
#bwn2.set_color(r.kRed)
#bwn2.set_treename("sig3")
#bwn2.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "406011")
#backgrounds.append(bwn2)


#### DATA
data = background.Data()
data.set_color(r.kBlack)
data.set_treename("Data")
data.set_chain_from_list_CONDOR(filelist_dir + "data/", data_rawdir)


#############################################
# Set up the regions
#############################################
regions = []

reg = region.Region()
reg.simplename = "wwpre"
reg.displayname = "WW-pre (DFOS-20)"
reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"
regions.append(reg)


#############################################
# Set up the plots
#############################################

plots = []

## R1
p = plot.Plot1D()
p.setComparison()
p.initialize("wwpre", "R1", "wwpre_R1")
p.labels(x="R1", y ="")
p.xax(0.05, 0, 1)
p.doLogY = True
p.leg_is_bottom_left = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

## R2
p = plot.Plot1D()
p.setComparison()
p.initialize("wwpre", "R2", "wwpre_R2")
p.labels(x="R2", y = "")
p.xax(0.05, 0, 1)
p.doLogY = True
p.leg_is_bottom_left = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

## H_11_SS
p = plot.Plot1D()
p.setComparison()
p.initialize("wwpre", "H_11_SS", "wwpre_H11SS")
p.labels(x="H_{11}^{SS} [GeV]", y = "")
p.xax(10, 0, 400)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

## H_21_SS
p = plot.Plot1D()
p.setComparison()
p.initialize("wwpre", "H_21_SS", "wwpre_H21SS")
p.labels(x="H_{21}^{SS} [GeV]", y = "")
p.xax(10, 0, 600)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

## H_22_SS
p = plot.Plot1D()
p.setComparison()
p.initialize("wwpre", "H_22_SS", "wwpre_H22SS")
p.labels(x="H_{22}^{SS} [GeV]", y = "")
p.xax(10, 0, 800)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

## H_11_S1
p = plot.Plot1D()
p.setComparison()
p.initialize("wwpre", "H_11_S1", "wwpre_H11S1")
p.labels(x="H_{11}^{S1} [GeV]", y = "")
p.xax(10, 0, 300)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

## H_11_SS / H_21_SS
p = plot.Plot1D()
p.setComparison()
p.initialize("wwpre", "H_11_SS/H_21_SS", "wwpre_RH11SSH21SS")
p.labels(x="H_{11}^{SS}/H_{21}^{SS}", y = "")
p.xax(0.05, 0, 1)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

## H_11_SS / H_11_S1
p = plot.Plot1D()
p.setComparison()
p.initialize("wwpre", "H_11_SS/H_11_S1", "wwpre_RH11SSH11S1")
p.labels(x="H_{11}^{SS}/H_{11}^{S1}", y = "")
p.xax(0.5, 0, 20)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

## H_11_S1 / H_22_SS
p = plot.Plot1D()
p.setComparison()
p.initialize("wwpre", "H_11_S1/H_22_SS", "wwpre_RH11S1H22SS")
p.labels(x="H_{11}^{S1}/H_{22}^{SS}", y = "")
p.xax(0.02, 0, 0.5)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

## shat
p = plot.Plot1D()
p.setComparison()
p.initialize("wwpre", "shat", "wwpre_shat")
p.labels(x="shat [GeV]", y = "")
p.xax(10, 0, 500)
p.doLogY =True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

## pTT_T
p = plot.Plot1D()
p.setComparison()
p.initialize("wwpre", "pTT_T", "wwpre_pTT_T")
p.labels(x="p_{TT}^{T} [GeV]", y = "")
p.xax(10, 0, 500)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

## pTT_T / H_22_SS
p = plot.Plot1D()
p.setComparison()
p.initialize("wwpre", "pTT_T/H_22_SS", "wwpre_RpTT_T_H_22_SS")
p.labels(x="p_{TT}^{T}/H_{22}^{SS}", y = "")
p.xax(0.05, 0, 2)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)


## pTT_Z
p = plot.Plot1D()
p.setComparison()
p.initialize("wwpre", "pTT_Z", "wwpre_pTT_Z")
p.labels(x="p_{TT}^{Z} [GeV]", y = "")
p.xax(10, 0, 500)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

## RPT
p = plot.Plot1D()
p.setComparison()
p.initialize("wwpre", "RPT", "wwpre_RPT")
p.labels(x="RPT", y = "")
p.xax(0.05, 0, 1)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

## RPZ
p = plot.Plot1D()
p.setComparison()
p.initialize("wwpre", "RPZ", "wwpre_RPZ")
p.labels(x="RPZ", y = "")
p.xax(0.05, 0, 1)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

## gamInvRp1
p = plot.Plot1D()
p.setComparison()
p.initialize("wwpre", "gamInvRp1", "wwpre_gamInvRp1")
p.labels(x="1/#gamma_{R+1}", y = "")
p.xax(0.05, 0, 1)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

## costheta_SS
p = plot.Plot1D()
p.setComparison()
p.initialize("wwpre", "costheta_SS", "wwpre_costheta_SS")
p.labels(x="cos#theta_{SS}", y = "")
p.xax(0.1, -1, 1)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

## dphi_v_SS
p = plot.Plot1D()
p.setComparison()
p.initialize("wwpre", "dphi_v_SS", "wwpre_dphi_v_SS")
p.labels(x="#Delta#phi_{vis}^{SS}", y = "")
p.xax(0.1, 0, 3.2)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)
