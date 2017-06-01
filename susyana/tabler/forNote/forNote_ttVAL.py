
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
rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/d_jan30/mc/Raw/"
diboson_rawdir_SF = "/data/uclhc/uci/user/dantrim/ntuples/n0231/d_jan30/mc/diboson_SF/Raw/"
diboson_rawdir_DF = "/data/uclhc/uci/user/dantrim/ntuples/n0231/d_jan30/mc/diboson_DF/Raw/"
fake_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0226/forFake3/fakes.3body/"
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/d_jan30/data/Raw/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0231val/filelists/"
backgrounds = []

#### MC
lumi_ = {}
lumi_[36.0] = 36.0

lumi_val = 36.0
#
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

# ttV
ttv = background.Background("ttV", "t+bar{t} V")
ttv.set_debug()
ttv.scale_factor = lumi_[lumi_val]
ttv.set_fillStyle(0)
ttv.setLineStyle(1)
ttv.set_color(r.TColor.GetColor("#9bcdfd"))
ttv.set_treename("TTV")
ttv.set_chain_from_list_CONDOR(filelist_dir+ "ttV/", rawdir)
backgrounds.append(ttv)

# diboson SF
diboson = background.Background("vvSF", "VV-SF (Sherpa)")
diboson.set_debug()
diboson.scale_factor = lumi_[lumi_val]
diboson.set_fillStyle(0)
diboson.setLineStyle(1)
diboson.set_color(r.TColor.GetColor("#41C1FC"))
diboson.set_treename("diboson_sherpa_SF")
diboson.set_chain_from_list_CONDOR(filelist_dir+ "BLAHHHVV/", diboson_rawdir_SF)
#diboson.set_chain_from_list_CONDOR(filelist_dir+ "diboson_new_check/", diboson_rawdir_SF)
backgrounds.append(diboson)

# diboson DF
diboson1 = background.Background("vvDF", "VV-DF (Sherpa)")
diboson1.set_debug()
diboson1.scale_factor = lumi_[lumi_val]
diboson1.set_fillStyle(0)
diboson1.setLineStyle(1)
diboson1.set_color(r.TColor.GetColor("#41C1FC"))
diboson1.set_treename("diboson_sherpa_DF")
diboson1.set_chain_from_list_CONDOR(filelist_dir+ "BLAHHHVV/", diboson_rawdir_DF)
#diboson1.set_chain_from_list_CONDOR(filelist_dir+ "diboson_new_check/", diboson_rawdir_DF)
backgrounds.append(diboson1)

## diboson DF
#diboson2 = background.Background("vvDFEWK", "VV-DF (Sherpa, EWK)")
#diboson2.set_debug()
#diboson2.scale_factor = lumi_[lumi_val]
#diboson2.set_fillStyle(0)
#diboson2.setLineStyle(1)
#diboson2.set_color(r.TColor.GetColor("#41C1FC"))
#diboson2.set_treename("diboson_sherpa_DF_EWK")
#diboson2.set_chain_from_list_CONDOR(filelist_dir+ "EWK/", diboson_rawdir_DF)
##diboson1.set_chain_from_list_CONDOR(filelist_dir+ "diboson_new_check/", diboson_rawdir_DF)
#backgrounds.append(diboson2)




## diboson DF
#diboson3 = background.Background("vvSFEWK", "VV-SF (Sherpa, EWK)")
#diboson3.set_debug()
#diboson3.scale_factor = lumi_[lumi_val]
#diboson3.set_fillStyle(0)
#diboson3.setLineStyle(1)
#diboson3.set_color(r.TColor.GetColor("#41C1FC"))
#diboson3.set_treename("diboson_sherpa_SF_EWK")
#diboson3.set_chain_from_list_CONDOR(filelist_dir+ "EWK/", diboson_rawdir_SF)
##diboson1.set_chain_from_list_CONDOR(filelist_dir+ "diboson_new_check/", diboson_rawdir_DF)
#backgrounds.append(diboson3)
#
## diboson DF
#diboson4 = background.Background("vvDFEWK2", "VV-DF (Sherpa, EWK2)")
#diboson4.set_debug()
#diboson4.scale_factor = lumi_[lumi_val]
#diboson4.set_fillStyle(0)
#diboson4.setLineStyle(1)
#diboson4.set_color(r.TColor.GetColor("#41C1FC"))
#diboson4.set_treename("diboson_sherpa_DF_EWK2")
#diboson4.set_chain_from_list_CONDOR(filelist_dir+ "EWK2/", diboson_rawdir_DF)
##diboson1.set_chain_from_list_CONDOR(filelist_dir+ "diboson_new_check/", diboson_rawdir_DF)
#backgrounds.append(diboson4)

