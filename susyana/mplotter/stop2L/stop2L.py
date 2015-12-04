
import sys
sys.path.append('../../../../../')
import supersusy.utils.mplot as mplot
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region


#############################################
# Set up the samples
#############################################
rawdir = "/data/uclhc/uci/user/dantrim/ntuples/rjigsaw/mc/Raw/"
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/rjigsaw/data/Raw/"
#filelist_dir = "/data/uclhc/uci/user/dantrim/n0216val/fine_filelists/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0216val/filelists/"
backgrounds = []

#### MC
# Zjets
zjets = background.Background("zjets", "Z+jets (PowHeg)")
zjets.scale_factor = 1.96
zjets.set_color(r.TColor.GetColor("#85DC6E"))
zjets.set_treename("zjets_powheg")
zjets.set_chain_from_list_CONDOR(filelist_dir + "zjets_powheg/", rawdir)
backgrounds.append(zjets)

# diboson
diboson = background.Background("diboson", "VV (Sherpa)")
diboson.scale_factor = 1.96
diboson.set_color(r.TColor.GetColor("#49C2F9"))
diboson.set_treename("diboson_sherpa")
diboson.set_chain_from_list_CONDOR(filelist_dir + "diboson_sherpa/", rawdir)
backgrounds.append(diboson)

# single top
st = background.Background("singletop", "Single top + Wt")
st.scale_factor = 1.96
st.set_color(r.TColor.GetColor("#DC101C"))
st.set_treename("singletop")
st.set_chain_from_list_CONDOR(filelist_dir + "singletop/", rawdir)
backgrounds.append(st)

# ttbar
ttbar = background.Background("ttbar", "t#bar{t}")
ttbar.scale_factor = 1.96
ttbar.set_color(r.TColor.GetColor("#F91628"))
ttbar.set_treename("ttbar")
ttbar.set_chain_from_list_CONDOR(filelist_dir + "ttbar/", rawdir)
backgrounds.append(ttbar)

# wjets
wjets = background.Background("wjets_powheg", "W+jets (PowHeg)")
wjets.scale_factor = 1.96
wjets.set_color(r.TColor.GetColor("#619BD4"))
wjets.set_treename("wjets_powheg")
wjets.set_chain_from_list_CONDOR(filelist_dir + "wjets_powheg/", rawdir)
backgrounds.append(wjets)

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
reg.simplename = "SR"
reg.displayname = "Stop-2#it{l} WW-like SR"
reg.tcut = "nLeptons==2 && nMuons==1 && nElectrons==1 && nBJets==0 && l_pt[0]>20 && l_pt[1]>20 && RPT>0.6 && DPB_vSS>2.0 && mt2>90"
regions.append(reg)

reg = region.Region()
reg.simplename = "CRT"
reg.displayname = "Stop-2#it{l} WW-like CRT"
reg.tcut = "nLeptons==2 && nMuons==1 && nElectrons==1 && nBJets>0 && l_pt[0]>20 && l_pt[1]>20 && RPT>0.6 && DPB_vSS<2.0 && mt2>30"
regions.append(reg)

reg = region.Region()
reg.simplename = "CRW"
reg.displayname = "Stop-2#it{l} WW-like CRW"
reg.tcut = "nLeptons==2 && nMuons==1 && nElectrons==1 && nBJets==0 && l_pt[0]>20 && l_pt[1]>20 && RPT<0.2 && DPB_vSS<2.0 && mt2>20"
regions.append(reg)

reg = region.Region()
reg.simplename = "VRT"
reg.displayname = "Stop-2#it{l} WW-like VRT"
reg.tcut = "nLeptons==2 && nMuons==1 && nElectrons==1 && nBJets==0 && l_pt[0]>20 && l_pt[1]>20 && RPT>0.6 && DPB_vSS<2.0 && mt2>30"
regions.append(reg)

reg = region.Region()
reg.simplename = "VRW"
reg.displayname = "Stop-2#it{l} WW-like VRW"
reg.tcut = "nLeptons==2 && nMuons==1 && nElectrons==1 && nBJets==0 && l_pt[0]>20 && l_pt[1]>20 && RPT<0.4 && DPB_vSS>2.0 && mt2>20"
regions.append(reg)


reg = region.Region()
reg.simplename = "wwPre"
reg.displayname = "wwPre (DFOS incl)"
reg.tcut = "nLeptons==2 && nMuons==1 && nElectrons==1 && nSJets>=0 && nBJets==0 && (l_q[0]*l_q[1])<1 && l_pt[0]>20 && l_pt[1]>20"
regions.append(reg)

#############################################
# Set up the plots
#############################################

plots = []

logy = 100000

sas = ["ttbar", "diboson"]
reg = "wwPre"

for sa in sas :
    print "BLAH"
    p = mplot.mJointPlot()
    p.initialize(reg, "RPT", "DPB_vSS", reg + "_" + sa + "_RPT_DPB_Joint")
    p.set_title("RPT vs. DPB (sample: %s)"%sa)
    p.set_sample(sa)
    p.set_labels(x="RPT", y="DPB")
    p.xax(0, 1)
    p.yax(0, 3.2)
    p.kind = "kde"
    #p.cmap = "cubehelix" 
    p.cmap = "blues"
    plots.append(p)
    

  
