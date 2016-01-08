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
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/rjigsaw/xrj/data/Raw/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0216val/filelists/"
backgrounds = []

#### MC
lumi_ = {}
lumi_[3.34] = 1.0
lumi_[6.0] = 1.79
lumi_[7.0] = 2.10
lumi_[8.0] = 2.40
lumi_[9.0] = 2.70
lumi_[10.0] = 3.0
lumi_[20.0] = 5.98

lumi_val = 10.0

# ttbro
ttbar = background.Background("ttbar", "t#bar{t}")
ttbar.set_debug()
ttbar.scale_factor = lumi_[lumi_val]
ttbar.set_fillStyle(0)
ttbar.setLineStyle(1)
ttbar.set_color(r.TColor.GetColor("#E67067"))
#ttbar.set_color(r.TColor.GetColor("#FC0D1B"))
ttbar.set_treename("ttbar_powheg")
ttbar.set_chain_from_list_CONDOR(filelist_dir+ "ttbar/", rawdir)
backgrounds.append(ttbar)

# singletop
stop = background.Background("st", "ST")
stop.set_debug()
stop.scale_factor = lumi_[lumi_val]
stop.set_color(r.TColor.GetColor("#DE080C"))
#stop.set_color(r.TColor.GetColor("#DE080C"))
stop.set_treename("ST")
stop.set_chain_from_list_CONDOR(filelist_dir+ "singletop/", rawdir)
backgrounds.append(stop)

# diboson
diboson = background.Background("vv", "VV (Sherpa)")
diboson.set_debug()
diboson.scale_factor = lumi_[lumi_val]
diboson.set_color(r.TColor.GetColor("#315E88"))
#diboson.set_color(r.TColor.GetColor("#41C1FC"))
diboson.set_treename("diboson_sherpa")
diboson.set_chain_from_list_CONDOR(filelist_dir+ "diboson_sherpa/", rawdir)
backgrounds.append(diboson)


# Zjets
zjets = background.Background("zjets", "Z+jets (Sherpa)")
zjets.set_debug()
zjets.scale_factor = lumi_[lumi_val]
zjets.set_color(r.TColor.GetColor("#82DE68"))
#zjets.set_color(r.TColor.GetColor("#FFEF53"))
zjets.set_treename("zjets_sherpa")
zjets.set_chain_from_list_CONDOR(filelist_dir+ "zjets_sherpa/", rawdir)
backgrounds.append(zjets)

# Wjets
wjets = background.Background("wjets", "W+Jets (PowHeg)")
wjets.set_debug()
wjets.scale_factor = lumi_[lumi_val]
wjets.set_fillStyle(0)
wjets.setLineStyle(1)
wjets.set_color(r.TColor.GetColor("#5E9AD6"))
#wjets.set_color(r.TColor.GetColor("#5E9AD6"))
wjets.set_treename("wjets")
wjets.set_chain_from_list_CONDOR(filelist_dir+ "wjets_powheg/", rawdir)
backgrounds.append(wjets)

#sig1 = background.Background("bwn250_160", "(250,160)")
#sig1.setSignal()
#sig1.set_debug()
#sig1.scale_factor = lumi_[lumi_val]
#sig1.set_color(r.kBlue)
#sig1.set_treename("sig1")
#sig1.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", rawdir, "406009")
#backgrounds.append(sig1)
#
#sig2 = background.Background("bwn300_180", "(300,180)")
#sig2.setSignal()
#sig2.set_debug()
#sig2.scale_factor = lumi_[lumi_val]
#sig2.set_color(r.kGreen)
#sig2.set_treename("sig2")
#sig2.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", rawdir, "406011")
#backgrounds.append(sig2)
#
#sig3 = background.Background("bwn300_150", "(300,150)")
#sig3.setSignal()
#sig3.set_debug()
#sig3.scale_factor = lumi_[lumi_val]
#sig3.set_color(r.kRed)
#sig3.set_treename("sig3")
#sig3.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "406010")
#backgrounds.append(sig3)


#### DATA
data = background.Data()
data.set_color(r.kBlack)
data.set_treename("Data")

#############################################
# Set up the regions
#############################################
regions = []
isEE = "(nElectrons==2 && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0"
isMM = "(nMuons==2 && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0"
isSF = "((nElectrons==2 || nMuons==2) && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0"
isDF = "(nElectrons==1 && nMuons==1) && (l_q[0]*l_q[1])<0"

#####################
# SIGNAL REGIONS
#####################

#reg = region.Region()
#reg.simplename = "rjigsawDF"
#reg.displayname = "Stop2l-Jigsaw (DF)"
#reg.setCutFlow()
#reg.addCut("DF SELECTION", "nLeptons==2 && " + isDF + " && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && nJets>=2 && MDR>80 && xH_11_SS/xH_42_SS_T>0.65 && gamInvRp1>0.62 && RPT>0.5 && DPB_vSS>2. && xMS>150")
#regions.append(reg)
#
#reg = region.Region()
#reg.simplename = "rjigsawSF"
#reg.displayname = "Stop2l-Jigsaw (SF)"
#reg.setCutFlow() 
#reg.addCut("SF SELECTION", "nLeptons==2 && " + isSF + " && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && nJets>=2 && MDR>80 && xH_11_SS/xH_42_SS_T>0.65 && gamInvRp1>0.62 && RPT>0.5 && DPB_vSS>2. && xMS>150")
#regions.append(reg)

