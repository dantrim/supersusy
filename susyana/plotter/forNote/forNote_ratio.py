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
rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/a_jan16/mc/Raw/"
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/a_jan16/dataToRun/Raw/"
fake_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0226/forFake3/fakes.3body/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0231val/filelists/"

lumi_ = [32.82] # norm from 1.0/fb to 32.82/fb
lumi_val = 0

######## MC
## ttbro
ttbar = background.Background("ttbar", "t#bar{t}")
ttbar.set_debug()
ttbar.scale_factor = lumi_[lumi_val] #* 1.18 # ttbar sample in n0229 was made with incorrect sumw
ttbar.set_fillStyle(0)
ttbar.setLineStyle(1)
#ttbar.set_color(r.kSpring-5)
#ttbar.set_color(r.TColor.GetColor("#FC0D1B"))
ttbar.set_color(r.TColor.GetColor("#e4706a"))
ttbar.set_treename("ttbar_powheg")
ttbar.set_chain_from_list_CONDOR(filelist_dir+ "ttbar/", rawdir)
backgrounds.append(ttbar)

# singletop
stop = background.Background("st", "Wt")
stop.set_debug()
stop.scale_factor = lumi_[lumi_val]
stop.set_fillStyle(0)
stop.setLineStyle(1)
#stop.set_color(r.kYellow-7)
#stop.set_color(r.TColor.GetColor("#DE080C"))
stop.set_color(r.TColor.GetColor("#db101c"))
stop.set_treename("ST")
stop.set_chain_from_list_CONDOR(filelist_dir+ "singletop/", rawdir)
backgrounds.append(stop)

## ttV
#ttv = background.Background("ttV", "t#bar{t} V")
#ttv.set_debug()
#ttv.scale_factor = lumi_[lumi_val]
#ttv.set_fillStyle(0)
#ttv.setLineStyle(1)
##ttv.set_color(r.kCyan-7)
##ttv.set_color(46)
#ttv.set_color(r.TColor.GetColor("#9bcdfd"))
#ttv.set_treename("TTV")
#ttv.set_chain_from_list_CONDOR(filelist_dir+ "ttV/", rawdir)
#backgrounds.append(ttv)

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
diboson = background.Background("vv", "VV")
diboson.set_debug()
diboson.scale_factor = lumi_[lumi_val] #* 1.06
diboson.set_fillStyle(0)
diboson.setLineStyle(1)
#diboson.set_color(r.kAzure+6)
#diboson.set_color(r.TColor.GetColor("#41C1FC"))
diboson.set_color(r.TColor.GetColor("#325f85"))
diboson.set_treename("diboson_sherpa")
diboson.set_chain_from_list_CONDOR(filelist_dir+ "diboson_sherpa_lvlv/", rawdir)
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
zjets = background.Background("zjets", "Z/#gamma^{*} + jets")
zjets.set_debug()
zjets.scale_factor = lumi_[lumi_val]
zjets.set_fillStyle(0)
zjets.setLineStyle(1)
#zjets.set_color(93)
#zjets.set_color(r.TColor.GetColor("#FFEF53"))
zjets.set_color(r.TColor.GetColor("#85dc6e"))
zjets.set_treename("zjets_sherpa")
zjets.set_chain_from_list_CONDOR(filelist_dir+ "zjets_sherpa/", rawdir)
backgrounds.append(zjets)


# Wjets
wjets = background.Background("wjets", "W+jets")
wjets.set_debug()
wjets.scale_factor = lumi_[lumi_val]
wjets.set_fillStyle(0)
wjets.setLineStyle(1)
#wjets.set_color(r.TColor.GetColor("#5E9AD6"))
wjets.set_color(r.TColor.GetColor("#619bd3"))
wjets.set_treename("wjets")
wjets.set_chain_from_list_CONDOR(filelist_dir+ "wjets_sherpa/", rawdir)
backgrounds.append(wjets)

