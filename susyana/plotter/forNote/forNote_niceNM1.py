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
rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0225/jul6/mc/Raw/"
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0225/jul6/n0225_data/Raw/"
#data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0225/jun30/data15/Raw/"
fake_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0224/fakes_jun13/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0225val/filelists/"
#zjets_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0224/jun1/mc/Raw/" 
#zjets_filelist_dir = "/data/uclhc/uci/user/dantrim/n0224val/filelists/"

#sherpa21_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0222/may23/mc/Raw/" 
#sherpa21_filelist_dir = "/data/uclhc/uci/user/dantrim/n0222val/filelists/"


#lumi_ = [0.937]
#lumi_ = [1.0]
lumi_ = [1.81] # norm to 2.614 for DS!
#if "data15" in data_rawdir :
#    lumi_.append(1.0)
#elif "data16" in data_rawdir :
#    lumi_.append(0.937)
#lumi_ = [1.0]
lumi_val = 0

######## MC
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

# singletop
ttv = background.Background("ttV", "tt+V")
ttv.set_debug()
ttv.scale_factor = lumi_[lumi_val]
ttv.set_fillStyle(0)
ttv.setLineStyle(1)
ttv.set_color(46)
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
#diboson.set_chain_from_list_CONDOR(filelist_dir+ "test_diboson/", rawdir)
#diboson.set_chain_from_list_CONDOR(filelist_dir+ "diboson_sherpa/", rawdir)
diboson.set_chain_from_list_CONDOR(filelist_dir+ "diboson_sherpa_lvlv/", rawdir)
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
#zjets.set_chain_from_list_CONDOR(filelist_dir+ "zjets_sherpa_withtau/", rawdir)
#zjets.set_chain_from_list_CONDOR(sherpa21_filelist_dir+"zjets_sherpa/",sherpa21_rawdir)
backgrounds.append(zjets)

# Wjets
#wjets = background.Background("wjets", "W+Jets (Sherpa)")
#wjets.set_debug()
#wjets.scale_factor = lumi_[lumi_val]
#wjets.set_fillStyle(0)
#wjets.setLineStyle(1)
#wjets.set_color(r.TColor.GetColor("#5E9AD6"))
#wjets.set_treename("wjets")
#wjets.set_chain_from_list_CONDOR(filelist_dir+ "wjets_sherpa22/", rawdir)
##wjets.set_chain_from_list_CONDOR(sherpa21_filelist_dir+"wjets_sherpa/",sherpa21_rawdir)
#backgrounds.append(wjets)

drel = background.Background("drellyan", "Drell-Yan")
drel.set_debug()
drel.scale_factor = lumi_[lumi_val]
drel.set_fillStyle(0)
drel.setLineStyle(1)
drel.set_color(r.kYellow)
drel.set_treename("drellyan")
drel.set_chain_from_list_CONDOR(filelist_dir+ "drellyan_sherpa/", rawdir)
backgrounds.append(drel)

fakes = background.Background("fakes", "Non-prompt")
fakes.scale_factor = lumi_[lumi_val]
fakes.set_treename("superNt")
fakes.set_file(fake_rawdir + "CENTRAL_fakes.3body_v02.root")
fakes.set_merged_tree("superNt")
fakes.set_color(r.kGray+1)
fakes.set_fillStyle(0)
fakes.setLineStyle(1)
backgrounds.append(fakes)


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


#### DATA
data = background.Data()
data.set_color(r.kBlack)
data.set_treename("dataToDS1")
#data.set_chain_from_list_CONDOR(filelist_dir + "n0225_data15/", data_rawdir)
data.set_chain_from_list_CONDOR(filelist_dir + "n0225_data_2015DSW/", data_rawdir)


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
#
# muons
syst = systematic.Systematic("MUONS_ID", "UP", "DN")
syst.setKinSys()
systematics.append(syst)

syst = systematic.Systematic("MUONS_MS", "UP", "DN")
syst.setKinSys()
systematics.append(syst)

syst = systematic.Systematic("MUONS_SCALE", "UP", "DN")
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

syst = systematic.Systematic("FT_EFF_extrapolation", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)

syst = systematic.Systematic("FT_EFF_extrapolation_charm", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)

##########################################
# regions
##########################################
regions = []

#isEE = "(nElectrons==2 && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0"
#isMM = "(nMuons==2 && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0"
#isDF = "(nElectrons==1 && nMuons==1) && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"
#inZ = ("((nMuons==2 || nElectrons==2) && abs(mll-91.2)<10)")
isEE = "(nElectrons==2 && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"


#isSFOS = "((nMuons==2 || nElectrons==2) && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"

isSFOS = "(( (nMuons==2 && l_pt[0]>22 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>20 && l_pt[1]>20)) && abs(mll-91.2)>10 && (l_q[0]*l_q[1])<0)"
isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && l_pt[0]>20 && l_pt[1]>20 && (l_q[0]*l_q[1])<0"
isSFcheck = "((nMuons==2 || nElectrons==2)) && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"

sr_w_def = "nBJets==0 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && MDR>95 && trig_pass2016==1 && mll>20"
srwMDR   = "nBJets==0 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && trig_pass2016==1 && mll>20"
sr_t_def = "nBJets>0 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && MDR>110 && trig_pass2016==1 && mll>20"
srtMDR = "nBJets>0 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8)  && trig_pass2016==1 && mll>20"

reg = region.Region()
reg.name = "srwNM1"
reg.displayname = "SRw N-1 (DF)"
reg.tcut = isDFOS + " && " + srwMDR
regions.append(reg)

reg = region.Region()
reg.name = "srwNM1SF"
reg.displayname = "SRw N-1 (SF)"
reg.tcut = isSFOS + " && " + srwMDR
regions.append(reg)


reg = region.Region()
reg.name = "srtNM1"
reg.displayname = "SRt N-1 (DF)"
reg.tcut = isDFOS + " && " + srtMDR
regions.append(reg)


reg = region.Region()
reg.name = "srtNM1SF"
reg.displayname = "SRt N-1 (SF)"
reg.tcut = isSFOS + " && " + srtMDR
regions.append(reg)
