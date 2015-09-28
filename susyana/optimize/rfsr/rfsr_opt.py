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
rawdir = "/gdata/atlas/dantrim/SusyAna/histoAna/run2early/n0213/mc/rfsr/Raw/"
data_rawdir = "/gdata/atlas/dantrim/SusyAna/histoAna/run2early/n0213/data/Sep12/Raw/"
filelist_dir = "/gdata/atlas/dantrim/SusyAna/n0213val/Superflow/run/filelists/"
backgrounds = []


# ttbro
ttbar = background.Background("ttbar", "t#bar{t}")
ttbar.set_debug()
ttbar.scale_factor = 127.7
ttbar.set_fillStyle(0)
ttbar.setLineStyle(1)
ttbar.set_color(r.TColor.GetColor("#FC0D1B"))
ttbar.set_treename("ttbar_powheg")
ttbar.set_chain_from_list(filelist_dir + "ttbar_powheg_n0213.txt", rawdir)
backgrounds.append(ttbar)

# Zjets
zjets = background.Background("zjets", "Z+jets (Powheg)")
zjets.set_debug()
zjets.scale_factor = 127.7
zjets.set_color(r.TColor.GetColor("#82DE68"))
#zjets.set_treename("Zjets_powheg")
zjets.set_treename("Zjets_sherpa")
#zjets.set_chain_from_list(filelist_dir + "zjets_powheg_n0213.txt", rawdir)
zjets.set_chain_from_list(filelist_dir + "zjets_sherpa_n0213.txt", rawdir)
backgrounds.append(zjets)

# singletop
stop = background.Background("st", "ST")
stop.set_debug()
stop.scale_factor = 127.7
stop.set_color(r.TColor.GetColor("#DE080C"))
stop.set_treename("ST")
stop.set_chain_from_list(filelist_dir + "singletop_powheg_n0213.txt", rawdir)
backgrounds.append(stop)

# wjets
wjets = background.Background("wjets", "W+jets (Sherpa)")
wjets.set_debug()
wjets.scale_factor = 127.7
wjets.set_color(r.TColor.GetColor("#5E9AD6"))
wjets.set_treename("Wjets_sherpa")
wjets.set_chain_from_list(filelist_dir + "wjets_sherpa_n0213.txt", rawdir)
backgrounds.append(wjets)

# ww
ww = background.Background("ww", "WW (Powheg)")
ww.set_debug()
ww.scale_factor = 127.7
ww.set_fillStyle(0)
ww.setLineStyle(1)
ww.set_color(r.TColor.GetColor("#41C1FC"))
ww.set_treename("WW_powheg")
ww.set_chain_from_list(filelist_dir + "ww_powheg_n0213.txt", rawdir)
backgrounds.append(ww)

# wz
wz = background.Background("wz", "WZ (Powheg)")
wz.set_debug()
wz.scale_factor = 127.7
wz.set_color(r.TColor.GetColor("#F9F549"))
wz.set_treename("WZ_powheg")
wz.set_chain_from_list(filelist_dir + "wz_powheg_n0213.txt", rawdir)
backgrounds.append(wz)

# zz
zz = background.Background("zz", "ZZ (Powheg)")
zz.set_debug()
zz.scale_factor = 127.7
zz.set_color(r.TColor.GetColor("#FFEF53"))
zz.set_treename("ZZ_powheg")
zz.set_chain_from_list(filelist_dir + "zz_powheg_n0213.txt", rawdir)
backgrounds.append(zz)


sig = background.Background("bwn_250_160", "(250,160)")
sig.setSignal()
sig.set_debug()
sig.scale_factor = 127.7
sig.set_fillStyle(0)
sig.setLineStyle(2)
sig.set_color(r.kBlue)
sig.set_treename("sig1")
sig.set_chain_from_list(filelist_dir + "bwn_406009_n0213.txt", rawdir)
backgrounds.append(sig)

sig2 = background.Background("bwn300_150", "(300,150)")
sig2.setSignal()
sig2.set_debug()
sig2.scale_factor = 127.7
sig2.set_fillStyle(0)
sig2.setLineStyle(2)
sig2.set_color(r.kGreen)
sig2.set_treename("sig2")
sig2.set_chain_from_list(filelist_dir + "bwn_406010_n0213.txt", rawdir)
backgrounds.append(sig2)


