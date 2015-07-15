import sys
sys.path.append('../..')

class Region :
    def __init__(self) :
        self.simplename = ""
        self.tcut = ""
        self.displayname = ""

    def Print(self) :
        print 'Region "%s": %s'%(self.displayname, self.tcut)
