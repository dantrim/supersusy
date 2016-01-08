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
rawdir = "/data/uclhc/uci/user/dantrim/ntuples/rjigsaw/xrj/mc/Raw/"
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/rjigsaw/data/Raw/"
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
ttbar.set_color(r.TColor.GetColor("#FC0D1B"))
ttbar.set_treename("ttbar_powheg")
ttbar.set_chain_from_list_CONDOR(filelist_dir+ "ttbar/", rawdir)
backgrounds.append(ttbar)

# singletop
stop = background.Background("st", "ST")
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
sig3.set_color(r.kRed)
sig3.set_treename("sig3")
sig3.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "406010")
backgrounds.append(sig3)



#### DATA
data = background.Data()
data.set_color(r.kBlack)
data.set_treename("Data")
data.set_chain_from_list_CONDOR(filelist_dir + "data/", data_rawdir)


#############################################
# Set up the regions
#############################################
regions = []

#reg = region.Region()
#reg.simplename = "wwpre"
#reg.displayname = "WW-pre (DFOS-20)"
#reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && nJets>=2"
#regions.append(reg)

reg = region.Region()
reg.name = "xrjpre"
reg.displayname = "XRJ-PRE"
isEE = "(nElectrons==2 && abs(mll-91.2)>10)"
isMM = "(nMuons==2 && abs(mll-91.2)>10)"
isSF = "((nMuons==2 || nElectrons==2) && abs(mll-91.2)>10)"
isDF = "(nElectrons==1 && nMuons==1)"
#xH_11_SS/xH_42_SS_T>0.6 &&
reg.tcut = "nLeptons==2 && " + isDF + " && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && nJets>=2 && MDR>80 && xH_11_SS/xH_42_SS_T>0.65 && gamInvRp1>0.62 && RPT>0.5 && DPB_vSS>2. && xMS>150" 


#reg.tcut = "nLeptons==2 && " + isDF + " && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && DPB_vSS>2.0 && RPT>0.6 && mt2>90"
#reg.tcut = "nLeptons==2 && ((mll>20 && (nElectrons==1 && nMuons==1)) || ((mll>20 && abs(mll-91.2)>10) && (nElectrons==2 || nMuons==2))) && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && nJets>=2 && nJets<4 && nBJets==0 && DPB_vSS>2.6 && xH_11_SS/xH_42_SS_T>0.4 && xH_42_SS_T/xH_42_SS<0.8 && RPT>0.6 && MDR>70"
#reg.tcut = "nLeptons==2 && ((mll>20 && (nElectrons==1 && nMuons==1)) || ((mll>20 && abs(mll-91.2)>10) && (nElectrons==2 || nMuons==2))) && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && nJets>=2 && nJets<4 &&  nBJets==0 && MDR>90 && RPT>0.7 && DPB_vSS>2.5 && gamInvRp1>0.65" 
#reg.tcut = "nLeptons==2 && ((mll>20 && (nElectrons==1 && nMuons==1)) || ((mll>20 && abs(mll-91.2)>10) && (nElectrons==2 || nMuons==2))) && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && nJets>=2 && nJets<4 &&  nBJets==0 && xH_11_SS/xH_42_SS_T>0.6  && xH_42_SS_T/xH_42_SS<0.5 && RPT>0.6 && DPB_vSS>2.3 && MDR>80"
#reg.tcut = "nLeptons==2 && ((mll>20 && (nElectrons==1 && nMuons==1)) || ((mll>20 && abs(mll-91.2)>10) && (nElectrons==2 || nMuons==2))) && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && nJets>=2 && nJets<4 &&  MDR>100 &&  nBJets==0 && xH_11_SS/xH_42_SS_T>0.55 && RPT>0.58 && DPB_vSS>2.3 && xH_42_SS_T/xH_42_SS<0.6"
#reg.tcut = "nLeptons==2 && ((mll>20 && (nElectrons==1 && nMuons==1)) || ((mll>20 && abs(mll-91.2)>10) && (nElectrons==2 || nMuons==2))) && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && nJets>=2 && nJets<4 && DPB_vSS>2.5 && RPT>0.7 && MDR>50 &&  nBJets==0 && xH_42_SS_T/xH_42_SS<0.6"
#reg.tcut = "nLeptons==2 && ((mll>20 && (nElectrons==1 && nMuons==1)) || ((mll>20 && abs(mll-91.2)>10) && (nElectrons==2 || nMuons==2))) && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && nJets>=2 && xDeltaBetaSS<0.5 && xDPB_vSS>2.5 && MDR>80 && xH_11_SS/xH_42_SS_T>0.7"
regions.append(reg)