sig3 = background.Background("bwn300_180", "(300,180)")
sig3.setSignal()
sig3.set_debug()
sig3.scale_factor = 127.7
sig3.set_fillStyle(0)
sig3.setLineStyle(2)
sig3.set_color(r.kMagenta)
sig3.set_treename("sig3")
sig3.set_chain_from_list(filelist_dir + "bwn_406011_n0213.txt", rawdir)
backgrounds.append(sig3)


#### DATA
data = background.Data()
data.set_color(r.kBlack)
data.set_treename("Data")
data.set_chain_from_list(filelist_dir + "data15_periodA_n0213.txt", data_rawdir)


#################################################
## Set up the regions
#################################################
regions = []

reg = region.Region("rfsr", "Stop2l-RFSR")
reg.displayname = "WW-pre (DFOS-20)"
#reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && COS_tt_0 > (-1 * (RPT_0 - 0.5) + 1)"
#reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && DPB_vTT_0 > 2.5 && COS_tt_0 > 0.2 && RPT_0 > 0.65 && nBJets==0 && MDR_v1_t1_0 > 80"
#reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && DPB_vTT_0 > 2.5 && COS_tt_0 > 0 && RPT_0 > 0.4 && nBJets==0 && ((MDR_v1_t1_0 - MDR_i1_t1_0)) > 30"
#reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && DPB_vTT_0 > 4*abs(cosThetaB) && nBJets==0 && RPT_0 > 0.65 && COS_tt_0 > 0.2"
#reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && DPB_vTT_0 > (1.0 * abs(cosThetaB) + 1.8) && R2 > 0.65  && nBJets==0 && mt2>80"
#reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && sj_pt[0] > 100 && DPB_vTT_0 > 2.5 && MDR_v1_t1_0 > 30 && COS_tt_0 > -0.5 && RPT_0 > 0.7 && abs(cosThetaB)<0.5" 



### SEP 22
#reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && DPB_vTT_0 > 2.5 && RPT_0 > 0.6 && nBJets==0 && mt2>80"
#nm1 RPT
#reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && DPB_vTT_0 > 2.5 && nBJets==0 && mt2>80"
#nm1 DPB_vTT
#reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && RPT_0 > 0.6 && nBJets==0 && mt2>80"
#nm1 mt2
#reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && DPB_vTT_0 > 2.5 && RPT_0 > 0.6 && nBJets==0"

reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && DPB_vTT_0 > 2. && RPT_0>0.65 && nBJets==0 && mt2>90"
regions.append(reg)

#################################################
## Set up the plots
#################################################

plots = []

#p = plot.Plot1D()
#p.initialize("rfsr", "(RPT_0/RPZ_0)", "rfsr_RPTZratio")
#p.labels(x="RPT/RPZ", y = "")
#p.xax(0.1, 0, 2)
#p.doLogY = True
#p.yax(0.1,10000)
#p.setDoubleRatioCanvas(p.name)
#plots.append(p)
#
#
#p = plot.Plot1D()
#
#p.initialize("rfsr", "((MDR_v1_t1_0 - MDR_i1_t1_0))", "rfsr_MASSRATIO")
#p.labels(x="RATIO [GeV]", y = "")
#p.xax(1, 0, 100)
#p.doLogY = True
#p.yax(0.1,100)
#p.setDoubleRatioCanvas(p.name)
#plots.append(p)
#
#
#
#p = plot.Plot1D()
#p.initialize("rfsr", "sj_pt[0]", "rfsr_sjpt0")
#p.labels(x="jpt0 [GeV]", y = "")
#p.xax(10, 0, 220)
#p.doLogY = True
#p.yax(0.1,100)
#p.setDoubleRatioCanvas(p.name)
#plots.append(p)

### r2

### mt2
p = plot.Plot1D()