## higgs
higgs = background.Background("higgs", "Higgs")
higgs.scale_factor = lumi_[lumi_val]
higgs.set_fillStyle(0)
higgs.setLineStyle(1)
higgs.set_color(r.kGreen-9)
higgs.set_treename("higgs")
higgs.set_chain_from_list_CONDOR(filelist_dir+ "higgs/", rawdir)
backgrounds.append(higgs)


drel = background.Background("drellyan", "Drell-Yan")
drel.set_debug()
drel.scale_factor = lumi_[lumi_val]
drel.set_fillStyle(0)
drel.setLineStyle(1)
#drel.set_color(r.kYellow)
drel.set_color(r.TColor.GetColor("#feec60"))
drel.set_treename("drellyan")
drel.set_chain_from_list_CONDOR(filelist_dir+ "drellyan_sherpa/", rawdir)
backgrounds.append(drel)

#fakes = background.Background("fakes", "FNP")
##fakes.scale_factor = 1.0
#fakes.scale_factor = 2.87 # scale from 12.2/fb to 30.5/fb
#fakes.set_treename("superNt")
#fakes.set_file(fake_rawdir + "physics_Main_276262_303560_FakesInclusive.root")
#fakes.set_merged_tree("superNt")
#fakes.set_color(r.kOrange+7)
#fakes.set_fillStyle(0)
#fakes.setLineStyle(1)
#backgrounds.append(fakes)

#sig1 = background.Background("bwn250_160", "#tilde{t}_{1}#tilde{t}_{1}, m(#tilde{t}_{1}, #tilde{#chi}_{1}^{ 0}) = (250, 160) GeV")
##sig1 = background.Background("bwn250_160", "(250,160)")
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
#sig2 = background.Background("bwn300_180", "#tilde{t}_{1}#tilde{t}_{1}, m(#tilde{t}_{1}, #tilde{#chi}_{1}^{ 0}) = (300, 180) GeV")
##sig2 = background.Background("bwn300_180", "(300,180)")
#sig2.setSignal()
#sig2.set_debug()
#sig2.scale_factor = lumi_[lumi_val]
#sig2.setLineStyle(2)
#sig2.set_color(r.kGreen)
#sig2.set_treename("sig2")
#sig2.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", rawdir, "387948")
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
#sig3.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "387947")
#backgrounds.append(sig3)


#### DATA
data = background.Data()
data.set_color(r.kBlack)
data.set_treename("data")
data.set_chain_from_list_CONDOR(filelist_dir + "dataToRun/", data_rawdir)


##########################################
# systematics
##########################################
systematics = []

#######################
### shape systematics
#######################
# e-gamma
#syst = systematic.Systematic("EG_RESOLUTION_ALL", "UP", "DN")
#syst.setKinSys()
#systematics.append(syst)
#
#syst = systematic.Systematic("EG_SCALE_ALL", "UP", "DN")
#syst.setKinSys()
#systematics.append(syst)
#
# muons
#syst = systematic.Systematic("MUONS_ID", "UP", "DN")
#syst.setKinSys()
#systematics.append(syst)

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

#syst = systematic.Systematic("PILEUP", "UP", "DOWN")
#syst.setWeightSys()
#systematics.append(syst)

## e-gamma
#syst = systematic.Systematic("EL_EFF_ID", "UP", "DOWN")
#syst.setWeightSys()
#systematics.append(syst)
#
#syst = systematic.Systematic("EL_EFF_Iso", "UP", "DOWN")
#syst.setWeightSys()
#systematics.append(syst)
#
#syst = systematic.Systematic("EL_EFF_Reco", "UP", "DOWN")
#syst.setWeightSys()
#systematics.append(syst)
#
## muons
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
## jets
##syst = systematic.Systematic("JET_JVTEff", "UP", "DOWN")
##syst.setWeightSys()
##systematics.append(syst)
##
## flavor tagging
#syst = systematic.Systematic("FT_EFF_B", "UP", "DOWN")
#syst.setWeightSys()
#systematics.append(syst)
#
#syst = systematic.Systematic("FT_EFF_C", "UP", "DOWN")
#syst.setWeightSys()
#systematics.append(syst)
#
#syst = systematic.Systematic("FT_EFF_Light", "UP", "DOWN")
#syst.setWeightSys()
#systematics.append(syst)
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
isEE = "(nElectrons==2 && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"
isMM = "(nMuons==2 && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"


