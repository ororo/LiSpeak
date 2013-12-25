#!/usr/bin/env python

import subprocess,sys,platform,tarfile,os
import sqlite3 as sql

home = subprocess.Popen("echo $HOME", shell=True, stdout=subprocess.PIPE).communicate()[0].replace('\n','')
root = home + "/.lispeak"

approvedDistros = {"Ubuntu":["13.10"]}

def displayInstallWarning():
    d,v,j = platform.linux_distribution()
    if d != "":
        if d in approvedDistros:
            if v in approvedDistros[d]:
                print d,v,"is a supported operating system"
            else:
                print d,"is a supported operating system, but has not been tested on",v
                print "LiSpeak may not work properly"
                raw_input("Press enter to continue")
        else:
            print d,"is NOT a supported operating system"
            print "LiSpeak may not work properly"
            raw_input("Press enter to continue")
    else:
        print "Your operating system could not be detected"
        print "LiSpeak may not work properly"
        raw_input("Press enter to continue")

def output(text):
    print text

def askInfo(title="LiSpeak User Configuration",text="User Information",askFor={},plugin="UserInfo"):
    if askFor == {}:
        askFor = [["first","First Name"],["last","Last Name"],["email","Email"],["lang","Language (en,es,fr)"],["wakey","Wolfram Alpha Key"]]
        text2 = ""
        for e in askFor:
            text2 = text2 + " --add-entry='"+e[1]+"'"
        res = subprocess.Popen("zenity --forms "+text2+" --text='"+text+"' --title='"+title+"'", shell=True, stdout=subprocess.PIPE).communicate()[0].replace('\n','')
        res = res.split("|")
        installDir = ''.join([e+'/' for e in os.path.realpath(__file__).split('/')[0:-1]])
        x = 0
        data = {}
        for e in askFor:
            data[e[0]] = res[x]
            x = x + 1
        
        data["ROOTDIR"] = installDir
        
        writeInfo(data,plugin)
        
def parseData(text):
    oData = text.split("\n")
    orig = {}
    for e in oData:
        if e.strip().startswith("#") == False and "=" in e:
            pre,suf = e.strip().split("=",1)
            suf = suf.strip()
            if pre in ['depends','types','lang','configs']:
                data = []
                for d in suf.split(','):
                    data.append(d)
                suf = data
            orig[pre.strip()] = suf
    return orig
    
def getInfo(plugin="UserInfo"):
    if plugin == "UserInfo":
        oFile = open(root+"/UserInfo")
    else:
        oFile = open(root+"/configs/"+plugin)
    oData = oFile.read()
    oFile.close()
    return parseData(oData)
    
def homeDir():
    return home 
 
def displayNotification(text,text2 = False,image=False):
    if type(text) == list:
        for line in text:
            os.system("echo \""+line+"\n\" >> "+getSingleInfo("ROOTDIR")+"Microphone/result")
    else:
        if text2 == False:
            os.system("echo \""+text+"\n\" >> "+getSingleInfo("ROOTDIR")+"Microphone/result")
        else:
            os.system("echo \""+text+"\" >> "+getSingleInfo("ROOTDIR")+"Microphone/result")
    if text2 != False:
        os.system("echo \""+text2+"\n\" >> "+getSingleInfo("ROOTDIR")+"Microphone/result")
    if image != False:
        os.system("echo \""+image+"\n\" >> "+getSingleInfo("ROOTDIR")+"Microphone/result_image")
    os.system(getSingleInfo("ROOTDIR")+"pycmd result")
    print getSingleInfo("ROOTDIR")+"pycmd result"
 
def getSingleInfo(item):
    return getInfo()[item.upper()]
    
def writeSingleInfo(item,new=False):
    try:
        writeInfo({item.upper():new})
        return True
    except:
        return False
 
def writeInfo(new,plugin="UserInfo"):
    if plugin == "UserInfo":
        path = root+"/UserInfo"
    else:
        path = root+"/configs/"+plugin
    oFile = open(path)
    oData = oFile.read()
    oFile.close()
    orig = parseData(oData)
    data = new
    for e in orig:
        if e not in data:
            data[e] = orig[e]
    with open(path,'w') as info:
        info.write("#LiSpeak Config File: "+plugin)
        for each in data:
            info.write("\n"+each.upper()+"="+data[each])
            
def sqlCheck(cur):
    cur.execute("CREATE TABLE IF NOT EXISTS plugins(id INTEGER PRIMARY KEY, name TEXT, identifier TEXT,type TEXT, version TEXT, author TEXT, binFiles TEXT,services TEXT, dicts TEXT, actions TEXT)")
            
