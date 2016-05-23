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
rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0222/apr17/mc/Raw/"
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0222/nom/data/Raw/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0222val/filelists/"


lumi_ = [1.0]
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
stop = background.Background("ttV", "tt+V")
stop.set_debug()
stop.scale_factor = lumi_[lumi_val]
stop.set_fillStyle(0)
stop.setLineStyle(1)
stop.set_color(46)
stop.set_treename("TTV")
stop.set_chain_from_list_CONDOR(filelist_dir+ "ttV/", rawdir)
backgrounds.append(stop)

# diboson
diboson = background.Background("vv", "VV (Sherpa)")
diboson.set_debug()
diboson.scale_factor = lumi_[lumi_val]
diboson.set_fillStyle(0)
diboson.setLineStyle(1)
diboson.set_color(r.TColor.GetColor("#41C1FC"))
diboson.set_treename("diboson_sherpa")
diboson.set_chain_from_list_CONDOR(filelist_dir+ "diboson_sherpa/", rawdir)
backgrounds.append(diboson)


# Zjets
zjets = background.Background("zjets", "Z+jets (Sherpa)")
zjets.set_debug()
zjets.scale_factor = lumi_[lumi_val]
zjets.set_fillStyle(0)
zjets.setLineStyle(1)
zjets.set_color(r.TColor.GetColor("#FFEF53"))
zjets.set_treename("zjets_sherpa")
zjets.set_chain_from_list_CONDOR(filelist_dir+ "zjets_sherpa/", rawdir)
backgrounds.append(zjets)

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

#sig1 = background.Background("bwn250_160", "(250,160)")
#sig1.setSignal()
#sig1.set_debug()
#sig1.scale_factor = lumi_[lumi_val]
#sig1.set_fillStyle(0)
#sig1.setLineStyle(2)
#sig1.set_color(r.kBlue)
#sig1.set_treename("sig1")
#sig1.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", rawdir, "406009")
#backgrounds.append(sig1)
#
#sig2 = background.Background("bwn300_180", "(300,180)")
#sig2.setSignal()
#sig2.set_debug()
#sig2.scale_factor = lumi_[lumi_val]
#sig2.setLineStyle(2)
#sig2.set_color(r.kGreen)
#sig2.set_treename("sig2")
#sig2.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", rawdir, "406011")
#backgrounds.append(sig2)
#
#sig3 = background.Background("bwn300_150", "(300,150)")
#sig3.setSignal()
#sig3.set_debug()
#sig3.scale_factor = lumi_[lumi_val]
#sig3.setLineStyle(2)
#sig3.set_color(r.kBlack)
#sig3.set_treename("sig3")
#sig3.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "406010")
#backgrounds.append(sig3)


#### DATA
data = background.Data()
data.set_color(r.kBlack)
data.set_treename("Data")
data.set_chain_from_list_CONDOR(filelist_dir + "n0222_data/", data_rawdir)


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
## muons
#syst = systematic.Systematic("MUONS_ID", "UP", "DN")
#syst.setKinSys()
#systematics.append(syst)
#
#syst = systematic.Systematic("MUONS_MS", "UP", "DN")
#syst.setKinSys()
#systematics.append(syst)
#
#syst = systematic.Systematic("MUONS_SCALE", "UP", "DN")
#syst.setKinSys()
#systematics.append(syst)
## jets
##syst = systematic.Systematic("JER", "", "")
##syst.setOneSided()
##syst.setKinSys()
##systematics.append(syst)
#
#syst = systematic.Systematic("JET_GroupedNP_1", "UP", "DN")
#syst.setKinSys()
#systematics.append(syst)
#
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

#syst = systematic.Systematic("MET_SoftTrk_Scale", "Up", "Down")
#syst.setKinSys()
#systematics.append(syst)



######################
### weight systematics
######################

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
#syst = systematic.Systematic("JET_JVTEff", "UP", "DOWN")
#syst.setWeightSys()
#systematics.append(syst)
#
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

isEE = "(nElectrons==2 && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0"
isMM = "(nMuons==2 && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0"
isSF = "((nMuons==2 || nElectrons==2) && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"
isDF = "(nElectrons==1 && nMuons==1) && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"

reg = region.Region()
reg.name = "dfpresel"
reg.displayname = "DF Preselection + b-veto"
reg.tcut = "nLeptons==2 && " + isDF + " && nBJets==0"
regions.append(reg)

