import sys
sys.path.append(os.environ['SUSYDIR'])
import supersusy.utils.plot as plot
import supersusy.utils.background as background
import supersusy.utils.region as region
import supersusy.utils.systematic as systematic


#######################################
# samples
#######################################
mc_file = "/data/uclhc/uci/user/dantrim/n0222val/SuperFitter/HFT_BG_13TeV.root"
backgrounds = []


######## MC

# ttbar
ttbar = background.Background("TTbar", "t#bar{t}")
ttbar.set_file(mc_file)
ttbar.set_treename("TTbar")
ttbar.set_central_tree_from_merged()
ttbar.scale_factor = 1.0
backgrounds.append(ttbar)

# Z+jets
zjets = background.Background("Zjets", "Z+jets (Sherpa)")
zjets.set_file(mc_file)
zjets.set_treename("Zjets")
zjets.set_central_tree_from_merged()
zjets.scale_factor = 1.0
backgrounds.append(zjets)

# W+jets
wjets = background.Background("Wjets", "W+jets (Sherpa)")
wjets.set_file(mc_file)
wjets.set_treename("Wjets")
wjets.set_central_tree_from_merged()
wjets.scale_factor = 1.0
backgrounds.append(wjets)

# diboson
diboson = background.Background("VV", "VV (Sherpa)")
diboson.set_file(mc_file)
diboson.set_treename("VV")
diboson.set_central_tree_from_merged()
diboson.scale_factor = 1.0
backgrounds.append(diboson)

# singletop
stop = background.Background("ST", "st + Wt")
stop.set_file(mc_file)
stop.set_treename("ST")
stop.set_central_tree_from_merged()
stop.scale_factor = 1.0
backgrounds.append(stop)


##########################################
# systematics
##########################################
systematics = []

syst = systematic.Systematic("PILEUP", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)

syst = systematic.Systematic("EG_RESOLUTION_ALL", "UP", "DN")
syst.setKinSys()
#syst.setOneSided()
systematics.append(syst)

syst = systematic.Systematic("FT_EFF_B", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)

syst = systematic.Systematic("JER", "","")
syst.setKinSys()
syst.setOneSided()
systematics.append(syst)



##########################################
# regions
##########################################
regions = []

isEE = "(nElectrons==2 && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0"
isMM = "(nMuons==2 && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0"
isSF = "((nMuons==2 || nElectrons==2) && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"
isDF = "(nElectrons==1 && nMuons==1) && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"

reg = region.Region()
reg.name = "crt"
reg.displayname = "CR-Top"
reg.tcut = "nLeptons==2 && " + isDF + " && nBJets>0 && MDR>30 && RPT>0.5 && DPB_vSS<(0.8*abs(cosThetaB)+1.8)"
regions.append(reg)

reg = region.Region()
reg.name = "vrt"
reg.displayname = "VR-Top"
reg.tcut = "nLeptons==2 && " + isDF + " && nBJets==0 && nSJets>0 && MDR>30 && RPT<0.5 && DPB_vSS>(0.8*abs(cosThetaB)+1.8)"
regions.append(reg)

reg = region.Region()
reg.name = "crv"
reg.displayname = "CR-VV"
reg.tcut = "nLeptons==2 && " + isDF + " && nBJets==0 && nSJets==0 && MDR>30 && RPT<0.5 && DPB_vSS<(0.8*abs(cosThetaB)+1.8) && DPB_vSS>(0.8*abs(cosThetaB)+1)"
regions.append(reg)

reg = region.Region()
reg.name = "vrv"
reg.displayname = "VR-VV"
reg.tcut = "nLeptons==2 && " + isDF + " && nBJets==0 && nSJets==0 && MDR>30 && RPT<0.5 && DPB_vSS>(0.8*abs(cosThetaB)+1.8)"
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
vars["l_pt[0]"]         = { "crt" : [20, 0, 500, 1e6],   "vrt" : [15, 0, 300,200],      "crv" : [10, 0, 185, 110],      "vrv" : [10, 0, 200, 180] }
vars["l_pt[1]"]         = { "crt" : [12, 0, 200, 1e6],   "vrt" : [8, 0, 220, 200],      "crv" : [5, 0, 80, 110],        "vrv" : [5, 0, 100, 160] }
vars["MDR"]             = { "crt" : [10, 0, 200, 1e6],   "vrt" : [5, 0, 140, 140],      "crv" : [5, 0, 100, 120],       "vrv" : [5, 0, 100, 100] }
vars["DPB_vSS"]         = { "crt" : [.1, 0, 2.8, 1e6],   "vrt" : [.1, 1.6, 3.2, 120],   "crv" : [.14, 0.8, 2.7, 80],    "vrv" : [.1, 1.6, 3.2, 100] }
vars["gamInvRp1"]       = { "crt" : [.05, 0, 1,  1e6],   "vrt" : [.05, 0, 1,  120],     "crv" : [.05, 0, 1,  70],       "vrv" : [.05, 0, 1,  100] }
vars["abs(cosThetaB)"]  = { "crt" : [.05, 0, 1,  1e7],   "vrt" : [.05, 0, 1,  80 ],     "crv" : [.05, 0, 1,  55],       "vrv" : [.05, 0, 1,  80] } 
vars["RPT"]             = { "crt" : [.02, 0.5, 1,1e7],   "vrt" : [.04, 0, 0.5, 175],    "crv" : [.02, 0, 0.45,55],      "vrv" : [.02, 0, 0.5,  65] }
vars["nSJets"]          = { "crt" : [1, 0, 10, 1e7],     "vrt" : [1, 0, 10,   420],     "crv" : [1, 0, 10,   200],      "vrv" : [1, 0, 10,   200]   }
vars["nBJets"]          = { "crt" : [1, 0, 10, 1e7],     "vrt" : [1, 0, 10,   1000],    "crv" : [1, 0, 10,   200],      "vrv" : [1, 0, 10,   200]   }

run_reg = "vrt"

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
    p.labels(x=name_, y = "Entries / %s"%(str(bounds[run_reg][0])))
    p.xax(bounds[run_reg][0], bounds[run_reg][1], bounds[run_reg][2])
    if "crt" in run_reg:
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
