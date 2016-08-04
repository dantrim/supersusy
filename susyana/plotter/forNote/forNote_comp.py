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
backgrounds = []
rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0226/jul25/mc/Raw/"
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0226/jul25/data/Raw/"
fake_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0226/forFake3/fakes.3body/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0226val/filelists/"

#### MC

### ttbar
ttbar = background.Background("ttbar", "t#bar{t}")
ttbar.scale_factor = 1
ttbar.set_color(r.TColor.GetColor("#FC0D1B"))
ttbar.set_treename("ttbar")
ttbar.set_chain_from_list_CONDOR(filelist_dir+ "ttbar/", rawdir)
backgrounds.append(ttbar)

### ww
ww = background.Background("vv", "VV")
ww.scale_factor = 1.0
ww.set_color(r.TColor.GetColor("#41C1FC"))
ww.set_treename("vv")
ww.set_chain_from_list_CONDOR(filelist_dir+ "diboson_sherpa_lvlv/", rawdir)
backgrounds.append(ww)

### zjets
#zjets = background.Background("zjets", "Zjets")
#zjets.scale_factor = 1.0
#zjets.set_color(r.kBlack)
#zjets.set_treename("zjets")
#zjets.set_chain_from_list_CONDOR(filelist_dir + "zjets_sherpa22/", rawdir)
#backgrounds.append(zjets)

sig1 = background.Background("bwn250_160", "(250,160)")
sig1.setSignal()
sig1.set_debug()
sig1.scale_factor = 1.0
sig1.set_fillStyle(0)
sig1.setLineStyle(2)
sig1.set_color(r.kBlue)
sig1.set_treename("sig1")
sig1.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", rawdir, "387943")
backgrounds.append(sig1)

sig2 = background.Background("bwn300_180", "(300,180)")
sig2.setSignal()
sig2.set_debug()
sig2.scale_factor = 1.0
sig2.setLineStyle(2)
sig2.set_color(r.kGreen)
sig2.set_treename("sig2")
sig2.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", rawdir, "387948")
backgrounds.append(sig2)

sig3 = background.Background("bwn300_150", "(300,150)")
sig3.setSignal()
sig3.set_debug()
sig3.scale_factor = 1.0
sig3.setLineStyle(2)
sig3.set_color(r.kBlack)
sig3.set_treename("sig3")
sig3.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "387947")
backgrounds.append(sig3)
### bwn -- (250, 160)
#bwn0 = background.Background("bwn250_160", "(250,160)")
#bwn0.setSignal()
#bwn0.scale_factor = 1.0
#bwn0.set_fillStyle(0)
#bwn0.setLineStyle(2)
#bwn0.set_color(r.kBlue)
#bwn0.set_treename("sig1")
#bwn0.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "387943")
##bwn0.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "406009")
#backgrounds.append(bwn0)
#
#### bwn -- (300, 150)
#bwn1 = background.Background("bwn300_150", "(350,150)")
#bwn1.setSignal()
#bwn1.scale_factor = 1.0
#bwn1.set_fillStyle(0)
#bwn1.setLineStyle(2)
#bwn1.set_color(r.kGreen)
#bwn1.set_treename("sig2")
#bwn1.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "387947")
##bwn1.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "406010")
#backgrounds.append(bwn1)
#
#### bwn -- (300, 180)
#bwn2 = background.Background("bwn300_180", "(300,180)")
#bwn2.setSignal()
#bwn2.scale_factor = 1.0
#bwn2.set_fillStyle(0)
#bwn2.setLineStyle(2)
#bwn2.set_color(r.kRed)
#bwn2.set_treename("sig3")
#bwn2.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "387948")
##bwn2.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "406011")
#backgrounds.append(bwn2)


##### DATA
#data = background.Data()
#data.set_color(r.kBlack)
#data.set_treename("Data")
#data.set_chain_from_list_CONDOR(filelist_dir + "data/", data_rawdir)


#############################################
# Set up the regions
#############################################
regions = []

isEE = "(nElectrons==2 && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"
isMM = "(nMuons==2 && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"


isSFOS = "(( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && abs(mll-91.2)>10 && (l_q[0]*l_q[1])<0)"
isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<0"
isSFcheck = "((nMuons==2 || nElectrons==2)) && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"

trigger = "((year==2015 && trig_pass2015==1) || (year==2016 && trig_pass2016update==1))"


reg = region.Region()
reg.name = "dfprebv"
reg.displayname = "DF Preselection + b-veto"
reg.tcut = "nLeptons==2 && " + isDFOS + " && nBJets==0 && mll>20 && " + trigger 
regions.append(reg)

reg = region.Region()
reg.name = "sfprebv"
reg.displayname = "DF Preselection + b-veto"
reg.tcut = "nLeptons==2 && " + isSFOS + " && nBJets==0 && mll>20 && " + trigger 
regions.append(reg)

reg = region.Region()
reg.name = "sfprebvEE"
reg.displayname = "SF Preselection + b-veto (ee)"
reg.tcut = "nLeptons==2 && " + isEE + " && nBJets==0 && mll>20 && " + trigger 
regions.append(reg)