isSFOS = "(( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && abs(mll-91.2)>10 && (l_q[0]*l_q[1])<0)"
isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<0"
isSFcheck = "((nMuons==2 || nElectrons==2)) && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"

trigger = "((year==2015 && trig_pass2015==1) || (year==2016 && trig_pass2016update==1))"


reg = region.Region()
reg.name = "dfprebv"
reg.displayname = "DF Preselection + b-veto"
reg.tcut = "nLeptons==2 && " + isDFOS + " && nBJets==0 && mll>20 && " + trigger 
regions.append(reg)

reg = region.Region()
reg.name = "sfprebv"
reg.displayname = "SF Preselection + b-veto (ee only)"
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
reg.name = "crv"
reg.displayname = "CR-VV-DF"
reg.tcut = isDFOS + " && nBJets==0 && MDR>30 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && RPT<0.5  && gamInvRp1>0.75 && mll>20 && " + trigger
#reg.tcut = isDFOS + " && nBJets==0 && MDR>30 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && RPT<0.5  && gamInvRp1>0.8 && mll>20 && " + trigger
regions.append(reg)

reg = region.Region()
reg.name = "crvB"
reg.displayname = "CR-VV-DF (b>0)"
reg.tcut = isDFOS + " && nBJets>0 && MDR>30 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && RPT<0.5  && gamInvRp1>0.8 && mll>20 && " + trigger
regions.append(reg)


reg = region.Region()
reg.name = "crvSF"
reg.displayname = "CR-VV-SF"
reg.tcut = isSFOS + " && nBJets==0 && MDR>30 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && RPT<0.5 && gamInvRp1>0.75 && met>80 && mll>20 && " + trigger
regions.append(reg)


reg = region.Region()
reg.name = "vrv"
reg.displayname = "VR-VV-DF"
reg.tcut = isDFOS + " && nBJets==0 && MDR>30 && MDR<80 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && RPT<0.5 && gamInvRp1>0.75 && mll>20 && " + trigger
regions.append(reg)

reg = region.Region()
reg.name = "vrvSF"
reg.displayname = "VR-VV-SF"
reg.tcut = isSFOS + " && nBJets==0 && MDR>30 && MDR<80 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && RPT<0.5 && gamInvRp1>0.75 && met>80 && mll>20 && " + trigger
regions.append(reg)

reg = region.Region()
reg.name = "crt"
reg.displayname = "CR-Top"
reg.tcut = isDFOS + " && nBJets>0 && MDR>80 && RPT>0.65 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && mll>20 && " + trigger
#reg.tcut = isDFOS + " && nBJets>0 && MDR>80 && RPT>0.5 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && mll>20 && " + trigger
regions.append(reg)

reg = region.Region()
reg.name = "vrt"
reg.displayname = "VR-Top"
reg.tcut = isDFOS + " && nBJets==0 && MDR>80 && RPT<0.65 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && mll>20 && " + trigger
#reg.tcut = isDFOS + " && nBJets==0 && MDR>80 && RPT<0.5 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && mll>20 && " + trigger
regions.append(reg)

reg = region.Region()
reg.name = "ttrj"
reg.displayname = "t#bar{t}-RJ"
#reg.tcut = isDFOS + " && nJets>1 && nBJets>0 && l_pt[0]>35 && l_pt[1]>20 && mll>20"
reg.tcut = "nJets>2 && nBJets>1 && nLeptons==2 && nMuons==1 && nElectrons==1 && mll>40 && l_pt[0]>30 && l_pt[1]>20 && abs(dphi_ll)>2.5 && j_eta[0]<2.5 && j_eta[1]<2.5"
regions.append(reg)