## diboson DF
#diboson5 = background.Background("vvSFEWK2", "VV-SF (Sherpa, EWK2)")
#diboson5.set_debug()
#diboson5.scale_factor = lumi_[lumi_val]
#diboson5.set_fillStyle(0)
#diboson5.setLineStyle(1)
#diboson5.set_color(r.TColor.GetColor("#41C1FC"))
#diboson5.set_treename("diboson_sherpa_SF_EWK2")
#diboson5.set_chain_from_list_CONDOR(filelist_dir+ "EWK2/", diboson_rawdir_SF)
##diboson1.set_chain_from_list_CONDOR(filelist_dir+ "diboson_new_check/", diboson_rawdir_DF)
#backgrounds.append(diboson5)




# Zjets
zjets = background.Background("zjets", "Z+jets (Sherpa)")
zjets.set_debug()
zjets.scale_factor = lumi_[lumi_val]
zjets.set_fillStyle(0)
zjets.setLineStyle(1)
zjets.set_color(r.TColor.GetColor("#FFEF53"))
zjets.set_treename("zjets_sherpa")
zjets.set_chain_from_list_CONDOR(filelist_dir+ "zjets_and_DY/", rawdir)
backgrounds.append(zjets)
#
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



##### DATA
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

#mll_req = "(mll<71 || mll>111)"
mll_req = "abs(mll-91.2)>10"
mll_reqRevert = "abs(mll-91.2)<10"
mll_req20 = "abs(mll-91.2)>20."

isEE = "(nElectrons==2 && %s && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"%mll_req
isMM = "(nMuons==2 && %s && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"%mll_req
isSF = "((nMuons==2 || nElectrons==2) && %s"%mll_req
isDF = "(nElectrons==1 && nMuons==1)"
inZ = "((nMuons==2 || nElectrons==2) && %s"%mll_req

isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<0"
isSFOS = "(( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && abs(mll-91.2)>10 && (l_q[0]*l_q[1])<0)"
isSFOSNoMll = "(( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && (l_q[0]*l_q[1])<0)"
isSFOSRevert = "(( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && abs(mll-91.2)<10 && (l_q[0]*l_q[1])<0)"
isSFOS20 = "(( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && abs(mll-91.2)>20 && (l_q[0]*l_q[1])<0)"

isDF = "nLeptons==2 && nMuons==1 && nElectrons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"
isEE = "nLeptons==2 && nElectrons==2 && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20 && %s"%mll_req
isEERevert = "nLeptons==2 && nElectrons==2 && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20 && %s"%mll_reqRevert
isMM = "nLeptons==2 && nMuons==2     && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20 && %s"%mll_req
isMMRevert = "nLeptons==2 && nMuons==2     && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20 && %s"%mll_reqRevert
isSF = "(nLeptons==2 && ( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && %s && (l_q[0]*l_q[1])<0)"%mll_req
isSFRevert = "(nLeptons==2 && ( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && %s && (l_q[0]*l_q[1])<0)"%mll_reqRevert
isEE20 = "nLeptons==2 && nElectrons==2 && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20 && %s"%mll_req20
isMM20 = "nLeptons==2 && nMuons==2     && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20 && %s"%mll_req20
isSF20 = "(nLeptons==2 && ( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && %s && (l_q[0]*l_q[1])<0)"%mll_req20

