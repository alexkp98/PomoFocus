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

    year: IntProperty(default=PomoStatic.current_time.year)
    month: IntProperty(default=PomoStatic.current_time.month)
    day: IntProperty(default=PomoStatic.current_time.day)
    hour: IntProperty(default=PomoStatic.current_time.hour)
    minute: IntProperty(default=PomoStatic.current_time.minute)
    secs: IntProperty(default=PomoStatic.current_time.second)

    srtyear: IntProperty(default=PomoStatic.current_time.year)
    srtmonth: IntProperty(default=PomoStatic.current_time.month)
    srtday: IntProperty(default=PomoStatic.current_time.day)
    srthour: IntProperty(default=PomoStatic.current_time.hour)
    srtminute: IntProperty(default=PomoStatic.current_time.minute)
    srtsecs: IntProperty(default=PomoStatic.current_time.second)

    lngyear: IntProperty(default=PomoStatic.current_time.year)
    lngmonth: IntProperty(default=PomoStatic.current_time.month)
    lngday: IntProperty(default=PomoStatic.current_time.day)
    lnghour: IntProperty(default=PomoStatic.current_time.hour)
    lngminute: IntProperty(default=PomoStatic.current_time.minute)
    lngsecs: IntProperty(default=PomoStatic.current_time.second)

    total_timeSpent :StringProperty(name="Total time", default='00h 00m 00s')
    anytimerrinning : BoolProperty(default = False)