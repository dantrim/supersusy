
import sys
sys.path.append('../../../..')
import supersusy.utils.plot as plot
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region


#############################################
# Set up the samples
#############################################
scratchdir = "/scratch/dantrim/n0209/wwlike/"
#datafile = scratchdir + "data15_13TeV.root"
datafile = scratchdir + "data15_perC_13TeV.root"
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

# zee
zee = background.Background("zee", "Zee")
zee.set_debug()
zee.set_file(mcfile)
zee.scale_factor = 7.5
zee.set_color(r.TColor.GetColor("#A7E851"))
zee.set_treename("Zee_CENTRAL")
zee.set_merged_tree(zee.treename)
backgrounds.append(zee)

# ztt
ztt = background.Background("ztt", "Z#tau#tau")
ztt.set_debug()
ztt.set_file(mcfile)
ztt.scale_factor = 7.5
ztt.set_color(r.TColor.GetColor("#91D2FC"))
ztt.set_treename("Ztt_CENTRAL")
ztt.set_merged_tree(ztt.treename)
backgrounds.append(ztt)

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

# singletop
stop = background.Background("st", "ST")
stop.set_debug()
stop.set_file(mcfile)
stop.scale_factor = 7.5
stop.set_color(r.TColor.GetColor("#DE080C"))
stop.set_treename("ST_CENTRAL")
stop.set_merged_tree(stop.treename)
backgrounds.append(stop)

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

# ww
ww = background.Background("ww", "WW")
ww.set_debug()
ww.set_file(mcfile)
ww.scale_factor = 7.5
ww.set_color(r.TColor.GetColor("#315E88"))
ww.set_treename("WW_CENTRAL")
ww.set_merged_tree(ww.treename)
backgrounds.append(ww)

# wz
wz = background.Background("wz", "WZ")
wz.set_debug()
wz.set_file(mcfile)
wz.scale_factor = 7.5
wz.set_color(r.TColor.GetColor("#F9F549"))
wz.set_treename("WZ_CENTRAL")
wz.set_merged_tree(wz.treename)
backgrounds.append(wz)

# zz
zz = background.Background("zz", "ZZ")
zz.set_debug()
zz.set_file(mcfile)
zz.scale_factor = 7.5
zz.set_color(r.TColor.GetColor("#FFEF53"))
zz.set_treename("ZZ_CENTRAL")
zz.set_merged_tree(zz.treename)
backgrounds.append(zz)



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
reg.simplename = "zpeak_mm0j"
reg.displayname = "Z#mu#mu 0-j"
reg.tcut = "nLeptons==2 && nMuons==2 && nSJets==0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<1 && abs(mll-91.2)<20 && abs(l_d0sigBSCorr[0])<3 && abs(l_d0sigBSCorr[1])<3"
regions.append(reg)

reg = region.Region()
reg.simplename = "zpeak_mmj"
reg.displayname = "Z#mu#mu >=0j"
reg.tcut = "nLeptons==2 && nMuons==2 && nSJets>=0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<0 && abs(mll-91.2)<20 && abs(l_d0sigBSCorr[0])<3 && abs(l_d0sigBSCorr[1])<3"
regions.append(reg)



#############################################
# Set up the plots
#############################################

plots = []

#### zpeak_mmj

p = plot.Plot1D()
p.initialize("zpeak_mmj", "mll", "zpeak_mmj_mll")
p.labels(x="m_{#mu#mu} [GeV]", y="Entries / 2 GeV")
p.xax(2,70,110)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "pTll", "zpeak_mmj_pTll")
p.labels(x="Dilepton p_{T} [GeV]", y="Entries / 5 GeV")
p.xax(5,0,300)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "dphi_ll", "zpeak_mmj_dphill")
p.labels(x="#delta#phi_{ll}", y = "Entries / 0.2")
p.xax(0.2, -3.2,3.2)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "l_pt[0]", "zpeak_mmj_lpt0")
p.labels(x="Lead lepton p_{T} [GeV]", y="Entries / 2 GeV")
p.xax(2, 25, 90)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "l_pt[1]", "zpeak_mmj_lpt1")
p.labels(x="Sub-lead lepton p_{T} [GeV]", y="Entries / 3 GeV")
p.xax(3, 25, 80)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "l_eta[0]", "zpeak_mmj_leta0")
p.labels(x="Lead lepton #eta", y="Entries / 0.2")
p.xax(0.2,-3, 3)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "l_eta[1]", "zpeak_mmj_leta1")
p.labels(x="Sub-lead lepton #eta", y="Entries / 0.2")
p.xax(0.2, -3, 3)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "nSJets", "zpeak_mmj_nSJets")
p.labels(x="Number of jets", y = "Entries / 1")
p.xax(1,0,10)
p.yax(0.1,100000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "sj_pt[0]", "zpeak_mmj_sjpt0")
p.labels(x="Lead jet p_{T} [GeV]", y = "Entries / 15 GeV")
p.xax(15,0,300)
p.doLogY=True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "sj_eta[0]", "zpeak_mmj_sjeta0")
p.labels(x="Lead jet #eta", y = "Entries / 0.2")
p.xax(0.2,-3,3)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "sj_jvt[0]", "zpeak_mmj_sjvt0")
p.labels(x="Lead jet JVT", y = "Entries / 0.05")
p.xax(0.05, -0.5, 1)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "sj_pt[1]", "zpeak_mmj_sjpt1")
p.labels(x="Sub-lead jet p_{T} [GeV]", y = "Entries / 15 GeV")
p.xax(15,0,300)
p.doLogY=True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "sj_eta[1]", "zpeak_mmj_sjeta1")
p.labels(x="Sub-lead jet #eta", y = "Entries / 0.2")
p.xax(0.2,-3,3)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "sj_jvt[1]", "zpeak_mmj_sjvt1")
p.labels(x="Sub-lead jet JVT", y = "Entries / 0.05")
p.xax(0.05, -0.5, 1)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)


