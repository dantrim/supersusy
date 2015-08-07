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
mcfile = scratchdir + "sigOpt_mc15_noPRW.root"
backgrounds = []

#### MC

# ttbar
ttbar = background.Background("ttbar", "t#bar{t}")
ttbar.marker = 24
ttbar.set_debug()
ttbar.set_file(mcfile)
ttbar.scale_factor = 1.0
ttbar.set_color(r.TColor.GetColor("#FC0D1B"))
ttbar.set_treename("TTbar_CENTRAL")
ttbar.set_merged_tree(ttbar.treename)
backgrounds.append(ttbar)

# ww
ww = background.Background("ww", "WW")
ww.marker = 26
ww.set_debug()
ww.set_file(mcfile)
ww.scale_factor = 1.0
ww.set_color(r.TColor.GetColor("#41C1FC"))
ww.set_treename("WW_CENTRAL")
ww.set_merged_tree(ww.treename)
backgrounds.append(ww)

# bwn (250, 160)
bwn250 = background.Background("bwn_250_160", "(250, 160)")
bwn250.marker = 20
bwn250.set_debug()
bwn250.set_file(mcfile)
bwn250.scale_factor = 1.0
bwn250.set_color(r.kBlue)
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
reg.simplename = "wwLoose"
reg.displayname = "WW loose"
reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1] >20"
regions.append(reg)


#############################################
# Set up the plots
#############################################

plots = []

##
#### wwLoose
##

samples = ['ttbar', 'ww', 'bwn_250_160']
for samp in samples :

    #### DPB vs cosThetaB
    p = plot.Plot2D()
    p.initialize("wwLoose", "DPB", "abs(cosThetaB)", "wwLoose_DPB_cosThetaB_%s_2d"%samp)
    p.labels(x="#Delta#phi_{#beta}^{R}", y="|cos#theta_{b}|")
    p.set_sample("%s"%samp)
    p.xax(0.032,0,3.2)
    p.yax(0.01,0,1.0)
    p.defaultCanvas()
    plots.append(p)

    #### cosThetaB vs cosThetaLL
    p = plot.Plot2D()
    p.initialize("wwLoose", "cosThetaB", "cosThetaLL", "wwLoose_cosThetaB_cosThetaLL_%s_2d"%samp)
    p.labels(x="cos#theta_{ll}", y="cos#theta_{b}")
    p.set_sample(samp)
    p.xax(0.1, -1, 1)
    p.yax(0.1, -1, 1)
    p.defaultCanvas()
    plots.append(p)

    #### R1 vs meff
    p = plot.Plot2D()
    p.initialize("wwLoose", "R1", "meff", "wwLoose_R1_meff_%s_2d"%samp)
    p.labels(x="R_{1}", y="m_{eff} [GeV]")
    p.set_sample(samp)
    p.xax(0.01, 0, 1)
    p.yax(5, 0, 1500)
    p.defaultCanvas()
    plots.append(p)

    #### R2 vs meff
    p = plot.Plot2D()
    p.initialize("wwLoose", "R2", "meff", "wwLoose_R2_meff_%s_2d"%samp)
    p.labels(x="R_{2}", y="m_{eff} [GeV]")
    p.set_sample(samp)
    p.xax(0.01, 0, 1)
    p.yax(5, 0, 1500)
    p.defaultCanvas()
    plots.append(p)

    #### cosThetaRp1 vs cosThetaB
    p = plot.Plot2D()
    p.initialize("wwLoose", "cosThetaRp1", "cosThetaB", "wwLoose_cosThetaRp1_cosThetaB_%s_2d"%samp)
    p.labels(x="cos#theta_{R+1}", y="cos#theta_{b}")
    p.set_sample(samp)
    p.xax(0.01, 0, 1)
    p.yax(0.01, 0, 1)
    p.defaultCanvas()
    plots.append(p)

    #### R1 vs R2
    p = plot.Plot2D()
    p.initialize("wwLoose", "R1", "R2", "wwLoose_R1_R2_%s_2d"%samp)
    p.labels(x="R_{1}", y="R_{2}")
    p.set_sample(samp)
    p.xax(0.01, 0, 1)
    p.yax(0.01, 0, 1)
    p.defaultCanvas()
    plots.append(p)

    #### pBll vs pTll
    p = plot.Plot2D()
    p.initialize("wwLoose", "pBll", "pTll", "wwLoose_pBll_pTll_%s_2d"%samp)
    p.labels(x="p_{T}^{ll} [GeV]", y="p_{b}^{ll} [GeV]")
    p.set_sample(samp)
    p.xax(5, 0, 500)
    p.yax(5, 0, 500)
    p.defaultCanvas()
    plots.append(p)

    #### pBll vs meff
    p = plot.Plot2D()
    p.initialize("wwLoose", "pBll", "meff", "wwLoose_pBll_meff_%s_2d"%samp)
    p.labels(x="p_{b}^{ll} [GeV]", y = "m_{eff} [GeV]")
    p.set_sample(samp)
    p.xax(5, 0, 500)
    p.yax(10, 0, 1000)
    p.defaultCanvas()
    plots.append(p)

    #### DPB vs dphi_met_pbll
    p = plot.Plot2D()
    p.initialize("wwLoose", "DPB", "dphi_met_pbll", "wwLoose_DBP_dphi_met_pbll_%s_2d"%samp)
    p.labels(x="#Delta#phi_{#beta}^{R}", y="|#Delta#phi(#slash{E}_{T},p_{b}^{ll})|")
    p.set_sample(samp)
    p.xax(0.05,0,3.2)
    p.yax(0.05,0,3.2)
    p.defaultCanvas()
    plots.append(p)

    #### shatr vs R2
    p = plot.Plot2D()
    p.initialize("wwLoose", "shatr", "R2", "wwLoose_shatr_R2_%s_2d"%samp)
    p.labels(x="#sqrt{#hat{s}}_{R} [GeV]", y="R_{2}")
    p.set_sample(samp)
    p.xax(20,0,500)
    p.yax(0.05,0,1)
    p.defaultCanvas()
    plots.append(p)

    #### shatr vs deltax
    p = plot.Plot2D()
    p.initialize("wwLoose", "shatr", "deltaX", "wwLoose_shatr_deltaX_%s_2d"%samp)
    p.labels(x="#sqrt{#hat{s}}_{R} [GeV]", y="|x_{1}-x_{2}|")
    p.set_sample(samp)
    p.xax(20,0,500)
    p.yax(0.005,0,0.1)
    p.defaultCanvas()
    plots.append(p)


