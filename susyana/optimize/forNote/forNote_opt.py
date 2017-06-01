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
#rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0224/jun1/mc/Raw/"
rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/a_jan16/mc/Raw/"
signal_4body_dir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/b_jan18/mc/Raw/"
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/a_jan16/dataToRun/Raw/"
data15_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/a_jan16/data15/Raw/"
data16_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/a_jan16/data16/Raw/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0231val/filelists/"
backgrounds = []

#### MC
lumi_ = {}
lumi_[36] = 36

lumi_val = 36

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
#diboson.set_chain_from_list_CONDOR(filelist_dir+ "diboson_sherpa/", rawdir)
diboson.set_chain_from_list_CONDOR(filelist_dir+ "diboson_sherpa_lvlv/", rawdir)
backgrounds.append(diboson)


## Zjets
#zjets = background.Background("zjets", "Z+jets (Sherpa)")
#zjets.set_debug()
#zjets.scale_factor = lumi_[lumi_val]
#zjets.set_fillStyle(0)
#zjets.setLineStyle(1)
#zjets.set_color(r.TColor.GetColor("#FFEF53"))
#zjets.set_treename("zjets_sherpa")
#zjets.set_chain_from_list_CONDOR(filelist_dir+ "zjets_sherpa22/", rawdir)
#backgrounds.append(zjets)

## Wjets
#wjets = background.Background("wjets", "W+Jets (Sherpa)")
#wjets.set_debug()
#wjets.scale_factor = lumi_[lumi_val]
#wjets.set_fillStyle(0)
#wjets.setLineStyle(1)
#wjets.set_color(r.TColor.GetColor("#5E9AD6"))
#wjets.set_treename("wjets")
#wjets.set_chain_from_list_CONDOR(filelist_dir+ "wjets_sherpa22/", rawdir)
#backgrounds.append(wjets)

"""
#sig1 = background.Background("bwn250_160", "(250,160)")
sig1 = background.Background("bwn350_200", "(350,200)")
sig1.setSignal()
sig1.set_debug()
sig1.scale_factor = lumi_[lumi_val]
sig1.set_fillStyle(0)
sig1.setLineStyle(2)
sig1.set_color(r.kBlue)
sig1.set_treename("sig1")
#sig1.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "389945")
sig1.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "387953")
backgrounds.append(sig1)

#sig2 = background.Background("bwn300_210", "(300,210)")
sig2 = background.Background("bwn300_150", "(300,150)")
sig2.setSignal()
sig2.set_debug()
sig2.scale_factor = lumi_[lumi_val]
sig2.setLineStyle(2)
sig2.set_color(r.kGreen)
sig2.set_treename("sig2")
#sig2.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", rawdir, "389951")
sig2.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", rawdir, "387947")
backgrounds.append(sig2)

#sig3 = background.Background("bwn350_260", "(350,260)")
sig3 = background.Background("bwn325_150", "(325,150)")
sig3.setSignal()
sig3.set_debug()
sig3.scale_factor = lumi_[lumi_val]
sig3.setLineStyle(2)
sig3.set_color(r.kBlack)
sig3.set_treename("sig3")
#sig3.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "389957")
sig3.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "387950")
backgrounds.append(sig3)
"""

#s30 = background.Background("s30", "(275,185)")
#s30.setSignal()
#s30.scale_factor = lumi_[lumi_val]
#s30.setLineStyle(2)
#s30.set_color(r.kRed)
#s30.set_treename("s30")
#s30.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "389948")
#backgrounds.append(s30)
#
#s31 = background.Background("s31", "(325,235)")
#s31.setSignal()
#s31.scale_factor = lumi_[lumi_val]
#s31.setLineStyle(2)
#s31.set_color(r.kGreen)
#s31.set_treename("s31")
#s31.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "389954")
#backgrounds.append(s31)
#
#s32 = background.Background("s32", "(375,285)")
#s32.setSignal()
#s32.scale_factor = lumi_[lumi_val]
#s32.setLineStyle(2)
#s32.set_color(r.kBlack)
#s32.set_treename("s32")
#s32.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "389960")
#backgrounds.append(s32)

s40 = background.Background("s40", "(275,195)")
s40.setSignal()
s40.scale_factor = lumi_[lumi_val]
s40.setLineStyle(2)
s40.set_color(r.kRed)
s40.set_treename("s40")
s40.set_chain_from_list_CONDOR(filelist_dir + "bffN/",signal_4body_dir, "389984")
backgrounds.append(s40)