#####################
# CONTROL REGIONS
#####################

#reg = region.Region()
#reg.simplename = "crt"
#reg.displayname = "xrj CRT"
#reg.setCutFlow()
#reg.addCut("CRT", "nLeptons==2 && " + isDF + " && l_pt[0]>20 && l_pt[1]>20 && nBJets>0 && nJets>=2 && MDR>30 && xMS>150 && RPT>0.5 && DPB_vSS<2.0")
##reg.addCut("CRT", "nLeptons==2 && " + isDF + " && l_pt[0]>20 && l_pt[1]>20 && nBJets>0 && nJets>=2 && MDR>30 && xH_11_SS/xH_42_SS_T>0.65 && gamInvRp1>0.62 && xMS>150 && RPT>0.5 && DPB_vSS<2.0")
#regions.append(reg)
#
#reg = region.Region()
#reg.simplename = "vrt"
#reg.displayname = "xrj VRT"
#reg.setCutFlow()
#reg.addCut("VRT", "nLeptons==2 && " + isDF + " && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && nJets>=2 && MDR>30 && xMS>150 && RPT>0.5 && DPB_vSS<2.0")
##reg.addCut("VRT", "nLeptons==2 && " + isDF + " && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && nJets>=2 && MDR>30 && xH_11_SS/xH_42_SS_T>0.65 && gamInvRp1>0.62 && xMS>150 && RPT>0.5 && DPB_vSS<2.0")
#regions.append(reg)

reg = region.Region()
reg.simplename = "crw"
reg.displayname = "xrj CRW"
reg.setCutFlow()
#reg.addCut("CRW", "nLeptons==2 && " + isDF + " && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && nJets>=2 && MDR>30 && xMS>150 && DPB_vSS<1 && RPT>0.5 && gamInvRp1<0.4")
#reg.addCut("SF SELECTION", "nLeptons==2 && " + isSF + " && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && nJets>=2 && MDR>80 && xH_11_SS/xH_42_SS_T>0.65 && gamInvRp1>0.62 && RPT>0.5 && DPB_vSS>2. && xMS>150")
#reg.addCut("CRW", "nLeptons==2 && " + isSF + " && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && nJets==2 && MDR>30 && DPB_vSS<2 && xMS>150 && RPT>0.5")
#reg.addCut("CRW", "nLeptons==2 && " + isDF + " && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && nJets>=2 && MDR>30 && xH_11_SS/xH_42_SS_T>0.65 && gamInvRp1>0.62 && xMS>150 && RPT<0.2 && DPB_vSS<2.0")

## TODAY
reg.addCut("CRW", "nLeptons==2 && " + isDF + " && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && nJets>=2 && MDR>30 && xH_11_SS/xH_42_SS_T<0.65 && gamInvRp1>0.62 && xMS>150 && DPB_vSS<1 && RPT>0.5")





#reg.addCut("CRW", "nLeptons==2 && " + isDF + " && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && nJets>=2 && MDR>30 && xH_11_SS/xH_42_SS_T>0.3 && gamInvRp1>0.62 && xMS>150 && DPB_vSS<2")
#reg.addCut("CRW", "nLeptons==2 && " + isDF + " && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && nJets==2 && MDR>30  && gamInvRp1>0.7 && RPT>0.5 && DPB_vSS<0.7")# && xMS>150")
#reg.addCut("CRW", "nLeptons==2 && " + isSF + " && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && nJets==2 && MDR>30 && xH_11_SS/xH_42_SS_T>0.65 && gamInvRp1>0.62 && RPT<0.3 && DPB_vSS<2 && DPB_vSS>1")# && xMS>150")
regions.append(reg)

#reg = region.Region()
#reg.simplename = "vrw"
#reg.displayname = "xrj VRW"
#reg.setCutFlow()
#reg.addCut("VRW", "nLeptons==2 && " + isDF + " && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && nJets>=2 && MDR>30 && xMS>150 && RPT<0.4 && DPB_vSS>2.0")
#regions.append(reg)

reg = region.Region()
reg.simplename = "vrw"
reg.displayname = "xrj VRW"
reg.setCutFlow()
reg.addCut("VRW", "nLeptons==2 && " + isDF + " && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && nJets>=2 && MDR>30 && xH_11_SS/xH_42_SS_T<0.65 && gamInvRp1>0.62 && xMS>150 && DPB_vSS>1 && DPB_vSS<2 && RPT>0.5")
regions.append(reg)

#############################################
# Set up the plots
#############################################

plots = []

