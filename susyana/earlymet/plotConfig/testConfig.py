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
zjets.set_color = r.kRed
zjets.set_treename("Zjets_CENTRAL")
zjets.set_merged_tree(zjets.treename)
backgrounds.append(zjets)

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
reg.tcut = "nLeptons==2 && nJets>=0 && l_pt[0]>25 && l_pt[1]>25"
regions.append(reg)


#############################################
# Set up the plots
#############################################

plots = []
# test plot
p = plot.Plot1D()
p.initialize(variable="l_pt[0]", region="sr1a", name = "sr1a_lpt0")
p.labels(x="Lead lepton p_{T} [GeV]", y="Entries / 5 GeV")
p.xax(5, 25, 150)
p.yax(0,500)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("sr1c", "met", "sr1c_met")
p.labels(x="MET [GeV]", y="Entries / 10 GeV")
p.xax(10,0,500)
p.yax(0,500)
p.defaultCanvas(p.name)
plots.append(p)

