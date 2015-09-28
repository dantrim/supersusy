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


#### DATA
data = background.Data()
data.set_color(r.kBlack)
data.set_treename("Data")
data.set_chain_from_list(filelist_dir + "data15_periodA_n0213.txt", data_rawdir)


#################################################
## Set up the regions
#################################################
regions = []
#reg = region.Region("test", "TEST")
#reg.tcut = "nLeptons==2 && nMuons==1 && nElectrons==1"
#regions.append(reg)


#//reg = region.Region()
#//reg.simplename = "wwpre"
#//reg.displayname = "WW-pre (DFOS-20)"
#//reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"
#//regions.append(reg)

#reg = region.Region()
#reg.simplename = "wwpre"
#reg.displayname = "WW-pre CR"
#reg.tcut = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && nBJets==0"
#regions.append(reg)

## CRT
#reg = region.Region("stopCRT", "CRT-test (DPB<2, RPT>0.6)")
#reg.setCutFlow()
#reg.addCut("Exactly 2 leptons", "nLeptons==2")
#reg.addCut("DF", "nElectrons==1 && nMuons==1")
#reg.addCut("OS", "(l_q[0]*l_q[1])<0")
#reg.addCut("Lepton pT > 20 GeV", "l_pt[0]>20 && l_pt[1]>20")
##reg.addCut("B-Veto", "nBJets==0")
#reg.addCut("mt2>30", "mt2>30")
#reg.addCut("DPB_vTT<2", "DPB_vTT_0 < 2")
#reg.addCut("RPT_0>0.6", "RPT_0 > 0.6")
#regions.append(reg)

## CRW
reg = region.Region("stopCRW", "CRW-test (DPB>2, RPT<0.3)")
reg.setCutFlow()
reg.addCut("Exactly 2 leptons", "nLeptons==2")
reg.addCut("DF", "nElectrons==1 && nMuons==1")
reg.addCut("OS", "(l_q[0]*l_q[1])<0")
reg.addCut("Lepton pT > 20 GeV", "l_pt[0]>20 && l_pt[1]>20")
reg.addCut("B-Veto", "nBJets==0")
reg.addCut("mt2>20", "mt2>20")
reg.addCut("DPB_vTT>0 && DPB_vTT<2", "(DPB_vTT_0 > 0 && DPB_vTT_0 <2)")
reg.addCut("RPT_0<0.2", "RPT_0 < 0.2")
regions.append(reg)


plots = []
samples = ["ww"] #, "ttbar", "bwn_250_160"]
for samp in samples :


    p = plot.Plot2D()
    p.initialize("wwpre", "RPT_0", "DPB_vTT_0", "wwpre_RPT_DPB_vTT_%s_2d"%samp)
    p.labels(x="RPT", y = "DPB_vTT")
    p.set_sample(samp)
    p.xax(0.05, 0, 1)
    p.yax(0.1, 0, 3.2)
    p.defaultCanvas()
    plots.append(p)

    
    p = plot.Plot2D()
    p.initialize("wwpre", "RPT_0", "mt2", "wwpre_RPT_mt2_%s_2d"%samp)
    p.labels(x="RPT", y = "mt2")
    p.set_sample(samp)
    p.xax(0.05, 0, 1)
    p.yax(5, 0, 200)
    p.defaultCanvas()
    plots.append(p)

    p = plot.Plot2D()
    p.initialize("wwpre", "DPB_vTT_0", "mt2", "wwpre_DPB_vTT_mt2_%s_2d"%samp)
    p.labels(x="DPB_vTT", y = "mt2")
    p.set_sample(samp)
    p.xax(0.1, 0, 3.2)
    p.yax(5, 0, 200)
    p.defaultCanvas()
    plots.append(p)

