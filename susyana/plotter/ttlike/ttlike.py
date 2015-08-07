import os
import sys
sys.path.append(os.environ['SUSYDIR'])
#sys.path.append('../../../../../')
import supersusy.utils.plot as plot
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region


#############################################
# Set up the samples
#############################################
scratchdir = "/scratch/dantrim/n0211/"
#datafile = scratchdir + "data15_13TeV.root"
datafile = scratchdir + "data15_13TeV.root"
wjetsfile = scratchdir + "mc15_13TeV_wjets_sherpa.root"
mcfile = scratchdir + "mc15_13TeV.root"
backgrounds = []

#### MC
# Zjets
zjets = background.Background("zjets", "Z+jets")
zjets.set_debug()
zjets.set_file(mcfile)
zjets.scale_factor = 1.0
zjets.set_color(r.TColor.GetColor("#82DE68"))
zjets.set_treename("Zjets_CENTRAL")
zjets.set_merged_tree(zjets.treename)
backgrounds.append(zjets)

ttbar = background.Background("ttbar", "TTbar")
ttbar.set_debug()
ttbar.set_file(mcfile)
ttbar.scale_factor = 1.0
ttbar.set_color(r.TColor.GetColor("#E67067"))
ttbar.set_treename("TTbar_CENTRAL")
ttbar.set_merged_tree(ttbar.treename)
backgrounds.append(ttbar)

# singletop
stop = background.Background("st", "ST")
stop.set_debug()
stop.set_file(mcfile)
stop.scale_factor = 1.0
stop.set_color(r.TColor.GetColor("#DE080C"))
stop.set_treename("ST_CENTRAL")
stop.set_merged_tree(stop.treename)
backgrounds.append(stop)

# wjets
wjets = background.Background("wjets", "W+jets")
wjets.set_debug()
wjets.set_file(wjetsfile)
wjets.scale_factor = 1.0
wjets.set_color(r.TColor.GetColor("#5E9AD6"))
wjets.set_treename("Wjets_CENTRAL")
wjets.set_merged_tree(wjets.treename)
backgrounds.append(wjets)

# ww
ww = background.Background("ww", "WW")
ww.set_debug()
ww.set_file(mcfile)
ww.scale_factor = 1.0
ww.set_color(r.TColor.GetColor("#315E88"))
ww.set_treename("WW_CENTRAL")
ww.set_merged_tree(ww.treename)
backgrounds.append(ww)

# wz
wz = background.Background("wz", "WZ")
wz.set_debug()
wz.set_file(mcfile)
wz.scale_factor = 1.0
wz.set_color(r.TColor.GetColor("#F9F549"))
wz.set_treename("WZ_CENTRAL")
wz.set_merged_tree(wz.treename)
backgrounds.append(wz)

# zz
zz = background.Background("zz", "ZZ")
zz.set_debug()
zz.set_file(mcfile)
zz.scale_factor = 1.0
zz.set_color(r.TColor.GetColor("#FFEF53"))
zz.set_treename("ZZ_CENTRAL")
zz.set_merged_tree(zz.treename)
backgrounds.append(zz)

#### DATA
data = background.Data()
data.set_file(datafile)
data.set_color(r.kBlack)
data.set_treename("Data_CENTRAL")
data.set_merged_tree(data.treename)



#############################################
# Set up the regions
#############################################
regions = []
reg = region.Region()
reg.simplename = "zpeak_mm0j"
reg.displayname = "Z#mu#mu 0-j"
reg.tcut = "nLeptons==2 && nMuons==2 && nSJets==0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<1 && abs(mll-91.2)<20 && abs(l_d0sigBSCorr[0])<3 && abs(l_d0sigBSCorr[1])<3"
regions.append(reg)

reg = region.Region()
reg.simplename = "zpeak_mmj"
reg.displayname = "Z#mu#mu >=0j"
reg.tcut = "nLeptons==2 && nMuons==2 && nSJets>=0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<0 && abs(mll-91.2)<20 && abs(l_d0sigBSCorr[0])<3 && abs(l_d0sigBSCorr[1])<3"
regions.append(reg)

reg = region.Region()
reg.simplename = "ttlike"
reg.displayname = "t#bar{t}-like"
reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && nBJets>=1 && l_pt[0]>20 && l_pt[1]>20 && abs(l_d0sigBSCorr[0])<3 && abs(l_d0sigBSCorr[1])<3"
regions.append(reg)



