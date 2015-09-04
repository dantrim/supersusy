
import sys
sys.path.append('../../../../../')
import supersusy.utils.plot as plot
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region


#############################################
# Set up the samples
#############################################
rawdir = "/gdata/atlas/dantrim/SusyAna/histoAna/run2early/n0213/mc/2lep/Raw/" 
data_rawdir = "/gdata/atlas/dantrim/SusyAna/histoAna/run2early/n0213/data/2lep/Raw/"
filelist_dir = "/gdata/atlas/dantrim/SusyAna/n0213val/Superflow/run/filelists/"
backgrounds = []

#### MC
# Zjets
zjets = background.Background("zjets", "Z+jets (Powheg)")
zjets.set_debug()
zjets.scale_factor = 0.73
zjets.set_color(r.TColor.GetColor("#82DE68"))
zjets.set_treename("Zjets_powheg")
#zjets.set_treename("Zjets_sherpa")
zjets.set_chain_from_list(filelist_dir + "zjets_powheg_n0213.txt", rawdir)
#zjets.set_chain_from_list(filelist_dir + "zjets_sherpa_n0213.txt", rawdir)
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
# Set up the regions
#############################################
regions = []

reg = region.Region()
reg.simplename = "pre_zbalance_1j0b_mu"
reg.displayname = "Pre Z-balance (1j0b) (#mu)"
reg.tcut = "nLeptons==2 && nMuons==2 && nJets==1 && nSJets==1 && nBJets==0 && l_pt[0]>25 && l_pt[1]>20 && mll>60"
regions.append(reg)

reg = region.Region()
reg.simplename = "zbalance_1j0b_mu"
reg.displayname = "Z-balance (1j0b) (#mu)"
reg.tcut = "nLeptons==2 && nMuons==2 && nJets==1 && nSJets==1 && nBJets==0 && l_pt[0]>25 && l_pt[1]>20 && abs(1-pT_balance)<0.2 && abs(phi_balance)>2.5 && mll>60"
regions.append(reg)



#############################################
# Set up the plots
#############################################

plots = []

prezbal = "pre_zbalance_1j0b_mu"

p = plot.Plot1D()
p.initialize(prezbal, "pTll", prezbal + "_pTll")
p.labels(x="p_{T}^{ll} [GeV]", y = "Entries / 5 GeV")
p.xax(5, 0, 500)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize(prezbal, "dphi_ll", prezbal + "_dphi_ll")
p.labels(x="#Delta#phi_{ll}", y = "Entries")
p.xax(0.2, -3.2, 3.2)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize(prezbal, "deta_ll", prezbal + "_deta_ll")
p.labels(x="#Delta#eta_{ll}", y = "Entries")
p.xax(0.2, -3, 3)
p.yax(0.1, 100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize(prezbal, "abs(phi_balance)", prezbal + "_phi_balance")
p.labels(x="|#Delta#phi(Z,jet)|", y = "Entries")
p.xax(0.2, 0, 3.2)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize(prezbal, "pT_balance", prezbal + "_pT_balance")
p.labels(x="p_{T}^{ref} / p_{T}^{Z}", y = "Entries / 0.2")
p.xax(0.2, 0, 10)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize(prezbal, "j_jvt[0]", prezbal + "_jvt0")
p.labels(x="Jet JVT", y = "Entries")
p.xax(0.1, 0, 2)
p.yax(0.1, 100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize(prezbal, "j_pt[0]", prezbal + "_jpt0")
p.labels(x="Jet p_{T} [GeV]", y = "Entries / 10 GeV")
p.xax(10, 0, 500)
p.yax(0.1, 100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize(prezbal, "met", prezbal + "_met")
p.labels(x="TST #slash{E}_{T} [GeV]", y = "Entries / 10 GeV")
p.xax(10, 0, 200)
p.yax(0.1, 100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize(prezbal, "dphi_met_jetTerm", prezbal + "_dphi_met_jetTerm")
p.labels(x="#Delta#phi(#slash{E}_{T}, jet-term)", y = "Entries")
p.xax(0.2,-3.2, 3.2)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize(prezbal, "dphi_met_softTerm", prezbal + "_dphi_met_softTerm")
p.labels(x="#Delta#phi(#slash{E}_{T}, soft-term)", y = "Entries")
p.xax(0.2, -3.2, 3.2)
p.yax(0.1, 100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize(prezbal, "dphi_met_muonTerm", prezbal + "_dphi_met_muonTerm")
p.labels(x="#Delta#phi(#slash{E}_{T}, muon-term)", y = "Entries")
p.xax(0.2, -3.2, 3.2)
p.yax(0.1, 100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize(prezbal, "dphi_met_j", prezbal + "_dphi_met_j")
p.labels(x="#Delta#phi(#slash{E}_{T}, jet)", y = "Entries")
p.xax(0.2, -3.2, 3.2)
p.yax(0.1, 100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize(prezbal, "metX", prezbal + "_metX")
p.labels(x="#slash{E}_{T}^{x} [GeV]", y = "Entries / 5 GeV")
p.xax(5, -100, 100)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize(prezbal, "metY", prezbal + "_metY")
p.labels(x="#slash{E}_{T}^{y} [GeV]", y = "Entries / 5 GeV")
p.xax(5, -100, 100)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)
