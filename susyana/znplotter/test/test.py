#!/bin/env python

import sys
import os
sys.path.append(os.environ['SUSYDIR'])

import supersusy.utils.background as background
import supersusy.susyana.znplotter.znregion as znregion
import supersusy.susyana.znplotter.znsignal as znsignal


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


rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0222/apr17/mc/Raw/" 
filelist_dir = "/data/uclhc/uci/user/dantrim/n0222val/filelists/" 

backgrounds = []

lumi = {}
lumi[3.21] = 1.0
lumi[10.0] = 3.12

lumi_val = 10.0

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

## diboson
diboson = background.Background("vv", "VV (Sherpa)")
diboson.scale_factor = lumi[lumi_val]
diboson.set_treename("diboson_sherpa")
diboson.set_chain_from_list_CONDOR(filelist_dir + "diboson_sherpa/", rawdir)
backgrounds.append(diboson)


###############################################
# prepare the signal configuration
###############################################

#signal_file_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0222/apr17/mc/Raw/" 
signal_file_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0222/apr17/sigB/Raw/"
#signal_grid = "bWN"
signal_grid = "bWNnew"
signal_scale_factor = lumi[lumi_val]


###############################################
# prepare the regions
###############################################

regions = []

####################
## mw selection
####################
isOS = "(l_q[0]*l_q[1])<0"
isDF = "nLeptons==2 && nElectrons==1 && nMuons==1 && l_pt[0]>20 && l_pt[1]>20"
isEE = "nLeptons==2 && nElectrons==2 && abs(mll-91.2)>10 && l_pt[0]>20 && l_pt[1]>20"
isMM = "nLeptons==2 && nMuons==2 && abs(mll-91.2)>10 && l_pt[0]>20 && l_pt[1]>20"

isDFOS = isDF + " && " + isOS
isEEOS = isEE + " && " + isOS
isMMOS = isMM + " && " + isOS

znreg = znregion.ZnRegion("mwsel", "mwsel", 1)
znreg.setParent(True)

# subregions
znregEE = znregion.ZnRegion("mwsel_ee", "mwsel_ee", 1.1)
znregEE.setTcut(isEEOS + " && MDR>90 && RPT>0.65 && gamInvRp1>0.65 && DPB_vSS>(1.1*abs(cosThetaB)+1.8) && nBJets==0")

znregMM = znregion.ZnRegion("mwsel_mm", "mwsel_mm", 1.2)
znregMM.setTcut(isMMOS + " && MDR>90 && RPT>0.65 && gamInvRp1>0.65 && DPB_vSS>(1.1*abs(cosThetaB)+1.8) && nBJets==0")

znregDF = znregion.ZnRegion("mwsel_df", "mwsel_df", 1.3)
znregDF.setTcut(isDFOS + " && MDR>90 && RPT>0.65 && gamInvRp1>0.65 && DPB_vSS>(1.1*abs(cosThetaB)+1.8) && nBJets==0")



# add mwsel subregions
znreg.add_orthogonal_subregion(znregEE)
znreg.add_orthogonal_subregion(znregMM)
znreg.add_orthogonal_subregion(znregDF)

regions.append(znreg)


####################
## mtselection
####################

znregMT = znregion.ZnRegion("mtsel", "mtsel", 2)
znregMT.setParent(True)

# subregions
znregMTEE = znregion.ZnRegion("mtsel_ee", "mtsel_ee", 2.1)
znregMTEE.setTcut(isEEOS + " && MDR>110 && RPT>0.65 && gamInvRp1>0.65 && DPB_vSS>(1.1*abs(cosThetaB)+1.8) && nBJets>0")

znregMTMM = znregion.ZnRegion("mtsel_mm", "mtsel_mm", 2.2)
znregMTMM.setTcut(isMMOS + " && MDR>110 && RPT>0.65 && gamInvRp1>0.65 && DPB_vSS>(1.1*abs(cosThetaB)+1.8) && nBJets>0")

znregMTDF = znregion.ZnRegion("mtsel_df", "mtsel_df", 2.3)
znregMTDF.setTcut(isDFOS + " && MDR>110 && RPT>0.65 && gamInvRp1>0.65 && DPB_vSS>(1.1*abs(cosThetaB)+1.8) && nBJets>0")



# add mwsel subregions
znregMT.add_orthogonal_subregion(znregMTEE)
znregMT.add_orthogonal_subregion(znregMTMM)
znregMT.add_orthogonal_subregion(znregMTDF)

regions.append(znregMT)



