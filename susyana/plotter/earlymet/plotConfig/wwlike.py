import sys
sys.path.append('../../../..')
import supersusy.utils.plot as plot
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region


#############################################
# Set up the samples
#############################################
scratchdir = "/scratch/dantrim/n0209/wwlike/"
#datafile = scratchdir + "data15_13TeV.root"
datafile = scratchdir + "data15_perC_13TeV.root"
mcfile = scratchdir + "mc15_13TeV.root"
backgrounds = []

#### MC
# zmumu
zmm = background.Background("zmm", "Z#mu#mu")
zmm.set_debug()
zmm.set_file(mcfile)
zmm.scale_factor = 7.5
#zmm.set_scale_factor = 0.9
zmm.set_color(r.TColor.GetColor("#82DE68"))
zmm.set_treename("Zmm_CENTRAL")
zmm.set_merged_tree(zmm.treename)
backgrounds.append(zmm)

# zee
zee = background.Background("zee", "Zee")
zee.set_debug()
zee.set_file(mcfile)
zee.scale_factor = 7.5
zee.set_color(r.TColor.GetColor("#A7E851"))
zee.set_treename("Zee_CENTRAL")
zee.set_merged_tree(zee.treename)
backgrounds.append(zee)

# ztt
ztt = background.Background("ztt", "Z#tau#tau")
ztt.set_debug()
ztt.set_file(mcfile)
ztt.scale_factor = 7.5
ztt.set_color(r.TColor.GetColor("#91D2FC"))
ztt.set_treename("Ztt_CENTRAL")
ztt.set_merged_tree(ztt.treename)
backgrounds.append(ztt)

# ttbar
ttbar = background.Background("ttbar", "TTbar")
ttbar.set_debug()
ttbar.set_file(mcfile)
ttbar.scale_factor = 7.5
#ttbar.scale_factor = 0.9
ttbar.set_color(r.TColor.GetColor("#E67067"))
ttbar.set_treename("TTbar_CENTRAL")
ttbar.set_merged_tree(ttbar.treename)
backgrounds.append(ttbar)

# singletop
stop = background.Background("st", "ST")
stop.set_debug()
stop.set_file(mcfile)
stop.scale_factor = 7.5
stop.set_color(r.TColor.GetColor("#DE080C"))
stop.set_treename("ST_CENTRAL")
stop.set_merged_tree(stop.treename)
backgrounds.append(stop)

# wjets
wjets = background.Background("wjets", "W+jets")
wjets.set_debug()
wjets.set_file(mcfile)
wjets.scale_factor = 7.5
#wjets.scale_factor = 0.9
wjets.set_color(r.TColor.GetColor("#5E9AD6"))
wjets.set_treename("Wjets_CENTRAL")
wjets.set_merged_tree(wjets.treename)
backgrounds.append(wjets)

# ww
ww = background.Background("ww", "WW")
ww.set_debug()
ww.set_file(mcfile)
ww.scale_factor = 7.5
ww.set_color(r.TColor.GetColor("#315E88"))
ww.set_treename("WW_CENTRAL")
ww.set_merged_tree(ww.treename)
backgrounds.append(ww)

# wz
wz = background.Background("wz", "WZ")
wz.set_debug()
wz.set_file(mcfile)
wz.scale_factor = 7.5
wz.set_color(r.TColor.GetColor("#F9F549"))
wz.set_treename("WZ_CENTRAL")
wz.set_merged_tree(wz.treename)
backgrounds.append(wz)

# zz
zz = background.Background("zz", "ZZ")
zz.set_debug()
zz.set_file(mcfile)
zz.scale_factor = 7.5
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
reg.tcut = "nLeptons==2 && nMuons==2 && nSJets==0 && nBJets==0 && l_pt[5]>20 && l_pt[1]>20 && (l_q[0]*l_q[1])<1 && abs(mll-91.2)<20 && abs(l_d0sigBSCorr[0])<3 && abs(l_d0sigBSCorr[1])<3"
regions.append(reg)

reg = region.Region()
reg.simplename = "zpeak_mmj"
reg.displayname = "Z#mu#mu >=0j"
reg.tcut = "nLeptons==2 && nMuons==2 && nSJets>=0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<0 && abs(mll-91.2)<20 && abs(l_d0sigBSCorr[0])<3 && abs(l_d0sigBSCorr[1])<3"
regions.append(reg)

