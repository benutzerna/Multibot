### GUI ###
import tkinter as tk
from tkinter import ttk
import tkinter
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog as fd

import pyautogui
import time
import threading

import sys
import os
import subprocess
from io import BytesIO
from pywinauto import keyboard
import pywinauto
import pyperclip
from PIL import Image

import win32clipboard as clip
import win32con

##################################
######### GLOBAL VARS ############
##################################

T_global_pause = ""
root = tk.Tk()

tgs_running     = False

r_clock_thread  = ""
proc_1_thread   = ""
proc_2_thread   = ""

_no_media_tag = "_NO_MEDIA_TGSB3_"

_name = "Telegram Multibot"
_version = "(1.0)"
_height = 830
_width = 400

shill_2_enabled = tk.StringVar()

TG_PATH_GLOBAL = ""
global_counter = 0

rounds_completed_counter = 0
# Betritt wieder Shill-Func von Proc2() aus
global_reentry = False
#############################


########## Kalibrierung ##########

_settings_x = 0
_settings_y = 0
_account1_x = 0
_account1_y = 0
_account2_x = 0
_account2_x = 0

multiple_accs_enabled = tk.StringVar()

########## clock vars ############
r_clock_thread = 0
_days = 0
_hours = 0
_minutes = 0
_seconds = 0
_dayss = "0"
_hourss = "0"
_minutess = "0"
_secondss = "0"

#######################################
### TGSB3_WEIMAR_CONFIG.txt (UTF-8) ###
#######################################

# config_datei
T_CONTENT_FILE_PATH = os.path.dirname(os.path.realpath(__file__)) + "\\TGSB3CONFIG.txt"

############################### Shilltxt 1 ###############################

# Shilltxt 1
T_CONTENT_SHILL_TXT_1           = ""
T_CONTENT_CHANNEL_1             = ""
T_CONTENT_PAUSE_1               = ""
T_CONTENT_MEDIA_1               = ""
T_CONTENT_MEDIA_1_BYTES         = ""
T_CONTENT_VIDEO_1_COORDS        = "0,0"

############################### Shilltxt 2 ###############################

T_CONTENT_SHILL_TXT_2           = ""
T_CONTENT_CHANNEL_2             = ""
T_CONTENT_PAUSE_2               = ""
T_CONTENT_MEDIA_2               = ""
T_CONTENT_MEDIA_2_BYTES         = ""
T_CONTENT_SHILL_ENABLED         = ""
T_CONTENT_VIDEO_2_COORDS        = "0,0"

############################### Config ###############################

T_CONTENT_USER_XY               = "0,0"
T_CONTENT_ACC_1_XY              = "0,0"
T_CONTENT_ACC_2_XY              = "0,0"
T_CONTENT_CALIBRE_ENABLED       = ""
T_CONTENT_GLOBAL_PAUSE          = ""

##################################
######## GLOBAL VARS ENDE ########
##################################


##################################
###### BUTTON KALIBRIERUNG #######
##################################

def calibre_BTN_ACTION(arg):
    print(arg)

def calibre_BTN_ENTER_SETTINGS(arg):
    global T_CONTENT_USER_XY
    _settings_x, _settings_y = pyautogui.position()
    settings_BTN.unbind('<Return>')
    settings_BTN.configure(text="Users OK")
    T_CONTENT_USER_XY = str(_settings_x) + "," + str(_settings_y)
    print(T_CONTENT_USER_XY)

def calibre_BTN_ENTER_ACC_1(arg):
    global T_CONTENT_ACC_1_XY
    _account1_x, _account1_y = pyautogui.position()
    account1_BTN.unbind('<Return>')
    account1_BTN.configure(text="Acc 1 OK")
    T_CONTENT_ACC_1_XY = str(_account1_x) + "," + str(_account1_y)
    print(calibre_BTN_ENTER_ACC_1)

def calibre_BTN_ENTER_ACC_2(arg):
    global T_CONTENT_ACC_2_XY
    _account2_x, _account2_y = pyautogui.position()
    account2_BTN.configure(text="Acc 2 OK")
    T_CONTENT_ACC_2_XY = str(_account2_x) + "," + str(_account2_y)
    print(T_CONTENT_ACC_2_XY)

def calibre_TOGGLE(param):
    if param.get() == "enabled":
        print("calibre_TOGGLE() - enabled")

        settings_BTN.bind('<Return>', calibre_BTN_ENTER_SETTINGS)
        account1_BTN.bind('<Return>', calibre_BTN_ENTER_ACC_1)
        account2_BTN.bind('<Return>', calibre_BTN_ENTER_ACC_2)

        settings_BTN.state(['!disabled'])
        account1_BTN.state(['!disabled'])
        account2_BTN.state(['!disabled'])

    if param.get() == "disabled":
        print("calibre_TOGGLE() - disabled")

        settings_BTN.configure(text="Users")
        account1_BTN.configure(text="Account 1")
        account2_BTN.configure(text="Account 2")

        settings_BTN.unbind('<Return>')
        account1_BTN.unbind('<Return>')
        account2_BTN.unbind('<Return>')

        settings_BTN.state(['disabled'])
        account1_BTN.state(['disabled'])
        account2_BTN.state(['disabled'])

    print("calibre_TOGGLE()")

##################################
#### BUTTON KALIBRIERUNG ENDE ####
##################################

#######################################################
########## MEDIA 1 SELECTION ##########################
#######################################################

def VIDEO1_COORDS(args):
    global T_CONTENT_VIDEO_1_COORDS
    _settings_x, _settings_y = pyautogui.position()
    load_video_1_BTN.unbind('<Return>')
    load_video_1_BTN.configure(text="X,Y SET")
    T_CONTENT_VIDEO_1_COORDS = str(_settings_x) + "," + str(_settings_y)
    print(T_CONTENT_VIDEO_1_COORDS)

def select_video_file_1():
    load_video_1_BTN.bind('<Return>', VIDEO1_COORDS)

