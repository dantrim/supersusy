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
reg.simplename = "zlike_mm0j"
reg.displayname = "Z#mu#mu 0-j"
reg.tcut = "nLeptons==2 && nMuons==2 && nJets==0 && nBJets==0 && l_pt[0]>20 && l_pt[1]>20 && (l_q[0]*l_q[1])<1 && abs(mll-91.2)<25"
regions.append(reg)

reg = region.Region()
reg.simplename = "zlike_mm0j_wd0z0"
reg.displayname = "Z#mu#mu 0-j (w/ d0 + z0)"
reg.tcut = "nLeptons==2 && nMuons==2 && nJets==0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>25 && abs(l_d0[0])<1 && abs(l_d0[1])<1 && abs(l_z0[0])<2 && abs(l_z0[1])<2"
regions.append(reg)


reg = region.Region()
reg.simplename = "zlike_mm0j_wd0"
reg.displayname = "Z#mu#mu 0-j (w/ d0)"
reg.tcut = "nLeptons==2 && nMuons==2 && nJets==0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>25 && abs(l_d0[0])<1 && abs(l_d0[1])<1"
regions.append(reg)

reg = region.Region()
reg.simplename = "zlike_mmj_dsigzsin"
reg.displayname = "Z#mu#mu >=0j (d0sig and zsin)"
reg.tcut = "nLeptons==2 && nMuons==2 && nJets>=0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>25 && (l_q[0]*l_q[1])<0 && abs(mll-91.2)<25 && abs(l_d0sig[0])<3 && abs(l_d0sig[1])<3 && abs(l_z0sinTheta)<0.4 && abs(l_z0sinTheta)<0.4"
regions.append(reg)

reg = region.Region()
reg.simplename = "zlike_mmj_dsig"
reg.displayname = "Z#mu#mu >=0j (d0sig)"
reg.tcut = "nLeptons==2 && nMuons==2 && nJets>=0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>25 && (l_q[0]*l_q[1])<0 && abs(mll-91.2)<25 && abs(l_d0sig[0])<3 && abs(l_d0sig[1])<3"
regions.append(reg)

reg = region.Region()
reg.simplename = "zlike_mmj"
reg.displayname = "Z#mu#mu >=0j (no d0sig, no zsin)"
reg.tcut = "nLeptons==2 && nMuons==2 && nJets>=0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>25 && (l_q[0]*l_q[1])<0 && abs(mll-91.2)<25"
regions.append(reg)

reg = region.Region()
reg.simplename = "zlike_mmjNegEta"
reg.displayname = "Z#mu#mu >=0j (#eta^{0}<0, w/ d0sig)"
reg.tcut = "nLeptons==2 && nMuons==2 && nJets>=0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>25 && (l_q[0]*l_q[1])<0 && abs(mll-91.2)<25 && l_eta[0]<0 && abs(l_d0sig[0])<3 && abs(l_d0sig[1])<3"
regions.append(reg)

reg = region.Region()
reg.simplename = "zmm_positive"
reg.displayname = "Z#mu#mu (Lead lepton Q+)"
reg.tcut = "nLeptons==2 && nMuons==2 && nJets==0 && nBJets==0 && l_pt[0]>20 && l_pt[1]>20 && (l_q[0]*l_q[1])<0 && l_q[0]>0"
regions.append(reg)

reg = region.Region()
reg.simplename = "zmm_negative"
reg.displayname = "Z#mu#mu (Lead lepton Q-)"
reg.tcut = "nLeptons==2 && nMuons==2 && nJets==0 && nBJets==0 && l_pt[0]>20 && l_pt[1]>20 && (l_q[0]*l_q[1])<0 && l_q[0]<0"
regions.append(reg)


#############################################
# Set up the plots
#############################################

plots = []

#### zlike_mm0j

p = plot.Plot1D()
p.initialize("zlike_mm0j", "mll", "zlike_mm0j_mll")
p.labels(x="m_{#mu#mu} [GeV]", y="Entries / 2 GeV")
p.xax(2,70,110)
p.yax(0,1000)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j", "l_pt[0]", "zlike_mm0j_lpt0")
p.labels(x="Lead lepton p_{T} [GeV]", y="Entries / 2 GeV")
p.xax(2, 25, 90)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j", "l_pt[1]", "zlike_mm0j_lpt1")
p.labels(x="Sub-lead lepton p_{T} [GeV]", y="Entries / 5 GeV")
p.xax(5, 25, 120)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j", "l_eta[0]", "zlike_mm0j_leta0")
p.labels(x="Lead lepton #eta", y="Entries")
p.xax(0.5, 5, 5)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j", "l_eta[1]", "zlike_mm0j_leta1")
p.labels(x="Sub-lead lepton #eta", y="Entries")
p.xax(0.5, 5, 5)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)


