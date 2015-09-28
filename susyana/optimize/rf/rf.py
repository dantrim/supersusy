import os
import sys
sys.path.append(os.environ['SUSYDIR'])
import supersusy.utils.plot as plot
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region


#################################################
## Set up your backgrounds and signal samples
#################################################
#rawdir = "/gdata/atlas/dantrim/SusyAna/histoAna/run2early/n0213/mc/2lep_mu/Raw/"
rawdir = "/gdata/atlas/dantrim/SusyAna/histoAna/run2early/n0213/mc/rf/Raw/"
filelist_dir = "/gdata/atlas/dantrim/SusyAna/n0213val/Superflow/run/filelists/"
backgrounds = []


# ttbro
ttbar = background.Background("ttbar", "TTbar")
ttbar.set_debug()
ttbar.scale_factor = 25.5
ttbar.set_color(r.TColor.GetColor("#E67067"))
ttbar.set_treename("ttbar_powheg")
ttbar.set_chain_from_list(filelist_dir + "ttbar_powheg_n0213.txt", rawdir)
backgrounds.append(ttbar)

# Zjets
zjets = background.Background("zjets", "Z+jets (Powheg)")
zjets.set_debug()
zjets.scale_factor = 25.5
zjets.set_color(r.TColor.GetColor("#82DE68"))
zjets.set_treename("Zjets_powheg")
#zjets.set_treename("Zjets_sherpa")
zjets.set_chain_from_list(filelist_dir + "zjets_powheg_n0213.txt", rawdir)
#zjets.set_chain_from_list(filelist_dir + "zjets_sherpa_n0213.txt", rawdir)
backgrounds.append(zjets)

# singletop
stop = background.Background("st", "ST")
stop.set_debug()
stop.scale_factor = 25.5
stop.set_color(r.TColor.GetColor("#DE080C"))
stop.set_treename("ST")
stop.set_chain_from_list(filelist_dir + "singletop_powheg_n0213.txt", rawdir)
backgrounds.append(stop)

# wjets
wjets = background.Background("wjets", "W+jets (Sherpa)")
wjets.set_debug()
wjets.scale_factor = 25.5
wjets.set_color(r.TColor.GetColor("#5E9AD6"))
wjets.set_treename("Wjets_sherpa")
wjets.set_chain_from_list(filelist_dir + "wjets_sherpa_n0213.txt", rawdir)
backgrounds.append(wjets)

# ww
ww = background.Background("ww", "WW (Powheg)")
ww.set_debug()
ww.scale_factor = 25.5
ww.set_color(r.TColor.GetColor("#315E88"))
ww.set_treename("WW_powheg")
ww.set_chain_from_list(filelist_dir + "ww_powheg_n0213.txt", rawdir)
backgrounds.append(ww)

# wz
wz = background.Background("wz", "WZ (Powheg)")
wz.set_debug()
wz.scale_factor = 25.5
wz.set_color(r.TColor.GetColor("#F9F549"))
wz.set_treename("WZ_powheg")
wz.set_chain_from_list(filelist_dir + "wz_powheg_n0213.txt", rawdir)
backgrounds.append(wz)

# zz
zz = background.Background("zz", "ZZ (Powheg)")
zz.set_debug()
zz.scale_factor = 25.5
zz.set_color(r.TColor.GetColor("#FFEF53"))
zz.set_treename("ZZ_powheg")
zz.set_chain_from_list(filelist_dir + "zz_powheg_n0213.txt", rawdir)




sig = background.Background("bwn250_160", "(250,160)")
sig.setSignal()
sig.set_debug()
sig.scale_factor = 25.5
sig.set_color(r.kBlue)
sig.set_treename("sig1")
sig.set_chain_from_list(filelist_dir + "bwn_406009_n0213.txt", rawdir)
backgrounds.append(sig)

sig2 = background.Background("bwn300_150", "(300,150)")
sig2.setSignal()
sig2.set_debug()
sig2.scale_factor = 25.5
sig2.set_color(r.kGreen)
sig2.set_treename("sig2")
sig2.set_chain_from_list(filelist_dir + "bwn_406010_n0213.txt", rawdir)
backgrounds.append(sig2)


sig3 = background.Background("bwn300_180", "(300,180)")
sig3.setSignal()
sig3.set_debug()
sig3.scale_factor = 25.5
sig3.set_color(r.kCyan)
sig3.set_treename("sig3")
sig3.set_chain_from_list(filelist_dir + "bwn_406011_n0213.txt", rawdir)
backgrounds.append(sig3)

#################################################
## Set up the regions
#################################################
regions = []

reg = region.Region("rf", "Stop2l-RF")
reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && nBJets==1 && DPB_vTT>(1.5*abs(cosThetaB) +2)"

regions.append(reg)



#################################################
## Set up any plots
#################################################
plots = []

