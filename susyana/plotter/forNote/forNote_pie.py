import sys
sys.path.append(os.environ['SUSYDIR'])
import supersusy.utils.plot as plot
import supersusy.utils.background as background
import supersusy.utils.region as region
import supersusy.utils.systematic as systematic


#######################################
# samples
########################################
backgrounds = []
rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0222/apr17/mc/Raw/"
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0222/nom/data/Raw/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0222val/filelists/"


lumi_ = [1.0]
lumi_val = 0

######## MC
# ttbro
ttbar = background.Background("ttbar", "t#bar{t}")
ttbar.set_debug()
ttbar.scale_factor = lumi_[lumi_val]
ttbar.set_fillStyle(0)
ttbar.setLineStyle(1)
ttbar.set_color("#FC0D1B")
ttbar.set_treename("ttbar_powheg")
ttbar.set_chain_from_list_CONDOR(filelist_dir+ "ttbar/", rawdir)
backgrounds.append(ttbar)

# singletop
stop = background.Background("st", "Single top")
stop.set_debug()
stop.scale_factor = lumi_[lumi_val]
stop.set_fillStyle(0)
stop.setLineStyle(1)
stop.set_color("#DE080C")
stop.set_treename("ST")
stop.set_chain_from_list_CONDOR(filelist_dir+ "singletop/", rawdir)
backgrounds.append(stop)

# diboson
diboson = background.Background("vv", "VV (Sherpa)")
diboson.set_debug()
diboson.scale_factor = lumi_[lumi_val]
diboson.set_fillStyle(0)
diboson.setLineStyle(1)
diboson.set_color("#41C1FC")
diboson.set_treename("diboson_sherpa")
diboson.set_chain_from_list_CONDOR(filelist_dir+ "diboson_sherpa/", rawdir)
backgrounds.append(diboson)


# Zjets
zjets = background.Background("zjets", "Z+jets (Sherpa)")
zjets.set_debug()
zjets.scale_factor = lumi_[lumi_val]
zjets.set_fillStyle(0)
zjets.setLineStyle(1)
zjets.set_color("#FFEF53")
zjets.set_treename("zjets_sherpa")
zjets.set_chain_from_list_CONDOR(filelist_dir+ "zjets_sherpa/", rawdir)
backgrounds.append(zjets)

# Wjets
wjets = background.Background("wjets", "W+Jets (Sherpa)")
wjets.set_debug()
wjets.scale_factor = lumi_[lumi_val]
wjets.set_fillStyle(0)
wjets.setLineStyle(1)
wjets.set_color("#5E9AD6")
wjets.set_treename("wjets")
wjets.set_chain_from_list_CONDOR(filelist_dir+ "wjets_sherpa/", rawdir)
backgrounds.append(wjets)

#sig1 = background.Background("bwn250_160", "(250,160)")
#sig1.setSignal()
#sig1.set_debug()
#sig1.scale_factor = lumi_[lumi_val]
#sig1.set_fillStyle(0)
#sig1.setLineStyle(2)
#sig1.set_color(r.kBlue)
#sig1.set_treename("sig1")
#sig1.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", rawdir, "406009")
#backgrounds.append(sig1)
#
#sig2 = background.Background("bwn300_180", "(300,180)")
#sig2.setSignal()
#sig2.set_debug()
#sig2.scale_factor = lumi_[lumi_val]
#sig2.setLineStyle(2)
#sig2.set_color(r.kGreen)
#sig2.set_treename("sig2")
#sig2.set_chain_from_list_CONDOR(filelist_dir+ "bwn/", rawdir, "406011")
#backgrounds.append(sig2)
#
#sig3 = background.Background("bwn300_150", "(300,150)")
#sig3.setSignal()
#sig3.set_debug()
#sig3.scale_factor = lumi_[lumi_val]
#sig3.setLineStyle(2)
#sig3.set_color(r.kBlack)
#sig3.set_treename("sig3")
#sig3.set_chain_from_list_CONDOR(filelist_dir + "bwn/", rawdir, "406010")
#backgrounds.append(sig3)


##### DATA
#data = background.Data()
#data.set_color(r.kBlack)
#data.set_treename("Data")
#data.set_chain_from_list_CONDOR(filelist_dir + "n0222_data/", data_rawdir)



##########################################
# regions
##########################################
regions = []

isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && l_pt[0]>20 && l_pt[1]>20 && (l_q[0]*l_q[1])<0"

reg = region.Region()
reg.name = "crv"
reg.displayname = "CR-VV"
reg.tcut = isDFOS + " && nSJets==0 && nBJets==0 && MDR>30 && RPT<0.5 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && DPB_vSS>(0.85*abs(cosThetaB)+1)"
regions.append(reg)

reg = region.Region()
reg.name = "vrv"
reg.displayname = "VR-VV"
reg.tcut = isDFOS + " && nSJets==0 && nBJets==0 && MDR>30 && RPT<0.5 && DPB_vSS>(0.85*abs(cosThetaB)+1.8)"
regions.append(reg)

reg = region.Region()
reg.name = "crt"
reg.displayname = "CR-T"
reg.tcut = isDFOS + " && nSJets>=0 && nBJets>0 && MDR>30 && RPT>0.5 && DPB_vSS<(0.85*abs(cosThetaB)+1.8)"
regions.append(reg)

reg = region.Region()
reg.name = "vrt"
reg.displayname = "VR-T"
reg.tcut = isDFOS + " && nSJets>0 && nBJets==0 && MDR>30 && RPT<0.5 && DPB_vSS>(0.85*abs(cosThetaB)+1.8)"
regions.append(reg)




