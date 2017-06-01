import sys
sys.path.append(os.environ['SUSYDIR'])
import supersusy.utils.plot as plot
import supersusy.utils.background as background
import supersusy.utils.region as region
import supersusy.utils.systematic as systematic



do_eff_nVtx = False
do_lumi_yields = True

#######################################
# samples
########################################
backgrounds = []
rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/d_jan30/mc/Raw/"
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0231/d_jan30/data/Raw/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0231val/filelists/"


lumi_ = [36]
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
backgrounds.append(zjets)

# Wjets
wjets = background.Background("wjets", "W+Jets (Sherpa)")
wjets.set_debug()
wjets.scale_factor = lumi_[lumi_val]
wjets.set_fillStyle(0)
wjets.setLineStyle(1)
wjets.set_color(r.TColor.GetColor("#5E9AD6"))
wjets.set_treename("wjets")
wjets.set_chain_from_list_CONDOR(filelist_dir+ "wjets_sherpa22/", rawdir)
#wjets.set_chain_from_list_CONDOR(sherpa21_filelist_dir+"wjets_sherpa/",sherpa21_rawdir)
backgrounds.append(wjets)

drel = background.Background("drellyan", "Drell-Yan")
drel.set_debug()
drel.scale_factor = lumi_[lumi_val]
drel.set_fillStyle(0)
drel.setLineStyle(1)
drel.set_color(r.kYellow)
drel.set_treename("drellyan")
drel.set_chain_from_list_CONDOR(filelist_dir+ "drellyan_sherpa/", rawdir)
backgrounds.append(drel)

#fakes = background.Background("fakes", "Non-prompt")
#fakes.scale_factor = 1.0
#fakes.set_treename("superNt")
#fakes.set_file(fake_rawdir + "CENTRAL_fakes.3body_v02.root")
#fakes.set_merged_tree("superNt")
#fakes.set_color(r.kGray+1)
#fakes.set_fillStyle(0)
#fakes.setLineStyle(1)
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


#### DATA
data = background.Data()
data.set_color(r.kBlack)
data.set_treename("Data")
data.set_chain_from_list_CONDOR(filelist_dir + "dataToRun/", data_rawdir)


##########################################
# systematics
##########################################
systematics = []



##########################################
# regions
##########################################
regions = []

isEE = "(nElectrons==2 && abs(mll-91.2)>20) && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"
isMM = "(nMuons==2 && abs(mll-91.2)>20) && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"
isSFOS = "( ( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20) ) && abs(mll-91.2)>20 && (l_q[0]*l_q[1])<0)"
isDFOS = "(nElectrons==1 && nMuons==1) && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"

trigger = "((year==2015 && trig_pass2015==1) || (year==2016 && trig_pass2016update==1))"

reg = region.Region()
reg.name = "srwPreselEE"
reg.displayname = "SRw-type Preselection (ee)"
reg.tcut = "nLeptons==2 && " + isEE + " && nBJets==0 && MDR>30 && RPT>0.5 && " + trigger 
regions.append(reg)


reg = region.Region()
reg.name = "srwPreselMM"
reg.displayname = "SRw-type Preselection (#mu#mu)"
reg.tcut = "nLeptons==2 && " + isMM + " && nBJets==0 && MDR>30 && RPT>0.5 && " + trigger
regions.append(reg)

reg = region.Region()
reg.name = "srwPreselDF"
reg.displayname = "SRw-type Preselection (e#mu)"
reg.tcut = "nLeptons==2 && " + isDFOS + " && nBJets==0 && MDR>30 && RPT>0.5 && " + trigger 
regions.append(reg)

reg = region.Region()
reg.name = "srtPreselEE"
reg.displayname = "SRt-type Preselection (ee)"
reg.tcut = "nLeptons==2 && " + isEE + " && nBJets>0 && MDR>30 && RPT>0.5 && " + trigger 
regions.append(reg)


reg = region.Region()
reg.name = "srtPreselMM"
reg.displayname = "SRt-type Preselection (#mu#mu)"
reg.tcut = "nLeptons==2 && " + isMM + " && nBJets>0 && MDR>30 && RPT>0.5 && " + trigger 
regions.append(reg)

