
import sys
sys.path.append('../../../../../')
import supersusy.utils.plot as plot
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region


#############################################
# Set up the samples
#############################################
rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0216/validation/mc/Raw/"
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0216/validation/data/Raw/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0216val/filelists/"
backgrounds = []

#### MC
# Zjets
zjets = background.Background("zjets", "Z+jets (PowHeg)")
zjets.set_debug()
zjets.scale_factor = 1
zjets.set_color(r.TColor.GetColor("#82DE68"))
zjets.set_treename("Zjets_powheg")
zjets.set_chain_from_list_CONDOR(filelist_dir + "zjets/", rawdir)
backgrounds.append(zjets)

ttbar = background.Background("ttbar", "TTbar")
ttbar.set_debug()
ttbar.scale_factor = 1.0
ttbar.set_color(r.TColor.GetColor("#E67067"))
ttbar.set_treename("ttbar_powheg")
ttbar.set_chain_from_list_CONDOR(filelist_dir + "ttbar/", rawdir)
backgrounds.append(ttbar)

# singletop
stop = background.Background("st", "ST")
stop.set_debug()
stop.scale_factor = 1.0
stop.set_color(r.TColor.GetColor("#DE080C"))
stop.set_treename("ST")
stop.set_chain_from_list_CONDOR(filelist_dir + "singletop/", rawdir)
backgrounds.append(stop)

# wjets
wjets = background.Background("wjets", "W+jets (PowHeg)")
wjets.set_debug()
wjets.scale_factor = 1.0
wjets.set_color(r.TColor.GetColor("#5E9AD6"))
wjets.set_treename("Wjets_powheg")
wjets.set_chain_from_list_CONDOR(filelist_dir + "wjets/", rawdir)
backgrounds.append(wjets)

#diboson
diboson = background.Background("vv", "VV (Sherpa)")
diboson.set_debug()
diboson.scale_factor = 1.0
diboson.set_color(r.TColor.GetColor("#315E88"))
diboson.set_treename("VV_sherpa")
diboson.set_chain_from_list_CONDOR(filelist_dir + "sherpaVV/", rawdir)
backgrounds.append(diboson)

## ww
#ww = background.Background("ww", "WW (Powheg)")
#ww.set_debug()
#ww.scale_factor = 1.0
#ww.set_color(r.TColor.GetColor("#315E88"))
#ww.set_treename("WW_powheg")
#ww.set_chain_from_list(filelist_dir + "ww_powheg_n0213.txt", rawdir)
#backgrounds.append(ww)
#
## wz
#wz = background.Background("wz", "WZ (Powheg)")
#wz.set_debug()
#wz.scale_factor = 1.0
#wz.set_color(r.TColor.GetColor("#F9F549"))
#wz.set_treename("WZ_powheg")
#wz.set_chain_from_list(filelist_dir + "wz_powheg_n0213.txt", rawdir)
#backgrounds.append(wz)
#
## zz
#zz = background.Background("zz", "ZZ (Powheg)")
#zz.set_debug()
#zz.scale_factor = 1.0
#zz.set_color(r.TColor.GetColor("#FFEF53"))
#zz.set_treename("ZZ_powheg")
#zz.set_chain_from_list(filelist_dir + "zz_powheg_n0213.txt", rawdir)
#backgrounds.append(zz)

#### DATA
data = background.Data()
data.set_color(r.kBlack)
data.set_treename("Data")
data.set_chain_from_list_CONDOR(filelist_dir + "data/", data_rawdir)


#############################################
# Set up the regions
#############################################
regions = []
reg = region.Region()
reg.simplename = "zpeak_ee_inc"
reg.displayname = "Z #rightarrow ee (nJ>=0 nB=0)"
reg.tcut = "nLeptons==2 && nElectrons==2 && nSJets>=0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<1 && abs(mll-91.2)<20"
regions.append(reg)


reg = region.Region()
reg.simplename = "zpeak_ee_0j"
reg.displayname = "Z #rightarrow ee (nJ==0 nB=0)"
reg.tcut = "nLeptons==2 && nElectrons==2 && nSJets==0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<1 && abs(mll-91.2)<20"
regions.append(reg)

reg = region.Region()
reg.simplename = "val_gt2l"
reg.displayname = "pre-sel + >=2#it{l}"
reg.tcut = "nLeptons>=2"
regions.append(reg)

#############################################
# Set up the plots
#############################################

plots = []

#### val_gt2l
logy = 10000000

p = plot.Plot1D()
p.initialize("val_gt2l", "met", "val_gt2l_met")
p.labels(x="TST #slash{E}_{T} [GeV]", y="Entries / 10 GeV")
p.xax(10,0,200)
p.yax(0.1,10000000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

## nVtx
p = plot.Plot1D()
p.initialize("val_gt2l", "nVtx", "val_gt2l_nVtx")
p.labels(x="nVtx", y = "Entries / 1")
p.xax(1, 0, 45)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

## mu
p = plot.Plot1D()
p.initialize("val_gt2l", "avgMu", "val_gt2l_avgMu")
p.labels(x="<#mu>", y = "Entries / 2")
p.xax(2, 0, 50)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

## leptons
p = plot.Plot1D()
p.initialize("val_gt2l", "l_pt[0]", "val_gt2l_lpt0")
p.labels(x="lead lepton pt [GeV]", y = "Entries / 10 GeV")
p.xax(10, 0, 350)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("val_gt2l", "l_pt[1]", "val_gt2l_lpt1")
p.labels(x="sub-lead lepton pt [GeV]", y = "Entries / 10 GeV")
p.xax(10, 0, 250)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("val_gt2l", "l_eta[0]", "val_gt2l_leta0")
p.labels(x="lead lepton eta", y = "Entries / 0.1")
p.xax(0.1, -5, 5)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("val_gt2l", "l_eta[1]", "val_gt2l_leta1")
p.labels(x="sub-lead lepton eta", y = "Entries / 0.1")
p.xax(0.1, -5, 5)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("val_gt2l", "l_phi[0]", "val_gt2l_lphi0")
p.labels(x="lead lepton phi", y = "Entries / 0.1 rad")
p.xax(0.1, -3.2, 3.2)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("val_gt2l", "l_phi[1]", "val_gt2l_lphi1")
p.labels(x="sub-lead lepton phi", y = "Entries / 0.1 rad")
p.xax(0.1, -3.2, 3.2)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("val_gt2l", "pTll", "val_gt2l_pTll")
p.labels(x="dilepton pT [GeV]", y = "Entries / 10 GeV")
p.xax(10, 0, 500)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("val_gt2l", "dphi_ll", "val_gt2l_dphi_ll")
p.labels(x="dphi_ll", y = "Entries / 0.1 rad")
p.xax(0.1, -3.2, 3.2)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("val_gt2l", "mll", "val_gt2l_mll")
p.labels(x="dilepton invariant mass [GeV]", y = "Entries / 2 GeV")
p.xax(2, 80, 110)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

## jets
p = plot.Plot1D()
p.initialize("val_gt2l", "nSJets", "val_gt2l_nSJets")
p.labels(x="number of jets (non-b-tag)", y = "Entries / 1")
p.xax(1, 0, 10)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("val_gt2l", "sj_pt[0]", "val_gt2l_sjpt0")
p.labels(x="lead jet (non b) pt [GeV]", y = "Entires / 20 GeV")
p.xax(20, 0, 500)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)








