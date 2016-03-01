
import sys
sys.path.append('../../../../../')
import supersusy.utils.plot as plot
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region


#############################################
# Set up the samples
#############################################
rawdir = "/gdata/atlas/dantrim/SusyAna/ntuples/n0220/rj/mc/Raw/"
data_rawdir = "/gdata/atlas/dantrim/SusyAna/ntuples/n0220/rj/data/Raw/"
filelist_dir = "/data7/atlas/dantrim/SusyAna/n0220val/SuperRest/run/filelists/"
backgrounds = []

#### MC
# Zjets
zjets = background.Background("zjets", "Z+jets (Sherpa)")
zjets.set_debug()
zjets.scale_factor = 1
zjets.set_color(r.TColor.GetColor("#82DE68"))
zjets.set_treename("Zjets_sherpa")
zjets.set_chain_from_list(filelist_dir + "zjets_sherpa.txt", rawdir)
backgrounds.append(zjets)

ttbar = background.Background("ttbar", "TTbar")
ttbar.set_debug()
ttbar.scale_factor = 1.0
ttbar.set_color(r.TColor.GetColor("#E67067"))
ttbar.set_treename("ttbar_powheg")
ttbar.set_chain_from_list(filelist_dir + "ttbar.txt", rawdir)
backgrounds.append(ttbar)

# singletop
stop = background.Background("st", "ST")
stop.set_debug()
stop.scale_factor = 1.0
stop.set_color(r.TColor.GetColor("#DE080C"))
stop.set_treename("ST")
stop.set_chain_from_list(filelist_dir + "singletop.txt", rawdir)
backgrounds.append(stop)

# wjets
wjets = background.Background("wjets", "W+jets (PowHeg)")
wjets.set_debug()
wjets.scale_factor = 1.0
wjets.set_color(r.TColor.GetColor("#5E9AD6"))
wjets.set_treename("Wjets_powheg")
wjets.set_chain_from_list(filelist_dir + "wjets_powheg.txt", rawdir)
backgrounds.append(wjets)

#diboson
diboson = background.Background("vv", "VV (Sherpa)")
diboson.set_debug()
diboson.scale_factor = 1.0
diboson.set_color(r.TColor.GetColor("#315E88"))
diboson.set_treename("VV_sherpa")
diboson.set_chain_from_list(filelist_dir + "diboson_sherpa.txt", rawdir)
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
data.set_chain_from_list(filelist_dir + "n0220_data.txt", data_rawdir)


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
reg.simplename = "zpeak_mm_0j"
reg.displayname = "Z #rightarrow #mu#mu (nJ==0 nB=0)"
reg.tcut = "nLeptons==2 && nMuons==2 && nSJets==0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<1 && abs(mll-91.2)<20"
regions.append(reg)

reg = region.Region()
reg.simplename = "val_gt2l"
reg.displayname = "pre-sel + >=2#it{l}"
reg.tcut = "nLeptons>=2"
regions.append(reg)

reg = region.Region()
reg.simplename = "wwpre"
reg.displayname = "WW-Pre (DFOS)"
reg.tcut = "nLeptons==2 && nMuons==1 && nElectrons==1 && nBJets==0 && nJets>=2 && l_pt[0]>20 && l_pt[1]>20 && (l_q[0]*l_q[1]})<1"

reg = region.Region()
reg.simplename = "ttbarValZ"
reg.displayname = "t#bar{t} val"
reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<1 && nBJets>0 && l_pt[0]>20 && l_pt[1]>20"
regions.append(reg)


reg = region.Region()
reg.simplename = "vvVal"
reg.displayname = "VV val"
reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<1 && nBJets==0 && nSJets==0 && l_pt[0]>15 && l_pt[1]>10 && mt2>30"
regions.append(reg)


#############################################
# Set up the plots
#############################################

plots = []

#### check_2OS20
logy = 100000000
logy = 1100
p = plot.Plot1D()
p.initialize("vvVal", "mt2", "vvVal_mt2")
p.labels(x="m_{t2} [GeV]", y = "Entries / 5 GeV")
p.xax(5, 0, 110)
p.yax(0., 1200)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("vvVal", "mll", "vvVal_mll")
p.labels(x="dilepton invariant mass [GeV]", y = "Entries / 2 GeV")
if "ttbar" in p.name or "vv" in p.name:
    p.xax(20, 40, 400)