def select_file_1():
    print("select_file_1()")
    global T_CONTENT_MEDIA_1

    filetypes = (
        ('Images', '*.*'),
        ('Videos', '*.mp4')
    )

    filename = fd.askopenfilename(
        title='Open media file',
        filetypes=filetypes)
    
    T_CONTENT_MEDIA_1 = filename

    if T_CONTENT_MEDIA_1 != "":
        if T_CONTENT_MEDIA_1.split(".")[len(T_CONTENT_MEDIA_1.split("."))-1] == "mp4" or T_CONTENT_MEDIA_1.split(".")[len(T_CONTENT_MEDIA_1.split("."))-1] == "GIF" or T_CONTENT_MEDIA_1.split(".")[len(T_CONTENT_MEDIA_1.split("."))-1] == "gif":
            load_media_1_BTN.configure(text="VID OK")
            load_video_1_BTN.configure(text="VID X,Y")
            load_video_1_BTN.configure(state=tk.ACTIVE)
            print(T_CONTENT_MEDIA_1)
        else:
            load_media_1_BTN.configure(text="IMG OK")
            load_video_1_BTN.configure(text="NO VID")
            load_video_1_BTN.configure(state=tk.DISABLED)
            print(T_CONTENT_MEDIA_1)


#######################################################
########## MEDIA 2 SELECTION ##########################
#######################################################

def VIDEO2_COORDS(args):
    global T_CONTENT_VIDEO_2_COORDS
    _settings_x, _settings_y = pyautogui.position()
    load_video_2_BTN.unbind('<Return>')
    load_video_2_BTN.configure(text="X,Y SET")
    T_CONTENT_VIDEO_2_COORDS = str(_settings_x) + "," + str(_settings_y)
    print(T_CONTENT_VIDEO_2_COORDS)

def select_video_file_2():
    load_video_2_BTN.bind('<Return>', VIDEO2_COORDS)

def select_file_2():
    print("select_file_2()")
    global T_CONTENT_MEDIA_2

    filetypes = (
        ('Images', '*.*'),
        ('Videos', '*.mp4')
    )

    filename = fd.askopenfilename(
        title='Open media file',
        filetypes=filetypes)
    
    T_CONTENT_MEDIA_2 = filename

    if T_CONTENT_MEDIA_2 != "":
        if T_CONTENT_MEDIA_2.split(".")[len(T_CONTENT_MEDIA_2.split("."))-1] == "mp4" or T_CONTENT_MEDIA_2.split(".")[len(T_CONTENT_MEDIA_2.split("."))-1] == "GIF" or T_CONTENT_MEDIA_2.split(".")[len(T_CONTENT_MEDIA_2.split("."))-1] == "gif":
            load_media_2_BTN.configure(text="VID OK")
            load_video_2_BTN.configure(text="VID X,Y")
            load_video_2_BTN.configure(state=tk.ACTIVE)
            print(T_CONTENT_MEDIA_2)
        else:
            load_media_2_BTN.configure(text="IMG OK")
            load_video_2_BTN.configure(text="NO VID")
            load_video_2_BTN.configure(state=tk.DISABLED)
            print(T_CONTENT_MEDIA_2)

###########################################
########### MEDIA SELECTION ENDE ##########
###########################################

#################################
############ SHILL 2 ############
#################################

def shill_2_TOGGLE(param):
    if param.get() == "enabled":
        print("shill_2_TOGGLE() - enabled")
        shill_pause_2.configure(state=tk.NORMAL)
        load_media_2_BTN.configure(state=tk.NORMAL)

    if param.get() == "disabled":
        print("shill_2_TOGGLE() - disabled")

        shill_pause_2.configure(state=tk.DISABLED)
        load_media_2_BTN.configure(state=tk.DISABLED)

    print("shill_2_TOGGLE()")

#################################
######### SHILL 2 ENDE ##########
#################################

#################################
####### BUTTON GLOBAL ACT #######
#################################

############################
####### UHR
############################
def r_clock():
    print("r_clock()")
    global tgs_running, r_clock_thread

    while tgs_running == True:
        global _days
        global _hours
        global _minutes
        global _seconds

        global _dayss
        global _hourss
        global _minutess
        global _secondss

        time.sleep(1)
        _seconds += 1

        if _seconds == 60:
            _seconds = 0
            _minutes += 1
            if _minutes == 60:
                _minutes = 0
                _hours += 1
                if _hours == 24:
                    _hours = 0
                    _days += 1
                        
        if _seconds < 10:
            _secondss = "0" + str(_seconds)
        if _seconds >= 10:
            _secondss = str(_seconds)

        if _minutes < 10:
            _minutess = "0" + str(_minutes)
        if _minutes >= 10:
            _minutess = str(_minutes)

        if _hours < 10:
            _hourss = "0" + str(_hours)
        if _hours >= 10:
            _hourss = str(_hours)
            
        if _days < 10:
            _dayss = "0" + str(_days)
        if _days >= 10:
            _dayss = str(_days)

        kaatschklacks = _dayss + ":" + _hourss + ":" + _minutess + ":" + _secondss
        runtime_Label.configure(text=kaatschklacks)

        # break BEENDET THREAD
        # break

#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
######################################## SHILLEN ######################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################