##########################################
# plots
##########################################
plots = []


vars = {}
vars["l_pt[0]"]         = { "dfprebv" : [40, 25,500,1e9],     "dfpreb" : [40, 25,500,1e9],    "crt" : [30, 25, 600, 1e5], "vrt"  : [20,25,300, 150],
                            "sfprebv" : [40, 25,400,1e10],    "sfpreb" : [40, 25,500,1e10],
                            "sfprebvEE" : [40, 25,400,1e10],    "sfprebEE" : [40, 25,500,1e10],
                            "sfprebvMM" : [40, 25,400,1e10],    "sfprebMM" : [40, 25,500,1e10],
                            #"crv"     : [10, 25, 100, 10000],   "crvSF"  : [15, 25, 105, 450 ], "vrv" : [5,25,70, 90],     "vrvSF" : [10,25,70,140]}
                            "crv"     : [10, 25, 100, 720],   "crvSF"  : [15, 25, 105, 800 ], "vrv" : [5,25,70, 200],     "vrvSF" : [10,25,70,140]}
                            #"crv"     : [10, 25, 100, 300],   "crvSF"  : [15, 25, 105, 250 ], "vrv" : [5,25,70, 90],     "vrvSF" : [10,25,70,140]}

vars["l_pt[1]"]         = { "dfprebv" : [40,20,500, 1e9],     "dfpreb" : [40,20,500, 1e9],    "crt" : [10, 20, 200, 7e5], "vrt"   : [10,20,130, 150],
                            "sfprebv" : [40,20,500,1e10],     "sfpreb" : [40,20,400,1e10],
                            "sfprebvEE" : [40,20,500,1e10],     "sfprebEE" : [40,20,400,1e10],
                            "sfprebvMM" : [40,20,500,1e10],     "sfprebMM" : [40,20,400,1e10],
                            #"crv"     : [4, 20, 60, 10000],     "crvSF" :  [8, 20, 70, 420 ],   "vrv" : [2,20,40, 80],      "vrvSF" : [4,20,40, 120]}
                            "crv"     : [4, 20, 60, 550],     "crvSF" :  [8, 20, 70, 600 ],   "vrv" : [2,20,40, 220],      "vrvSF" : [4,20,40, 120]}
                            #"crv"     : [4, 20, 60, 220],     "crvSF" :  [8, 20, 70, 200 ],   "vrv" : [2,20,40, 80],      "vrvSF" : [4,20,40, 120]}

vars["MDR" ]            = { "dfprebv" : [10,0,200, 1e9],      "dfpreb" : [10,0,200, 1e9],     "crt" : [ 5, 80,200, 7e5],  "vrt"   : [5,80,135, 210],
                            "sfprebv" : [10,0,200,1e10],      "sfpreb" : [10,0,200,1e10],
                            "sfprebvEE" : [10,0,200,1e10],      "sfprebEE" : [10,0,200,1e10],
                            "sfprebvMM" : [10,0,200,1e10],      "sfprebMM" : [10,0,200,1e10],
                            #"crv"     : [10,  30, 120, 1e4],  "crvSF"  : [10, 50, 130, 400 ], "vrv" : [10,30,80,    150],  "vrvSF" : [10,30,80, 180]}
                            "crv"     : [10,  30, 120, 600],  "crvSF"  : [10, 50, 130, 650 ], "vrv" : [10,30,80,    300],  "vrvSF" : [10,30,80, 180]}
                            #"crv"     : [10,  30, 120, 230],  "crvSF"  : [10, 50, 130, 220 ], "vrv" : [10,30,80,    150],  "vrvSF" : [10,30,80, 180]}

