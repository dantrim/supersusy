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
## ttbro
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
fakes.scale_factor = 1.0
fakes.set_treename("superNt")
fakes.set_file(fake_rawdir + "CENTRAL_fakes.3body_v02.root")
fakes.set_merged_tree("superNt")
fakes.set_color(r.kGray+1)
fakes.set_fillStyle(0)
fakes.setLineStyle(1)
backgrounds.append(fakes)


sig1 = background.Background("bwn250_160", "(250,160)")
sig1.setSignal()
sig1.set_debug()
sig1.scale_factor = lumi_[lumi_val]
sig1.set_fillStyle(0)
sig1.setLineStyle(2)
sig1.set_color(r.kBlue)
sig1.set_treename("sig1")
sig1.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", rawdir, "387943")
backgrounds.append(sig1)

sig2 = background.Background("bwn300_180", "(300,180)")
sig2.setSignal()
sig2.set_debug()
sig2.scale_factor = lumi_[lumi_val]
sig2.setLineStyle(2)
sig2.set_color(r.kGreen)
sig2.set_treename("sig2")
sig2.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", rawdir, "387948")
backgrounds.append(sig2)

sig3 = background.Background("bwn300_150", "(300,150)")
sig3.setSignal()
sig3.set_debug()
sig3.scale_factor = lumi_[lumi_val]
sig3.setLineStyle(2)
sig3.set_color(r.kBlack)
sig3.set_treename("sig3")
sig3.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "387947")
backgrounds.append(sig3)


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

isEE = "(nElectrons==2 && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"
isMM = "(nMuons==2 && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0 && l_pt[0]>22 && l_pt[1]>20"
#isSFOS = "(( (nMuons==2 && l_pt[0]>22 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>20 && l_pt[1]>20)) && abs(mll-91.2)>10 && (l_q[0]*l_q[1])<0)"
isSFOS = "( (nMuons==2 || nElectrons==2) && abs(mll-91.2)>10 && (l_q[0]*l_q[1])<0)"
isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0"# && l_pt[0]>20 && l_pt[1]>20 && (l_q[0]*l_q[1])<0"

sr_w_def = "nBJets==0 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && MDR>95 && mll>20"# && trig_pass2016==1 && mll>20"
sr_t_def = "nBJets>0 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && MDR>110 && mll>20"# && trig_pass2016==1 && mll>20"

reg = region.Region()
reg.name = "srwSF"
reg.displayname = "SRw (SF)"
reg.tcut = isSFOS + " && " + sr_w_def
regions.append(reg)

reg = region.Region()
reg.name = "srwDF"
reg.displayname = "SRw (DF)"
reg.tcut = isDFOS + " && " + sr_w_def
regions.append(reg)

reg = region.Region()
reg.name = "srtSF"
reg.displayname = "SRt (SF)"
reg.tcut = isSFOS + " && " + sr_t_def
regions.append(reg)

reg = region.Region()
reg.name = "srtDF"
reg.displayname = "SRt (DF)"
reg.tcut = isDFOS + " && " + sr_t_def
regions.append(reg)




##########################################
# plots
##########################################
plots = []


vars = {}

vars["l_pt[0]"]     = { "srwSF" : [2, 15, 100, 5], "srwDF" : [2, 15, 100, 5], "srtSF" : [2, 15, 100, 5], "srtDF" : [2, 15, 100, 5] }

