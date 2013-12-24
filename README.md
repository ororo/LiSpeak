LiSpeak
=======

A voice command system built on the base of Palaver

Language Support
======
LiSpeak plugins are structured to easily have support for any language.
Files are named in accordance to their language. An English dictionary file is just name "en" and a Spanish dictionary file is name "es". It is that simple to add different languages.

Window Focus
=======
Plugins can add dictionaires that are applied only when a certain window is in focus.

The gedit control plugin is only in effect while gedit has focus.

Services
======
Services are plugins that run in the background and provided non-command features.

Services will also have access to the LiSpeak app indicator to add addition toggles and commands. (This is still under development)

Example:
    The Android plugin is a service, it doesn't add any commands but creates a service that uses http protocol to allow mobile phones to send it commands.
    
Multi-User Support
=======
The way plugins are installed was modified so their is now much better multi-user support. One user's plugins will no longer interfere with another user's.
