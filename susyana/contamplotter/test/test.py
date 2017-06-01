#!/bin/env python

import sys
import os
sys.path.append(os.environ['SUSYDIR'])

import supersusy.utils.background as background
import supersusy.utils.region as region


###############################################
# significance metric
###############################################
significance_metric = "Zn"

###############################################
# uncertainty assumption on bkg (fractional)
###############################################
bkg_uncertainty = 0.30


###############################################
# setup background samples
###############################################


#rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/d_jan30/mc/Raw/"
#diboson_rawdir_SF = "/data/uclhc/uci/user/dantrim/ntuples/n0231/d_jan30/mc/diboson_SF/Raw/"
#diboson_rawdir_DF = "/data/uclhc/uci/user/dantrim/ntuples/n0231/d_jan30/mc/diboson_DF/Raw/"
#filelist_dir = "/data/uclhc/uci/user/dantrim/n0231val/filelists/"

rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0232/b_mar7/mc/Raw/"
diboson_rawdir_SF = "/data/uclhc/uci/user/dantrim/ntuples/n0232/b_mar7/mc/diboson_SF/Raw/"
diboson_rawdir_DF = "/data/uclhc/uci/user/dantrim/ntuples/n0232/b_mar7/mc/diboson_DF/Raw/"
fake_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0232/fakes/mar9/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0232val/filelists/"

backgrounds = []

lumi = {}
lumi[36] = 36.0

lumi_val = 36

## ttbar
ttbar = background.Background("ttbar", "t#bar{t}")
ttbar.scale_factor = lumi[lumi_val]
ttbar.set_treename("ttbar_powheg")
ttbar.set_chain_from_list_CONDOR(filelist_dir + "ttbar/", rawdir)
backgrounds.append(ttbar)

## singletop
stop = background.Background("st", "Single top")
stop.scale_factor = lumi[lumi_val]
stop.set_treename("ST")
stop.set_chain_from_list_CONDOR(filelist_dir + "singletop/", rawdir)
backgrounds.append(stop)

## ttV
ttv = background.Background("ttV", "tt+V")
ttv.scale_factor = lumi[lumi_val]
ttv.set_treename("TTV")
ttv.set_chain_from_list_CONDOR(filelist_dir + "ttV/", rawdir)
backgrounds.append(ttv)

## diboson
diboson = background.Background("vvDF", "VV")
diboson.scale_factor = lumi[lumi_val]
diboson.set_treename("diboson_sherpa_DF")
diboson.set_chain_from_list_CONDOR(filelist_dir + "diboson_sherpa/", diboson_rawdir_DF)
backgrounds.append(diboson)

## zjets
zjets = background.Background("zjets", "Z+Jets")
zjets.scale_factor = lumi[lumi_val]
zjets.set_treename("zjets_sherpa")
zjets.set_chain_from_list_CONDOR(filelist_dir + "zjets_and_DY/", rawdir)
backgrounds.append(zjets)

## wjets
#wjets = background.Background("wjets", "W+Jets")
#wjets.scale_factor = lumi[lumi_val]
#wjets.set_treename("wjets_sherpa")
#wjets.set_chain_from_list_CONDOR(filelist_dir + "wjets_sherpa/", rawdir)
#backgrounds.append(wjets)

fakes = background.Background("fakes","FNP")
fakes.scale_factor = 1.0
fakes.set_treename("superNt")
fakes.set_file(fake_rawdir + "fakes_3body_mar10_361ifb.root")
fakes.set_merged_tree("superNt")
fakes.set_color(94)
fakes.set_fillStyle(0)
fakes.setLineStyle(1)
backgrounds.append(fakes)


## higgs
higgs = background.Background("higgs", "Higgs")
higgs.scale_factor = lumi[lumi_val]
higgs.set_treename("higgs")
higgs.set_chain_from_list_CONDOR(filelist_dir+ "higgs/", rawdir)
backgrounds.append(higgs)

#drel = background.Background("drellyan", "Drell-Yan")
#drel.set_debug()
#drel.scale_factor = lumi[lumi_val]
#drel.set_fillStyle(0)
#drel.setLineStyle(1)
##drel.set_color(r.kYellow)
#drel.set_color(r.TColor.GetColor("#feec60"))
#drel.set_treename("drellyan")
#drel.set_chain_from_list_CONDOR(filelist_dir+ "drellyan_sherpa/", rawdir)
#backgrounds.append(drel)


