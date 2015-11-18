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

### bwn -- (250, 160)
bwn0 = background.Background("bwn250_160", "(250,160)")
bwn0.setSignal()
bwn0.scale_factor = 1.0
bwn0.set_fillStyle(0)
bwn0.setLineStyle(2)
bwn0.set_color(r.kBlue)
bwn0.set_treename("sig1")
bwn0.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "406009")
backgrounds.append(bwn0)

### bwn -- (300, 150)
bwn1 = background.Background("bwn300_150", "(350,150)")
bwn1.setSignal()
bwn1.scale_factor = 1.0
bwn1.set_fillStyle(0)
bwn1.setLineStyle(2)
bwn1.set_color(r.kGreen)
bwn1.set_treename("sig2")
bwn1.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "406010")
backgrounds.append(bwn1)

### bwn -- (300, 180)
bwn2 = background.Background("bwn300_180", "(300,180)")
bwn2.setSignal()
bwn2.scale_factor = 1.0
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

reg = region.Region()
reg.simplename = "wwpre"
reg.displayname = "WW-pre (DFOS-20)"
reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"
regions.append(reg)


#############################################
# Set up the plots
#############################################

plots = []
#samples = ["vv"]
#samples = ["ttbar"]
samples = ["bwn300_150"]

plots = []
for s in samples :
    p = plot.Plot2D()
    p.initialize("wwpre", "H_11_S1/H_22_SS", "H_11_SS/H_21_SS", "wwpre_R11S122SS_R11SS21SS_%s_2d"%s)
    p.labels(x="H_{11}^{S1}/H_{22}^{SS}", y = "H_{11}^{SS}/H_{21}^{SS}")
    p.set_sample(s)
    p.xax(0.02, 0, 0.5)
    p.yax(0.05, 0, 1)
    p.defaultCanvas()
    plots.append(p)

    p = plot.Plot2D()
    p.initialize("wwpre", "H_11_S1/H_22_SS", "RPT", "wwpre_R11S122SS_RPT_%s_2d"%s)
    p.labels(x="H_{11}^{S1}/H_{22}^{SS}", y = "RPT")
    p.set_sample(s)
    p.xax(0.02, 0, 0.5)
    p.yax(0.05, 0, 1)
    p.defaultCanvas()
    plots.append(p)

    p = plot.Plot2D()
    p.initialize("wwpre", "H_11_S1/H_22_SS", "DPB_vSS", "wwpre_R11S122SS_DPB_%s_2d"%s)
    p.labels(x="H_{11}^{S1}/H_{22}^{SS}", y = "DPB")
    p.set_sample(s)
    p.xax(0.02, 0, 0.5)
    p.yax(0.1, 0, 3.2)
    p.defaultCanvas()
    plots.append(p)

    p = plot.Plot2D()
    p.initialize("wwpre", "H_11_S1/H_22_SS", "gamInvRp1", "wwpre_R11S122SS_gamInvRp1_%s_2d"%s)
    p.labels(x="H_{11}^{S1}/H_{22}^{SS}", y = "1/#gamma_{R+1}")
    p.set_sample(s)
    p.xax(0.02, 0, 0.5)
    p.yax(0.05, 0, 1)
    p.defaultCanvas()
    plots.append(p)

    p = plot.Plot2D()
    p.initialize("wwpre", "H_11_SS/H_21_SS", "dphi_v_SS", "wwpre_R11S122SS_dphi_v_SS_%s_2d"%s)
    p.labels(x="H_{11}^{S1}/H_{22}^{SS}", y = "dphi_v_SS")
    p.set_sample(s)
    p.xax(0.02, 0, 0.5)
    p.yax(0.1, 0, 3.2)
    p.defaultCanvas()
    plots.append(p)

    ##
    p = plot.Plot2D()
    p.initialize("wwpre", "H_11_SS/H_21_SS", "RPT", "wwpre_R11SS21SS_RPT_%s_2d"%s)
    p.labels(x="H_{11}^{SS}/H_{21}^{SS}", y = "RPT")
    p.set_sample(s)
    p.xax(0.05, 0, 1)
    p.yax(0.05, 0, 1)
    p.defaultCanvas()
    plots.append(p)

    p = plot.Plot2D()
    p.initialize("wwpre", "H_11_SS/H_21_SS", "DPB_vSS", "wwpre_R11SS21SS_DPB_%s_2d"%s)
    p.labels(x="H_{11}^{SS}/H_{21}^{SS}", y = "DPB")
    p.set_sample(s)
    p.xax(0.05, 0, 1)
    p.yax(0.1, 0, 3.2)
    p.defaultCanvas()
    plots.append(p)

    p = plot.Plot2D()
    p.initialize("wwpre", "H_11_SS/H_21_SS", "gamInvRp1", "wwpre_R11SS21SS_gamInvRp1_%s_2d"%s)
    p.labels(x="H_{11}^{SS}/H_{21}^{SS}", y = "1/#gamma_{R+1}")
    p.set_sample(s)
    p.xax(0.05, 0,1)
    p.yax(0.05, 0, 1)
    p.defaultCanvas()
    plots.append(p)

    p = plot.Plot2D()
    p.initialize("wwpre", "H_11_SS/H_21_SS", "dphi_v_SS", "wwpre_R11SS21SS_dphi_v_SS_%s_2d"%s)
    p.labels(x="H_{11}^{SS}/H_{21}^{SS}", y = "dphi_v_SS")
    p.set_sample(s)
    p.xax(0.05, 0, 1)
    p.yax(0.1, 0, 3.2)
    p.defaultCanvas()
    plots.append(p)

    ##
    p = plot.Plot2D()
    p.initialize("wwpre", "RPT", "gamInvRp1", "wwpre_RPT_gamInvRp1_%s_2d"%s)
    p.labels(x="RPT", y = "1/#gamma_{R+1}")
    p.set_sample(s)
    p.xax(0.05, 0, 1)
    p.yax(0.05, 0, 1)
    p.defaultCanvas()
    plots.append(p)

    ##
    p = plot.Plot2D()
    p.initialize("wwpre", "shat", "gamInvRp1", "wwpre_shat_gamInvRp1_%s_2d"%s)
    p.labels(x="shat", y = "1/#gamma_{R+1}")
    p.set_sample(s)
    p.xax(40, 0, 1000)
    p.yax(0.05, 0, 1)
    p.defaultCanvas()
    plots.append(p)

    ##
    p = plot.Plot2D()
    p.initialize("wwpre", "DPB_vSS", "dphi_v_SS", "wwpre_DPB_dphi_v_SS_%s_2d"%s)
    p.labels(x="DPB", y="dphi_v_SS")
    p.set_sample(s)
    p.xax(0.1, 0, 3.2)
    p.yax(0.1, 0, 3.2)
    p.defaultCanvas()
    plots.append(p)
    
