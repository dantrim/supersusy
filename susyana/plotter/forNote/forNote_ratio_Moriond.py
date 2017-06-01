import sys
sys.path.append(os.environ['SUSYDIR'])
import supersusy.utils.plot as plot
import supersusy.utils.background as background
import supersusy.utils.region as region
import supersusy.utils.systematic as systematic


#######################################
# samples
########################################
backgrounds = []
#rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/b_jan18/mc/Raw/"
#diboson_raw_dir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/b_jan18/mc/new_diboson_SF/Raw/" 
#signal_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/a_jan16/mc/Raw/" 
#data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/b_jan18/data/Raw/"

rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0232/b_mar7/mc/Raw/"
diboson_rawdir_SF = "/data/uclhc/uci/user/dantrim/ntuples/n0232/b_mar7/mc/diboson_SF/Raw/"
diboson_rawdir_DF = "/data/uclhc/uci/user/dantrim/ntuples/n0232/b_mar7/mc/diboson_DF/Raw/"
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0232/b_mar7/data/Raw/"
zjets_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0232/b_mar7/mc/zjets_window/Raw//"



#fake_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/fakes/from_claudia/"
fake_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0232/fakes/mar9/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0232val/filelists/"

lumi_ = [36.06] 
lumi_val = 0

######## MC
## ttbro
ttbar = background.Background("ttbar", "t#bar{t}")
ttbar.set_debug()
ttbar.scale_factor = lumi_[lumi_val]#
ttbar.set_fillStyle(0)
ttbar.setLineStyle(1)
ttbar.set_color(r.kYellow) # stop-2l uglify for Moriond
#ttbar.set_color(r.kSpring-5)
#ttbar.set_color(r.TColor.GetColor("#e4706a"))
ttbar.set_treename("ttbar_powheg")
ttbar.set_chain_from_list_CONDOR(filelist_dir+ "ttbar/", rawdir)
backgrounds.append(ttbar)

#tt1 = background.Background("ttbarAMCHPP", "t#bar{t} (aMC@NLO + H++)")
#tt1.set_debug()
#tt1.scale_factor = lumi_[lumi_val]
#tt1.set_fillStyle(0)
#tt1.setLineStyle(1)
#tt1.set_color(r.TColor.GetColor("#e4706a"))
#tt1.set_treename("ttbar_amc_hpp")
#tt1.set_chain_from_list_CONDOR(filelist_dir + "ttbar_amc_hpp/", ttbar_amc_dir)
#backgrounds.append(tt1)

#tt2 = background.Background("ttbarAMCPythia", "t#bar{t} (aMC@NLO + Pythia)")
#tt2.set_debug()
#tt2.scale_factor = lumi_[lumi_val]
#tt2.set_fillStyle(0)
#tt2.setLineStyle(1)
#tt2.set_color(r.TColor.GetColor("#e4706a"))
#tt2.set_treename("ttbar_amc_hpp")
#tt2.set_chain_from_list_CONDOR(filelist_dir + "ttbar_amc_pythia8/", ttbar_amc_dir)
#backgrounds.append(tt2)

# singletop
stop = background.Background("st", "Wt")
stop.set_debug()
stop.scale_factor = lumi_[lumi_val]
stop.set_fillStyle(0)
stop.setLineStyle(1)
stop.set_color(r.kRed) # stop-2l uglify for Moriond
#stop.set_color(r.kYellow-7)
#stop.set_color(r.TColor.GetColor("#DE080C"))
#stop.set_color(r.TColor.GetColor("#db101c"))
stop.set_treename("ST")
stop.set_chain_from_list_CONDOR(filelist_dir+ "singletop/", rawdir)
backgrounds.append(stop)

# ttV
ttv = background.Background("ttV", "t#bar{t}+V")
ttv.set_debug()
ttv.scale_factor = lumi_[lumi_val]
ttv.set_fillStyle(0)
ttv.setLineStyle(1)
ttv.set_color(r.kBlue+1) # stop-2l uglify for Moriond
#ttv.set_color(r.kCyan-7)
#ttv.set_color(46)
#ttv.set_color(r.TColor.GetColor("#9bcdfd"))
ttv.set_treename("TTV")
ttv.set_chain_from_list_CONDOR(filelist_dir+ "ttV/", rawdir)
backgrounds.append(ttv)

###ttX
#ttx = background.Background("ttX", "t#bar{t} + H, 3/4 top, ttH")
#ttx.scale_factor = lumi_[lumi_val]
#ttx.set_fillStyle(0)
#ttx.setLineStyle(1)
#ttx.set_color(r.kViolet-4)
#ttx.set_treename("TTX")
#ttx.set_chain_from_list_CONDOR(filelist_dir + "ttX/", rawdir)
##backgrounds.append(ttx)

# diboson
diboson = background.Background("vvSF", "VV")
diboson.set_debug()
diboson.scale_factor = lumi_[lumi_val] #* 1.06
diboson.set_fillStyle(0)
diboson.setLineStyle(1)
diboson.set_color(r.kAzure+8) # stop-2l uglify for Moriond
#diboson.set_color(r.kAzure+6)
#diboson.set_color(r.TColor.GetColor("#41C1FC"))
#diboson.set_color(r.TColor.GetColor("#325f85"))
diboson.set_treename("diboson_sherpa_SF")
diboson.set_chain_from_list_CONDOR(filelist_dir+ "diboson_sherpa/", diboson_rawdir_SF)
#diboson.set_chain_from_list_CONDOR(filelist_dir+ "diboson_new_check/", diboson_rawdir_SF)
backgrounds.append(diboson)

###triboson
#triboson = background.Background("vvv", "VVV")
#triboson.scale_factor = lumi_[lumi_val]
#triboson.set_fillStyle(0)
#triboson.setLineStyle(1)
#triboson.set_color(r.kCyan+3)
#triboson.set_treename("triboson")
#triboson.set_chain_from_list_CONDOR(filelist_dir+"triboson/", rawdir)
#backgrounds.append(triboson)