#vars["l_pt[0]"]         = { "dfprebv" : [40, 20,500,1e7] ,"dfpreb" : [40, 20,500,1e7] ,"crt" : [10, 20, 500, 1e4]  , "vrt" : [20,20,250,   40]    , "crv" : [10, 20, 100,    95]  ,"crvSF" : [15, 20, 105,    95]  , "vrv" : [5,20,70,     35], "vrvSF" : [10,20,70,       70]}
#vars["l_pt[1]"]         = { "dfprebv" : [40,20,500, 1e7] ,"dfpreb" : [40,20,500, 1e7] ,"crt" : [10, 20, 200, 1e4]  , "vrt" : [10,20,130,   55]    , "crv" : [4, 20, 60,      85]  ,"crvSF" : [8, 20, 70,      85]  , "vrv" : [2,20,40,     30], "vrvSF" : [4,20,40,       55]}
#vars["MDR" ]            = { "dfprebv" : [10,0,200,  1e7] ,"dfpreb" : [10,0,200,  1e7] ,"crt" : [ 5, 80,160, 1e4]   , "vrt" : [5,80,125,    65]    , "crv" : [10,  30, 120,   85]  ,"crvSF" : [10, 50, 130,    85] ,  "vrv" : [10,30,80,    70], "vrvSF" : [10,30,80,      70]}
#vars["DPB_vSS"]         = { "dfprebv" : [0.2,0,3.2, 1e7] ,"dfpreb" : [0.2,0,3.2, 1e7] ,"crt" : [0.1, 0, 2.8, 1e4]  , "vrt" : [0.2,1.8,3.2, 60]    , "crv" : [0.5, 0, 2.8,   100]  ,"crvSF" : [0.5, 0, 2.8,   100]  , "vrv" : [0.2,1.8,3.2, 40], "vrvSF" : [0.2,1.8,3.2,   50]}
#vars["gamInvRp1"]       = { "dfprebv" : [0.05,0,1,  1e7] ,"dfpreb" : [0.05,0,1,  1e7] ,"crt" : [0.1, 0, 1, 1e4]    , "vrt" : [0.1,0,1,     35]    , "crv" : [0.02, 0.8, 1,   70]  ,"crvSF" : [0.04, 0.8, 1,   70]  , "vrv" : [0.05,0.8,1,  60], "vrvSF" : [0.05,0.8,1,    60]}
#vars["abs(cosThetaB)"]  = { "dfprebv" : [0.05,0,1,  1e7] ,"dfpreb" : [0.05,0,1,  1e7] ,"crt" : [0.05, 0, 1, 1e4]   , "vrt" : [0.1,0,1,     35]    , "crv" : [0.15, 0, 1,     80]  ,"crvSF" : [0.2, 0, 1,      80]  , "vrv" : [0.2,0,1,     45], "vrvSF" : [0.2,0,1,       45]}
#vars["RPT"]             = { "dfprebv" : [0.05,0,1,  1e7] ,"dfpreb" : [0.05,0,1,  1e7] ,"crt" : [0.05, 0.5, 1, 1e4] , "vrt" : [0.05,0,0.5,  40]    , "crv" : [0.1, 0, 0.5,   110]  ,"crvSF" : [0.1, 0, 0.5,   110]  , "vrv" : [0.1,0,0.5,   55], "vrvSF" : [0.1,0,0.5,     50]}
#vars["nSJets"]          = { "dfprebv" : [1, 0,15,   1e7] ,"dfpreb" : [1, 0,15,   1e7] ,"crt" : [1, 0, 10, 1e4]     , "vrt" : [1,0,10,      55]    , "crv" : [1, 0, 7,       175]  ,"crvSF" : [1, 0, 7,       100]  , "vrv" : [1,0,7,       85], "vrvSF" : [1,0,7,         50]}
#vars["nBJets"]          = { "dfprebv" : [1, 0,3,    1e7] ,"dfpreb" : [1, 0,6,    1e7] ,"crt" : [1, 0, 10, 1e4]     , "vrt" : [1,0,3,       145]   , "crv" : [1, 0, 3,       330]  ,"crvSF" : [1, 0, 3,       250]  , "vrv" : [1,0,3,      140], "vrvSF" : [1,0,3,        120]}
#vars["met"]             = { "dfprebv" : [30,0,500,  1e7] ,"dfpreb" : [30,0,500,  1e7] ,"crt" : [30,0,400,1e4]      , "vrt" : [10,80,250,   30]    , "crv" : [10, 30, 120,    85]  ,"crvSF" : [10, 70, 135,   120]  , "vrv" : [10,40,100,   50], "vrvSF" : [5,70,110,      40]}
#vars["mll"]             = { "dfpreb" : [10,0,300,1e7],   "dfprebv" : [10,0,300,1e7],   "crt" : [10,0,120,1e4], "vrv" : [5, 20, 60, 30], "crv" : [5, 20, 70, 60], "crvSF" : [8, 20, 80, 40] , "vrvSF" : [5, 20, 60, 25] }
#vars["nVtx"]            = { "dfpreb" : [1,0,40,1e7], "dfprebv" : [1,0,40,1e7] }