p = plot.Plot1D()
p.initialize("zlike_mm0j", "nJets", "zlike_mm0j_nJets")
p.labels(x="Number of Jets", y="Entries")
p.xax(1,0,8)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j", "met", "zlike_mm0j_met")
p.labels(x="TST #slash{E}_{T} [GeV]", y="Entries / 5 GeV")
p.xax(5,0,180)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j", "refJet_et", "zlike_mm0j_refJet_et")
p.labels(x="TST #slash{E}_{T} jet term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,180)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j", "refMuo_et", "zlike_mm0j_refMuo_et")
p.labels(x="TST #slash{E}_{T} muon term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,180)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j", "softTerm_et", "zlike_mm0j_softTerm_et")
p.labels(x="TST #slash{E}_{T} muon term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,180)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j", "l_d0sig[0]", "zlike_mm0j_d0sig0")
p.labels(x="Lead lepton d0sig", y="Entries")
p.xax(0.5,-10,10)
p.yax(0.1,1000000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j", "l_d0sigBSCorr[0]", "zlike_mm0j_d0sigBSCorr0")
p.labels(x="Lead lepton d0sig (BSCorr)", y="Entries")
p.xax(0.5,-10,10)
p.yax(0.1,1000000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j", "l_d0[0]", "zlike_mm0j_d00")
p.labels(x="Lead lepton d0 [mm]", y="Entries")
p.xax(0.01,-0.2,0.2)
p.yax(0.1,1000000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

### zlike_mm0j_wd0

p = plot.Plot1D()
p.initialize("zlike_mm0j_wd0", "mll", "zlike_mm0j_wd0_mll")
p.labels(x="m_{#mu#mu} [GeV]", y="Entries / 2 GeV")
p.xax(2,70,110)
p.yax(0,1000)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j_wd0", "l_pt[0]", "zlike_mm0j_wd0_lpt0")
p.labels(x="Lead lepton p_{T} [GeV]", y="Entries / 2 GeV")
p.xax(2, 25, 90)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j_wd0", "l_pt[1]", "zlike_mm0j_wd0_lpt1")
p.labels(x="Sub-lead lepton p_{T} [GeV]", y="Entries / 5 GeV")
p.xax(5, 25, 120)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j_wd0", "nJets", "zlike_mm0j_wd0_nJets")
p.labels(x="Number of Jets", y="Entries")
p.xax(1,0,8)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j_wd0", "met", "zlike_mm0j_wd0_met")
p.labels(x="TST #slash{E}_{T} [GeV]", y="Entries / 5 GeV")
p.xax(5,0,180)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)


### zlike_mm0j_wd0wz0
p = plot.Plot1D()
p.initialize("zlike_mm0j_wd0z0", "mll", "zlike_mm0j_wd0z0_mll")
p.labels(x="m_{#mu#mu} [GeV]", y="Entries / 2 GeV")
p.xax(2,70,110)
p.yax(0,1000)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j_wd0z0", "l_pt[0]", "zlike_mm0j_wd0z0_lpt0")
p.labels(x="Lead lepton p_{T} [GeV]", y="Entries / 2 GeV")
p.xax(2, 25, 90)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j_wd0z0", "l_pt[1]", "zlike_mm0j_wd0z0_lpt1")
p.labels(x="Sub-lead lepton p_{T} [GeV]", y="Entries / 5 GeV")
p.xax(5, 25, 120)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j_wd0z0", "nJets", "zlike_mm0j_wd0z0_nJets")
p.labels(x="Number of Jets", y="Entries")
p.xax(1,0,8)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j_wd0z0", "met", "zlike_mm0j_wd0z0_met")
p.labels(x="TST #slash{E}_{T} [GeV]", y="Entries / 5 GeV")
p.xax(5,0,180)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

#### zlike_mmj

p = plot.Plot1D()
p.initialize("zlike_mmj", "met", "zlike_mmj_met")
p.labels(x="TST #slash{E}_{T} [GeV]", y="Entries / 5 GeV")
p.xax(5,0,200)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmj", "refJet_et", "zlike_mmj_refJet_et")
p.labels(x="TST #slash{E}_{T} jet term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,200)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmj", "refMuo_et", "zlike_mmj_refMuo_et")
p.labels(x="TST #slash{E}_{T} muon term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,200)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmj", "softTerm_et", "zlike_mmj_softTerm_et")
p.labels(x="TST #slash{E}_{T} soft term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,60)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmj", "metX", "zlike_mmj_metX")
p.labels(x="TST #slash{E}_{T}-x [GeV]", y="Entries / 5 GeV")
p.xax(5,-150,150)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmj", "metY", "zlike_mmj_metY")
p.labels(x="TST #slash{E}_{T}-y [GeV]", y="Entries / 5 GeV")
p.xax(5,-150,150)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)


p = plot.Plot1D()
p.initialize("zlike_mmj", "j_jvf[0]", "zlike_mmj_jvf0")
p.labels(x="Lead jet JVF", y="Entries")
p.xax(0.05,-0.2,1)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

#### zlike_mmj_dsigzsin
p = plot.Plot1D()
p.initialize("zlike_mmj_dsigzsin", "met", "zlike_mmj_dsigzsin_met")
p.labels(x="TST #slash{E}_{T} [GeV]", y="Entries / 5 GeV")
p.xax(5,0,200)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmj_dsigzsin", "refJet_et", "zlike_mmj_dsigzsin_refJet_et")
p.labels(x="TST #slash{E}_{T} jet term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,200)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmj_dsigzsin", "refMuo_et", "zlike_mmj_dsigzsin_refMuo_et")
p.labels(x="TST #slash{E}_{T} muon term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,200)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmj_dsigzsin", "softTerm_et", "zlike_mmj_dsigzsin_softTerm_et")
p.labels(x="TST #slash{E}_{T} soft term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,60)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmj_dsigzsin", "metX", "zlike_mmj_dsigzsin_metX")
p.labels(x="TST #slash{E}_{T}-x [GeV]", y="Entries / 5 GeV")
p.xax(5,-150,150)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmj_dsigzsin", "metY", "zlike_mmj_dsigzsin_metY")
p.labels(x="TST #slash{E}_{T}-y [GeV]", y="Entries / 5 GeV")
p.xax(5,-150,150)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)


