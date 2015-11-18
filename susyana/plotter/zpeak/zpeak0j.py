
import sys
sys.path.append('../../../../../')
import supersusy.utils.plot as plot
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region


#############################################
# Set up the samples
#############################################
rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0216/zee/mc/raw/"
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0216/zee/data/raw/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0216val/filelists/"
backgrounds = []

#### MC
# Zjets
zjets = background.Background("zjets", "Z #rightarrow ee (Sherpa)")
zjets.set_debug()
zjets.scale_factor = 1
zjets.set_color(r.TColor.GetColor("#82DE68"))
#zjets.set_treename("Zjets_powheg")
zjets.set_treename("Zjets_sherpa")
zjets.set_chain_from_list_CONDOR(filelist_dir + "mc/zee_sherpa/", rawdir)
#zjets.set_chain_from_list_CONDOR(filelist_dir + "zjets_sherpa_n0213.txt", rawdir)
backgrounds.append(zjets)

#ttbar = background.Background("ttbar", "TTbar")
#ttbar.set_debug()
#ttbar.scale_factor = 1.0
#ttbar.set_color(r.TColor.GetColor("#E67067"))
#ttbar.set_treename("ttbar_powheg")
#ttbar.set_chain_from_list(filelist_dir + "ttbar_powheg_n0213.txt", rawdir)
#backgrounds.append(ttbar)
#
## singletop
#stop = background.Background("st", "ST")
#stop.set_debug()
#stop.scale_factor = 1.0
#stop.set_color(r.TColor.GetColor("#DE080C"))
#stop.set_treename("ST")
#stop.set_chain_from_list(filelist_dir + "singletop_powheg_n0213.txt", rawdir)
#backgrounds.append(stop)
#
## wjets
#wjets = background.Background("wjets", "W+jets (Sherpa)")
#wjets.set_debug()
#wjets.scale_factor = 1.0
#wjets.set_color(r.TColor.GetColor("#5E9AD6"))
#wjets.set_treename("Wjets_sherpa")
#wjets.set_chain_from_list(filelist_dir + "wjets_sherpa_n0213.txt", rawdir)
#backgrounds.append(wjets)
#
## ww
#ww = background.Background("ww", "WW (Powheg)")
#ww.set_debug()
#ww.scale_factor = 1.0
#ww.set_color(r.TColor.GetColor("#315E88"))
#ww.set_treename("WW_powheg")
#ww.set_chain_from_list(filelist_dir + "ww_powheg_n0213.txt", rawdir)
#backgrounds.append(ww)
#
## wz
#wz = background.Background("wz", "WZ (Powheg)")
#wz.set_debug()
#wz.scale_factor = 1.0
#wz.set_color(r.TColor.GetColor("#F9F549"))
#wz.set_treename("WZ_powheg")
#wz.set_chain_from_list(filelist_dir + "wz_powheg_n0213.txt", rawdir)
#backgrounds.append(wz)
#
## zz
#zz = background.Background("zz", "ZZ (Powheg)")
#zz.set_debug()
#zz.scale_factor = 1.0
#zz.set_color(r.TColor.GetColor("#FFEF53"))
#zz.set_treename("ZZ_powheg")
#zz.set_chain_from_list(filelist_dir + "zz_powheg_n0213.txt", rawdir)
#backgrounds.append(zz)

#### DATA
data = background.Data()
data.set_color(r.kBlack)
data.set_treename("Data")
data.set_chain_from_list_CONDOR(filelist_dir + "data/p2425/", data_rawdir)


#############################################
# Set up the regions
#############################################
regions = []
reg = region.Region()
reg.simplename = "zpeak_eej"
reg.displayname = "Z #rightarrow ee (nJ>=0 nB=0)"
reg.tcut = "nLeptons==2 && nElectrons==2 && nSJets>=0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<1 && abs(mll-91.2)<20"
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

#### zpeak_eej

