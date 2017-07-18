import socket
import sys
import os
from os.path import basename
import subprocess
import re
import json
import base64
import urllib2


G_XDOTOOL = "xdotool"
G_MOVIELIST = []
credentials = b'kodi:kodi'
encoded_credentials = base64.b64encode(credentials)
authorization = b'Basic ' + encoded_credentials
SCRIPTDIR = os.path.dirname(os.path.abspath(__file__))
#########################################################


def doKodi(data):
    headers = {'Content-Type': 'application/json', 'Authorization': authorization}
    url = 'http://192.168.0.5:8080/jsonrpc'
    try:
        json_data = json.dumps(data)
        post_data = json_data.encode('utf-8')
        request = urllib2.Request(url, post_data, headers)
        result = urllib2.urlopen(request)
        return result.read()
    except:
        return "error in kodi"
#########################################################################


def notif_msg(msg):
    # icon=APPDIR+"/notebox.png"
    os.system("notify-send PyLinuxBot \""+msg+"\"")

###################################################################


def getCurrIP():
    currip = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
    #print([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
    return currip


def checkrequest(line):
    global scommand
    global G_XDOTOOL
    global G_MOVIELIST
    global outmessage
    linesplit = line.split(" ")
    srequest = linesplit[1]

    if srequest == "/kodinext":
        print "next Command"
        scommand = "kodinext"
        #cmd = "xdotool getactivewindow key Right"
        data = {"jsonrpc":"2.0","id":"1","method":"Player.Seek", "params": {"value": "smallforward", "playerid": 1}}
        doKodi(data)
        outmessage = "OK"
        return 0
    elif srequest == "/kodiback":
        print "back Command"
        scommand = "kodiback"
        data = {"jsonrpc":"2.0","id":"1","method":"Player.Seek", "params": {"value": "smallbackward", "playerid": 1}}
        #cmd = "xdotool getactivewindow key Left"
        doKodi(data)
        outmessage = "OK"
        return 0
    elif srequest == "/up":
        print "Up Command"
        scommand = "up"
        cmd = "xdotool getactivewindow key Up"
        os.system(cmd)
        return 0
    elif srequest == "/down":
        print "Down Command"
        scommand = "down"
        cmd = "xdotool getactivewindow key Down"
        os.system(cmd)
        return 0
    elif srequest == "/kodiexit":
        print "Kodiexit Command"
        scommand = "kodiexit"
        data = {"jsonrpc":"2.0","id":"1","method":"System.Shutdown"}
        #cmd = "xdotool getactivewindow type s"
        doKodi(data)
        outmessage = "OK"
        #os.system(cmd)
        return 0
    elif srequest == "/escape":
        print "escape Command"
        scommand = "escape"
        cmd = "xdotool getactivewindow key Escape"
        os.system(cmd)
        return 0
    elif srequest == "/enter":
        print "escape Command"
        scommand = "escape"
        cmd = "xdotool getactivewindow key KP_Enter"
        os.system(cmd)
        return 0
    elif srequest.startswith("/kodiplaymovie"):
        print "playmovie Command"
        scommand = "kodiplaymovie"
        m = re.search('/.*\?movie=(.*)', srequest)
        if m:
            movielabel = m.group(1)
            j = 0
            for i in G_MOVIELIST:
                #print "DD1 ", G_MOVIELIST[j]
                if G_MOVIELIST[j].startswith(movielabel):
                    arritem = G_MOVIELIST[j].split(":")
                    #print "DD1 ", arritem[0], arritem[1]
                    data = {"jsonrpc":"2.0","id":"1","method":"Player.Open","params":{"item":{"file": arritem[1]}}}
                    #print json.dumps(data)
                    doKodi(data)
                    outmessage = "movie " + arritem[0] + " playing"
                    return 0
                j += 1
            outmessage = "movie not found!"
            return 0
        else:
            outmessage = "error: Wrong parameters!"
        return 0
    elif srequest == "/kodigetmovies":
        print "getmovies Command"
        scommand = "kodigetmovies"
        data = {"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": { "properties" : [ "file" ], "sort": { "order": "ascending", "method": "label" } }, "id": "libMovies"}
        moviesdata = doKodi(data)
        if not moviesdata.startswith("error"):
            j = json.loads(moviesdata)
            arr = j["result"]
            movies = arr["movies"]
            outmessage = ""
            j = 0
            for i in movies:
                if j == 0:
                    outmessage = movies[j]['label'] + ":" + movies[j]['file']
                #elif i == len(movies)-1:
                    #outmessage = outmessage + "," + movies[j]['file']
                else:
                    outmessage = outmessage + "," + movies[j]['label'] + ":" + movies[j]['file']
                j = j + 1
            G_MOVIELIST = outmessage.split(",")
        else:
            outmessage = moviesdata
        return 0
    elif srequest == "/kodipause":
        print "pause Command"
        scommand = "kodipause"
        data = {"jsonrpc":"2.0","method":"Player.PlayPause","params":{"playerid":1},"id":1}
        doKodi(data)
        return 0
    elif srequest == "/plus":
        print "+ Command"
        scommand = "plus"
        cmd = "xdotool getactivewindow type '+'"
        os.system(cmd)
        return 0
    elif srequest == "/minus":
        print "- Command"
        scommand = "minus"
        cmd = "xdotool getactivewindow type '-'"
        os.system(cmd)
        return 0
    elif srequest == "/rewind":
        print "rewind Command"
        scommand = "rewind"
        cmd = "xdotool getactivewindow type 'R'"
        os.system(cmd)
        return 0
    elif srequest == "/fforward":
        print "fast forward Command"
        scommand = "fastforward"
        cmd = "xdotool getactivewindow type 'F'"
        os.system(cmd)
        return 0
    elif srequest == "/volup":
        print "volume up Command"
        scommand = "volup"
        cmd = "amixer -D pulse sset Master 10%+"
        os.system(cmd)
        return 0
    elif srequest == "/voldown":
        print "volume down Command"
        scommand = "voldown"
        cmd = "amixer -D pulse sset Master 10%-"
        os.system(cmd)
        return 0
    elif srequest == "/mute":
        print "Mute Command"
        scommand = "mute"
        cmd = "amixer -D pulse sset Master mute"
        os.system(cmd)
        return 0
    elif srequest == "/unmute":
        print "Unmute Command"
        scommand = "unmute"
        cmd = "amixer -D pulse sset Master unmute"
        os.system(cmd)
        return 0
    elif srequest == "/runplayer":
        print "Unmute Command"
        scommand = "unmute"
        cmd = "totem &"
        os.system(cmd)
        return 0
    elif srequest == "/ping":
        print "ping Command"
        scommand = "ping"
        return 0
    else:
        print "DEBUG: returning 1"
        return 1
