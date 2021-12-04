import bpy, os
from bpy.props import (StringProperty, BoolProperty, IntProperty, EnumProperty, FloatProperty)
import rna_keymap_ui
from .. import utils
from ..operators import PomoFocus_Addonkey
import datetime
from ..operators.updater import changelog,latest_msg
# from .PomoFocus_property import timeCalc

class Utils():

    @staticmethod
    def get_default_csv_path():
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "{0}.csv".format('Pomodoro List'))

def timeCalcDefault(self, context):
    pomogrp = utils.common.props()
    totalPomotime = (pomogrp.esti_pomo) * int(self.pomod_dur)
    totalsrttime = (pomogrp.esti_pomo) * int(self.srtbrk_dur)
    if pomogrp.esti_pomo >= int(self.lng_pomoCount):
        lng = pomogrp.esti_pomo % int(self.lng_pomoCount)
        totallngtime = lng * int(self.lngbrk_dur)
        pomogrp.TimeCalc = int(totalPomotime) + int(totalsrttime) + int(totallngtime)
        totaltime = Runtime.start + datetime.timedelta(minutes = pomogrp.TimeCalc) 
        pomogrp.est_clk = totaltime.strftime("%Y-%m-%d %H:%M")

    else:
        pomogrp.TimeCalc = int(totalPomotime) + int(totalsrttime)
        totaltime = Runtime.start + datetime.timedelta(minutes = pomogrp.TimeCalc) 
        pomogrp.est_clk = totaltime.strftime("%Y-%m-%d %H:%M")

class Runtime():
    start = datetime.datetime.now()

