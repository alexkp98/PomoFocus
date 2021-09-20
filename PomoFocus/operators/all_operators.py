import bpy,os,json
from bpy.props import *
import datetime
import time
from ..ui import PF_PT_NPanel, draw_pomodoro
from .. import utils
from .. import properties
import aud
import platform
import csv
from pathlib import Path


class PomoFocus_OT_Pomostart(bpy.types.Operator):
    """Start Pomodoro Timer"""
    bl_idname = "pomofocus.pomostart"
    bl_label = ""
    bl_options = {"UNDO", "INTERNAL"}


    def execute(self, context):
        prefs = utils.common.prefs()
        pomogrp = utils.common.props()
        now = datetime.datetime.now()
        dt = __class__.date_cvrt
        __class__.file_status_check()
        if prefs.file_status:
            __class__.redraw_panel(PF_PT_NPanel)
            return {'FINISHED'}
        else:
            pass

        if pomogrp.added_time == '':
            pomogrp.added_time = now.strftime("%Y-%m-%d %H:%M:%S")
        totaltime = now + datetime.timedelta(minutes = int(prefs.pomod_dur)) 
        added_time = totaltime.strftime("%Y-%m-%d %H:%M:%S")

        pomogrp.year = dt(totaltime,"%Y")
        pomogrp.month = dt(totaltime,"%m")
        pomogrp.day = dt(totaltime,"%d")
        pomogrp.hour = dt(totaltime,"%H")
        pomogrp.minute = dt(totaltime,"%M")
        pomogrp.secs = dt(totaltime,"%S")
        pomogrp.estipomo_time = added_time

        cur_time = totaltime
        # int(prefs.srtbrk_dur)
        totalsrttime = cur_time + datetime.timedelta(minutes = int(prefs.srtbrk_dur))
        added_srttime = totalsrttime.strftime("%Y-%m-%d %H:%M:%S")

        pomogrp.srtyear = dt(totalsrttime,"%Y")
        pomogrp.srtmonth =  dt(totalsrttime,"%m")
        pomogrp.srtday = dt(totalsrttime,"%d")
        pomogrp.srthour =  dt(totalsrttime,"%H")
        pomogrp.srtminute =dt(totalsrttime,"%M")
        pomogrp.srtsecs =  dt(totalsrttime,"%S")
        pomogrp.estisrt_time = added_srttime

        if not pomogrp.pomotimer_run_stat:
            bpy.app.timers.register(__class__.check_pomo)
            pomogrp.pomotimer_run_stat = True
            pomogrp.anytimerrinning = True

        return {'FINISHED'}
    
    def date_cvrt(t,s):
        ct = int(t.strftime(s))
        return ct

    def file_status_check():
        prefs = utils.common.prefs()
        p = prefs.csv_path
        try:
            p = Path(p)
            p.rename(p)
            prefs.file_status = False
        except PermissionError:
            prefs.file_status = True

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
            if estipomoCount >= 1 and estipomoCount>= pomogrp.complted_pomo :
                if pomogrp.complted_pomo % lngbropomo == 0:
                    dt = __class__.date_cvrt
                    totalsrttime = datetime.datetime.now()
                    totallngtime = totalsrttime + datetime.timedelta(minutes = int(prefs.lngbrk_dur)) 
                    added_lngtime = totallngtime.strftime("%Y-%m-%d %H:%M:%S")
                    pomogrp.lngyear = dt(totallngtime,"%Y")
                    pomogrp.lngmonth = dt(totallngtime,"%m")
                    pomogrp.lngday = dt(totallngtime,"%d")
                    pomogrp.lnghour = dt(totallngtime,"%H")
                    pomogrp.lngminute = dt(totallngtime,"%M")
                    pomogrp.lngsecs = dt(totallngtime,"%S")
                    pomogrp.estilng_time = added_lngtime
                    if pomogrp.lngtimer_run_stat:
                        pomogrp.anytimerrinning = True
                        lngbrk = 'Long break started'
                        bpy.ops.message.messagebox('INVOKE_DEFAULT', message = lngbrk, alrt_message = 'Long Break')
                        bpy.app.timers.register(PomoFocus_OT_Pomostart.check_lngbrk)
                elif pomogrp.srttimer_run_stat:
                    pomogrp.anytimerrinning = True
                    srtbrk = 'Short break started'
                    bpy.ops.message.messagebox('INVOKE_DEFAULT', message = srtbrk, alrt_message = 'Short Break')
                    bpy.app.timers.register(PomoFocus_OT_Pomostart.check_srtbrk)
            return None

        if NaN_var == current_time:
            pomogrp.estipomo_time = 'NaN'
            pomogrp.rem_minute = 0
            pomogrp.srttimer_run_stat = True
            pomogrp.rem_seconds = 0

            if estipomoCount>=1:
                pomogrp.complted_pomo= pomogrp.complted_pomo +1
            __class__.redraw_panel(PF_PT_NPanel)
            
        if current_time < NaN_var:
            if prefs.use_tick and pomogrp.anytimerrinning:
                __class__.playsound(prefs.playtickfile)
            
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
            __class__.redraw_panel(PF_PT_NPanel)
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
            __class__.redraw_panel(PF_PT_NPanel)
            
            if compltedpomoCount < estipomoCount:
                bpy.ops.pomofocus.pomostart()
            if compltedpomoCount == estipomoCount:
                pomogrp.csv_status = 'Completed'
                __class__.time_calc(pomogrp.csv_status)
                track(pomogrp.taskname, pomogrp.csv_status)
                pomogrp.complted_pomo = 0
                pomogrp.complted_lng = 0
                pomogrp.complted_srt = 0
                pomogrp.anytimerrinning = False
                pomogrp.pomotimer_run_stat = False
                pomogrp.lngtimer_run_stat = False
                pomogrp.srttimer_run_stat = False
                tasknm = pomogrp.taskname
                
                if prefs.use_endSound and not pomogrp.anytimerrinning:
                    __class__.playendsound(prefs.playendfile)
                bpy.ops.message.messagebox('INVOKE_DEFAULT', message = tasknm, alrt_message = 'Task Completed')
                __class__.killsound()
                __class__.redraw_panel(PF_PT_NPanel)
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
            __class__.redraw_panel(PF_PT_NPanel)

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
            __class__.redraw_panel(PF_PT_NPanel)
            if compltedpomoCount < estipomoCount:
                bpy.ops.pomofocus.pomostart()
            
            if compltedpomoCount == estipomoCount:
                pomogrp.csv_status = 'Completed'
                __class__.time_calc(pomogrp.csv_status)
                track(pomogrp.taskname, pomogrp.csv_status)
                pomogrp.complted_pomo = 0
                pomogrp.complted_lng = 0
                pomogrp.complted_srt = 0
                pomogrp.pomotimer_run_stat = False
                pomogrp.srttimer_run_stat = False
                pomogrp.anytimerrinning = False
                tasknm = pomogrp.taskname
                
                if prefs.use_endSound and not pomogrp.anytimerrinning:
                    __class__.playendsound(prefs.playendfile)
                bpy.ops.message.messagebox('INVOKE_DEFAULT', message = tasknm, alrt_message = 'Task Completed')
                __class__.killsound()
                __class__.redraw_panel(PF_PT_NPanel)
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
            __class__.redraw_panel(PF_PT_NPanel)
            return 1.0

    def redraw_panel(panel):
        try:
            bpy.utils.unregister_class(panel)
        except:
            pass
        bpy.utils.register_class(panel)

    def playsound(sound): 
        device = aud.Device()
        handle = bpy.types.Scene.music_handle
        playMusic = aud.Sound.file(sound)
        if not hasattr(handle, "status") or (hasattr(handle, "status") and handle.status == False):
            handle = device.play(playMusic)

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

    def time_calc(status):
        pomogrp = utils.common.props()
        prefs = utils.common.prefs()
        pomo = pomogrp.esti_pomo
        pomotime = int(prefs.lng_pomoCount)
        if status == 'Completed':
            lng_pomo_count = pomo // pomotime
            pomogrp.complted_lng = lng_pomo_count
            srt_pomo_count = pomo - lng_pomo_count
            pomogrp.complted_srt = srt_pomo_count
            fullpomotime = pomo * int(prefs.pomod_dur)
            fullsrttime = srt_pomo_count * int(prefs.srtbrk_dur)
            fulllngtime = lng_pomo_count * int(prefs.lngbrk_dur)
            totaltime_inmins = fullpomotime + fullsrttime + fulllngtime
            totaltime_insecs = totaltime_inmins * 60
            pomogrp.total_timeSpent = __class__.format_time(totaltime_insecs)
        elif status == 'Stopped':
            pomogrp.complted_lng = 0
            pomogrp.complted_srt = 0
            addedDt = pomogrp.added_time 
            DtTm = datetime.datetime.strptime(addedDt, "%Y-%m-%d %H:%M:%S")
            now = datetime.datetime.now()
            # curDt = now.strftime("%Y-%m-%d %H:%M:%S")
            Tm_wked = now - DtTm
            pomogrp.total_timeSpent = __class__.format_time(Tm_wked.seconds)

    def format_time(d):
        return '{:02}h {:02}m {:02}s'.format(d // 3600, d % 3600 // 60, d % 60)

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
        pomogrp = utils.common.props()
        pomogrp.csv_status = 'Stopped'
        PomoFocus_OT_Pomostart.time_calc(pomogrp.csv_status)
        track(pomogrp.taskname, pomogrp.csv_status)
        if bpy.app.timers.is_registered(PomoFocus_OT_Pomostart.check_pomo):
            bpy.app.timers.unregister(PomoFocus_OT_Pomostart.check_pomo)

        if bpy.app.timers.is_registered(PomoFocus_OT_Pomostart.check_srtbrk):
            bpy.app.timers.unregister(PomoFocus_OT_Pomostart.check_srtbrk)

        if bpy.app.timers.is_registered(PomoFocus_OT_Pomostart.check_lngbrk):
            bpy.app.timers.unregister(PomoFocus_OT_Pomostart.check_lngbrk)
        
        
        pomogrp.pomotimer_run_stat = False
        pomogrp.srttimer_run_stat = False
        pomogrp.lngtimer_run_stat = False
        pomogrp.anytimerrinning = False

        pomogrp.rem_minute = 0
        pomogrp.rem_seconds = 0
        pomogrp.complted_pomo = 0
        pomogrp.complted_lng = 0
        pomogrp.complted_srt = 0
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


def track(e,status):
    
    prefs = utils.common.prefs()
    pomogrp = utils.common.props()
    l = "{0},{1},{2},{3},{4},{5},{6}\n".format(pomogrp.added_time, e, pomogrp.complted_pomo, pomogrp.complted_srt, pomogrp.complted_lng, pomogrp.total_timeSpent,status )
    try:
        with open(prefs.csv_path, mode='a', encoding='utf-8') as f:
            f.write(l)
    except PermissionError:
        bpy.ops.message.messagebox('INVOKE_DEFAULT', message = 'Please close file before updating the data', alrt_message = 'Error')
    # resetting the value to empty
    pomogrp.csv_status = ''
    pomogrp.added_time = ''

class PF_OT_open_csv(bpy.types.Operator):
    bl_idname = "pomofocus.open_csv"
    bl_label = "Open CSV"
    bl_description = "Open CSV with tracking data."
    
    def execute(self, context):
        prefs = utils.common.prefs()
        csv = prefs.csv_path
        
        if(not os.path.exists(csv)):
            self.report({'ERROR'}, "No such file: {}".format(csv))
            return {'FINISHED'}
        
        p = platform.system()
        if(p == 'Windows'):
            os.startfile(os.path.normpath(csv))
        else:
            raise OSError("Unknown platform: {}.".format(csv))
        
        return {'FINISHED'}

class PF_OT_clear_alldata(bpy.types.Operator):
    bl_idname = "pomofocus.clear_alldata"
    bl_label = "Clear Data"
    bl_description = "Removes all tracked data."
    
    def execute(self, context):
        prefs = utils.common.prefs()
        p = prefs.csv_path
        try:
            with open(p, mode='w', encoding='utf-8') as f:
                f.write("{0}\n".format(prefs.csv_first_line))
        except PermissionError:
            bpy.ops.message.messagebox('INVOKE_DEFAULT', message = 'Please close the file before clearing the data', alrt_message = 'Error')
        return {'FINISHED'}


        