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
	cp Recognition/dictionary $(DESTDIR)$(LISPEAKDIR)/Recognition
	cp -r Setup/defaults/bin $(DESTDIR)$(LISPEAKDIR)/Recognition
	#Language-spec
	mkdir -p $(DESTDIR)/usr/share/gtksourceview-3.0/language-specs
	cp Setup/lidic.lang $(DESTDIR)/usr/share/gtksourceview-3.0/language-specs
	#pyshared. We don't need to copy lispeak and gooslate in every subfolder any more!
	mkdir -p $(DESTDIR)/usr/share/pyshared/lispeak
	cp lispeak $(DESTDIR)/usr/share/pyshared/lispeak/lispeak.py
	cp Setup/libraries/goslate.py $(DESTDIR)/usr/share/pyshared/lispeak/goslate.py
	#launch icon
	mkdir -p $(DESTDIR)/usr/share/applications/
	cp lispeak.desktop $(DESTDIR)/usr/share/applications/

uninstall:
	rm -rf $(DESTDIR)$(LISPEAKDIR)
	rm -rf $(DESTDIR)/usr/share/pyshared/lispeak
	rm -f $(DESTDIR)/usr/share/gtksourceview-3.0/language-specs/lidic.lang
	rm -f $(DESTDIR)/usr/share/applications/lispeak.desktop
	

