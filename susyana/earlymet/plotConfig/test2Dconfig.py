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
zjets = background.Background("zjets", "Z+jets")
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
ttbar = background.Background("ttbar", "TTbar")
ttbar.set_debug()
ttbar.set_file(ttfile)
ttbar.scale_factor = 0.9
ttbar.set_color(r.TColor.GetColor("#E67067"))
ttbar.set_treename("TTbar_CENTRAL")
ttbar.set_merged_tree(ttbar.treename)
backgrounds.append(ttbar)

# w+jets
wjetsfile = "/afs/cern.ch/work/d/dantrim/public/SusyAna/ntuples/n0208/n0208/ttbar_wjets_mc15_13TeV.root"
wjets = background.Background("wjets", "W+jets")
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

#############################################
# Set up the plots
#############################################

plots = []

#### zlike_mm0j

p = plot.Plot2D()
p.initialize("twoLep_1j", "j_jvt[0]", "j_pt[0]", "twoLep_1j_jvt0_jpt0")
p.labels(x="Lead jet JVT", y="Lead jet p_{T} [GeV]")
p.set_sample("zjets")
p.xax(0.1,0.5,1)
#p.set_style("lego")
p.yax(5,25,100)
p.defaultCanvas()
plots.append(p)

