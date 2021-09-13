import bpy,os,json
from bpy.props import *
import datetime
import time
from ..ui import PF_PT_NPanel, draw_pomodoro
from .. import utils
from .. import properties
import aud
import csv


class PomoFocus_OT_Pomostart(bpy.types.Operator):
    """Start Pomodoro Timer"""
    bl_idname = "pomofocus.pomostart"
    bl_label = ""
    bl_options = {"UNDO", "INTERNAL"}


    def execute(self, context):
        prefs = utils.common.prefs()
        pomogrp = utils.common.props()
        now = datetime.datetime.now()
        totaltime = now + datetime.timedelta(minutes = 1) 
        added_time = totaltime.strftime("%Y-%m-%d %H:%M:%S")

        pomogrp.year = int(totaltime.strftime("%Y"))
        pomogrp.month = int(totaltime.strftime("%m"))
        pomogrp.day = int(totaltime.strftime("%d"))
        pomogrp.hour = int(totaltime.strftime("%H"))
        pomogrp.minute = int(totaltime.strftime("%M"))
        pomogrp.secs = int(totaltime.strftime("%S"))
        pomogrp.estipomo_time = added_time

        cur_time = totaltime
        # int(prefs.srtbrk_dur)
        totalsrttime = cur_time + datetime.timedelta(minutes = int(prefs.srtbrk_dur))
        added_srttime = totalsrttime.strftime("%Y-%m-%d %H:%M:%S")
        pomogrp.srtyear = int(totalsrttime.strftime("%Y"))
        pomogrp.srtmonth = int(totalsrttime.strftime("%m"))
        pomogrp.srtday = int(totalsrttime.strftime("%d"))
        pomogrp.srthour = int(totalsrttime.strftime("%H"))
        pomogrp.srtminute = int(totalsrttime.strftime("%M"))
        pomogrp.srtsecs = int(totalsrttime.strftime("%S"))
        pomogrp.estisrt_time = added_srttime

        if not pomogrp.pomotimer_run_stat:
            bpy.app.timers.register(check_pomo)
            pomogrp.pomotimer_run_stat = True
            pomogrp.anytimerrinning = True

        return {'FINISHED'}

def redraw_panel(panel):
    try:
        bpy.utils.unregister_class(panel)
    except:
        pass

    bpy.utils.register_class(panel)

