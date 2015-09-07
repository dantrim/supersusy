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
rawdir = "/gdata/atlas/dantrim/SusyAna/histoAna/run2early/n0213/mc/2lep_mu/Raw/"
filelist_dir = "/gdata/atlas/dantrim/SusyAna/n0213val/Superflow/run/filelists/"
backgrounds = []


# ttbro
ttbar = background.Background("ttbar", "TTbar")
ttbar.set_debug()
ttbar.scale_factor = 1.0
ttbar.set_color(r.TColor.GetColor("#E67067"))
ttbar.set_treename("ttbar_powheg")
ttbar.set_chain_from_list(filelist_dir + "ttbar_powheg_n0213.txt", rawdir)
backgrounds.append(ttbar)

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




sig = background.Background("bwn250_160", "(250,160)")
sig.setSignal()
sig.set_debug()
sig.scale_factor = 1.0
sig.set_color(r.kBlue)
sig.set_treename("sig1")
sig.set_chain_from_list(filelist_dir + "bwn_406009_n0213.txt", rawdir)
backgrounds.append(sig)

sig2 = background.Background("bwn300_150", "(300,150)")
sig2.setSignal()
sig2.set_debug()
sig2.scale_factor = 1.0
sig2.set_color(r.kGreen)
sig2.set_treename("sig2")
sig2.set_chain_from_list(filelist_dir + "bwn_406010_n0213.txt", rawdir)
backgrounds.append(sig2)


sig3 = background.Background("bwn300_180", "(300,180)")
sig3.setSignal()
sig3.set_debug()
sig3.scale_factor = 1.0
sig3.set_color(r.kCyan)
sig3.set_treename("sig3")
sig3.set_chain_from_list(filelist_dir + "bwn_406011_n0213.txt", rawdir)
backgrounds.append(sig3)

#################################################
## Set up the regions
#################################################
regions = []
reg = region.Region("test", "TEST")
reg.tcut = "nLeptons==2 && nMuons==1 && nElectrons==1"
regions.append(reg)

reg = region.Region("stop", "Stop2l")
reg.tcut = "nLeptons==2 && nMuons==1 && nElectrons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && abs(cosThetaB) < 0.60"
regions.append(reg)


#################################################
## Set up any plots
#################################################
plots = []

p = plot.Plot1D()
p.initialize("stop", "DPB", "stop_DPB")
p.labels(x="dpb", y = "Entries")
p.xax(0.1,0,3.2)
p.doLogY = True
p.yax(0.1, 100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)


p = plot.Plot1D()
p.initialize("stop", "mt2", "stop_mt2")
p.labels(x="mt2", y = "Entries")
p.xax(5, 0, 150)
p.doLogY = True
p.yax(0.1, 100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

p = plot.Plot1D()
p.initialize("stop", "abs(deltaX)", "stop_deltaX")
p.labels(x="deltaX", y = "Entries")
p.xax(0.01, 0, 0.1)
p.doLogY = True
p.yax(0.1, 100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)


p = plot.Plot1D()
p.initialize("stop", "abs(cosThetaB)", "stop_cosThetaB")
p.labels(x="cosThetaB", y = "Entries")
p.xax(0.05,0,1)
p.doLogY = True
p.yax(0.1, 100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)


p = plot.Plot1D()
p.initialize("stop", "R2", "stop_R2")
p.labels(x="R2", y = "Entries")
p.xax(0.05,0,1)
p.doLogY = True
p.yax(0.1, 100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)


p = plot.Plot1D()
p.initialize("stop", "nBJets", "stop_nBJets")
p.labels(x="nBJets", y = "Entries")
p.xax(1,0,10)
p.doLogY = True
p.yax(0.1, 100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)


p = plot.Plot1D()
p.initialize("stop", "nSJets", "stop_nSJets")
p.labels(x="nSJets", y = "Entries")
p.xax(1,0,10)
p.doLogY = True
p.yax(0.1, 100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)
