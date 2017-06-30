import socket
import sys
import os
import subprocess

XDOTOOL = "xdotool"

#########################################################


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
    global XDOTOOL
    global outmessage
    linesplit = line.split(" ")
    srequest = linesplit[1]

    if srequest == "/next":
        print "next Command"
        scommand = "next"
        cmd = "xdotool getactivewindow key Right"
        os.system(cmd)
        return 0
    elif srequest == "/back":
        print "back Command"
        scommand = "back"
        cmd = "xdotool getactivewindow key Left"
        os.system(cmd)
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
        cmd = "xdotool getactivewindow type s"
        os.system(cmd)
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
    elif srequest == "/pause":
        print "pause Command"
        scommand = "pause"
        cmd = "xdotool getactivewindow type ' '"
        os.system(cmd)
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
        #
    elif srequest == "/startppt":
        print "startppt Command"
        scommand = "startppt"
        cmd = "xdotool key F5"
        os.system(cmd)
        return 0
    elif srequest == "/getpptxfile":
        print "getpptxdata Command"
        scommand = "getpptxdata"
        PPT_PID = subprocess.check_output("wmctrl -lp | grep pptx | tr -s " " | cut -d" " -f 3", shell=True)
        PPT_FILE = subprocess.check_output("lsof -Fn -p " + PPT_PID + " | grep pptx", shell=True)
        outmessage = PPT_FILE
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

#try:
#    # WIFICARD = subprocess.check_output("ifconfig | grep -E ^enx | cut -d' ' -f 1", shell=True)
#    WIFICARD = subprocess.check_output("ifconfig | grep -E ^w | cut -d' ' -f 1", shell=True)
#except:
#    WIFICARD = ""

#WIFICARD = WIFICARD.rstrip('\n')
#print "dd: " + WIFICARD
#if WIFICARD == "":
if IP_ADDR == "":
    notif_msg("No IP found! Aborting...")
    print "PyLinuxBot: No network card enabled. Aborting...\n"
    sys.exit(2)

#IP_ADDR = subprocess.check_output("ifconfig "+WIFICARD+" | grep 'inet addr' | tr -s ' ' | cut -d' ' -f 3 | cut -d: -f 2", shell=True)

notif_msg("PylinuxBot: Running with IP: " + IP_ADDR + " port 8888")

print ("PylinuxBot: Running with IP: " + IP_ADDR + " port 8888")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print 'pybot: Socket created'

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

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
        if scommand == "getpptxdata":
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