#### zlike_mmj_dsig

p = plot.Plot1D()
p.initialize("zlike_mmj_dsig", "met", "zlike_mmj_dsig_met")
p.labels(x="TST #slash{E}_{T} [GeV]", y="Entries / 5 GeV")
p.xax(5,0,200)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmj_dsig", "refJet_et", "zlike_mmj_dsig_refJet_et")
p.labels(x="TST #slash{E}_{T} jet term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,200)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmj_dsig", "refMuo_et", "zlike_mmj_dsig_refMuo_et")
p.labels(x="TST #slash{E}_{T} jet term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,200)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmj_dsig", "softTerm_et", "zlike_mmj_dsig_softTerm_et")
p.labels(x="TST #slash{E}_{T} jet term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,60)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmj_dsig", "metX", "zlike_mmj_dsig_metX")
p.labels(x="TST #slash{E}_{T}-x [GeV]", y="Entries / 5 GeV")
p.xax(5,-150,150)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmj_dsig", "metY", "zlike_mmj_dsig_metY")
p.labels(x="TST #slash{E}_{T}-y [GeV]", y="Entries / 5 GeV")
p.xax(5,-150,150)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

### zmm_positive
p = plot.Plot1D()
p.initialize("zmm_positive", "l_d0sig[0]", "zmm_positive_ld0sig0")
p.labels(x="Postive lead lepton d0sig", y="Entries")
p.xax(0.5,-10,10)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zmm_positive", "l_d0[0]", "zmm_positive_ld00")
p.labels(x="Postive lead lepton d0 [mm]", y="Entries")
p.xax(0.01,-0.2,0.2)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

### zmm_negative
p = plot.Plot1D()
p.initialize("zmm_negative", "l_d0sig[0]", "zmm_negative_ld0sig0")
p.labels(x="Negative lead lepton d0sig", y="Entries")
p.xax(0.5,-10,10)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zmm_negative", "l_d0[0]", "zmm_negative_ld00")
p.labels(x="Negative lead lepton d0 [mm]", y="Entries")
p.xax(0.01,-0.2,0.2)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

#### zlike_mmjNegEta

p = plot.Plot1D()
p.initialize("zlike_mmjNegEta", "met", "zlike_mmjNegEta_met")
p.labels(x="TST #slash{E}_{T} [GeV]", y="Entries / 5 GeV")
p.xax(5,0,200)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmjNegEta", "refJet_et", "zlike_mmjNegEta_refJet_et")
p.labels(x="TST #slash{E}_{T} jet term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,200)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmjNegEta", "refMuo_et", "zlike_mmjNegEta_refMuo_et")
p.labels(x="TST #slash{E}_{T} muon term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,200)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmjNegEta", "softTerm_et", "zlike_mmjNegEta_softTerm_et")
p.labels(x="TST #slash{E}_{T} soft term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,60)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmjNegEta", "metX", "zlike_mmjNegEta_metX")
p.labels(x="TST #slash{E}_{T}-x [GeV]", y="Entries / 5 GeV")
p.xax(5,-150,150)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmjNegEta", "metY", "zlike_mmjNegEta_metY")
p.labels(x="TST #slash{E}_{T}-y [GeV]", y="Entries / 5 GeV")
p.xax(5,-150,150)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)


p = plot.Plot1D()
p.initialize("zlike_mmjNegEta", "j_jvt[0]", "zlike_mmjNegEta_jvt0")
p.labels(x="Lead jet JVT", y="Entries")
p.xax(0.05,-0.2,1)
p.doLogY = True
p.yax(0.1,10000)
p.setRatioCanvas(p.name)
plots.append(p)
