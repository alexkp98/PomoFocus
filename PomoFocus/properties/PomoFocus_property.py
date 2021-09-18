import bpy
from datetime import datetime
from bpy.props import (StringProperty, BoolProperty, IntProperty)

name = __name__.partition('.')[0]

class PomoStatic:
    current_time = datetime.now()

class PomoFocus_PG_Properties(bpy.types.PropertyGroup):
    
    lngtimer_run_stat : BoolProperty(default = False)
    pomotimer_run_stat : BoolProperty(default = False)
    srttimer_run_stat : BoolProperty(default = False)
    rem_minute: IntProperty(default=0)
    rem_seconds: IntProperty(default=0)
    taskname: StringProperty(name="Title", default='New Pomodoro')
    csv_status: StringProperty(name="Satus", default='')
    added_time: StringProperty(name="Time and Date", default='')
    esti_pomo: IntProperty(default=1, min = 1, max = 10)
    
    estipomo_time : StringProperty(name="alarm time", default='NaN')
    estisrt_time : StringProperty(name="short break time", default='NaN')
    estilng_time : StringProperty(name="long break time", default='NaN')

    complted_pomo : IntProperty(default=0)
    complted_lng : IntProperty(default=0)
    complted_srt : IntProperty(default=0)
    
    ct = PomoStatic.current_time
    year: IntProperty(default=ct.year)
    month: IntProperty(default=ct.month)
    day: IntProperty(default=ct.day)
    hour: IntProperty(default=ct.hour)
    minute: IntProperty(default=ct.minute)
    secs: IntProperty(default=ct.second)

    srtyear: IntProperty(default=ct.year)
    srtmonth: IntProperty(default=ct.month)
    srtday: IntProperty(default=ct.day)
    srthour: IntProperty(default=ct.hour)
    srtminute: IntProperty(default=ct.minute)
    srtsecs: IntProperty(default=ct.second)

    lngyear: IntProperty(default=ct.year)
    lngmonth: IntProperty(default=ct.month)
    lngday: IntProperty(default=ct.day)
    lnghour: IntProperty(default=ct.hour)
    lngminute: IntProperty(default=ct.minute)
    lngsecs: IntProperty(default=ct.second)

    total_timeSpent :StringProperty(name="Total time", default='00h 00m 00s')
    anytimerrinning : BoolProperty(default = False)