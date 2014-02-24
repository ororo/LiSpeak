#!/usr/bin/env python

# -*- coding: utf-8 -*-

import math

import cairo

import urllib2,sys,time,os,lispeak,json
from HTMLParser import HTMLParser

from gi.repository import Gtk
from gi.repository import Gdk as gdk
from gi.repository import GdkPixbuf as pixbuf
from gi.repository import Gtk as gtk
from gi.repository import GObject as gobject

ar = lispeak.getSingleInfo("ARDUINO")
if ar == "":
    ar = '/dev/ttyACM1'
    lispeak.writeSingleInfo('ARDUINO','/dev/ttyACM1')
lcd = lispeak.arduino(lispeak.getSingleInfo("ARDUINO"))
lcd.sendText("Welcome|LiSpeak LCD;")

try:
    os.chdir("Microphone")
except:
    print "Currently in",os.getcwd()


from dbus.mainloop.glib import DBusGMainLoop
#there is also dbus.mainloop.qt.DBusQtMainLoop for KDE...
DBusGMainLoop(set_as_default=True)

import dbus
bus = dbus.SessionBus()

SIG_WAIT=1
SIG_DONE=2
SIG_STOP=3
SIG_RECORD=4
SIG_RESULT=5

last_signal=None

def msg_handler(*args,**keywords):
    global last_signal
    try:
        last_signal=int(keywords['path'].split("/")[4])
        print keywords['path'], last_signal #debug
    except:
        pass

bus.add_signal_receiver(handler_function=msg_handler, dbus_interface='com.bmandesigns.lispeak', interface_keyword='iface',  member_keyword='member', path_keyword='path')


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if len(attrs) > 0:
            self.data[tag] = {}
            for a in attrs:
                self.data[tag][a[0]] = a[1] 

class ShapedWindow(gtk.Window):
  def __init__(self):
      gtk.Window.__init__(self)
      self.connect('size-allocate', self._on_size_allocate)
      self.set_decorated(False)

  def _on_size_allocate(self, win, allocation):
      w,h = allocation.width, allocation.height
      bitmap = gtk.gdk.Pixmap(None, w, h, 1)
      cr = bitmap.cairo_create()

      # Clear the bitmap
      cr.set_source_rgb(0.0, 0.0, 0.0)
      cr.set_operator(cairo.OPERATOR_CLEAR)
      cr.paint()

      # Draw our shape into the bitmap using cairo
      cr.set_source_rgb(1.0, 1.0, 1.0)
      cr.set_operator(cairo.OPERATOR_SOURCE)
      cr.arc(w / 2, h / 2, min(h, w) / 2, 0, 2 * math.pi)
      cr.fill()

      # Set the window shape
      win.shape_combine_mask(bitmap, 0, 0)

