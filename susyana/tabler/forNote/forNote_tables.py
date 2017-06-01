
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
#signal_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/d_jan30/mc/Raw/"
signal_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0232/b_mar7/mc/Raw/"
signal_4body_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/b_jan18/mc/Raw/" 
diboson_rawdir_SF = "/data/uclhc/uci/user/dantrim/ntuples/n0231/d_jan30/mc/diboson_SF/Raw/"
diboson_rawdir_DF = "/data/uclhc/uci/user/dantrim/ntuples/n0231/d_jan30/mc/diboson_DF/Raw/"
#fake_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0226/forFake3/fakes.3body/"
fake_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/fakes/from_claudia/"
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/d_jan30/data/Raw/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0231val/filelists/"
backgrounds = []

#### MC
lumi_ = {}
lumi_[36.0] = 36.0

lumi_val = 36.0
"""
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
diboson.set_chain_from_list_CONDOR(filelist_dir+ "diboson_new_check/", diboson_rawdir_SF)
backgrounds.append(diboson)

# diboson DF
diboson1 = background.Background("vvDF", "VV-DF (Sherpa)")
diboson1.set_debug()
diboson1.scale_factor = lumi_[lumi_val]
diboson1.set_fillStyle(0)
diboson1.setLineStyle(1)
diboson1.set_color(r.TColor.GetColor("#41C1FC"))
diboson1.set_treename("diboson_sherpa_DF")
diboson1.set_chain_from_list_CONDOR(filelist_dir+ "diboson_new_check/", diboson_rawdir_DF)
backgrounds.append(diboson1)

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
#wjets = background.Background("wjets", "W+Jets (Sherpa)")
#wjets.set_debug()
#wjets.scale_factor = lumi_[lumi_val]
#wjets.set_fillStyle(0)
#wjets.setLineStyle(1)
#wjets.set_color(r.TColor.GetColor("#5E9AD6"))
#wjets.set_treename("wjets")
#wjets.set_chain_from_list_CONDOR(filelist_dir+ "wjets_sherpa/", rawdir)
#backgrounds.append(wjets)


#
#drel = background.Background("drellyan", "Drell-Yan")
#drel.set_debug()
#drel.scale_factor = lumi_[lumi_val]
#drel.set_fillStyle(0)
#drel.setLineStyle(1)
#drel.set_color(r.kYellow)
#drel.set_treename("drellyan")
#drel.set_chain_from_list_CONDOR(filelist_dir+ "drellyan_sherpa/", rawdir)
#backgrounds.append(drel)
###
##
"""
### fakes
#fakes = background.Background("fakes", "Non-Prompt")
##fakes.scale_factor = 2.95
#fakes.scale_factor = 1.00
#fakes.set_treename("superNt")
##fakes.set_file(fake_rawdir + "physics_Main_276262_303560_FakesInclusive.root")
#fakes.set_file(fake_rawdir + "fakes_3body.root")
#fakes.set_merged_tree("superNt")
#backgrounds.append(fakes)

lines = open("signal_list.txt").readlines()
for iline, line in enumerate(lines) :
    if not line : continue
    line = line.strip()

    line = line.split()
    dsid = line[0]
    mx = line[1]
    my = line[2]

    funny = "bwn%s_%s"%(mx,my)
    notfunny = "(%s,%s)"%(mx,my)
    name = "sig%d"%iline

    s = background.Background(funny, notfunny)
    s.setSignal()
    s.set_debug()
    s.scale_factor = lumi_[lumi_val]
    s.set_treename(name)
    s.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", signal_rawdir, dsid)
    backgrounds.append(s)