# Zjets
zjets = background.Background("zjetsDY", "Z/#gamma*+jets")
zjets.set_debug()
zjets.scale_factor = lumi_[lumi_val]
zjets.set_fillStyle(0)
zjets.setLineStyle(1)
zjets.set_color(r.kSpring) # stop-2l uglify for Moriond
#zjets.set_color(93)
#zjets.set_color(r.TColor.GetColor("#FFEF53"))
#zjets.set_color(r.TColor.GetColor("#85dc6e"))
zjets.set_treename("zjets_sherpa")
zjets.set_chain_from_list_CONDOR(filelist_dir+ "zjets_and_DY/", zjets_rawdir)
#zjets.set_chain_from_list_CONDOR(filelist_dir+ "zjets_sherpa/", rawdir)
backgrounds.append(zjets)


# Wjets
#wjets = background.Background("wjets", "W+jets")
#wjets.set_debug()
#wjets.scale_factor = lumi_[lumi_val]
#wjets.set_fillStyle(0)
#wjets.setLineStyle(1)
##wjets.set_color(r.TColor.GetColor("#5E9AD6"))
#wjets.set_color(r.TColor.GetColor("#619bd3"))
#wjets.set_treename("wjets")
#wjets.set_chain_from_list_CONDOR(filelist_dir+ "wjets_sherpa/", rawdir)
#backgrounds.append(wjets)

## higgs
higgs = background.Background("higgs", "Others")
higgs.scale_factor = lumi_[lumi_val]
higgs.set_fillStyle(0)
higgs.setLineStyle(1)
higgs.set_color(r.kTeal+4) # stop-2l uglify for Moriond
#higgs.set_color(r.kGreen-9)
higgs.set_treename("higgs")
higgs.set_chain_from_list_CONDOR(filelist_dir+ "higgs/", rawdir)
backgrounds.append(higgs)


#drel = background.Background("drellyan", "Drell-Yan")
#drel.set_debug()
#drel.scale_factor = lumi_[lumi_val]
#drel.set_fillStyle(0)
#drel.setLineStyle(1)
##drel.set_color(r.kYellow)
#drel.set_color(r.TColor.GetColor("#feec60"))
#drel.set_treename("drellyan")
#drel.set_chain_from_list_CONDOR(filelist_dir+ "drellyan_sherpa/", rawdir)
#backgrounds.append(drel)

fakes = background.Background("fakes", "FNP")
fakes.scale_factor = 1.0 # Feb 7 2017 - fakes are full dataset, yo
#fakes.scale_factor = 2.95 # scale from 12.2/fb to 36/fb
fakes.set_treename("superNt")
#fakes.set_file(fake_rawdir + "physics_Main_276262_303560_FakesInclusive.root")
#fakes.set_file(fake_rawdir + "fakes_3body.root")
fakes.set_file(fake_rawdir + "fakes_3body_mar10_361ifb.root")
fakes.set_merged_tree("superNt")
fakes.set_color(94) # stop-2l uglify for Moriond
#fakes.set_color(r.kOrange+7)
fakes.set_fillStyle(0)
fakes.setLineStyle(1)
backgrounds.append(fakes)

#sig1 = background.Background("bwn250_160", "#tilde{t}_{1}#tilde{t}_{1}, m(#tilde{t}_{1}, #tilde{#chi}_{1}^{ 0}) = (250, 160) GeV")
##sig1 = background.Background("bwn250_160", "(250,160)")
#sig1.setSignal()
#sig1.set_debug()
#sig1.scale_factor = lumi_[lumi_val]
#sig1.set_fillStyle(0)
#sig1.setLineStyle(2)
#sig1.set_color(r.kBlue)
#sig1.set_treename("sig1")
#sig1.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", signal_rawdir, "389945")
#backgrounds.append(sig1)
#
#sig2 = background.Background("bwn300_180", "#tilde{t}_{1}#tilde{t}_{1}, m(#tilde{t}_{1}, #tilde{#chi}_{1}^{ 0}) = (300, 180) GeV")
##sig2 = background.Background("bwn300_180", "(300,180)")
#sig2.setSignal()
#sig2.set_debug()
#sig2.scale_factor = lumi_[lumi_val]
#sig2.setLineStyle(2)
#sig2.set_color(r.kGreen)
#sig2.set_treename("sig2")
#sig2.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", signal_rawdir, "389950")
#backgrounds.append(sig2)
#
#sig3 = background.Background("bwn300_150", "#tilde{t}_{1}#tilde{t}_{1}, m(#tilde{t}_{1}, #tilde{#chi}_{1}^{ 0}) = (300, 150) GeV")
##sig3 = background.Background("bwn300_150", "(300,150)")
#sig3.setSignal()
#sig3.set_debug()
#sig3.scale_factor = lumi_[lumi_val]
#sig3.setLineStyle(2)
#sig3.set_color(r.kBlack)
#sig3.set_treename("sig3")
#sig3.set_chain_from_list_CONDOR(filelist_dir + "bwn/", signal_rawdir, "389949")
#backgrounds.append(sig3)


#### DATA
data = background.Data()
data.set_color(r.kBlack)
data.set_treename("data")
data.set_chain_from_list_CONDOR(filelist_dir + "data/", data_rawdir)
#data.set_chain_from_list_CONDOR2([filelist_dir + "data15ToRun/", filelist_dir + "data16ToRun/"] , [data15_rawdir, data16_rawdir])


##########################################
# systematics
##########################################
systematics = []

#######################
### shape systematics
#######################
# e-gamma

syst = systematic.Systematic("EG_RESOLUTION_ALL", "UP", "DN")
syst.setKinSys()
systematics.append(syst)

syst = systematic.Systematic("EG_SCALE_ALL", "UP", "DN")
syst.setKinSys()
systematics.append(syst)

