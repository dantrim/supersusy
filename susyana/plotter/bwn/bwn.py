import os
import sys
sys.path.append(os.environ['SUSYDIR'])
#sys.path.append('../../../../../')
import supersusy.utils.plot as plot
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region


#############################################
# Set up the samples
#############################################
scratchdir = "/scratch/dantrim/n0211/"
#datafile = scratchdir + "data15_13TeV.root"
datafile = scratchdir + "data15_13TeV.root"
mcfile = scratchdir + "sigOpt_mc15_noPRW_RF.root"
backgrounds = []

#### MC

# ttbar
ttbar = background.Background("ttbar", "t#bar{t}")
ttbar.set_debug()
ttbar.set_file(mcfile)
ttbar.scale_factor = 1.0
ttbar.set_color(r.TColor.GetColor("#FC0D1B"))
#ttbar.set_color(r.TColor.GetColor("#E4817D"))
ttbar.set_treename("TTbar_CENTRAL")
ttbar.set_merged_tree(ttbar.treename)
backgrounds.append(ttbar)

# ww
ww = background.Background("ww", "WW")
ww.set_debug()
ww.set_file(mcfile)
ww.scale_factor = 1.0
#ww.set_color(r.TColor.GetColor("#55BDE6"))
ww.set_color(r.TColor.GetColor("#41C1FC"))
ww.set_treename("WW_CENTRAL")
ww.set_merged_tree(ww.treename)
backgrounds.append(ww)

# bwn (250, 160)
bwn250 = background.Background("bwn_250_160", "(250, 160)")
bwn250.set_debug()
bwn250.set_file(mcfile)
bwn250.scale_factor = 1.0
bwn250.set_color(r.kRed)
bwn250.set_treename("bwn_250_160_CENTRAL")
bwn250.setLineStyle(2)
bwn250.set_merged_tree(bwn250.treename)
backgrounds.append(bwn250)

# bwn (300, 180)
bwn300 = background.Background("bwn_300_180", "(300, 180)")
bwn300.set_debug()
bwn300.set_file(mcfile)
bwn300.scale_factor = 1.0
bwn300.set_color(r.kBlue)
bwn300.set_treename("bwn_300_180_CENTRAL")
bwn300.setLineStyle(2)
bwn300.set_merged_tree(bwn300.treename)
backgrounds.append(bwn300)

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
reg.simplename = "wwLooseSF"
reg.displayname = "WW loose"
#reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1] >20"
reg.tcut = "nLeptons==2 && (nElectrons==2 || nMuons==2) && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1] > 20"
regions.append(reg)


#############################################
# Set up the plots
#############################################

plots = []

#### wwLooseSF

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "mt2", "wwLooseSF_mt2")
p.labels(x="m_{T2} [GeV]", y = "Entries / 5 GeV")
p.xax(5, 0, 200)
p.doLogY = True
p.yax(0.1,100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "meff", "wwLooseSF_meff")
p.labels(x="m_{eff} [GeV]", y = "")
p.xax(5, 0, 1500)
p.doLogY = True
p.yax(0.1,100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "R1", "wwLooseSF_R1")
p.labels(x="R_{1}", y = "")
p.xax(0.01, 0, 1)
p.doLogY = True
p.yax(0.1,100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "R2", "wwLooseSF_R2")
p.leg_is_bottom_left = True
p.labels(x="R_{2}", y = "")
p.xax(0.01, 0, 1)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "deltaX", "wwLooseSF_deltaX")
p.labels(x="|x_{1}-x_{2}|", y = "")
p.xax(0.01, 0, 0.2)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "cosThetaB", "wwLooseSF_cosThetaB")
p.labels(x="cos#theta_{b}", y = "")
p.xax(0.05, -1, 1)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "cosThetaLL", "wwLooseSF_cosThetaLL")
p.leg_is_bottom_right = True
p.labels(x="cos#theta_{ll}", y = "")
p.xax(0.05, -1, 1)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "pBll", "wwLooseSF_pBll")
p.labels(x="p_{b}^{ll} [GeV]", y = "")
p.xax(5, 0, 500)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "dphi_met_pbll", "wwLooseSF_dphi_met_pbll")
p.labels(x="#Delta#phi(#slash{E}_{T}, p_{b}^{ll})", y = "")
p.xax(0.05, 0, 3.2)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "MDR", "wwLooseSF_MDR")
p.labels(x="M_{#Delta}^{R} [GeV]", y = "")
p.xax(5, 0, 200)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "abs(cosThetaRp1)", "wwLooseSF_cosThetaRp1")
p.labels(x="|cos#theta_{R+1}|", y = "")
p.xax(0.05, 0, 1)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "DPB", "wwLooseSF_DPB")
p.leg_is_left = True
p.labels(x="|#Delta#phi_{#beta}^{R}|", y = "")
p.xax(0.05, 0, 3.2)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "shatr", "wwLooseSF_shatr")
p.labels(x="#sqrt{#hat{s}_{R}} [GeV]", y = "")
p.xax(5, 0, 1200)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)


p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "pTll", "wwLooseSF_pTll")
p.labels(x="p_{T}^{ll} [GeV]", y = "")
p.xax(5, 0, 400)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "l_pt[0]", "wwLooseSF_lpt0")
p.labels(x="Lead lepton p_{T} [GeV]", y = "")
p.xax(5, 20, 200)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "l_pt[1]", "wwLooseSF_lpt1")
p.labels(x="Sub-lead lepton p_{T} [GeV]", y = "")
p.xax(5, 20, 200)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "nBJets", "wwLooseSF_nBJets")
p.labels(x="Number of b-jets", y="")
p.xax(1,0,10)
p.doLogY = True
p.yax(0.1,100)
p.setDefaultCanvas(p.name)
plots.append(p)
