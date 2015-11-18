
import sys
sys.path.append('../../../../../')
import supersusy.utils.plot as plot
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region


#############################################
# Set up the samples
#############################################
rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0216/validation/mc/Raw/"
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0216/validation/data/Raw/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0216val/fine_filelists/"
backgrounds = []

#### MC
# Zjets
zjee = background.Background("zee", "Z(ee)+jets (Sherpa)")
zjee.set_debug()
zjee.scale_factor = 1.96
zjee.set_color(r.TColor.GetColor("#2ACB85"))
zjee.set_treename("zjee_sherpa")
zjee.set_chain_from_list_CONDOR(filelist_dir + "zjets_sherpa_ee", rawdir)
backgrounds.append(zjee)

zjmm = background.Background("zmm", "Z(#mu#mu)+jets (Sherpa)")
zjmm.set_debug()
zjmm.scale_factor = 1.96
zjmm.set_color(r.TColor.GetColor("#29C692"))
zjmm.set_treename("zjmm_sherpa")
zjmm.set_chain_from_list_CONDOR(filelist_dir + "zjets_sherpa_mm", rawdir)
backgrounds.append(zjmm)

zjtt = background.Background("ztt", "Z(#tau#tau)+jets (Sherpa)")
zjtt.set_debug()
zjtt.scale_factor = 1.96
zjtt.set_color(r.TColor.GetColor("#29B6B2"))
zjtt.set_treename("zjtt_sherpa")
zjtt.set_chain_from_list_CONDOR(filelist_dir + "zjets_sherpa_tautau", rawdir)
backgrounds.append(zjtt)

zjnn = background.Background("znn", "Z(#nu#nu)+jets (Sherpa)")
zjnn.set_debug()
zjnn.scale_factor = 1.96
zjnn.set_color(r.TColor.GetColor("#28B0BF"))
zjnn.set_treename("zjnn_sherpa")
zjnn.set_chain_from_list_CONDOR(filelist_dir + "zjets_sherpa_nunu", rawdir)
backgrounds.append(zjnn)

ttbar = background.Background("ttbar", "TTbar")
ttbar.set_debug()
ttbar.scale_factor = 1.96
ttbar.set_color(r.TColor.GetColor("#E67067"))
ttbar.set_treename("ttbar_powheg")
ttbar.set_chain_from_list_CONDOR(filelist_dir + "ttbar/", rawdir)
backgrounds.append(ttbar)

# singletop
stop_t = background.Background("st_tchan", "Singletop (t-chan)")
stop_t.set_debug()
stop_t.scale_factor = 1.96
stop_t.set_color(r.TColor.GetColor("#DE080C"))
stop_t.set_treename("stop_t")
stop_t.set_chain_from_list_CONDOR(filelist_dir + "st_tchan/", rawdir)
backgrounds.append(stop_t)

stop_wt = background.Background("st_wt", "Singletop (Wt)")
stop_wt.set_debug()
stop_wt.scale_factor = 1.96
stop_wt.set_color(r.TColor.GetColor("#FEBEA1"))
stop_wt.set_treename("stop_wt")
stop_wt.set_chain_from_list_CONDOR(filelist_dir + "st_wtinc/", rawdir)
backgrounds.append(stop_wt)

# wjets
wjets_e = background.Background("wjets_enu", "W(e#nu)+jets (Sherpa)")
wjets_e.set_debug()
wjets_e.scale_factor = 1.96
wjets_e.set_color(r.TColor.GetColor("#5E9AD6"))
wjets_e.set_treename("wjets_enu")
wjets_e.set_chain_from_list_CONDOR(filelist_dir + "wjets_sherpa_enu/", rawdir)
backgrounds.append(wjets_e)

wjets_m = background.Background("wjets_munu", "W(#mu#nu)+jets (Sherpa)")
wjets_m.set_debug()
wjets_m.scale_factor = 1.96
wjets_m.set_color(r.TColor.GetColor("#27A0E1"))
wjets_m.set_treename("wjets_munu")
wjets_m.set_chain_from_list_CONDOR(filelist_dir + "wjets_sherpa_munu/", rawdir)
backgrounds.append(wjets_m)

wjets_t = background.Background("wjets_taunu", "W(#tau#nu)+jets (Sherpa)")
wjets_t.set_debug()
wjets_t.scale_factor = 1.96
wjets_t.set_color(r.TColor.GetColor("#28AFC1"))
wjets_t.set_treename("wjets_taunu")
wjets_t.set_chain_from_list_CONDOR(filelist_dir + "wjets_sherpa_taunu/", rawdir)
backgrounds.append(wjets_t)


#diboson
diboson = background.Background("vv", "VV (Sherpa)")
diboson.set_debug()
diboson.scale_factor = 1.96
diboson.set_color(r.TColor.GetColor("#315E88"))
diboson.set_treename("VV_sherpa")
diboson.set_chain_from_list_CONDOR(filelist_dir + "diboson_sherpa/", rawdir)
backgrounds.append(diboson)

#### DATA
data = background.Data()
data.set_color(r.kBlack)
data.set_treename("Data")
data.set_chain_from_list_CONDOR(filelist_dir + "data/", data_rawdir)


#############################################
# Set up the regions
#############################################
regions = []
reg = region.Region()
reg.simplename = "zpeak_mm_0j"
reg.displayname = "Z #rightarrow #mu#mu (nJ>=0 nB=0)"
reg.tcut = "nLeptons==2 && nMuons==2 && nSJets>=0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<1 && abs(mll-91.2)<20"
regions.append(reg)


