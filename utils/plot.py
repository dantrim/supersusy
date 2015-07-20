import ROOT as r
r.TCanvas.__init__._creates = False
import glob
from math import floor
import sys
sys.path.append('../..')

class Plot1D :
    def __init__(self) :
        self.is2D = False
        self.variable = ""
        self.region = ""
        self.name = ""
        self.x_label = "x-Label"
        self.y_label = "Entries"
        self.doLogY = False
        self.leg_is_left = False
        self.x_bin_width = 1.0
        self.x_range_min = 0.0
        self.x_range_max = 50.0
        self.y_range_min = 0.0
        self.y_range_max = 50.0

        self.canvas = None
        self.ratioCanvas = None

    def initialize(self, region = "", variable = "", name = "") :
        self.region = region
        self.variable = variable
        self.name = name

    def labels(self, x="", y="Entries") :
        self.x_label = x
        self.y_label = y

    def xax(self, width=1.0, min = 0.0, max = 500) :
        self.x_bin_width = width
        self.x_range_min = min
        self.x_range_max = max
        # call this to reset nbins
        self.nbins = self.get_n_bins()

    def yax(self, min = 0.0, max = 500) :
        self.y_range_min = min
        self.y_range_max = max

    def doLog(self) :
        '''
        Set y-axis logarithmic
        '''
        self.doLogY = True

    def defaultCanvas(self, name) :
        c = r.TCanvas("c_"+name, "c_"+name, 768, 768)
        return c

    def setRatioCanvas(self, name) :
        self.ratioCanvas = RatioCanvas(name)


    def default_name() :
        '''
        Default plot name is of the form:
            <region>_<variable>
        '''
        return self.region + "_" + self.variable

    def get_n_bins(self) :
        '''
        From the user-provided bin width and (min,max) get
        the number of bins
        '''
        max = self.x_range_max
        min = self.x_range_min
        width = self.x_bin_width
        nbins = floor( (max - min) / (width) + 0.5 ) 
        return nbins

    def set_name(self, plotname) :
        '''
        Override the default plot name
        '''
        self.name = plotname

    def Print(self) :
        print "Plot1D    plot: %s  (region: %s  var: %s)"%(self.name, self.region, self.variable)

class Plot2D :
    def __init__(self) :
        self.is2D = True
        self.xVariable = ""
        self.yVariable = ""
        self.name = self.default_plot_name(self)
        self.x_label = "x-Label"
        self.y_label = "y-Label"
        self.x_bin_width = 1.0
        self.y_bin_width = 1.0
        self.x_range_min = 0.0
        self.x_range_max = 50.0
        self.y_range_min = 0.0
        self.y_range_max = 0.0 

        self.n_binsX = self.get_n_bins(self, "X")
        self.n_binsY = self.get_n_bins(self, "Y")
        self.style = "colz"


    def default_plot_name(self) :
        '''
        Default plot name for 2D plots is of the form:
            <region>_<xVar>_<yVar>
        '''
        return self.region + "_" + self.xVariable + "_" + self.yVariable 

    def get_n_bins(self, axis="X") :
        '''
        From the user-provided bin width and (min,max) get
        the number of bins for the specified axis
        '''
        min, max, width, nbins = 0.0, 0.0, 0.0, 0.0
        if axis=="X" :
            min = self.x_range_min
            max = self.x_range_max
            width = self.x_bin_width
        elif axis=="Y" :
            min = self.y_range_min
            max = self.y_range_max
            width = self.y_bin_width
        nbins = floor( (max - min) / (width) + 0.5 )
        return nbins

    def set_plot_name(self, plotname) :
        '''
        Override the default plot name
        '''
        self.name = plotname

    def set_style(self, style="") :
        '''
        Override the default style of "colz"
        '''
        self.style = style

    def Print(self) :
        print "Plot2D    plot: %s  (region: %s  xVar: %s  yVar: %s)"%(self.name, self.xVariable, self.yVariable)

class RatioCanvas :
    def __init__(self, name) :
        self.name = "c_" + name
        self.canvas = r.TCanvas(self.name,self.name, 768, 768)
        self.upper_pad = r.TPad("upper", "upper", 0.0, 0.0, 1.0, 1.0)
        self.lower_pad = r.TPad("lower", "lower", 0.0, 0.0, 1.0, 1.0)
        self.set_pad_dimensions()

    def set_pad_dimensions(self) :
        can = self.canvas
        up  = self.upper_pad
        dn  = self.lower_pad

        can.cd()
        up_height = 0.55
        dn_height = 0.50
        up.SetPad(0.0, 1.0-up_height, 1.0, 1.0)
        dn.SetPad(0.0, 0.0, 1.0, dn_height)

        up.SetTickx(0)
        dn.SetGrid(0)
        dn.SetTicky(0)

        up.SetFrameFillColor(0)
        up.SetFillColor(0)
        dn.SetLeftMargin(0.04)
        dn.SetRightMargin(0.01)
        dn.SetBottomMargin(0.5)
        dn.SetTopMargin(0.03)

        up.SetLeftMargin(0.04)
        up.SetRightMargin(0.01)

        up.Draw()
        dn.Draw()
        can.Update()

        self.canvas = can
        self.upper_pad = up
        self.lower_pad = dn
        
        
