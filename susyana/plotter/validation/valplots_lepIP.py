
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
reg.simplename = "zpeak_ee_inc"
reg.displayname = "Z #rightarrow ee (nJ>=0 nB=0)"
reg.tcut = "nLeptons==2 && nElectrons==2 && nSJets>=0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<1 && abs(mll-91.2)<20"
regions.append(reg)


reg = region.Region()
reg.simplename = "zpeak_ee_0j"
reg.displayname = "Z #rightarrow ee (nJ==0 nB=0)"
reg.tcut = "nLeptons==2 && nElectrons==2 && nSJets==0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<1 && abs(mll-91.2)<20"
regions.append(reg)

#############################################
# Set up the plots
#############################################

plots = []

#### zpeak_ee_inc
logy = 1000000000


## nVtx
p = plot.Plot1D()
p.initialize("zpeak_ee_inc", "nVtx", "zpeak_ee_inc_nVtx")
p.labels(x="nVtx", y = "Entries / 1")
p.xax(1, 0, 45)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

## mu
p = plot.Plot1D()
p.initialize("zpeak_ee_inc", "avgMu", "zpeak_ee_inc_avgMu")
p.labels(x="<#mu>", y = "Entries / 2")
p.xax(2, 0, 50)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_ee_inc", "l_d0sigBSCorr[0]", "zpeak_ee_inc_d0sigBSCorr0")
p.labels(x="lead lep d0sigBSCorr", y = "Entries / 0.25")
p.xax(0.25, -4, 4)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_ee_inc", "l_z0sinTheta[0]", "zpeak_ee_inc_z0sinTheta0")
p.labels(x="lead lepton z0sinTheta", y = "Entries / 0.1 mm")
p.xax(0.1, -1, 1)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_ee_inc", "l_ptvarcone20[0]", "zpeak_ee_inc_ptvarcone200")
p.labels(x="lead lepton ptvarcone20", y = "Entries / 5 GeV")
p.xax(5, 0, 100)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_ee_inc", "l_etconetopo20[0]", "zpeak_ee_inc_etconetopo200")
p.labels(x="lead lepton etconetopo20", y = "Entries / 1 GeV")
p.xax(1, 0, 30)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_ee_inc", "l_ptvarcone30[0]", "zpeak_ee_inc_ptvarcone300")
p.labels(x="lead lepton ptvarcone30", y = "Entries / 5 GeV")
p.xax(5, 0, 100)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_ee_inc", "l_etconetopo30[0]", "zpeak_ee_inc_etconetopo300")
p.labels(x="lead lepton etconetopo30", y = "Entreis / 5 GeV")
p.xax(5, 0, 100)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)


p = plot.Plot1D()
p.initialize("zpeak_ee_inc", "l_d0sigBSCorr[1]", "zpeak_ee_inc_d0sigBSCorr1")
p.labels(x="sub-lead lep d0sigBSCorr", y = "Entries / 0.25")
p.xax(0.25, -4, 4)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_ee_inc", "l_z0sinTheta[1]", "zpeak_ee_inc_z0sinTheta1")
p.labels(x="sub-lead lepton z0sinTheta", y = "Entries / 0.1 mm")
p.xax(0.1, -1, 1)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_ee_inc", "l_ptvarcone20[1]", "zpeak_ee_inc_ptvarcone201")
p.labels(x="sub-lead lepton ptvarcone20", y = "Entries / 5 GeV")
p.xax(5, 0, 100)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_ee_inc", "l_etconetopo20[1]", "zpeak_ee_inc_etconetopo201")
p.labels(x="sub-lead lepton etconetopo20", y = "Entries / 1 GeV")
p.xax(1, 0, 20)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_ee_inc", "l_ptvarcone30[1]", "zpeak_ee_inc_ptvarcone301")
p.labels(x="sub-lead lepton ptvarcone30", y = "Entries / 5 GeV")
p.xax(5, 0, 100)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("zpeak_ee_inc", "l_etconetopo30[1]", "zpeak_ee_inc_etconetopo301")
p.labels(x="sub-lead lepton etconetopo30", y = "Entreis / 5 GeV")
p.xax(5, 0, 100)
p.yax(0.1, logy)
p.doLogY = True
p.setRatioCanvas(p.name)
plots.append(p)