## muons
#syst = systematic.Systematic("MUON_ID", "UP", "DN")
#syst.setKinSys()
#systematics.append(syst)
#
#syst = systematic.Systematic("MUON_MS", "UP", "DN")
#syst.setKinSys()
#systematics.append(syst)
#
#syst = systematic.Systematic("MUON_SCALE", "UP", "DN")
#syst.setKinSys()
#systematics.append(syst)
# jets

syst = systematic.Systematic("JET_GroupedNP_1", "UP", "DN")
syst.setKinSys()
systematics.append(syst)

syst = systematic.Systematic("JET_GroupedNP_2", "UP", "DN")
syst.setKinSys()
systematics.append(syst)

syst = systematic.Systematic("JET_GroupedNP_3", "UP", "DN")
syst.setKinSys()
systematics.append(syst)

syst = systematic.Systematic("JER", "", "")
syst.setKinSys()
syst.setOneSided()
systematics.append(syst)
## met
#syst = systematic.Systematic("MET_SoftTrk_ResoPara", "", "")
#syst.setOneSided()
#syst.setKinSys()
#systematics.append(syst)
#
#syst = systematic.Systematic("MET_SoftTrk_ResoPerp", "", "")
#syst.setOneSided()
#syst.setKinSys()
#systematics.append(syst)
#
#syst = systematic.Systematic("MET_SoftTrk_Scale", "Up", "Down")
#syst.setKinSys()
#systematics.append(syst)



######################
### weight systematics
######################


syst = systematic.Systematic("PILEUP", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)

# e-gamma
syst = systematic.Systematic("EL_EFF_ID", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)

#syst = systematic.Systematic("EL_EFF_Iso", "UP", "DOWN")
#syst.setWeightSys()
#systematics.append(syst)
#
#syst = systematic.Systematic("EL_EFF_Reco", "UP", "DOWN")
#syst.setWeightSys()
#systematics.append(syst)

# muons
#syst = systematic.Systematic("MUON_EFF_STAT", "UP", "DOWN")
#syst.setWeightSys()
#systematics.append(syst)
#
#syst = systematic.Systematic("MUON_EFF_STAT_LOWPT", "UP", "DOWN")
#syst.setWeightSys()
#systematics.append(syst)
#
#syst = systematic.Systematic("MUON_EFF_SYS", "UP", "DOWN")
#syst.setWeightSys()
#systematics.append(syst)
#
#syst = systematic.Systematic("MUON_EFF_SYS_LOWPT", "UP", "DOWN")
#syst.setWeightSys()
#systematics.append(syst)
#
#syst = systematic.Systematic("MUON_ISO_STAT", "UP", "DOWN")
#syst.setWeightSys()
#systematics.append(syst)
#
#syst = systematic.Systematic("MUON_ISO_SYS", "UP", "DOWN")
#syst.setWeightSys()
#systematics.append(syst)
#
# jets
syst = systematic.Systematic("JET_JVTEff", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)
##
# flavor tagging
syst = systematic.Systematic("FT_EFF_B", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)

#syst = systematic.Systematic("FT_EFF_C", "UP", "DOWN")
#syst.setWeightSys()
#systematics.append(syst)

syst = systematic.Systematic("FT_EFF_Light", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)
#
#syst = systematic.Systematic("FT_EFF_extrapolation", "UP", "DOWN")
#syst.setWeightSys()
#systematics.append(syst)
#
#syst = systematic.Systematic("FT_EFF_extrapolation_charm", "UP", "DOWN")
#syst.setWeightSys()
#systematics.append(syst)

##########################################
# regions
##########################################
regions = []

#isEE = "(nElectrons==2 && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0"
#isMM = "(nMuons==2 && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0"
#isDF = "(nElectrons==1 && nMuons==1) && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"
#inZ = ("((nMuons==2 || nElectrons==2) && abs(mll-91.2)<10)")
isEE = "(nElectrons==2 && abs(mll-91.2)>20) && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"
isMM = "(nMuons==2 && abs(mll-91.2)>20) && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"


isSFOS = "(( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && abs(mll-91.2)>20 && (l_q[0]*l_q[1])<0)"
isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<0"

trigger = "((year==2015 && trig_pass2015==1) || (year==2016 && trig_pass2016update==1))"

reg = region.Region()
reg.name = "srwSF"
reg.displayname = "SRw SF (n-1 RPT)"
sr_w_def = "nBJets==0  && gamInvRp1>0.7 && MDR>95 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger
reg.tcut = isSFOS + " && " + sr_w_def
regions.append(reg)

reg = region.Region()
reg.name = "srwDF"
reg.displayname = "SRw DF (n-1 RPT)"
sr_w_def = "nBJets==0  && MDR>95 && gamInvRp1>0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger
reg.tcut = isDFOS + " && " + sr_w_def
regions.append(reg)


reg = region.Region()
reg.name = "srwSFpre"
reg.displayname = "SRw SF (pre)"
sr_w_def_pre = "nBJets==0 && gamInvRp1>0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && MDR>95 && mll>20 && " + trigger
reg.tcut = isSFOS + " && " + sr_w_def_pre
regions.append(reg)


reg = region.Region()
reg.name = "dfprebGam" 
reg.displayname = "DF Preselection + >0 b-jets"
reg.tcut = "nLeptons==2 && " + isDFOS + " && nBJets>0 && mll>20 && MDR>95 && " + trigger
regions.append(reg)

reg = region.Region()
reg.name = "dfprebvGam"
reg.displayname = "DF Preselection + b-veto"
reg.tcut = "nLeptons==2 && " + isDFOS + " && nBJets==0 && mll>20 && MDR>95  && " + trigger
regions.append(reg)


reg = region.Region()
reg.name = "dfprebv"
reg.displayname = "DF Preselection + b-veto"
reg.tcut = "nLeptons==2 && " + isDFOS + " && nBJets==0 && mll>20 && " + trigger 
regions.append(reg)

reg = region.Region()
reg.name = "sfprebv"
reg.displayname = "SF Preselection + b-veto"
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
#reg.displayname = "DF Presel. + >=3 b-jets"
reg.displayname = "DF Preselection + >0 b-jets"
reg.tcut = "nLeptons==2 && " + isDFOS + " && nBJets>0 && mll>20  && " + trigger
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