reg = region.Region()
reg.simplename = "zpeak_mm_0j"
reg.displayname = "Z #rightarrow #mu#mu (nJ==0 nB=0)"
reg.tcut = "nLeptons==2 && nMuons==2 && nSJets==0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<1 && abs(mll-91.2)<20"
regions.append(reg)

#############################################
# Set up the plots
#############################################

plots = []

#### zpeak_mm_0j
logy = 1000000000


## nVtx
p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "nVtx", "zpeak_mm_0j_nVtx")
p.labels(x="nVtx", y = "Entries / 1")
p.xax(1, 0, 45)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

## mu
p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "avgMu", "zpeak_mm_0j_avgMu")
p.labels(x="<#mu>", y = "Entries / 2")
p.xax(2, 0, 50)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

## leptons
p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "l_pt[0]", "zpeak_mm_0j_lpt0")
p.labels(x="lead lepton pt [GeV]", y = "Entries / 30 GeV")
p.xax(30, 0, 700)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "l_pt[1]", "zpeak_mm_0j_lpt1")
p.labels(x="sub-lead lepton pt [GeV]", y = "Entries / 20 GeV")
p.xax(20, 0, 350)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "l_eta[0]", "zpeak_mm_0j_leta0")
p.labels(x="lead lepton eta", y = "Entries / 0.2")
p.xax(0.2, -3.5, 3.5)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "l_eta[1]", "zpeak_mm_0j_leta1")
p.labels(x="sub-lead lepton eta", y = "Entries / 0.2")
p.xax(0.2, -3.5, 3.5)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "l_phi[0]", "zpeak_mm_0j_lphi0")
p.labels(x="lead lepton phi", y = "Entries / 0.5 rad")
p.xax(0.5, -3.2, 3.2)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "l_phi[1]", "zpeak_mm_0j_lphi1")
p.labels(x="sub-lead lepton phi", y = "Entries / 0.5 rad")
p.xax(0.5, -3.2, 3.2)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "pTll", "zpeak_mm_0j_pTll")
p.labels(x="dilepton pT [GeV]", y = "Entries / 20 GeV")
p.xax(20, 0, 600)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "dphi_ll", "zpeak_mm_0j_dphi_ll")
p.labels(x="dphi_ll", y = "Entries / 0.5 rad")
p.xax(0.5, -3.2, 3.2)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "mll", "zpeak_mm_0j_mll")
p.labels(x="dilepton invariant mass [GeV]", y = "Entries / 2 GeV")
p.xax(2, 80, 110)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

## jets
p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "nSJets", "zpeak_mm_0j_nSJets")
p.labels(x="number of jets (non-b-tag)", y = "Entries / 1")
p.xax(1, 0, 10)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "sj_pt[0]", "zpeak_mm_0j_sjpt0")
p.labels(x="lead jet (non b) pt [GeV]", y = "Entries / 20 GeV")
p.xax(20, 0, 500)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "sj_eta[0]", "zpeak_mm_0j_sjeta0")
p.labels(x="lead jet (non b) #eta", y = "Entries")
p.xax(0.5, -5, 5)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "sj_pt[1]", "zpeak_mm_0j_sjpt1")
p.labels(x="sub-lead jet (non b) pt [GeV]", y = "Entries / 20 GeV")
p.xax(20, 0, 500)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "sj_eta[1]", "zpeak_mm_0j_sjeta1")
p.labels(x="sub-lead jet (non b) #eta", y = "Entries")
p.xax(0.5, -5, 5)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "mt2", "zpeak_mm_0j_mt2")
p.labels(x="m_{T2} [GeV]", y = "Entries / 10 GeV")
p.xax(10, 0, 220)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

#### met plots
p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "met", "zpeak_mm_0j_met")
p.labels(x="TST #slash{E}_{T} [GeV]", y="Entries / 10 GeV")
p.xax(10,0,275)
p.yax(0.1,logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "metPhi", "zpeak_mm_0j_metPhi")
p.labels(x="metPhi", y="Entries / 0.5 radian")
p.xax(0.5, -3.2, 3.2)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "refEle_et", "zpeak_mm_0j_refEle_et")
p.labels(x="refEle_et", y = "Entries / 20 GeV")
p.xax(20, 0, 600)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "refJet_et", "zpeak_mm_0j_refJet_et")
p.labels(x="refJet_et", y="Entries / 40 GeV")
p.xax(40, 0, 800)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "softTerm_et", "zpeak_mm_0j_softTerm_et")
p.labels(x="softTerm_et", y="Entries / 5 GeV")
p.xax(5, 0, 200)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "refMuo_et", "zpeak_mm_0j_refMuo_et")
p.labels(x="refMuo_et", y = "Entries / 20 GeV")
p.xax(20, 0, 600)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "sumet", "zpeak_mm_0j_sumet")
p.labels(x="sumet", y = "Entries / 20 GeV")
p.xax(20, 0, 500)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "refEle_sumet", "zpeak_mm_0j_refEle_sumet")
p.labels(x="refEle_sumet", y = "Entries / 40 GeV")
p.xax(40, 0, 800)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "refJet_sumet", "zpeak_mm_0j_refJet_sumet")
p.labels(x="refJet_sumet", y = "Entries / 40 GeV")
p.xax(40, 0, 1000)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "softTerm_sumet", "zpeak_mm_0j_softTerm_sumet")
p.labels(x="softTerm_sumet", y = "Entries / 10 GeV")
p.xax(10, 0, 200)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_mm_0j", "refMuo_sumet", "zpeak_mm_0j_refMuo_sumet")
p.labels(x="refMuo_sumet", y = "Entries / 40 GeV")
p.xax(40, 0 ,800)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)