# ------------------------------------------------


HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8888  # Arbitrary non-privileged port
scommand = ""
outmessage = ""
IP_ADDR = ""

IP_ADDR = getCurrIP()

if IP_ADDR == "":
    notif_msg("No IP found! Aborting...")
    print "PyLinuxBot: No network card enabled. Aborting...\n"
    sys.exit(2)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print 'pybot: Socket created'

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

notif_msg("PylinuxBot: Running with IP: " + IP_ADDR + " port 8888")

print ("PylinuxBot: Running with IP: " + IP_ADDR + " port 8888")
print 'pybot: Socket bind complete'

# Start listening on socket
s.listen(1)
print 'pybot: Socket now listening'

# now keep talking with the client
while 1:
    # wait to accept a connection - blocking call
    conn, addr = s.accept()
    cfile = conn.makefile('rw', 0)
    print 'pybot: Connected with ' + addr[0] + ':' + str(addr[1])
    line = cfile.readline().strip()
    print "Request: ", line
    status = checkrequest(line)
    if status == 0:
        cfile.write('HTTP/1.0 200 OK\n\n')
        cfile.write('<html><head><title>Welcome %s!</title></head>' % (str(addr)))
        if scommand.startswith("kodi"):
            cfile.write('<body><p>%s</p><body></html>' % outmessage)
        else:
            cfile.write('<body><h1>Command %s proccessed...</h1><body></html>' % scommand)
    else:
        print "DEBUG: HTTP 400"
        cfile.write('HTTP/1.0 404 Not Found\n\n')
        cfile.write('<html><body>404 Not Found</body></html>')
    # cfile.flush()
    cfile.close()
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()
s.close()
