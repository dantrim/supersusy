import os
import sys
sys.path.append(os.environ['SUSYDIR'])
#sys.path.append('../../../../../')
import supersusy.utils.plot as plot
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region
import supersusy.utils.systematic as systematic


#############################################
# Set up the samples
#############################################
rawdir = "/gdata/atlas/dantrim/SusyAna/histoAna/run2early/n0213/mc/corrected/Raw/" 
data_rawdir = "/gdata/atlas/dantrim/SusyAna/histoAna/run2early/n0213/data/corrected/Raw/"
filelist_dir = "/gdata/atlas/dantrim/SusyAna/n0213val/Superflow/run/filelists/"
backgrounds = []

#### MC
# Zjets
zjets = background.Background("zjets", "Z+jets (Sherpa)")
zjets.set_debug()
zjets.scale_factor = 1.0
zjets.set_color(r.TColor.GetColor("#82DE68"))
#zjets.set_treename("Zjets_powheg")
zjets.set_treename("Zjets_sherpa")
#zjets.set_chain_from_list(filelist_dir + "zjets_powheg_n0213.txt", rawdir)
zjets.set_chain_from_list(filelist_dir + "zjets_sherpa_n0213.txt", rawdir)
backgrounds.append(zjets)

ttbar = background.Background("ttbar", "TTbar")
ttbar.set_debug()
ttbar.scale_factor = 1.0
ttbar.set_color(r.TColor.GetColor("#E67067"))
ttbar.set_treename("ttbar_powheg")
ttbar.set_chain_from_list(filelist_dir + "ttbar_powheg_n0213.txt", rawdir)
backgrounds.append(ttbar)

# singletop
stop = background.Background("st", "ST")
stop.set_debug()
stop.scale_factor = 1.0
stop.set_color(r.TColor.GetColor("#DE080C"))
stop.set_treename("ST")
stop.set_chain_from_list(filelist_dir + "singletop_powheg_n0213.txt", rawdir)
backgrounds.append(stop)

# wjets
wjets = background.Background("wjets", "W+jets (Sherpa)")
wjets.set_debug()
wjets.scale_factor = 1.0
wjets.set_color(r.TColor.GetColor("#5E9AD6"))
wjets.set_treename("Wjets_sherpa")
wjets.set_chain_from_list(filelist_dir + "wjets_sherpa_n0213.txt", rawdir)
backgrounds.append(wjets)

# ww
ww = background.Background("ww", "WW (Powheg)")
ww.set_debug()
ww.scale_factor = 1.0
ww.set_color(r.TColor.GetColor("#315E88"))
ww.set_treename("WW_powheg")
ww.set_chain_from_list(filelist_dir + "ww_powheg_n0213.txt", rawdir)
backgrounds.append(ww)

# wz
wz = background.Background("wz", "WZ (Powheg)")
wz.set_debug()
wz.scale_factor = 1.0
wz.set_color(r.TColor.GetColor("#F9F549"))
wz.set_treename("WZ_powheg")
wz.set_chain_from_list(filelist_dir + "wz_powheg_n0213.txt", rawdir)
backgrounds.append(wz)

# zz
zz = background.Background("zz", "ZZ (Powheg)")
zz.set_debug()
zz.scale_factor = 1.0
zz.set_color(r.TColor.GetColor("#FFEF53"))
zz.set_treename("ZZ_powheg")
zz.set_chain_from_list(filelist_dir + "zz_powheg_n0213.txt", rawdir)
backgrounds.append(zz)

#### DATA
data = background.Data()
data.set_color(r.kBlack)
data.set_treename("Data")
data.set_chain_from_list(filelist_dir + "data15_periodA_n0213.txt", data_rawdir)

#############################################
# Set up the systematics
#############################################
systematics = []

syst = systematic.Systematic("PILEUP", "UP", "DOWN")
syst.setWeightSys() 
systematics.append(syst)

syst = systematic.Systematic("MUEFFSYST", "UP", "DOWN")
syst.setWeightSys() 
systematics.append(syst)

syst = systematic.Systematic("MUEFFSTAT", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)

syst = systematic.Systematic("ELEFFRECO", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)

syst = systematic.Systematic("ELEFFID", "UP", "DOWN")
syst.setWeightSys()
systematics.append(syst)


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

reg = region.Region()
reg.simplename = "wlikem"
reg.displayname = "W-like (#mu)"
reg.tcut = "nLeptons==1 && nMuons==1 && met > 50 && l_pt[0]>25 && abs(l_d0sigBSCorr[0])<3 && nBJets==0"
#reg.tcut = "nLeptons==1 && nMuons==1 && met > 50 &&  nBJets==0"
regions.append(reg)



#############################################
# Set up the plots
#############################################

plots = []

#### wlikem

