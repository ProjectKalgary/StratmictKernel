import bteve as eve
import time

limit = 34
textmode = 0

updaterate = .0
gd = ""
r = 0x00
g = 0x00
b = 0xFF
autoupdate = True

mem = []

def settextmode(i):
    global textmode
    if(i <= 1 and i >= 0):
        textmode = i

def setautoupdate(b):
    global autoupdate
    autoupdate = b

def setgd(g):
    global gd
    gd = g

def setrgb(nr, ng, nb):
    global r, g, b
    r = nr
    g = ng
    b = nb
    aupdate()

def aupdate():
    global autoupdate
    if autoupdate:
        update()
def customupdate(cmem):
    global updaterate
    gd.ClearColorRGB(r, g, b)
    gd.Clear()
    if(textmode == 0):
        global limit
        y = 20
        limit = 34
        for i in cmem:
            gd.cmd_text(35, y, 22, 0, i)
            y += 20
            time.sleep(updaterate)

    elif(textmode == 1):
        global limit
        y = 15
        limit = 19
        for i in cmem:
            gd.cmd_text(35, y, 25, 0, i)
            y += 35
            time.sleep(updaterate)

    gd.swap()

def update():
    global mem, updaterate
    gd.ClearColorRGB(r, g, b)
    gd.Clear()
    if(textmode == 0):
        global limit
        y = 20
        limit = 34
        for i in mem:
            gd.cmd_text(35, y, 22, 0, str(i))
            y += 20
            time.sleep(updaterate)

    elif(textmode == 1):
        global limit
        y = 15
        limit = 19
        for i in mem:
            gd.cmd_text(35, y, 25, 0, i)
            y += 35
            time.sleep(updaterate)

    gd.swap()

def clear():
    global mem
    mem = []
    aupdate()

def writeline(str):
    global mem
    global limit
    mem.append(str)
    if len(mem) >= limit:
        for i in range(len(mem) - limit):
            del mem[0]
    aupdate()

def write(str):
    global mem
    mem[len(mem)-1] += str
    aupdate()