def shill_BTN_ACTION():
    print("shill_BTN_ACTION()")

    global tgs_running, global_reentrym, rounds_completed_counter, global_reentry
    global r_clock_thread, proc_1_thread
    global shill_BTN, load_BTN, save_BTN, pause_BTN, load_media_1_BTN, load_media_2_BTN
    global T_CONTENT_CHANNEL_1, T_CONTENT_CHANNEL_2, _no_media_tag
    global T_CONTENT_SHILL_TXT_1, T_CONTENT_SHILL_TXT_2
    global T_CONTENT_PAUSE_1, T_CONTENT_PAUSE_2
    global T_CONTENT_MEDIA_1, T_CONTENT_MEDIA_2
    global TG_PATH_GLOBAL, IMAGE_BYTES, IMAGE_BYTES_2, TG_PATH_GLOBAL
    global shill_pause_1, shill_pause_2
    global global_pause, T_global_pause

    #######################################
    # Button-Ansicht, TG-Pfad beziehen
    #######################################
    if global_reentry == False:
        pause_BTN.configure(state=tk.ACTIVE)
        shill_BTN.configure(state=tk.DISABLED)
        load_BTN.configure(state=tk.DISABLED)
        save_BTN.configure(state=tk.DISABLED)

        load_media_1_BTN.configure(state=tk.DISABLED)
        load_media_2_BTN.configure(state=tk.DISABLED)

        cmd = subprocess.Popen(["powershell.exe", "Get-Process Telegram | Select-Object Path"], stdout=subprocess.PIPE, shell=True)
        (out, err) = cmd.communicate()
        T_global_pause = int(global_pause.get('1.0', tk.END).rstrip("\n")) 
        TG_PATH_GLOBAL = "C:" + str(out).split("C:")[1].split(".exe")[0] + ".exe"
        
        TG_PATH_GLOBAL = "\""+ TG_PATH_GLOBAL.replace("\\\\", "/") + "\""
        print("program output:" + str(TG_PATH_GLOBAL))

    #################################################################################
    ## Mediendateien einmalig in die Zwischenablage kopieren - wenn kein video
    #################################################################################
        if T_CONTENT_MEDIA_1 != "" and T_CONTENT_MEDIA_1.split(".")[1] != "mp4":
            image       = Image.open(T_CONTENT_MEDIA_1)
            output      = BytesIO()
            image.convert('RGB').save(output, 'BMP')
            IMAGE_BYTES = output.getvalue()[14:]
            output.close()

        if T_CONTENT_MEDIA_2 != "" and T_CONTENT_MEDIA_2.split(".")[1] != "mp4":
            image           = Image.open(T_CONTENT_MEDIA_2)
            output          = BytesIO()
            image.convert('RGB').save(output, 'BMP')
            IMAGE_BYTES_2   = output.getvalue()[14:]
            output.close()

    #######################################################################################################
    # Liste 1                                                                                            ##
    #######################################################################################################
    ## Shilltext 1                                                                                       ##
    T_CONTENT_SHILL_TXT_1 = shill_txt_1.get('1.0', tk.END).rstrip("\n")                                  ##
                                                                                                         ##                                            
    ## Kanalliste 1                                                                                      ##
    _t = shill_channel_1.get('1.0', tk.END).rstrip("\n").split("\n")                                     ##
    T_CONTENT_CHANNEL_1 = []                                                                             ##
                                                                                                         ##
    _counter = 0                                                                                         ##
    for _item in _t:                                                                                     ##
        # Falls ein nomediatag gefunden wird                                                             ##
        if _item.find(_no_media_tag) != -1:                                                              ##
            T_CONTENT_CHANNEL_1.append(_item + ",NO")                                                    ##
            _counter += 1                                                                                ##
        # Falls kein nomediatag gefunden wurde                                                           ##
        elif _item.find(_no_media_tag) == -1:                                                            ##
            T_CONTENT_CHANNEL_1.append(_item + ",YES")                                                   ##
                                                                                                         ##
    ## Pause 1                                                                                           ##
    T_CONTENT_PAUSE_1 = int(shill_pause_1.get('1.0', tk.END).rstrip("\n"))                               ##
    #######################################################################################################
    # Liste 1 - ENDE                                                                                     ##
    #######################################################################################################



    #######################################################################################################
    # Liste 2 - falls enabled                                                                            ##
    #######################################################################################################
    if shill_2_enabled.get() == "enabled":                                                               ##
        print("shill_2_enabled ENABLED")                                                                 ##
                                                                                                         ##
        ## Shilltext 2                                                                                   ##
        T_CONTENT_SHILL_TXT_2 = shill_txt_2.get('1.0', tk.END).rstrip("\n")                              ##
                                                                                                         ##
        ## Kanalliste 2                                                                                  ##
        _t = shill_channel_2.get('1.0', tk.END).rstrip("\n").split("\n")                                 ##
        T_CONTENT_CHANNEL_2 = []                                                                         ##
                                                                                                         ##
        _counter = 0                                                                                     ##
        for _item in _t:                                                                                 ##
            # Falls ein nomediatag gefunden wird                                                         ##
            if _item.find(_no_media_tag) != -1:                                                          ##
                T_CONTENT_CHANNEL_2.append(_item + ",NO")                                                ##
                _counter += 1                                                                            ##
            # Falls kein nomediatag gefunden wurde                                                       ##
            elif _item.find(_no_media_tag) == -1:                                                        ##
                T_CONTENT_CHANNEL_2.append(_item + ",YES")                                               ##
                                                                                                         ##
        ## Pause 2                                                                                       ##
        T_CONTENT_PAUSE_2 = int(shill_pause_2.get('1.0', tk.END).rstrip("\n"))                           ##
    #######################################################################################################
    # Liste 2 - ENDE                                                                                     ##
    #######################################################################################################

    ##########################
    # UHRENSTEUERUNG
    ##########################
    if tgs_running == False:
        try:
            tgs_running = True
            print("start r_clock Thread")
            r_clock_thread = threading.Thread(target=r_clock)
            r_clock_thread.start()
            r_clock_thread = ""
        except:
            print ("Error: unable to start thread")

    ##########################
    # Steuerung Proc 1
    ##########################
    try:
        print("start r_clock Thread")
        proc_1_thread = threading.Thread(target=shill_1_proc)
        proc_1_thread.start()
        proc_1_thread = ""
        rounds_completed_counter += 1
        rounds_completed_Label.configure(text="Round completed: " + str(rounds_completed_counter))
    except:
        print ("Error: unable to start thread")

