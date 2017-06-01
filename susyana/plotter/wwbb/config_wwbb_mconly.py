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

rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0232/c_apr27/mc/Raw/"
signal_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0232/d_may15/mc/Raw/" 
#diboson_rawdir_DF = "/data/uclhc/uci/user/dantrim/ntuples/n0232/b_mar7/mc/diboson_DF/Raw/"
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0232/b_mar7/data/Raw/"
#zjets_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0232/b_mar7/mc/zjets_window/Raw//"

filelist_dir = "/data/uclhc/uci/user/dantrim/n0232val/filelists/"

lumi_ = [36.01] 
lumi_val = 0

######## MC
## ttbro
ttbar = background.Background("ttbar", "t#bar{t}")
ttbar.set_debug()
ttbar.scale_factor = lumi_[lumi_val]#
ttbar.set_fillStyle(0)
ttbar.setLineStyle(1)
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
stop.set_color(r.TColor.GetColor("#db101c"))
stop.set_treename("ST")
stop.set_chain_from_list_CONDOR(filelist_dir+ "singletop/", rawdir)
backgrounds.append(stop)

# ttV
ttv = background.Background("ttV", "t#bar{t}+V")
ttv.set_debug()
ttv.scale_factor = lumi_[lumi_val]
ttv.set_fillStyle(0)
ttv.setLineStyle(1)
ttv.set_color(r.TColor.GetColor("#9bcdfd"))
ttv.set_treename("TTV")
ttv.set_chain_from_list_CONDOR(filelist_dir+ "ttV/", rawdir)
backgrounds.append(ttv)

# diboson
diboson = background.Background("vvSFDF", "VV")
diboson.set_debug()
diboson.scale_factor = lumi_[lumi_val] #* 1.06
diboson.set_fillStyle(0)
diboson.setLineStyle(1)
diboson.set_color(r.TColor.GetColor("#325f85"))
diboson.set_treename("diboson_sherpa_SFDF")
diboson.set_chain_from_list_CONDOR(filelist_dir+ "diboson_sherpa/", rawdir)
#diboson.set_chain_from_list_CONDOR(filelist_dir+ "diboson_new_check/", diboson_rawdir_SF)
backgrounds.append(diboson)

# Zjets
zjets = background.Background("zjetsDY", "Z/#gamma*+jets")
zjets.set_debug()
zjets.scale_factor = lumi_[lumi_val]
zjets.set_fillStyle(0)
zjets.setLineStyle(1)
zjets.set_color(r.TColor.GetColor("#85dc6e"))
zjets.set_treename("zjets_sherpa")
zjets.set_chain_from_list_CONDOR(filelist_dir+ "zjets_and_DY/", rawdir)
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
higgs = background.Background("higgs", "Higgs")
higgs.scale_factor = lumi_[lumi_val]
higgs.set_fillStyle(0)
higgs.setLineStyle(1)
higgs.set_color(r.kGreen-9)
higgs.set_treename("higgs")
higgs.set_chain_from_list_CONDOR(filelist_dir+ "higgs/", rawdir)
backgrounds.append(higgs)

#fakes = background.Background("fakes", "FNP")
#fakes.scale_factor = 1.0 # Feb 7 2017 - fakes are full dataset, yo
##fakes.scale_factor = 2.95 # scale from 12.2/fb to 36/fb
#fakes.set_treename("superNt")
##fakes.set_file(fake_rawdir + "physics_Main_276262_303560_FakesInclusive.root")
##fakes.set_file(fake_rawdir + "fakes_3body.root")
#fakes.set_file(fake_rawdir + "fakes_3body_mar10_361ifb.root")
#fakes.set_merged_tree("superNt")
#fakes.set_color(94) # stop-2l uglify for Moriond
##fakes.set_color(r.kOrange+7)
#fakes.set_fillStyle(0)
#fakes.setLineStyle(1)
#backgrounds.append(fakes)

s0 = background.Background("hhSM", "SM hh")
s0.setSignal()
s0.scale_factor = lumi_[lumi_val] * 10
s0.set_fillStyle(0)
s0.set_color(r.kBlue)
s0.set_treename("s0")
s0.set_chain_from_list_CONDOR(filelist_dir + "wwbb_susy2/", signal_rawdir, "342053")
backgrounds.append(s0)

s1 = background.Background("hhX400", "X 400 GeV")
s1.setSignal()
s1.scale_factor = lumi_[lumi_val] * 10
s1.set_fillStyle(0)
s1.set_color(r.kRed)
s1.set_treename("s1")
s1.set_chain_from_list_CONDOR(filelist_dir + "wwbb_susy2/", signal_rawdir, "343769")
backgrounds.append(s1)

s2 = background.Background("hhX600", "X 600 GeV")
s2.setSignal()
s2.scale_factor = lumi_[lumi_val] * 10
s2.set_fillStyle(0)
s2.set_color(r.kGreen)
s2.set_treename("s2")
s2.set_chain_from_list_CONDOR(filelist_dir + "wwbb_susy2/", signal_rawdir, "343772")
backgrounds.append(s2)