reg = region.Region()
reg.name = "srtPreselDF"
reg.displayname = "SRt-type Preselection (e#mu)"
reg.tcut = "nLeptons==2 && " + isDFOS + " && nBJets>0 && MDR>30 && RPT>0.5 && " + trigger 
regions.append(reg)


reg = region.Region()
reg.name = "dfprebv"
reg.displayname = "DF Preselection + b-veto"
reg.tcut = "nLeptons==2 && " + isDFOS + " && nBJets==0 && mll>20 && " + trigger 
regions.append(reg)

reg = region.Region()
reg.name = "sfprebv"
reg.displayname = "DF Preselection + b-veto"
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
reg.displayname = "DF Preselection + >0 b-jets"
reg.tcut = "nLeptons==2 && " + isDFOS + " && nBJets>0 && mll>20 && " + trigger 
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
reg.displayname = "CR-VV (DF)"
reg.tcut = isDFOS + " && nBJets==0 && MDR>30 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && RPT<0.5  && gamInvRp1>0.8 && mll>20 && " + trigger
regions.append(reg)

reg = region.Region()
reg.name = "crvSF"
reg.displayname = "CR-VV (SF)"
reg.tcut = isSFOS + " && nBJets==0 && MDR>30 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && RPT<0.5 && gamInvRp1>0.8 && met>70 && mll>20 && " + trigger
regions.append(reg)


reg = region.Region()
reg.name = "vrv"
reg.displayname = "VR-VV (DF)"
reg.tcut = isDFOS + " && nBJets==0 && MDR>30 && MDR<80 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && RPT<0.5 && gamInvRp1>0.8 && mll>20 && " + trigger
regions.append(reg)

reg = region.Region()
reg.name = "vrvSF"
reg.displayname = "VR-VV (SF)"
reg.tcut = isSFOS + " && nBJets==0 && MDR>30 && MDR<80 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && RPT<0.5 && gamInvRp1>0.8 && met>70 && mll>20 && " + trigger
regions.append(reg)

reg = region.Region()
reg.name = "crt"
reg.displayname = "CR-T"
reg.tcut = isDFOS + " && nBJets>0 && MDR>80 && RPT>0.5 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && mll>20 && " + trigger
regions.append(reg)

reg = region.Region()
reg.name = "vrt"
reg.displayname = "VR-T"
reg.tcut = isDFOS + " && nBJets==0 && MDR>80 && RPT<0.5 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && mll>20 && " + trigger
regions.append(reg)



##########################################
# plots
##########################################
plots = []