#    p = plot.Plot2D()
#    p.initialize("wwpre", "COS_tt_0", "DPB_vTT_0", "wwpre_COS_tt_DPB_vTT_%s_2d"%samp)
#    p.labels(x="COS_tt", y = "DPB_vTT")
#    p.set_sample(samp)
#    p.xax(0.05, -1, 1)
#    p.yax(0.01, 0, 3.2)
#    p.defaultCanvas()
#    plots.append(p)
#
#    p = plot.Plot2D()
#    p.initialize("wwpre", "abs(cosThetaB)", "DPB_vTT_0", "wwpre_cosThetaB_DPB_vTT_%s_2d"%samp)
#    p.labels(x="|cosThetaB|", y = "DPB_vTT")
#    p.set_sample(samp)
#    p.xax(0.01, 0, 1)
#    p.yax(0.01, 0, 3.2)
#    p.defaultCanvas()
#    plots.append(p)
#
##    ###### COS_t1_0
##    ## vs COS_tt_0
##    p = plot.Plot2D()
##    p.initialize("wwpre", "COS_t1_0", "COS_tt_0", "wwpre_COS_t1_COS_tt_%s_2d"%samp)
##    p.labels(x="COS_t1", y = "COS_tt")
##    p.set_sample(samp)
##    p.xax(0.05, -1, 1)
##    p.yax(0.05, -1, 1)
##    p.defaultCanvas()
##    plots.append(p)
##
##    ## vs cosThetaB
##    p = plot.Plot2D()
##    p.initialize("wwpre", "COS_t1_0", "cosThetaB", "wwpre_COS_t1_cosThetaB_%s_2d"%samp)
##    p.labels(x="COS_t1", y = "cosThetaB")
##    p.set_sample(samp)
##    p.xax(0.05, -1, 1)
##    p.yax(0.05, -1, 1)
##    p.defaultCanvas()
##    plots.append(p)
##
##    ## vs DPB_vTT
##    p = plot.Plot2D()
##    p.initialize("wwpre", "COS_t1_0", "DPB_vTT_0", "wwpre_COS_t1_DPB_vTT_%s_2d"%samp)
##    p.labels(x="COS_t1", y = "DPB_vTT")
##    p.set_sample(samp)
##    p.xax(0.05, -1, 1)
##    p.yax(0.1, 0, 3.2)
##    p.defaultCanvas()
##    plots.append(p)
##
##    ## vs DPD_lab_tt
##    p = plot.Plot2D()
##    p.initialize("wwpre", "COS_t1_0", "DPD_lab_tt_0", "wwpre_COS_t1_DPD_lab_tt_%s_2d"%samp)
##    p.labels(x="COS_t1", y = "DPD_lab_tt")
##    p.set_sample(samp)
##    p.xax(0.05, -1, 1)
##    p.yax(0.1, 0, 6.4)
##    p.defaultCanvas()
##    plots.append(p)
##
##    ## gamma_rp1
##    p = plot.Plot2D()
##    p.initialize("wwpre", "COS_t1_0", "gamma_rp1_0", "wwpre_COS_t1_gamma_rp1_%s_2d"%samp)
##    p.labels(x="COS_t1", y = "gamma_rp1")
##    p.set_sample(samp)
##    p.xax(0.05, -1, 1)
##    p.yax(0.01, 0, 1)
##    p.defaultCanvas()
##    plots.append(p)
##
##    ## vs RPT
##    p = plot.Plot2D()
##    p.initialize("wwpre", "COS_t1_0", "RPT_0", "wwpre_COS_t1_RPT_%s_2d"%samp)
##    p.labels(x="COS_t1", y = "RPT")
##    p.set_sample(samp)
##    p.xax(0.05, -1, 1)
##    p.yax(0.01, 0, 1)
##    p.defaultCanvas()
##    plots.append(p)
##
##    ## vs RPZ
##    p = plot.Plot2D()
##    p.initialize("wwpre", "COS_t1_0", "RPZ_0", "wwpre_COS_t1_RPZ_%s_2d"%samp)
##    p.labels(x="COS_t1", y = "RPZ")
##    p.set_sample(samp)
##    p.xax(0.05, -1, 1)
##    p.yax(0.01, 0, 1.5)
##    p.defaultCanvas()
##    plots.append(p)
##
##    ## vs DPD_tt_t1
##    p = plot.Plot2D()
##    p.initialize("wwpre", "COS_t1_0", "DPD_tt_t1_0", "wwpre_COS_t1_DPD_t1_%s_2d"%samp)
##    p.labels(x="COS_t1", y = "DPD_t1")
##    p.set_sample(samp)
##    p.xax(0.05, -1, 1)
##    p.yax(0.01, 0, 6.4)
##    p.defaultCanvas()
##    plots.append(p)
##
##    ## vs shat_0
##    p = plot.Plot2D()
##    p.initialize("wwpre", "COS_t1_0", "shat_0", "wwpre_COS_t1_shat_%s_2d"%samp)
##    p.labels(x="COS_t1", y = "shat_0")
##    p.set_sample(samp)
##    p.xax(0.05, -1, 1)
##    p.yax(40, 0, 1200)
##    p.defaultCanvas()
##    plots.append(p)
##
##
##    ############# RPT
##    ## vs DPB_vTT_0
##    p = plot.Plot2D()
##    p.initialize("wwpre", "RPT_0", "DPB_vTT_0", "wwpre_RPT_DPB_vTT_%s_2d"%samp)
##    p.labels(x="RPT", y = "DPB_vTT")
##    p.set_sample(samp)
##    p.xax(0.05, -1, 1)
##    p.yax(0.1, 0, 3.2)
##    p.defaultCanvas()
##    plots.append(p)
##
##    ## vs v_i1_0
##    p = plot.Plot2D()
##    p.initialize("wwpre", "RPT_0", "v_i1_0", "wwpre_RPT_v_i1_%s_2d"%samp)
##    p.labels(x="RPT", y = "v_i1")
##    p.set_sample(samp)
##    p.xax(0.05, -1, 1)
##    p.yax(0.005, 0.45, 0.5)
##    p.defaultCanvas()
##    plots.append(p)
##
##    ## vs gamma_rp1_0
##    p = plot.Plot2D()
##    p.initialize("wwpre", "RPT_0", "gamma_rp1_0", "wwpre_RPT_gamma_rp1_%s_2d"%samp)
##    p.labels(x="RPT", y = "gamma_rp1")
##    p.set_sample(samp)
##    p.xax(0.05, -1, 1)
##    p.yax(0.01, 0, 1)
##    p.defaultCanvas()
##    plots.append(p)
##
##    ## vs COS_tt
##    p = plot.Plot2D()
##    p.initialize("wwpre", "RPT_0", "COS_tt_0", "wwpre_RPT_COS_tt_%s_2d"%samp)
##    p.labels(x="RPT", y = "COS_tt")
##    p.set_sample(samp)
##    p.xax(0.05, -1, 1)
##    p.yax(0.05, -1,1)
##    p.defaultCanvas()
##    plots.append(p)
##
##    ## vs cosThetB
##    p = plot.Plot2D()
##    p.initialize("wwpre", "RPT_0", "abs(cosThetaB)", "wwpre_RPT_cosThetaB_%s_2d"%samp)
##    p.labels(x="RPT", y = "|cosThetaB|")
##    p.set_sample(samp)
##    p.xax(0.05, -1, 1)
##    p.yax(0.05, 0, 1)
##    p.defaultCanvas()
##    plots.append(p)
##
##    ########################
##    ## DPD_tt_t1
##    # vs DPD_tt_t2
##    p = plot.Plot2D()
##    p.initialize("wwpre", "DPD_tt_t1_0", "DPD_tt_t2_0", "wwpre_DPD_tt_t1_DPD_tt_t2_%s_2d"%samp)
##    p.labels(x="DPD_tt_t1", y = "DPD_tt_t2")
##    p.set_sample(samp)
##    p.xax(0.1, 0, 6.4)
##    p.yax(0.1, 0, 6.4)
##    p.defaultCanvas()
##    plots.append(p)
##
##    ## vs gamma_rp1
##    p = plot.Plot2D()
##    p.initialize("wwpre", "DPD_tt_t1_0", "gamma_rp1_0", "wwpre_DPD_tt_t1_gamma_rp1_%s_2d"%samp)
##    p.labels(x="DPD_tt_t1", y = "gamma_rp1")
##    p.set_sample(samp)
##    p.xax(0.1, 0, 6.4)
##    p.yax(0.01, 0, 2.2)
##    p.defaultCanvas()
##    plots.append(p)
##
##    ## vs RPT
##    p = plot.Plot2D()
##    p.initialize("wwpre", "DPD_tt_t1_0", "RPT_0", "wwpre_DPD_tt_t1_RPT_0_%s_2d"%samp)
##    p.labels(x="DPD_tt_t1", y = "RPT_0")
##    p.set_sample(samp)
##    p.xax(0.1, 0, 6.4)
##    p.yax(0.01, 0, 1)
##    p.defaultCanvas()
##    plots.append(p)
##
##    ## vs COS_tt
##    p = plot.Plot2D()
##    p.initialize("wwpre", "DPD_tt_t1_0", "COS_tt_0", "wwpre_DPD_tt_t1_COS_tt_%s_2d"%samp)
##    p.labels(x="DPD_tt_t1", y = "COS_tt")
##    p.set_sample(samp)
##    p.xax(0.1, 0, 6.4)
##    p.yax(0.01, -1, 1)
##    p.defaultCanvas()
##    plots.append(p)
##
##
##    
##    
##
##    
##
##
###    ##################################
###    ### R2
###
###    ## DPB vs R2
###    p = plot.Plot2D()
###    p.initialize("wwpre", "DPB", "R2", "wwpre_DPB_R2_%s_2d"%samp)
###    p.labels(x="dpb", y="r2")
###    p.set_sample(samp)
###    p.xax(0.1, 0, 3.2)
###    p.yax(0.05, 0, 1)
###    p.defaultCanvas()
###    plots.append(p)
###
###    ## cosThetaB vs R2
###    p = plot.Plot2D()
###    p.initialize("wwpre", "abs(cosThetaB)", "R2", "wwpre_cosThetaB_R2_%s_2d"%samp)
###    p.labels(x="|cos#theta_{b}|", y="R_{2}")
###    p.set_sample(samp)
###    p.xax(0.05, 0, 1)
###    p.yax(0.05, 0, 1)
###    p.defaultCanvas()
###    plots.append(p)
###
###    ## mt2 vs R2
###    p = plot.Plot2D()
###    p.initialize("wwpre", "mt2", "R2", "wwpre_mt2_R2_%s_2d"%samp)
###    p.labels(x="mt2", y="R_{2}")
###    p.set_sample(samp)
###    p.xax(5, 0, 100)
###    p.yax(0.05, 0, 1)
###    p.defaultCanvas()
###    plots.append(p)
###
###    ## MDR vs R2
###    p = plot.Plot2D()
###    p.initialize("wwpre", "MDR", "R2", "wwpre_MDR_R2_%s_2d"%samp)
###    p.labels(x="M_{#Delta}^{R} [GeV]", y="R_{2}")
###    p.set_sample(samp)
###    p.xax(5, 0, 100)
###    p.yax(0.05, 0, 1)
###    p.defaultCanvas()
###    plots.append(p)
###
###    ## nBJets vs R2
###    p = plot.Plot2D()
###    p.initialize("wwpre", "nBJets", "R2", "wwpre_nBJets_R2_%s_2d"%samp)
###    p.labels(x="Number of b-jets", y = "R_{2}")
###    p.set_sample(samp)
###    p.xax(1, 0, 6)
###    p.yax(0.05, 0, 1)
###    p.defaultCanvas()
###    plots.append(p)
###
###    ##################################
###    ## DPB
###
###    ## DPB vs cosThetaB
###    p = plot.Plot2D()
###    p.initialize("wwpre", "DPB", "abs(cosThetaB)", "wwpre_DPB_cosThetaB_%s_2d"%samp)
###    p.labels(x="#Delta#phi_{#beta}^{R}", y = "|cos#theta_{b}|")
###    p.set_sample(samp)
###    p.xax(0.1, 0, 3.2)
###    p.yax(0.05, 0, 1)
###    p.defaultCanvas()
###    plots.append(p)
###
###    ## DPB vs mt2
###    p = plot.Plot2D()
###    p.initialize("wwpre", "DPB", "mt2", "wwpre_DPB_mt2_%s_2d"%samp)
###    p.labels(x="#Delta#phi_{#beta}^{R}", y = "m_{T2} [GeV]")
###    p.set_sample(samp)
###    p.xax(0.1, 0, 3.2)
###    p.yax(5, 0, 100)
###    p.defaultCanvas()
###    plots.append(p)
###
###    ## DPB vs MDR
###    p = plot.Plot2D()
###    p.initialize("wwpre", "DPB", "MDR", "wwpre_DPB_MDR_%s_2d"%samp)
###    p.labels(x="#Delta#phi_{#beta}^{R}", y = "M_{#Delta}^{R} [GeV]")
###    p.set_sample(samp)
###    p.xax(0.1, 0, 3.2)
###    p.yax(5, 0, 100)
###    p.defaultCanvas()
###    plots.append(p)
###
###    ## DPB vs nBJets
###    p = plot.Plot2D()
###    p.initialize("wwpre", "DPB", "nBJets", "wwpre_DPB_nBJets_%s_2d"%samp)
###    p.labels(x="#Delta#phi_{#beta}^{R}", y = "Number of b-jets")
###    p.set_sample(samp)
###    p.xax(0.1, 0, 3.2)
###    p.yax(1, 0, 6)
###    p.defaultCanvas()
###    plots.append(p)
###
###    ##################################
###    ## mt2
###
###    ## mt2 vs cosThetaB
###    p = plot.Plot2D()
###    p.initialize("wwpre", "mt2", "abs(cosThetaB)", "wwpre_mt2_cosThetaB_%s_2d"%samp)
###    p.labels(x="m_{T2} [GeV]", y = "|cos#theta_{b}|")
###    p.set_sample(samp)
###    p.xax(5, 0, 100)
###    p.yax(0.05, 0, 1)
###    p.defaultCanvas()
###    plots.append(p)
###
###    ## mt2 vs nBJets
###    p = plot.Plot2D()
###    p.initialize("wwpre", "mt2", "nBJets", "wwpre_mt2_nBJets_%s_2d"%samp)
###    p.labels(x="m_{T2} [GeV]", y = "Number of b-jets")
###    p.set_sample(samp)
###    p.xax(5, 0, 100)
###    p.yax(1, 0, 6)
###    p.defaultCanvas()
###    plots.append(p)
###
###    #####################################
###    ## cosThetaB
###
###    ## MDR vs cosThetaB
###    p = plot.Plot2D()
###    p.initialize("wwpre", "MDR", "abs(cosThetaB)", "wwpre_MDR_cosThetaB_%s_2d"%samp)
###    p.labels(x="M_{#Delta}^{R} [GeV]", y = "|cos#theta_{b}|")
###    p.set_sample(samp)
###    p.xax(5, 0, 100)
###    p.yax(0.05, 0, 1)
###    p.defaultCanvas()
###    plots.append(p)
###
###    ## nBJets vs cosThetaB
###    p = plot.Plot2D()
###    p.initialize("wwpre", "nBJets", "abs(cosThetaB)", "wwpre_nBJets_cosThetaB_%s_2d"%samp)
###    p.labels(x="Number of b-jets", y = "|cos#theta_{b}|")
###    p.set_sample(samp)
###    p.xax(1,0,6)
###    p.yax(0.05, 0, 1)
###    p.defaultCanvas()
###    plots.append(p)
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
