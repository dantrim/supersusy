
import sys
sys.path.append('../../../../../')
import supersusy.utils.plot as plot
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region


#############################################
# Set up the samples
#############################################
backgrounds = []

ww_file = "/data/uclhc/uci/user/dantrim/TruthAna/WZtoWW/superTruth_361068_WWlvlv.root"
wz_file = "/data/uclhc/uci/user/dantrim/TruthAna/WZtoWW/superTruth_361601_WZlllv.root"

## WW
ww = background.Background("ww", "WW")
ww.scale_factor = 1.96
ww.set_color(r.kBlack)
ww.set_treename("superTruth")
ww.set_file(ww_file)
ww.set_tree()
backgrounds.append(ww)

## WZ
wz = background.Background("wz", "WZ'")
wz.scale_factor = 1.96
wz.set_color(46)
wz.set_treename("superTruth")
wz.set_file(wz_file)
wz.set_tree()
backgrounds.append(wz)




regions = []
reg = region.Region()
reg.simplename = "test"
reg.displayname = "test"
reg.tcut = "nLeptons==2 && (l_q[0]*l_q[1])<0 && isDF==1 && l_pt[0]>20 && l_pt[1]>20"
regions.append(reg)

#############################################
# Set up the plots
#############################################

plots = []

logy = 100000

#rs = ["CRT","CRW","VRT","VRW"]
rs = ["test"]

for rs_ in rs :
    # lepton pT 
    p = plot.Plot1D()
    p.initialize(rs_, "l_pt[0]", rs_ + "_lpt0")
    p.labels(x="Lead lepton p_{T} [GeV]", y = "Entries / 5 GeV")
    p.xax(5, 0, 250)
    p.yax(0.1, logy)
    p.doLogY = True
    p.setRatioCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.initialize(rs_, "l_pt[1]", rs_ + "_lpt1")
    p.labels(x="Sub-lead lepton p_{T} [GeV]", y = "Entries / 5 GeV")
    p.xax(5, 0, 250)
    p.yax(0.1, logy)
    p.doLogY = True
    p.setRatioCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.initialize(rs_, "l_eta[0]", rs_ + "_leta0")
    p.labels(x="Lead lepton #eta", y = "Entries / 0.5")
    p.xax(0.5, -5, 5)
    p.yax(0.1, logy)
    p.doLogY = True
    p.setRatioCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.initialize(rs_, "l_eta[1]", rs_ + "_leta1")
    p.labels(x="Sub-lead lepton #eta", y = "Entries / 0.5")
    p.xax(0.5, -5, 5)
    p.yax(0.1, logy)
    p.doLogY = True
    p.setRatioCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.initialize(rs_, "l_phi[0]", rs_ + "_lphi0")
    p.labels(x="Lead lepton #phi", y = "Entries / 0.1 rad")
    p.xax(0.1, -3.2, 3.2)
    p.yax(0.1, logy)
    p.doLogY = True
    p.setRatioCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.initialize(rs_, "l_phi[1]", rs_ + "_lphi1")
    p.labels(x="Sub-lead lepton #phi", y = "Entries / 0.1 rad")
    p.xax(0.1, -3.2, 3.2)
    p.yax(0.1, logy)
    p.doLogY = True
    p.setRatioCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.initialize(rs_, "dphiLL", rs_ + "_dphiLL")
    p.labels(x="#Delta#phi_{ll}", y = "Entries / 0.1 rad")
    p.xax(0.1, -3.2, 3.2)
    p.yax(0.1, logy)
    p.doLogY = True
    p.setRatioCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.initialize(rs_, "ptLL", rs_ + "_ptLL")
    p.labels(x="ptLL [GeV]", y = "Entries / 10 GeV")
    p.xax(10, 0, 250)
    p.yax(0.1, logy)
    p.doLogY = True
    p.setRatioCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.initialize(rs_, "drLL", rs_ + "_drLL")
    p.labels(x="drLL", y = "Entries / 0.2")
    p.xax(0.2, -5, 5)
    p.yax(0.1, logy)
    p.doLogY = True
    p.setRatioCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.initialize(rs_, "mll", rs_ + "_mll")
    p.labels(x="mll [GeV]", y = "Entries / 10 GeV")
    p.xax(10, 0, 200)
    p.yax(0.1, logy)
    p.doLogY = True
    p.setRatioCanvas(p.name)
    plots.append(p)


    p = plot.Plot1D()
    p.initialize(rs_, "mt2", rs_ + "_mt2")
    p.labels(x="m_{T2} [GeV]", y = 'Entries / 5 GeV')
    p.xax(5, 0, 250)
    p.yax(0.1, logy)
    p.doLogY = True
    p.setRatioCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.initialize(rs_, "j_n", rs_ + "_jn")
    p.labels(x="number of jets", y = 'Entries / 1')
    p.xax(1, 0, 10)
    p.yax(0.1, logy)
    p.doLogY = True
    p.setRatioCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.initialize(rs_, "lj_n", rs_ + "_ljn")
    p.labels(x="number of light jets", y = 'Entries / 1')
    p.xax(1, 0, 10)
    p.yax(0.1, logy)
    p.doLogY = True
    p.setRatioCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.initialize(rs_, "bj_n", rs_ + "_bjn")
    p.labels(x="number of b jets", y = 'Entries / 1')
    p.xax(1, 0, 10)
    p.yax(0.1, logy)
    p.doLogY = True
    p.setRatioCanvas(p.name)
    plots.append(p)

    p = plot.Plot1D()
    p.initialize(rs_, "met_et", rs_ + "_met")
    p.labels(x="met Et [GeV]", y = 'Entries / 10 GeV')
    p.xax(10, 0, 300)
    p.yax(0.1, logy)
    p.doLogY = True
    p.setRatioCanvas(p.name)
    plots.append(p)


#    # dpb
#    p = plot.Plot1D()
#    p.initialize(rs_, "DPB_vSS", rs_ + "_DPB")
#    p.labels(x="|#Delta#phi(#vec{#beta}_{CM}^{lab}, vis)|", y = "Entries / 0.1 radian")
#    p.xax(0.1, 0, 3.2)
#    p.yax(0.1, logy)
#    p.doLogY = True
#    p.setRatioCanvas(p.name)
#    plots.append(p)
#
#    # RPT
#    p = plot.Plot1D()
#    p.initialize(rs_, "RPT", rs_ + "_RPT")
#    p.labels(x="R_{p_{T}}", y = "Entries / 0.05")
#    p.xax(0.05, 0, 1)
#    p.yax(0.1, logy)
#    p.doLogY = True
#    p.setRatioCanvas(p.name)
#    plots.append(p)
#
#    # mt2
#    p = plot.Plot1D()
#    p.initialize(rs_, "mt2", rs_ + "_mt2")
#    p.labels(x="m_{T2} [GeV]", y = "Entries / 10 GeV")
#    p.xax(10, 0, 250)
#    p.yax(0.1, logy)
#    p.doLogY = True
#    p.setRatioCanvas(p.name)
#    plots.append(p)
#
#    # nBJets
#    p = plot.Plot1D()
#    p.initialize(rs_, "nBJets", rs_ + "_nBJets")
#    p.labels(x="Number of b-tagged jets", y = "Entries / 1")
#    p.xax(1, 0, 10)
#    p.yax(0.1, logy)
#    p.doLogY = True
#    p.setRatioCanvas(p.name)
#    plots.append(p)
#
