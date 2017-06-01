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
diboson = background.Background("vvDF", "VV")
diboson.set_debug()
diboson.scale_factor = lumi_[lumi_val] #* 1.06
diboson.set_fillStyle(0)
diboson.setLineStyle(1)
diboson.set_color(r.kAzure+8) # stop-2l uglify for Moriond
#diboson.set_color(r.kAzure+6)
#diboson.set_color(r.TColor.GetColor("#41C1FC"))
#diboson.set_color(r.TColor.GetColor("#325f85"))
diboson.set_treename("diboson_sherpa_DF")
diboson.set_chain_from_list_CONDOR(filelist_dir+ "diboson_sherpa/", diboson_rawdir_DF)
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

sig1 = background.Background("bwn250_160", "#tilde{t}_{1}#tilde{t}_{1}, m(#tilde{t}_{1}, #tilde{#chi}_{1}^{ 0}) = (250, 160) GeV")
#sig1 = background.Background("bwn250_160", "(250,160)")
sig1.setSignal()
sig1.set_debug()
sig1.scale_factor = lumi_[lumi_val]
sig1.set_fillStyle(0)
sig1.setLineStyle(2)
sig1.set_color(r.kBlue)
sig1.set_treename("sig1")
sig1.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", rawdir, "389945")
backgrounds.append(sig1)

sig2 = background.Background("bwn300_180", "#tilde{t}_{1}#tilde{t}_{1}, m(#tilde{t}_{1}, #tilde{#chi}_{1}^{ 0}) = (300, 180) GeV")
#sig2 = background.Background("bwn300_180", "(300,180)")
sig2.setSignal()
sig2.set_debug()
sig2.scale_factor = lumi_[lumi_val]
sig2.setLineStyle(2)
sig2.set_color(r.kGreen)
sig2.set_treename("sig2")
sig2.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", rawdir, "389950")
backgrounds.append(sig2)

sig3 = background.Background("bwn300_150", "#tilde{t}_{1}#tilde{t}_{1}, m(#tilde{t}_{1}, #tilde{#chi}_{1}^{ 0}) = (300, 150) GeV")
#sig3 = background.Background("bwn300_150", "(300,150)")
sig3.setSignal()
sig3.set_debug()
sig3.scale_factor = lumi_[lumi_val]
sig3.setLineStyle(2)
sig3.set_color(r.kBlack)
sig3.set_treename("sig3")
sig3.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "389949")
backgrounds.append(sig3)


#### DATA
data = background.Data()
data.set_color(r.kBlack)
data.set_treename("data")
data.set_chain_from_list_CONDOR(filelist_dir + "data/", data_rawdir)


##########################################
# systematics
##########################################
systematics = []

#######################
### shape systematics
#######################
## e-gamma
syst = systematic.Systematic("EG_RESOLUTION_ALL", "UP", "DN")
syst.setKinSys()
systematics.append(syst)

syst = systematic.Systematic("EG_SCALE_ALL", "UP", "DN")
syst.setKinSys()
systematics.append(syst)

# muons
syst = systematic.Systematic("MUON_ID", "UP", "DN")
syst.setKinSys()
systematics.append(syst)

syst = systematic.Systematic("MUON_MS", "UP", "DN")
syst.setKinSys()
systematics.append(syst)

syst = systematic.Systematic("MUON_SCALE", "UP", "DN")
syst.setKinSys()
systematics.append(syst)
# jets

syst = systematic.Systematic("JET_GroupedNP_1", "UP", "DN")
syst.setKinSys()
systematics.append(syst)

syst = systematic.Systematic("JER", "", "")
syst.setKinSys()
syst.setOneSided()
systematics.append(syst)
# met
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

#syst = systematic.Systematic("PILEUP", "UP", "DOWN")
#syst.setWeightSys()
#systematics.append(syst)

## e-gamma
syst = systematic.Systematic("EL_EFF_ID", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)

syst = systematic.Systematic("EL_EFF_Iso", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)

syst = systematic.Systematic("EL_EFF_Reco", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)

# muons
syst = systematic.Systematic("MUON_EFF_STAT", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)

syst = systematic.Systematic("MUON_EFF_STAT_LOWPT", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)

syst = systematic.Systematic("MUON_EFF_SYS", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)

syst = systematic.Systematic("MUON_EFF_SYS_LOWPT", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)

syst = systematic.Systematic("MUON_ISO_STAT", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)

syst = systematic.Systematic("MUON_ISO_SYS", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)

# jets
#syst = systematic.Systematic("JET_JVTEff", "UP", "DOWN")
#syst.setWeightSys()
#systematics.append(syst)
#
# flavor tagging
syst = systematic.Systematic("FT_EFF_B", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)

syst = systematic.Systematic("FT_EFF_C", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)

syst = systematic.Systematic("FT_EFF_Light", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)

#syst = systematic.Systematic("FT_EFF_extrapolation", "UP", "DOWN")
#syst.setWeightSys()
#systematics.append(syst)

#syst = systematic.Systematic("FT_EFF_extrapolation_charm", "UP", "DOWN")
#syst.setWeightSys()
#systematics.append(syst)

##########################################
# regions
##########################################
regions = []

isEE = "(nElectrons==2 && abs(mll-91.2)>20) && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"
isMM = "(nMuons==2 && abs(mll-91.2)>20) && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"

isSFOS = "(( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && abs(mll-91.2)>20 && (l_q[0]*l_q[1])<0)"
isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<0"
trigger = "((year==2015 && trig_pass2015==1) || (year==2016 && trig_pass2016update==1))"

sr_w_def = "nBJets==0 && RPT>0.7 && gamInvRp1>0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && MDR>95 && mll>20 && " + trigger
srwMDR   = "nBJets==0 && RPT>0.7 && gamInvRp1>0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger
srwRPT = "nBJets==0 && MDR>95 && gamInvRp1>0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger 
sr_t_def = "nBJets>0  && RPT>0.7 && gamInvRp1>0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && MDR>110 && mll>20 && " + trigger 
srtMDR = "nBJets>0    && RPT>0.7 && gamInvRp1>0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger

reg = region.Region()
reg.name = "srwNM1"
reg.displayname = "SR_{W}^{3-body} Different Flavor"
reg.tcut = isDFOS + " && " + srwRPT
regions.append(reg)

reg = region.Region()
reg.name = "srwNM1SF"
reg.displayname = "SR_{W}^{3-body} Same Flavor"
reg.tcut = isSFOS + " && " + srwRPT
regions.append(reg)


reg = region.Region()
reg.name = "srtNM1"
reg.displayname = "SR_{t}^{3-body} Different Flavor"
reg.tcut = isDFOS + " && " + srtMDR
regions.append(reg)


reg = region.Region()
reg.name = "srtNM1SF"
reg.displayname = "SR_{t}^{3-body} Same Flavor"
reg.tcut = isSFOS + " && " + srtMDR
regions.append(reg)
