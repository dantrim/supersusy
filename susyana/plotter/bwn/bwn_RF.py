
import sys
sys.path.append('../../../../../')
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

##
##### RestFrames variables
##

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "shat", "wwLooseSF_shat")
p.labels(x="#hat{s} (total CM mass) [GeV]", y = "")
p.xax(20,0,1000)
p.doLogY = True
p.yax(0.1,100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "RPT", "wwLooseSF_RPT")
p.labels(x="p_{T}^{CM} / m_{CM}", y = "")
p.leg_is_bottom_left = True
p.xax(0.01,0,1)
p.doLogY = True
p.yax(0.1,100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "RPZ", "wwLooseSF_RPZ")
p.labels(x="p_{z}^{CM} / m_{CM}", y = "")
p.xax(0.05,0,5)
p.doLogY = True
p.yax(0.1,100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "cosTT", "wwLooseSF_cosTT")
p.labels(x="cos#theta_{TT} (#theta_{TT}: dec. angle of TT system)", y = "")
p.xax(0.07,-1,1)
p.doLogY = True
p.yax(0.1,100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "dphiVT", "wwLooseSF_dphiVT")
p.labels(x="#Delta#phi_{vis}^{TT-axis} (bet. TT vis. decay products and TT dec. axis)", y = "")
p.xax(0.07,0,3.2)
p.doLogY = True
p.yax(0.1,100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "dphiVTT", "wwLooseSF_dphiVTT")
p.labels(x="|#Delta#phi_{vis}^{p_{TT}}|", y="")
p.xax(0.07,0,3.2)
p.doLogY = True
p.yax(0.1,100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "abs(cosT[0])", "wwLooseSF_cosTA")
p.labels(x="|cos#theta_{T}^{A}|", y = "")
p.xax(0.05,0,1)
p.doLogY = True
p.yax(0.1,100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "abs(cosT[1])", "wwLooseSF_cosTB")
p.labels(x="cos#theta_{T}^{B}", y = "")
p.xax(0.05,0,1)
p.doLogY = True
p.yax(0.1,100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "abs(cosW[0])", "wwLooseSF_cosWA")
p.labels(x="|cos#theta_{W}^{A}|", y = "")
p.xax(0.05,0,1)
p.doLogY = True
p.yax(0.1,100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "abs(cosW[1])", "wwLooseSF_cosWB")
p.labels(x="|cos#theta_{W}^{B}|", y = "")
p.xax(0.05,0,1)
p.doLogY = True
p.yax(0.1,100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "abs(dphiTW[0])", "wwLooseSF_dphiTWA")
p.labels(x="|#Delta#phi_{T-W}^{A}|", y = "")
p.xax(0.05, 0, 3.2)
p.doLogY = True
p.yax(0.1, 100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "abs(dphiTW[1])", "wwLooseSF_dphiTWB")
p.labels(x="|#Delta#phi_{T-W}^{B}|", y = "")
p.xax(0.05, 0,3.2)
p.doLogY = True
p.yax(0.1,100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "ELW", "wwLooseSF_ELW")
p.labels(x="E_{#it{l}}^{W} [GeV]", y = "")
p.xax(3, 0, 130)
p.doLogY = True
p.yax(0.1,100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "MT", "wwLooseSF_MT")
p.labels(x="m_{T} [GeV]", y = "")
p.xax(5, 0, 200)
p.doLogY = True
p.yax(0.1,100)
p.setDefaultCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.setComparison()
p.initialize("wwLooseSF", "MW", "wwLooseSF_MW")
p.labels(x="m_{W} [GeV]", y = "")
p.xax(5,0,200)
p.doLogY = True
p.yax(0.1,100)
p.setDefaultCanvas(p.name)
plots.append(p)

