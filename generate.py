from pycomcigan import TimeTable
from ics import Calendar, Event
from datetime import datetime, timedelta
import pytz

SCHOOL_NAME = "부산장안고등학교"
GRADE = 2
CLASS = 3

tz = pytz.timezone("Asia/Seoul")
calendar = Calendar()

today = datetime.now()

# 기준: 이번주 월요일
monday = today - timedelta(days=today.weekday())

tt = TimeTable(SCHOOL_NAME)

week_data = tt.timetable[GRADE][CLASS]

# 🔥 핵심: 평탄화 (flatten)
flat_days = []
for d in week_data:
    if isinstance(d, list):
        flat_days.append(d)

# 👉 이제 "그냥 순서대로 날짜 매핑"
for i, day in enumerate(flat_days[:5]):  # 월~금만

    current_day = monday + timedelta(days=i)

    for period, subject in enumerate(day, start=1):

        if not subject:
            continue

        start_times = [
            ("08:30", "09:20"),
            ("09:30", "10:20"),
            ("10:30", "11:20"),
            ("11:30", "12:20"),
            ("13:20", "14:10"),
            ("14:20", "15:10"),
            ("15:20", "16:10"),
        ]

        if period > len(start_times):
            continue

        sh, sm = map(int, start_times[period - 1][0].split(":"))
        eh, em = map(int, start_times[period - 1][1].split(":"))

        start_dt = tz.localize(datetime(current_day.year, current_day.month, current_day.day, sh, sm))
        end_dt = tz.localize(datetime(current_day.year, current_day.month, current_day.day, eh, em))

        event = Event()
        event.name = str(subject)
        event.begin = start_dt
        event.end = end_dt
        event.description = f"{GRADE}학년 {CLASS}반"

        event.uid = f"{current_day:%Y%m%d}-{period}-{GRADE}-{CLASS}"

        calendar.events.add(event)

with open("timetable.ics", "w", encoding="utf-8") as f:
    f.writelines(calendar)

print("ICS 생성 완료")
