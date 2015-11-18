
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
rnames = []
reg = region.Region()
reg.simplename = "zpeak_ee_inc"
reg.displayname = "Z #rightarrow ee (nJ>=0 nB=0)"
reg.tcut = "nLeptons==2 && nElectrons==2 && nSJets>=0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<1 && abs(mll-91.2)<20"
regions.append(reg)
#rnames.append(reg.simplename)


reg = region.Region()
reg.simplename = "zpeak_ee_0j"
reg.displayname = "Z #rightarrow ee (nJ==0 nB=0)"
reg.tcut = "nLeptons==2 && nElectrons==2 && nSJets==0 && nBJets==0 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<1 && abs(mll-91.2)<20"
regions.append(reg)
#rnames.append(reg.simplename)

reg = region.Region()
reg.simplename = "gte2l_0j"
reg.displayname = ">=2 leptons (nJ==0 nB==0)"
reg.tcut = "nLeptons>=2 && nSJets==0 && nBJets==0"
regions.append(reg)
rnames.append(reg.simplename)

reg = region.Region()
reg.simplename = "gte2l_inc"
reg.displayname = ">=2 leptons (nJ>=0 nB==0)"
reg.tcut = "nLeptons>=2 && nSJets>=0 && nBJets==0" 
regions.append(reg)
rnames.append(reg.simplename)

#############################################
# Set up the plots
#############################################

plots = []

#### zpeak_mm_0j
logy = 1000000000
#region = "zpeak_mm_inc"


for x in range(2) :
    pref_x = ""
    if x == 0 :
        pref_x = "lead "
    elif x == 1 :
        pref_x = "sub-lead "
    for region in rnames : 

        p = plot.Plot1D()
        p.initialize(region, "l_ptvarcone20[%s]/l_pt[%s]"%(str(x),str(x)), "%s_RELptvarcone20_%s"%(region,str(x)))
        x_ = pref_x + "ptvarcone20/pt"
        p.labels(x = x_, y = "Entries / 0.01")
        p.xax(0.01, 0, 0.2)
        p.yax(0.1, logy)
        p.doLogY = True
        p.setRatioCanvas(p.name)
        plots.append(p)

        p = plot.Plot1D()
        p.initialize(region, "l_ptvarcone30[%s]/l_pt[%s]"%(str(x), str(x)), "%s_RELptvarcone30_%s"%(region,str(x)))
        x_ = pref_x + "ptvarcone30/pt"
        p.labels(x = x_, y = "Entries / 0.01")
        p.xax(0.01, 0, 0.2)
        p.yax(0.1, logy)
        p.doLogY = True
        p.setRatioCanvas(p.name)
        plots.append(p)

        p = plot.Plot1D()
        p.initialize(region, "l_etconetopo20[%s]/l_pt[%s]"%(str(x), str(x)), "%s_RELetconetopo20_%s"%(region,str(x)))
        x_ = pref_x + "etconetopo20/pt"
        p.labels(x = x_, y = "Entries / 0.01")
        p.xax(0.01, 0, 0.2)
        p.yax(0.1, logy)
        p.doLogY = True
        p.setRatioCanvas(p.name)
        plots.append(p)

        p = plot.Plot1D()
        p.initialize(region, "l_etconetopo30[%s]/l_pt[%s]"%(str(x),str(x)), "%s_RELetconetopo30_%s"%(region,str(x)))
        x_ = pref_x + "etconetopo30/pt"
        p.labels(x = x_, y = "Entries / 0.05")
        p.xax(0.05, 0, 1)
        p.yax(0.1, logy)
        p.doLogY = True
        p.setRatioCanvas(p.name)
        plots.append(p)