##########################
# Shill 1 Proc           #
##########################
def shill_1_proc():
    print("shill_1_proc()")
    
    global global_counter, proc_2_thread, kickpb1_thread, T_global_pause, TG_PATH_GLOBAL
    global T_CONTENT_USER_XY, T_CONTENT_ACC_1_XY, T_CONTENT_ACC_2_XY, global_status_label

    #####################################################################################################################
    # Zu Account 1 navigieren, mehrere Texte geshillt werden                                                           ##
    #####################################################################################################################
    if shill_2_enabled.get() == "enabled":
        _set_tx = T_CONTENT_USER_XY.split(",")[0]
        _set_ty = T_CONTENT_USER_XY.split(",")[1]
        pywinauto.mouse.press(button='left', coords=(int(_set_tx), int(_set_ty)))
        pywinauto.mouse.release(button='left', coords=(int(_set_tx), int(_set_ty)))

        time.sleep(1)

        _acc1_tx = T_CONTENT_ACC_1_XY.split(",")[0]
        _acc1_ty = T_CONTENT_ACC_1_XY.split(",")[1]
        pywinauto.mouse.press(button='left', coords=(int(_acc1_tx), int(_acc1_ty)))
        pywinauto.mouse.release(button='left', coords=(int(_acc1_tx), int(_acc1_ty)))

        time.sleep(1)

        pywinauto.mouse.press(button='left', coords=(int(_acc1_tx), int(_acc1_ty)))
        pywinauto.mouse.release(button='left', coords=(int(_acc1_tx), int(_acc1_ty)))

        time.sleep(1)

    __counter = 0
    #####################################################################################################################
    # Posts abetzen - Liste 1                                                                                          ##
    #####################################################################################################################
    for channel in T_CONTENT_CHANNEL_1:

        __counter += 1
        _current_state = "LIST 1 - " + str(__counter) + " of " + str(len(T_CONTENT_CHANNEL_1)) + " shilled"
        print(_current_state)
        global_status_label = ttk.Label(root, text=_current_state)

        # Channel aufrufen
        os.system(TG_PATH_GLOBAL + " -- tg://resolve?domain=" + channel.split(",")[0])
        time.sleep(1)

        #####################################################################
        # Mediendatei - wenn definiert - in die Zwisenablage - KEIN VIDEO
        #####################################################################
        if T_CONTENT_MEDIA_1 != "" and channel.split(",")[1] != "NO" and T_CONTENT_MEDIA_1.split(".")[len(T_CONTENT_MEDIA_1.split("."))-1] != "mp4" or T_CONTENT_MEDIA_1.split(".")[len(T_CONTENT_MEDIA_1.split("."))-1] != "GIF" or T_CONTENT_MEDIA_1.split(".")[len(T_CONTENT_MEDIA_1.split("."))-1] != "gif":
            clip.OpenClipboard()
            clip.EmptyClipboard()
            clip.SetClipboardData(win32con.CF_DIB, IMAGE_BYTES)
            clip.CloseClipboard()

            pyautogui.hotkey('ctrl','a')
            time.sleep(0.2)
            pyautogui.hotkey('delete')
            time.sleep(0.2)
            pyautogui.hotkey('ctrl','v')
            time.sleep(0.5)

            # Shilltext in die Zwischenablage
            pyperclip.copy(T_CONTENT_SHILL_TXT_1)
            time.sleep(0.1)
            pyautogui.hotkey('ctrl','v')
            time.sleep(0.2)
            keyboard.send_keys("{ENTER}")
            time.sleep(0.2)

            try:
                # Thread einmal ausführen
                global_counter += 1
                # Progressbarwert berechnen
                _t = global_counter/len(T_CONTENT_CHANNEL_1) * 100
                _t = '{:.2f}%'.format(_t)
                # Berechnung zu Ende
                kickpb1_thread = threading.Thread(target=kickpb1, args=(_t,))
                kickpb1_thread.start()
                kickpb1_thread = ""
            except:
                print ("Error: unable to start thread")
        #########################################
        # Mediendatei - wenn definiert - VIDEO!
        #########################################
        elif T_CONTENT_MEDIA_1 != "" and T_CONTENT_MEDIA_1.split(".")[len(T_CONTENT_MEDIA_1.split("."))-1] == "mp4" or T_CONTENT_MEDIA_1.split(".")[len(T_CONTENT_MEDIA_1.split("."))-1] == "GIF" or T_CONTENT_MEDIA_1.split(".")[len(T_CONTENT_MEDIA_1.split("."))-1] == "gif":
            print("mit video")
            print(T_CONTENT_VIDEO_1_COORDS)
            _tx = T_CONTENT_VIDEO_1_COORDS.split(",")[0]
            _ty = T_CONTENT_VIDEO_1_COORDS.split(",")[1]

            #pywinauto.mouse.move()
            
            pywinauto.mouse.press(button='left', coords=(int(_tx), int(_ty)))
            pywinauto.mouse.release(button='left', coords=(int(_tx), int(_ty)))
            pyautogui.hotkey('ctrl','c')
            time.sleep(0.1)
            os.system(TG_PATH_GLOBAL + " -- tg://resolve?domain=" + channel.split(",")[0])
            time.sleep(1)
            
            pyautogui.hotkey('ctrl','a')
            time.sleep(0.2)
            pyautogui.hotkey('ctrl','v')
            time.sleep(1)
            
            # Shilltext in die Zwischenablage
            pyperclip.copy(T_CONTENT_SHILL_TXT_1)
            time.sleep(0.1)
            pyautogui.hotkey('ctrl','v')
            time.sleep(0.2)
            keyboard.send_keys("{ENTER}")
            time.sleep(0.2)
        else:
            # Shilltext in die Zwischenablage
            pyperclip.copy(T_CONTENT_SHILL_TXT_1)
            time.sleep(0.1)
            pyautogui.hotkey('ctrl','v')
            time.sleep(0.2)
            keyboard.send_keys("{ENTER}")
            time.sleep(0.2)
            try:
                # Thread einmal ausführen
                global_counter += 1
                # Progressbarwert berechnen
                _t = global_counter/len(T_CONTENT_CHANNEL_1) * 100
                _t = '{:.2f}%'.format(_t)
                # Berechnung zu Ende
                kickpb1_thread = threading.Thread(target=kickpb1, args=(_t,))
                kickpb1_thread.start()
                kickpb1_thread = ""
            except:
                print ("Error: unable to start thread")

    os.system('TASKKILL /IM Telegram.exe /f /t')
    time.sleep(10)
    try:
        threading.Thread(target=stg).start()
    except:
        print ("Error: unable to start thread")

    time.sleep(10)

    ########################################
    # Steuerung Proc 2 - falls enabled 
    ########################################
    if shill_2_enabled.get() == "enabled":
        try:
            print("start r_clock Thread")
            proc_2_thread = threading.Thread(target=shill_2_proc)
            proc_2_thread.start()
            proc_2_thread = ""
        except:
            print ("Error: unable to start thread")
    else:
        threading.main_thread()
        shill_BTN_ACTION()
    

