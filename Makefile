CC=gcc
CFLAGS=-c -Wall -Wno-unused  
LDFLAGS=-O3
SOURCES=Recognition/src/dictionary.c Recognition/src/match.c Recognition/src/commands.c
OBJECTS=$(SOURCES:.cpp=.o)
EXECUTABLE=Recognition/dictionary
DESTDIR ?= 
LISPEAKDIR ?= /opt/lispeak

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS) 
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@
.cpp.o:
	$(CC) $(CFLAGS) $< -o $@
check-syntax:
	$(CC) $(CFLAGS) -fsyntax-only $(SOURCES)

clean:
	rm -rf $(EXECUTABLE)
        
install: all 
	mkdir -p $(DESTDIR)$(LISPEAKDIR)
	cp * $(DESTDIR)$(LISPEAKDIR) 2>/dev/null || :       #non recursive!
	#Microphone
	cp -r Microphone $(DESTDIR)$(LISPEAKDIR)
	#Setup
	cp -r Setup $(DESTDIR)$(LISPEAKDIR)
	#Recognition. What about modes folder ?!?
	mkdir -p $(DESTDIR)$(LISPEAKDIR)/Recognition
	cp Recognition/*.py $(DESTDIR)$(LISPEAKDIR)/Recognition
	cp Recognition/dictionary $(DESTDIR)$(LISPEAKDIR)/Recognition
	cp -r Setup/defaults/bin $(DESTDIR)$(LISPEAKDIR)/Recognition
	#Language-spec
	mkdir -p $(DESTDIR)/usr/share/gtksourceview-3.0/language-specs
	cp Setup/lidic.lang $(DESTDIR)/usr/share/gtksourceview-3.0/language-specs
	#pyshared.
	cp lispeak $(DESTDIR)/usr/share/pyshared/lispeak.py
	cp Setup/libraries/goslate.py $(DESTDIR)/usr/share/pyshared/goslate.py
	#launch icon
	mkdir -p $(DESTDIR)/usr/share/applications/
	cp lispeak.desktop $(DESTDIR)/usr/share/applications/
	#binary symlinks
	mkdir -p $(DESTDIR)/usr/bin/
	ln -sf $(LISPEAKDIR)/lispeak $(DESTDIR)/usr/bin/lispeak
	ln -sf $(LISPEAKDIR)/start $(DESTDIR)/usr/bin/lispeak-start
	ln -sf $(LISPEAKDIR)/stop $(DESTDIR)/usr/bin/lispeak-stop
	#python modules symlinks
	mkdir -p $(DESTDIR)/usr/lib/python2.5/
	mkdir -p $(DESTDIR)/usr/lib/python2.6/
	mkdir -p $(DESTDIR)/usr/lib/python2.7/
	ln -sf /usr/share/pyshared/lispeak.py $(DESTDIR)/usr/lib/python2.5/
	ln -sf /usr/share/pyshared/lispeak.py $(DESTDIR)/usr/lib/python2.6/
	ln -sf /usr/share/pyshared/lispeak.py $(DESTDIR)/usr/lib/python2.7/
	ln -sf /usr/share/pyshared/goslate.py $(DESTDIR)/usr/lib/python2.5/
	ln -sf /usr/share/pyshared/goslate.py $(DESTDIR)/usr/lib/python2.6/
	ln -sf /usr/share/pyshared/goslate.py $(DESTDIR)/usr/lib/python2.7/
        
uninstall:
	rm -rf $(DESTDIR)$(LISPEAKDIR)
	rm -f $(DESTDIR)/usr/share/pyshared/lispeak.py
	rm -f $(DESTDIR)/usr/share/pyshared/goslate.py
	rm -f $(DESTDIR)/usr/lib/python2.*/goslate.py
	rm -f $(DESTDIR)/usr/lib/python2.*/lispeak.py
	rm -f $(DESTDIR)/usr/share/gtksourceview-3.0/language-specs/lidic.lang
	rm -f $(DESTDIR)/usr/share/applications/lispeak.desktop
	rm -f $(DESTDIR)/usr/bin/lispeak*
	