def check_pomo():
    pomogrp = utils.common.props()
    t = time.localtime()
    prefs = utils.common.prefs()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
    cur_yr = t.tm_year
    cur_mnth = t.tm_mon
    cur_day = t.tm_mday
    cur_hr = t.tm_hour
    cur_mins = t.tm_min
    cur_secs = t.tm_sec
    NaN_var = pomogrp.estipomo_time
    estipomoCount = pomogrp.esti_pomo
    lngbropomo = int(prefs.lng_pomoCount)
    if NaN_var == 'NaN' :
        # if pomogrp.complted_pomo == estipomoCount:
        #     time_calc()
        #     track(pomogrp.taskname)
        #     pomogrp.pomotimer_run_stat = False
        #     pomogrp.srttimer_run_stat = False
        #     pomogrp.complted_pomo = 0
        #     pomogrp.anytimerrinning = False
        #     tasknm = pomogrp.taskname
        #     killsound()
        #     if prefs.use_endSound and not pomogrp.anytimerrinning:
        #         playendsound(prefs.playendfile)
        #     bpy.ops.message.messagebox('INVOKE_DEFAULT', message = tasknm, alrt_message = 'Task Completed')
        #     redraw_panel(PF_PT_NPanel)
        #     return None


        if estipomoCount >= 1 and estipomoCount>= pomogrp.complted_pomo :
            if pomogrp.complted_pomo % lngbropomo == 0:
                totalsrttime = datetime.datetime.now()
                totallngtime = totalsrttime + datetime.timedelta(minutes = int(prefs.lngbrk_dur)) 
                added_lngtime = totallngtime.strftime("%Y-%m-%d %H:%M:%S")
                pomogrp.lngyear = int(totallngtime.strftime("%Y"))
                pomogrp.lngmonth = int(totallngtime.strftime("%m"))
                pomogrp.lngday = int(totallngtime.strftime("%d"))
                pomogrp.lnghour = int(totallngtime.strftime("%H"))
                pomogrp.lngminute = int(totallngtime.strftime("%M"))
                pomogrp.lngsecs = int(totallngtime.strftime("%S"))
                pomogrp.estilng_time = added_lngtime
                if pomogrp.lngtimer_run_stat:
                    pomogrp.anytimerrinning = True
                    lngbrk = 'Long break started'
                    bpy.ops.message.messagebox('INVOKE_DEFAULT', message = lngbrk, alrt_message = 'Long Break')
                    bpy.app.timers.register(check_lngbrk)
            elif pomogrp.srttimer_run_stat:
                pomogrp.anytimerrinning = True
                srtbrk = 'Short break started'
                bpy.ops.message.messagebox('INVOKE_DEFAULT', message = srtbrk, alrt_message = 'Short Break')
                bpy.app.timers.register(check_srtbrk)
        return None

    if NaN_var == current_time:
        pomogrp.estipomo_time = 'NaN'
        pomogrp.rem_minute = 0
        pomogrp.srttimer_run_stat = True
        pomogrp.rem_seconds = 0    
        # playSound(prefs.sound_type)
        if estipomoCount>=1:
            pomogrp.complted_pomo= pomogrp.complted_pomo +1
            print(pomogrp.complted_pomo)
        
        redraw_panel(PF_PT_NPanel)
        
    if current_time < NaN_var:
        if prefs.use_tick and pomogrp.anytimerrinning:
            playsound(prefs.playtickfile)
        
        in_day =pomogrp.day
        in_month =pomogrp.month
        in_year =pomogrp.year
        in_hour =pomogrp.hour
        in_minute =pomogrp.minute
        in_secs = pomogrp.secs

        # https://www.w3resource.com/python-exercises/date-time-exercise/python-date-time-exercise-37.php
        d0 = datetime.datetime(cur_yr,cur_mnth,cur_day,cur_hr,cur_mins,cur_secs)
        d1 = datetime.datetime(in_year,in_month,in_day,in_hour,in_minute,in_secs)
        delta = d1 - d0
        timediff = delta.days * 24 * 3600 + delta.seconds

        minz, timediff = divmod(timediff, 60)
        pomogrp.rem_minute = minz
        pomogrp.rem_seconds = timediff
        redraw_panel(PF_PT_NPanel)
    return 1.0

def check_srtbrk():
    
    pomogrp = utils.common.props()
    t = time.localtime()
    prefs = utils.common.prefs()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
    cur_yr = t.tm_year
    cur_mnth = t.tm_mon
    cur_day = t.tm_mday
    cur_hr = t.tm_hour
    cur_mins = t.tm_min
    cur_secs = t.tm_sec
    srtBrktm = pomogrp.estisrt_time
    compltedpomoCount =pomogrp.complted_pomo
    estipomoCount = pomogrp.esti_pomo

    if srtBrktm == 'NaN' :
        return None

    if  srtBrktm == current_time:
        pomogrp.srttimer_run_stat = False
        pomogrp.pomotimer_run_stat = False
        prefs = utils.common.prefs()
        if estipomoCount > int(prefs.lng_pomoCount):
            pomogrp.lngtimer_run_stat = True
        pomogrp.estisrt_time = 'NaN'
        
        pomogrp.rem_minute = 0
        pomogrp.rem_seconds = 0
        # playSound(prefs.sound_type)
        redraw_panel(PF_PT_NPanel)
        
        if compltedpomoCount < estipomoCount:
            bpy.ops.pomofocus.pomostart()
        if compltedpomoCount == estipomoCount:
            time_calc()
            track(pomogrp.taskname)
            pomogrp.complted_pomo = 0
            pomogrp.anytimerrinning = False
            pomogrp.pomotimer_run_stat = False
            pomogrp.lngtimer_run_stat = False
            pomogrp.srttimer_run_stat = False
            tasknm = pomogrp.taskname
            
            if prefs.use_endSound and not pomogrp.anytimerrinning:
                playendsound(prefs.playendfile)
            bpy.ops.message.messagebox('INVOKE_DEFAULT', message = tasknm, alrt_message = 'Task Completed')
            killsound()
            redraw_panel(PF_PT_NPanel)
            return None

    if current_time < srtBrktm:
        in_srtday =pomogrp.srtday
        in_srtmonth =pomogrp.srtmonth
        in_srtyear =pomogrp.srtyear
        in_srthour =pomogrp.srthour
        in_srtminute =pomogrp.srtminute
        in_srtsecs = pomogrp.srtsecs

        # https://www.w3resource.com/python-exercises/date-time-exercise/python-date-time-exercise-37.php
        d0 = datetime.datetime(cur_yr,cur_mnth,cur_day,cur_hr,cur_mins,cur_secs)
        d1 = datetime.datetime(in_srtyear,in_srtmonth,in_srtday,in_srthour,in_srtminute,in_srtsecs)
        delta = d1 - d0
        timediff = delta.days * 24 * 3600 + delta.seconds
        minz, timediff = divmod(timediff, 60)
        pomogrp.rem_minute = minz
        pomogrp.rem_seconds = timediff
        redraw_panel(PF_PT_NPanel)

        return 1.0