trigger = "((year==2015 && trig_pass2015==1) || (year==2016 && trig_pass2016update==1))"

#start_srw_sf = isSFOS + " && " + trigger + " && mll>20 && MDR>95 && nBJets==0"
#reg = region.Region()
#reg.name = "eoySRWSF"
#reg.displayname = "SRw-SF (EOY)"
##reg.tcut = start_srw_sf + " && RPT>0.65 && gamInvRp1>0.75 && DPB_vSS>(0.85*abs(cosThetaB) + 1.85)"
#reg.setCutFlow()
#reg.addCut("Start SRW-SF", start_srw_sf)
#reg.addCut("RPT>0.65", "RPT>0.65")
#reg.addCut("gamInvRp1>0.75", "gamInvRp1>0.75")
#reg.addCut("DIAG(0.85,1.85)", "DPB_vSS>(0.85*abs(cosThetaB)+1.85)")
##regions.append(reg)
#
#reg = region.Region()
#reg.name = "moriondSRWSF"
#reg.displayname = "SRw-SF (Moriond)"
#reg.setCutFlow()
##reg.addCut("Start SRW-SF", start_srw_sf)
##reg.addCut("RPT>0.65","RPT>0.65")
##reg.addCut("gamInvRp1>0.7","gamInvRp1>0.7")
##reg.addCut("DIAG(0.9,1.6)","DPB_vSS>(0.9*abs(cosThetaB)+1.6)")
#reg.addCut("(0.65,0.7,0.85,1.85)",start_srw_sf + " && RPT>0.65 && gamInvRp1>0.7 && DPB_vSS>(0.85*abs(cosThetaB)+1.85)")
#regions.append(reg)



#test_def = "nBJets==0 && abs(mll-91.2)>10 && l_pt[0]>25 && l_pt[1]>20 && (nMuons==2 || nElectrons==2) && mll>40 && (l_q[0]*l_q[1])<0 && " + trigger
#reg = region.Region()
#reg.name = "test"
#reg.tcut = test_def
#regions.append(reg)

#sr_w_def = "nBJets==0 && RPT>0.7 && gamInvRp1>0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && MDR>95 && mll>20 && " + trigger 
#reg = region.Region()
#reg.name = "srwDF"
#reg.displayname = "SRW-DF"
#reg.tcut = isDFOS + " && " + sr_w_def 
#regions.append(reg)
#
#reg = region.Region()
#reg.name = "srwEE"
#reg.displayname = "SRW-EE"
#reg.tcut = isEE + " && " + sr_w_def 
#regions.append(reg)
#
##reg = region.Region()
##reg.name = "srwEE20"
##reg.displayname = "SRW-EE 20"
##reg.tcut = isEE20 + " && " + sr_w_def 
##regions.append(reg)
#
#reg = region.Region()
#reg.name = "srwMM"
#reg.displayname = "SRW-MM"
#reg.tcut = isMM + " && " + sr_w_def 
#regions.append(reg)
#
##reg = region.Region()
##reg.name = "srwMM20"
##reg.displayname = "SRW-MM 20"
##reg.tcut = isMM20 + " && " + sr_w_def 
##regions.append(reg)
#
#sr_t_def = "nBJets>0 && RPT>0.7 && gamInvRp1>0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && MDR>110 && mll>20 && " + trigger 
#reg = region.Region()
#reg.name = "srtDF"
#reg.displayname = "SRt-DF"
#reg.tcut = isDFOS + " && " + sr_t_def 
#regions.append(reg)
#
#reg = region.Region()
#reg.name = "srtMM"
#reg.displayname = "SRt-MM"
#reg.tcut = isMM + " && " + sr_t_def 
#regions.append(reg)
#
##reg = region.Region()
##reg.name = "srtMM20"
##reg.displayname = "SRt-MM 20"
##reg.tcut = isMM20 + " && " + sr_t_def 
##regions.append(reg)
#
#reg = region.Region()
#reg.name = "srtEE"
#reg.displayname = "SRt-EE"
#reg.tcut = isEE + " && " + sr_t_def 
#regions.append(reg)
#
##reg = region.Region()
##reg.name = "srtEE20"
##reg.displayname = "SRt-EE 20"
##reg.tcut = isEE20 + " && " + sr_t_def 
##regions.append(reg)