#############################################
# Set up the plots
#############################################

plots = []

#### ttlike

p = plot.Plot1D()
p.initialize("ttlike", "mll", "ttlike_mll")
p.labels(x="m_{#mu#mu} [GeV]", y="Entries / 20 GeV")
p.xax(20,70,600)
p.yax(0.1,1000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "pTll", "ttlike_pTll")
p.labels(x="Dilepton p_{T} [GeV]", y="Entries / 15 GeV")
p.xax(15,0,300)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "dphi_ll", "ttlike_dphill")
p.labels(x="#Delta#phi_{ll}", y = "Entries / 0.2")
p.xax(0.2, -3.5,3.5)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "l_pt[0]", "ttlike_lpt0")
p.labels(x="Lead lepton p_{T} [GeV]", y="Entries / 4 GeV")
p.xax(4, 25, 200)
p.yax(0.1,1000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "l_pt[1]", "ttlike_lpt1")
p.labels(x="Sub-lead lepton p_{T} [GeV]", y="Entries / 5 GeV")
p.xax(5, 25, 160)
p.yax(0.1,1000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "l_eta[0]", "ttlike_leta0")
p.labels(x="Lead lepton #eta", y="Entries / 0.2")
p.xax(0.2,-3, 3)
p.yax(0.1,1000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "l_eta[1]", "ttlike_leta1")
p.labels(x="Sub-lead lepton #eta", y="Entries / 0.2")
p.xax(0.2, -3, 3)
p.yax(0.1,1000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "mt2", "ttlike_mt2")
p.labels(x="m_{T2} [GeV]", y = "Entries / 5 GeV ")
p.xax(5,0,140)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "MDR", "ttlike_MDR")
p.labels(x="M_{#Delta}^{R} [GeV]", y = "Entries / 5 GeV")
p.xax(5,0,140)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "nSJets", "ttlike_nSJets")
p.labels(x="Number of jets", y = "Entries / 1")
p.xax(1,0,10)
p.yax(0.1,1000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "nBJets", "ttlike_nBJets")
p.labels(x="Number of bjets", y = "Entries / 1")
p.xax(1,0,10)
p.yax(0.1,1000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "sj_pt[0]", "ttlike_sjpt0")
p.labels(x="Lead jet p_{T} [GeV]", y = "Entries / 15 GeV")
p.xax(15,0,300)
p.doLogY=True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "bj_pt[0]", "ttlike_bjpt0")
p.labels(x="Lead b-jet p_{T} [GeV]", y = "Entries / 15 GeV")
p.xax(15,0,300)
p.doLogY=True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "sj_eta[0]", "ttlike_sjeta0")
p.labels(x="Lead jet #eta", y = "Entries / 0.2")
p.xax(0.2,-3,3)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "bj_eta[0]", "ttlike_bjeta0")
p.labels(x="Lead b-jet #eta", y = "Entries / 0.2")
p.xax(0.2,-3,3)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "sj_jvt[0]", "ttlike_sjvt0")
p.labels(x="Lead jet JVT", y = "Entries / 0.05")
p.xax(0.05, -0.5, 1.2)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "bj_jvt[0]", "ttlike_bjvt0")
p.labels(x="Lead b-jet JVT", y = "Entries / 0.05")
p.xax(0.05, -0.5, 1.2)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "sj_pt[1]", "ttlike_sjpt1")
p.labels(x="Sub-lead jet p_{T} [GeV]", y = "Entries / 15 GeV")
p.xax(15,0,300)
p.doLogY=True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "bj_pt[1]", "ttlike_bjpt1")
p.labels(x="Sub-lead b-jet p_{T} [GeV]", y = "Entries / 15 GeV")
p.xax(15,0,300)
p.doLogY=True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "sj_eta[1]", "ttlike_sjeta1")
p.labels(x="Sub-lead jet #eta", y = "Entries / 0.2")
p.xax(0.2,-3,3)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "bj_eta[1]", "ttlike_bjeta1")
p.labels(x="Sub-lead b-jet #eta", y = "Entries / 0.2")
p.xax(0.2,-3,3)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "sj_jvt[1]", "ttlike_sjvt1")
p.labels(x="Sub-lead jet JVT", y = "Entries / 0.05")
p.xax(0.05, -0.5, 1.2)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "bj_jvt[1]", "ttlike_bjvt1")
p.labels(x="Sub-lead b-jet JVT", y = "Entries / 0.05")
p.xax(0.05, -0.5, 1.2)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "met", "ttlike_met")
p.labels(x="TST #slash{E}_{T} [GeV]", y="Entries / 10 GeV")
p.xax(10,0,400)
p.yax(0.1,1000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "sumet", "ttlike_sumet")
p.labels(x="#sum E_{T} [GeV]", y = "Entires / 60 GeV")
p.xax(60,40,1200)
p.yax(0.1,1000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "refJet_et", "ttlike_refJet_et")
p.labels(x="TST #slash{E}_{T} jet term [GeV]", y="Entries / 10 GeV")
p.xax(10,0,300)
p.yax(0.1,1000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "refMuo_et", "ttlike_refMuo_et")
p.labels(x="TST #slash{E}_{T} muon term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,180)
p.yax(0.1,1000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "refEle_et", "ttlike_refEle_et")
p.labels(x="TST #slash{E}_{T} electron term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,180)
p.yax(0.1,1000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "softTerm_et", "ttlike_softTerm_et")
p.labels(x="TST #slash{E}_{T} soft term [GeV]", y="Entries / 3 GeV")
p.xax(3,0,60)
p.yax(0.1,1000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "refMuo_sumet", "ttlike_refMuo_sumet")
p.labels(x="#sum E_{T} muon-term [GeV]", y="Entries / 10 GeV")
p.xax(10, 0, 250)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "refEle_sumet", "ttlike_refEle_sumet")
p.labels(x="#sum E_{T} electron-term [GeV]", y="Entries / 10 GeV")
p.xax(10, 0, 250)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "refJet_sumet", "ttlike_refJet_sumet")
p.labels(x="#sum E_{T} jet term [GeV]", y="Entries / 25 GeV")
p.xax(25,0,650)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "softTerm_sumet", "ttlike_softTerm_sumet")
p.labels(x="#sum E_{T} soft-term [GeV]", y="Entries / 5 GeV")
p.xax(5,0, 150)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "l_d0sig[0]", "ttlike_d0sig0")
p.labels(x="Lead lepton d0sig", y="Entries")
p.xax(0.5,-10,10)
p.yax(0.1,1000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "l_d0sigBSCorr[0]", "ttlike_d0sigBSCorr0")
p.labels(x="Lead lepton d0sig (BSCorr)", y="Entries")
p.xax(0.5,-10,10)
p.yax(0.1,1000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "l_d0[0]", "ttlike_d00")
p.labels(x="Lead lepton d0 [mm]", y="Entries")
p.xax(0.01,-0.2,0.2)
p.yax(0.1,1000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "meff", "ttlike_meff")
p.labels(x="m_{eff} [GeV]", y = "Entries / 60 GeV")
p.xax(60, 40, 1500)
p.yax(0.1,1000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "l_ptvarcone20[0]", "ttlike_ptvarcone200")
p.labels(x="Lead lepton ptvarcone20 [GeV]", y = "Entries / 0.2 GeV")
p.xax(0.2, 0, 6)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "l_ptvarcone20[1]", "ttlike_ptvarcone201")
p.labels(x="Sub-lead lepton ptvarcone20 [GeV]", y = "Entries / 0.2 GeV")
p.xax(0.2, 0, 6)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "l_etconetopo20[0]", "ttlike_etconetopo200")
p.labels(x="Lead lepton etconetopo20 [GeV]", y = "Entries / 0.2 GeV")
p.xax(0.2, 0, 6)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "l_etconetopo20[1]", "ttlike_etconetopo201")
p.labels(x="Sub-lead lepton etconetopo20 [GeV]", y = "Entries / 0.2 GeV")
p.xax(0.2, 0, 6)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "l_etconetopo30[0]", "ttlike_etconetopo300")
p.labels(x="Lead lepton etconetopo30 [GeV]", y = "Entries / 0.2 GeV")
p.xax(0.2, 0, 6)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("ttlike", "l_etconetopo30[1]", "ttlike_etconetopo301")
p.labels(x="Sub-lead lepton etconetopo30 [GeV]", y = "Entries / 0.2 GeV")
p.xax(0.2, 0, 6)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)