def shill_2_proc():
    print("shill_2_proc()")
    
    global global_counter, proc_2_thread, kickpb1_thread, T_global_pause, TG_PATH_GLOBAL
    global T_CONTENT_USER_XY, T_CONTENT_ACC_1_XY, T_CONTENT_ACC_2_XY

    #####################################################################################################################
    # Zu Account 2 navigieren, mehrere Texte geshillt werden                                                           ##
    #####################################################################################################################
    if shill_2_enabled.get() == "enabled":
        _set_tx = T_CONTENT_USER_XY.split(",")[0]
        _set_ty = T_CONTENT_USER_XY.split(",")[1]
        pywinauto.mouse.press(button='left', coords=(int(_set_tx), int(_set_ty)))
        pywinauto.mouse.release(button='left', coords=(int(_set_tx), int(_set_ty)))

        time.sleep(1)

        _acc2_tx = T_CONTENT_ACC_2_XY.split(",")[0]
        _acc2_ty = T_CONTENT_ACC_2_XY.split(",")[1]
        pywinauto.mouse.press(button='left', coords=(int(_acc2_tx), int(_acc2_ty)))
        pywinauto.mouse.release(button='left', coords=(int(_acc2_tx), int(_acc2_ty)))

        time.sleep(1)

        pywinauto.mouse.press(button='left', coords=(int(_acc2_tx), int(_acc2_ty)))
        pywinauto.mouse.release(button='left', coords=(int(_acc2_tx), int(_acc2_ty)))

        time.sleep(1)

    __counter = 0
    #####################################################################################################################
    # Posts abetzen - Liste 2                                                                                          ##
    #####################################################################################################################
    for channel in T_CONTENT_CHANNEL_2:

        __counter += 1
        _current_state = "LIST 2 - " + str(__counter) + " of " + str(len(T_CONTENT_CHANNEL_2)) + " shilled"
        print(_current_state)
        global_status_label = ttk.Label(root, text=_current_state)

        # Channel aufrufen
        os.system(TG_PATH_GLOBAL + " -- tg://resolve?domain=" + channel.split(",")[0])
        time.sleep(1)

        #####################################################################
        # Mediendatei - wenn definiert - in die Zwisenablage - KEIN VIDEO
        #####################################################################
        if T_CONTENT_MEDIA_2 != "" and channel.split(",")[1] != "NO" and T_CONTENT_MEDIA_2.split(".")[len(T_CONTENT_MEDIA_2.split("."))-1] != "mp4" or T_CONTENT_MEDIA_2.split(".")[len(T_CONTENT_MEDIA_2.split("."))-1] != "GIF" or T_CONTENT_MEDIA_2.split(".")[len(T_CONTENT_MEDIA_2.split("."))-1] != "gif":
            clip.OpenClipboard()
            clip.EmptyClipboard()
            clip.SetClipboardData(win32con.CF_DIB, IMAGE_BYTES_2)
            clip.CloseClipboard()

            pyautogui.hotkey('ctrl','a')
            time.sleep(0.2)
            pyautogui.hotkey('delete')
            time.sleep(0.2)
            pyautogui.hotkey('ctrl','v')
            time.sleep(0.5)

            # Shilltext in die Zwischenablage
            pyperclip.copy(T_CONTENT_SHILL_TXT_2)
            time.sleep(0.1)
            pyautogui.hotkey('ctrl','v')
            time.sleep(0.2)
            keyboard.send_keys("{ENTER}")
            time.sleep(0.2)

            try:
                # Thread einmal ausführen
                global_counter += 1
                # Progressbarwert berechnen
                _t = global_counter/len(T_CONTENT_CHANNEL_2) * 100
                _t = '{:.2f}%'.format(_t)
                # Berechnung zu Ende
                kickpb2_thread = threading.Thread(target=kickpb2, args=(_t,))
                kickpb2_thread.start()
                kickpb2_thread = ""
            except:
                print ("Error: unable to start thread")
        #########################################
        # Mediendatei - wenn definiert - VIDEO!
        #########################################
        elif T_CONTENT_MEDIA_2 != "" and T_CONTENT_MEDIA_2.split(".")[len(T_CONTENT_MEDIA_2.split("."))-1] == "mp4" or T_CONTENT_MEDIA_2.split(".")[len(T_CONTENT_MEDIA_2.split("."))-1] == "GIF" or T_CONTENT_MEDIA_2.split(".")[len(T_CONTENT_MEDIA_2.split("."))-1] == "gif":
            print("mit video")
            print(T_CONTENT_VIDEO_2_COORDS)
            _tx = T_CONTENT_VIDEO_2_COORDS.split(",")[0]
            _ty = T_CONTENT_VIDEO_2_COORDS.split(",")[1]

            #pywinauto.mouse.move()
            
            pywinauto.mouse.press(button='left', coords=(int(_tx), int(_ty)))
            pywinauto.mouse.release(button='left', coords=(int(_tx), int(_ty)))
            pyautogui.hotkey('ctrl','c')
            time.sleep(0.1)
            os.system(TG_PATH_GLOBAL + " -- tg://resolve?domain=" + channel.split(",")[0])
            time.sleep(1)
            
            pyautogui.hotkey('ctrl','a')
            time.sleep(0.2)
            pyautogui.hotkey('ctrl','v')
            time.sleep(1)
            
            # Shilltext in die Zwischenablage
            pyperclip.copy(T_CONTENT_SHILL_TXT_2)
            time.sleep(0.1)
            pyautogui.hotkey('ctrl','v')
            time.sleep(0.2)
            keyboard.send_keys("{ENTER}")
            time.sleep(0.2)
        else:
            # Shilltext in die Zwischenablage
            pyperclip.copy(T_CONTENT_SHILL_TXT_2)
            time.sleep(0.1)
            pyautogui.hotkey('ctrl','v')
            time.sleep(0.2)
            keyboard.send_keys("{ENTER}")
            time.sleep(0.2)
            try:
                # Thread einmal ausführen
                global_counter += 1
                # Progressbarwert berechnen
                _t = global_counter/len(T_CONTENT_CHANNEL_2) * 100
                _t = '{:.2f}%'.format(_t)
                # Berechnung zu Ende
                kickpb2_thread = threading.Thread(target=kickpb2, args=(_t,))
                kickpb2_thread.start()
                kickpb2_thread = ""
            except:
                print ("Error: unable to start thread")

    os.system('TASKKILL /IM Telegram.exe /f /t')
    time.sleep(10)
    try:
        threading.Thread(target=stg).start()
    except:
        print ("Error: unable to start thread")

    time.sleep(10)

