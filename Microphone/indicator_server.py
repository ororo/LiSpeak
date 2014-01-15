#!/usr/bin/env python

import gtk,gobject,os,appindicator,subprocess,lispeak

try:
    os.chdir("Microphone")
except:
    print "Currently in",os.getcwd()
PWD=str(os.getcwd())

class indicator:
    def __init__(self):
        
        self.ind = appindicator.Indicator("LiSpeak", PWD + "/Indicator/mic.png", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)

        self.menu_setup()
        self.ind.set_menu(self.menu)
        
        gobject.timeout_add(100, self.callback)

    def menu_setup(self):
        self.menu = gtk.Menu()

        self.p_item = gtk.MenuItem("Install a Plugin")
        self.p_item.connect("activate", self.install)
        self.p_item.show()
        self.menu.append(self.p_item)

        self.r_item = gtk.MenuItem("Restart Servers")
        self.r_item.connect("activate", self.restart)
        self.r_item.show()
        self.menu.append(self.r_item)
        
        separator = gtk.SeparatorMenuItem()
        separator.show()
        self.menu.append(separator)

        self.quit_item = gtk.MenuItem("Quit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()
        self.menu.append(self.quit_item)

    def main(self):
        gtk.main()

    def quit(self, widget):
        sys.exit(0)
    
    def restart(self,widget):
        os.chdir("../")
        subprocess.call(["./start"])

    def install(self,widget):
        p = subprocess.Popen("zenity --entry --text='Enter the Plugin Name' --title='Plugin Installer'", shell=True, stdout=subprocess.PIPE).communicate()[0].replace('\n','')
        print "Installing: "+p
        lispeak.downloadPackage(p)
        lispeak.dialogInfo("Plugin Installed",'LiSpeak')
        
    def callback(self):
        if os.path.exists("in_grey"):
            self.ind.set_icon(PWD + "/Indicator/mic.png")
            os.remove('in_grey')
        if os.path.exists("in_green"):
            self.ind.set_icon(PWD + "/Indicator/listen.png")
            os.remove("in_green")
        return True
ind = indicator()
gtk.main()