vars["DPB_vSS"]         = { "dfprebv" : [0.2,0,3.2, 1e9],     "dfpreb" : [0.2,0,3.2, 1e9],    "crt" : [0.1, 0, 2.8, 7e5], "vrt"   : [0.2,1.8,3.2, 200],
                            "sfprebv" : [0.2,0,3.2,1e10],      "sfpreb" : [0.2,0,3.2,1e10],
                            "sfprebvEE" : [0.2,0,3.2,1e10],      "sfprebEE" : [0.2,0,3.2,1e10],
                            "sfprebvMM" : [0.2,0,3.2,1e10],      "sfprebMM" : [0.2,0,3.2,1e10],
                            #"crv"     : [0.5, 0, 2.8, 1e4],   "crvSF"  : [0.5, 0, 2.8, 335],  "vrv" : [0.2,1.8,3.2, 120],  "vrvSF" : [0.2,1.8,3.2, 120]}
                            "crv"     : [0.5, 0, 2.8, 580],   "crvSF"  : [0.5, 0, 2.8, 500],  "vrv" : [0.2,1.8,3.2, 200],  "vrvSF" : [0.2,1.8,3.2, 120]}
                            #"crv"     : [0.5, 0, 2.8, 250],   "crvSF"  : [0.5, 0, 2.8, 250],  "vrv" : [0.2,1.8,3.2, 120],  "vrvSF" : [0.2,1.8,3.2, 120]}

vars["gamInvRp1"]       = { "dfprebv" : [0.05,0,1, 1e9],     "dfpreb"  : [0.05,0,1, 1e9],     "crt" : [0.1, 0, 1, 7e5],  "vrt"   : [0.1,0,1, 180],
                            "sfprebv" : [0.05,0,1,1e10],     "sfpreb"  : [0.05,0,1,1e10],
                            "sfprebvEE" : [0.05,0,1,1e10],     "sfprebEE"  : [0.05,0,1,1e10],
                            "sfprebvMM" : [0.05,0,1,1e10],     "sfprebMM"  : [0.05,0,1,1e10],
                            #"crv"     : [0.02, 0.8, 1, 1e4], "crvSF"   : [0.04, 0.8, 1, 350 ], "vrv" : [0.05,0.8,1, 140],  "vrvSF" : [0.05,0.8,1, 150]}
                            "crv"     : [0.02, 0.8, 1, 400], "crvSF"   : [0.04, 0.8, 1, 550 ], "vrv" : [0.05,0.8,1, 320],  "vrvSF" : [0.05,0.8,1, 150]}
                            #"crv"     : [0.02, 0.8, 1, 200], "crvSF"   : [0.04, 0.8, 1, 200 ], "vrv" : [0.05,0.8,1, 140],  "vrvSF" : [0.05,0.8,1, 150]}

vars["abs(cosThetaB)"]  = { "dfprebv" : [0.05,0,1, 1e9],     "dfpreb"  : [0.05,0,1, 1e9], "crt" : [0.05, 0, 1, 7e5],     "vrt" : [0.1,0,1, 200],
                            "sfprebv" : [0.05,0,1,1e10],     "sfpreb"  : [0.05,0,1,1e10],
                            "sfprebvEE" : [0.05,0,1,1e10],     "sfprebEE"  : [0.05,0,1,1e10],
                            "sfprebvMM" : [0.05,0,1,1e10],     "sfprebMM"  : [0.05,0,1,1e10],
                            #"crv" : [0.15, 0, 1, 1e4],       "crvSF"   : [0.2, 0, 1, 320 ], "vrv" : [0.2,0,1, 100], "vrvSF" : [0.2,0,1, 120]}
                            "crv" : [0.15, 0, 1, 400],       "crvSF"   : [0.2, 0, 1, 375 ], "vrv" : [0.2,0,1, 300], "vrvSF" : [0.2,0,1, 120]}
                            #"crv" : [0.15, 0, 1, 200],       "crvSF"   : [0.2, 0, 1, 200 ], "vrv" : [0.2,0,1, 100], "vrvSF" : [0.2,0,1, 120]}