reg = region.Region()
reg.name = "dfpreselMT"
reg.displayname = "DF Preselection + >0 b-jets"
reg.tcut = "nLeptons==2 && " + isDF + " && nBJets>0"
regions.append(reg)



isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && l_pt[0]>20 && l_pt[1]>20 && (l_q[0]*l_q[1])<0"

reg = region.Region()
reg.name = "crv"
reg.displayname = "CR-VV"

reg.tcut = isDFOS + " && nBJets==0 && MDR>30 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && RPT<0.5 && RPT>0.2 && gamInvRp1>0.5 && nSJets<3"


#reg.tcut = isDFOS + " && nBJets==0 && MDR>30 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && RPT<0.50 && RPT>0.2 && gamInvRp1>0.5 && nSJets<3"
#reg.tcut = isDFOS + " && nBJets==0 && MDR>30 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && DPB_vSS>(0.85*abs(cosThetaB)+0.5) && RPT<0.5 && RPT>0.1 && gamInvRp1>0.5 && nSJets<3"

#reg.tcut = isDFOS + " && nBJets==0 && nSJets<3 && MDR>40 && DPB_vSS>1.5 && abs(cosThetaB)>0.55 && RPT<0.5" 
#reg.tcut = isDFOS + " && nBJets==0 && nSJets<3 && MDR>30 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && DPB_vSS>(0.85*abs(cosThetaB)+1) && abs(cosThetaB)>0.25"

#reg.tcut = isDFOS + " && nBJets==0 && nSJets<3 && MDR>30 && RPT<0.5 && DPB_vSS>1.8 && abs(cosThetaB)>0.5"
#reg.tcut = isDFOS + " && nBJets==0 && MDR>30 && gamInvRp1<0.5 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && l_pt[0]>30"
#reg.tcut = isDFOS + " && nBJets==0 && MDR>30 && RPT<0.5 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && RPT>0.1 && nSJets<3" #&& DPB_vSS>(0.85*abs(cosThetaB)+1) && RPT>0.1 && nSJets<3"

# test 1
#reg.tcut = isDFOS + " && nBJets==0 && MDR>30 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && DPB_vSS>1.8 && RPT<0.5 && RPT>0.1"

# origin
#reg.tcut = isDFOS + " && nSJets==0 && nBJets==0 && MDR>30 && RPT<0.5 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && DPB_vSS>(0.85*abs(cosThetaB)+1)"
regions.append(reg)

reg = region.Region()
reg.name = "vrv"
reg.displayname = "VR-VV"
reg.tcut = isDFOS + " && nBJets==0 && MDR>30 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && RPT<0.5 && gamInvRp1>0.5 && nSJets==0"
#reg.tcut = isDFOS + " && nBJets==0 && nSJets<3 && MDR>30 && RPT<0.5 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && abs(cosThetaB)<0.5"
#origin
#reg.tcut = isDFOS + " && nSJets==0 && nBJets==0 && MDR>30 && RPT<0.5 && DPB_vSS>(0.85*abs(cosThetaB)+1.8)"
regions.append(reg)

reg = region.Region()
reg.name = "crt"
reg.displayname = "CR-T"
reg.tcut = isDFOS + " && nSJets>=0 && nBJets>0 && MDR>30 && RPT>0.5 && DPB_vSS<(0.85*abs(cosThetaB)+1.8)"
regions.append(reg)

reg = region.Region()
reg.name = "vrt"
reg.displayname = "VR-T"
reg.tcut = isDFOS + " && nSJets>0 && nBJets==0 && MDR>30 && RPT<0.5 && DPB_vSS>(0.85*abs(cosThetaB)+1.8)"
regions.append(reg)




##########################################
# plots
##########################################
plots = []

#logy = 1100
#do_log_y = False
#y_ax_min = 0
#if "ttbar" in reg_name  :
#    logy = 1e5
#    do_log_y = True
#    y_ax_min = 0.1

