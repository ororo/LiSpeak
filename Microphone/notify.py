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

#ar = lispeak.getSingleInfo("ARDUINO")
#if ar == "":
#    ar = '/dev/ttyACM1'
#    lispeak.writeSingleInfo('ARDUINO','/dev/ttyACM1')
#lcd = lispeak.arduino(lispeak.getSingleInfo("ARDUINO"))
#lcd.sendText("Welcome|LiSpeak LCD;")

try:
    os.chdir("Microphone")
except:
    print "Currently in",os.getcwd()

def check_and_import(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True
        
try:
    from dbus.mainloop.glib import DBusGMainLoop
except ImportError:
    return False
else:
    from dbus.mainloop.qt.DBusQtMainLoop import DBusGMainLoop
    #if none exists, an ImportError will be throw
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
        #print keywords['path'], last_signal #debug
        if last_signal==SIG_DONE:
            os.system("touch in_grey")
        if last_signal==SIG_RECORD:
            os.system("touch in_green")
        if last_signal==SIG_STOP:
            os.system("touch in_red")
        if last_signal==SIG_WAIT:
            os.system("touch in_progress")
    except:
        pass

bus.add_signal_receiver(handler_function=msg_handler, dbus_interface='com.bmandesigns.lispeak', interface_keyword='iface',  member_keyword='member', path_keyword='path')

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if len(attrs) > 0:
            self.data[tag] = {}
            for a in attrs:
                self.data[tag][a[0]] = a[1] 
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
        self.display = False
        self.window.set_keep_above(True)
        color = gdk.color_parse('#F7A900')
        for wid in [self.window,self.exit,self.titleBox]:
            wid.modify_bg(Gtk.StateFlags.NORMAL, color)
        self.counter = 0
        self.counter2 = 0
        self.counting = False
        self.queue = []
        
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
        if os.path.exists("notification.lmf"):          #may use dbus instead of notification.lmf ?
            print "Notification"
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