else :
    p.xax(2, 80, 110)
p.yax(0., 800)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("vvVal", "met", "vvVal_met")
p.labels(x="TST #slash{E}_{T} [GeV]", y="Entries / 10 GeV")
p.xax(10,0,200)
p.yax(0., 800 )
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)

## nVtx
p = plot.Plot1D()
p.initialize("vvVal", "nVtx", "vvVal_nVtx")
p.labels(x="nVtx", y = "Entries / 1")
p.xax(1, 0, 22)
p.yax(0., 500)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)

## mu
p = plot.Plot1D()
p.initialize("vvVal", "avgMu", "vvVal_avgMu")
p.labels(x="<#mu>", y = "Entries / 2")
p.xax(2, 0, 50)
p.yax(0., logy)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)

## leptons
p = plot.Plot1D()
p.initialize("vvVal", "l_pt[0]", "vvVal_lpt0")
p.labels(x="lead lepton pt [GeV]", y = "Entries / 10 GeV")
p.xax(5, 0, 150)
p.yax(0., 725)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("vvVal", "l_pt[1]", "vvVal_lpt1")
p.labels(x="sub-lead lepton pt [GeV]", y = "Entries / 10 GeV")
p.xax(5, 0, 100)
p.yax(0., 1200)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("vvVal", "l_eta[0]", "vvVal_leta0")
p.labels(x="lead lepton eta", y = "Entries / 0.4")
p.xax(0.4, -5, 5)
p.yax(0., 300)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("vvVal", "l_eta[1]", "vvVal_leta1")
p.labels(x="sub-lead lepton eta", y = "Entries / 0.4")
p.xax(0.4, -5, 5)
p.yax(0., 300)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("vvVal", "l_phi[0]", "vvVal_lphi0")
p.labels(x="lead lepton phi", y = "Entries / 0.4 rad")
p.xax(0.4, -3.2, 3.2)
p.yax(0., 300)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("vvVal", "l_phi[1]", "vvVal_lphi1")
p.labels(x="sub-lead lepton phi", y = "Entries / 0.4 rad")
p.xax(0.4, -3.2, 3.2)
p.yax(0., 300)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("vvVal", "pTll", "vvVal_pTll")
p.labels(x="dilepton pT [GeV]", y = "Entries / 8 GeV")
p.xax(8, 0, 175)
p.yax(0., 800)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("vvVal", "dphi_ll", "vvVal_dphi_ll")
p.labels(x="dphi_ll", y = "Entries / 0.4 rad")
p.xax(0.4, -3.2, 3.2)
p.yax(0., 300)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)


## jets
p = plot.Plot1D()
p.initialize("vvVal", "nSJets", "vvVal_nSJets")
p.labels(x="number of jets (non-b-tag)", y = "Entries / 1")
p.xax(1, 0, 10)
p.yax(0., logy)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("vvVal", "nBJets", "vvVal_nBJets")
p.labels(x="number of b-tagged jets", y = "Entries / 1")
p.xax(1, 0, 10)
p.yax(0.1,logy)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("vvVal", "sj_pt[0]", "vvVal_sjpt0")
p.labels(x="lead jet (non b) pt [GeV]", y = "Entires / 20 GeV")
p.xax(20, 0, 500)
p.yax(0., logy)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("vvVal", "sj_pt[1]", "vvVal_sjpt1")
p.labels(x="sub-lead jet (non b) pt [GeV]", y = "Entires / 20 GeV")
p.xax(20, 0, 500)
p.yax(0., logy)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("vvVal", "bj_pt[0]", "vvVal_bjpt0")
p.labels(x="lead b-jet pt [GeV]", y = "Entries / 20 GeV")
p.xax(20, 0, 500)
p.yax(0., logy)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("vvVal", "bj_pt[1]", "vvVal_bjpt1")
p.labels(x="sub-lead b-jet pt [GeV]", y = "Entries / 20 GeV")
p.xax(20, 0, 500)
p.yax(0., logy)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)







