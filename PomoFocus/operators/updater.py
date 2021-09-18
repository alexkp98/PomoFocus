import re
import requests
import bpy

from .. import utils

update_url = 'https://api.github.com/repos/alexkp98/PomoFocus/releases'
ver_regex = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+")
changelog = []
latest_msg = "You are running the latest version of PomoFocus add-on."

class Pomofocus_OT_CheckUpdate(bpy.types.Operator):
    bl_idname = "pomofocus.check_update"
    bl_label = "Check for Updates"
    bl_description = "checks if you are running the latest version"

    def execute(self,context):
        prefs = utils.common.prefs()
        prefs.needs_update = ""

        try:
            response = requests.get(update_url)
            if response.status_code == 200:
                resp_json = response.json()
                versions = list()
                
                for release in resp_json:
                    ver_info = [release['tag_name'],release['body']]          
                    if ver_regex.match(ver_info[0]):
                        versions.append(ver_info)
                versions = sorted(versions, reverse=True)

                lst_verStr = versions[0][0]
                print(lst_verStr)
                crnt_verStr = '.'.join(map(str, list(addon_version)))
                
                if str(crnt_verStr) < str(lst_verStr):
                    needs_update = f"PomoFocus {lst_verStr} is available!"
                    changelog.clear()
                    for ver in versions:
                        if ver[0] > crnt_verStr:
                            changelog.append(ver)
                    prefs.needs_update = needs_update
                else:
                    prefs.needs_update = latest_msg

        except:
            prefs.needs_update = 'Update Check Failed.'
            
        return{'FINISHED'}
