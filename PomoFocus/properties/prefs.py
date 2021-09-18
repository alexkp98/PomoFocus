import bpy, os
from bpy.props import (StringProperty, BoolProperty, IntProperty, EnumProperty, FloatProperty)
import rna_keymap_ui
from .. import utils
from ..operators import PomoFocus_Addonkey
import datetime

class Utils():

    @staticmethod
    def get_default_csv_path():
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "{0}.csv".format('Pomodoro List'))


class Runtime():
    start = datetime.datetime.now()

def update(self, context):
    prefs = Utils.get_preferences()
    
    current = prefs.csv_path
    previous = prefs.previous_csv_path
    
    if(current == previous):
        # no change
        return
    
    Runtime.path_message = ""
    
    if(current == ""):
        current = Utils.get_default_csv_path()
    
    if(os.path.isdir(current)):
        current = os.path.join(current, os.path.split(Utils.get_default_csv_path())[1])
    
    current = bpy.path.ensure_ext(current, ".csv", case_sensitive=True, )
    
    d = os.path.split(current)[0]
    if(not os.access(d, os.W_OK)):
        current = Utils.get_default_csv_path()
    if(current != previous and not os.path.exists(current) and os.path.exists(previous)):
        with open(current, mode='w', encoding='utf-8') as f:
            with open(previous, encoding='utf-8') as o:
                c = "".join(o.readlines())
            f.write(c)
    
    prefs.previous_csv_path = current
    prefs.csv_path = current


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
                 ('Sounds', "Sounds", "Sounds")), default='Pomodoro Settings')

    srtbrk_dur : EnumProperty(items=srtbrk, description='Short Break Duration', 
                name='Short Break', default = default_srtbrk)

    lngbrk_dur : EnumProperty(items=lngbrk, description='Long Break Duration', 
                name='Long Break', default = default_lngbrk)

    pomod_dur : EnumProperty(items=pomoDur, description='Simgle Pomodoro Duration', 
                name='Pomodoro Duration', default = default_pomoDur)

    lng_pomoCount : EnumProperty(items=pomoCount, name='Pomodoro count', 
                description='Pomodoro count for long break', default=default_pomoCount)

    scriptdir = bpy.path.abspath(os.path.dirname(__file__))

    # Saving the details
    csv_first_line: bpy.props.StringProperty(name=".csv First Line", description=".csv first line to be written, contains field names.", default="Added Date and time,Task Name,Pomodoro's used,Short Break Count,Long Break Count,Total Time Spent,Status", )
    previous_csv_path: bpy.props.StringProperty(name="Previous CSV Path", description="Used to detect path change and to copy old csv from on change.", default=Utils.get_default_csv_path(), maxlen=1024, subtype='FILE_PATH', )
    csv_path: bpy.props.StringProperty(name="CSV Path", description="Location of .csv with tracking data.", default=Utils.get_default_csv_path(), update=update, maxlen=1024, subtype='FILE_PATH', )
    file_status : BoolProperty(default = False)
    
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
        default = True)

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.prop(self, "prefs_tabs", expand=True)

        if self.prefs_tabs == 'Pomodoro Settings':
            
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
            row.prop(self, 'enable_reset', text='Enable the Reset Button', icon='NONE')
        
            
        if self.prefs_tabs == 'keymaps':
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
        
        if self.prefs_tabs == 'Sounds':
            column = layout.column()
            # playendfile
            column.prop(self,'playtickfile')
            column.prop(self,'use_tick')
            column.prop(self,'playendfile')
            column.prop(self,'use_endSound')
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


