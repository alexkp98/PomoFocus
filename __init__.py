# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "PomoFocusV3",
    "author" : "Alex Paul",
    "description" : "",
    "blender" : (2, 91, 0),
    "version" : (3, 0, 0),
    "location" : "View3D - N panel(default)",
    "tracker_url" : (
        "https://github.com/alexkp98/PomoFocus/issues/new?assignees=&labels=&template=bug_report.md&title="),
    # "wiki_url": (
    #     "##Documentation link"),
    "category" : "3D View"
}

from . import PomoFocus

def register():
    PomoFocus.register()

def unregister():
    PomoFocus.unregister()
