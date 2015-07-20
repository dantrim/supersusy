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
zjets.set_color(r.TColor.GetColor("#82DE68"))
zjets.set_treename("Zjets_CENTRAL")
zjets.set_merged_tree(zjets.treename)
backgrounds.append(zjets)

# ttbar
ttfile = "/afs/cern.ch/work/d/dantrim/public/SusyAna/ntuples/n0208/n0208/ttbar_wjets_mc15_13TeV.root"
ttbar = background.Background("TTbar")
ttbar.set_debug()
ttbar.set_file(ttfile)
ttbar.set_color(r.TColor.GetColor("#E67067"))
ttbar.set_treename("TTbar_CENTRAL")
ttbar.set_merged_tree(ttbar.treename)
backgrounds.append(ttbar)

# w+jets
wjetsfile = "/afs/cern.ch/work/d/dantrim/public/SusyAna/ntuples/n0208/n0208/ttbar_wjets_mc15_13TeV.root"
wjets = background.Background("Wjets")
wjets.set_debug()
wjets.set_file(wjetsfile)
wjets.set_color(r.TColor.GetColor("#5E9AD6"))
wjets.set_treename("Wjets_CENTRAL")
wjets.set_merged_tree(wjets.treename)
backgrounds.append(wjets)

#### DATA
datafile = "/afs/cern.ch/work/d/dantrim/public/SusyAna/ntuples/n0208/data15_13TeV.root"
data = background.Data()
data.set_file(datafile)
data.set_treename("Data_CENTRAL")
data.set_merged_tree(data.treename)


#############################################
# Set up the regions
#############################################
regions = []
reg = region.Region()
reg.simplename = "zlike"
reg.displayname = "Z-enriched"
reg.tcut = "nLeptons==2 && nMuons==2 && nJets>=0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>25 && abs(l_d0[0])<1 && abs(l_d0[1])<1"
regions.append(reg)

reg = region.Region()
reg.simplename = "ttlike"
reg.displayname = "ttbar"
reg.tcut = "nLeptons>=1 && nJets>=1 && nBJets>0 && l_pt[0]>2 && met>40"
regions.append(reg)


#############################################
# Set up the plots
#############################################

plots = []
# test plot
#p = plot.Plot1D()
#p.initialize(variable="l_pt[0]", region="zlike", name = "zlike_l_pt0")
#p.labels(x="Lead lepton p_{T} [GeV]", y="Entries / 5 GeV")
#p.xax(5, 25, 150)
#p.yax(0,1500)
##p.setRatioCanvas(p.name)
#p.defaultCanvas(p.name)
#plots.append(p)

p = plot.Plot1D()
p.initialize("zlike", "mll", "zlike_mll")
p.labels(x="m_{ee} [GeV]", y="Entries / 2 GeV")
p.xax(2,70,110)
p.yax(0,1800)
p.defaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike", "l_pt[0]", "zlike_lpt0")
p.labels(x="Lead lepton p_{T} [GeV]", y="Entries / 5 GeV")
p.xax(5, 25, 120)
p.yax(0,2000)
p.defaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zlike", "l_pt[0]", "zlike_lpt0")
p.labels(x="Lead lepton p_{T} [GeV]", y="Entries / 5 GeV")
p.xax(5, 25, 120)
p.yax(0,1200)
p.defaultCanvas(p.name)
plots.append(p)

#p = plot.Plot1D()
#p.initialize("ttlike", "met", "ttlike_met")
#p.labels(x="MET [GeV]", y="Entries / 10 GeV")
#p.xax(10,0.40,150.0)
#p.yax(0,40)
#p.defaultCanvas(p.name)
#plots.append(p)

