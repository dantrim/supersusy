import ROOT
ROOT.gROOT.SetBatch(True)

ROOT.TH1F.__init__._creates = False
ROOT.TH2F.__init__._creates = False
ROOT.TCanvas.__init__._creates = False
ROOT.TPad.__init__._creates = False
ROOT.TLine.__init__._creates = False
ROOT.TLegend.__init__._creates = False
ROOT.TGraphErrors.__init__._creates = False
ROOT.TGraphAsymmErrors.__init__._creates = False
ROOT.TLatex.__init__._creates = False

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
    draw_text(x=left_margin, y=1.0-0.85*top_margin, text=t, size=s)

def th1_to_tgraph(hist) :
    '''
    The provided histogram is turned into a TGraphErrors object
    '''
    g = ROOT.TGraphErrors()
    for ibin in xrange(hist.GetNbinsX()) :
        y = hist.GetBinContent(ibin)
        ey = hist.GetBinError(ibin)
        x = hist.GetBinCenter(ibin)
        ex = 0.5 * hist.GetBinWidth(ibin)


        g.SetPoint(ibin, x, y)
        g.SetPointError(ibin, ex, ey)
    return g

def convert_errors_to_poisson(hist) :
    value = 0.0
    error_poisson_up = 0.0
    error_poisson_down = 0.0
    alpha = 0.158655
    beta = 0.158655 # 68%

    g = ROOT.TGraphAsymmErrors()
    for i in range(int(hist.GetNbinsX())) :
        value = hist.GetBinContent(i)
        if value != 0 :
            error_poisson_up = 0.5 * ROOT.TMath.ChisquareQuantile(1-beta, 2 * (value + 1)) - value
            error_poisson_down = value - 0.5 * ROOT.TMath.ChisquareQuantile(alpha, 2 * value)
            g.SetPoint(i-1,hist.GetBinCenter(i), value)
            g.SetPointError(i-1, 0.5 * hist.GetBinWidth(i), 0.5 * hist.GetBinWidth(i), error_poisson_down, error_poisson_up)
        else :
            g.SetPoint(i-1, hist.GetBinCenter(i), -10)
            g.SetPointError(i-1, 0., 0., 0., 0.)

    return g 

def divide_histograms(hnum, hden, xtitle, ytitle) :
    '''
    Provide two histograms and divide hnum/hden.
    Converts the final result into a tgraph.
    '''
    nbins = hnum.GetNbinsX()
    xlow = hnum.GetBinCenter(1)
    xhigh = hnum.GetBinCenter(nbins+1)
    hratio = hnum.Clone("hratio")
    hratio.GetYaxis().SetTitle(ytitle)
    hratio.GetXaxis().SetTitle(xtitle)

    hratio.GetYaxis().SetTitleOffset(0.45 * hratio.GetYaxis().GetTitleOffset())
    hratio.GetYaxis().SetLabelSize(2 * hratio.GetYaxis().GetLabelSize())
    hratio.GetYaxis().SetTitleFont(42)
    hratio.GetYaxis().SetTitleSize(0.09)

    hratio.GetXaxis().SetTitleOffset(1.75 * hratio.GetYaxis().GetTitleOffset())
    hratio.GetXaxis().SetLabelSize(3 * hratio.GetXaxis().GetLabelSize())
    hratio.GetXaxis().SetTitleSize(0.15)
    hratio.GetXaxis().SetTitleFont(42)

    g = ROOT.TGraphAsymmErrors()
    gdata = th1_to_tgraph(hnum)
    for i in range(1,nbins+1) :
        c1 = float(hnum.GetBinContent(i))
        c2 = float(hden.GetBinContent(i))
        if c2 == 0 : break
        c3 = c1 / c2 * 1.0
        if c3 == 0 : c3 = -99
        hratio.SetBinContent(i, c3)

        g.SetPoint(i-1, hnum.GetBinCenter(i), c3)
        error_up = ( ( c2 + gdata.GetErrorYhigh(i-1) ) / c2 ) - 1.0
        error_dn = 1.0 - ( ( c2 - gdata.GetErrorYlow(i-1)) / c2 )
        g.SetPointError(i-1, 0.5 * hratio.GetBinWidth(i), 0.5 * hratio.GetBinWidth(i), error_dn, error_up)
    return g

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
def default_legend(xl=0.7,yl=0.75,xh=0.9,yh=0.88) :
    leg = ROOT.TLegend(xl, yl, xh, yh)
   # leg.SetNDC()
    leg.SetFillStyle(0)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetTextFont(42)
    return leg

# ----------------------------------------------
#  Text/Label Methods
# ----------------------------------------------
def draw_text(x=0.7, y=0.65, font=42, color=ROOT.kBlack, text="", size=0.04, angle=0.0) :
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


# ----------------------------------------------
#  TLine Methods
# ----------------------------------------------
def draw_line(xl=0.0,yl=0.0,xh=1.0,yh=1.0,color=ROOT.kBlack,width=2,style=1) :
    l = ROOT.TLine(xl,yl,xh,yh)
    l.SetLineColor(color)
    l.SetLineWidth(width)
    l.SetLineStyle(style)
    l.Draw()