reg = region.Region()
reg.name = "crv17"

reg.displayname = "CR_{VV-DF}^{3-body}"
reg.tcut = isDFOS + " && nBJets==0 && MDR>50 && DPB_vSS<(0.9*abs(cosThetaB)+1.6) && RPT<0.5  && gamInvRp1>0.7 && mll>20 && " + trigger
#reg.tcut = isDFOS + " && nBJets==0 && MDR>30 && DPB_vSS<(0.9*abs(cosThetaB)+1.6) && RPT<0.7  && gamInvRp1>0.77 && mll>20 && " + trigger
regions.append(reg)


reg = region.Region()
reg.name = "crvSF17"
reg.displayname = "CR_{VV-SF}^{3-body}"
reg.tcut = isSFOS + " && nBJets==0 && MDR>70 && DPB_vSS<(0.9*abs(cosThetaB)+1.6) && RPT<0.5 && gamInvRp1>0.7 && mll>20 && " + trigger
regions.append(reg)

reg = region.Region()
reg.name = "vrv17"
reg.displayname = "VR-VV-DF"
reg.tcut = isDFOS + " && nBJets==0 && MDR>50 && MDR<95 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && RPT<0.7 && gamInvRp1>0.7 && mll>20 && " + trigger
#reg.tcut = isDFOS + " && nBJets==0 && MDR>30 && MDR<80 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && RPT<0.7 && gamInvRp1>0.7 && mll>20 && " + trigger
regions.append(reg)

reg = region.Region()
reg.name = "vrvSF17"
reg.displayname = "VR-VV-SF"
reg.tcut = isSFOS + " && nBJets==0 && MDR>60 && MDR<95 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && RPT<0.4 && gamInvRp1>0.7 && mll>20 && " + trigger
regions.append(reg)

reg = region.Region()
reg.name = "crt17"
reg.displayname = "CR_{t#bar{t}}^{3-body}"
reg.tcut = isDFOS + " && nBJets>0 && MDR>80 && RPT>0.7 && DPB_vSS<(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger
regions.append(reg)

reg = region.Region()
reg.name = "vrt17"
reg.displayname = "VR-Top"
reg.tcut = isDFOS + " && nBJets==0 && MDR>95 && RPT<0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger
#reg.tcut = isDFOS + " && nBJets==0 && MDR>80 && RPT<0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger
regions.append(reg)

reg = region.Region()
reg.name = "vrtSF17"
reg.displayname = "VR-Top-SF"
reg.tcut = isSFOS + " && nBJets==0 && MDR>80 && RPT<0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger
regions.append(reg)

reg = region.Region()
reg.name = "vrtB17"
reg.displayname = "VR-Top-B"
reg.tcut = isDFOS + " && nBJets>0 && MDR>60 && MDR<95 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && RPT<0.4 && gamInvRp1>0.7 && mll>20 && " + trigger
regions.append(reg)




##########################################
# plots
##########################################
plots = []


vars = {}
vars["l_pt[0]"]         = { "dfprebv" : [40, 25,500,1e9],     "dfpreb" : [40, 25,500,1e9],    "crt17" : [30, 25, 600, 1e5], "vrt17"  : [20,25,300, 375],
#vars["l_pt[0]"]         = { "dfprebv" : [40, 25,500,1e9],     "dfpreb" : [40, 25,500,1e9],    "crt17" : [30, 25, 600, 1e5], "vrtSF17"  : [20,25,300, 375],
                            "srwSF" : [10,0,100,10],
                            "sfprebv" : [40, 25,400,1e10],    "sfpreb" : [40, 25,500,1e10],
                            "sfprebvEE" : [40, 25,400,1e10],    "sfprebEE" : [40, 25,500,1e10],
                            "sfprebvMM" : [40, 25,400,1e10],    "sfprebMM" : [40, 25,500,1e10],
                            "crv17"     : [10, 25, 100, 900],   "crvSF17"  : [15, 25, 105, 800 ], "vrv17" : [5,25,70, 200],     "vrvSF17" : [10,25,70,140]}
                            #"crv17"     : [10, 25, 100, 900],   "crvSF17"  : [15, 25, 105, 800 ], "vrv17" : [5,25,70, 200],     "vrtB17" : [10,25,120,140]}
                            #"crv17"     : [10, 25, 100, 900],   "crvSF17"  : [15, 25, 105, 800 ], "vrv17" : [5,25,70, 200],     "vrtB17" : [10,25,70,140]}

vars["l_pt[1]"]         = { "dfprebv" : [40,20,500, 1e9],     "dfpreb" : [40,20,500, 1e9],    "crt17" : [10, 20, 200, 7e5], "vrt17"   : [10,20,130, 375],
#vars["l_pt[1]"]         = { "dfprebv" : [40,20,500, 1e9],     "dfpreb" : [40,20,500, 1e9],    "crt17" : [10, 20, 200, 7e5], "vrtSF17"   : [10,20,130, 375],
                            "srwSF" : [10,0,100,10],
                            "sfprebv" : [40,20,500,1e10],     "sfpreb" : [40,20,400,1e10],
                            "sfprebvEE" : [40,20,500,1e10],     "sfprebEE" : [40,20,400,1e10],
                            "sfprebvMM" : [40,20,500,1e10],     "sfprebMM" : [40,20,400,1e10],
                            "crv17"     : [4, 20, 60, 700],     "crvSF17" :  [8, 20, 70, 600 ],   "vrv17" : [2,20,40, 220],      "vrvSF17" : [4,20,40, 120]}
                            #"crv17"     : [4, 20, 60, 700],     "crvSF17" :  [8, 20, 70, 600 ],   "vrv17" : [2,20,40, 220],      "vrtB17" : [8,20,100, 120]}
                            #"crv17"     : [4, 20, 60, 700],     "crvSF17" :  [8, 20, 70, 600 ],   "vrv17" : [2,20,40, 220],      "vrtB17" : [4,20,40, 120]}

