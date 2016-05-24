import sys
sys.path.append(os.environ['SUSYDIR'])
import supersusy.utils.plot as plot
import supersusy.utils.background as background
import supersusy.utils.region as region


###########################
## signal sample
###########################
rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0222/may23/mc/Raw/"
#rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0222/apr17/sigB/Raw_May18/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0222val/filelists/"


sf_ = 1.0

#signal_ = background.Background("sig_250_160", "(250,160)")
#signal_.setSignal()
#signal_.scale_factor = sf_
#signal_.set_chain_from_list_CONDOR(filelist_dir + "bwn_new/", rawdir, "387943")

#signal_ = background.Background("sig_350_200", "(350,200)")
#signal_.setSignal()
#signal_.scale_factor = sf_
#signal_.set_chain_from_list_CONDOR(filelist_dir + "bwn_new/", rawdir, "387953")

signal_ = background.Background("sig_300_150", "(300,150)")
signal_.setSignal()
signal_.scale_factor = sf_
signal_.set_chain_from_list_CONDOR(filelist_dir + "bwn_new/", rawdir, "387947")

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
p.yax(0.1, 1e5)
p.doLogY = True
p.setRatioCanvas(p.name)
plots_.append(p)


p = plot.Plot1D()
p.initialize(run_reg, "RPT", "RPT_%s"%run_reg)
p.labels(x="R_{pT}",y="Entries")
p.xax(0.05, 0, 1)
p.yax(0.1, 1e5)
p.doLogY = True
p.setRatioCanvas(p.name)
plots_.append(p)

p = plot.Plot1D()
p.initialize(run_reg, "DPB_vSS", "DPB_%s"%run_reg)
p.labels(x="#Delta#phi_{#beta}^{R}",y="Entries")
p.xax(0.1, 0, 3.2)
p.yax(0.1, 1e5)
p.doLogY = True
p.setRatioCanvas(p.name)
plots_.append(p)

p = plot.Plot1D()
p.initialize(run_reg, "gamInvRp1", "GAM_%s"%run_reg)
p.labels(x="1/#gamma",y="Entries")
p.xax(0.05, 0, 1)
p.yax(0.1, 1e5)
p.doLogY = True
p.setRatioCanvas(p.name)
plots_.append(p)

p = plot.Plot1D()
p.initialize(run_reg, "cosThetaB", "COS_%s"%run_reg)
p.labels(x="cos#theta_{b}",y="Entries")
p.xax(0.1, -1, 1)
p.yax(0.1, 1e5)
p.doLogY = True
p.setRatioCanvas(p.name)
plots_.append(p)

p = plot.Plot1D()
p.initialize(run_reg, "nBJets", "nBJets_%s"%run_reg)
p.labels(x="b-Jet Multiplicity",y="Entries")
p.xax(1, 0, 10)
p.yax(0.1, 1e5)
p.doLogY = True
p.setRatioCanvas(p.name)
plots_.append(p)

p = plot.Plot1D()
p.initialize(run_reg, "nSJets", "nSJets_%s"%run_reg)
p.labels(x="Signal (non-b) Jet Multiplicity",y="Entries")
p.xax(1, 0, 10)
p.yax(0.1, 1e5)
p.doLogY = True
p.setRatioCanvas(p.name)
plots_.append(p)

p = plot.Plot1D()
p.initialize(run_reg, "l_pt[0]", "pt0_%s"%run_reg)
p.labels(x="Leading lepton p_{T} [GeV]",y="Entries")
p.xax(5, 0, 200)
p.yax(0.1, 1e5)
p.doLogY = True
p.setRatioCanvas(p.name)
plots_.append(p)

p = plot.Plot1D()
p.initialize(run_reg, "l_pt[1]", "pt1_%s"%run_reg)
p.labels(x="Sub-leading lepton p_{T} [GeV]",y="Entries")
p.xax(5, 0, 200)
p.yax(0.1, 1e5)
p.doLogY = True
p.setRatioCanvas(p.name)
plots_.append(p)

p = plot.Plot1D()
p.initialize(run_reg, "sj_pt[0]", "sjpt0_%s"%run_reg)
p.labels(x="Lead signal (non-b) jet p_{T} [GeV]",y="Entries")
p.xax(5, 0, 200)
p.yax(0.1, 1e5)
p.doLogY = True
p.setRatioCanvas(p.name)
plots_.append(p)

p = plot.Plot1D()
p.initialize(run_reg, "bj_pt[0]", "bjpt0_%s"%run_reg)
p.labels(x="Lead b-jet p_{T} [GeV]",y="Entries")
p.xax(5, 0, 200)
p.yax(0.1, 1e5)
p.doLogY = True
p.setRatioCanvas(p.name)
plots_.append(p)











