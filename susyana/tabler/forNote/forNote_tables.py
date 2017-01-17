
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
rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0228/a_sep21/mc/Raw/"
fake_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0226/forFake3/fakes.3body/"
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0228/a_sep21/all_data_Nov15/" 
#sf_diboson_dir = "/data/uclhc/uci/user/dantrim/ntuples/n0224/jun1#/mc/sf_diboson/Raw/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0228val/filelists/"
backgrounds = []                                                  #
                                                                  #
#### MC
lumi_ = {}
lumi_[3.21] = 1.0
lumi_[5.82] = 1.81
lumi_[6.0] = 1.87
lumi_[7.0] = 2.18
lumi_[8.0] = 2.50
lumi_[9.0] = 2.80
lumi_[10.0] = 3.12
lumi_[12.2] =  3.81
lumi_[13.3] = 4.14
lumi_[20.0] = 6.23
lumi_[35.0] = 10.9

lumi_val = 35.0

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

# diboson
diboson = background.Background("vv", "VV (Sherpa)")
diboson.set_debug()
diboson.scale_factor = lumi_[lumi_val]
diboson.set_fillStyle(0)
diboson.setLineStyle(1)
diboson.set_color(r.TColor.GetColor("#41C1FC"))
diboson.set_treename("diboson_sherpa")
#diboson.set_chain_from_list_CONDOR(filelist_dir+ "diboson_sherpa_lvlv/", sf_diboson_dir)
print "USING DIBOSON TEST"
print "USING DIBOSON TEST"
print "USING DIBOSON TEST"
print "USING DIBOSON TEST"
diboson.set_chain_from_list_CONDOR(filelist_dir+ "diboson_sherpa_lvlv_test/", rawdir)
backgrounds.append(diboson)


# Zjets
zjets = background.Background("zjets", "Z+jets (Sherpa)")
zjets.set_debug()
zjets.scale_factor = lumi_[lumi_val]
zjets.set_fillStyle(0)
zjets.setLineStyle(1)
zjets.set_color(r.TColor.GetColor("#FFEF53"))
zjets.set_treename("zjets_sherpa")
zjets.set_chain_from_list_CONDOR(filelist_dir+ "zjets_sherpa22/", rawdir)
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
wjets.set_chain_from_list_CONDOR(filelist_dir+ "wjets_sherpa22/", rawdir)
backgrounds.append(wjets)
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
### fakes
#fakes = background.Background("fakes", "Non-Prompt")
#fakes.scale_factor = 1.0
#fakes.set_treename("superNt")
#fakes.set_file(fake_rawdir + "physics_Main_276262_303560_FakesInclusive.root")
#fakes.set_merged_tree("superNt")
#backgrounds.append(fakes)


#sig1 = background.Background("bwn250_160", "(250,160)")
#sig1.setSignal()
#sig1.set_debug()
#sig1.scale_factor = lumi_[lumi_val]
#sig1.set_fillStyle(0)
#sig1.setLineStyle(2)
#sig1.set_color(r.kBlue)
#sig1.set_treename("sig1")
#sig1.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", rawdir, "387943")
#backgrounds.append(sig1)
#
#sig2 = background.Background("bwn300_180", "(300,180)")
#sig2.setSignal()
#sig2.set_debug()
#sig2.scale_factor = lumi_[lumi_val]
#sig2.setLineStyle(2)
#sig2.set_color(r.kGreen)
#sig2.set_treename("sig2")
#sig2.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", rawdir, "387948")
#backgrounds.append(sig2)
#
#sig3 = background.Background("bwn300_150", "(300,150)")
#sig3.setSignal()
#sig3.set_debug()
#sig3.scale_factor = lumi_[lumi_val]
#sig3.setLineStyle(2)
#sig3.set_color(r.kBlack)
#sig3.set_treename("sig3")
#sig3.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "387947")
#backgrounds.append(sig3)

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



##### DATA
data = background.Data()
data.set_color(r.kBlack)
data.set_treename("Data")
data.set_chain_from_list_CONDOR(filelist_dir + "data_toRun/", data_rawdir)


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

isEE = "(nElectrons==2 && %s && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"%mll_req
isMM = "(nMuons==2 && %s && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"%mll_req
isSF = "((nMuons==2 || nElectrons==2) && %s"%mll_req
isDF = "(nElectrons==1 && nMuons==1)"
inZ = "((nMuons==2 || nElectrons==2) && %s"%mll_req

isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<0"
isSFOS = "(( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && abs(mll-91.2)>10 && (l_q[0]*l_q[1])<0)"

isDF = "nLeptons==2 && nMuons==1 && nElectrons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"
isEE = "nLeptons==2 && nElectrons==2 && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20 && %s"%mll_req
isMM = "nLeptons==2 && nMuons==2     && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20 && %s"%mll_req
isSF = "(nLeptons==2 && ( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && %s && (l_q[0]*l_q[1])<0)"%mll_req