############### CONTROL AND VALIDATION REGIONS ##################

### crtSF
reg = region.Region()
reg.name = "crtSF17"
reg.displayname = "CR-Top-SF"
reg.tcut = isDFOS + " && nBJets>0 && MDR>60 && MDR<95 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && RPT<0.4 && gamInvRp1>0.7 && mll>20 && " + trigger
regions.append(reg)

reg = region.Region()
reg.name = "vrtSF17"
reg.displayname = "VR-Top-SF"
reg.tcut = isSFOS20 + " && nBJets==0 && MDR>80 && RPT<0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger
regions.append(reg)

### crt
#reg = region.Region()
#reg.name = "crt"
#reg.displayname = "CR-Top"
#reg.tcut = isDFOS + " && nBJets>0 && MDR>80 && RPT>0.7 && DPB_vSS<(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger
#regions.append(reg)
#
## crv df
#reg = region.Region()
#reg.name = "crv"
#reg.displayname = "CR-VV-DF"
#reg.tcut = isDFOS + " && nBJets==0 && MDR>50 && DPB_vSS<(0.9*abs(cosThetaB)+1.6) && RPT<0.5  && gamInvRp1>0.7 && mll>20 && " + trigger
#regions.append(reg)
## crv sf
#reg = region.Region()
#reg.name = "crvSF_ZZ"
#reg.displayname = "CR-VV-SF (ZZ)"
#reg.tcut = isSFOSNoMll + " && nBJets==0 && MDR>95 && DPB_vSS<(0.9*abs(cosThetaB)+1.6) && RPT<0.5 && gamInvRp1>0.7 && mll>20 && " + trigger
#regions.append(reg)

# crv sf w/ mll window at 20 GeV width 
#reg = region.Region()
#reg.name = "crvSF20"
#reg.displayname = "CR-VV-SF (20)"
#reg.tcut = isSFOS20 + " && nBJets==0 && MDR>70 && DPB_vSS<(0.9*abs(cosThetaB)+1.6) && RPT<0.5 && gamInvRp1>0.7 && mll>20 && " + trigger
#regions.append(reg)
# vrt
#reg = region.Region()
#reg.name = "vrt"
#reg.displayname = "VR-Top"
#reg.tcut = isDFOS + " && nBJets==0 && MDR>80 && RPT<0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger
#regions.append(reg)

# vrt-SF
#reg = region.Region()
#reg.name = "vrtSF"
#reg.displayname = "VR-Top-SF"
#reg.tcut = isSFOS + " && nBJets==0 && MDR>80 && RPT<0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger 
#regions.append(reg)

## vrv df
#reg = region.Region()
#reg.name = "vrv"
#reg.displayname = "VR-VV-DF"
#reg.tcut = isDFOS + " && nBJets==0 && MDR>50 && MDR<95 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && RPT<0.7 && gamInvRp1>0.7 && mll>20 && " + trigger
#regions.append(reg)
## vrv sf
#reg = region.Region()
#reg.name = "vrvSF"
#reg.displayname = "VR-VV-SF"
#reg.tcut = isSFOSRevert + " && nBJets==0 && MDR>60 && MDR<95 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && RPT<0.4 && gamInvRp1>0.7 && mll>20 && " + trigger
#regions.append(reg)
#
### vrv sf with 20 GeV window for Z-veto
##reg = region.Region()
##reg.name = "vrvSF20"
##reg.displayname = "VR-VV-SF (20)"
##reg.tcut = isSFOS20 + " && nBJets==0 && MDR>60 && MDR<95 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && RPT<0.4 && gamInvRp1>0.7 && mll>20 && " + trigger
##regions.append(reg)