############################################################

    os.system('TASKKILL /IM Telegram.exe /f /t')
    time.sleep(T_global_pause)
    try:
        threading.Thread(target=stg).start()
    except:
        print ("Error: unable to start thread")
    
    print("Neustart")
    threading.main_thread()
    time.sleep(10)
    shill_BTN_ACTION()


def stg():
    print("stg()")
    _tg = TG_PATH_GLOBAL.replace("\\\\", "/")
    os.system(_tg)


# Erhöht Progressbar 1 entsprechend
def kickpb1(i):
    print("kickpb1()")
    #print("List 1 progress: {i} %")
    pb1.step(float(str(i).split("%")[0]))

# Erhöht Progressbar 2  entsprechend
def kickpb2(i):
    print("kickpb2()")
    pb1.step((float(str(i).split("%")[0])))


















































def pause_BTN_ACTION():
    
    #print("pause_BTN_ACTION()")

    print(shill_pause_2.get("1.0",'end-1c'))

    #print(T_CONTENT_USER_XY)
    #print(T_CONTENT_ACC_1_XY)
    #print(T_CONTENT_ACC_2_XY)

    #os.system('TASKKILL /IM TGSBot3beta.exe /f /t')  
    #sys.exit()
    
    
    #global tgs_running

    #if tgs_running == True:
    #    tgs_running = False
    #    return
    #if tgs_running == False:
    #    #tgs_running = True
    #    try:
    #        print("start r_clock Thread")
    #        r_clock_thread = threading.Thread(target=r_clock)
    #        r_clock_thread.start()
    #        r_clock_thread = ""
    #    except:
    #        print ("Error: unable to start thread")
    
##################################################################
################## LOAD 
##################################################################

def load_BTN_ACTION():

    global T_CONTENT_MEDIA_1, T_CONTENT_MEDIA_2
    global T_CONTENT_PAUSE_1, T_CONTENT_PAUSE_2, T_CONTENT_GLOBAL_PAUSE
    global T_CONTENT_SHILL_TXT_1, T_CONTENT_SHILL_TXT_2
    global T_CONTENT_CHANNEL_1, T_CONTENT_CHANNEL_2
    global T_CONTENT_USER_XY, T_CONTENT_ACC_1_XY, T_CONTENT_ACC_2_XY
    global T_CONTENT_SHILL_ENABLED, T_CONTENT_CALIBRE_ENABLED

    print("load_BTN_ACTION()")
    contents = ""

    load_BTN.configure(state=tk.DISABLED)

    with open(T_CONTENT_FILE_PATH, encoding='utf8') as f:
        contents = f.read()

        T_CONTENT_SHILL_TXT_1       = contents.split("TGSB3_W_DELIM_1")[0]
        T_CONTENT_CHANNEL_1         = contents.split("TGSB3_W_DELIM_1\n")[1].split("TGSB3_W_DELIM_2")[0]
        T_CONTENT_PAUSE_1           = contents.split("TGSB3_W_DELIM_2\n")[1].split("\n")[0]
        _media_1                    = contents.split("TGSB3_W_DELIM_3\n")[1].split("\n")[0]
        T_CONTENT_SHILL_TXT_2       = contents.split("TGSB3_W_DELIM_4\n")[1].split("TGSB3_W_DELIM_5")[0]
        T_CONTENT_CHANNEL_2         = contents.split("TGSB3_W_DELIM_5\n")[1].split("TGSB3_W_DELIM_6")[0]
        T_CONTENT_PAUSE_2           = contents.split("TGSB3_W_DELIM_6\n")[1].split("\n")[0]
        _media_2                    = contents.split("TGSB3_W_DELIM_7\n")[1].split("\n")[0]
        T_CONTENT_SHILL_ENABLED     = contents.split("TGSB3_W_DELIM_8\n")[1].split("\n")[0]
        T_CONTENT_USER_XY           = contents.split("TGSB3_W_DELIM_9\n")[1].split("\n")[0]
        T_CONTENT_ACC_1_XY          = contents.split("TGSB3_W_DELIM__10\n")[1].split("\n")[0]
        T_CONTENT_ACC_2_XY          = contents.split("TGSB3_W_DELIM__11\n")[1].split("\n")[0]
        T_CONTENT_CALIBRE_ENABLED   = contents.split("TGSB3_W_DELIM__12\n")[1].split("\n")[0]
        T_CONTENT_GLOBAL_PAUSE      = contents.split("TGSB3_W_DELIM__13\n")[1].split("\n")[0]

        f.close()

    # Shilltext 1, Channel 1, Pause 1
    shill_txt_1.insert(tkinter.INSERT, T_CONTENT_SHILL_TXT_1)
    shill_channel_1.insert(tkinter.INSERT, T_CONTENT_CHANNEL_1)
    shill_pause_1.insert(tkinter.INSERT, str(T_CONTENT_PAUSE_1))

    # Shilltext 2, Channel 2, Pause 2
    shill_txt_2.insert(tkinter.INSERT, T_CONTENT_SHILL_TXT_2)
    shill_channel_2.insert(tkinter.INSERT, T_CONTENT_CHANNEL_2)
    shill_pause_2.insert(tkinter.INSERT, str(T_CONTENT_PAUSE_2))
    shill_2_enabled.set(T_CONTENT_SHILL_ENABLED)

    # Multiaccs enabled
    multiple_accs_enabled.set(T_CONTENT_CALIBRE_ENABLED)

    # Global Pause
    global_pause.insert(tkinter.INSERT, str(T_CONTENT_GLOBAL_PAUSE))

    print("##################")
    print(T_CONTENT_PAUSE_1)

    # Media
    # "NaN.NaN"
    if _media_1 != "NaN.NaN":
        T_CONTENT_MEDIA_1 = _media_1
        load_media_1_BTN.config(text="OK")
    if _media_2 != "NaN.NaN":
        T_CONTENT_MEDIA_2 = _media_2
        load_media_2_BTN.config(text="OK")
    if _media_1 == "NaN.NaN":
        T_CONTENT_MEDIA_1 = "NaN.NaN"
    if _media_2 == "NaN.NaN":
        T_CONTENT_MEDIA_1 = "NaN.NaN"

    # Calibre
    if T_CONTENT_USER_XY != "0,0":
        _settings_x = int(T_CONTENT_USER_XY[0])
        _settings_y = int(T_CONTENT_USER_XY[1])
        settings_BTN.config(text="Users OK")
    if T_CONTENT_ACC_1_XY != "0,0":
        _account1_x = int(T_CONTENT_ACC_1_XY[0])
        _account1_y = int(T_CONTENT_ACC_1_XY[1])
        account1_BTN.config(text="Acc 1 OK")
    if T_CONTENT_ACC_2_XY != "0,0":
        _account2_x = int(T_CONTENT_ACC_2_XY[0])
        _account2_x = int(T_CONTENT_ACC_2_XY[1])
        account2_BTN.config(text="Acc 2 OK")

