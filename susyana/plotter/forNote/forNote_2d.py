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
rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0222/apr17/mc/Raw/"
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0222/nom/data/Raw/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0222val/filelists/"
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
ww.set_chain_from_list_CONDOR(filelist_dir + "diboson_sherpa/", rawdir)
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
bwn1 = background.Background("bwn300_150", "(300,150)")
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
#data = background.Data()
#data.set_color(r.kBlack)
#data.set_treename("Data")
#data.set_chain_from_list_CONDOR(filelist_dir + "data/", data_rawdir)


#############################################
# Set up the regions
#############################################
regions = []

isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"
isSFOS = "nLeptons==2 && (nElectrons==2 || nMuons==2) && abs(mll-91.2)>10 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"
isMMOS = "nLeptons==2 && nMuons==2 && abs(mll-91.2)>10 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"
isEEOS = "nLeptons==2 && nElectrons==2 && abs(mll-91.2)>10 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"

reg = region.Region()
reg.name = "wwbveto"
reg.displayname = "WW-pre (DFOS-20) - bveto"
reg.tcut = isDFOS + " && nBJets==0"
regions.append(reg)

#reg = region.Region()
#reg.name = "wwb"
#reg.displayname = "WW-pre (DFOS-20) - >0 b"
#reg.tcut = isDFOS + " && nBJets>0"
#regions.append(reg)


#############################################
# Set up the plots
#############################################

plots = []

vars = {}
vars["RPT"] = [0.05, 0, 1]
vars["DPB_vSS"] = [0.1, 0, 3.2]
vars["MDR"] = [10, 0, 220]
vars["gamInvRp1"] = [0.05, 0 ,1]
vars["abs(cosThetaB)"] = [0.05, 0, 1]

allvariables = vars.keys()

# ttbar vv bwn250_160
sam = "vv"
reg_name = "wwbveto"

p = plot.Plot2D()
xvar_name = "|cos#theta_{b}|"
xvar = "abs(cosThetaB)"
yvar_name = "#Delta#phi(#vec{#beta}_{PP}^{LAB}, #vec{p}_{V}^{PP})"
yvar = "DPB_vSS"
p.initialize(reg_name, xvar, yvar, "%s_%s_%s_%s_2d"%(reg_name, "cosThetaB", yvar, sam))
p.labels(x=xvar_name, y=yvar_name)
p.set_sample(sam)
p.xax(vars[xvar][0], vars[xvar][1], vars[xvar][2])
p.yax(vars[yvar][0], vars[yvar][1], vars[yvar][2])
p.defaultCanvas()
plots.append(p)