class PomoFocus_AP_Prefs(bpy.types.AddonPreferences):

    srtbrk = [('1', '1', ''),
              ('3', '3', ''),
              ('5', '5', ''),
              ('8', '8', ''),
              ('10', '10', '')]

    lngbrk = [('1', '1', ''),
              ('15', '15', ''),
              ('20', '20', ''),
              ('25', '25', '')]

    pomoDur = [('15', '15', ''),
               ('20', '20', ''),
               ('25', '25', ''),
               ('30', '30', '')]

    pomoCount = [('3', '3', ''),
               ('4', '4', ''),
               ('5', '5', ''),
               ('6', '6', '')]

    default_srtbrk = srtbrk[1][1]
    default_lngbrk = lngbrk[1][1]
    default_pomoDur = pomoDur[2][1]
    default_pomoCount = pomoCount[1][1]

    bl_idname = utils.common.module()

    prefs_tabs: EnumProperty(items=(('Pomodoro Settings', "Pomodoro Settings", "Pomodoro Settings"),
                 ('keymaps', "Keymaps", "Keymaps"),
                 ('Sounds', "Sounds", "Sounds"),
                 ('Update', "Update", "Update")), default='Pomodoro Settings')

    srtbrk_dur : EnumProperty(items=srtbrk, description='Short Break Duration', 
                name='Short Break', default = default_srtbrk, update =timeCalcDefault )

    lngbrk_dur : EnumProperty(items=lngbrk, description='Long Break Duration', 
                name='Long Break', default = default_lngbrk, update =timeCalcDefault)

    pomod_dur : EnumProperty(items=pomoDur, description='Simgle Pomodoro Duration', 
                name='Pomodoro Duration', default = default_pomoDur, update =timeCalcDefault)

    lng_pomoCount : EnumProperty(items=pomoCount, name='Pomodoro count', 
                description='Pomodoro count for long break', default=default_pomoCount, update =timeCalcDefault)

    scriptdir = bpy.path.abspath(os.path.dirname(__file__))

    # Saving the details
    csv_first_line: bpy.props.StringProperty(name=".csv First Line", description=".csv first line to be written, contains field names.", default="Added Date and time,Task Name,Pomodoro's used,Short Break Count,Long Break Count,Total Time Spent,Status", )
    csv_path: bpy.props.StringProperty(name="CSV Path", description="Location of .csv with tracking data.", default=Utils.get_default_csv_path(), maxlen=1024, subtype='FILE_PATH', )
    file_status : BoolProperty(default = False)

    # Updater Preference
    needs_update : StringProperty()
    changelog_expanded : BoolProperty(
        default= False,
    )

    # 2.93 check
    is_293 : BoolProperty(default = False)


    playtickfile: StringProperty(
        name = "Select ticking sound",
        description = "Music to play while Timer is running",
        subtype = 'FILE_PATH',
        default = scriptdir + "/tick.mp3")

    playendfile: StringProperty(
        name = "Select End sound",
        description = "Music to play after pomodoro completes",
        subtype = 'FILE_PATH',
        default = scriptdir + "/ring.mp3")

    show_sbinfo: BoolProperty(name="", 
                description="Recommended time for short break is 5 minutes",
                default=False)
    
    show_lbinfo: BoolProperty(name="", 
                description="Recommended time for long break is 20 minutes",
                default=False)
    
    show_ptinfo: BoolProperty(name="", 
                description="Recommended time for one pomodoro is 25 minutes",
                default=False)
    
    show_pcinfo: BoolProperty(name="", 
                description="Recommended count long break is 4",
                default=False)

    enable_reset: BoolProperty(name="", 
                description="Enable the Reset Button",
                default=False)
    
    use_tick: BoolProperty(
        name = "Play Tick sound",
        description = "Enable the ability to play sound while running",
        default = False)
    use_endSound: BoolProperty(
        name = "Play sound upon Pomodoro task completion",
        description = "Enable the ability to play a sound when a Pomodoro task completes",
        default = False)

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.prop(self, "prefs_tabs", expand=True)

        if self.prefs_tabs == 'Pomodoro Settings' :
            
            column = layout.column()
            row = column.row()
            props = utils.common.props()
            disable = props.anytimerrinning
            row.enabled = not disable
            row.label(text='Select short break duration: ')
            row.prop(self, 'srtbrk_dur', text='', icon='TIME')
            row.prop(self,'show_sbinfo', text='', icon = 'QUESTION', emboss=False)
            if self.show_sbinfo:
                column = layout.column()
                column.label(text='Recommended time for short break is 5 minutes', icon='INFO')

            column = layout.column()
            row = column.row()
            row.enabled = not disable
            row.label(text='Select long break duration: ')
            row.prop(self, 'lngbrk_dur', text='', icon='TIME')
            row.prop(self,'show_lbinfo', text='', icon = 'QUESTION', emboss=False)
            if self.show_lbinfo:
                column = layout.column()
                column.label(text='Recommended time for long break is 20 minutes', icon='INFO')

            column = layout.column()
            row = column.row()
            row.enabled = not disable
            row.label(text='Select single pomodoro duration: ')
            row.prop(self, 'pomod_dur', text='', icon='TIME')
            row.prop(self,'show_ptinfo', text='', icon = 'QUESTION', emboss=False)
            if self.show_ptinfo:
                column = layout.column()
                column.label(text='Recommended time for one pomodoro is 25 minutes', icon='INFO')

            column = layout.column()
            row = column.row()
            row.enabled = not disable
            row.label(text='Select pomodoro count for long break: ')
            row.prop(self, 'lng_pomoCount', text='', icon='NONE')
            row.prop(self,'show_pcinfo', text='', icon = 'QUESTION', emboss=False)
            if self.show_pcinfo:
                column = layout.column()
                column.label(text='Recommended count long break is 4 Pomodoro', icon='INFO')
            box = layout.box()
            row = box.row()
            row.enabled = not disable
            row.label(text='Remove all the data from the file:')
            row.operator("pomofocus.clear_alldata",text= 'Clear Data', icon="NONE")
            row = box.row()
            row.label(text='Data cannot be Restored',icon ="ERROR")
            box = layout.box()
            row = box.row()
            row.prop(self, 'enable_reset', text='Enable the Reset Button', icon='NONE')
             
        if self.prefs_tabs == 'keymaps' :
            column = layout.column()
            column.label(text='Add Shortcut for Pomodoro')
            box = layout.box()
            col = box.column()
            col.label(text='Setup Hotkey (shortcut works only inside blender ): ')
            col.separator()
            col.label(text=('{}: {}'.format('WARNING ', 'Using existing hotkey will replace the old functionality')), icon='ERROR')
            col.separator()
            wm = bpy.context.window_manager
            kc = wm.keyconfigs.user
            km = kc.keymaps['Window']
            kmi = get_hotkey_entry_item(km, 'pomofocus.float')
            if kmi:
                col.context_pointer_set('keymap', km)
                rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
                col.separator()
                col.label(text='Hotkey also listed in Edit -> Preferences -> Keymap -> Window')
            else:
                col.label(text='No hotkey found')
                col.operator((PomoFocus_Addonkey.bl_idname), text='Add hotkey entry')

        if self.prefs_tabs == 'Sounds' and not self.is_293:
            column = layout.column()
                # playendfile
            column.prop(self,'playtickfile')
            column.prop(self,'use_tick')
            column.prop(self,'playendfile')
            column.prop(self,'use_endSound')
        elif self.prefs_tabs == 'Sounds' and self.is_293:
            column = layout.column()
            column.label(text="Not available for 2.93 users")

        if self.prefs_tabs == 'Update':
            wm = bpy.context.window_manager

            box = layout.box()
            split = box.split(factor = 0.45)
            row = split.row()
            row.operator("pomofocus.check_update")
            row = split.row(align=True)
            row.operator("wm.url_open", text="Gumroad").url = "https://gumroad.com/library"
            row.operator("wm.url_open", text="Blender Market").url = "https://blendermarket.com/account/orders"
            if self.needs_update and self.needs_update != latest_msg:
                row = box.row()
                row.alert = True
                row.label(text=self.needs_update)
                
                row = box.row()
                row.prop(self, "changelog_expanded",
                    icon="TRIA_DOWN" if self.changelog_expanded else "TRIA_RIGHT",
                    icon_only=True, emboss=False
                )
                row.label(text='Changelog')
                if self.changelog_expanded:
                    for v in changelog:
                        version_box = box.box()
                        row = version_box.row()
                        row.scale_y = 0.6
                        row.label(text=v[0]+":")
                        
                        split_str = v[1].splitlines()
                        for str in split_str:
                            row = version_box.row()
                            row.scale_y = 0.5
                            row.label(text=str)
            if self.needs_update == latest_msg:
                row = box.row()
                row.label(text=latest_msg)            
            else:
                row = box.row()
                row.label(text="Press 'Check for Updates' to verify if you are "
                        "running the latest version of the add-on.")
    def execute(self, context):
        return {'FINISHED'}


def get_hotkey_entry_item(km, kmi_name):
    for i, km_item in enumerate(km.keymap_items):
        if km.keymap_items.keys()[i] == kmi_name:
            return km_item
    return None

def start():
    
    prefs = utils.common.prefs()
    p = prefs.csv_path
    
    # write starting csv if there is none
    if(not os.path.exists(p)):
        with open(p, mode='w', encoding='utf-8') as f:
            f.write("{0}\n".format(prefs.csv_first_line))