##################################################################
################## SAVE 
##################################################################

def save_BTN_ACTION():

    global shill_pause_1, shill_pause_2
    print("save_BTN_ACTION()")

    with open(T_CONTENT_FILE_PATH, 'w', encoding='utf8') as f:
        # Shilltext 1
        f.write(shill_txt_1.get('1.0', tk.END).rstrip("\n"))
        f.write("\n")
        f.write("TGSB3_W_DELIM_1\n")

        # Channellist 1
        f.write(shill_channel_1.get('1.0', tk.END).rstrip("\n"))
        f.write("\n")
        f.write("TGSB3_W_DELIM_2\n")

        # Pause 1
        f.write(shill_pause_1.get("1.0",'end-1c'))
        f.write("\n")
        f.write("TGSB3_W_DELIM_3\n")

        # Media 1
        f.write(T_CONTENT_MEDIA_1)
        f.write("\nTGSB3_W_DELIM_4\n")

        # Shill 2
        f.write(shill_txt_2.get('1.0', tk.END).rstrip("\n"))
        f.write("\nTGSB3_W_DELIM_5\n")

        # Channellist 2
        f.write(shill_channel_2.get('1.0', tk.END).rstrip("\n"))
        f.write("\n")
        f.write("TGSB3_W_DELIM_6\n")

        # Pause 2
        f.write(shill_pause_2.get("1.0",'end-1c'))
        f.write("\n")
        f.write("TGSB3_W_DELIM_7\n")

        # Media 2
        f.write(T_CONTENT_MEDIA_2)
        f.write("\nTGSB3_W_DELIM_8\n")

        # Enabled 2, Calibre, Calibre enabled
        # Platzhalter
        f.write("enabled\n")
        f.write("TGSB3_W_DELIM_9\n")

        f.write(T_CONTENT_USER_XY)
        f.write("\nTGSB3_W_DELIM__10\n")

        f.write(T_CONTENT_ACC_1_XY)
        f.write("\nTGSB3_W_DELIM__11\n")

        f.write(T_CONTENT_ACC_2_XY)
        f.write("\nTGSB3_W_DELIM__12\n")

        # Platzhalter
        f.write("enabled")
        f.write("\nTGSB3_W_DELIM__13\n")

        # Platzhalter
        f.write(T_CONTENT_GLOBAL_PAUSE)
        f.write("\nTGSB3_W_DELIM__14\n")

        f.close()

##################################
##### BUTTON GLOBAL ACT ENDE #####
##################################
    

#############################################################################################################
######################################### TK/TTK WIDGETS ANFANG #############################################
#############################################################################################################

# MENU
# create a menubar
menubar = tk.Menu(root)
root.config(menu=menubar)

# create a menu
file_menu = tk.Menu(menubar)

# add a menu item to the menu
file_menu.add_command(
    label='Performance settings',
    command=root.destroy
)


# add the File menu to the menubar
menubar.add_cascade(
    label="File",
    menu=file_menu
)
# MENU ENDE

###############
# ShillText 1
###############
ttk.Separator(root, orient='horizontal').pack(fill="x")
ttk.Label(root, text="Shilltext 1:").place(x=5,y=5)
ttk.Label(root, text="Channellist 1:").place(x=200,y=5)
shill_txt_1 = ScrolledText(root, height=12, width=22)
shill_txt_1.place(x=0,y=25)
shill_channel_1 = ScrolledText(root, height=12, width=22)
shill_channel_1.place(x=200,y=25)
ttk.Label(root, text="Configuration 1:").place(x=5, y=230)
#ttk.Checkbutton(root, text='Enabled', onvalue='enabled', offvalue='disabled').place(x=100, y=229)