p = plot.Plot1D()
p.initialize("zpeak_mmj", "met", "zpeak_mmj_met")
p.labels(x="TST #slash{E}_{T} [GeV]", y="Entries / 3 GeV")
p.xax(3,0,100)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "sumet", "zpeak_mmj_sumet")
p.labels(x="#sum E_{T} [GeV]", y = "Entires / 40 GeV")
p.xax(40,40,800)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "refJet_et", "zpeak_mmj_refJet_et")
p.labels(x="TST #slash{E}_{T} jet term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,180)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "refMuo_et", "zpeak_mmj_refMuo_et")
p.labels(x="TST #slash{E}_{T} muon term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,180)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "softTerm_et", "zpeak_mmj_softTerm_et")
p.labels(x="TST #slash{E}_{T} soft term [GeV]", y="Entries / 3 GeV")
p.xax(3,0,60)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "refMuo_sumet", "zpeak_mmj_refMuo_sumet")
p.labels(x="#sum E_{T} muon-term [GeV]", y="Entries / 5 GeV")
p.xax(5, 0, 500)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "refJet_sumet", "zpeak_mmj_refJet_sumet")
p.labels(x="#sum E_{T} jet term [GeV]", y="Entries / 5 GeV")
p.xax(5,0,500)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "softTerm_sumet", "zpeak_mmj_softTerm_sumet")
p.labels(x="#sum E_{T} soft-term [GeV]", y="Entries / 5 GeV")
p.xax(5,0, 100)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "l_d0sig[0]", "zpeak_mmj_d0sig0")
p.labels(x="Lead lepton d0sig", y="Entries")
p.xax(0.5,-10,10)
p.yax(0.1,1000000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "l_d0sigBSCorr[0]", "zpeak_mmj_d0sigBSCorr0")
p.labels(x="Lead lepton d0sig (BSCorr)", y="Entries")
p.xax(0.5,-10,10)
p.yax(0.1,1000000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "l_d0[0]", "zpeak_mmj_d00")
p.labels(x="Lead lepton d0 [mm]", y="Entries")
p.xax(0.01,-0.2,0.2)
p.yax(0.1,1000000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "meff", "zpeak_mmj_meff")
p.labels(x="m_{eff} [GeV]", y = "Entries / 40 GeV")
p.xax(40, 40, 800)
p.yax(0.1,1000000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "l_ptvarcone20[0]", "zpeak_mmj_ptvarcone200")
p.labels(x="Lead lepton ptvarcone20 [GeV]", y = "Entries / 0.2 GeV")
p.xax(0.2, 0, 6)
p.doLogY = True
p.yax(0.1,100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "l_ptvarcone20[1]", "zpeak_mmj_ptvarcone201")
p.labels(x="Sub-lead lepton ptvarcone20 [GeV]", y = "Entries / 0.2 GeV")
p.xax(0.2, 0, 6)
p.doLogY = True
p.yax(0.1, 100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "l_etconetopo20[0]", "zpeak_mmj_etconetopo200")
p.labels(x="Lead lepton etconetopo20 [GeV]", y = "Entries / 0.2 GeV")
p.xax(0.2, 0, 6)
p.doLogY = True
p.yax(0.1, 100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "l_etconetopo20[1]", "zpeak_mmj_etconetopo201")
p.labels(x="Sub-lead lepton etconetopo20 [GeV]", y = "Entries / 0.2 GeV")
p.xax(0.2, 0, 6)
p.doLogY = True
p.yax(0.1, 100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "l_etconetopo30[0]", "zpeak_mmj_etconetopo300")
p.labels(x="Lead lepton etconetopo30 [GeV]", y = "Entries / 0.2 GeV")
p.xax(0.2, 0, 6)
p.doLogY = True
p.yax(0.1, 100000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mmj", "l_etconetopo30[1]", "zpeak_mmj_etconetopo301")
p.labels(x="Sub-lead lepton etconetopo30 [GeV]", y = "Entries / 0.2 GeV")
p.xax(0.2, 0, 6)
p.doLogY = True
p.yax(0.1, 100000)
p.setRatioCanvas(p.name)
plots.append(p)

