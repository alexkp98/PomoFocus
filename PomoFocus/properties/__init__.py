import bpy
from . PomoFocus_property import PomoFocus_PG_Properties
from .prefs import PomoFocus_AP_Prefs,start


def register():
    bpy.types.Scene.music_handle = None
    bpy.utils.register_class(PomoFocus_AP_Prefs)
    bpy.utils.register_class(PomoFocus_PG_Properties)
    bpy.types.Scene.pomoproperty = bpy.props.PointerProperty(type=PomoFocus_PG_Properties)
    start()

def unregister():
    bpy.utils.unregister_class(PomoFocus_AP_Prefs)
    bpy.utils.unregister_class(PomoFocus_PG_Properties)
    try:
        del bpy.types.Scene.pomoproperty
        
    except:
        pass