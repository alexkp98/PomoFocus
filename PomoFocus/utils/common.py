import bpy
from .. import properties

def module() -> str:
    return properties.PomoFocus_property.name

def prefs() -> bpy.types.AddonPreferences:
    return bpy.context.preferences.addons[module()].preferences

def props() -> bpy.types.PropertyGroup:
    return bpy.context.scene.pomoproperty