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
filelist_dir = "/data/uclhc/uci/user/dantrim/n0232val/filelists/"
rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0232/f_jun5/mc/Raw/"
data15_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/a_jan16/data15/Raw/"
data16_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/a_jan16/data16/Raw/"
backgrounds = []

#### MC
lumi_ = {}
lumi_[100] = 100

lumi_val = 100

# ttbro
ttbar = background.Background("ttbar", "t#bar{t}")
ttbar.set_debug()
ttbar.scale_factor = lumi_[lumi_val]
ttbar.set_fillStyle(0)
ttbar.setLineStyle(1)
ttbar.set_color(r.TColor.GetColor("#e4706a"))
ttbar.set_treename("ttbar_powheg")
ttbar.set_chain_from_list_CONDOR(filelist_dir+ "ttbar/", rawdir)
backgrounds.append(ttbar)

# singletop
stop = background.Background("st", "Single top")
stop.set_debug()
stop.scale_factor = lumi_[lumi_val]
stop.set_fillStyle(0)
stop.setLineStyle(1)
stop.set_color(r.TColor.GetColor("#db101c"))
stop.set_treename("ST")
stop.set_chain_from_list_CONDOR(filelist_dir+ "singletop/", rawdir)
backgrounds.append(stop)

# ttV
ttv = background.Background("ttV", "t#bar{t}+V")
ttv.set_debug()
ttv.scale_factor = lumi_[lumi_val]
ttv.set_fillStyle(0)
ttv.setLineStyle(1)
ttv.set_color(r.TColor.GetColor("#9bcdfd"))
ttv.set_treename("TTV")
ttv.set_chain_from_list_CONDOR(filelist_dir+ "ttV/", rawdir)
backgrounds.append(ttv)


# diboson
diboson = background.Background("vv", "VV")
diboson.set_debug()
diboson.scale_factor = lumi_[lumi_val]
diboson.set_fillStyle(0)
diboson.setLineStyle(1)
diboson.set_color(r.TColor.GetColor("#325f85"))
diboson.set_treename("diboson_sherpa")
#diboson.set_chain_from_list_CONDOR(filelist_dir+ "diboson_sherpa/", rawdir)
diboson.set_chain_from_list_CONDOR(filelist_dir+ "diboson_sherpa/", rawdir)
backgrounds.append(diboson)

## Zjets
zjets = background.Background("zjets", "Z+jets")
zjets.set_debug()
zjets.scale_factor = lumi_[lumi_val]
zjets.set_fillStyle(0)
zjets.setLineStyle(1)
zjets.set_color(r.TColor.GetColor("#85dc6e"))
zjets.set_treename("zjets_sherpa")
zjets.set_chain_from_list_CONDOR(filelist_dir+ "zjets_sherpa/", rawdir)
backgrounds.append(zjets)

drel = background.Background("drellyan", "Drell-Yan")
drel.set_debug()
drel.scale_factor = lumi_[lumi_val]
drel.set_fillStyle(0)
drel.setLineStyle(1)
#drel.set_color(r.kYellow)
drel.set_color(r.TColor.GetColor("#feec60"))
drel.set_treename("drellyan")
drel.set_chain_from_list_CONDOR(filelist_dir+ "drellyan_sherpa/", rawdir)
backgrounds.append(drel)

## Wjets
wjets = background.Background("wjets", "W+Jets")
wjets.set_debug()
wjets.scale_factor = lumi_[lumi_val]
wjets.set_fillStyle(0)
wjets.setLineStyle(1)
wjets.set_color(r.TColor.GetColor("#619bd3"))
wjets.set_treename("wjets")
wjets.set_chain_from_list_CONDOR(filelist_dir+ "wjets_sherpa/", rawdir)
backgrounds.append(wjets)

#signals

sig1 = background.Background("xhh400", "X 400")
sig1.setSignal()
sig1.set_debug()
sig1.scale_factor = lumi_[lumi_val]
sig1.set_fillStyle(0)
sig1.setLineStyle(2)
sig1.set_color(r.kBlue)
sig1.set_treename("sig1")
sig1.set_chain_from_list_CONDOR(filelist_dir + "wwbb_susy2/", rawdir, "343769")
backgrounds.append(sig1)

sig3 = background.Background("xhh800", "X 800")
sig3.setSignal()
sig3.set_debug()
sig3.scale_factor = lumi_[lumi_val]
sig3.set_fillStyle(0)
sig3.setLineStyle(2)
sig3.set_color(r.kGreen)
sig3.set_treename("sig3")
sig3.set_chain_from_list_CONDOR(filelist_dir + "wwbb_susy2/", rawdir, "343775")
backgrounds.append(sig3)

sig4 = background.Background("xhh1000", "X 1000")
sig4.setSignal()
sig4.set_debug()
sig4.scale_factor = lumi_[lumi_val]
sig4.set_fillStyle(0)
sig4.setLineStyle(2)
sig4.set_color(r.kMagenta)
sig4.set_treename("sig4")
sig4.set_chain_from_list_CONDOR(filelist_dir + "wwbb_susy2/", rawdir, "343777")
backgrounds.append(sig4)