s41 = background.Background("s41", "(325,245)")
s41.setSignal()
s41.scale_factor = lumi_[lumi_val]
s41.setLineStyle(2)
s41.set_color(r.kGreen)
s41.set_treename("s41")
s41.set_chain_from_list_CONDOR(filelist_dir + "bffN/", signal_4body_dir, "389990")
backgrounds.append(s41)

s42 = background.Background("s42", "(375,295)")
s42.setSignal()
s42.scale_factor = lumi_[lumi_val]
s42.setLineStyle(2)
s42.set_color(r.kBlack)
s42.set_treename("s42")
s42.set_chain_from_list_CONDOR(filelist_dir + "bffN/", signal_4body_dir, "389996")
backgrounds.append(s42)





#### DATA
data = background.Data()
data.set_color(r.kBlack)
data.set_treename("Data")
data.set_chain_from_list_CONDOR(filelist_dir + "dataToRun/", data_rawdir)


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
isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"

reg = region.Region()
reg.name = "ww"
reg.displayname = "WW-like"
#reg.tcut = isDFOS + " && MDR>110 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8)"
#reg.tcut = isDFOS + " && MDR>95 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8)"
#reg.tcut = isDFOS + " && MDR>110 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8)"
reg.tcut = isDFOS + " && MDR>95 && nBJets==0"
#reg.tcut = isDFOS + " && nBJets==0 && trig_pass2016==1 && MDR>95" 
regions.append(reg)

reg = region.Region()
reg.name = "wwMT"
reg.displayname = "WW-like (mT)"
#reg.tcut = isDFOS + " && MDR>110 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8)"
#reg.tcut = isDFOS + " && MDR>95 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8)"
#reg.tcut = isDFOS + " && MDR>110 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8)"
reg.tcut = isDFOS + " && MDR>110 && nBJets>0"
#reg.tcut = isDFOS + " && nBJets==0 && trig_pass2016==1 && MDR>95" 
regions.append(reg)

reg = region.Region()
reg.name = "wwPlotNMMDR"
reg.displayname = "SRw-DF (N-1 MDR)"
reg.tcut = isDFOS + " && nBJets==0 && RPT>0.7 && gamInvRp1>0.7 && DPB_vSS>(0.9*abs(cosThetaB) + 1.6) + mll>20"
regions.append(reg)

reg = region.Region()
reg.name = "wwPlotMTNMMDR"
reg.displayname = "SRt-DF (N-1 MDR)"
reg.tcut = isDFOS + " && nBJets>0 && RPT>0.7 && gamInvRp1>0.7 && DPB_vSS>(0.9*abs(cosThetaB) + 1.6) + mll>20"
regions.append(reg)



#############################################
# Set up the plots
#############################################

plots = []
reg_ = "wwPlotNMMDR"

vars = {}

vars["MDR"] = [5, 0, 150]
#vars["RPT"] = [0.1, 0, 1]
#vars["abs(cosThetaB)"] = [0.05, 0, 1]
#vars["gamInvRp1"] = [0.1, 0, 1]
##vars["DPB_vSS"] = [0.1, 0, 3.2]
##vars["l_pt[0]"] = [5, 0, 200]
##vars["l_pt[1]"] = [5, 0, 200]
#vars["nBJets"] = [1, 0, 5]
#vars["mt2"] = [5, 0, 150]

nice_names = {}
nice_names["RPT"] = "R_{p_{T}}"
nice_names["MDR"] = "E_{V}^{P} [GeV]"
nice_names["gamInvRp1"] = "1/#gamma_{P}^{PP}"
nice_names["abs(cosThetaB)"] = "|#cos#theta_{b}| [rad]"
nice_names["DPB_vSS"] = "#Delta#phi(#vec{#beta}_{PP}^{LAB}, #vec{p}_{V}^{PP})"
nice_names["nBJets"] = "b-Jet Multiplicity"

logy = 10000000

for var, bounds in vars.iteritems() :
    p = plot.Plot1D()
    name_ = ""
    if "/" in var :
        name_ = var.replace("/","")
    elif "abs(" in var :
        name_ = var.replace("abs(","")
        name_ = name_.replace(")","")
    else :
        name_ = var
    p.initialize(reg_, var, "%s_%s"%(reg_,name_))
    p.labels(x=nice_names[var])
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
