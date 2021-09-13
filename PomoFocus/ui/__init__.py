import bpy
from . panel import PF_PT_NPanel,draw_pomodoro


# registering 
def register():
    bpy.utils.register_class(PF_PT_NPanel)
# unregistering 
def unregister():
    bpy.utils.unregister_class(PF_PT_NPanel)