def check_lngbrk():
    
    pomogrp = utils.common.props()
    t = time.localtime()
    prefs = utils.common.prefs()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
    cur_yr = t.tm_year
    cur_mnth = t.tm_mon
    cur_day = t.tm_mday
    cur_hr = t.tm_hour
    cur_mins = t.tm_min
    cur_secs = t.tm_sec
    lngBrktm = pomogrp.estilng_time
    compltedpomoCount =pomogrp.complted_pomo
    estipomoCount = pomogrp.esti_pomo

    if lngBrktm == 'NaN' :
        return None

    if  lngBrktm == current_time:
        pomogrp.srttimer_run_stat = False
        pomogrp.pomotimer_run_stat = False
        pomogrp.lngtimer_run_stat = False
        pomogrp.estilng_time = 'NaN'
        pomogrp.rem_minute = 0
        pomogrp.rem_seconds = 0
        # playSound(prefs.sound_type)
        redraw_panel(PF_PT_NPanel)
        if compltedpomoCount < estipomoCount:
            bpy.ops.pomofocus.pomostart()
        if compltedpomoCount == estipomoCount:
            time_calc()
            track(pomogrp.taskname)
            pomogrp.complted_pomo = 0
            pomogrp.pomotimer_run_stat = False
            pomogrp.srttimer_run_stat = False
            pomogrp.anytimerrinning = False
            tasknm = pomogrp.taskname
            
            if prefs.use_endSound and not pomogrp.anytimerrinning:
                playendsound(prefs.playendfile)
            bpy.ops.message.messagebox('INVOKE_DEFAULT', message = tasknm, alrt_message = 'Task Completed')
            killsound()
            redraw_panel(PF_PT_NPanel)
            return None

    if current_time < lngBrktm:
        in_lngday =pomogrp.lngday
        in_lngmonth =pomogrp.lngmonth
        in_lngyear =pomogrp.lngyear
        in_lnghour =pomogrp.lnghour
        in_lngminute =pomogrp.lngminute
        in_lngsecs = pomogrp.lngsecs

        # https://www.w3resource.com/python-exercises/date-time-exercise/python-date-time-exercise-37.php
        d0 = datetime.datetime(cur_yr,cur_mnth,cur_day,cur_hr,cur_mins,cur_secs)
        d1 = datetime.datetime(in_lngyear,in_lngmonth,in_lngday,in_lnghour,in_lngminute,in_lngsecs)
        delta = d1 - d0
        timediff = delta.days * 24 * 3600 + delta.seconds
        minz, timediff = divmod(timediff, 60)
        pomogrp.rem_minute = minz
        pomogrp.rem_seconds = timediff
        redraw_panel(PF_PT_NPanel)

        return 1.0

class MessageBox(bpy.types.Operator):
    bl_idname = "message.messagebox"
    bl_label = ""
 
    message : bpy.props.StringProperty(
        name = "message",
        description = "message",
        default = ''
    )
    alrt_message : bpy.props.StringProperty(
        name = "alert message",
        description = "alert message",
        default = ''
    )
 
    def execute(self, context):
        self.report({'INFO'}, self.message)
        return {'FINISHED'}
 
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 200)
 
    def draw(self, context):
        self.layout.label(text = self.alrt_message, icon = 'ERROR')
        box= self.layout.box()
        box.label(text = self.message)