#sig1 = background.Background("bwn350_230", "(350,230)")
#sig1.setSignal()
#sig1.set_debug()
#sig1.scale_factor = lumi_[lumi_val]
#sig1.set_fillStyle(0)
#sig1.setLineStyle(2)
#sig1.set_color(r.kBlue)
#sig1.set_treename("sig1")
#sig1.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", signal_rawdir, "389956")
#backgrounds.append(sig1)
"""

sig2 = background.Background("bwn300_180", "(300,180)")
sig2.setSignal()
sig2.set_debug()
sig2.scale_factor = lumi_[lumi_val]
sig2.setLineStyle(2)
sig2.set_color(r.kGreen)
sig2.set_treename("sig2")
sig2.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", signal_rawdir, "389950")
backgrounds.append(sig2)

sig3 = background.Background("bwn300_150", "(300,150)")
sig3.setSignal()
sig3.set_debug()
sig3.scale_factor = lumi_[lumi_val]
sig3.setLineStyle(2)
sig3.set_color(r.kBlack)
sig3.set_treename("sig3")
sig3.set_chain_from_list_CONDOR(filelist_dir + "bwn/", signal_rawdir, "389949")
backgrounds.append(sig3)

sig3body = background.Background("bwn300_210", "(300,210)")
sig3body.setSignal()
sig3body.set_debug()
sig3body.scale_factor = lumi_[lumi_val]
sig3body.set_treename("sig3body")
sig3body.set_chain_from_list_CONDOR(filelist_dir + "bwn/", signal_rawdir, "389951")
backgrounds.append(sig3body)

sig4body = background.Background("bwn300_220", "(300,220)")
sig4body.setSignal()
sig4body.set_debug()
sig4body.scale_factor = lumi_[lumi_val]
sig4body.set_treename("sig4body")
sig4body.set_chain_from_list_CONDOR(filelist_dir + "bffN/", signal_4body_rawdir, "389987")
backgrounds.append(sig4body)

s1 = background.Background("bwn1","(250,160)")
s1.setSignal()
s1.scale_factor = lumi_[lumi_val]
s1.set_treename("s1")
s1.set_chain_from_list_CONDOR(filelist_dir + "bwn/", signal_rawdir, "389945")
backgrounds.append(s1)

s2 = background.Background("bwn2","(275,155)")
s2.setSignal()
s2.scale_factor = lumi_[lumi_val]
s2.set_treename("s2")
s2.set_chain_from_list_CONDOR(filelist_dir + "bwn/", signal_rawdir, "387947")
backgrounds.append(s2)

s3 = background.Background("bwn3","(300,150)")
s3.setSignal()
s3.scale_factor = lumi_[lumi_val]
s3.set_treename("s3")
s3.set_chain_from_list_CONDOR(filelist_dir + "bwn/", signal_rawdir, "389949")
backgrounds.append(s3)

s4 = background.Background("bwn4","(350,260)")
s4.setSignal()
s4.scale_factor = lumi_[lumi_val]
s4.set_treename("s4")
s4.set_chain_from_list_CONDOR(filelist_dir + "bwn/", signal_rawdir, "389957")
backgrounds.append(s4)

s5 = background.Background("bwn5","(375,255)")
s5.setSignal()
s5.scale_factor = lumi_[lumi_val]
s5.set_treename("s5")
s5.set_chain_from_list_CONDOR(filelist_dir + "bwn/", signal_rawdir, "389959")
backgrounds.append(s5)

s6 = background.Background("bwn6","(400,250)")
s6.setSignal()
s6.scale_factor = lumi_[lumi_val]
s6.set_treename("s6")
s6.set_chain_from_list_CONDOR(filelist_dir + "bwn/", signal_rawdir, "389961")
backgrounds.append(s6)
"""

