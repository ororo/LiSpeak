#!/usr/bin/env python

from gi.repository import Gtk
import sys,os

try:
    os.chdir("Microphone")
except:
    print "Currently in",os.getcwd()

class PopUp:
    def __init__(self):
        filename = "../Setup/templates/settings.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(filename)
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window1")
        self.window.set_title("LiSpeak Settings")
        self.about = self.builder.get_object("aboutdialog1")
        self.aboutBtn = self.builder.get_object("btnAbout")
        self.aboutBtn.connect("clicked", self.aboutOpen)
        self.notebook = self.builder.get_object("notebook1")
        self.exit = self.builder.get_object("btnClose")
        self.exit.connect("button-release-event",self.close)
        try:
            self.fillFields(lispeak.getInfo())
            self.window.show_all()
        except KeyError:
            print "LiSpeak needs to be setup first"
            Gtk.main_quit()
    def close(self,a=None,b=None,c=None):
        self.userinfo = {}
        self.userinfo["AUTOSTART"] = str(self.builder.get_object("chkStart").get_active())
        self.userinfo["MESSAGES"] = str(self.builder.get_object("chkMessage").get_active())
        self.userinfo["UPDATES"] = self.builder.get_object("chkUpdates").get_active()
        self.userinfo["PROXY"] = str(self.builder.get_object("chkProxy").get_active())
        self.userinfo["PROXYHOST"] = self.builder.get_object("txtProxyhost").get_text()
        self.userinfo["PROXYPORT"] = self.builder.get_object("txtProxyport").get_text()
        lispeak.writeInfo(self.userinfo)
        if self.userinfo["AUTOSTART"] == "True":
            lispeak.autostart(True)
        else:
            lispeak.autostart(False)
        Gtk.main_quit()
    def aboutOpen(self,widget):
        self.about.show_all()
    def fillFields(self, userinfo):
        for e in ['proxyport','proxyhost']:
            if e.upper() in userinfo:
                print 'txt'+e[0].upper()+e[1:]
                self.builder.get_object('txt'+e[0].upper()+e[1:]).set_text(userinfo[e.upper()])
        if "AUTOSTART" in userinfo:
            self.builder.get_object("chkStart").set_active(userinfo["AUTOSTART"] == "True")
        if "MESSAGES" in userinfo:
            self.builder.get_object("chkMessage").set_active(userinfo["MESSAGES"] == "True")
        if "UPDATES" in userinfo:
            self.builder.get_object("chkUpdates").set_active(userinfo["UPDATES"] == "True")
        if "PROXY" in userinfo:
            self.builder.get_object("chkProxy").set_active(userinfo["PROXY"] == "True")
try:
    import lispeak
except KeyError:
    print "LiSpeak needs to be setup first"
    sys.exit(1)
    
popup = PopUp()
Gtk.main()