class ResetTime(bpy.types.Operator):
    bl_description = 'Reset to Default'
    bl_idname = 'pomofocus.resettime'
    bl_label = 'Reset to Default'

    def execute(self, context):
        if bpy.app.timers.is_registered(check_pomo):
            bpy.app.timers.unregister(check_pomo)

        if bpy.app.timers.is_registered(check_srtbrk):
            bpy.app.timers.unregister(check_srtbrk)

        if bpy.app.timers.is_registered(check_lngbrk):
            bpy.app.timers.unregister(check_lngbrk)
        
        pomogrp = utils.common.props()
        pomogrp.pomotimer_run_stat = False
        pomogrp.srttimer_run_stat = False
        pomogrp.lngtimer_run_stat = False
        pomogrp.anytimerrinning = False

        pomogrp.rem_minute = 0
        pomogrp.rem_seconds = 0
        pomogrp.complted_pomo = 0
        pomogrp.esti_pomo = 1

        pomogrp.taskname = 'New Pomodoro'
        pomogrp.estipomo_time = 'NaN'
        pomogrp.estisrt_time = 'NaN'
        pomogrp.estilng_time = 'NaN'

        return {'FINISHED'}

class PomoFocus_OT_popup(bpy.types.Operator):
    """Detach Player menu"""
    bl_idname = "pomofocus.float"
    bl_label = ""
    bl_options = {'REGISTER', 'INTERNAL'}
   

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width = 500)

    def draw(self, context):
        layout = self.layout
        column = layout.column()
        draw_pomodoro(self,context)

class PomoFocus_Addonkey(bpy.types.Operator):
    ''' Add hotkey entry '''
    bl_idname = "pomofocus.addpomo_hotkey"
    bl_label = "Pomodoro Hotkey"
    bl_options = {'REGISTER', 'INTERNAL'}
    
    def execute(self, context):
        add_hotkey()
        self.report({'INFO'}, "Hotkey added to Edit -> Preferences -> Keymap -> Window")
        return {'FINISHED'}

addon_keymaps = []

def add_hotkey():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon    
    km = kc.keymaps.new(name="Window", space_type='EMPTY', region_type='WINDOW')  
    kmi = km.keymap_items.new("pomofocus.float", "K", "PRESS", alt=True) 
    kmi.active = True
    addon_keymaps.append((km, kmi)) 

def remove_hotkey():
    ''' clears all addon level keymap hotkeys stored in addon_keymaps '''
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = kc.keymaps['Window']
    
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
        wm.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()

def playsound(sound): 
    device = aud.Device()
    handle = bpy.types.Scene.music_handle
    playMusic = aud.Sound.file(sound)
    if not hasattr(handle, "status") or (hasattr(handle, "status") and handle.status == False):
        handle = device.play(playMusic)
        # handle.loop_count = -1

def killsound():
    handle = bpy.types.Scene.music_handle
    if hasattr(handle, "status") and handle.status == True:
        handle.stop()

def playendsound(sound): 
    device = aud.Device()
    handle = bpy.types.Scene.music_handle
    playendMusic = aud.Sound.file(sound)
    if not hasattr(handle, "status") or (hasattr(handle, "status") and handle.status == False):
        handle = device.play(playendMusic)
        handle.loop_count = 1
        handle.status == False

def time_calc():
    pomogrp = utils.common.props()
    prefs = utils.common.prefs()
    pomo = pomogrp.esti_pomo
    pomotime = int(prefs.lng_pomoCount)
    lng_pomo_count = pomo // pomotime
    pomogrp.complted_lng = lng_pomo_count
    srt_pomo_count = pomo - lng_pomo_count
    pomogrp.complted_srt = srt_pomo_count
    fullpomotime = pomo * int(prefs.pomod_dur)
    fullsrttime = srt_pomo_count * int(prefs.srtbrk_dur)
    fulllngtime = lng_pomo_count * int(prefs.lngbrk_dur)
    totaltime_inmins = fullpomotime + fullsrttime + fulllngtime
    totaltime_insecs = totaltime_inmins * 60
    pomogrp.total_timeSpent = format_time(totaltime_insecs)

def format_time(d):
    return '{:02}h {:02}m {:02}s'.format(d // 3600, d % 3600 // 60, d % 60)

def track(e):
    
    prefs = utils.common.prefs()
    pomogrp = utils.common.props()
    l = "{0},{1},{2},{3},{4}\n".format(e, pomogrp.complted_pomo, pomogrp.complted_srt, pomogrp.complted_lng, pomogrp.total_timeSpent, )
    try:
        with open(prefs.csv_path, mode='a', encoding='utf-8') as f:
            f.write(l)
    except PermissionError:
        bpy.ops.message.messagebox('INVOKE_DEFAULT', message = 'Please close the file to write the data', alrt_message = 'Error')