#### for ~3/fb these are ok
#vars["l_pt[0]"]         = { "dfprebv" : [40, 20,500,1e7] ,"dfpreb" : [40, 20,500,1e7] ,"crt" : [10, 20, 500, 1e4]  , "vrt" : [20,20,250,   30]    , "crv" : [10, 20, 100,    60]  ,"crvSF" : [15, 20, 105,    60]  , "vrv" : [5,20,70,     25], "vrvSF" : [5,20,70,     25]}
#vars["l_pt[1]"]         = { "dfprebv" : [40,20,500, 1e7] ,"dfpreb" : [40,20,500, 1e7] ,"crt" : [10, 20, 200, 1e4]  , "vrt" : [10,20,130,   40]    , "crv" : [4, 20, 60,      55]  ,"crvSF" : [8, 20, 70,     50]   , "vrv" : [2,20,40,     20], "vrvSF" : [4,20,40,     20]}
#vars["MDR" ]            = { "dfprebv" : [10,0,200,  1e7] ,"dfpreb" : [10,0,200,  1e7] ,"crt" : [ 5, 80,160, 1e4]   , "vrt" : [5,80,125,    50]    , "crv" : [10,  30, 120,   50]  ,"crvSF" : [10, 50, 130,     50] , "vrv" : [10,30,80,    40], "vrvSF" : [10,30,80,    40]}
#vars["DPB_vSS"]         = { "dfprebv" : [0.2,0,3.2, 1e7] ,"dfpreb" : [0.2,0,3.2, 1e7] ,"crt" : [0.1, 0, 2.8, 1e4]  , "vrt" : [0.2,1.8,3.2, 40]    , "crv" : [0.5, 0, 2.8,    50]  ,"crvSF" : [0.5, 0, 2.8,    40]  , "vrv" : [0.2,1.8,3.2, 35], "vrvSF" : [0.2,1.8,3.2, 30]}
#vars["gamInvRp1"]       = { "dfprebv" : [0.05,0,1,  1e7] ,"dfpreb" : [0.05,0,1,  1e7] ,"crt" : [0.1, 0, 1, 1e4]    , "vrt" : [0.1,0,1,     35]    , "crv" : [0.02, 0.8, 1,   40]  ,"crvSF" : [0.04, 0.8, 1,   50]  , "vrv" : [0.05,0.8,1,  40], "vrvSF" : [0.05,0.8,1,  40]}
#vars["abs(cosThetaB)"]  = { "dfprebv" : [0.05,0,1,  1e7] ,"dfpreb" : [0.05,0,1,  1e7] ,"crt" : [0.05, 0, 1, 1e4]   , "vrt" : [0.1,0,1,     25]    , "crv" : [0.15, 0, 1,     55]  ,"crvSF" : [0.2, 0, 1,      40]  , "vrv" : [0.2,0,1,     25], "vrvSF" : [0.2,0,1,     25]}
#vars["RPT"]             = { "dfprebv" : [0.05,0,1,  1e7] ,"dfpreb" : [0.05,0,1,  1e7] ,"crt" : [0.05, 0.5, 1, 1e4] , "vrt" : [0.05,0,0.5,  40]    , "crv" : [0.1, 0, 0.5,    65]  ,"crvSF" : [0.1, 0, 0.5,    60]  , "vrv" : [0.1,0,0.5,30], "vrvSF" : [0.1,0,0.5, 30]}
#vars["nSJets"]          = { "dfprebv" : [1, 0,15,   1e7] ,"dfpreb" : [1, 0,15,   1e7] ,"crt" : [1, 0, 10, 1e4]     , "vrt" : [1,0,10,      40]    , "crv" : [1, 0, 7,        90]  ,"crvSF" : [1, 0, 7,        40]  , "vrv" : [1,0,7,       40], "vrvSF" : [1,0,7,       30]}
#vars["nBJets"]          = { "dfprebv" : [1, 0,3,    1e7] ,"dfpreb" : [1, 0,6,    1e7] ,"crt" : [1, 0, 10, 1e4]     , "vrt" : [1,0,3,       100]   , "crv" : [1, 0, 3,       175]  ,"crvSF" : [1, 0, 3,       120]  , "vrv" : [1,0,3,      100], "vrvSF" : [1,0,3,      100]}
#vars["met"]             = { "dfprebv" : [30,0,500,  1e7] ,"dfpreb" : [30,0,500,  1e7] ,"crt" : [30,0,400,1e4]      , "vrt" : [10,80,250,   25]    , "crv" : [10, 30, 120,    50]  ,"crvSF" : [10, 70, 135,    55]  , "vrv" : [10,40,100,   35], "vrvSF" : [5,70,110,   20]}
##vars["mll"]             = { "dfpreb" : [10,0,300,1e7],   "dfprebv" : [10,0,300,1e7],   "crt" : [10,0,120,1e4], "vrv" : [5, 20, 60, 30], "crv" : [5, 20, 70, 60], "crvSF" : [8, 20, 80, 40] , "vrvSF" : [5, 20, 60, 25] }
##vars["nVtx"]            = { "dfpreb" : [1,0,40,1e7], "dfprebv" : [1,0,40,1e7] }





run_reg = "srtDF"

nice_names = {}
nice_names["MDR"] = "E_{V}^{P} [GeV]"
nice_names["DPB_vSS"] = "#Delta#phi(#vec{#beta}_{PP}^{LAB}, #vec{p}_{V}^{PP})"
nice_names["met"] = "E_{T}^{miss} [GeV]"
nice_names["gamInvRp1"] = "1/#gamma_{P}^{PP}"
nice_names["abs(cosThetaB)"] = "|cos#theta_{b}|"
nice_names["RPT"] = "R_{p_{T}}"
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
nice_names["nVtx"] = "Num. Primary Vertices"
nice_names["mll"] = "Dilepton Invariant Mass [GeV]"

for var, bounds in vars.iteritems() :
    p = plot.Plot1D()
    name_ = ""
    if "abs(" in var :
        name_ = var.replace("abs(","")
        name_ = name_.replace(")", "")
    elif "[" in var :
        name_ = var.replace("[","")
        name_ = name_.replace("]","")
    else :
        name_ = var
    p.initialize(run_reg, var, "%s_%s"%(run_reg, name_))
    p.labels(x=nice_names[var], y = "Entries / %s"%(str(bounds[run_reg][0])))
    p.xax(bounds[run_reg][0], bounds[run_reg][1], bounds[run_reg][2])
    if "crt" in run_reg or "dfpre" in run_reg or "sfcr" in run_reg or "checkSF" in run_reg : #or "crv" in run_reg or "vrv" in run_reg:
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