## 8TeV wwlike CRT
reg = region.Region()
reg.simplename = "wwCRT"
reg.displayname = "CRT"
reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && R1<0.3 && mt2>35 && deltaX<0.02 && R2>0.5"
regions.append(reg)

## 8TeV wwlike CRW
reg = region.Region()
reg.simplename = "wwCRW"
reg.displayname = "CRW"
reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && nBJets==0 && (R1>1.5*(meff/1000)) && mt2>35"
regions.append(reg)

## 8 TeV wwlike CRZ
reg = region.Region()
reg.simplename = "wwCRZ"
reg.displayname = "CRZ"
reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (R1>(meff/1000)) && mt2<20 && deltaX<0.02 && (mll>30 && mll<80) && l_pt[0]>30"
regions.append(reg)

reg = region.Region()
reg.simplename = "wwLoose"
reg.displayname = "ww-loose"
reg.tcut  = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && abs(l_d0sigBSCorr[0])<3 && abs(l_d0sigBSCorr[1])<3 && l_pt[0]>20 && l_pt[1]>20"
regions.append(reg)



#############################################
# Set up the plots
#############################################

plots = []

#### zpeak_mm0j

p = plot.Plot1D()
p.initialize("zpeak_mm0j", "mll", "zpeak_mm0j_mll")
p.labels(x="m_{#mu#mu} [GeV]", y="Entries / 2 GeV")
p.xax(2,70,110)
p.yax(0,1000)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm0j", "l_pt[0]", "zpeak_mm0j_lpt0")
p.labels(x="Lead lepton p_{T} [GeV]", y="Entries / 2 GeV")
p.xax(2, 25, 90)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm0j", "l_pt[1]", "zpeak_mm0j_lpt1")
p.labels(x="Sub-lead lepton p_{T} [GeV]", y="Entries / 5 GeV")
p.xax(5, 25, 120)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm0j", "l_eta[0]", "zpeak_mm0j_leta0")
p.labels(x="Lead lepton #eta", y="Entries")
p.xax(0.5, 5, 5)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm0j", "l_eta[1]", "zpeak_mm0j_leta1")
p.labels(x="Sub-lead lepton #eta", y="Entries")
p.xax(0.5, 5, 5)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)