def installPlugin(path):
    dictionaries = []
    services = []
    executables = []
    complete = False
    config = root + "/config/"
    if path.endswith('.sp') or path.endswith('.tar.gz'):
        plugins = {}
        con = sql.connect(root+"/plugins.db")
        with con:
            cur = con.cursor()
            sqlCheck(cur)
            cur.execute("SELECT * FROM plugins")
            pluginList = cur.fetchall()
            for line in pluginList:
                pid,name,identifier,types,version,author,cmdfile,servicefiles,dictionaries,actions = line
                plugins[identifier] = [float(version),eval(cmdfile)]
        tar = tarfile.open(mode='r:gz',fileobj=file(path))
        dataf = tar.extractfile('main.info')
        data = dataf.read()
        dataf.close()
        data = parseData(data)       
        try:
            currentVersion = plugins[data['identifier']][0]
            version = float(data['version'])
            if currentVersion > version:
                output("A newer version is already installed")
                with open('InstallResult','w') as d:
                    d.write("A newer version is already installed")
            elif currentVersion == version:
                output("This version is already installed")
                with open('InstallResult','w') as d:
                    d.write("This version is already installed")
            else:
                output("Updating Files Has Not Yet Been Added, please remove the old version with -r and then install again")
                with open('InstallResult','w') as d:
                    d.write("Updating Files Has Not Yet Been Added, please remove the old version with -r and then install again")
                #Install Files
        except:
            isntall = False
            userLang = getSingleInfo("lang")
            if userLang in data['lang']:
                print "This plugin is available in",userLang
                install = True
                installLang = userLang
            else:
                if len(data['lang']):
                    print "This plugin is only available in",data['lang'][0]
                    installLang = data['lang'][0]
                    install = raw_input("Install Anyway? (y/n) ").lower() in ['y','yes']
                else:
                    while install == False:
                        print "This plugin is only available in",data['lang']
                        l = raw_input("Which language would you like to install it in?")
                        if l in data['lang']:
                            installLang = l
                            install = True
            while install == True and complete == False:
                actions = {}
                if "depends" in data:
                    depend = data['depends']
                    os.system("sudo -i apt-get install "+" ".join(depend))
                print "Installation is beginning"
                os.system("rm "+root+"/"+data['identifier']+" -r")
                print "Extracting"
                tar.extractall(root+"/"+data['identifier'])
                if "commands" in data['types']:
                    print "Scanning Files"
                    try:
                        new = os.listdir(root+"/"+data['identifier']+"/bin")
                        executables = new
                        os.system("mkdir "+root+"/bin")
                        existing = os.listdir(root+"/bin")
                        for f in new:
                            if f in existing:
                                print "Conflict Found: "+f
                                install = False
                        if install == False:
                            break
                        print "Moving Executables"
                        for f in new:
                            os.system("mv \""+root+"/"+data['identifier']+"/bin/"+f+"\" \""+root+"/bin/"+f+"\"")
                            os.system("chmod +x \""+root+"/bin/"+f+"\"")
                    except:
                        print "No Executable Files"
                    try:
                        dictionary = open(root+'/plugins.dic')
                    except:
                        os.system("touch "+root+'/plugins.dic')
                        dictionary = open(root+'/plugins.dic')
                    text = dictionary.read()
                    dictionary.close()
                    actions = open(root+"/"+data['identifier']+"/dictionaries/"+installLang)
                    command = actions.read()
                    actions.close()
                    try:
                        dictionary = open(root+'/plugins.dic','w')
                        dictionary.write("#PLUGIN: "+data['identifier']+"\n")
                        dictionary.write(command)
                        dictionary.write("#END\n")
                        dictionary.write(text)
                    except:
                        output("Error Installing Plugin In main.dic")
                    dictionary.close()
                    try:
                        os.system("mkdir "+root+"/dictionaries")
                        new = os.listdir(root+"/"+data['identifier']+"/dictionaries")
                        for f in new:
                            if os.path.isdir(root+"/"+data['identifier']+"/dictionaries/"+f):
                                try:
                                    dictionary = open(root+'/dictionaries/'+f+'.dic')
                                except:
                                    os.system("touch "+root+'/dictionaries/'+f+'.dic')
                                    dictionary = open(root+'/dictionaries/'+f+'.dic')
                                text = dictionary.read()
                                dictionary.close()
                                actions = open(root+"/"+data['identifier']+"/dictionaries/"+f+"/"+installLang)
                                command = actions.read()
                                actions.close()
                                try:
                                    dictionary = open(root+'/dictionaries/'+f+'.dic','w')
                                    dictionary.write("#PLUGIN: "+data['identifier']+"\n")
                                    dictionary.write(command)
                                    dictionary.write("#END\n")
                                    dictionary.write(text)
                                except:
                                    output("Error Installing Plugin In "+f+".dic")
                                dictionaries.append(f)
                    except:
                        print "Error Scanning Dictionaries"
                    descfile = open(root+"/"+data['identifier']+"/languages/"+installLang)
                    desc = descfile.read()
                    descfile.close()
                    desc = desc.split('\n')
                    actions = {}
                    for d in desc:
                        if ":" in d:
                            n = d.split(":",1)
                            actions[n[0]] = n[1]
                if "service" in data['types']:
                    print "Scanning Files"
                    new = os.listdir(root+"/"+data['identifier']+"/services")
                    services = new
                    os.system("mkdir "+root+"/services")
                    existing = os.listdir(root+"/services")
                    for f in new:
                        if f in existing:
                            print "Conflict Found: "+f
                            install = False
                    if install == False:
                        break
                    print "Moving Services"
                    for f in new:
                       os.system("mv \""+root+"/"+data['identifier']+"/services/"+f+"\" \""+root+"/services/"+f+".service\"")
                os.system("mkdir "+root+"/configs")
                os.system("touch \""+root+"/configs/"+data['identifier']+"\"")
                con = sql.connect(root+"/plugins.db")
                with con:
                    cur = con.cursor()
                    sqlCheck(cur)
                    execline = "INSERT INTO plugins VALUES(NULL, \""+data['name']+"\", \""+str(data['identifier'])+"\", \""+str(data['types'])+"\", \""+str(data['version'])+"\", \""+data['author']+"\", \""+str(executables)+"\", \""+str(services)+"\", \""+str(dictionaries)+"\", \""+str(actions)+"\")"
                    cur.execute(execline)
                os.system("rm "+root+"/"+data['identifier']+" -r")
                print "Done"
                complete = True
                
            if complete == False:
                print
                print "Installation Cancelled"
                print
            else:
                print
                print "Installation Done!"
                print
            