p = plot.Plot1D()
p.initialize("zpeak_eej", "met", "zpeak_eej_met")
p.labels(x="TST #slash{E}_{T} [GeV]", y="Entries / 10 GeV")
p.xax(10,0,200)
p.yax(0.1,10000000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_eej", "mll", "zpeak_eej_mll")
p.labels(x="m_{ee} [GeV]", y="Entries / 2 GeV")
p.xax(2,70,110)
p.yax(0.1,10000000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_eej", "pTll", "zpeak_eej_pTll")
p.labels(x="Dilepton p_{T} [GeV]", y="Entries / 10 GeV")
p.xax(10,0,300)
p.doLogY = True
p.yax(0.1,10000000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_eej", "dphi_ll", "zpeak_eej_dphill")
p.labels(x="#Delta#phi_{ll}", y = "Entries / 0.2")
p.xax(0.2, -3.2,3.2)
p.doLogY = True
p.yax(0.1,10000000)
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_eej", "l_pt[0]", "zpeak_eej_lpt0")
p.labels(x="Lead lepton p_{T} [GeV]", y="Entries / 15 GeV")
p.xax(15, 25, 320)
p.yax(0.1,10000000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_eej", "l_pt[1]", "zpeak_eej_lpt1")
p.labels(x="Sub-lead lepton p_{T} [GeV]", y="Entries / 10 GeV")
p.xax(10, 25, 250)
p.yax(0.1,10000000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_eej", "l_eta[0]", "zpeak_eej_leta0")
p.labels(x="Lead lepton #eta", y="Entries / 0.2")
p.xax(0.2,-3, 3)
p.yax(0.1,10000000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_eej", "l_eta[1]", "zpeak_eej_leta1")
p.labels(x="Sub-lead lepton #eta", y="Entries / 0.2")
p.xax(0.2, -3, 3)
p.yax(0.1,10000000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)



p = plot.Plot1D()
p.initialize("zpeak_eej", "sumet", "zpeak_eej_sumet")
p.labels(x="#sum E_{T} [GeV]", y = "Entires / 10 GeV")
p.xax(10,40,400)
p.yax(0.1,10000)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

#p = plot.Plot1D()
#p.initialize("zpeak_eej", "refJet_et", "zpeak_eej_refJet_et")
#p.labels(x="TST #slash{E}_{T} jet term [GeV]", y="Entries / 5 GeV")
#p.xax(5,0,180)
#p.yax(0.1,10000)
#p.doLogY = True
#p.setRatioCanvas(p.name)
#plots.append(p)
#
#p = plot.Plot1D()
#p.initialize("zpeak_eej", "refMuo_et", "zpeak_eej_refMuo_et")
#p.labels(x="TST #slash{E}_{T} muon term [GeV]", y="Entries / 5 GeV")
#p.xax(5,0,180)
#p.yax(0.1,10000)
#p.doLogY = True
#p.setRatioCanvas(p.name)
#plots.append(p)
#
#p = plot.Plot1D()
#p.initialize("zpeak_eej", "softTerm_et", "zpeak_eej_softTerm_et")
#p.labels(x="TST #slash{E}_{T} soft term [GeV]", y="Entries / 3 GeV")
#p.xax(3,0,60)
#p.yax(0.1,10000)
#p.doLogY = True
#p.setRatioCanvas(p.name)
#plots.append(p)
#
#p = plot.Plot1D()
#p.initialize("zpeak_eej", "refMuo_sumet", "zpeak_eej_refMuo_sumet")
#p.labels(x="#sum E_{T} muon-term [GeV]", y="Entries / 2 GeV")
#p.xax(2, 30, 200)
#p.doLogY = True
#p.yax(0.1,10000000)
#p.setRatioCanvas(p.name)
#plots.append(p)
#
#p = plot.Plot1D()
#p.initialize("zpeak_eej", "refJet_sumet", "zpeak_eej_refJet_sumet")
#p.labels(x="#sum E_{T} jet term [GeV]", y="Entries / 10 GeV")
#p.xax(10,20,200)
#p.doLogY = True
#p.yax(0.1,10000000)
#p.setRatioCanvas(p.name)
#plots.append(p)
#
#p = plot.Plot1D()
#p.initialize("zpeak_eej", "softTerm_sumet", "zpeak_eej_softTerm_sumet")
#p.labels(x="#sum E_{T} soft-term [GeV]", y="Entries / 10 GeV")
#p.xax(10,0, 200)
#p.doLogY = True
#p.yax(0.1,10000000)
#p.setRatioCanvas(p.name)
#plots.append(p)
#
#p = plot.Plot1D()
#p.initialize("zpeak_eej", "l_d0sig[0]", "zpeak_eej_d0sig0")
#p.labels(x="Lead lepton d0sig", y="Entries")
#p.xax(0.5,-10,10)
#p.yax(0.1,100000000)
#p.doLogY = True
#p.setRatioCanvas(p.name)
#plots.append(p)
#
#p = plot.Plot1D()
#p.initialize("zpeak_eej", "l_d0sigBSCorr[0]", "zpeak_eej_d0sigBSCorr0")
#p.labels(x="Lead lepton d0sig (BSCorr)", y="Entries")
#p.xax(0.5,-10,10)
#p.yax(0.1,100000000)
#p.doLogY = True
#p.setRatioCanvas(p.name)
#plots.append(p)
#
#p = plot.Plot1D()
#p.initialize("zpeak_eej", "l_d0[0]", "zpeak_eej_d00")
#p.labels(x="Lead lepton d0 [mm]", y="Entries")
#p.xax(0.01,-0.2,0.2)
#p.yax(0.1,100000000)
#p.doLogY = True
#p.setRatioCanvas(p.name)
#plots.append(p)
#
#p = plot.Plot1D()
#p.initialize("zpeak_eej", "meff", "zpeak_eej_meff")
#p.labels(x="m_{eff} [GeV]", y = "Entries / 10 GeV")
#p.xax(10, 0, 300)
#p.yax(0.1,100000000)
#p.doLogY = True
#p.setRatioCanvas(p.name)
#plots.append(p)
#
#p = plot.Plot1D()
#p.initialize("zpeak_eej", "l_ptvarcone20[0]", "zpeak_eej_ptvarcone200")
#p.labels(x="Lead lepton ptvarcone20 [GeV]", y = "Entries / 0.2 GeV")
#p.xax(0.2, 0, 6)
#p.doLogY = True
#p.yax(0.1,10000000)
#p.setRatioCanvas(p.name)
#plots.append(p)
#
#p = plot.Plot1D()
#p.initialize("zpeak_eej", "l_ptvarcone20[1]", "zpeak_eej_ptvarcone201")
#p.labels(x="Sub-lead lepton ptvarcone20 [GeV]", y = "Entries / 0.2 GeV")
#p.xax(0.2, 0, 6)
#p.doLogY = True
#p.yax(0.1, 100000)
#p.setRatioCanvas(p.name)
#plots.append(p)
#
#p = plot.Plot1D()
#p.initialize("zpeak_eej", "l_etconetopo20[0]", "zpeak_eej_etconetopo200")
#p.labels(x="Lead lepton etconetopo20 [GeV]", y = "Entries / 0.2 GeV")
#p.xax(0.2, 0, 6)
#p.doLogY = True
#p.yax(0.1, 100000)
#p.setRatioCanvas(p.name)
#plots.append(p)
#
#p = plot.Plot1D()
#p.initialize("zpeak_eej", "l_etconetopo20[1]", "zpeak_eej_etconetopo201")
#p.labels(x="Sub-lead lepton etconetopo20 [GeV]", y = "Entries / 0.2 GeV")
#p.xax(0.2, 0, 6)
#p.doLogY = True
#p.yax(0.1, 100000)
#p.setRatioCanvas(p.name)
#plots.append(p)
#
#p = plot.Plot1D()
#p.initialize("zpeak_eej", "l_etconetopo30[0]", "zpeak_eej_etconetopo300")
#p.labels(x="Lead lepton etconetopo30 [GeV]", y = "Entries / 0.2 GeV")
#p.xax(0.2, 0, 6)
#p.doLogY = True
#p.yax(0.1, 100000)
#p.setRatioCanvas(p.name)
#plots.append(p)
#
#p = plot.Plot1D()
#p.initialize("zpeak_eej", "l_etconetopo30[1]", "zpeak_eej_etconetopo301")
#p.labels(x="Sub-lead lepton etconetopo30 [GeV]", y = "Entries / 0.2 GeV")
#p.xax(0.2, 0, 6)
#p.doLogY = True
#p.yax(0.1, 100000)
#p.setRatioCanvas(p.name)
#plots.append(p)
#
