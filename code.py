import os
import bteve as eve
import time
import sys

gd = eve.Gameduino()
gd.init()

warningtime = 1
sleeptime = .3
afterboot = 1

boottxt = "Loading.."

global displaylogo
displaylogo = False

warnings = []

autorun = ""
osname = ""
osver = ""

def BootScreenUpdate():
    gd.ClearColorRGB(0x20, 0x40, 0x20)
    gd.Clear()
    gd.cmd_text(gd.w//2, (gd.h//4)*3, 31, eve.OPT_CENTER, osname)
    gd.cmd_text(gd.w // 2, (gd.h // 4)*3+50, 31, eve.OPT_CENTER, osver)
    gd.cmd_text(gd.w // 2, (gd.h // 4)*3+100, 22, eve.OPT_CENTER, boottxt)
    print(boottxt)

    if displaylogo:
        gd.cmd_loadimage(0, 0)
        gd.load(open("/sd/boot/logo.png", "rb"))
        gd.Begin(eve.BITMAPS)
        gd.Vertex2f(gd.w//2-75, gd.h//2-75)

    gd.swap()

def BootError(errmsg, exitcode):
    gd.ClearColorRGB(0xFF, 0x00, 0x00)
    gd.Clear()
    gd.cmd_text(gd.w//2, (gd.h//4), 31, eve.OPT_CENTER, "There was a problem booting.")
    gd.cmd_text(gd.w // 2, (gd.h // 2), 25, eve.OPT_CENTER, errmsg)
    gd.cmd_text(gd.w//2, (gd.h//4)*3+100, 22, eve.OPT_CENTER, "Exit Code: " + exitcode)
    gd.swap()

def Boot():
    global sleeptime
    global afterboot
    global boottxt

    boottxt = "Detecting SD Storage..."
    BootScreenUpdate()
    time.sleep(sleeptime)

    dirinfo = os.listdir("/")
    if 'sd' in dirinfo:
        boottxt = "Detecting SD Storage...Complete"
        BootScreenUpdate()
    else:
        BootError("SD Storage could not be detected.", "-1")
        return -1

    time.sleep(sleeptime)
    boottxt = "Detecting /sd/boot directory"
    BootScreenUpdate()
    time.sleep(sleeptime)

    dirinfo = os.listdir("/sd")
    if 'boot' in dirinfo:
        boottxt = "Detecting /sd/boot directory...Complete"
        BootScreenUpdate()
    else:
        BootError("/sd/boot doesn't exist.", "-1")
        return -1

    time.sleep(sleeptime)
    boottxt = "Loading /sd/boot/deviceinfo file..."
    BootScreenUpdate()
    time.sleep(sleeptime)

    dirinfo = os.listdir("/sd/boot")
    if 'deviceinfo' in dirinfo:
        global osname
        global osver
        boottxt = "Loading /sd/boot/deviceinfo file...Complete"
        global devinfo
        devinfof = open("/sd/boot/deviceinfo", "rt")
        devinfo = devinfof.read()
        devinfof.close()
        devinfo = devinfo.split(",")
        osname = devinfo[0]
        osver = devinfo[1]
        print(osname)
        print(osver)
        BootScreenUpdate()
    else:
        BootError("Device Info could not be found.", "-2")
        return -2

    time.sleep(sleeptime)
    boottxt = "Loading kernelinfo..."
    BootScreenUpdate()
    time.sleep(sleeptime)

    dirinfo = os.listdir("/")
    if 'kernelinfo' in dirinfo:
        boottxt = "Loading kernelinfo...Complete"
        global devinfo
        global kernelinfo
        kernelinfof = open("/kernelinfo", "rt")
        kernelinfo = kernelinfof.read()
        kernelinfof.close()
        kernelinfo = kernelinfo.split(",")
        if kernelinfo[0] != devinfo[2]:
            warnings.append("KERNEL MISMATCH -- MIGHT NOT BE COMPATIBLE")
        if kernelinfo[1] != devinfo[3]:
            warnings.append("VERSION MISMATCH -- MIGHT NOT BE COMPATIBLE")
        BootScreenUpdate()
    else:
        BootError("Kernel Info could not be found.", "-3")
        return -3

    time.sleep(sleeptime)
    boottxt = "Loading /sd/boot/logo.png file..."
    BootScreenUpdate()
    time.sleep(sleeptime)

    dirinfo = os.listdir("/sd/boot")
    if 'logo.png' in dirinfo:
        boottxt = "Loading /sd/boot/logo.png file...Complete"
        global displaylogo
        displaylogo = True
        logo = open("/sd/boot/logo.png", "rb")
        global logobytes
        logobytes = logo.read()
        logo.close()
        BootScreenUpdate()

    else:
        boottxt = "Loading /sd/boot/logo.png file...Failed"
        BootScreenUpdate()

    time.sleep(sleeptime)
    boottxt = "Loading /sd/boot/autorun.py/mpy file..."
    BootScreenUpdate()
    time.sleep(sleeptime)

    dirinfo = os.listdir("/sd/boot")
    if 'autorun.py' in dirinfo or 'autorun.mpy' in dirinfo:
        boottxt = "Loading /sd/boot/autorun.py/mpy file...Complete"
        sys.path.insert('1', "/sd")
        global autorun
        import boot.autorun as autorun
        BootScreenUpdate()
    else:
        BootError("Autorun file could not be found.", "-2")
        return -3

    for i in warnings:
        global warningtime
        boottxt = i
        BootScreenUpdate()
        time.sleep(warningtime)

    time.sleep(sleeptime)
    boottxt = "Done"
    BootScreenUpdate()
    time.sleep(afterboot)
    return 0

bootreturn = Boot()
if(bootreturn == 0):
    global kernelinfo
    global devinfo
    autorun.PRG_INIT([gd, devinfo, kernelinfo])

# Stop from looping
while True:
    time.sleep(1)