vars["MDR" ]            = { "dfprebv" : [20,0,200, 1e9],      "dfpreb" : [10,0,200, 1e9],     "crt17" : [ 5, 80,200, 7e5],  "vrt17"   : [5,80,135, 500],
#vars["MDR" ]            = { "dfprebv" : [10,0,200, 1e9],      "dfpreb" : [10,0,200, 1e9],     "crt17" : [ 5, 80,200, 7e5],  "vrtSF17"   : [5,80,135, 500],
                            "srwDF" : [10,0,200,10],
                            "sfprebv" : [10,0,200,1e10],      "sfpreb" : [10,0,200,1e10],
                            "sfprebvEE" : [10,0,200,1e10],      "sfprebEE" : [10,0,200,1e10],
                            "sfprebvMM" : [10,0,200,1e10],      "sfprebMM" : [10,0,200,1e10],
                            "crv17"     : [10,  50, 140, 800],  "crvSF17"  : [5, 70, 100, 950 ], "vrv17" : [10,50,95,    300],  "vrvSF17" : [5,60,100, 180]}
                            #"crv17"     : [10,  50, 140, 800],  "crvSF17"  : [10, 70, 150, 650 ], "vrv17" : [10,50,95,    300],  "vrtB17" : [5,60,100, 180]}
vars["DPB_vSS"]         = { "dfprebv" : [0.2,0,3.2, 1e9],     "dfpreb" : [0.2,0,3.2, 1e9],    "crt17" : [0.2, 0, 2.8, 5e4], "vrt17"   : [0.2,1.8,3.2, 380],
#vars["DPB_vSS"]         = { "dfprebv" : [0.2,0,3.2, 1e9],     "dfpreb" : [0.2,0,3.2, 1e9],    "crt17" : [0.1, 0, 2.8, 7e5], "vrtSF17"   : [0.2,1.8,3.2, 380],
                            "srwSF" : [0.05,1.5,3.2,10],
                            "sfprebv" : [0.2,0,3.2,1e10],      "sfpreb" : [0.2,0,3.2,1e10],
                            "sfprebvEE" : [0.2,0,3.2,1e10],      "sfprebEE" : [0.2,0,3.2,1e10],
                            "sfprebvMM" : [0.2,0,3.2,1e10],      "sfprebMM" : [0.2,0,3.2,1e10],
                            "crv17"     : [0.5, 0, 2.8, 720],   "crvSF17"  : [0.5, 0, 2.8, 500],  "vrv17" : [0.2,1.8,3.2, 200],  "vrvSF17" : [0.2,1.8,3.2, 120]}
                            #"crv17"     : [0.5, 0, 2.8, 720],   "crvSF17"  : [0.5, 0, 2.8, 500],  "vrv17" : [0.2,1.8,3.2, 200],  "vrtB17" : [0.2,1.8,3.2, 120]}

vars["gamInvRp1"]       = { "dfprebv" : [0.05,0,1, 1e9],     "dfpreb"  : [0.05,0,1, 1e9],     "crt17" : [0.1, 0, 1, 7e5],  "vrt17"   : [0.1,0,1, 280],
#vars["gamInvRp1"]       = { "dfprebv" : [0.05,0,1, 1e9],     "dfpreb"  : [0.05,0,1, 1e9],     "crt17" : [0.1, 0, 1, 7e5],  "vrtSF17"   : [0.1,0,1, 280],
                            "srwDF" : [0.1,0,1,10],
                            "sfprebv" : [0.05,0,1,1e10],     "sfpreb"  : [0.05,0,1,1e10],
                            "sfprebvEE" : [0.05,0,1,1e10],     "sfprebEE"  : [0.05,0,1,1e10],
                            "sfprebvMM" : [0.05,0,1,1e10],     "sfprebMM"  : [0.05,0,1,1e10],
                            "crv17"     : [0.02, 0.7, 1, 400], "crvSF17"   : [0.04, 0.7, 1, 550 ], "vrv17" : [0.05,0.7,1, 320],  "vrvSF17" : [0.05,0.7,1, 150],
                            #"crv17"     : [0.02, 0.7, 1, 400], "crvSF17"   : [0.04, 0.7, 1, 550 ], "vrv17" : [0.05,0.7,1, 320],  "vrtB17" : [0.05,0.7,1, 150],
                            "dfprebvGam" : [0.05,0,1,500], "dfprebGam" : [0.05,0,1,500] }

vars["abs(cosThetaB)"]  = { "dfprebv" : [0.05,0,1, 1e9],     "dfpreb"  : [0.05,0,1, 1e9], "crt17" : [0.05, 0, 1, 7e5],     "vrt17" : [0.1,0,1, 240],
#vars["abs(cosThetaB)"]  = { "dfprebv" : [0.05,0,1, 1e9],     "dfpreb"  : [0.05,0,1, 1e9], "crt17" : [0.05, 0, 1, 7e5],     "vrtSF17" : [0.1,0,1, 240],
                            "srwSF" : [0.02,0,1,10],
                            "sfprebv" : [0.05,0,1,1e10],     "sfpreb"  : [0.05,0,1,1e10],
                            "sfprebvEE" : [0.05,0,1,1e10],     "sfprebEE"  : [0.05,0,1,1e10],
                            "sfprebvMM" : [0.05,0,1,1e10],     "sfprebMM"  : [0.05,0,1,1e10],
                            "crv17" : [0.15, 0, 1,800],       "crvSF17"   : [0.2, 0, 1, 375 ], "vrv17" : [0.2,0,1, 300], "vrvSF17" : [0.2,0,1, 120]}
                            #"crv17" : [0.15, 0, 1, 575],       "crvSF17"   : [0.2, 0, 1, 375 ], "vrv17" : [0.2,0,1, 300], "vrtB17" : [0.2,0,1, 120]}

