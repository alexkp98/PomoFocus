import bpy
from .. import operators
from .. import utils
from datetime import datetime, timedelta
import calendar
import aud


class PF_PT_NPanel(bpy.types.Panel):
    bl_idname = "PF_PT_NPanel"
    bl_category = "PomoFocus"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Pomodoro"

    def draw(self, context):
        draw_pomodoro(self,context)
       
def draw_pomodoro(self, context):
    l = self.layout
    pomo_grp = context.scene.pomoproperty
    row = l.row()
    row.ui_units_x = 5
    row.scale_y = 5
    row.alignment="CENTER"
    row.label(
            text='{:02} Minute(s) :{:02} Second(s)'.format(pomo_grp.rem_minute,pomo_grp.rem_seconds ))
    
    
    if pomo_grp.anytimerrinning == False:
        box = l.box()
        box.label(text='What you are focusing on?')
        box.prop(pomo_grp, "taskname", text="")
        box.label(text='Time needed to finish the task?')
        box.prop(pomo_grp, "esti_pomo", text="Pomodoro")
        # box.operator("pomofocus.open_csv", text= 'Open Data', icon= "NONE")
        # box.operator("pomofocus.clear_alldata", text= 'Open Data', icon= "NONE")
        boxcol = box.column()
        rows = boxcol.row()
        rows.operator("pomofocus.open_csv", text= 'Open Data', icon= "NONE")
        rows.operator("pomofocus.clear_alldata",text= 'Clear Data', icon="NONE")
        boxcol = box.column()
        rows = boxcol.row()
        rows.operator("pomofocus.pomostart", text= 'Start Pomodoro', icon= "PLAY")
        rows.operator(
                "preferences.addon_show", icon="SETTINGS"
                    ).module = utils.common.module()

    else:
        box = l.box()
        boxcol = box.column()            
        boxcol.label(text = 'Selected task to complete:')
        boxcol.label(text = pomo_grp.taskname)
        box = l.box()
        boxcol = box.column()
        boxcol.label(text=('{}: {}'.format('Estimated Pomodoro Count ', pomo_grp.esti_pomo )), icon='NONE')
        boxcol.label(text=('{}: {}'.format('Completed Pomodoro Count ', pomo_grp.complted_pomo )), icon='NONE')
        box = l.box()
        boxcol = box.column()
        rows = boxcol.row()
        prefs = utils.common.prefs()
        rows.enabled = prefs.enable_reset
        rows.operator("pomofocus.resettime", text= 'Reset to default', icon= "FILE_REFRESH")
        # rows = boxcol.row()
        rows.operator(
                "preferences.addon_show", icon="SETTINGS"
                    ).module = utils.common.module()
 