#dib0 = background.Background("dib0", "WW->lvlv")
#dib0.scale_factor = lumi_[lumi_val]
#dib0.set_fillStyle(0)
#dib0.setLineStyle(1)
#dib0.set_treename("powhegVV_WWlvlv")
#dib0.set_chain_from_list_CONDOR(filelist_dir + "powhegVV_WWlvlv/", rawdir)
#backgrounds.append(dib0)
#
#dib1 = background.Background("dib1", "ZZ->vvll")
#dib1.scale_factor = lumi_[lumi_val]
#dib1.set_fillStyle(0)
#dib1.setLineStyle(1)
#dib1.set_treename("powhegVV_ZZvvll")
#dib1.set_chain_from_list_CONDOR(filelist_dir + "powhegVV_ZZvvll/", rawdir)
#backgrounds.append(dib1)
#
#dib2 = background.Background("dib2", "WZ->qqll")
#dib2.scale_factor = lumi_[lumi_val]
#dib2.set_fillStyle(0)
#dib2.setLineStyle(1)
#dib2.set_treename("powhegVV_WZqqll")
#dib2.set_chain_from_list_CONDOR(filelist_dir + "powhegVV_WZqqll/", rawdir)
#backgrounds.append(dib2)
#
#dib3 = background.Background("dib3", "ZZ->qqll")
#dib3.scale_factor = lumi_[lumi_val]
#dib3.set_fillStyle(0)
#dib3.setLineStyle(1)
#dib3.set_treename("powhegVV_ZZqqll")
#dib3.set_chain_from_list_CONDOR(filelist_dir + "powhegVV_ZZqqll/", rawdir)
#backgrounds.append(dib3)

#s0 = background.Background("bwn225_135", "(225,135)")
#s0.setSignal()
#s0.scale_factor = lumi_[lumi_val]
#s0.set_treename("s0")
#s0.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "387940")
#backgrounds.append(s0)
#
#s1 = background.Background("bwn250_160", "(250,160)")
#s1.setSignal()
#s1.scale_factor = lumi_[lumi_val]
#s1.set_treename("s1")
#s1.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "387943")
#backgrounds.append(s1)
#
#s6 = background.Background("bwn275_185", "(275,185)")
#s6.setSignal()
#s6.scale_factor = lumi_[lumi_val]
#s6.set_treename("s6")
#s6.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "387946")
#backgrounds.append(s6)
#
#s7 = background.Background("bwn300_210", "(300,210)")
#s7.setSignal()
#s7.scale_factor = lumi_[lumi_val]
#s7.set_treename("s7")
#s7.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "387949")
#backgrounds.append(s7)
#
#s8 = background.Background("bwn325_235", "(325,235)")
#s8.setSignal()
#s8.scale_factor = lumi_[lumi_val]
#s8.set_treename("s8")
#s8.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "387952")
#backgrounds.append(s8)
#
#
#s2 = background.Background("bwn250_100", "(250,100)")
#s2.setSignal()
#s2.scale_factor = lumi_[lumi_val]
#s2.set_treename("s2")
#s2.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "387941")
#backgrounds.append(s2)
#
#s3 = background.Background("bwn275_125", "(275,125)")
#s3.setSignal()
#s3.scale_factor = lumi_[lumi_val]
#s3.set_treename("s3")
#s3.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "3879444")
#backgrounds.append(s3)
#
#s4 = background.Background("bwn250_130", "(250,130)")
#s4.setSignal()
#s4.scale_factor = lumi_[lumi_val]
#s4.set_treename("s4")
#s4.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "387942")
#backgrounds.append(s4)
#
#s5 = background.Background("bwn275_155", "(275,155)")
#s5.setSignal()
#s5.scale_factor = lumi_[lumi_val]
#s5.set_treename("s5")
#s5.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "387945")
#backgrounds.append(s5)


"""
#### DATA
data = background.Data()
data.set_color(r.kBlack)
data.set_treename("Data")
data.set_chain_from_list_CONDOR(filelist_dir + "dataToRun/", data_rawdir)
"""


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
mll_req = "abs(mll-91.2)>20"
mll_reqRevert = "abs(mll-91.2)<20"

isEE = "(nElectrons==2 && %s && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"%mll_req
isMM = "(nMuons==2 && %s && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"%mll_req
isSF = "((nMuons==2 || nElectrons==2) && %s"%mll_req
isDF = "(nElectrons==1 && nMuons==1)"
inZ = "((nMuons==2 || nElectrons==2) && %s"%mll_req

isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<0"
isSFOS = "(( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && abs(mll-91.2)>20 && (l_q[0]*l_q[1])<0)"
isSFOSNoMll = "(( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && (l_q[0]*l_q[1])<0)"
isSFOSRevert = "(( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && abs(mll-91.2)<20 && (l_q[0]*l_q[1])<0)"

isDF = "nLeptons==2 && nMuons==1 && nElectrons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"
isEE = "nLeptons==2 && nElectrons==2 && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20 && %s"%mll_req
isEERevert = "nLeptons==2 && nElectrons==2 && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20 && %s"%mll_reqRevert
isMM = "nLeptons==2 && nMuons==2     && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20 && %s"%mll_req
isMMRevert = "nLeptons==2 && nMuons==2     && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20 && %s"%mll_reqRevert
isSF = "(nLeptons==2 && ( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && %s && (l_q[0]*l_q[1])<0)"%mll_req
isSFRevert = "(nLeptons==2 && ( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && %s && (l_q[0]*l_q[1])<0)"%mll_reqRevert
isSF = "( %s ) || ( %s )"%(isEE, isMM)

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
sr_w_def = "nBJets==0 && RPT>0.7 && gamInvRp1>0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && MDR>95 && mll>20 && " + trigger 
reg = region.Region()
reg.name = "srwDF"
reg.displayname = "SRW-DF"
reg.tcut = isDFOS + " && " + sr_w_def 
regions.append(reg)

reg1 = region.Region()
reg1.name = "srwSF"
reg1.displayname = "SRW-SF"
reg1.tcut = isSFOS + " && " + sr_w_def
regions.append(reg1)

#reg = region.Region()
#reg.name = "srwEE"
#reg.displayname = "SRW-EE"
#reg.tcut = isEE + " && " + sr_w_def 
#regions.append(reg)
#
#reg = region.Region()
#reg.name = "srwMM"
#reg.displayname = "SRW-MM"
#reg.tcut = isMM + " && " + sr_w_def 
#regions.append(reg)

sr_t_def = "nBJets>0 && RPT>0.7 && gamInvRp1>0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && MDR>110 && mll>20 && " + trigger 
reg2 = region.Region()
reg2.name = "srtDF"
reg2.displayname = "SRT-DF"
reg2.tcut = isDFOS + " && " + sr_t_def 
regions.append(reg2)

reg3 = region.Region()
reg3.name = "srtSF"
reg3.displayname = "SRT-SF"
reg3.tcut = isSFOS + " && " + sr_t_def
regions.append(reg3)

#reg = region.Region()
#reg.name = "srtMM"
#reg.displayname = "SRt-MM"
#reg.tcut = isMM + " && " + sr_t_def 
#regions.append(reg)
#
#reg = region.Region()
#reg.name = "srtEE"
#reg.displayname = "SRt-EE"
#reg.tcut = isEE + " && " + sr_t_def 
#regions.append(reg)

################ CONTROL AND VALIDATION REGIONS ##################
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
#
## crvSF
#reg = region.Region()
#reg.name = "crvSF"
#reg.displayname = "CR-VV-SF"
#reg.tcut = isSFOS + " && nBJets==0 && MDR>70 && DPB_vSS<(0.9*abs(cosThetaB)+1.6) && RPT<0.5 && gamInvRp1>0.7 && mll>20 && " + trigger
#regions.append(reg)
#
## vrt
#reg = region.Region()
#reg.name = "vrt"
#reg.displayname = "VR-Top"
#reg.tcut = isDFOS + " && nBJets==0 && MDR>80 && RPT<0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger
#regions.append(reg)
#
## vrt-SF
##reg = region.Region()
##reg.name = "vrtSF"
##reg.displayname = "VR-Top-SF"
##reg.tcut = isSFOS + " && nBJets==0 && MDR>80 && RPT<0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger 
##regions.append(reg)
#
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
#reg.tcut = isSFOS + " && nBJets==0 && MDR>60 && MDR<95 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && RPT<0.4 && gamInvRp1>0.7 && mll>20 && " + trigger
#regions.append(reg)
#
#
