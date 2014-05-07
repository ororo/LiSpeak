#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from gi.repository import Gtk
import sys,os


class PopUp:
    def __init__(self,data,path):

        filename = "Setup/templates/plugininstall.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(filename)
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window1")
        self.window.set_title("LiSpeak - Install Plugin")
        self.notebook = self.builder.get_object("notebook1")
        #self.exit = self.builder.get_object("btnClose")
        #self.exit.connect("button-release-event",self.close)
        self.name = self.builder.get_object("lblName")
        self.name2 = self.builder.get_object("lblName2")
        self.depends = self.builder.get_object("lblDepends")
        self.spin = self.builder.get_object("spinner")
        self.btnInstall = self.builder.get_object("btnInstall")
        self.btnInstall.connect("button-release-event",self.install)
        self.name.set_text(data['name'])
        self.spin.start()
        self.name2.set_text(data['name'])
        if 'depends' in data:
            self.depends.set_text("\n".join(data['depends']))
        else:
            self.depends.set_text("None")
        print "Showing Installer"
        self.window.show_all()
        self.data = data
        self.path = path
    
    def install(self,a,b):
        print "Installing"
        self.notebook.next_page()
        self.installPlugin(self.path,parent=self)
        self.notebook.next_page()
        self.window.destroy()
        Gtk.main_quit()
        
    def refresh(self):
        while Gtk.events_pending():
            Gtk.main_iteration_do(True)
        
#try:
#    import lispeak
#except KeyError:
#    print "LiSpeak needs to be setup first"
#    sys.exit(1)