#############################################
# Set up the plots
#############################################

plots = []

vars = {}
vars["nJets"] = [1, 0, 10]
vars["nBJets"] = [1, 0, 10]
#vars["bj_pt[0]"] = [5, 0, 100]
vars["j_pt[0]"] = [10, 0, 200]
#vars["bj_eta[0]"] = [0.1, -3, 3]
#vars["j_eta[0]"] = [0.1, -3, 3]
vars["xshat"] = [120, 0, 2000]
vars["xgaminv"] = [0.05, 0, 1]
vars["xRPT"] = [0.05, 0, 1]
vars["xRPZ"] = [0.4, -2, 5]
vars["xcosSS"] = [0.1, -1, 1]
vars["xdphiLSS"] = [0.2, 0, 7]
vars["xMS"] = [40, 0, 600]
vars["xPS"] = [60, 0, 1000]
vars["xMSS"] = [160, 0, 2000]
vars["xgaminvSS"] = [0.05, 0, 1]
vars["xDPD_vSS"] = [0.1, 0, 3.2]
vars["xDPB_vSS"] = [0.1, 0, 3.2]
#vars["xNV[0]"] = [1, 0, 6]
#vars["xNV[1]"] = [1, 0, 6]
vars["xcosS[0]"] = [0.1, -1, 1]
vars["xcosS[1]"] = [0.1, -1, 1]
vars["xdphiSC[0]"] = [0.2, 0, 7]
vars["xdphiSC[1]"] = [0.2, 0, 7]
#vars["xRCS[0]"] = [0.05, 0, 1]
#vars["xRCS[1]"] = [0.05, 0, 1]
vars["xjet1PT[0]"] = [20, 0, 700]
vars["xjet1PT[1]"] = [20, 0, 700]
vars["xjet2PT[0]"] = [20, 0, 700]
vars["xjet2PT[1]"] = [20, 0, 700]
#vars["xPinv[0]"] = [0.05, 0, 1]
#vars["xPinv[1]"] = [0.05, 0, 1]
vars["xH_11_SS"] = [40, 0, 1000]
vars["xH_21_SS"] = [80, 0, 2500]
vars["xH_41_SS"] = [100, 0, 2500]
vars["xH_42_SS"] = [110, 0, 2500]
vars["xH_11_S1"] = [200, 0, 5000]
vars["xH_21_S1"] = [200, 0, 5000]
vars["xH_11_SS_T"] = [40, 0, 1000]
vars["xH_21_SS_T"] = [60, 0, 1500]
vars["xH_41_SS_T"] = [80, 0, 2500]
vars["xH_42_SS_T"] = [150, 0, 3000]
vars["xH_11_S1_T"] = [200, 0, 5000]
vars["xH_21_S1_T"] = [200, 0, 5000]
vars["xH_11_S1/xH_42_SS"] = [0.5, 0, 10]
vars["xH_42_SS_T/xH_42_SS"] = [0.05, 0, 1]
vars["xH_11_SS/xH_42_SS_T"] = [0.05, 0, 2]
vars["MDR"] = [10, 0, 220]
vars["RPT"] = [0.05, 0, 1]
vars["DPB_vSS"] = [0.1, 0, 3.2]
vars["xDeltaBetaSS"] = [0.1, -1, 1]
vars["gamInvRp1"] = [0.05, 0, 1]

logy = 10000000

for var, bounds in vars.iteritems() :
    p = plot.Plot1D()
    name_ = ""
    if "(xNV[0]-xNV[1])/(xNV[0]+xNV[1])" in var :
        name_ = "n_obs_asym"
    elif "/" in var :
        name_ = var.replace("/","")
    else :
        name_ = var
    p.initialize("xrjpre", var, "xrjpre_%s"%name_)
    p.labels(x=var)
    p.xax(bounds[0], bounds[1], bounds[2])
    p.doLogY = True
    p.yax(0.1, logy)
    p.setDoubleRatioCanvas(p.name)
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