vars = {}
#vars["l_pt[0]"]         = { "dfprebv" : [40, 20,500,1e7] ,"dfpreb" : [40, 20,500,1e7] ,"crt" : [10, 20, 500, 1e4]  , "vrt" : [20,20,250,   30]    , "crv" : [10, 20, 100,    60]  ,"crvSF" : [15, 30, 105,    50]  , "vrv" : [5,20,70,     25], "vrvSF" : [5,20,70,     25]}
#vars["l_pt[1]"]         = { "dfprebv" : [40,20,500, 1e7] ,"dfpreb" : [40,20,500, 1e7] ,"crt" : [10, 20, 200, 1e4]  , "vrt" : [10,20,130,   40]    , "crv" : [4, 20, 60,      55]  ,"crvSF" : [8, 20, 70,     50]   , "vrv" : [2,20,40,     20], "vrvSF" : [4,20,40,     20]}
#vars["MDR" ]            = { "dfprebv" : [10,0,200,  1e7] ,"dfpreb" : [10,0,200,  1e7] ,"crt" : [ 5, 80,160, 1e4]   , "vrt" : [5,80,125,    50]    , "crv" : [10,  30, 120,   50]  ,"crvSF" : [10, 50, 130,     40] , "vrv" : [10,30,80,    40], "vrvSF" : [10,30,80,    40]}
#vars["DPB_vSS"]         = { "dfprebv" : [0.2,0,3.2, 1e7] ,"dfpreb" : [0.2,0,3.2, 1e7] ,"crt" : [0.1, 0, 2.8, 1e4]  , "vrt" : [0.2,1.8,3.2, 40]    , "crv" : [0.5, 0, 2.8,    50]  ,"crvSF" : [0.5, 0, 2.8,    40]  , "vrv" : [0.2,1.8,3.2, 35], "vrvSF" : [0.2,1.8,3.2, 30]}
#vars["gamInvRp1"]       = { "dfprebv" : [0.05,0,1,  1e7] ,"dfpreb" : [0.05,0,1,  1e7] ,"crt" : [0.1, 0, 1, 1e4]    , "vrt" : [0.1,0,1,     35]    , "crv" : [0.02, 0.8, 1,   40]  ,"crvSF" : [0.04, 0.8, 1,   50]  , "vrv" : [0.05,0.8,1,  40], "vrvSF" : [0.05,0.8,1,  40]}
#vars["abs(cosThetaB)"]  = { "dfprebv" : [0.05,0,1,  1e7] ,"dfpreb" : [0.05,0,1,  1e7] ,"crt" : [0.05, 0, 1, 1e4]   , "vrt" : [0.1,0,1,     25]    , "crv" : [0.15, 0, 1,     55]  ,"crvSF" : [0.2, 0, 1,      40]  , "vrv" : [0.2,0,1,     25], "vrvSF" : [0.2,0,1,     25]}
#vars["RPT"]             = { "dfprebv" : [0.05,0,1,  1e7] ,"dfpreb" : [0.05,0,1,  1e7] ,"crt" : [0.05, 0.5, 1, 1e4] , "vrt" : [0.05,0,0.5,  40]    , "crv" : [0.1, 0, 0.5,    65]  ,"crvSF" : [0.1, 0, 0.5,    60]  , "vrv" : [0.1,0,0.5,30], "vrvSF" : [0.1,0,0.5, 30]}
#vars["nSJets"]          = { "dfprebv" : [1, 0,15,   1e7] ,"dfpreb" : [1, 0,15,   1e7] ,"crt" : [1, 0, 10, 1e4]     , "vrt" : [1,0,10,      40]    , "crv" : [1, 0, 7,        90]  ,"crvSF" : [1, 0, 7,        40]  , "vrv" : [1,0,7,       40], "vrvSF" : [1,0,7,       30]}
#vars["nBJets"]          = { "dfprebv" : [1, 0,3,    1e7] ,"dfpreb" : [1, 0,6,    1e7] ,"crt" : [1, 0, 10, 1e4]     , "vrt" : [1,0,3,       100]   , "crv" : [1, 0, 3,       175]  ,"crvSF" : [1, 0, 3,       120]  , "vrv" : [1,0,3,      100], "vrvSF" : [1,0,3,      100]}
#vars["met"]             = { "dfprebv" : [30,0,500,  1e7] ,"dfpreb" : [30,0,500,  1e7] ,"crt" : [30,0,400,1e4]      , "vrt" : [10,80,250,   25]    , "crv" : [10, 30, 120,    50]  ,"crvSF" : [10, 70, 135,    55]  , "vrv" : [10,40,100,   35], "vrvSF" : [5,70,110,   20]}
#vars["mll"]             = { "dfpreb" : [10,0,300,1e7],   "dfprebv" : [10,0,300,1e7],   "crt" : [10,0,120,1e4], "vrv" : [5, 20, 60, 30], "crv" : [5, 20, 70, 60], "crvSF" : [8, 20, 80, 40] , "vrvSF" : [5, 20, 60, 25] }
vars["nVtx"]            = { "dfpreb" : [1,0,40,1e7], "dfprebv" : [1,0,40,1e7], "crt" : [1, 0, 40, 1e7], "vrt" : [1,0,40,1e7],  "crv" : [1,0,40,1e7], "crvSF" : [1,0,40,1e7], "vrv" : [1,0,40,1e7], "vrvSF" : [1,0,40,1e7]}