vars["RPT"]             = { "dfprebv" : [0.05,0,1, 1e9], "dfpreb" : [0.05,0,1, 1e9], "crt"    : [0.05, 0.5, 1, 7e5], "vrt" : [0.05,0,0.5, 150],
                            "sfprebv" : [0.05,0,1,1e10], "sfpreb" : [0.05,0,1,1e10],
                            "sfprebvEE" : [0.05,0,1,1e10], "sfprebEE" : [0.05,0,1,1e10],
                            "sfprebvMM" : [0.05,0,1,1e10], "sfprebMM" : [0.05,0,1,1e10],
                            #"crv" : [0.1, 0, 0.5, 1e4],  "crvSF"  : [0.1, 0, 0.5, 375], "vrv" : [0.1,0,0.5,120],    "vrvSF" : [0.1,0,0.5, 150]}
                            "crv" : [0.1, 0, 0.5, 700],  "crvSF"  : [0.1, 0, 0.5, 600], "vrv" : [0.1,0,0.5,240],    "vrvSF" : [0.1,0,0.5, 150]}
                            #"crv" : [0.1, 0, 0.5, 290],  "crvSF"  : [0.1, 0, 0.5, 230], "vrv" : [0.1,0,0.5,120],    "vrvSF" : [0.1,0,0.5, 150]}

vars["nSJets"]          = { "dfprebv" : [1, 0,15, 1e9], "dfpreb" : [1, 0,15, 1e9], "crt" : [1, 0, 12, 7e5], "vrt" : [1,0,10, 220],
                            "sfprebv" : [1,0,15,1e10],  "sfpreb" : [1,0,15,1e10],
                            "sfprebvEE" : [1,0,15,1e10],  "sfprebEE" : [1,0,15,1e10],
                            "sfprebvMM" : [1,0,15,1e10],  "sfprebMM" : [1,0,15,1e10],
                            #"crv" : [1, 0, 7, 1e4],     "crvSF" : [1, 0, 7, 375],  "vrv" : [1,0,7, 180],     "vrvSF" : [1,0,7, 180]}
                            "crv" : [1, 0, 7, 1100],     "crvSF" : [1, 0, 7, 600],  "vrv" : [1,0,7, 400],     "vrvSF" : [1,0,7, 180]}
                            #"crv" : [1, 0, 7, 500],     "crvSF" : [1, 0, 7, 250],  "vrv" : [1,0,7, 180],     "vrvSF" : [1,0,7, 180]}

vars["nBJets"]          = { "dfprebv" : [1, 0,3, 1e9], "dfpreb" : [1, 0,6, 1e9], "crt"  : [1, 0, 10, 7e5], "vrt" : [1,0,3, 1000],
                            "sfprebv" : [1,0,3,1e10],  "sfpreb" : [1,0,6,1e10],
                            "sfprebvEE" : [1,0,3,1e10],  "sfprebEE" : [1,0,6,1e10],
                            "sfprebvMM" : [1,0,3,1e10],  "sfprebMM" : [1,0,6,1e10],
                            #"crv" : [1, 0, 3, 1e4], "crvSF"     : [1, 0, 3, 1000], "vrv" : [1,0,3, 300], "vrvSF"  : [1,0,3, 320]}
                            "crv" : [1, 0, 3, 2000], "crvSF"     : [1, 0, 3, 1600], "vrv" : [1,0,3, 750], "vrvSF"  : [1,0,3, 320]}
                            #"crv" : [1, 0, 3, 1000], "crvSF"     : [1, 0, 3, 600], "vrv" : [1,0,3, 300], "vrvSF"  : [1,0,3, 320]}

