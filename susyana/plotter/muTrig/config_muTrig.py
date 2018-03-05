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


filedir = "/data/uclhc/uci/user/dantrim/for_muTrigPlot/"

lumi_ = [1.0] 
lumi_val = 0

######## MC
bkg = background.Background("bkg", "Background 0")
bkg.scale_factor = lumi_[lumi_val]
bkg.set_fillStyle(0)
bkg.setLineStyle(1)
bkg.set_color(r.TColor.GetColor("#e4706a"))
bkg.set_treename("segPerf")
bkg.set_file(filedir + "muTrigAna_segments_user.asoffa.11790973.EXT0")
bkg.set_merged_tree("segPerf")
backgrounds.append(bkg)

##########################################
# regions
##########################################
regions = []

reg = region.Region()
reg.name = "testMuTrig"
reg.displayname = "Test #mu-Trig"
reg.tcut = "seg_muon_pt > 20"
regions.append(reg)

##########################################
# plots
##########################################
plots = []

vars = {}
vars["seg_muon_pt"] = { "testMuTrig" : [5, 0, 115, 1000000] }

run_reg = "testMuTrig"

nice_names = {}
nice_names["seg_muon_pt"] = "Segment #mu p_{T} [GeV]"

logy_regions = ["testMuTrig"]


for var in vars.keys() :
    nice_names[var] = var

for var, bounds in vars.iteritems() :
    p = plot.Plot1D()
    name_ = ""
    if "abs(" in var :
        name_ = var.replace("abs(","")
        name_ = name_.replace(")", "")
    elif "[" in var :
        name_ = var.replace("[","")
        name_ = name_.replace("]","")
    else :
        name_ = var
    p.initialize(run_reg, var, "%s_%s"%(run_reg, name_))
    ylabel_unit = ""
    gev_variables = []
    if var in gev_variables :
        ylabel_unit = " GeV"
    ylabel_title = str(bounds[run_reg][0]) + ylabel_unit
    p.labels(x=nice_names[var], y = "Events / %s"%(str(ylabel_title)))
    p.xax(bounds[run_reg][0], bounds[run_reg][1], bounds[run_reg][2])
    if run_reg in logy_regions :
        p.doLogY = True
        if len(bounds[run_reg]) == 4 :
            p.yax(0.1, bounds[run_reg][3])
        else :
            p.yax(0.1, 1e7)
    else :
        p.doLogY = False
        if len(bounds[run_reg]) == 4 :
            p.yax(0, bounds[run_reg][3])
        else :
            p.yax(0, 5000)
    p.setDefaultCanvas(p.name)
    plots.append(p)