reg = region.Region()
reg.name = "sfprebvMM"
reg.displayname = "SF Preselection + b-veto (#mu#mu)"
reg.tcut = "nLeptons==2 && " + isMM + " && nBJets==0 && mll>20 && " + trigger 
regions.append(reg)

reg = region.Region()
reg.name = "dfpreb"
reg.displayname = "DF Preselection + >0 b-jets"
reg.tcut = "nLeptons==2 && " + isDFOS + " && nBJets>0 && mll>20 && " + trigger 
regions.append(reg)

reg = region.Region()
reg.name = "sfpreb"
reg.displayname = "SF Preselection + >0 b-jets"
reg.tcut = "nLeptons==2 && " + isSFOS + " && nBJets>0 && mll>20 && " + trigger 
regions.append(reg)

reg = region.Region()
reg.name = "sfprebEE"
reg.displayname = "SF Preselection + >0 b-jets (ee)"
reg.tcut = "nLeptons==2 && " + isEE + " && nBJets>0 && mll>20 && " + trigger 
regions.append(reg)

reg = region.Region()
reg.name = "sfprebMM"
reg.displayname = "SF Preselection + >0 b-jets (#mu#mu)"
reg.tcut = "nLeptons==2 && " + isMM + " && nBJets>0 && mll>20 && " + trigger 
regions.append(reg)



#####isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"
#####isSFOS = "nLeptons==2 && (nElectrons==2 || nMuons==2) && abs(mll-91.2)>10 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"
#####isMMOS = "nLeptons==2 && nMuons==2 && abs(mll-91.2)>10 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"
#####isEEOS = "nLeptons==2 && nElectrons==2 && abs(mll-91.2)>10 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"
#####
#####reg = region.Region()
#####reg.name = "dfpre"
#####reg.displayname = "Preselection"
#####reg.tcut = isEEOS + " && MDR>95 && RPT>0.5 && nBJets==0 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8)"
######reg.tcut = "1"
#####regions.append(reg)
#####
#####reg = region.Region()
#####reg.name = "wwbveto"
#####reg.displayname = "Preselection"
#####reg.tcut = isDFOS + " && nBJets==0"
#####regions.append(reg)
#####
######reg = region.Region()
######reg.name = "wwb"
######reg.displayname = "WW-pre (DFOS-20) - > 0 b"
######reg.tcut = isDFOS + " && nBJets>0 && DPB_vSS>(1.1*abs(cosThetaB) + 1.8)"
######regions.append(reg)


#############################################
# Set up the plots
#############################################

plots = []

reg_name = "sfprebv"

vars_ = {}
vars_["DPB_vSS - 0.85*abs(cosThetaB)"] = [0.5, -1.4, 4, 1e9]
#vars_["pupw"] = [0.5,0, 30]
#vars_["nJets"] = [1, 0, 10]
#vars_["nSJets"] = [1, 0, 10]
#vars_["nBJets"] = [1, 0, 6]

#vars_["MDR"] = [8, 0, 200]
#vars_["RPT"] = [0.05, 0, 1]
#vars_["gamInvRp1"] = [0.05, 0, 1]
#vars_["cosThetaB"] = [0.2, -1, 1]
#vars_["cosThetaB"] = [0.1, -1, 1]
#vars_["DPB_vSS"] = [0.1, 0, 3.2]
#vars_["l_pt[0]"] = [5, 0, 120]
#vars_["l_pt[1]"] = [5, 0, 120]

nice_names = {}
nice_names["pupw"] = "Pileup Weight"
nice_names["nBJets"] = "b-Jet Multiplicity"
nice_names["abs(cosThetaB)"] = "|cos#theta_{b}|"
nice_names["cosThetaB"] = "cos#theta_{b}"
nice_names["MDR"] = "E_{V}^{P} [GeV]"
nice_names["RPT"] = "R_{p_{T}}"
nice_names["DPB_vSS"] = "#Delta#phi(#vec{#beta}_{PP}^{LAB}, #vec{p}_{V}^{PP})"
nice_names["gamInvRp1"] = "1/#gamma_{P}^{PP}"
nice_names["DPB_vSS - 0.85*abs(cosThetaB)"] = "#Delta#phi_{#beta}^{R} - 0.85#times|cos#theta_{b}|"

for v_ in vars_.keys() :
    p = plot.Plot1D()
    p.setComparison()
    name = ""
    if "abs(" in v_  and "DPB_vSS" not in v_:
        name = v_.replace("abs(", "")
        name = name.replace(")","")
    elif v_ =="DPB_vSS - 0.85*abs(cosThetaB)" :
        name_ = "DPB_minus_COSB" 
    else :
        name = v_

    #if "DPB_vSS" in v_ or "cosThetaB" == v_ and v_!="DPB_vSS - 0.85*abs(cosThetaB)":
    #    p.leg_is_bottom_right = True
    p.initialize(reg_name, v_, "%s_%s"%(reg_name, name))
    p.labels(x=nice_names[v_], y = "Arb. Units")
    p.xax(vars_[v_][0], vars_[v_][1], vars_[v_][2])
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