###############################################
# prepare the signal configuration
###############################################

signal_file_rawdir = rawdir
signal_grid = "bWNnew"
signal_scale_factor = lumi[lumi_val]


###############################################
# prepare the regions
###############################################

regions = []
isEE = "(nElectrons==2 && abs(mll-91.2)>20) && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"
isMM = "(nMuons==2 && abs(mll-91.2)>20) && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"
isSFOS = "(( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && abs(mll-91.2)>20 && (l_q[0]*l_q[1])<0)"
isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<0"
trigger = "((year==2015 && trig_pass2015==1) || (year==2016 && trig_pass2016update==1))"


reg = region.Region()
reg.name = "crv"
reg.displayname = "CR-VV-DF"
reg.tcut = isDFOS + " && nBJets==0 && MDR>50 && DPB_vSS<(0.9*abs(cosThetaB)+1.6) && RPT<0.5  && gamInvRp1>0.7 && mll>20 && " + trigger
regions.append(reg)

reg = region.Region()
reg.name = "crvSF"
reg.displayname = "CR-VV-SF"
reg.tcut = isSFOS + " && nBJets==0 && MDR>70 && DPB_vSS<(0.9*abs(cosThetaB)+1.6) && RPT<0.5 && gamInvRp1>0.7 && mll>20 && " + trigger
regions.append(reg)

reg = region.Region()
reg.name = "vrv"
reg.displayname = "VR-VV-DF"
reg.tcut = isDFOS + " && nBJets==0 && MDR>50 && MDR<95 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && RPT<0.7 && gamInvRp1>0.7 && mll>20 && " + trigger
regions.append(reg)

reg = region.Region()
reg.name = "vrvSF"
reg.displayname = "VR-VV-SF"
reg.tcut = isSFOS + " && nBJets==0 && MDR>60 && MDR<95 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && RPT<0.4 && gamInvRp1>0.7 && mll>20 && " + trigger
regions.append(reg)

reg = region.Region()
reg.name = "crt"
reg.displayname = "CR-Top"
reg.tcut = isDFOS + " && nBJets>0 && MDR>80 && RPT>0.7 && DPB_vSS<(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger
regions.append(reg)

reg = region.Region()
reg.name = "vrt"
reg.displayname = "VR-Top"
reg.tcut = isDFOS + " && nBJets==0 && MDR>95 && RPT<0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger
regions.append(reg)





#reg = region.Region()
#reg.name = "crv"
#reg.displayname = "CR-VV-DF"
#reg.tcut = isDFOS + " && nBJets==0 && MDR>50 && DPB_vSS<(0.9*abs(cosThetaB)+1.6) && RPT<0.5  && gamInvRp1>0.7 && mll>20 && " + trigger
#regions.append(reg)
#
#reg = region.Region()
#reg.name = "crvSF"
#reg.displayname = "CR-VV-SF"
#reg.tcut = isSFOS + " && nBJets==0 && MDR>70 && DPB_vSS<(0.9*abs(cosThetaB)+1.6) && RPT<0.5 && gamInvRp1>0.7 && mll>20 && " + trigger
#regions.append(reg)
#
#reg = region.Region()
#reg.name = "vrv"
#reg.displayname = "VR-VV-DF"
#reg.tcut = isDFOS + " && nBJets==0 && MDR>50 && MDR<95 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && RPT<0.7 && gamInvRp1>0.7 && mll>20 && " + trigger
#regions.append(reg)
#
#reg = region.Region()
#reg.name = "vrvSF"
#reg.displayname = "VR-VV-SF"
#reg.tcut = isSFOS + " && nBJets==0 && MDR>60 && MDR<95 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && RPT<0.4 && gamInvRp1>0.7 && mll>20 && " + trigger
#regions.append(reg)
#
#reg = region.Region()
#reg.name = "crt"
#reg.displayname = "CR-Top"
#reg.tcut = isDFOS + " && nBJets>0 && MDR>80 && RPT>0.7 && DPB_vSS<(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger
#regions.append(reg)
#
#reg = region.Region()
#reg.name = "vrt"
#reg.displayname = "VR-Top"
#reg.tcut = isDFOS + " && nBJets==0 && MDR>80 && RPT<0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger
#regions.append(reg)
