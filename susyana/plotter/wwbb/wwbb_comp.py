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
#rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0226/jul25/mc/Raw/"
#data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0226/jul25/data/Raw/"
#fake_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0226/forFake3/fakes.3body/"

rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0232/c_apr27/mc/Raw/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0232val/filelists/"

#### MC

### ttbar
ttbar = background.Background("ttbar", "t#bar{t}")
ttbar.scale_factor = 36
ttbar.set_color(r.TColor.GetColor("#FC0D1B"))
ttbar.set_treename("ttbar")
ttbar.set_chain_from_list_CONDOR(filelist_dir+ "ttbar/", rawdir)
backgrounds.append(ttbar)

### ww
ww = background.Background("vv", "VV")
ww.scale_factor = 36
ww.set_color(r.TColor.GetColor("#41C1FC"))
ww.set_treename("vv")
ww.set_chain_from_list_CONDOR(filelist_dir+ "diboson_sherpa/", rawdir)
backgrounds.append(ww)

### zjets
#zjets = background.Background("zjets", "Zjets")
#zjets.scale_factor = 1.0
#zjets.set_color(r.kBlack)
#zjets.set_treename("zjets")
#zjets.set_chain_from_list_CONDOR(filelist_dir + "zjets_sherpa22/", rawdir)
#backgrounds.append(zjets)

sig1 = background.Background("xhh400", "400")
sig1.setSignal()
sig1.set_debug()
sig1.scale_factor = 36
sig1.set_fillStyle(0)
sig1.setLineStyle(2)
sig1.set_color(r.kBlue)
sig1.set_treename("sig1")
sig1.set_chain_from_list_CONDOR(filelist_dir + "wwbb_susynt/", rawdir, "343769")
backgrounds.append(sig1)

sig2 = background.Background("xhh600", "600")
sig2.setSignal()
sig2.set_debug()
sig2.scale_factor = 36
sig2.set_fillStyle(0)
sig2.setLineStyle(2)
sig2.set_color(r.kRed)
sig2.set_treename("sig2")
sig2.set_chain_from_list_CONDOR(filelist_dir + "wwbb_susynt/", rawdir, "343772")
backgrounds.append(sig2)

sig3 = background.Background("xhh800", "800")
sig3.setSignal()
sig3.set_debug()
sig3.scale_factor = 36
sig3.set_fillStyle(0)
sig3.setLineStyle(2)
sig3.set_color(r.kGreen)
sig3.set_treename("sig3")
sig3.set_chain_from_list_CONDOR(filelist_dir + "wwbb_susynt/", rawdir, "343775")
backgrounds.append(sig3)

sig4 = background.Background("xhh1000", "1000")
sig4.setSignal()
sig4.set_debug()
sig4.scale_factor = 36
sig4.set_fillStyle(0)
sig4.setLineStyle(2)
sig4.set_color(r.kMagenta)
sig4.set_treename("sig4")
sig4.set_chain_from_list_CONDOR(filelist_dir + "wwbb_susynt/", rawdir, "343777")
backgrounds.append(sig4)

sig5 = background.Background("hh", "hh")
sig5.setSignal()
sig5.set_debug()
sig5.scale_factor = 36
sig5.set_fillStyle(0)
sig5.setLineStyle(2)
sig5.set_color(r.kBlack)
sig5.set_treename("sig5")
sig5.set_chain_from_list_CONDOR(filelist_dir + "wwbb_susynt/", rawdir, "342053")
backgrounds.append(sig5)



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
reg.name = "wwbbpre"
reg.displayname = "WWBB (n bjets == 2)"
reg.tcut = "nLeptons ==2 && nBJets==2 && mll>20 && l_pt[0]>25 && l_pt[1]>20 && abs(dphi_bb)<1.5 && HT2Ratio>0.8 && abs(dphi_ll)<1.5 && " + trigger
regions.append(reg)


#############################################
# Set up the plots
#############################################

plots = []

reg_name = "wwbbpre"

vars_ = {}
vars_["l_pt[0]"] = [5, 0, 300]
vars_["l_pt[1]"] = [5, 0, 300]
vars_["l_eta[0]"] = [0.2, -3, 3]
vars_["l_eta[1]"] = [0.2, -3, 3]
vars_["abs(dphi_ll)"] = [0.1, 0, 3.2]
vars_["pTll"] = [20, 0, 600]
vars_["dRll"] = [0.2, 0, 6]
vars_["abs(cosThetaB)"] = [0.05, 0, 1]
vars_["abs(cosTheta1)"] = [0.05, 0, 1]
vars_["abs(cosTheta2)"] = [0.05, 0, 1]
vars_["abs(dphi_boost_ll)"] = [0.1, 0, 3.2]
vars_["nJets"] = [1, 0, 12]
vars_["nSJets"] = [1, 0, 12]
vars_["nBJets"] = [1, 0, 12]
for i in xrange(3) :
    name = "j_pt[%d]"%i
    vars_[name] = [10,0,500]
    name = "j_eta[%d]"%i
    vars_[name] = [0.5, -5,5]

    name = "sj_pt[%d]"%i
    vars_[name] = [10,0,500]
    name = "sj_eta[%d]"%i
    vars_[name] = [0.5, -5,5]

    name = "bj_pt[%d]"%i
    vars_[name] = [20,0,800]
    name = "bj_eta[%d]"%i
    vars_[name] = [0.5, -5,5]

vars_["dRbb"] = [0.2, 0, 6]
vars_["abs(dphi_bb)"] = [0.1, 0, 3.2]
vars_["abs(dphi_ll_bb)"] = [0.1, 0, 3.2]
vars_["dR_ll_bb"] = [0.2, 0, 6]
vars_["abs(dphi_WW_bb)"] = [0.1, 0, 3.2]
vars_["mass_X"] = [20, 100, 1300]
vars_["mass_X_scaled"] = [20, 100, 1300]
vars_["met"] = [10, 0, 500]
vars_["abs(metPhi)"] = [0.1, 0, 3.2]
vars_["abs(dphi_met_ll)"] = [0.1, 0, 3.2]
vars_["mass_met_ll"] = [10, 0, 400]
vars_["met_pTll"] = [20, 0, 800]

vars_["HT2"] = [20, 0, 1200]
vars_["HT2Ratio"] = [0.05, 0, 1]
vars_["MT_HWW"] = [10, 0, 300]
vars_["MT_1"] = [20,0,1200]
vars_["MT_1_scaled"] = [20,0,1200]
vars_["mll"] = [10,0,600]
vars_["mt2"] = [5, 0, 140]
vars_["mt2_00"] = [20, 0, 1000]
vars_["mt2_01"] = [10, 0, 800]
vars_["mt2_10"] = [10, 0, 800]
vars_["mt2_llbb"] = [2, 0, 300]
vars_["mbb"] = [5,0,350]
vars_["mt2_bb"] = [10,0,800]
vars_["mt2_bvis"] = [10,0,600]
vars_["mt2_lvis"] = [10, 0, 600]
vars_["mT_llmet"] = [20,0,1200]
vars_["mT_bb"] = [10, 0, 500]
vars_["min_mT_llmet_bb"] = [10,0,700]
vars_["max_mT_llmet_bb"] = [20,0,2000]

vars_["mt2_llbb"] = [10, 0, 500]
vars_["abs(cosTheta2)"] = [0.05, 0, 1]


nice_names = {}
for x in vars_.keys() :
    nice_names[x] = x

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

