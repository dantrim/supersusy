import os
import sys
#sys.path.append('../../../../../')
sys.path.append(os.environ['SUSYDIR'])
import supersusy.utils.background as background
import supersusy.utils.signal as signal
import supersusy.utils.region as region


############################################################
## set up the samples
############################################################

##
### directories
##
scratchdir = "/scratch/dantrim/n0211/"
datafile = scratchdir + "data15_13TeV.root"
mcfile = scratchdir + "sigOpt_mc15_noPRW_RF.root"

backgrounds = []

## ttbar
ttbar = background.Background("ttbar", "t#bar{t}")
ttbar.set_debug()
ttbar.set_file(mcfile)
ttbar.scale_factor = 1.0
ttbar.set_treename("TTbar_CENTRAL")
ttbar.set_merged_tree(ttbar.treename)
backgrounds.append(ttbar)


## bwn (250, 160)
bwn1 = background.Background("bwn_250_160", "(250, 160)")
bwn1.setSignal()
bwn1.set_debug()
bwn1.set_file(mcfile)
bwn1.scale_factor = 1.0
bwn1.set_treename("bwn_250_160_CENTRAL")
bwn1.set_merged_tree(bwn1.treename)
backgrounds.append(bwn1)

## bwn (300, 180)
bwn2 = background.Background("bwn_300_180", "(300, 180)")
bwn2.setSignal()
bwn2.set_debug()
bwn2.set_file(mcfile)
bwn2.scale_factor = 1.0
bwn2.set_treename("bwn_300_180_CENTRAL")
bwn2.set_merged_tree(bwn2.treename)
backgrounds.append(bwn2)

## ww
ww = background.Background("ww", "WW")
ww.set_debug()
ww.set_file(mcfile)
ww.scale_factor = 1.0
ww.set_treename("WW_CENTRAL")
ww.set_merged_tree(ww.treename)
backgrounds.append(ww)

############################################################
# Set up the regions
############################################################
regions = []

##
### wwLoose
##

reg = region.Region("wwLoose", "wwLoose")
reg.setCutFlow()
reg.addCut("Exactly 2 leptons", "nLeptons==2")
reg.addCut("DF", "nElectrons==1 && nMuons==1")
reg.addCut("OS", "(l_q[0]*l_q[1])<0")
reg.addCut("Lepton pT > 20 GeV", "l_pt[0]>20 && l_pt[1]>20")
regions.append(reg)

reg = region.Region("wwLooseSF", "wwLooseSF")
reg.setCutFlow()
reg.addCut("Exactly 2 leptons", "nLeptons==2")
reg.addCut("SF", "(nElectrons==2 || nMuons==2)")
reg.addCut("OS", "(l_q[0]*l_q[1])<0")
reg.addCut("Lepton pT > 20 GeV", "l_pt[0]>20 && l_pt[1]>20")
regions.append(reg)