sig5 = background.Background("hh", "hh")
sig5.setSignal()
sig5.set_debug()
sig5.scale_factor = lumi_[lumi_val]
sig5.set_fillStyle(0)
sig5.setLineStyle(2)
sig5.set_color(r.kBlack)
sig5.set_treename("sig5")
sig5.set_chain_from_list_CONDOR(filelist_dir + "wwbb_susy2/", rawdir, "342053")
backgrounds.append(sig5)



#### DATA
#data = background.Data()
#data.set_color(r.kBlack)
#data.set_treename("Data")
#data.set_chain_from_list_CONDOR(filelist_dir + "dataToRun/", data_rawdir)


#############################################
# Set up the regions
#############################################
regions = []

#reg = region.Region()
#reg.simplename = "wwpre"
#reg.displayname = "WW-pre (DFOS-20)"
#reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && nJets>=2"
#regions.append(reg)


isEE = "(nElectrons==2 && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"
isMM = "(nMuons==2 && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"

isSFOS = "(( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && abs(mll-91.2)>10 && (l_q[0]*l_q[1])<0)"
isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<0"
trigger = "((year==2015 && trig_pass2015==1) || (year==2016 && trig_pass2016update==1))"

reg = region.Region()
reg.name = "ww"
reg.displayname = "WW-like"
reg.tcut = isDFOS + " && MDR>95 && nBJets==0"
regions.append(reg)

reg = region.Region()
reg.name = "wwbb"
reg.displayname = "WWbb"
presel = " ( (%s) || (%s) ) && %s && nBJets>=2 && mll>20"%(isSFOS, isDFOS, trigger)
cut = presel
cut += " && dRll<1.2"
cut += " && met_pTll>250"
cut += " && mll<100"
cut += " && mt2_llbb>75 && mt2_llbb<150"
cut += " && HT2Ratio>0.75"
cut += " && mbb>80 && mbb<150"
cut += " && dR_ll_bb>2.2"
cut += " && dRbb<1.25"
#reg.tcut = presel + " && dRll<1.5 && met_pTll>120 && mll<100 && mt2_llbb>75 && mt2_llbb<150 && HT2Ratio>0.75 && mbb>80 && mbb<150 && dR_ll_bb>2.2"

reg.tcut = cut
regions.append(reg)




#############################################
# Set up the plots
#############################################

plots = []
reg_ = "wwbb"

vars = {}
vars["abs(dphi_ll)"] = [0.1, 0, 3.2]
vars["dRll"] = [0.2, 0, 6]
vars["met_pTll"] = [20, 0, 600]
vars["mll"] = [20, 0, 600]
vars["mt2"] = [10, 0, 300]
vars["meff"] = [40, 0, 1500]
vars["mt2_llbb"] = [10, 0, 500]
vars["HT2Ratio"] = [0.05, 0, 1]
vars["dRbb"] = [0.1, 0, 5]
vars["pTll"] = [20, 0, 500]
vars["mbb"] = [10, 0, 500]
vars["mass_X_scaled"] = [20, 0, 1200]
vars["MT_1_scaled"] = [30, 0, 1500]
vars["dR_ll_bb"] = [0.1, 0, 5]
vars["abs(dphi_met_ll)"] = [0.1, 0, 3.2]
vars["mt2_bvis"] = [20, 0, 500]
vars["mt2_lvis"] = [20, 0, 500]
vars["mt2_bb"] = [10, 0, 300]
vars["dR_ll_bb"] = [0.1, 0, 5]
vars["abs(dphi_ll_bb)"] = [0.1, 0, 3.2]
vars["abs(dphi_WW_bb)"] = [0.1, 0, 3.2]
vars["mass_met_ll"] = [20, 0, 1200]
vars["MT_HWW"] = [20, 0, 800]
vars["abs(cosThetaB)"] = [0.05, 0, 1]
vars["mT_llmet"] = [10, 0, 1000]
vars["mT_bb"] = [10, 0, 1000]

nice_names = {}
nice_names["RPT"] = "R_{p_{T}}"
nice_names["MDR"] = "E_{V}^{P} [GeV]"
nice_names["gamInvRp1"] = "1/#gamma_{P}^{PP}"
nice_names["abs(cosThetaB)"] = "|#cos#theta_{b}| [rad]"
nice_names["DPB_vSS"] = "#Delta#phi(#vec{#beta}_{PP}^{LAB}, #vec{p}_{V}^{PP})"
nice_names["nBJets"] = "b-Jet Multiplicity"
nice_names["dRll"] = "#Delta R_{ll}"

for v in vars.keys() :
    nice_names[v] = v

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
    name_ = name_.replace("[","").replace("]","")
    p.initialize(reg_, var, "%s_%s"%(reg_,name_))
    p.labels(x=nice_names[var])
    p.xax(bounds[0], bounds[1], bounds[2])
    p.doLogY = True
    p.yax(0.1, logy)
    p.setDoubleRatioCanvas(p.name)
    plots.append(p)


