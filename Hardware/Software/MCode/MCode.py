#!/usr/bin/env python
from ast import expr_context
from curses import echo
import Rec_snds
import Camcap
import readhbeat
from mlxRead import readoC
import time
import Send_dta
import os
import sys


def HrtRate():
    next_scrn.invis_btn()
    next_scrn.set_text('Recording..')
    beat.start_sensor()
    time.sleep(20)
    bpm, spo2 = beat.stop_sensor()
    try:
        fire.fire_hrt(bpm, spo2)
    except:
        pass
    next_scrn.send_HSp(bpm, spo2)
    next_scrn.reset_txt()
    next_scrn.vis_btn()
    print("HrtRate Terminated\n")  # "{}".format(arg)
    next_scrn.ref()


def SkinTemp():
    next_scrn.invis_btn()
    amb, obj = readoC()
    next_scrn.send_temp(obj)
    print("Sending last Value to Fire DB-------\n")
    try:
        fire.fire_temp(amb, obj)
    except:
        pass
    next_scrn.vis_btn()
    print("Temperature Terminated\n")
    next_scrn.ref()


def Record_snd():
    next_scrn.invis_btn()
    next_scrn.invis_btn1()
    next_scrn.set_text('Recording..')
    rec.Mic_strt()
    next_scrn.set_text('Filtering..')
    rec.Flt_snd()
    iname = "rec_test.mp3"
    next_scrn.set_text('Uploading..')
    try:
        fire.fire_snd(iname)
    except:
        pass
    next_scrn.reset_txt()
    next_scrn.vis_btn()
    next_scrn.vis_btn1()
    next_scrn.ref()


def Snd_replay():
    next_scrn.set_text('Playing..')
    next_scrn.invis_btn()
    next_scrn.invis_btn1()
    rec.Play_snd()
    next_scrn.reset_txt()
    next_scrn.vis_btn()
    next_scrn.vis_btn1()
    next_scrn.ref()


def CaptureCam(imgtyp):
    next_scrn.invis_btn()
    next_scrn.invis_btn1()
    iname = cam.imgCap()
    next_scrn.set_text('Uploading..')
    print("Image Captured")
    try:
        fire.fire_img(iname, imgtyp)
    except:
        pass
    next_scrn.set_text('Done!')
    time.sleep(1)
    next_scrn.reset_txt()
    next_scrn.vis_btn()
    next_scrn.vis_btn1()
    next_scrn.ref()


def CaptureVid():
    next_scrn.invis_btn()
    next_scrn.invis_btn1()
    next_scrn.set_text('Recording..')
    iname = cam.strt_vid()
    print("Video Recording")
    try:
        fire.fire_vid(iname)
    except:
        pass
    next_scrn.reset_txt()
    next_scrn.vis_btn()
    next_scrn.vis_btn1()
    next_scrn.ref()


def Rebooot():
    sys.stdout.flush()
    os.execl(sys.executable, 'python', __file__, *sys.argv[1:])


if __name__ == "__main__":
    try:
        next_scrn = Send_dta.nextScrn()  # initaite Nextion Screen
        next_scrn.page_load()

        next_scrn.prg_bar(20)
        time.sleep(0.5)

        beat = readhbeat.HeartRateMonitor()  # initiate Max30105

        next_scrn.prg_bar(40)
        time.sleep(0.5)

        rec = Rec_snds.Rec_Mic()  # initiate MIC

        next_scrn.prg_bar(60)
        time.sleep(0.5)

        cam = Camcap.Rpi_Cam()  # initiate Camera

        next_scrn.prg_bar(80)
        time.sleep(0.5)

        try:
            fire = Send_dta.FireDB()  # initiate Fire Database
        except:
            pass

        next_scrn.prg_bar(100)
        time.sleep(0.5)
        next_scrn.prg_bar(0)
        next_scrn.page_home()

        while True:
            # Taking input from user
            ioput = next_scrn.Read()
            print(ioput)

            if ioput == '0b':
                # start Reading Heart rate
                HrtRate()
            elif ioput == '0c':
                # start Reading Temperature
                SkinTemp()
            elif ioput == '11':
                # start Recording Mic
                Record_snd()
            elif ioput == '\\r' or ioput == '05':
                # start Capturing Cam Ear
                CaptureCam('Ear')
            elif ioput == '0f':
                # start Capturing Cam Skin
                CaptureCam('Skin')
            elif ioput == '0e':
                # start Capturing Cam Throat
                CaptureCam('Throat')
            elif ioput == '10':
                # start Recording Video
                CaptureVid()
            elif ioput == '12':
                Snd_replay()
            elif ioput == '13':
                cam.CamClose()
                next_scrn.page_load()
                next_scrn.set_text('Rebooting in...3')
                time.sleep(1)
                next_scrn.set_text('Rebooting in...2')
                time.sleep(1)
                next_scrn.set_text('Rebooting in...1')
                time.sleep(1)
                next_scrn.reset_txt()
                next_scrn.reset()
                Rebooot()
            else:
                print("Enter Valid Response")

            print("Waiting for User!")
    except:
        cam.CamClose()
        sys.stdout.flush()
        os.execl(sys.executable, 'python', __file__, *sys.argv[1:])
