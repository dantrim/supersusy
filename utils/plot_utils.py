import ROOT
ROOT.gROOT.SetBatch(True)

ROOT.TH1F.__init__._creates = False
ROOT.TH2F.__init__._creates = False
ROOT.TCanvas.__init__._creates = False
ROOT.TPad.__init__._creates = False
ROOT.TLine.__init__._creates = False
ROOT.TLegend.__init__._creates = False


# ----------------------------------------------
#  TCanvas Methods
# ----------------------------------------------
def basic_canvas(name = "c", width = 768, height = 768, nxpads = 1, nypads = 1) :
    '''
    Book a canvas and return it
    '''
    c = ROOT.TCanvas(name, name, width, height)
    c.Divide(nxpads, nypads)
    c.cd(1)
    c.Modified()
    return c



# ----------------------------------------------
#  TH1F Methods
# ----------------------------------------------
def th1f(name, title, nbin, nlow, nhigh, xtitle, ytitle) :
    '''
    Book a TH1F and return it
    '''
    h = ROOT.TH1F(name, title, nbin, nlow, nhigh)
    font = 42
    h.SetTitleFont(font)

    # x-axis
    xaxis = h.GetXaxis()
    xaxis.SetTitle(xtitle)
    xaxis.SetTitleOffset(1.2 * xaxis.GetTitleOffset()) 
    xaxis.SetTitleFont(font)
    xaxis.SetLabelFont(font)
    
    # y-axis
    yaxis = h.GetYaxis()
    yaxis.SetTitle(ytitle)
    yaxis.SetTitleOffset(1.2 * yaxis.GetTitleOffset())
    yaxis.SetTitleFont(font)
    yaxis.SetLabelFont(font)

    # 2 is better than 1
    h.Sumw2()
    return h

def draw_text_on_top(text="", size=0.04, ) :
    s = size
    t = text
    top_margin = ROOT.gPad.GetTopMargin()
    left_margin = ROOT.gPad.GetLeftMargin()
    draw_text(x=left_margin, y=1.0-0.93*top_margin, text=t, size=s)

# ----------------------------------------------
#  TH2F Methods
# ----------------------------------------------
def th2f(name, title, nxbin, xlow, xhigh, nybin, ylow, yhigh, xtitle, ytitle) :
    '''
    Book a TH2F and return it
    '''
    h = ROOT.TH2F(name, title, nxbin, xlow, xhigh, nybin, ylow, yhigh)
    h.GetXaxis().SetTitle(xtitle)
    h.GetYaxis().SetTitle(ytitle)
    h.Sumw2()
    return h

# ----------------------------------------------
#  TLegend Methods
# ----------------------------------------------
def default_legend(xl=0.7,yl=0.7,xh=0.9,yh=0.9) :
    leg = ROOT.TLegend(xl, yl, xh, yh)
   # leg.SetNDC()
    leg.SetFillStyle(0)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetTextFont(62)
    return leg

# ----------------------------------------------
#  Text/Label Methods
# ----------------------------------------------
def draw_text(x=0.7, y=0.65, font=62, color=ROOT.kBlack, text="", size=0.04, angle=0.0) :
    '''
    Draw text on the current pad
    (coordinates are normalized to the current pad)
    '''
    l = ROOT.TLatex()
    l.SetTextSize(size)
    l.SetTextFont(font)
    l.SetNDC()
    l.SetTextColor(color)
    l.SetTextAngle(angle)
    l.DrawLatex(x, y, text)
