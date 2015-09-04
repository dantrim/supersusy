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
ttbar.set_treename("ttbar_powheg")
ttbar.set_chain_from_list(filelist_dir + "ttbar_powheg_n0213.txt", rawdir)
backgrounds.append(ttbar)


sig = background.Background("sig", "SIG")
sig.setSignal()
sig.set_debug()
sig.scale_factor = 1.0
sig.set_treename("sig")
sig.set_chain_from_list(filelist_dir + "bwn_406009_n0213.txt", rawdir)
backgrounds.append(sig)


#################################################
## Set up the regions
#################################################
regions = []
reg = region.Region()
reg.simplename = "test"
reg.displayname = "TEST"
reg.tcut = "nLeptons==2 && nMuons==1 && nElectrons==1"
regions.append(reg)