##vars["nVtx"] = { "dfpresel" : [1,0,35,1e7]}
##vars["avgMu"] = { "dfpresel" : [1,0,35,1e7]}
#vars["l_pt[0]"]         = { "crt" : [20, 0, 500, 1e6],   "vrt" : [15, 20, 300,200],      "crv" : [5, 20, 120, 110],      "vrv" : [4, 20, 80, 40] }
#vars["l_pt[1]"]         = { "crt" : [12, 0, 200, 1e6],   "vrt" : [5, 20, 130, 200],      "crv" : [2, 20, 60, 110],        "vrv" : [2, 20, 60, 50] }
##vars["l_eta[0]"]        = { "crv" : [0.2, -3, 3, 80] }
##vars["l_eta[1]"]        = { "crv" : [0.2, -3, 3, 80] }
#vars["MDR"]             = { "dfpreselMT" : [10, 0, 180, 1e7], "dfpresel" : [10, 0, 180, 1e7], "crt" : [10, 30, 200, 1e6],   "vrt" : [5, 30, 115, 110],      "crv" : [5, 30, 100, 100],       "vrv" : [4, 30, 100, 50] }
#vars["DPB_vSS"]         = { "dfpreselMT" : [0.1, 0, 3.2,1e7 ],"dfpresel" : [0.1, 0, 3.2,1e7 ], "crt" : [.1, 0, 2.8, 1e6],   "vrt" : [.1, 1.6, 3.2, 120],   "crv" : [.14, 0, 3.2, 80],    "vrv" : [.1, 1.6, 3.2, 50] }
##vars["DPB_vSS"]         = { "dfpreselMT" : [0.1, 0, 3.2,1e7 ],"dfpresel" : [0.1, 0, 3.2,1e7 ], "crt" : [.1, 0, 2.8, 1e6],   "vrt" : [.1, 1.6, 3.2, 120],   "crv" : [.14, 0.8, 2.7, 80],    "vrv" : [.1, 1.6, 3.2, 100] }
#vars["gamInvRp1"]       = { "dfpreselMT" : [ 0.05, 0, 1,1e7], "dfpresel" : [ 0.05, 0, 1,1e7], "crt" : [.05, 0, 1,  1e6],   "vrt" : [.05, 0, 1,  120],     "crv" : [.02, 0.5, 1,  75],       "vrv" : [.02, 0.5, 1,  30] }
#vars["abs(cosThetaB)"]  = { "dfpreselMT" : [ 0.05, 0, 1,1e7], "dfpresel" : [ 0.05, 0, 1,1e7], "crt" : [.05, 0, 1,  1e7],   "vrt" : [.05, 0, 1,  80 ],     "crv" : [.05, 0, 1,  60],       "vrv" : [.05, 0, 1,  30] } 
##vars["RPT"]             = { "dfpreselMT" : [ 0.05, 0, 1,1e7], "dfpresel" : [ 0.05, 0, 1,1e7], "crt" : [.02, 0.5, 1,1e7],   "vrt" : [.04, 0, 0.5, 175],    "crv" : [.04, 0, 1,55],      "vrv" : [.02, 0, 0.5,  65] }
#vars["RPT"]             = { "dfpreselMT" : [ 0.05, 0, 1,1e7], "dfpresel" : [ 0.05, 0, 1,1e7], "crt" : [.02, 0.5, 1,1e7],   "vrt" : [.04, 0, 0.5, 175],    "crv" : [.02, 0.2, 0.5,75],      "vrv" : [.04, 0, 0.5,  40] }
#vars["nSJets"]          = { "crt" : [1, 0, 10, 1e7],     "vrt" : [1, 0, 10,   420],     "crv" : [1, 0, 3,   360],      "vrv" : [1, 0, 5,   250]   }
#vars["nBJets"]          = { "dfpreselMT" : [1, 0, 8, 1e7], "dfpresel" : [1, 0, 8, 1e7], "crt" : [1, 0, 10, 1e7],     "vrt" : [1, 0, 10,   1000],    "crv" : [1, 0, 5,   700],      "vrv" : [1, 0, 5,   250]   }


run_reg = "crvSF"

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
    p.setDefaultCanvas(p.name)
    #p.setRatioCanvas(p.name)
    plots.append(p)
