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

lumi_val = 3.34

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
data.set_chain_from_list_CONDOR(filelist_dir + "data/", data_rawdir)


#############################################
# Set up the regions
#############################################
regions = []

isSF = "((nElectrons==2 || nMuons==2) && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0"
isDF = "(nElectrons==1 && nMuons==1) && (l_q[0]*l_q[1])<0"

reg = region.Region()
reg.simplename = "pre"
reg.displayname = "WW-like (DFOS-20)"
reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"
regions.append(reg)

reg = region.Region()
reg.simplename = "zee"
reg.displayname = "Z->ee"
reg.tcut = "nLeptons==2 && nElectrons==2 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && abs(mll-91.2)<15"
regions.append(reg)

reg = region.Region()
reg.simplename = "crw"
reg.displayname = "CRW"
reg.tcut = "nLeptons==2 && " + isDF + " && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && nJets>=2 && MDR>30 && xH_11_SS/xH_42_SS_T<0.65 && gamInvRp1>0.62 && xMS>150 && DPB_vSS<1 && RPT>0.5"
regions.append(reg)

reg = region.Region()
reg.simplename = "vrw"
reg.displayname = "VRW"
reg.tcut = "nLeptons==2 && " + isDF + " && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && nJets>=2 && MDR>30 && xH_11_SS/xH_42_SS_T<0.65 && gamInvRp1>0.62 && xMS>150 && DPB_vSS>1 && DPB_vSS<2 && RPT>0.5"
regions.append(reg)

reg = region.Region()
reg.simplename = "test"
reg.displayname = "test"
reg.tcut = "nLeptons==2 && " + isDF + " && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && nJets>=2 && MDR>30"
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


vars["xMS"] = [40, 0, 1000]
vars["xH_11_SS/xH_42_SS_T"] = [0.05, 0, 0.95]
vars["cosThetaB"] = [0.1, -1, 1]
vars["RPT"] = [0.05, 0, 1]
vars["DPB_vSS"] = [0.2, 0, 3.2]
vars["gamInvRp1"] = [0.05, 0, 1]
vars["MDR"] = [20, 0, 250]
vars["l_pt[0]"] = [10, 20, 400]
vars["l_pt[1]"] = [10, 20, 250]
vars["l_eta[0]"] = [0.5, -3, 3]
vars["l_eta[1]"] = [0.5, -3, 3]
vars["l_phi[0]"] = [0.4, -3.2, 3.2]
vars["l_phi[1]"] = [0.4, -3.2, 3.2]
vars["j_pt[0]"] = [40, 20, 800]
vars["j_pt[1]"] = [40, 20, 600]
vars["j_eta[0]"] = [0.5, -3, 3]
vars["j_eta[1]"] = [0.5, -3, 3]
vars["j_phi[0]"] = [0.4, -3.2, 3.2]
vars["j_phi[1]"] = [0.4, -3.2, 3.2]
vars["nJets"] = [1, 0, 16]
vars["nBJets"] = [1, 0, 8]
vars["met"] = [40, 0, 650]
vars["mll"] = [50, 20, 1000]

map = {}
map["DPB_vSS"] = "#Delta#phi_{#beta}^{R}"
map["cosThetaB"] = "cos#theta_{b}"
map["xH_11_SS/xH_42_SS_T"] = "H_{11}^{SS}/H_{42,T}^{SS}"
map["RPT"] = "R_{pT}"
map["gamInvRp1"] = "1/#gamma_{R+1}"
map["MDR"] = "M_{#Delta}^{R} [GeV]"
map["l_pt[0]"] = "Lead lepton p_{T} [GeV]"
map["l_pt[1]"] = "Sub-lead lepton p_{T} [GeV]"
map["l_eta[0]"] = "Lead lepton #eta"
map["l_eta[1]"] = "Sub-lead lepton #eta"
map["l_phi[0]"] = "Lead lepton #phi [rad]"
map["l_phi[1]"] = "Sub-lead lepton #phi [rad]"
map[ "j_pt[0]"] = "Lead jet p_{T} [GeV]"
map["j_eta[0]"] = "Lead jet #eta"
map["j_phi[0]"] = "Lead jet #phi [rad]"
map[ "j_pt[1]"] = "Sub-lead jet p_{T} [GeV]"
map["j_eta[1]"] = "Sub-lead jet #eta"
map["j_phi[1]"] = "Sub-lead jet #phi [rad]"
map["nJets"] = "Jet multiplicity"
map["nBJets"] = "b-Jet multiplicity"
map["met"] = "#slash{E}_{T}-TST"
map["xMS"] = "M_{S} [GeV]"
map["mll"] = "Dilepton invariant mass [GeV]"


logy = 10000000
for var, bounds in vars.iteritems() :
    p = plot.Plot1D()
    name_ = ""
    if "/" in var :
        name_ = var.replace("/","")
    else :
        name_ = var
    p.initialize("test", var, "test_%s"%name_)
    unit_ = ""
    if "MDR" in var or "xMS" in var or "mll" in var or "pt" in var:
        unit_ = "GeV"
    p.labels(x=map[var], y="Entries / %s %s"%(str(bounds[0]), unit_))
    p.xax(bounds[0], bounds[1], bounds[2])
    p.doLogY = True
    p.yax(0.1, logy)
    p.setRatioCanvas(p.name)
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