vars = {}
vars["l_pt[0]"]         = { "crt" : [20, 0, 500, 1e6],   "vrt" : [15, 20, 300,200],      "crv" : [5, 20, 120, 110],      "vrv" : [4, 20, 80, 40] }
vars["l_pt[1]"]         = { "crt" : [12, 0, 200, 1e6],   "vrt" : [5, 20, 130, 200],      "crv" : [2, 20, 60, 110],        "vrv" : [2, 20, 60, 50] }
#vars["l_eta[0]"]        = { "crv" : [0.2, -3, 3, 80] }
#vars["l_eta[1]"]        = { "crv" : [0.2, -3, 3, 80] }
vars["MDR"]             = { "dfpreselMT" : [10, 0, 180, 1e7], "dfpresel" : [10, 0, 180, 1e7], "crt" : [10, 30, 200, 1e6],   "vrt" : [5, 30, 115, 110],      "crv" : [5, 30, 100, 100],       "vrv" : [4, 30, 100, 50] }
vars["DPB_vSS"]         = { "dfpreselMT" : [0.1, 0, 3.2,1e7 ],"dfpresel" : [0.1, 0, 3.2,1e7 ], "crt" : [.1, 0, 2.8, 1e6],   "vrt" : [.1, 1.6, 3.2, 120],   "crv" : [.14, 0, 3.2, 80],    "vrv" : [.1, 1.6, 3.2, 50] }
#vars["DPB_vSS"]         = { "dfpreselMT" : [0.1, 0, 3.2,1e7 ],"dfpresel" : [0.1, 0, 3.2,1e7 ], "crt" : [.1, 0, 2.8, 1e6],   "vrt" : [.1, 1.6, 3.2, 120],   "crv" : [.14, 0.8, 2.7, 80],    "vrv" : [.1, 1.6, 3.2, 100] }
vars["gamInvRp1"]       = { "dfpreselMT" : [ 0.05, 0, 1,1e7], "dfpresel" : [ 0.05, 0, 1,1e7], "crt" : [.05, 0, 1,  1e6],   "vrt" : [.05, 0, 1,  120],     "crv" : [.02, 0.5, 1,  75],       "vrv" : [.02, 0.5, 1,  30] }
vars["abs(cosThetaB)"]  = { "dfpreselMT" : [ 0.05, 0, 1,1e7], "dfpresel" : [ 0.05, 0, 1,1e7], "crt" : [.05, 0, 1,  1e7],   "vrt" : [.05, 0, 1,  80 ],     "crv" : [.05, 0, 1,  60],       "vrv" : [.05, 0, 1,  30] } 
#vars["RPT"]             = { "dfpreselMT" : [ 0.05, 0, 1,1e7], "dfpresel" : [ 0.05, 0, 1,1e7], "crt" : [.02, 0.5, 1,1e7],   "vrt" : [.04, 0, 0.5, 175],    "crv" : [.04, 0, 1,55],      "vrv" : [.02, 0, 0.5,  65] }
vars["RPT"]             = { "dfpreselMT" : [ 0.05, 0, 1,1e7], "dfpresel" : [ 0.05, 0, 1,1e7], "crt" : [.02, 0.5, 1,1e7],   "vrt" : [.04, 0, 0.5, 175],    "crv" : [.02, 0.2, 0.5,75],      "vrv" : [.04, 0, 0.5,  40] }
vars["nSJets"]          = { "crt" : [1, 0, 10, 1e7],     "vrt" : [1, 0, 10,   420],     "crv" : [1, 0, 3,   360],      "vrv" : [1, 0, 5,   250]   }
vars["nBJets"]          = { "dfpreselMT" : [1, 0, 8, 1e7], "dfpresel" : [1, 0, 8, 1e7], "crt" : [1, 0, 10, 1e7],     "vrt" : [1, 0, 10,   1000],    "crv" : [1, 0, 5,   700],      "vrv" : [1, 0, 5,   250]   }
#vars["bj_pt[0]"]    = { "crt" : [10, 0, 200, 1e7] }
#vars["bj_pt[1]"]    = { "crt" : [10, 0, 200, 1e7] }
#vars["bj_pt[2]"]    = { "crt" : [10, 0, 200, 1e7] }
#vars["bj_pt[3]"]    = { "crt" : [10, 0, 200, 1e7] }
#vars["bj_pt[4]"]    = { "crt" : [10, 0, 200, 1e7] }
#vars["bj_pt[5]"]    = { "crt" : [10, 0, 200, 1e7] }
#vars["bj_pt[6]"]    = { "crt" : [10, 0, 200, 1e7] }


run_reg = "crt"

nice_names = {}
nice_names["MDR"] = "E_{V}^{P} [GeV]"
nice_names["DPB_vSS"] = "#Delta#phi(#vec{#beta}_{PP}^{LAB}, #vec{p}_{V}^{PP})"
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
    if "crt" in run_reg or "dfpresel" in run_reg:
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
