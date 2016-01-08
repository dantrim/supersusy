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
rawdir = "/data/uclhc/uci/user/dantrim/ntuples/rjigsaw/xrj/mc/Raw/"
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/rjigsaw/data/Raw/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0216val/filelists/"
backgrounds = []

#### MC

### zjets
zjets = background.Background("zjets", "zjets (sherpa)")
zjets.scale_factor = 1.0
zjets.set_color(r.kBlack)
zjets.set_treename("zjets")
zjets.set_chain_from_list_CONDOR(filelist_dir + "zjets_sherpa/", rawdir)
backgrounds.append(zjets)

### ttbar
ttbar = background.Background("ttbar", "ttbar")
ttbar.scale_factor = 1
ttbar.set_color(r.TColor.GetColor("#FC0D1B"))
ttbar.set_treename("ttbar")
ttbar.set_chain_from_list_CONDOR(filelist_dir + "ttbar/", rawdir)
backgrounds.append(ttbar)

### singletop
stop = background.Background("st", "st")
stop.scale_factor = 1
stop.set_color(r.TColor.GetColor("#DE080C"))
stop.set_treename("ST")
stop.set_chain_from_list_CONDOR(filelist_dir + "singletop/", rawdir)
backgrounds.append(stop)

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

isSF = "((nElectrons==2 || nMuons==2) && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0"
isDF = "(nElectrons==1 && nMuons==1) && (l_q[0]*l_q[1])<0"

reg = region.Region()
reg.simplename = "wwpre"
reg.displayname = "WW-pre (DFOS-20)"
reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && nJets>=2 && nBJets==0 && DPB_vSS<1 && MDR>30 && xMS>150"
regions.append(reg)

reg = region.Region()
reg.simplename = "wwpre2"
reg.displayname = "WW (DFOS-20, nJets>=2, #Delta#beta^{SS}<0.6, DPB>2"
reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && nJets>=2 && xDeltaBetaSS<0.6 && xDPB_vSS>2.0"
regions.append(reg)

reg = region.Region()
reg.simplename = "pre"
reg.displayname = "WW (DFOS-20)"
reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"
regions.append(reg)

reg = region.Region()
reg.simplename = "crw"
reg.displayname = "WW CRW"
reg.tcut = "nLeptons==2 && " + isDF + " && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && nJets>=2 && MDR>30 && xH_11_SS/xH_42_SS_T>0.3 && xMS>150 && DPB_vSS<2"# && gamInvRp1>0.62"
#reg.tcut = "nLeptons==2 && " + isDF + " && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && nJets>=2 && MDR>30 && xH_11_SS/xH_42_SS_T>0.3 && gamInvRp1>0.3 && xMS>150 && DPB_vSS<2"
#reg.tcut = "nLeptons==2 && " + isSF + " && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && nJets==2 && MDR>30 && RPT<0.3 && DPB_vSS<2 && DPB_vSS>1"
regions.append(reg)


#############################################
# Set up the plots
#############################################

plots = []

vars = {}
#vars["xshat"] = [40, 0, 3000]
#vars["xgaminv"] = [0.05, 0, 1]
#vars["xRPT"] = [0.05, 0, 1]
#vars["xRPZ"] = [0.2, -2, 5]
#vars["xcosSS"] = [0.1, -1, 1]
#vars["xdphiLSS"] = [0.2, 0, 7]
vars["xMS"] = [20, 0, 600]
#vars["xPS"] = [40, 0, 1000]
#vars["xMSS"] = [40, 0, 2000]
#vars["xgaminvSS"] = [0.05, 0, 1]
#vars["xDeltaBetaSS"] = [0.1, -1, 1]
#vars["xDPD_vSS"] = [0.1, 0, 3.2]
#vars["xDPB_vSS"] = [0.1, 0, 3.2]
#vars["xNV[0]"] = [1, 0, 6]
#vars["xNV[1]"] = [1, 0, 6]
#vars["xcosS[0]"] = [0.1, -1, 1]
#vars["xcosS[1]"] = [0.1, -1, 1]
#vars["xdphiSC[0]"] = [0.2, 0, 7]
#vars["xdphiSC[1]"] = [0.2, 0, 7]
#vars["xRCS[0]"] = [0.05, 0, 1]
#vars["xRCS[1]"] = [0.05, 0, 1]
#vars["xjet1PT[0]"] = [20, 0, 700]
#vars["xjet1PT[1]"] = [20, 0, 700]
#vars["xjet2PT[0]"] = [20, 0, 700]
#vars["xjet2PT[1]"] = [20, 0, 700]
#vars["xPinv[0]"] = [0.05, 0, 1]
#vars["xPinv[1]"] = [0.05, 0, 1]
#vars["xH_11_SS"] = [40, 0, 1000]
#vars["xH_21_SS"] = [40, 0, 2500]
#vars["xH_41_SS"] = [40, 0, 2500]
#vars["xH_42_SS"] = [40, 0, 2500]
#vars["xH_11_S1"] = [20, 0, 5000]
#vars["xH_21_S1"] = [20, 0, 5000]
#vars["xH_11_SS_T"] = [40, 0, 1000]
#vars["xH_21_SS_T"] = [40, 0, 1500]
#vars["xH_41_SS_T"] = [40, 0, 2500]
#vars["xH_42_SS_T"] = [40, 0, 3000]
#vars["xH_11_S1_T"] = [20, 0, 5000]
#vars["xH_21_S1_T"] = [20, 0, 5000]
#vars["xH_11_S1/xH_42_SS"] = [0.5, 0, 10]
#vars["xH_42_SS_T/xH_42_SS"] = [0.05, 0, 1]
vars["xH_11_SS/xH_42_SS_T"] = [0.05, 0, 2]
#vars["deltaX"] = [0.01, 0, 0.2]
#vars["cosThetaB"] = [0.1, -1, 1]
vars["RPT"] = [0.05, 0, 1]
vars["DPB_vSS"] = [0.1, 0, 3.2]
vars["gamInvRp1"] = [0.05, 0, 1]
vars["MDR"] = [10, 0, 300]

run_reg = "crw"
for var, bounds in vars.iteritems() :
    p = plot.Plot1D()
    p.setComparison()
    name_ = ""
    if "/" in var :
        name_ = var.replace("/","")
    else :
        name_ = var
    if "xH_11_SS/xH_42_SS_T" in var or "DPB_vSS" in var or "gamInvRp1" in var or "RPT" in var or "MDR" in var:
        p.leg_is_bottom_left = True
    p.initialize(run_reg, var, "%s_%s"%(run_reg, name_))
    p.labels(x=var)
    p.xax(bounds[0], bounds[1], bounds[2])
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)




#p = plot.Plot1D()
#p.setComparison()
#p.initialize("wwpre2", "nJets", "wwpre2_nJets")
#p.labels(x="nJets", y = "")
#p.xax(1, 0, 12)
#p.doLogY = True
#p.yax(0.1, 100)
#p.setDefaultCanvas(p.name)
#plots.append(p)
#