class PopUp:
    def __init__(self):
        filename = "popup.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(filename)
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window1")
        self.title = self.builder.get_object("lblTitle")
        self.message = self.builder.get_object("lblMessage")
        self.titleBox = self.builder.get_object("labelbox")
        self.titleBox.connect("button-release-event", self.on_clicked)
        self.exit = self.builder.get_object("exitbox")
        self.exit.connect("button-release-event",self.close_notify)
        self.icon = self.builder.get_object("imgIcon") 
        self.window.set_gravity(gdk.Gravity.NORTH_WEST)  
        #self.window.show_all()
        self.display = False
        self.window.set_keep_above(True)
        color = gdk.color_parse('#F7A900')
        for wid in [self.window,self.exit,self.titleBox]:
            wid.modify_bg(Gtk.StateFlags.NORMAL, color)
        self.counter = 0
        self.counter2 = 0
        self.counting = False
        self.queue = []
        
        #print self.window.get_screen().get_active_window()
        #monitor = self.window.get_screen().get_monitor_geometry(self.window.get_screen().get_monitor_at_window(self.window.get_screen().get_active_window()))
        #print("Heigh: %s, Width: %s" % (monitor.height, monitor.width))
        
        self.builder2 = Gtk.Builder()
        self.builder2.add_from_file("nonclose.glade")
        self.builder2.connect_signals(self)
        #self.nwindow = self.builder2.get_object("window1")
        #self.ntitle = self.builder2.get_object("title")
        #self.nimage = self.builder2.get_object("image")
        #self.nwindow.set_keep_above(True)
        #self.ntitle.set_text("Waiting...")
        #self.nwindow.show_all()
        #monitor = self.nwindow.get_screen().get_monitor_geometry(self.nwindow.get_screen().get_monitor_at_window(self.nwindow.get_screen().get_active_window()))
        #print("Heigh: %s, Width: %s" % (monitor.height, monitor.width))
        #self.nwindow.move(monitor.width-self.nwindow.get_size()[0],monitor.height-self.nwindow.get_size()[1])
        
        gobject.timeout_add_seconds(1, self.timer)
        gobject.timeout_add_seconds(0.2, self.display_notify)
        gobject.timeout_add_seconds(30, self.message_system)
        while gtk.events_pending():
            gtk.main_iteration_do(True)
        self.message_system()
            
    def speak(self,a=None,b=None,c=None):
        lispeak.speak(self.speech)
        return False

    def close_notify(self,a=None,b=None,c=None):
        print "Closing"
        for each in range(10,-1,-1):
            self.window.set_opacity(float("0."+str(each)))
            while gtk.events_pending():
                gtk.main_iteration_do(True)
            time.sleep(0.05)
        self.display = False
        self.window.hide()
        self.counting = False
            
    def on_clicked(self, widget, thrid):
        if self.counting:
            self.counting = False   
            self.window.set_opacity(1.0)
            self.message.set_visible(True)
        else:
            self.counting = True
            self.window.set_opacity(0.9)
            self.message.set_visible(not self.message_hide)
        
    def message_system(self):
        print "Checking for Message"
        f = urllib2.urlopen("http://lispeak.bmandesigns.com/functions.php?f=messageUpdate")
        text = f.read()
        message = json.loads(text.replace('\r', '\\r').replace('\n', '\\n'),strict=False)
        lastId = lispeak.getSingleInfo("lastid")
        print "Checking done." #debug 14 seconds !?!
        if lastId == "":
            lastId = message['id']
        try:
            go = int(message['id']) > int(lastId)
        except:
            go = True
        if go:
            if 'icon' in message:
                urllib.urlretrieve(message['icon'], "/tmp/lsicon.png")
                self.queue.append({'TITLE':"LiSpeak - "+message['title'],'MESSAGE':message['text'],'ICON':"/tmp/lsicon.png","SPEECH":message['text']})
            else:
                self.queue.append({'TITLE':"LiSpeak - "+message['title'],'MESSAGE':message['text'],"SPEECH":message['text']})
        
        lispeak.writeSingleInfo("lastid",str(int(message['id'])))
        return True
        
    def display_notify(self):
        #if os.path.exists("pycmd_done"):
        if last_signal==SIG_DONE:
            #self.ntitle.set_text("Done!")
            os.system("touch in_grey")
        #if os.path.exists("pycmd_record"):
        if last_signal==SIG_RECORD:
            os.system("touch in_green")
            #self.ntitle.set_text("Listening...")
        #if os.path.exists("pycmd_stop"):
        if last_signal==SIG_STOP:
            #self.ntitle.set_text("Please Wait...")
            os.system("touch in_red")
        #if os.path.exists("pycmd_wait"):
        if last_signal==SIG_WAIT:
            #self.ntitle.set_text("Analyzing...")
            os.system("touch in_progress")
        if os.path.exists("notification.lmf"):          #may use dbus instead of notification.lmf ?
            time.sleep(0.05)
            with open("notification.lmf") as f:
                data = lispeak.parseData(f.read())
                self.queue.append(data)
                print data,"ADDED TO QUEUE"
            os.remove("notification.lmf")
        return True
        
    def timer(self):
        try:
            if self.counting:
                if self.counter == 0:
                    self.display = True
                    for each in range(0,10):
                        if self.counting:
                            self.window.set_opacity(float("0."+str(each)))
                            while gtk.events_pending():
                                gtk.main_iteration_do(True)
                            self.window.show_all()
                            self.window.move(100,150)
                            self.message.set_visible(not self.message_hide)
                            self.icon.set_visible(not self.image_hide)
                    self.speak(self.speech)
                if self.counter == 5:
                    if self.window.get_opacity() != 0.0:
                        for each in range(9,-1,-1):
                            self.window.set_opacity(float("0."+str(each)))
                            while gtk.events_pending():
                                gtk.main_iteration_do(True)
                            time.sleep(0.02)
                        self.window.hide()
                        self.display = False
                        self.counting = False
                self.counter += 1
            elif len(self.queue) > 0 and self.display == False:
                data = self.queue[0]
                try:
                    self.message.set_text("")
                    self.message_hide = True
                    self.message.set_text(data['MESSAGE'].replace("\\n","\n"))
                    if data['MESSAGE'].count("\\n") < 3 and data['MESSAGE'].count("\n") < 3:
                        self.message_hide = False
                except:
                    pass
                self.title.set_text(data['TITLE'])
                if 'ICON' in data:
                    if data['ICON'].startswith("http"):
                        f2 = urllib2.urlopen(data['ICON'])
                        output = open('/tmp/lispeak-image','wb')
                        output.write(f2.read())
                        output.close()
                        buf = pixbuf.Pixbuf.new_from_file_at_size("/tmp/lispeak-image",75,75)
                        self.icon.set_from_pixbuf(buf)
                    else:
                        try:
                            buf = pixbuf.Pixbuf.new_from_file_at_size(data['ICON'].replace("file://",""),75,75)
                            self.icon.set_from_pixbuf(buf)
                        except:
                            print "Invalid Image:",data['ICON']
                    self.image_hide = False
                else:
                    self.image_hide = True
                if "SPEECH" in data:
                    print data['SPEECH']
                    if data["SPEECH"] != "None":
                        self.speech = data['SPEECH']
                    else:
                        self.speech = data['TITLE']
                else:
                    self.speech = data['TITLE']
                self.counter = 0
                self.counting = True
                self.queue.pop(0)
                lcd.sendText(self.title.get_text()+"|"+self.message.get_text()+";")
            return True
        except:
            print "AN ERROR OCCURED!"
            return True
        


PopUp()
Gtk.main()