s3 = background.Background("hhX800", "X 800 GeV")
s3.setSignal()
s3.scale_factor = lumi_[lumi_val] * 10
s3.set_fillStyle(0)
s3.set_color(r.kMagenta)
s3.set_treename("s3")
s3.set_chain_from_list_CONDOR(filelist_dir + "wwbb_susy2/", signal_rawdir, "343775")
backgrounds.append(s3)

s4 = background.Background("hhX1000", "X 1000 GeV")
s4.setSignal()
s4.scale_factor = lumi_[lumi_val] * 10
s4.set_fillStyle(0)
s4.set_color(r.kBlack)
s4.set_treename("s4")
s4.set_chain_from_list_CONDOR(filelist_dir + "wwbb_susy2/", signal_rawdir, "343777")
backgrounds.append(s4)


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
#data = background.Data()
#data.set_color(r.kBlack)
#data.set_treename("data")
#data.set_chain_from_list_CONDOR(filelist_dir + "data/", data_rawdir)
#data.set_chain_from_list_CONDOR2([filelist_dir + "data15ToRun/", filelist_dir + "data16ToRun/"] , [data15_rawdir, data16_rawdir])


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

isSFOS = "(( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && abs(mll-91.2)>10 && (l_q[0]*l_q[1])<0)"
isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<0"
trigger = "((year==2015 && trig_pass2015==1) || (year==2016 && trig_pass2016update==1))"

reg = region.Region()
reg.name = "wwbbpre"
reg.displayname = "WWbb (pre, dphi_ll<1.5, mbb, mt2llbb)"
reg.tcut = "((%s) || (%s)) && %s && nBJets==2 && mll>20 && mbb>80 && mbb<140 && mt2_llbb>100 && mt2_llbb<150 && dR_ll_bb>2.2 && dRbb<1.25 && dRll<1 && HT2Ratio>0.8 && abs(dphi_met_ll)<1.25"%(isSFOS, isDFOS, trigger)
regions.append(reg)

##########################################
# plots
##########################################
plots = []

vars = {}
#usual
vars["l_pt[0]"]         = { "wwbbpre" : [20, 0, 500, 1e6] }
vars["l_pt[1]"]         = { "wwbbpre" : [20, 0, 500, 1e6] }
vars["pTll"]            = { "wwbbpre" : [20, 0, 1000, 1e6] }
vars["nJets"]           = { "wwbbpre" : [1, 0, 12, 1e6] }
vars["nBJets"]          = { "wwbbpre" : [1, 0, 12, 1e6] }
vars["nSJets"]          = { "wwbbpre" : [1, 0, 12, 1e6] }

vars["bj_pt[0]"]        = { "wwbbpre" : [20, 0, 500, 1e6] }
vars["bj_pt[1]"]        = { "wwbbpre" : [20, 0, 500, 1e6] }

vars["sj_pt[0]"]        = { "wwbbpre" : [20, 0, 800, 1e6] }
vars["sj_pt[1]"]        = { "wwbbpre" : [20, 0, 800, 1e6] }


#sr-like
vars["mbb"]             = { "wwbbpre" : [20, 0, 1200, 1e6] }
vars["mll"]             = { "wwbbpre" : [20, 0, 1200, 1e6] }
vars["abs(dphi_ll)"]    = { "wwbbpre" : [0.1, 0, 3.2, 1e6] }
vars["abs(dphi_bb)"]    = { "wwbbpre" : [0.1, 0, 3.2, 1e6] }
vars["dRbb"]            = { "wwbbpre" : [0.1, 0, 6, 1e6] }
vars["dRll"]            = { "wwbbpre" : [0.1, 0, 6, 1e6] }
vars["dR_ll_bb"]        = { "wwbbpre" : [0.1, 0, 6, 1e6] }
vars["MT_1_scaled"]     = { "wwbbpre" : [40, 0, 1400, 1e6] }
vars["mt2_llbb"]        = { "wwbbpre" : [20, 0, 1000, 1e6] }
vars["HT2Ratio"]        = { "wwbbpre" : [0.05, 0, 1, 1e6] }
vars["abs(cosThetaB)"]  = { "wwbbpre" : [0.05, 0, 1, 1e6] }
vars["abs(dphi_met_ll)"]= { "wwbbpre" : [0.1, 0, 3.2, 1e6] }

run_reg = "wwbbpre"

nice_names = {}
#nice_names["mt2_llbb"] = "m_{t2}^{llbb} [GeV]"
for var in vars.keys() :
    nice_names[var] = var

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
    if run_reg=="wwbbpre" :
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
    #p.setRatioCanvas(p.name)
    p.setDefaultCanvas(p.name)
    plots.append(p)