trigger = "((year==2015 && trig_pass2015==1) || (year==2016 && trig_pass2016update==1))"


test_def = "nBJets==0 && abs(mll-91.2)>10 && l_pt[0]>25 && l_pt[1]>20 && (nMuons==2 || nElectrons==2) && mll>40 && (l_q[0]*l_q[1])<0 && " + trigger
reg = region.Region()
reg.name = "test"
reg.tcut = test_def
regions.append(reg)

#sr_w_def = "nBJets==0 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && MDR>95 && mll>20 && " + trigger 
##sr_w_def = "nBJets==0 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && MDR>95 && mll>20 && " + trigger 
#reg = region.Region()
#reg.name = "srwDF"
#reg.displayname = "SRW-DF"
#reg.tcut = isDFOS + " && " + sr_w_def 
#regions.append(reg)

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
#
#sr_t_def = "nBJets>0 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && MDR>110 && mll>20 && " + trigger 
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
#reg = region.Region()
#reg.name = "srtEE"
#reg.displayname = "SRt-EE"
#reg.tcut = isEE + " && " + sr_t_def 
#regions.append(reg)
#
#reg = region.Region()
#reg.name = "crvDF"
#reg.displayname = "CRVDF"
#reg.tcut = isDFOS + " && nBJets==0 && MDR>30  && RPT<0.5 && gamInvRp1>0.8 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && mll>20 && " + trigger 
#regions.append(reg)
#
#reg = region.Region()
#reg.name = "crvSF"
#reg.displayname = "CRVSF"
#reg.tcut = isSFOS + " && nBJets==0 && MDR>30  && RPT<0.5 && gamInvRp1>0.8 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && met>70 && mll>20 && " + trigger
#regions.append(reg)
#
#reg = region.Region()
#reg.name = "vrv"
#reg.displayname = "VRVDF"
#reg.tcut = isDFOS + " && nBJets==0 && MDR>30 && MDR<80 && RPT<0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && mll>20 && " + trigger
#regions.append(reg)
#
#reg = region.Region()
#reg.name = "vrvSF"
#reg.displayname = "VRVSF"
#reg.tcut = isSFOS + " && nBJets==0 && MDR>30 && MDR<80  && RPT<0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && met>70 && mll>20 && " + trigger
#regions.append(reg)
##
##
###reg = region.Region()
###reg.name = "crvSF"
###reg.displayname = "crvSF"
###reg.tcut = isSFOS + " && nBJets==0 && MDR>30 && RPT>0.2 && RPT<0.5 && gamInvRp1>0.8 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && trig_pass2016==1"#"
###regions.append(reg)
##
#reg = region.Region()
#reg.name = "crt"
#reg.displayname = "CR-T"
#reg.tcut = isDFOS + " && nBJets>0 && MDR>80 && RPT>0.5 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && mll>20"# && " + trigger
#regions.append(reg)
#
#reg = region.Region()
#reg.name = "vrt"
#reg.displayname = "VR-T"
#reg.tcut = isDFOS + " && nBJets==0 && MDR>80 && RPT<0.5 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && mll>20 && " + trigger 
#regions.append(reg)
###
###
###
####
####
###reg = region.Region()
###reg.name = "srw_df"
###reg.displayname = "srw_df"
###reg.tcut = isDFOS + " && nBJets==0 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && MDR>95 && trig_pass2016==1 && mll>20" 
###regions.append(reg)
###
###reg = region.Region()
###reg.name = "srw_mm"
###reg.displayname = "srw_mm"
###reg.tcut = isMM + " && nBJets==0 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && MDR>95 && trig_pass2016==1 && mll>20" 
###regions.append(reg)
###
###reg = region.Region()
###reg.name = "srw_ee"
##
##reg = region.Region()
##reg.name = "crvDF"
##reg.displayname = "CRVDF"
##reg.tcut = isDFOS + " && nBJets==0 && MDR>30  && RPT<0.5 && gamInvRp1>0.8 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && trig_pass2016==1 && mll>20"
##regions.append(reg)
##
##reg = region.Region()
##reg.name = "crvSF"
##reg.displayname = "CRVSF"
##reg.tcut = isSFOS + " && nBJets==0 && MDR>30  && RPT<0.5 && gamInvRp1>0.8 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && trig_pass2016==1 && mll>20 && met>70"
##regions.append(reg)
##
##reg = region.Region()
##reg.name = "vrvSF"
##reg.displayname = "VRVSF"
##reg.tcut = isSFOS + " && nBJets==0 && MDR>30 && MDR<80 && RPT>0.2 && RPT<0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && trig_pass2016==1 && mll>20"
##regions.append(reg)
##
##
###reg = region.Region()
###reg.name = "crvSF"
###reg.displayname = "crvSF"
###reg.tcut = isSFOS + " && nBJets==0 && MDR>30 && RPT>0.2 && RPT<0.5 && gamInvRp1>0.8 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && trig_pass2016==1"#"
###regions.append(reg)
##
###reg = region.Region()
###reg.name = "crt"
###reg.displayname = "CR-T"
###reg.tcut = isDFOS + " && nBJets>0 && MDR>80 && RPT>0.5 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && trig_pass2016==1 && mll>20"
###regions.append(reg)
###
###reg = region.Region()
###reg.name = "vrt"
###reg.displayname = "VR-T"
###reg.tcut = isDFOS + " && nBJets==0 && MDR>80 && RPT<0.5 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && trig_pass2016==1 && mll>20"
###regions.append(reg)
###
###
###
###reg = region.Region()
###reg.name = "vrv"
###reg.displayname = "VRV"
###reg.tcut = isDFOS + " && nBJets==0 && MDR>30 && MDR<80 && RPT>0.2 && RPT<0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && trig_pass2016==1 && mll>20"
###regions.append(reg)
####
####
###reg = region.Region()
###reg.name = "srw_df"
###reg.displayname = "srw_df"
###reg.tcut = isDFOS + " && nBJets==0 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && MDR>95 && trig_pass2016==1 && mll>20" 
###regions.append(reg)
###
###reg = region.Region()
###reg.name = "srw_mm"
###reg.displayname = "srw_mm"
###reg.tcut = isMM + " && nBJets==0 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && MDR>95 && trig_pass2016==1 && mll>20" 
###regions.append(reg)
###
###reg = region.Region()
###reg.name = "srw_ee"
###reg.displayname = "srw_ee"
###reg.tcut = isEE + " && nBJets==0 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && MDR>95 && trig_pass2016==1 && mll>20" 
###regions.append(reg)
###
###reg = region.Region()
###reg.name = "srt_df"
###reg.displayname = "srt_df"
###reg.tcut = isDFOS + " && nBJets>0 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && MDR>110 && trig_pass2016==1 && mll>20" 
###regions.append(reg)
###
###reg = region.Region()
###reg.name = "srt_mm"
###reg.displayname = "srt_mm"
###reg.tcut = isMM + " && nBJets>0 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && MDR>110 && trig_pass2016==1 && mll>20" 
###regions.append(reg)
###
###reg = region.Region()
###reg.name = "srt_ee"
###reg.displayname = "srt_ee"
###reg.tcut = isEE + " && nBJets>0 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && MDR>110 && trig_pass2016==1 && mll>20" 
###regions.append(reg)
##
##
###reg = region.Region()
###reg.name = "ww"
###reg.displayname = "WW-like"
###### checking SF CR
####reg_cut = "nLeptons==2 && " + isSFOS +" && abs(mll-91.2)<10 && MDR>95 && nBJets==0 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && RPT<0.5 && RPT>0.2 && gamInvRp1>0.8"
###reg_cut = "nLeptons==2 && " + inZ + " && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && MDR>95 && nBJets==0 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && RPT<0.5 && RPT>0.2 && gamInvRp1>0.5"
###reg.tcut = reg_cut
###regions.append(reg)
###
####reg = region.Region()
####reg.simplename = "sfSRT"
####reg.displayname = "sfSRT"
####reg.tcut = isSFOS + " && MDR>110 && nBJets>0 && RPT>0.5 && gamInvRp1>0.7 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && trig_pass2016==1"#"
####regions.append(reg)
####
####reg = region.Region()
####reg.simplename = "dfSRT"
####reg.displayname = "dfSRT"
####reg.tcut = isDFOS + " && MDR>110 && nBJets>0 && RPT>0.5 && gamInvRp1>0.7 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && trig_pass2016==1"#"
####regions.append(reg)
###
####reg = region.Region()
####reg.simplename = "sfSRW"
####reg.displayname = "sfSRW"
####reg.tcut = isSFOS + " && MDR>95 && nBJets==0 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && trig_pass2016==1"#"
####regions.append(reg)
####
####reg = region.Region()
####reg.simplename = "dfSRW"
####reg.displayname = "dfSRW"
####reg.tcut = isDFOS + " && MDR>95 && nBJets==0 && RPT>0.5 && gamInvRp1>0.7 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && trig_pass2016==1"#"
####regions.append(reg)
###
###
###
###reg = region.Region()
###reg.name = "crv2"
###reg.displayname = "crv2"
###reg.tcut = isDFOS + " && nBJets==0 && MDR>30 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && RPT<0.5 && RPT>0.2 && gamInvRp1>0.8"
###regions.append(reg)
####
####reg = region.Region()
####reg.name = "vrv2"
####reg.displayname = "vrv2"
####reg.tcut = isDFOS + " && nBJets==0 && MDR>30 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && RPT<0.5 && gamInvRp1>0.8 && MDR<80" 
####regions.append(reg)

#############################################
# Set up the plots
#############################################

plots = []

