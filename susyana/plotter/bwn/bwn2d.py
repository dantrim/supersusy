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
rawdir = "/gdata/atlas/dantrim/SusyAna/histoAna/run2early/n0213/mc/Sep12/Raw/"
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
#zjets = background.Background("zjets", "Z+jets (Powheg)")
#zjets.set_debug()
#zjets.scale_factor = 25.5
#zjets.set_color(r.TColor.GetColor("#82DE68"))
#zjets.set_treename("Zjets_powheg")
##zjets.set_treename("Zjets_sherpa")
#zjets.set_chain_from_list(filelist_dir + "zjets_powheg_n0213.txt", rawdir)
##zjets.set_chain_from_list(filelist_dir + "zjets_sherpa_n0213.txt", rawdir)
#backgrounds.append(zjets)

# singletop
stop = background.Background("st", "ST")
stop.set_debug()
stop.scale_factor = 25.5
stop.set_color(r.TColor.GetColor("#DE080C"))
stop.set_treename("ST")
stop.set_chain_from_list(filelist_dir + "singletop_powheg_n0213.txt", rawdir)
backgrounds.append(stop)

# wjets
#wjets = background.Background("wjets", "W+jets (Sherpa)")
#wjets.set_debug()
#wjets.scale_factor = 25.5
#wjets.set_color(r.TColor.GetColor("#5E9AD6"))
#wjets.set_treename("Wjets_sherpa")
#wjets.set_chain_from_list(filelist_dir + "wjets_sherpa_n0213.txt", rawdir)
#backgrounds.append(wjets)

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
backgrounds.append(zz)




sig = background.Background("bwn_250_160", "(250,160)")
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
#reg = region.Region("test", "TEST")
#reg.tcut = "nLeptons==2 && nMuons==1 && nElectrons==1"
#regions.append(reg)

initials = ["1.0", "1.2", "1.4", "1.6", "1.8", "2.0", "2.2", "2.4", "2.6", "2.8", "3.0"]
finals = ["1.0", "1.4", "1.8", "2.0", "2.2", "2.4", "2.5"]



reg = region.Region()
reg.simplename = "wwLoose"
reg.displayname = "wwLoose"
reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0"
regions.append(reg)


plots = []
samples = ["ww", "ttbar", "bwn_250_160"]
for samp in samples :
    p = plot.Plot2D()
    p.initialize("wwLoose", "DPB", "R2", "wwLoose_DPB_R2_%s_2d"%samp)
    p.labels(x="dpb", y="r2")
    p.set_sample(samp)
    p.xax(0.1, 0, 3.2)
    p.yax(0.05, 0, 1)
    p.defaultCanvas()
    plots.append(p)

    p = plot.Plot2D()
    p.initialize("wwLoose", "abs(cosThetaB)", "R2", "wwLoose_cosThetaB_R2_%s_2d"%samp)
    p.labels(x="|cosThetaB|", y="r2")
    p.set_sample(samp)
    p.xax(0.05, 0, 1)
    p.yax(0.05, 0, 1)
    p.defaultCanvas()
    plots.append(p)

#    #### dphi_l1_l2 R2
#    #### dphi_l1_l2 R2
#    p = plot.Plot2D()
#    p.initialize("wwLoose", "R2", "abs(dphi_l1_l2)", "wwLoose_R2_dphi_l1_l2_%s_2d"%samp)
#    p.labels(x="R2", y = "#Delta#phi(l_{1},l_{2})^{CM}")
#    p.set_sample(samp)
#    p.xax(0.05, 0, 1)
#    p.yax(0.1, 0, 3.2)
#    p.defaultCanvas()
#    plots.append(p)
#
#    #### dphi_l1_l2 cosThetaRp1
#    p = plot.Plot2D()
#    p.initialize("wwLoose", "abs(cosThetaRp1)", "abs(dphi_l1_l2)", "wwLoose_cosThetaRp1_dphi_l1_l2_%s_2d"%samp)
#    p.labels(x="|cosThetaRp1|", y = "#Delta#phi(l_{1},l_{2})^{CM}")
#    p.set_sample(samp)
#    p.xax(0.05, 0, 1)
#    p.yax(0.1, 0, 3.2)
#    p.defaultCanvas()
#    plots.append(p)
#
#
#
#
#
#
#
#
#
