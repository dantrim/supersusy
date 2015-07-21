import sys
sys.path.append('../../../..')
import supersusy.utils.plot as plot
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region


#############################################
# Set up the samples
#############################################
zjetsfile = "/afs/cern.ch/work/d/dantrim/public/SusyAna/ntuples/n0208/n0208/mc15_13TeV.root"
backgrounds = []

#### MC
# z+jets
zfile = zjetsfile
zjets = background.Background("Zjets")
zjets.set_debug()
zjets.set_file(zfile)
zjets.scale_factor = 0.9
zjets.set_color(r.TColor.GetColor("#82DE68"))
zjets.set_fillStyle(3609)
zjets.set_treename("Zjets_CENTRAL")
zjets.set_merged_tree(zjets.treename)
backgrounds.append(zjets)

# ttbar
ttfile = "/afs/cern.ch/work/d/dantrim/public/SusyAna/ntuples/n0208/n0208/ttbar_wjets_mc15_13TeV.root"
ttbar = background.Background("TTbar")
ttbar.set_debug()
ttbar.set_file(ttfile)
ttbar.scale_factor = 0.9
ttbar.set_color(r.TColor.GetColor("#E67067"))
ttbar.set_treename("TTbar_CENTRAL")
ttbar.set_merged_tree(ttbar.treename)
backgrounds.append(ttbar)

# w+jets
wjetsfile = "/afs/cern.ch/work/d/dantrim/public/SusyAna/ntuples/n0208/n0208/ttbar_wjets_mc15_13TeV.root"
wjets = background.Background("Wjets")
wjets.set_debug()
wjets.set_file(wjetsfile)
wjets.scale_factor = 0.9
wjets.set_color(r.TColor.GetColor("#5E9AD6"))
wjets.set_treename("Wjets_CENTRAL")
wjets.set_merged_tree(wjets.treename)
backgrounds.append(wjets)

#### DATA
datafile = "/afs/cern.ch/work/d/dantrim/public/SusyAna/ntuples/n0208/data15_13TeV.root"
data = background.Data()
data.set_file(datafile)
data.set_color(r.kBlue)
data.set_treename("Data_CENTRAL")
data.set_merged_tree(data.treename)


#############################################
# Set up the regions
#############################################
regions = []
reg = region.Region()
reg.simplename = "zlike_mm0j"
reg.displayname = "Z#mu#mu 0-j (MC: Q*d0sig (BSCorr))"
reg.tcut = "nLeptons==2 && nMuons==2 && nJets==0 && nBJets==0 && l_pt[0]>20 && l_pt[1]>20 && (l_q[0]*l_q[1])<1 && abs(mll-91.2)<25"
regions.append(reg)

reg = region.Region()
reg.simplename = "zlike_mm0j_wd0"
reg.displayname = "Z-enriched"
reg.tcut = "nLeptons==2 && nMuons==2 && nJets==0 && nBJets==0 && l_pt[0]>20 && l_pt[1]>20 && abs(l_d0[0])<1 && abs(l_d0[1])<1"
regions.append(reg)

reg = region.Region()
reg.simplename = "zlike_mmj"
reg.displayname = "Z-enriched"
reg.tcut = "nLeptons==2 && nMuons==2 && nJets>=0 && l_pt[0]>20 && l_pt[1]>20 && (l_q[0]*l_q[1])<0 && abs(mll-91.2)<25"
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
p.initialize("zlike_mm0j", "l_d0[0]", "zlike_mm0j_ld00_dataQ")
p.labels(x="Lead lepton d0 [mm]", y="Entries")
p.xax(0.01,-0.2,0.2)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j", "l_d0sig[1]", "zlike_mm0j_ld0sig1")
p.labels(x="Sub-lead lepton d0sig", y="Entries")
p.xax(0.5,-10,10)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j", "l_d0sigBSCorr[0]", "zlike_mm0j_d0sigBSCorr0_mcQ")
p.labels(x="Lead lepton d0sig (BSCorr)", y="Entries")
p.xax(0.5,-10,10)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j", "l_q[1]*l_d0sig[1]", "zlike_mm0j_lQd0sig1")
p.labels(x="Sub-lead lepton Q*d0sig", y="Entries")
p.xax(0.5,-10,10)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

### zlike_mm0j_wd0

p = plot.Plot1D()
p.initialize("zlike_mm0j_wd0", "mll", "zlike_mm0j_mll_wd0")
p.labels(x="m_{#mu#mu} [GeV]", y="Entries / 2 GeV")
p.xax(2,70,110)
p.yax(0,1000)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j_wd0", "l_pt[0]", "zlike_mm0j_lpt0_wd0")
p.labels(x="Lead lepton p_{T} [GeV]", y="Entries / 2 GeV")
p.xax(2, 25, 90)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j_wd0", "l_pt[1]", "zlike_mm0j_lpt1_wd0")
p.labels(x="Sub-lead lepton p_{T} [GeV]", y="Entries / 5 GeV")
p.xax(5, 25, 120)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j_wd0", "nJets", "zlike_mm0j_nJets_wd0")
p.labels(x="Number of Jets", y="Entries")
p.xax(1,0,8)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mm0j_wd0", "met", "zlike_mm0j_met_wd0")
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
p.xax(5,0,180)
p.doLogY = True
p.yax(0.001,10000)
p.defaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmj", "refJet_et", "zlike_mmj_refJet_et")
p.labels(x="TST #slash{E}_{T} jet term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,180)
p.doLogY = True
p.yax(0.001,10000)
p.defaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmj", "refMuo_et", "zlike_mmj_refMuo_et")
p.labels(x="TST #slash{E}_{T} jet term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,180)
p.doLogY = True
p.yax(0.001,10000)
p.defaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmj", "softTerm_et", "zlike_mmj_softTerm_et")
p.labels(x="TST #slash{E}_{T} jet term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,180)
p.doLogY = True
p.yax(0.001,10000)
p.defaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmj", "metX", "zlike_mmj_metX")
p.labels(x="TST #slash{E}_{T}-x [GeV]", y="Entries / 5 GeV")
p.xax(5,-150,150)
p.doLogY = True
p.yax(0.001,10000)
p.defaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike_mmj", "metY", "zlike_mmj_metY")
p.labels(x="TST #slash{E}_{T}-y [GeV]", y="Entries / 5 GeV")
p.xax(5,-150,150)
p.doLogY = True
p.yax(0.001,10000)
p.defaultCanvas(p.name)
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