p = plot.Plot1D()
p.initialize("zpeak_mm0j", "nJets", "zpeak_mm0j_nJets")
p.labels(x="Number of Jets", y="Entries")
p.xax(1,0,8)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm0j", "met", "zpeak_mm0j_met")
p.labels(x="TST #slash{E}_{T} [GeV]", y="Entries / 5 GeV")
p.xax(5,0,180)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm0j", "refJet_et", "zpeak_mm0j_refJet_et")
p.labels(x="TST #slash{E}_{T} jet term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,180)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm0j", "refMuo_et", "zpeak_mm0j_refMuo_et")
p.labels(x="TST #slash{E}_{T} muon term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,180)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm0j", "softTerm_et", "zpeak_mm0j_softTerm_et")
p.labels(x="TST #slash{E}_{T} muon term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,180)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm0j", "l_d0sig[0]", "zpeak_mm0j_d0sig0")
p.labels(x="Lead lepton d0sig", y="Entries")
p.xax(0.5,-10,10)
p.yax(0.1,1000000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm0j", "l_d0sigBSCorr[0]", "zpeak_mm0j_d0sigBSCorr0")
p.labels(x="Lead lepton d0sig (BSCorr)", y="Entries")
p.xax(0.5,-10,10)
p.yax(0.1,1000000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm0j", "l_d0[0]", "zpeak_mm0j_d00")
p.labels(x="Lead lepton d0 [mm]", y="Entries")
p.xax(0.01,-0.2,0.2)
p.yax(0.1,1000000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

#### zpeak_mmj

p = plot.Plot1D()
p.initialize("zpeak_mmj", "met", "zpeak_mmj_met")
p.labels(x="TST #slash{E}_{T} [GeV]", y="Entries / 5 GeV")
p.xax(5,0,200)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "refJet_et", "zpeak_mmj_refJet_et")
p.labels(x="TST #slash{E}_{T} jet term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,200)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "refMuo_et", "zpeak_mmj_refMuo_et")
p.labels(x="TST #slash{E}_{T} muon term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,200)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "softTerm_et", "zpeak_mmj_softTerm_et")
p.labels(x="TST #slash{E}_{T} soft term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,60)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "metX", "zpeak_mmj_metX")
p.labels(x="TST #slash{E}_{T}-x [GeV]", y="Entries / 5 GeV")
p.xax(5,-150,150)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "metY", "zpeak_mmj_metY")
p.labels(x="TST #slash{E}_{T}-y [GeV]", y="Entries / 5 GeV")
p.xax(5,-150,150)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)


p = plot.Plot1D()
p.initialize("zpeak_mmj", "j_jvf[0]", "zpeak_mmj_jvf0")
p.labels(x="Lead jet JVF", y="Entries")
p.xax(0.05,-0.2,1)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

#################################################
## wwlike 8 TeV CR plots
## wwlike 8 TeV CR plots
## wwlike 8 TeV CR plots
## wwlike 8 TeV CR plots
#################################################

##
### CRT
##

p = plot.Plot1D()
p.initialize("wwCRT", "meff", "wwCRT_meff")
p.labels(x="M_{eff} [GeV]", y="Entries / 60 GeV")
p.xax(60, 100, 1100)
p.doLogY = True
p.yax(0.1,100)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwCRT", "met", "wwCRT_met")
p.labels(x="TST #slash{E}_{T} [GeV]", y="Entries / 12 GeV")
p.xax(12, 35, 275)
p.doLogY = True
p.yax(0.1, 100)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwCRT", "mt2", "wwCRT_mt2")
p.labels(x="m_{T2} [GeV]", y="Entries / 4 GeV")
p.xax(4, 35, 100)
p.doLogY = True
p.yax(0.1,100)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwCRT", "deltaX", "wwCRT_deltaX")
p.labels(x="|x_{1}-x_{2}|", y = "Entries / 0.0025")
p.xax(0.0025, 0, 0.025)
p.doLogY = True
p.yax(0.1,100)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwCRT", "R1", "wwCRT_R1")
p.labels(x="R_{1}", y="Entries / 0.02")
p.xax(0.02, 0.05, 0.31)
p.doLogY = True
p.yax(0.1, 100)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwCRT", "R2", "wwCRT_R2")
p.labels(x="R_{2}", y="Entries / 0.03")
p.xax(0.03, 0.5, 0.9)
p.doLogY = True
p.yax(0.1, 100)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwCRT", "abs(cosThetaB)", "wwCRT_cosThetaB")
p.labels(x="|cos#theta_{b}|", y = "Entries / 0.08")
p.xax(0.08, 0, 1.0)
p.doLogY = True
p.yax(0.1, 100)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwCRT", "l_pt[0]", "wwCRT_lpt0")
p.labels(x="Lead lepton p_{T} [GeV]", y = "Entries / 8 GeV")
p.xax(8, 20, 180)
p.doLogY = True
p.yax(0.1, 100)
p.setRatioCanvas(p.name)
plots.append(p)


##
### CRW
##

p = plot.Plot1D()
p.initialize("wwCRW", "l_pt[0]", "wwCRW_lpt0")
p.labels(x="Lead lepton p_{T} [GeV]", y = "Entries / 8 GeV")
p.xax(8,25,120)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwCRW", "l_pt[1]", "wwCRW_lpt1")
p.labels(x="Sub-lead lepton p_{T} [GeV]", y = "Entries / 4 GeV")
p.xax(4, 10, 70)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwCRW", "met", "wwCRW_met")
p.labels(x="TST #slash{E}_{T} [GeV]", y="Entries / 8 GeV")
p.xax(8, 30, 150)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwCRW", "mt2", "wwCRW_mt2")
p.labels(x="m_{T2} [GeV]", y="Entries / 5 GeV")
p.xax(5, 35, 100)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwCRW", "deltaX", "wwCRW_deltaX")
p.labels(x="|x_{1}-x_{2}|", y = "Entries / 0.0025")
p.xax(0.0025, 0.00, 0.04)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwCRW", "R2", "wwCRW_R2")
p.labels(x="R_{2}", y = "Entries / 0.03")
p.xax(0.03, 0.35, 0.75)
p.doLogY = True
p.yax(0.1, 1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwCRW", "abs(cosThetaB)", "wwCRW_cosThetaB")
p.labels(x="|cos#theta_{b}|", y = "Entries / 0.1")
p.xax(0.1,0,1)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwCRW", "meff", "wwCRW_meff")
p.labels(x="m_{eff} [GeV]", y = "Entries / 12 GeV")
p.xax(12, 60, 300)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

##
### wwLoose
##

p = plot.Plot2D()
p.is2D = True
p.initialize("wwLoose", "meff", "R1", "wwCRW_R1_meff_ttbar_2d")
p.labels(x="m_{eff} [GeV]",y="R_{1}")
p.set_sample("ttbar")
p.yax(0.05,0,1)
p.xax(25,0,500)
p.defaultCanvas()
plots.append(p)

p = plot.Plot2D()
p.is2D = True
p.initialize("wwLoose", "meff", "R1", "wwCRW_R1_meff_ww_2d")
p.labels(x="m_{eff} [GeV]", y = "R_{1}")
p.set_sample("ww")
p.yax(0.05,0,1)
p.xax(25,0,500)
p.defaultCanvas()
plots.append(p)

p = plot.Plot2D()
p.is2D = True
p.initialize("wwLoose", "meff", "R1", "wwCRW_R1_meff_wjets_2d")
p.labels(x="m_{eff} [GeV]",y="R_{1}")
p.set_sample("wjets")
p.yax(0.05,0,1)
p.xax(25,0,500)
p.defaultCanvas()
plots.append(p)

p = plot.Plot1D()
p.initialize("wwLoose", "meff", "wwLoose_meff")
p.labels(x="m_{eff} [GeV]", y = "Entries / 40 GeV")
p.xax(40,0,1200)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwLoose", "R1", "wwLoose_R1")
p.labels(x="R_{1}", y = "Entries / 0.1")
p.xax(0.1,0,1.0)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwLoose", "R2", "wwLoose_R2")
p.labels(x="R_{2}", y = "Entries / 0.1")
p.xax(0.1,0,1.0)
p.doLogY = True
p.yax(0.1, 100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwLoose", "deltaX", "wwLoose_deltaX")
p.labels(x="|x_{1}-x_{2}|", y="Entries / 0.004")
p.xax(0.004, 0,0.08)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwLoose", "abs(cosThetaB)", "wwLoose_cosThetaB")
p.labels(x="|cos#theta_{b}|", y = "Entries / 0.1")
p.xax(0.1,0,1)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwLoose", "mt2", "wwLoose_mt2")
p.labels(x="m_{T2} [GeV]", y = "Entries / 7 GeV")
p.xax(7,0,150)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwLoose", "pBll", "wwLoose_pBll")
p.labels(x="p_{b}^{ll} [GeV]", y = "Entries / 10 GeV")
p.xax(10,0,400)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwLoose", "dphi_met_pbll", "wwLoose_dphi_met_pbll")
p.labels(x="#Delta#phi(#slash{E}_{T},p_{b}^{ll})", y="Entries / 0.1")
p.xax(0.1,0,3.4)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

##
### CRZ
##

p = plot.Plot1D()
p.initialize("wwCRZ", "l_pt[0]", "wwCRZ_lpt0")
p.labels(x="Lead lepton p_{T} [GeV]", y = "Entries / 4 GeV")
p.xax(4,25, 75)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwCRZ", "l_pt[1]", "wwCRZ_lpt1")
p.labels(x="Sub-lead lepton p_{T} [GeV]", y = "Entries / 2 GeV")
p.xax(2,20,50)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwCRZ", "met", "wwCRZ_met")
p.labels(x="#slash{E}_{T} [GeV]", y = "Entries / 4 GeV")
p.xax(4, 20, 120)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwCRZ", "abs(cosThetaB)", "wwCRZ_cosThetaB")
p.labels(x="|cos#theta_{b}|", y = "Entries / 0.1")
p.xax(0.1, 0, 0.9)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwCRZ", "deltaX", "wwCRZ_deltaX")
p.labels(x="|x_{1}-x_{2}|", y = "Entries / 0.0025")
p.xax(0.0025, 0, 0.03)
p.doLogY = True
p.yax(0.1,1000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wwCRZ", "R2", "wwCRZ_R2")
p.labels(x="R_{2}", y = "Entries / 0.01")
p.xax(0.01, 0.3, 0.7)
p.doLogY = True
p.yax(0.1, 1000)
p.setRatioCanvas(p.name)
plots.append(p)