p.initialize("rfsr", "mt2", "rfsr_mt2")
p.labels(x="m_{t2} [GeV]", y = "")
p.xax(10, 0, 220)
p.doLogY = True
p.yax(0.1,10000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

### r2
#p = plot.Plot1D()
#
#p.initialize("rfsr", "R2", "rfsr_R2")
#p.leg_is_bottom_left = True
#p.labels(x="R2", y = "")
#p.xax(0.05, 0, 1)
#p.doLogY = True
#p.yax(0.1,10000)
#p.setDoubleRatioCanvas(p.name)
#plots.append(p)

#### r1
#p = plot.Plot1D()
#
#p.initialize("rfsr", "R1", "rfsr_R1")
#p.labels(x="R1", y = "")
#p.xax(0.05, 0, 1)
#p.doLogY = True
#p.yax(0.1,10000)
#p.setDoubleRatioCanvas(p.name)
#plots.append(p)
#
#### cosThetaB
#p = plot.Plot1D()
#
#p.initialize("rfsr", "cosThetaB", "rfsr_cosThetaB")
#p.leg_is_bottom_left = True
#p.labels(x="cos#theta_{b}", y = "")
#p.xax(0.1, -1, 1)
#p.doLogY = True
#p.yax(0.1,10000)
#p.setDoubleRatioCanvas(p.name)
#plots.append(p)
#
#### shat_0
#p = plot.Plot1D()
#
#p.initialize("rfsr", "shat_0", "rfsr_shat0")
#p.labels(x="shat_0", y = "")
#p.xax(40, 0, 1000)
#p.doLogY = True
#p.yax(0.01, 100000)
#p.setDoubleRatioCanvas(p.name)
#plots.append(p)

### RPT_0
p = plot.Plot1D()

p.initialize("rfsr", "RPT_0", "rfsr_RPT0")
p.labels(x="RPT_0", y="")
p.xax(0.05, 0, 1)
p.doLogY = True
p.yax(0.01, 100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

### RPZ_0
#p = plot.Plot1D()
#
#p.initialize("rfsr", "RPZ_0", "rfsr_RPZ0")
#p.labels(x="RPZ_0", y="")
#p.xax(0.05, 0, 1)
#p.doLogY = True
#p.yax(0.01, 100000)
#p.setDoubleRatioCanvas(p.name)
#plots.append(p)
#
#### gamma_rp1_0
#p = plot.Plot1D()
#
#p.initialize("rfsr", "gamma_rp1_0", "rfsr_gamma_rp10")
#p.labels(x="gamma_rp1_0", y="")
#p.xax(0.1, 0, 2)
#p.doLogY = True
#p.yax(0.01, 100000)
#p.setDoubleRatioCanvas(p.name)
#plots.append(p)

### MDR_i1_t1_0
#p = plot.Plot1D()
#
#p.initialize("rfsr", "MDR_i1_t1_0", "rfsr_MDR_i1_t10")
#p.labels(x="MDR_i1_t1_0", y = "")
#p.xax(5, 0, 150)
#p.doLogY = True
#p.yax(0.01, 100000)
#p.setDoubleRatioCanvas(p.name)
#plots.append(p)
#
#### MDR_i1_t2_0
#p = plot.Plot1D()
#
#p.initialize("rfsr", "MDR_i1_t2_0", "rfsr_MDR_i1_t20")
#p.labels(x="MDR_i1_t2_0", y = "")
#p.xax(20, 0, 1000)
#p.doLogY = True
#p.yax(0.01, 100000)
#p.setDoubleRatioCanvas(p.name)
#plots.append(p)
#
#### MDR_i2_t1_0
#p = plot.Plot1D()
#
#p.initialize("rfsr", "MDR_i2_t1_0", "rfsr_MDR_i2_t10")
#p.labels(x="MDR_i2_t1_0", y = "")
#p.xax(20, 0, 1000)
#p.doLogY = True
#p.yax(0.01, 100000)
#p.setDoubleRatioCanvas(p.name)
#plots.append(p)
#
#### MDR_v1_t1_0
#p = plot.Plot1D()
#
#p.initialize("rfsr", "MDR_v1_t1_0", "rfsr_MDR_v1_t10")
#p.labels(x="MDR_v1_t1_0", y="")
#p.xax(10, 0, 200)
#p.doLogY = True
#p.yax(0.01, 100000)
#p.setDoubleRatioCanvas(p.name)
#plots.append(p)
#
#### MDR_v1_t2_0
#p = plot.Plot1D()
#
#p.initialize("rfsr", "MDR_v1_t2_0", "rfsr_MDR_v1_t20")
#p.labels(x="MDR_v1_t2_0", y="")
#p.xax(40, 0, 1000)
#p.doLogY = True
#p.yax(0.01, 100000)
#p.setDoubleRatioCanvas(p.name)
#plots.append(p)
#
#### MDR_v2_t1_0
#p = plot.Plot1D()
#
#p.initialize("rfsr", "MDR_v2_t1_0", "rfsr_MDR_v2_t10")
#p.labels(x="MDR_v2_t1_0", y="")
#p.xax(40, 0, 1000)
#p.doLogY = True
#p.yax(0.01, 100000)
#p.setDoubleRatioCanvas(p.name)
#plots.append(p)


### COS_tt_0
p = plot.Plot1D()

p.initialize("rfsr", "COS_tt_0", "rfsr_COS_tt0")
p.labels(x="COS_tt_0", y = "")
p.xax(0.05, -1,1)
p.doLogY = True
p.yax(0.01, 100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

### COS_t1_0
#p = plot.Plot1D()
#
#p.initialize("rfsr", "COS_t1_0", "rfsr_COS_t10")
#p.labels(x="COS_t1_0", y = "")
#p.xax(0.05, -1, 1)
#p.doLogY = True
#p.yax(0.01, 100000)
#p.setDoubleRatioCanvas(p.name)
#plots.append(p)
#
#### COS_t2_0
#p = plot.Plot1D()
#
#p.initialize("rfsr", "COS_t2_0", "rfsr_COS_t20")
#p.labels(x="COS_t2_0", y = "")
#p.xax(0.05, -1, 1)
#p.doLogY = True
#p.yax(0.01, 100000)
#p.setDoubleRatioCanvas(p.name)
#plots.append(p)
#
#### DPD_tt_t1_0
#p = plot.Plot1D()
#
#p.initialize("rfsr", "DPD_tt_t1_0", "rfsr_DPD_tt_t10")
#p.labels(x="DPD_tt_t1_0", y = "")
#p.xax(0.1, 0, 6.4)
#p.doLogY = True
#p.yax(0.01, 100000)
#p.setDoubleRatioCanvas(p.name)
#plots.append(p)
#
#### DPD_tt_t2_0
#p = plot.Plot1D()
#
#p.initialize("rfsr", "DPD_tt_t2_0", "rfsr_DPD_tt_t20")
#p.labels(x="DPD_tt_t2_0", y = "")
#p.xax(0.1, 0, 6.4)
#p.doLogY = True
#p.yax(0.01, 100000)
#p.setDoubleRatioCanvas(p.name)
#plots.append(p)
#
#### DPD_lab_tt_0
#p = plot.Plot1D()
#
#p.initialize("rfsr", "DPD_lab_tt_0", "rfsr_DPD_lab_tt0")
#p.labels(x="DPD_lab_tt_0", y = "")
#p.xax(0.1, 0, 6.4)
#p.doLogY = True
#p.yax(0.01, 100000)
#p.setDoubleRatioCanvas(p.name)
#plots.append(p)

### DPB_vTT_0
p = plot.Plot1D()

p.initialize("rfsr", "DPB_vTT_0", "rfsr_DPB_vTT0")
p.labels(x="DPB_vTT_0", y = "")
p.xax(0.1, 0, 3.2)
p.doLogY = True
p.yax(0.01, 100000)
p.setDoubleRatioCanvas(p.name)
plots.append(p)

#### v_i1_0
#p = plot.Plot1D()
#
#p.initialize("rfsr", "v_i1_0", "rfsr_v_i1_0")
#p.labels(x="v_i1_0", y = "")
#p.xax(0.01, 0.35, 0.5)
#p.doLogY = True
#p.yax(0.01, 100000)
#p.setDoubleRatioCanvas(p.name)
#plots.append(p)
#