vars["RPT"]             = { "dfprebv" : [0.05,0,1, 1e9], "dfpreb" : [0.05,0,1, 1e9], "crt17"    : [0.02, 0.7, 1, 5e4], "vrt17" : [0.05,0,0.7,400],
#vars["RPT"]             = { "dfprebv" : [0.05,0,1, 1e9], "dfpreb" : [0.05,0,1, 1e9], "crt17"    : [0.02, 0.7, 1, 7e5], "vrtSF17" : [0.05,0,0.7,400],
                            "srwSF" : [0.1,0,1,10],
                            "sfprebv" : [0.05,0,1,1e10], "sfpreb" : [0.05,0,1,1e10],
                            "sfprebvEE" : [0.05,0,1,1e10], "sfprebEE" : [0.05,0,1,1e10],
                            "sfprebvMM" : [0.05,0,1,1e10], "sfprebMM" : [0.05,0,1,1e10],
                            #"crv17" : [0.05, 0, 0.5, 1000],  "crvSF17"  : [0.05, 0, 0.5, 600], "vrv17" : [0.1,0,0.7,240],    "vrvSF17" : [0.1,0,0.4, 150]}
                            "crv17" : [0.05, 0, 0.5, 1000],  "crvSF17"  : [0.05, 0, 0.5, 600], "vrv17" : [0.1,0,0.7,240],    "vrvSF17" : [0.1,0,0.4, 150],
                            "dfprebvGam" : [0.05, 0, 1, 1e9], "dfprebGam" : [0.05, 0, 1, 500],
                            "srwSFpre" : [0.1, 0, 1, 1e9] }
                            #"crv17" : [0.05, 0, 0.5, 1000],  "crvSF17"  : [0.05, 0, 0.5, 600], "vrv17" : [0.1,0,0.7,240],    "vrtB17" : [0.1,0,0.4, 150]}
vars["nSJets"]          = { "dfprebv" : [1, 0,15, 1e9], "dfpreb" : [1, 0,15, 1e9], "crt17" : [1, 0, 12, 7e5], "vrt17" : [1,0,10, 380],
                            "srwSF" : [1,0,10,10],
                            "sfprebv" : [1,0,15,1e10],  "sfpreb" : [1,0,15,1e10],
                            "sfprebvEE" : [1,0,15,1e10],  "sfprebEE" : [1,0,15,1e10],
                            "sfprebvMM" : [1,0,15,1e10],  "sfprebMM" : [1,0,15,1e10],
                            "crv17" : [1, 0, 7, 1500],     "crvSF17" : [1, 0, 7, 600],  "vrv17" : [1,0,7, 400],     "vrvSF17" : [1,0,7, 180]}
                            #"crv17" : [1, 0, 7, 1500],     "crvSF17" : [1, 0, 7, 600],  "vrv17" : [1,0,7, 400],     "vrtB17" : [1,0,7, 180]}

vars["nBJets"]          = { "dfprebv" : [1, 0,3, 1e9], "dfpreb" : [1, 0,6, 1e9], "crt17"  : [1, 0, 10, 7e5], "vrt17" : [1,0,3, 1500],
#vars["nBJets"]          = { "dfprebv" : [1, 0,3, 1e9], "dfpreb" : [1, 0,6, 1e9], "crt17"  : [1, 0, 10, 7e5], "vrtSF17" : [1,0,3, 1500],
                            "srwSF" : [1,0,10,10],
                            "sfprebv" : [1,0,3,1e10],  "sfpreb" : [1,0,6,1e10],
                            "sfprebvEE" : [1,0,3,1e10],  "sfprebEE" : [1,0,6,1e10],
                            "sfprebvMM" : [1,0,3,1e10],  "sfprebMM" : [1,0,6,1e10],
                            "crv17" : [1, 0, 3, 3000], "crvSF17"     : [1, 0, 3, 1600], "vrv17" : [1,0,3, 750], "vrvSF17"  : [1,0,3, 320]}
                            #"crv17" : [1, 0, 3, 3000], "crvSF17"     : [1, 0, 3, 1600], "vrv17" : [1,0,3, 750], "vrtB17"  : [1,0,6, 320]}
                            #"crv17" : [1, 0, 3, 3000], "crvSF17"     : [1, 0, 3, 1600], "vrv17" : [1,0,3, 750], "vrtB17"  : [1,0,3, 320]}

vars["met"]             = { "dfprebv" : [30,0,500, 1e9], "dfpreb" : [30,0,500, 1e9], "crt17" : [30,0,460, 7e5], "vrt17" : [20,40,280, 370],
#vars["met"]             = { "dfprebv" : [30,0,500, 1e9], "dfpreb" : [30,0,500, 1e9], "crt17" : [30,0,460, 7e5], "vrtSF17" : [20,40,280, 370],
                            "srwSF" : [10,0,200,10],
                            "sfprebv" : [30,0,500,1e10], "sfpreb" : [30,0,500,1e10],
                            "sfprebvEE" : [30,0,500,1e10], "sfprebEE" : [30,0,500,1e10],
                            "sfprebvMM" : [30,0,500,1e10], "sfprebMM" : [30,0,500,1e10],
                            "crv17" : [10, 30, 120, 720], "crvSF17"   : [10, 50, 150,  950 ], "vrv17" : [10,40,130, 22], "vrvSF17" : [5,50,120, 130]}
                            #"crv17" : [10, 30, 120, 720], "crvSF17"   : [10, 50, 150,  950 ], "vrv17" : [10,40,130, 22], "vrtB17" : [5,50,120, 130]}

