import sys
import os
sys.path.append(os.environ['SUSYDIR'])


class mPlot2D :
    def __init__(self) :
        self.is2D = True
        self.name = ""
        self.title = ""
        self.region = ""
        self.sample = ""
        self.x_var = ""
        self.y_var = ""
        self.x_label = "x-label"
        self.y_label = "y-label"
        self.x_bin_width = 1.0
        self.y_bin_width = 1.0
        self.x_range_min = 0.0
        self.x_range_max = 0.0
        self.y_range_min = 0.0
        self.y_range_max = 0.0

    def initialize(self, region_="", xvar_="", yvar_="", name_="") :
        '''
        Initialize the selection (region_), x- and y-variables
        to be plotted (should match what is in the trees), as well
        as the name of the plot (this is the name that the image
        will be saved as)
        '''
        self.region = region_
        self.x_var  = xvar_
        self.y_var  = yvar_
        self.name   = name_

    def set_sample(self, sample_ = "") :
        self.sample = sample_

    def set_title(self, title_ = "") :
        self.title = title_

    def set_labels(self, x="", y ="Entries") :
        self.x_label = x
        self.y_label = y

    def xax(self, min = 0.0, max = 500) :
        self.x_range_min = min
        self.x_range_max = max

    def yax(self, min = 0.0, max = 500) :
        self.y_range_min = min
        self.y_range_max = max



class mJointPlot(mPlot2D) :
    def __init__(self) :
        mPlot2D.__init__(self)

        self.color = "#FEC9AA"
        self.kind = "kde"
        self.stat_func = None
        self.line_width = 1.2
        self.cmap = None
        self.n_levels = 60
        self.shade = True

    def Print(self) :
        print "mJointPlot    plot: %s (region: %s  xvar: %s  yvar: %s  kind: %s)"%(self.name, self.region, self.x_var, self.y_var, self.kind)