vars["met"]             = { "dfprebv" : [30,0,500, 1e9], "dfpreb" : [30,0,500, 1e9], "crt" : [30,0,460, 7e5], "vrt" : [20,80,280, 250],
                            "sfprebv" : [30,0,500,1e10], "sfpreb" : [30,0,500,1e10],
                            "sfprebvEE" : [30,0,500,1e10], "sfprebEE" : [30,0,500,1e10],
                            "sfprebvMM" : [30,0,500,1e10], "sfprebMM" : [30,0,500,1e10],
                            #"crv" : [10, 30, 120, 1e4], "crvSF"   : [10, 70, 135,  550 ], "vrv" : [10,40,100, 100], "vrvSF" : [5,70,110, 130]}
                            "crv" : [10, 30, 120, 520], "crvSF"   : [10, 70, 135,  950 ], "vrv" : [10,40,100, 225], "vrvSF" : [5,70,110, 130]}
                            #"crv" : [10, 30, 120, 230], "crvSF"   : [10, 70, 135,  250 ], "vrv" : [10,40,100, 100], "vrvSF" : [5,70,110, 130]}

vars["DPB_vSS - 0.85*abs(cosThetaB)"] = { "dfpreb" : [0.5, -1.5, 4, 1e9], "dfprebv" : [0.5, -1.5, 4.0, 1e9],
                                          "sfpreb" : [0.5, -1.5, 4, 1e10],  "sfprebv" : [0.5, -1.5, 4, 1e10],
                                          "crt" : [0.2, -1.2, 1.8, 7e5], "vrt" : [0.2, 1.8, 3.4, 250],
                                          #"crv" : [0.2, -1, 1.8, 1e4], "vrv" : [0.2, 1.8, 3.4, 90],
                                          "crv" : [0.2, -1, 1.8, 300], "vrv" : [0.2, 1.8, 3.4, 200],
                                          "crvSF" : [0.2, -1.2, 1.8, 400], "vrvSF" : [0.2, 1.8, 3.2, 140]  }
                                          #"crv" : [0.2, -1, 1.8, 130], "vrv" : [0.2, 1.8, 3.4, 90],
                                          #"crvSF" : [0.2, -1.2, 1.8, 120], "vrvSF" : [0.2, 1.8, 3.2, 140]  }

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
##vars["mll"]             = { "dfpreb" : [10,0,300,1e7],   "dfprebv" : [10,0,300,1e7],   "crt" : [10,0,120,1e4], "vrv" : [5, 20, 60, 30], "crv" : [5, 20, 70, 60], "crvSF" : [8, 20, 80, 40] , "vrvSF" : [5, 20, 60, 25] }
#vars["nVtx"]            = { "dfpreb" : [1,0,38,1e9], "dfprebv" : [1,0,40,1e7] }
#vars["avgMu"]           = { "dfpreb" : [1,0,45,1e9] }

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






run_reg = "crvSF"

nice_names = {}
nice_names["MDR"] = "M_{#Delta}^{R} [GeV]"
nice_names["DPB_vSS"] = "#Delta#phi_{#beta}^{R}"
nice_names["met"] = "E_{T}^{miss} [GeV]"
nice_names["gamInvRp1"] = "1/#gamma_{R+1}"
nice_names["abs(cosThetaB)"] = "|cos#theta_{b}|"
nice_names["RPT"] = "R_{p_{T}}"
nice_names["DPB_vSS - 0.85*abs(cosThetaB)"] = "#Delta#phi_{#beta}^{R} - 0.85#times|cos#theta_{b}|" 
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
    elif var=="DPB_vSS - 0.85*abs(cosThetaB)" :
        name_ = "DPB_minus_COSB"
    else :
        name_ = var
    p.initialize(run_reg, var, "%s_%s"%(run_reg, name_))
    ylabel_unit = ""
    gev_variables = ["MDR", "met", "l_pt[0]", "l_pt[1]", "mll"]
    if var in gev_variables :
        ylabel_unit = " GeV"
    ylabel_title = str(bounds[run_reg][0]) + ylabel_unit
    p.labels(x=nice_names[var], y = "Entries / %s"%(str(ylabel_title)))
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