p = plot.Plot1D()
p.initialize("wlikem", "mT0", "wlikem_mt0")
p.labels(x="Transverse mass [GeV]", y = "Entries / 5 GeV")
p.xax(5, 0, 275)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "l_pt[0]", "wlikem_lpt0")
p.labels(x="Lead lepton p_{T} [GeV]", y="Entries / 6 GeV")
p.xax(6, 25, 300)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "l_eta[0]", "wlikem_leta0")
p.labels(x="Lead lepton #eta", y="Entries / 0.2")
p.xax(0.2,-3, 3)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "MDR", "wlikem_MDR")
p.labels(x="M_{#Delta}^{R} [GeV]", y = "Entries / 5 GeV")
p.xax(5,0,140)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "nSJets", "wlikem_nSJets")
p.labels(x="Number of jets", y = "Entries / 1")
p.xax(1,0,15)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "sj_pt[0]", "wlikem_sjpt0")
p.labels(x="Lead jet p_{T} [GeV]", y = "Entries / 30 GeV")
p.xax(30,0,700)
p.doLogY=True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)


p = plot.Plot1D()
p.initialize("wlikem", "sj_eta[0]", "wlikem_sjeta0")
p.labels(x="Lead jet #eta", y = "Entries / 0.2")
p.xax(0.2,-3,3)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "sj_jvt[0]", "wlikem_sjvt0")
p.labels(x="Lead jet JVT", y = "Entries / 0.05")
p.xax(0.05, -0.5, 1.2)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "sj_pt[1]", "wlikem_sjpt1")
p.labels(x="Sub-lead jet p_{T} [GeV]", y = "Entries / 15 GeV")
p.xax(15,0,300)
p.doLogY=True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "sj_eta[1]", "wlikem_sjeta1")
p.labels(x="Sub-lead jet #eta", y = "Entries / 0.2")
p.xax(0.2,-3,3)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "sj_jvt[1]", "wlikem_sjvt1")
p.labels(x="Sub-lead jet JVT", y = "Entries / 0.05")
p.xax(0.05, -0.5, 1.2)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "met", "wlikem_met")
p.labels(x="TST #slash{E}_{T} [GeV]", y="Entries / 10 GeV")
p.xax(10,0,400)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "sumet", "wlikem_sumet")
p.labels(x="#sum E_{T} [GeV]", y = "Entires / 60 GeV")
p.xax(60,40,1200)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "refJet_et", "wlikem_refJet_et")
p.labels(x="TST #slash{E}_{T} jet term [GeV]", y="Entries / 10 GeV")
p.xax(10,0,300)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "refMuo_et", "wlikem_refMuo_et")
p.labels(x="TST #slash{E}_{T} muon term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,180)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "refEle_et", "wlikem_refEle_et")
p.labels(x="TST #slash{E}_{T} electron term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,180)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "softTerm_et", "wlikem_softTerm_et")
p.labels(x="TST #slash{E}_{T} soft term [GeV]", y="Entries / 3 GeV")
p.xax(3,0,60)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "refMuo_sumet", "wlikem_refMuo_sumet")
p.labels(x="#sum E_{T} muon-term [GeV]", y="Entries / 10 GeV")
p.xax(10, 0, 250)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "refEle_sumet", "wlikem_refEle_sumet")
p.labels(x="#sum E_{T} electron-term [GeV]", y="Entries / 10 GeV")
p.xax(10, 0, 250)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "refJet_sumet", "wlikem_refJet_sumet")
p.labels(x="#sum E_{T} jet term [GeV]", y="Entries / 25 GeV")
p.xax(25,0,650)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "softTerm_sumet", "wlikem_softTerm_sumet")
p.labels(x="#sum E_{T} soft-term [GeV]", y="Entries / 5 GeV")
p.xax(5,0, 150)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "l_d0sig[0]", "wlikem_d0sig0")
p.labels(x="Lead lepton d0sig", y="Entries")
p.xax(0.5,-10,10)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "l_d0sigBSCorr[0]", "wlikem_d0sigBSCorr0")
p.labels(x="Lead lepton d0sig (BSCorr)", y="Entries")
p.xax(0.5,-10,10)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "l_d0[0]", "wlikem_d00")
p.labels(x="Lead lepton d0 [mm]", y="Entries")
p.xax(0.01,-0.2,0.2)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "meff", "wlikem_meff")
p.labels(x="m_{eff} [GeV]", y = "Entries / 80 GeV")
p.xax(80, 40, 2000)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "l_ptvarcone20[0]", "wlikem_ptvarcone200")
p.labels(x="Lead lepton ptvarcone20 [GeV]", y = "Entries / 0.2 GeV")
p.xax(0.2, 0, 6)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "l_etconetopo20[0]", "wlikem_etconetopo200")
p.labels(x="Lead lepton etconetopo20 [GeV]", y = "Entries / 0.2 GeV")
p.xax(0.2, 0, 6)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("wlikem", "l_etconetopo30[0]", "wlikem_etconetopo300")
p.labels(x="Lead lepton etconetopo30 [GeV]", y = "Entries / 0.4 GeV")
p.xax(0.4, 0, 10)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