load_media_1_BTN = ttk.Button(root, text="Image", command=select_file_1)
load_media_1_BTN.place(x=240, y=229)

load_video_1_BTN = ttk.Button(root, text="VID X,Y", command=select_video_file_1)
load_video_1_BTN.place(x=315, y=229)

ttk.Label(root, text="Status 1:").place(x=5,y=260)
ttk.Label(root, text="Pause:").place(x=170,y=229)

#shill_pause_1 = ttk.Entry(root, textvariable=tk.NUMERIC,width=12)
shill_pause_1 = tk.Text(root, width=3, height=1)
shill_pause_1.place(x=210,y=229)

pb1 = ttk.Progressbar(root, orient='horizontal', mode='determinate',length=320)
pb1.place(x=60,y=260)
# ShillText 1 - ENDE

ttk.Separator(root, orient='horizontal').pack(fill="x", pady=290)

################
# Shill-Text 2
################
ttk.Label(root, text="Shilltext 2:").place(x=5,y=5+300)
ttk.Label(root, text="Channellist 2:").place(x=200,y=5+300)

shill_txt_2 = ScrolledText(root, height=12, width=22)
shill_txt_2.place(x=0,y=25+300)

shill_channel_2 = ScrolledText(root, height=12, width=22)
shill_channel_2.place(x=200,y=25+300)
ttk.Label(root, text="Configuration 2:").place(x=5, y=230+300)

#ttk.Checkbutton(root, text='Enabled', onvalue='enabled', offvalue='disabled')

shill_2_checkbox = ttk.Checkbutton(root, text='Enabled', variable=shill_2_enabled, onvalue='enabled', offvalue='disabled', command=lambda: shill_2_TOGGLE(shill_2_enabled))
shill_2_checkbox.place(x=100, y=229+300)

load_media_2_BTN = ttk.Button(root, text="Image", command=select_file_2)
load_media_2_BTN.place(x=240, y=229+300)

load_video_2_BTN = ttk.Button(root, text="VID X,Y", command=select_video_file_2)
load_video_2_BTN.place(x=315, y=229+300)

ttk.Label(root, text="Status 2:").place(x=5,y=260+300)
ttk.Label(root, text="Pause:").place(x=170,y=229+300)




































shill_pause_2 = tk.Text(root, width=3, height=1)
shill_pause_2.place(x=210,y=229+300)

pb2 = ttk.Progressbar(root, orient='horizontal', mode='determinate',length=320).place(x=60,y=260+300)
# Shill-Text 2

ttk.Separator(root, orient='horizontal').pack(fill="x", pady=10)

###################
# Multiple TG-Accs
###################

ttk.Label(root, text="Calibrate:").place(x=5,y=5+600)

settings_BTN = ttk.Button(root, text="Users", command=lambda: calibre_BTN_ACTION("Settings"))
account1_BTN = ttk.Button(root, text="Account 1", command=lambda: calibre_BTN_ACTION("Acc1"))
account2_BTN = ttk.Button(root, text="Account 2", command=lambda: calibre_BTN_ACTION("Acc2"))

settings_BTN.place(x=70, y=602)
account1_BTN.place(x=150, y=602)
account2_BTN.place(x=230, y=602)

settings_BTN.state(['disabled'])
account1_BTN.state(['disabled'])
account2_BTN.state(['disabled'])

calibre_checkbox = ttk.Checkbutton(root, text='Enabled', variable=multiple_accs_enabled, onvalue='enabled', offvalue='disabled', command=lambda: calibre_TOGGLE(multiple_accs_enabled))
calibre_checkbox.place(x=310, y=605)
# Multiple TG-Ende

ttk.Separator(root, orient='horizontal').pack(fill="x", pady=30)

##########
# Status
##########
runtime_Label = ttk.Label(
    root,
    text='00:00:00:00',
    font=("Verdana", 45))
runtime_Label.place(x=5, y=640)

rounds_completed_Label = ttk.Label(root, text="Rounds completed: 0")
rounds_completed_Label.place(x=5, y=720)

global_status_label = ttk.Label(root, text="Status: IDLE")
global_status_label.place(x=5, y=810)

ttk.Label(root, text="Pause:").place(x=275,y=740)
global_pause = tk.Text(root, width=9, height=1)
global_pause.place(x=315,y=740)
# Status Ende

#################
# Global Button
#################

shill_BTN = tk.Button(root, text="Shill", height=2, width=21, command=shill_BTN_ACTION)
shill_BTN.place(x=5, y=770)

# Wenn Threading funktioniert, dann Umwandlung in Pause
pause_BTN = tk.Button(root, text="STOP", height=2, width=10, command=pause_BTN_ACTION)
pause_BTN.place(x=165, y=770)

load_BTN = tk.Button(root, text="Load", height=2, width=8,command=load_BTN_ACTION)
load_BTN.place(x=250, y=770)

save_BTN = tk.Button(root, text="Save", height=2, width=9, command=save_BTN_ACTION)
save_BTN.place(x=320, y=770)
############################################
############################################
############################################
#pause_BTN.configure(state=tk.DISABLED)

# Global Buttons Ende

#############################################################################################################
########################################## TK/TTK WIDGETS ENDE ##############################################
#############################################################################################################

# Fensterposition
_posx = root.winfo_screenwidth() - (_width+20)
_posy = 10

# Andere Fenstereinstellungen
root.title(_name + " " + _version)
root.geometry(f'{_width}x{_height}+{_posx}+{_posy}')
root.resizable(True, True)
root.attributes('-topmost', 1)

root.mainloop()
# Brussi Brussi Gewlinnheit
# Euni
# Knuizi Fuizi