p = plot.Plot1D()
p.initialize("stop", "mt2", "stop_mt2")
p.labels(x="mt2", y = "Entries")
p.xax(5, 0, 150)
p.doLogY = True
p.yax(0.01, 100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("stop", "R2", "stop_R2")
p.labels(x="R2", y = "Entries")
p.xax(0.05,0,1)
p.doLogY = True
p.yax(0.01, 100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)


##### simple vars
p = plot.Plot1D()
p.initialize("stop", "l_pt[0]", "stop_lpt0")
p.labels(x="lpt0 [GeV]", y="Entries")
p.xax(10, 0, 250)
p.doLogY = True
p.yax(0.01, 100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("stop", "l_pt[1]", "stop_lpt1")
p.labels(x="lpt1 [GeV]", y="Entries")
p.xax(10, 0, 250)
p.doLogY = True
p.yax(0.01, 100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("stop", "l_eta[0]", "stop_leta0")
p.labels(x="leta0 [GeV]", y="Entries")
p.xax(0.5, -5, 5)
p.doLogY = True
p.yax(0.01, 100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("stop", "l_eta[1]", "stop_leta1")
p.labels(x="leta1 [GeV]", y="Entries")
p.xax(0.5, -5, 5)
p.doLogY = True
p.yax(0.01, 100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("stop", "pTll", "stop_pTll")
p.labels(x="pTll [GeV]", y="Entries")
p.xax(10,0,200)
p.doLogY = True
p.yax(0.01,100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("stop", "abs(dphi_ll)", "stop_dphi_ll")
p.labels(x="|dphill|", y="Entries")
p.xax(0.05,0,3.2)
p.doLogY = True
p.yax(0.01,100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("stop", "shat", "stop_shatr")
p.labels(x="shatr [GeV]", y = "Entries")
p.xax(20,0,400)
p.doLogY = True
p.yax(0.01, 100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("stop", "abs(cosThetaRp1)", "stop_cosThetaRp1")
p.labels(x="|cosThetaRp1|", y = "Entries")
p.xax(0.05,0,1)
p.doLogY = True
p.yax(0.01, 100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)


p = plot.Plot1D()
p.initialize("stop", "MDR", "stop_MDR")
p.labels(x="mdr [GeV]", y = "Entries")
p.xax(10,0,200)
p.doLogY = True
p.yax(0.01, 100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)



p = plot.Plot1D()
p.initialize("stop", "abs(cosThetaB)", "stop_cosThetaB")
p.labels(x="|cosThetaB|", y = "Entries")
p.xax(0.05,0,1)
p.doLogY = True
p.yax(0.01, 100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)


### bjets

p = plot.Plot1D()
p.initialize("stop", "nBJets", "stop_nBJets")
p.labels(x="nBJets", y = "Entries")
p.xax(1,0,10)
p.doLogY = True
p.yax(0.01, 100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("stop", "bj_pt[0]", "stop_bjpt0")
p.labels(x="bjpt0 [GeV]", y = "Entries")
p.xax(10,0,250)
p.doLogY = True
p.yax(0.01,100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("stop", "bj_pt[1]", "stop_bjpt1")
p.labels(x="bjpt1 [GeV]", y = "Entries")
p.xax(10,0,250)
p.doLogY = True
p.yax(0.01,100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("stop", "bj_eta[0]", "stop_bjeta0")
p.labels(x="bjeta0", y = "Entries")
p.xax(0.5,-5,5)
p.doLogY = True
p.yax(0.01,100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("stop", "bj_eta[1]", "stop_bjeta1")
p.labels(x="bjeta1", y = "Entries")
p.xax(0.5,-5,5)
p.doLogY = True
p.yax(0.01,100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)


### jets

p = plot.Plot1D()
p.initialize("stop", "nSJets", "stop_nSJets")
p.labels(x="nSJets", y = "Entries")
p.xax(1,0,10)
p.doLogY = True
p.yax(0.01, 100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)


p = plot.Plot1D()
p.initialize("stop", "sj_pt[0]", "stop_sjpt0")
p.labels(x="sjpt0 [GeV]", y = "Entries")
p.xax(10,0,250)
p.doLogY = True
p.yax(0.01,100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("stop", "sj_pt[1]", "stop_sjpt1")
p.labels(x="sjpt1 [GeV]", y = "Entries")
p.xax(10,0,250)
p.doLogY = True
p.yax(0.01,100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("stop", "sj_eta[0]", "stop_sjeta0")
p.labels(x="sjeta0", y = "Entries")
p.xax(0.5,-5,5)
p.doLogY = True
p.yax(0.01,100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("stop", "sj_eta[1]", "stop_sjeta1")
p.labels(x="sjeta1", y = "Entries")
p.xax(0.5,-5,5)
p.doLogY = True
p.yax(0.01,100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("stop", "pBll", "stop_pBll")
p.labels(x="pBll [GeV]", y = "Entries")
p.xax(10,0,200)
p.doLogY = True
p.yax(0.01,100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)


### RF
### mt2
p = plot.Plot1D()

p.initialize("rf", "mt2", "rf_mt2")
p.labels(x="m_{t2} [GeV]", y = "")
p.xax(10, 0, 220)
p.doLogY = True
p.yax(0.1,100)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

### shat
p = plot.Plot1D()

p.initialize("rf", "shat", "rf_shat")
p.labels(x="shat", y="")
p.xax(40, 0, 1500)
p.doLogY = True
p.yax(0.1, 100)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## RPT
p = plot.Plot1D()

p.initialize("rf", "RPT", "rf_RPT")
p.labels(x="RPT", y= "")
p.xax(0.05, 0, 1)
p.doLogY = True
p.yax(0.1, 100)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## dphi_b_w2_t1
p = plot.Plot1D()

p.initialize("rf", "dphi_b_w2_t1", "rf_dphi_b_w2_t1")
p.labels(x="dphi_b_w2_t1", y="")
p.xax(0.1, -3.2, 3.2)
p.doLogY = True
p.yax(0.1, 100)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## dphi_b_w1_t2
p = plot.Plot1D()

p.initialize("rf", "dphi_b_w1_t2", "rf_dphi_b_w1_t2")
p.labels(x="dphi_b_w1_t2", y ="")
p.xax(0.1, -3.2, 3.2)
p.doLogY = True
p.yax(0.1, 100)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## DPB_vTT
p = plot.Plot1D()

p.initialize("rf", "DPB_vTT", "rf_DPB_vTT")
p.labels(x="DPB_vTT", y="")
p.xax(0.05, 0, 3.2)
p.doLogY = True
p.yax(0.1, 100)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## DPB_vT1
p = plot.Plot1D()

p.initialize("rf", "DPB_vT1", "rf_DPB_vT1")
p.labels(x="DPB_vT1", y="")
p.xax(0.05, 0, 3.2)
p.doLogY = True
p.yax(0.1, 100)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## DPD_t1_tt
p = plot.Plot1D()

p.initialize("rf", "DPD_t1_tt", "rf_DPD_t1_tt")
p.labels(x="DPD_t1_tt", y="")
p.xax(0.1, 0, 6.4)
p.doLogY = True
p.yax(0.1, 100)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## DPD_t2_tt
p = plot.Plot1D()

p.initialize("rf", "DPD_t2_tt", "rf_DPD_t2_tt")
p.labels(x="DPD_t2_tt", y="")
p.xax(0.1, 0, 6.4)
p.doLogY = True
p.yax(0.1, 100)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## DPD_t1_t2
p = plot.Plot1D()

p.initialize("rf", "DPD_t1_t2", "rf_DPD_t1_t2")
p.labels(x="DPD_t1_t2", y="")
p.xax(0.1, 0, 6.4)
p.doLogY = True
p.yax(0.1, 100)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## COS_t1_lab
p = plot.Plot1D()

p.initialize("rf", "COS_t1_lab", "rf_COS_t1_lab")
p.labels(x="COS_t1_lab", y="")
p.xax(0.05, -1, 1)
p.doLogY = True
p.yax(0.1, 100)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## COS_t2_lab
p = plot.Plot1D()

p.initialize("rf", "COS_t2_lab", "rf_COS_t2_lab")
p.labels(x="COS_t2_lab", y = "")
p.xax(0.05, -1, 1)
p.doLogY = True
p.yax(0.1, 100)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## COS_tt_lab
p = plot.Plot1D()

p.initialize("rf", "COS_tt_lab", "rf_COS_tt_lab")
p.labels(x="COS_tt_lab", y="")
p.xax(0.05, -1, 1)
p.doLogY = True
p.yax(0.1, 100)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## MDR_l1_t1
p = plot.Plot1D()

p.initialize("rf", "MDR_l1_t1", "rf_MDR_l1_t1")
p.labels(x="MDR_l1_t1", y="")
p.xax(10, 0, 600)
p.doLogY = True
p.yax(0.1, 100)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## MDR_l2_t2
p = plot.Plot1D()

p.initialize("rf", "MDR_l2_t2", "rf_MDR_l2_t2")
p.labels(x="MDR_l2_t2", y ="")
p.xax(10, 0, 600)
p.doLogY = True
p.yax(0.1, 100)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## MDR_b1_t1
p = plot.Plot1D()

p.initialize("rf", "MDR_b1_t1", "rf_MDR_b1_t1")
p.labels(x="MDR_b1_t1", y="")
p.xax(10, 0, 600)
p.doLogY = True
p.yax(0.1, 100)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## MDR_l1_w1
p = plot.Plot1D()

p.initialize("rf", "MDR_l1_w1", "rf_MDR_l1_w1")
p.labels(x="MDR_l1_w1", y="")
p.xax(10, 0, 250)
p.doLogY = True
p.yax(0.1, 100)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## MDR_l2_w2
p = plot.Plot1D()

p.initialize("rf", "MDR_l2_w2", "rf_MDR_l2_w2")
p.labels(x="MDR_l2_w2", y="")
p.xax(10, 0, 250)
p.doLogY = True
p.yax(0.1, 100)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

## MTT
p = plot.Plot1D()

p.initialize("rf", "MTT", "rf_MTT")
p.labels(x="MTT", y="")
p.xax(20, 0, 1000)
p.doLogY = True
p.yax(0.1, 100)
p.setDoubleRatioCanvas(p.name)
plots.append(p)





