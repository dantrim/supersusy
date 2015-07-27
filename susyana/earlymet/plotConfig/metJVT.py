import sys
sys.path.append('../../../..')
import supersusy.utils.plot as plot
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region


#############################################
# Set up the samples
#############################################
scratchdir = "/scratch/dantrim/n0209/july24/"
#datafile = scratchdir + "data15_13TeV.root"
datafile = scratchdir + "data15_periodC_13TeV.root"
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
reg.simplename = "zlike_mmj"
reg.displayname = "Z#mu#mu >=0j"
reg.tcut = "nLeptons==2 && nMuons==2 && nJets>=0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>25 && (l_q[0]*l_q[1])<0 && abs(mll-91.2)<25"
regions.append(reg)

#############################################
# Set up the plots
#############################################

plots = []

#########################
# Region: zlike_mmj
#########################

### mll
p = plot.Plot1D()
p.initialize("zlike_mmj", "mll", "zlike_mmj_mll")
p.labels(x="m_{#mu#mu} [GeV]", y="Entries / 2 GeV")
p.xax(2,70,110)
p.yax(0,15000)
p.doLogY = False
p.setRatioCanvas(p.name)
plots.append(p)

### met
p = plot.Plot1D()
p.initialize("zlike_mmj", "met", "zlike_mmj_met")
p.labels(x="TST #slash{E}_{T} (JVT cut) [GeV]", y="Entries / 5 GeV")
p.xax(5, 0, 200)
p.yax(0.1, 100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

### met jet term
p = plot.Plot1D()
p.initialize("zlike_mmj", "refJet_et", "zlike_mmj_refJet_et")
p.labels(x="TST #slash{E}_{T} jet term (JVT cut) [GeV]", y="Entries / 10 GeV")
p.xax(10, 0, 300)
p.yax(0.1, 100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

### met muon term
p = plot.Plot1D()
p.initialize("zlike_mmj", "refMuo_et", "zlike_mmj_refMuo_et")
p.labels(x="TST #slash{E}_{T} muon term (JVT cut) [GeV]", y="Entries / 10 GeV")
p.xax(10, 0, 300)
p.yax(0.1, 100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

### met soft term
p = plot.Plot1D()
p.initialize("zlike_mmj", "softTerm_et", "zlike_mmj_softTerm_et")
p.labels(x="TST #slash{E}_{T} soft term (JVT cut) [GeV]", y="Entries / 2 GeV")
p.xax(2, 0, 60)
p.yax(0.1, 100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

### met-x
p = plot.Plot1D()
p.initialize("zlike_mmj", "metX", "zlike_mmj_metX")
p.labels(x="TST #slash{E}_{T}-x (JVT cut) [GeV]", y="Entries / 5 GeV")
p.xax(5, -130, 130)
p.yax(0.1, 10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

### met-y
p = plot.Plot1D()
p.initialize("zlike_mmj", "metY", "zlike_mmj_metY")
p.labels(x="TST #slash{E}_{T}-y (JVT cut) [GeV]", y="Entries / 5 GeV")
p.xax(5, -130, 130)
p.yax(0.1, 10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

### dphi met jet term
p = plot.Plot1D()
p.initialize("zlike_mmj", "dphi_met_jetTerm", "zlike_mmj_dphi_met_jetTerm")
p.labels(x="#Delta#phi(#slash{E}_{T}, jet-Term) (JVT cut)", y="Entries")
p.xax(0.2, -3.2, 3.2)
p.yax(0.1, 10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

### dphi met muon term
p = plot.Plot1D()
p.initialize("zlike_mmj", "dphi_met_muonTerm", "zlike_mmj_dphi_met_muonTerm")
p.labels(x="#Delta#phi(#slash{E}_{T}, muon-Term) (JVT cut)", y="Entries")
p.xax(0.2, -3.2, 3.2)
p.yax(0.1, 10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

### dphi met soft term
p = plot.Plot1D()
p.initialize("zlike_mmj", "dphi_met_softTerm", "zlike_mmj_dphi_met_softTerm")
p.labels(x="#Delta#phi(#slash{E}_{T}, soft-Term) (JVT cut)", y="Entries")
p.xax(0.2, -3.2, 3.2)
p.yax(0.1, 10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)


