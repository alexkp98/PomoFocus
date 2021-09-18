import bpy
from bpy.app.handlers import persistent
from .. import utils
from ...__init__ import bl_info
from . updater import Pomofocus_OT_CheckUpdate
from .all_operators import( 
                        PomoFocus_OT_Pomostart,
                        PomoFocus_OT_popup,
                        PomoFocus_Addonkey,
                        PF_OT_open_csv,
                        PF_OT_clear_alldata,
                        MessageBox,
                        ResetTime,
                        add_hotkey,
                        remove_hotkey,
                        
                        )

classes = [Pomofocus_OT_CheckUpdate,
           PomoFocus_OT_Pomostart,
           PomoFocus_OT_popup,
           PomoFocus_Addonkey,
           PF_OT_open_csv,
           PF_OT_clear_alldata,
           MessageBox,
           ResetTime
	]

@persistent
def load_handler(dummy):
    if bpy.app.timers.is_registered(PomoFocus_OT_Pomostart.check_pomo):
        bpy.app.timers.unregister(PomoFocus_OT_Pomostart.check_pomo)

    if bpy.app.timers.is_registered(PomoFocus_OT_Pomostart.check_srtbrk):
        bpy.app.timers.unregister(PomoFocus_OT_Pomostart.check_srtbrk)

    if bpy.app.timers.is_registered(PomoFocus_OT_Pomostart.check_lngbrk):
        bpy.app.timers.unregister(PomoFocus_OT_Pomostart.check_lngbrk)
    pomogrp = utils.common.props()
    pomogrp.pomotimer_run_stat = False
    pomogrp.srttimer_run_stat = False
    pomogrp.lngtimer_run_stat = False
    pomogrp.anytimerrinning = False
    pomogrp.rem_minute = 0
    pomogrp.rem_seconds = 0
    pomogrp.esti_pomo = 1
    pomogrp.complted_pomo = 0
    pomogrp.complted_lng = 0
    pomogrp.complted_srt = 0

def register():
    # Reset Updater
    prefs = utils.common.prefs()
    prefs.needs_update = ""
    # Pass current add-on version to Updater
    updater.addon_version = bl_info['version']
    add_hotkey()
    for c in classes:
        bpy.utils.register_class(c)
    
    bpy.types.Scene.pomofocus_idx = bpy.props.IntProperty(name = "Index for my Pomodoro Tasks", default = 0)
    bpy.app.handlers.load_post.append(load_handler)

# unregistering 
def unregister():
    remove_hotkey()
    for c in classes:
        bpy.utils.unregister_class(c)

    if bpy.app.timers.is_registered(PomoFocus_OT_Pomostart.check_pomo):
        bpy.app.timers.unregister(PomoFocus_OT_Pomostart.check_pomo)

    if bpy.app.timers.is_registered(PomoFocus_OT_Pomostart.check_srtbrk):
        bpy.app.timers.unregister(PomoFocus_OT_Pomostart.check_srtbrk)

    if bpy.app.timers.is_registered(PomoFocus_OT_Pomostart.check_lngbrk):
        bpy.app.timers.unregister(PomoFocus_OT_Pomostart.check_lngbrk)
    pomogrp = utils.common.props()
    pomogrp.pomotimer_run_stat = False
    pomogrp.srttimer_run_stat = False
    pomogrp.lngtimer_run_stat = False
    pomogrp.anytimerrinning = False
    pomogrp.rem_minute = 0
    pomogrp.rem_seconds = 0
    pomogrp.esti_pomo = 1
    pomogrp.complted_pomo = 0
    pomogrp.complted_lng = 0
    pomogrp.complted_srt = 0
    
    try:
        del bpy.types.Scene.pomofocus_idx
        
    except:
        pass
    
    