vars["DPB_vSS - 0.9*abs(cosThetaB)"] = { "dfpreb" : [0.5, -1.5, 4, 1e9], "dfprebv" : [0.5, -1.5, 4.0, 1e9],
                            "srwSF" : [0.2,1.6,3,10],
                                          "sfpreb" : [0.5, -1.5, 4, 1e10],  "sfprebv" : [0.5, -1.5, 4, 1e10],
                                          "crt17" : [0.2, -1.2, 1.8, 7e5], "vrt17" : [0.2, 1.6, 3.4, 380],
                                          #"crt17" : [0.2, -1.2, 1.8, 7e5], "vrtSF17" : [0.2, 1.6, 3.4, 380],
                                          "crv17" : [0.2, -1, 1.8, 350], "vrv17" : [0.2, 1.6, 3.4, 200],
                                          "crvSF17" : [0.2, -1.2, 1.8, 400], "vrvSF17" : [0.2, 1.6, 3.2, 140]  }
                                          #"crvSF17" : [0.2, -1.2, 1.8, 400], "vrtB17" : [0.2, 1.6, 3.2, 140]  }

#vars["avgMu"] = {       "dfpreb" : [1,0,45,1e10],"dfprebv" : [1,0,45,1e10],"sfpreb" : [1,0,45,1e10],"sfprebv" : [1,0,45,1e10] }
#vars["avgMuDataSF"] = { "dfpreb" : [1,0,45,1e10],"dfprebv" : [1,0,45,1e10],"sfpreb" : [1,0,45,1e10],"sfprebv" : [1,0,45,1e10] }

#vars["abs(dphi_j0_ll)"]  = { "dfpreb" : [0.16, 0, 3.2, 1e9], "crt" : [0.16, 0, 3.2, 1e9], "vrt" : [0.16,0,3.2,1e9] }
#vars["abs(dphi_j0_l0)"]  = { "dfpreb" : [0.16, 0, 3.2, 1e9], "crt" : [0.16, 0, 3.2, 1e9], "vrt" : [0.16,0,3.2,1e9] }
#vars["abs(dphi_sj0_ll)"] = { "dfpreb" : [0.16, 0, 3.2, 1e9], "crt" : [0.16, 0, 3.2, 1e9], "vrt" : [0.16,0,3.2,1e9] }
#vars["abs(dphi_sj0_l0)"] = { "dfpreb" : [0.16, 0, 3.2, 1e9], "crt" : [0.16, 0, 3.2, 1e9], "vrt" : [0.16,0,3.2,1e9] }
#vars["abs(dphi_bj0_ll)"] = { "dfpreb" : [0.16, 0, 3.2, 1e9], "crt" : [0.16, 0, 3.2, 1e9], "vrt" : [0.16,0,3.2,1e9] }
#vars["abs(dphi_bj0_l0)"] = { "dfpreb" : [0.16, 0, 3.2, 1e9], "crt" : [0.16, 0, 3.2, 1e9], "vrt" : [0.16,0,3.2,1e9] }

#vars["bj_pt[0]"] = { "dfpreb" : [10, 0, 450, 1e9] }
#vars["bj_pt[1]"] = { "dfpreb" : [10, 0, 350, 1e9] }
#vars["bj_pt[2]"] = { "dfpreb" : [10, 0, 220, 1e9] }
#vars["bj_pt[3]"] = { "dfpreb" : [10, 0, 220, 1e9] }
#vars["bj_pt[4]"] = { "dfpreb" : [10, 0, 220, 1e9] }
#vars["bj_pt[5]"] = { "dfpreb" : [10, 0, 220, 1e9] }
#
#
#vars["mll"]             = { "crvSF17" : [10, 20, 250,1e7], "sfpreb" : [10,0,300,1e7],   "sfprebv" : [10,0,300,1e7],   "crt" : [10,0,120,1e4],
#                            "vrv" : [5, 20, 60, 30], "crv" : [5, 20, 70, 60], "crvSF" : [8, 20, 80, 40] , "vrvSF" : [5, 20, 60, 25],
#                            "dfprebGam" : [10, 0, 150, 1e7], "dfprebvGam" : [10, 0, 300, 1e7] }
#vars["nVtx"]            = { "dfpreb" : [1,0,42,1e9], "dfprebv" : [1,0,44,1e7], "sfpreb" : [1,0,42,1e9], "sfprebv" : [1,0,44,1e7] }
#vars["avgMu"] = {       "dfpreb" : [1,0,45,1e10],"dfprebv" : [1,0,45,1e10],"sfpreb" : [1,0,45,1e10],"sfprebv" : [1,0,45,1e10] }
#vars["avgMuDataSF"] = { "dfpreb" : [1,0,45,1e10],"dfprebv" : [1,0,45,1e10],"sfpreb" : [1,0,45,1e10],"sfprebv" : [1,0,45,1e10] }

#vars["nVtx"]    = { "dfpreb" : [1,0,38,1e9], "dfprebv" : [1,0,40,1e9], "sfpreb" : [1,0,40,1e10], "sfprebv" : [1,0,40,1e10], "crt" : [1,0,40,1e9] }
#vars["avgMu"]   = { "dfpreb" : [1,0,45,1e9], "dfprebv" : [1,0,45,1e9], "sfpreb" : [1,0,45,1e10], "sfprebv" : [1,0,45,1e10], "crt" : [1,0,45,1e9] }
#vars["metTST"]  = { "dfpreb" : [5,0,100,1e9], "dfprebv" : [5,0,100,1e9], "sfpreb" : [5,0,100,1e10], "sfprebv" : [5,0,100,1e10], "crt" : [5,0,100,1e9] }



#vars["Mtt"] =   { "ttrj" : [100, 0, 2800, 4000] }
#vars["pT_TT"] = { "ttrj" : [ 10, 0, 200,  10000] }
#vars["Mt"] =    { "ttrj" : [ 12, 0, 400,  3500] }
#vars["Eb_Ta"] = { "ttrj" : [ 10, 0, 250, 4000] }
#vars["M_top"] = { "ttrj" : [8, 0, 400,   3000] }
#vars["E_bl"] =  { "ttrj" : [10, 0, 350,  3200] }
##vars["Mtt"] =   { "ttrj" : [100, 0, 2800, 3.8e4] }
##vars["pT_TT"] = { "ttrj" : [ 10, 0, 200, 8.5e4] }
##vars["Mt"] =    { "ttrj" : [ 12, 0, 400, 4.5e4] }
##vars["Eb_Ta"] = { "ttrj" : [ 10, 0, 250, 4.2e4] }
##vars["M_top"] = { "ttrj" : [8, 0, 400,  4.5e4] }
##vars["E_bl"] =  { "ttrj" : [10, 0, 350,  2.5e4] }



