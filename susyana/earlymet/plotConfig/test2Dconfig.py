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
zmm.set_scale_factor = 0.9
zmm.set_color(r.TColor.GetColor("#82DE68"))
zmm.set_treename("Zmm_CENTRAL")
zmm.set_merged_tree(zmm.treename)
backgrounds.append(zmm)

# ttbar
ttbar = background.Background("ttbar", "TTbar")
ttbar.set_debug()
ttbar.set_file(mcfile)
ttbar.scale_factor = 0.9
ttbar.set_color(r.TColor.GetColor("#E67067"))
ttbar.set_treename("TTbar_CENTRAL")
ttbar.set_merged_tree(ttbar.treename)
backgrounds.append(ttbar)

# wjets
wjets = background.Background("wjets", "W+jets")
wjets.set_debug()
wjets.set_file(mcfile)
wjets.scale_factor = 0.9
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
reg.displayname = "Z#mu#mu 0-j (MC: Q*d0sig (BSCorr))"
reg.tcut = "nLeptons==2 && nMuons==2 && nJets==0 && nBJets==0 && l_pt[0]>20 && l_pt[1]>20 && (l_q[0]*l_q[1])<1 && abs(mll-91.2)<25"
regions.append(reg)

reg = region.Region()
reg.simplename = "zlike_mm0j_wd0"
reg.displayname = "Z-enriched"
reg.tcut = "nLeptons==2 && nMuons==2 && nJets==0 && nBJets==0 && l_pt[0]>20 && l_pt[1]>20 && abs(l_d0[0])<1 && abs(l_d0[1])<1"
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

reg = region.Region()
reg.simplename = "zlike_mm1j"
reg.displayname = "Z#mu#mu-1j"
reg.tcut = "nLeptons==2 && nJets==1 && nBJets==0 && l_pt[0]>20 && l_pt[1]>20 && (l_q[0]*l_q[1])<0 && abs(mll-91.2)<25"
regions.append(reg)

reg = region.Region()
reg.simplename = "twoLep_1j"
reg.displayname = "2l-1j"
reg.tcut = "nLeptons==2 && nJets==1 && nBJets==0"
regions.append(reg)


reg = region.Region()
reg.simplename = "zlike_mmj"
reg.displayname = "Z#mu#mu >=0j (no d0sig, no zsin)"
reg.tcut = "nLeptons==2 && nMuons==2 && nJets>=0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>25 && (l_q[0]*l_q[1])<0 && abs(mll-91.2)<25"
regions.append(reg)

#############################################
# Set up the plots
#############################################

plots = []

p = plot.Plot2D()
p.initialize("zlike_mmj", "l_eta[0]", "l_d0sigBSCorr[0]", "zlike_mmj_d0sigBSCorr_eta0_data_prof")
p.labels(x="Lead lepton #eta", y="Lead lepton d0sig (BSCorr)")
p.set_sample("Data")
p.xax(0.5,-3,3)
p.yax(0.5,-0.035,0.035)
p.doProfile()
p.defaultCanvas()
plots.append(p)


p = plot.Plot2D()
p.initialize("zlike_mmj", "l_phi[0]", "l_d0sigBSCorr[0]", "zlike_mmj_d0sigBSCorr_phi0_data_prof")
p.labels(x="Lead lepton #phi", y="Lead lepton d0sig (BSCorr)")
p.set_sample("Data")
p.xax(0.5,-3,3)
p.yax(0.5,-0.04,0.04)
p.doProfile()
p.defaultCanvas()
plots.append(p)

#p = plot.Plot2D()
#p.initialize("zlike_mmj", "l_eta[0]", "l_d0sig[0]", "zlike_mmj_d0sig_eta0_data_prof")
#p.labels(x="Lead lepton #eta", y="Lead lepton d0sig")
#p.set_sample("Data")
#p.xax(0.5,-3,3)
#p.yax(0.5,-0.09,0.09)
#p.doProfile()
#p.defaultCanvas()
#plots.append(p)
#
#p = plot.Plot2D()
#p.initialize("zlike_mmj", "l_phi[0]", "l_d0sig[0]", "zlike_mmj_d0sig_phi0_data_prof")
#p.labels(x="Lead lepton #phi", y="Lead lepton d0sig")
#p.set_sample("Data")
#p.xax(0.5,-3,3)
#p.yax(0.5,-0.04,0.04)
#p.doProfile()
#p.defaultCanvas()
#plots.append(p)

### d0(eta), d0(phi)
#p = plot.Plot2D()
#p.initialize("zlike_mmj", "l_eta[0]", "l_d0[0]", "zlike_mmj_d00_eta0_data_prof")
#p.labels(y="Lead lepton d0 [mm]", x="Lead lepton #eta")
#p.set_sample("Data")
#p.yax(0.005,-0.1,0.1)
#p.xax(0.5,-3,3)
#p.doProfile()
#p.defaultCanvas()
#plots.append(p)
#
#p = plot.Plot2D()
#p.initialize("zlike_mmj", "l_phi[0]", "l_d0[0]", "zlike_mmj_d00_phi0_data_prof")
#p.labels(y="Lead lepton d0 [mm]", x="Lead lepton #phi")
#p.set_sample("Data")
#p.yax(0.005,-0.1,0.1)
#p.xax(0.5,-3,3)
#p.doProfile()
#p.defaultCanvas()
#plots.append(p)