def removePlugin(ridentifier):
    con = sql.connect(root+"/plugins.db")
    with con:
        cur = con.cursor()
        sqlCheck(cur)
        cur.execute("SELECT * FROM plugins")
        pluginList = cur.fetchall()
        for line in pluginList:
            pid,name,identifier,types,version,author,cmdfile,servicefiles,dictionaries,actions = line
            print identifier,ridentifier
            if identifier == ridentifier:
                print "Removing "+name
                for cmd in eval(cmdfile):
                    print "Removing Executable:",cmd
                    os.system("rm "+root+"/bin/"+cmd)
                for ser in eval(servicefiles):
                    print "Removing Service:",ser
                    os.system("rm "+root+"/services/"+ser)
                print "Removing Config File"
                os.system("rm "+root+"/configs/"+identifier)
                print "Removng Dictionaries"
                for dic in eval(dictionaries):
                    dictionary = open(root+'/dictionaries/'+dic+'.dic')
                    text = ""
                    deleting = False
                    for line in dictionary:
                        if deleting == False:
                            add = True
                            if line.startswith('#PLUGIN: '):
                                if line.replace('#PLUGIN: ','').replace('\n','') == identifier:
                                    add = False
                                    deleting = True
                        else:
                            add = False
                            if line == "#END\n":
                                deleting = False
                        if add == True:
                            text = text + line
                    dictionary.close()
                    try:
                        dictionary = open(root+'/dictionaries/'+dic+'.dic','w')
                        dictionary.write(text)
                    except:
                        output("Error Cleaning "+dic+'.dic')
                    dictionary.close()
                dictionary = open(root+'/plugins.dic')
                text = ""
                deleting = False
                for line in dictionary:
                    if deleting == False:
                        add = True
                        if line.startswith('#PLUGIN: '):
                            if line.replace('#PLUGIN: ','').replace('\n','') == identifier:
                                add = False
                                deleting = True
                    else:
                        add = False
                        if line == "#END\n":
                            deleting = False
                    if add == True:
                        text = text + line
                dictionary.close()
                try:
                    dictionary = open(root+'/plugins.dic','w')
                    dictionary.write(text)
                except:
                    output("Error Cleaning plugins.dic")
                dictionary.close()
                cur.execute("DELETE FROM plugins WHERE id = "+str(pid))

commands = {"askInfo":askInfo,"getInfo":getSingleInfo,"writeInfo":writeSingleInfo,"displayInstallWarning":displayInstallWarning,'installPlugin':installPlugin,'removePlugin':removePlugin,'notification':displayNotification}
if __name__ == "__main__":
    args = sys.argv
    if args[1] in commands:
        if len(args[2:]) > 2:
            r = commands[args[1]](args[2:])
            if r != None:
                print r
        else:
            try:
                r = commands[args[1]](args[2],args[3])
                if r != None:
                    print r
            except IndexError as e:
                print e
                try:
                    r = commands[args[1]](args[2])
                    if r != None:
                      print r
                except TypeError as e:
                    print e
                    r = commands[args[1]]()
                    if r != None:
                        print r
    else:
        print "Invalid Argument:",args[1]
        print
        print "Valid Commands:"
        for e in commands:
            print e
    