vars_tmp = {}
vars_tmp["MDR"] = vars["MDR"]
#vars_tmp["gamInvRp1"] = vars["gamInvRp1"]
#vars_tmp["RPT"] = vars["RPT"]
#vars_tmp["DPB_vSS"] = vars["DPB_vSS"]
#vars_tmp["abs(cosThetaB)"] = vars["abs(cosThetaB)"]
vars = vars_tmp



run_reg = "crvSF17"

nice_names = {}
nice_names["MDR"] = "M_{#Delta}^{R} [GeV]"
nice_names["DPB_vSS"] = "#Delta#phi_{#beta}^{R}"
nice_names["met"] = "E_{T}^{miss} [GeV]"
nice_names["gamInvRp1"] = "1/#gamma_{R+1}"
nice_names["abs(cosThetaB)"] = "|cos#theta_{b}|"
nice_names["RPT"] = "R_{p_{T}}"
nice_names["DPB_vSS - 0.9*abs(cosThetaB)"] = "#Delta#phi_{#beta}^{R} - 0.9#times|cos#theta_{b}|" 
nice_names["Mtt"] = "m_{t#bar{t}} [GeV]"
nice_names["pT_TT"] = "p_{T}^{t#bar{t}} [GeV]"
nice_names["Mt"] = "m_{t} [GeV]"
nice_names["Eb_Ta"] = "E_{b}^{t-frame} [GeV]"
nice_names["M_top"] = "M_top [GeV]"
nice_names["E_bl"] = "E_{bl} [GeV]"
nice_names["metTST"] = "met soft term [GeV]"



nice_names["abs(dphi_j0_ll)"]  = "|#Delta#phi(lead jet, dilepton system)|" 
nice_names["abs(dphi_j0_l0)"]  = "|#Delta#phi(lead jet, lead lepton)|" 
nice_names["abs(dphi_sj0_ll)"] = "|#Delta#phi(lead non-b jet, dilepton system)|"
nice_names["abs(dphi_sj0_l0)"] = "|#Delta#phi(lead non-b jet, lead lepton)|"
nice_names["abs(dphi_bj0_ll)"] = "|#Delta#phi(lead b-jet, dilepton system)|"
nice_names["abs(dphi_bj0_l0)"] = "|#Delta#phi(lead b-jet, lead lepton)|"


#nice_names["MDR"] = "E_{V}^{P} [GeV]"
#nice_names["DPB_vSS"] = "#Delta#phi(#vec{#beta}_{PP}^{LAB}, #vec{p}_{V}^{PP})"
#nice_names["met"] = "E_{T}^{miss} [GeV]"
#nice_names["gamInvRp1"] = "1/#gamma_{P}^{PP}"
#nice_names["abs(cosThetaB)"] = "|cos#theta_{b}|"
#nice_names["RPT"] = "R_{p_{T}}"
nice_names["nBJets"] = "b-Jet Multiplicity"
nice_names["nSJets"] = "Signal Jet Multiplicity"
nice_names["l_pt[0]"] = "Leading lepton p_{T} [GeV]"
nice_names["l_pt[1]"] = "Sub-leading lepton p_{T} [GeV]"
nice_names["l_eta[0]"] = "Leading lepton #eta"
nice_names["l_eta[1]"] = "Sub-leading lepton #eta"
nice_names["bj_pt[0]"] = "bjpt0"
nice_names["bj_pt[1]"] = "bjpt1"
nice_names["bj_pt[2]"] = "bjpt2"
nice_names["bj_pt[3]"] = "bjpt3"
nice_names["bj_pt[4]"] = "bjpt4"
nice_names["bj_pt[5]"] = "bjpt5"
nice_names["bj_pt[6]"] = "bjpt6"
nice_names["avgMu"] = "<#mu>"
nice_names["avgMuDataSF"] = "<#mu>_{SF}"
nice_names["nVtx"] = "Num. Primary Vertices"
nice_names["mll"] = "Dilepton Invariant Mass [GeV]"

for var, bounds in vars.iteritems() :
    p = plot.Plot1D()
    name_ = ""
    if "abs(" in var and "DPB_vSS" not in var :
        name_ = var.replace("abs(","")
        name_ = name_.replace(")", "")
    elif "[" in var :
        name_ = var.replace("[","")
        name_ = name_.replace("]","")
    elif var=="DPB_vSS - 0.9*abs(cosThetaB)" :
        name_ = "DPB_minus_COSB"
    else :
        name_ = var
    p.initialize(run_reg, var, "%s_%s"%(run_reg, name_))
    ylabel_unit = ""
    gev_variables = ["MDR", "met", "l_pt[0]", "l_pt[1]", "mll"]
    if var in gev_variables :
        ylabel_unit = " GeV"
    ylabel_title = str(bounds[run_reg][0]) + ylabel_unit
    p.labels(x=nice_names[var], y = "Events / %s"%(str(ylabel_title)))
    #p.labels(x=nice_names[var], y = "Entries / %s"%(str(bounds[run_reg][0])))
    p.xax(bounds[run_reg][0], bounds[run_reg][1], bounds[run_reg][2])
    if "crt" in run_reg or "dfpre" in run_reg or "sfcr" in run_reg or "checkSF" in run_reg or "sfpre" in run_reg : #or "crv" in run_reg or "vrv" in run_reg:
        p.doLogY = True
        if len(bounds[run_reg]) == 4 :
            p.yax(0.1, bounds[run_reg][3])
        else :
            p.yax(0.1, 1e7)
    else :
        p.doLogY = False
        if len(bounds[run_reg]) == 4 :
            p.yax(0, bounds[run_reg][3])
        else :
            p.yax(0, 5000)
    p.setRatioCanvas(p.name)
    plots.append(p)
