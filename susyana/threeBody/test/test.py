import sys
sys.path.append(os.environ['SUSYDIR'])
import supersusy.utils.plot as plot
import supersusy.utils.background as background
import supersusy.utils.region as region


###########################
## signal sample
###########################
rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0222/apr17/sigB/Raw_May18/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0222val/filelists/"


sf_ = 1.0

signal_ = background.Background("sig_250_160", "(250,160)")
signal_.scale_factor = sf_
signal_.set_chain_from_list_CONDOR(filelist_dir + "bwn_new/", rawdir, "387943")

isEE = "(nElectrons==2 && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0"
isMM = "(nMuons==2 && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0" 
isSF = "((nMuons==2 || nElectrons==2) && abs(mll-91.2)>10) && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"
isDF = "(nElectrons==1 && nMuons==1) && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"

region_ = region.Region()
region_.name = "dfpresel"
region_.displayname = "DF Preselection"
region_.tcut = "nLeptons==2 && " + isDF


run_reg = "dfpresel"


plots_ = []

p = plot.Plot1D()
p.initialize(run_reg, "MDR", "MDR_%s"%run_reg)
p.labels(x="MDR",y="Entries")
p.xax(8, 0, 250)
p.yax(0.1, 1e7)
p.doLogY = True
p.setRatioCanvas(p.name)
plots_.append(p)
