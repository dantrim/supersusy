
##!/bin/env python

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
lumi_ = {}
lumi_[3.21] = 1.0
lumi_[6.0] = 1.87
lumi_[7.0] = 2.18
lumi_[8.0] = 2.50
lumi_[9.0] = 2.80
lumi_[10.0] = 3.12
lumi_[20.0] = 6.23

lumi_val = 10.0

# ttbro
ttbar = background.Background("ttbar", "t#bar{t}")
ttbar.set_debug()
ttbar.scale_factor = lumi_[lumi_val]
ttbar.set_fillStyle(0)
ttbar.setLineStyle(1)
ttbar.set_color(r.TColor.GetColor("#FC0D1B"))
ttbar.set_treename("ttbar_powheg")
ttbar.set_chain_from_list_CONDOR(filelist_dir+ "ttbar/", rawdir)
backgrounds.append(ttbar)

# singletop
stop = background.Background("st", "Single top")
stop.set_debug()
stop.scale_factor = lumi_[lumi_val]
stop.set_fillStyle(0)
stop.setLineStyle(1)
stop.set_color(r.TColor.GetColor("#DE080C"))
stop.set_treename("ST")
stop.set_chain_from_list_CONDOR(filelist_dir+ "singletop/", rawdir)
backgrounds.append(stop)

# diboson
diboson = background.Background("vv", "VV (Sherpa)")
diboson.set_debug()
diboson.scale_factor = lumi_[lumi_val]
diboson.set_fillStyle(0)
diboson.setLineStyle(1)
diboson.set_color(r.TColor.GetColor("#41C1FC"))
diboson.set_treename("diboson_sherpa")
diboson.set_chain_from_list_CONDOR(filelist_dir+ "diboson_sherpa/", rawdir)
backgrounds.append(diboson)


# Zjets
zjets = background.Background("zjets", "Z+jets (Sherpa)")
zjets.set_debug()
zjets.scale_factor = lumi_[lumi_val]
zjets.set_fillStyle(0)
zjets.setLineStyle(1)
zjets.set_color(r.TColor.GetColor("#FFEF53"))
zjets.set_treename("zjets_sherpa")
zjets.set_chain_from_list_CONDOR(filelist_dir+ "zjets_sherpa/", rawdir)
backgrounds.append(zjets)

# Wjets
wjets = background.Background("wjets", "W+Jets (Sherpa)")
wjets.set_debug()
wjets.scale_factor = lumi_[lumi_val]
wjets.set_fillStyle(0)
wjets.setLineStyle(1)
wjets.set_color(r.TColor.GetColor("#5E9AD6"))
wjets.set_treename("wjets")
wjets.set_chain_from_list_CONDOR(filelist_dir+ "wjets_sherpa/", rawdir)
backgrounds.append(wjets)

sig1 = background.Background("bwn250_160", "(250,160)")
sig1.setSignal()
sig1.set_debug()
sig1.scale_factor = lumi_[lumi_val]
sig1.set_fillStyle(0)
sig1.setLineStyle(2)
sig1.set_color(r.kBlue)
sig1.set_treename("sig1")
sig1.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", rawdir, "406009")
backgrounds.append(sig1)

sig2 = background.Background("bwn300_180", "(300,180)")
sig2.setSignal()
sig2.set_debug()
sig2.scale_factor = lumi_[lumi_val]
sig2.setLineStyle(2)
sig2.set_color(r.kGreen)
sig2.set_treename("sig2")
sig2.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", rawdir, "406011")
backgrounds.append(sig2)

sig3 = background.Background("bwn300_150", "(300,150)")
sig3.setSignal()
sig3.set_debug()
sig3.scale_factor = lumi_[lumi_val]
sig3.setLineStyle(2)
sig3.set_color(r.kBlack)
sig3.set_treename("sig3")
sig3.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "406010")
backgrounds.append(sig3)



##### DATA
#data = background.Data()
#data.set_color(r.kBlack)
#data.set_treename("Data")
#data.set_chain_from_list_CONDOR(filelist_dir + "data/", data_rawdir)


#############################################
# Set up the regions
#############################################
regions = []

#reg = region.Region()
#reg.simplename = "wwpre"
#reg.displayname = "WW-pre (DFOS-20)"
#reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && nJets>=2"
#regions.append(reg)

isEE = "(nElectrons==2 && abs(mll-91.2)>10)"
isMM = "(nMuons==2 && abs(mll-91.2)>10)"
isSF = "((nMuons==2 || nElectrons==2) && abs(mll-91.2)>10)"
isDF = "(nElectrons==1 && nMuons==1)"

reg = region.Region()
reg.name = "ww"
reg.displayname = "WW-like"
#reg.setCutFlow()

reg_cut = "nLeptons==2 && " + isMM + " && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && MDR>110 && RPT>0.65 && gamInvRp1>0.65 && DPB_vSS>(1.1*abs(cosThetaB)+1.8) && nBJets>0"
#reg_cut = "nLeptons==2 && " + isMM + " && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && MDR>90 && RPT>0.65 && gamInvRp1>0.65 && DPB_vSS>(1.1*abs(cosThetaB)+1.8) && nBJets==0"
reg.tcut = reg_cut

#reg.addCut("MW", reg_cut)
regions.append(reg)



#############################################
# Set up the plots
#############################################

plots = []

