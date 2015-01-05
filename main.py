import wx
from drawgraph import *
import cascades


class InfoBox(wx.Panel):
    def __init__(self, parent, title):
        wx.Panel.__init__(self, parent)
        
        self.label=wx.StaticText(self, label=title)
        self.display=wx.TextCtrl(self)
        self.display.SetEditable(False)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.label, 0)
        sizer.Add(self.display, 1, wx.EXPAND)
        
        self.SetSizer(sizer)

#the main app window
class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, size=(800,600))        
        self.Center()

        self.main_panel = wx.Panel(self)

        #panel with buttons and text boxes
        self.info_panel = wx.Panel(self.main_panel)
        self.info_sizer = wx.FlexGridSizer(rows=0,cols=2)
        self.info_sizer.AddGrowableCol(1, proportion=5)
        self.info_panel.SetSizer(self.info_sizer)

        #buttons panel
        button_panel = wx.Panel(self.main_panel, pos = (0, 20))
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_panel.SetSizer(button_sizer)

        self.tikz = wx.Button(button_panel, -1, "Export TikZ")
        self.clear = wx.Button(button_panel, -1, "Clear network")
        self.cleardiv = wx.Button(button_panel, -1, "Clear values")

        self.onegen = wx.Button(button_panel, -1, "Advance 1 generation")
        self.tengen = wx.Button(button_panel, -1, "Advance 10 generations")
        self.fiftygen = wx.Button(button_panel, -1, "Advance 50 generations")

        button_sizer.AddMany([(self.tikz, 0), 
                              (self.clear,0), 
                              (self.cleardiv,0),
                              (self.onegen, 0),
                              (self.tengen, 0),
        					  (self.fiftygen, 0)])
        
        #text boxes and parameter entry
        self.sigma_button = wx.Button(self.info_panel, -1, "Set sigma")
        self.tau_button = wx.Button(self.info_panel, -1, "Set tau")
        self.La_button = wx.Button(self.info_panel, -1, "Set La")
        self.Ln_button = wx.Button(self.info_panel, -1, "Set Ln")
        self.v_button = wx.Button(self.info_panel, -1, "Set viscosity")

        self.sigma = wx.TextCtrl(self.info_panel)
        self.tau = wx.TextCtrl(self.info_panel)
        self.La = wx.TextCtrl(self.info_panel)
        self.Ln = wx.TextCtrl(self.info_panel)
        self.v = wx.TextCtrl(self.info_panel)

        self.info_sizer.Add(self.sigma_button, 0)
        self.info_sizer.Add(self.sigma, 1, wx.EXPAND)

        self.info_sizer.Add(self.tau_button, 0)
        self.info_sizer.Add(self.tau, 1, wx.EXPAND)

        self.info_sizer.Add(self.La_button, 0)
        self.info_sizer.Add(self.La, 1, wx.EXPAND)

        self.info_sizer.Add(self.Ln_button,0 )
        self.info_sizer.Add(self.Ln, 1, wx.EXPAND)

        self.info_sizer.Add(self.v_button)
        self.info_sizer.Add(self.v, 1, wx.EXPAND)

        #self.stable= self.add_infobox("Stable percentages:")

        #the graph drawing panel
        self.view = DrawPanel(self.main_panel, 
                              self.update_info)
        
        self.tikz.Bind(wx.EVT_BUTTON, self.export_tikz)
        self.clear.Bind(wx.EVT_BUTTON, self.clear_event)
        self.cleardiv.Bind(wx.EVT_BUTTON, self.clear_divisor)

        self.onegen.Bind(wx.EVT_BUTTON, self.gen1)
        self.tengen.Bind(wx.EVT_BUTTON, self.gen10)
        self.fiftygen.Bind(wx.EVT_BUTTON, self.gen50)

        self.sigma_button.Bind(wx.EVT_BUTTON, self.get_s)
        self.tau_button.Bind(wx.EVT_BUTTON, self.get_t)
        self.La_button.Bind(wx.EVT_BUTTON, self.get_La)
        self.Ln_button.Bind(wx.EVT_BUTTON, self.get_Ln)
        self.v_button.Bind(wx.EVT_BUTTON, self.get_v)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(button_panel)
        main_sizer.Add(self.info_panel, 0, wx.EXPAND)
        main_sizer.Add(self.view, 1, wx.EXPAND)
        self.main_panel.SetSizer(main_sizer)

    #open up a file dialog and write to a file
    def export_tikz(self, evt):
        dialog = wx.FileDialog(self, style = wx.FD_SAVE)
        dialog.ShowModal()
        path = dialog.GetPath()
        if path != "":
            print path
            tf = open(path, "w")
            tf.write(get_tikz_code(self.view.graph))
            tf.close()

    def get_s(self, event):
        value = self.sigma.GetValue()
        if not value:
            value = 0
        else:
            try:
                self.view.graph.sigma = float(value)
                if not 0 <= float(value) <= 1:
                    self.view.graph.sigma = 0
                    self.sigma.SetValue("Enter a value between 0 and 1, please!")
            except: 
                self.sigma.SetValue("Enter a number, please!")
        self.update_info()

    def get_t(self, event):
        value = self.tau.GetValue()
        if not value:
            value = 0
        else:
            try:
                self.view.graph.tau = float(value)
                if not 0 <= float(value) <= 1:
                    self.view.graph.tau = 0
                    self.tau.SetValue("Enter a value between 0 and 1, please!")
            except: 
                self.tau.SetValue("Enter a number, please!")
        self.update_info()

    def get_La(self, event):
        value = self.La.GetValue()
        if not value:
            value = 0
        else:
            try:
                self.view.graph.La = int(value)
            except: 
                self.La.SetValue("Enter an integer, please!")
        self.update_info()

    def get_Ln(self, event):
        value = self.Ln.GetValue()
        if not value:
            value = 0
        else:
            try:
                self.view.graph.Ln = int(value)
            except: 
                self.Ln.SetValue("Enter an integer, please!")
        self.update_info()

    def get_v(self, event):
        value = self.v.GetValue()
        if not value:
            value = 0
        else: 
            is_ok = True
            try: 
                v = float(value)
            except:
                self.v.SetValue("Enter a number, please!")
                is_ok = False
            if is_ok:
                if not 0 <= float(value) <= 1:
                        self.view.graph.viscosity = 0
                        self.v.SetValue("Enter a value between 0 and 1, please!")
                elif float(value)*self.view.divisor.max_degree() > 1:
                    self.view.graph.viscosity = 0
                    self.v.SetValue("This viscosity is too large for this graph!")
                else:
                    self.view.graph.viscosity = v
        self.update_info()

    def gen1(self, event):
        self.gen(1)

    def gen10(self, event):
        self.gen(10)

    def gen50(self, event):
        self.gen(50)

    def gen(self, n):
    	for x in range(n):
    		self.view.divisor.migration()
    		self.view.divisor.conversion()
        self.view.divisor.generation += n

        print "After " + str(self.view.divisor.generation) + " cycles:"

        for i in range(self.view.graph.vcount):
            print "Density at Island #" + str(i+1) + ": " + "{0: .4f}".format(self.view.divisor.values[i])
        print "\n"
        self.view.update_info()
    	self.view.Refresh()

    #the function to call whenever an edge or vertex is updated
    def update_info(self):
    	#self.stable.SetValue(repr(self.view.divisor.beta_crit()))
        return True
    
    def clear_event(self, event):
        self.view.clear()
        #self.stable.SetValue("")

    def clear_divisor(self, event):
        self.view.divisor.values = ([0]*len(self.view.graph.vertices))[:]
        self.generation = 0
        #self.stable.SetValue("")
        self.view.Refresh()

    def add_infobox(self, title):
        infolabel = wx.StaticText(self.info_panel, label=title)
        infobox = wx.TextCtrl(self.info_panel)
        self.info_sizer.Add(infolabel)
        self.info_sizer.Add(infobox, 1, wx.EXPAND)
        return infobox

app = wx.App()

frame=Frame('Graphmake')
frame.Show()

app.MainLoop()
