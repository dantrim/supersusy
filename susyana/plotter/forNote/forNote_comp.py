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
rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0224/jun1/mc/Raw/"
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0222/nom/data/Raw/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0224val/filelists/"
backgrounds = []

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

## zjets
zjets = background.Background("zjets", "Zjets")
zjets.scale_factor = 1.0
zjets.set_color(r.kBlack)
zjets.set_treename("zjets")
zjets.set_chain_from_list_CONDOR(filelist_dir + "zjets_sherpa22/", rawdir)
backgrounds.append(zjets)

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

isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"
isSFOS = "nLeptons==2 && (nElectrons==2 || nMuons==2) && abs(mll-91.2)>10 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"
isMMOS = "nLeptons==2 && nMuons==2 && abs(mll-91.2)>10 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"
isEEOS = "nLeptons==2 && nElectrons==2 && abs(mll-91.2)>10 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"



reg = region.Region()
reg.name = "dfpre"
reg.displayname = "Preselection"
reg.tcut = isEEOS + " && MDR>95 && RPT>0.5 && nBJets==0 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8)"
#reg.tcut = "1"
regions.append(reg)

reg = region.Region()
reg.name = "wwbveto"
reg.displayname = "Preselection"
reg.tcut = isDFOS + " && nBJets==0"
regions.append(reg)

#reg = region.Region()
#reg.name = "wwb"
#reg.displayname = "WW-pre (DFOS-20) - > 0 b"
#reg.tcut = isDFOS + " && nBJets>0 && DPB_vSS>(1.1*abs(cosThetaB) + 1.8)"
#regions.append(reg)


#############################################
# Set up the plots
#############################################

plots = []

reg_name = "dfpre"

vars_ = {}
vars_["pupw"] = [0.5,0, 30]
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

for v_ in vars_.keys() :
    p = plot.Plot1D()
    p.setComparison()
    name = ""
    if "abs(" in v_ :
        name = v_.replace("abs(", "")
        name = name.replace(")","")
    else :
        name = v_

    if "DPB_vSS" in v_ or "cosThetaB" == v_:
        p.leg_is_bottom_right = True
    p.initialize(reg_name, v_, "%s_%s"%(reg_name, name))
    p.labels(x=nice_names[v_], y = "Arb. Units")
    p.xax(vars_[v_][0], vars_[v_][1], vars_[v_][2])
    p.doLogY = True
    p.yax(0.1, 100)
    p.setDefaultCanvas(p.name)
    plots.append(p)

