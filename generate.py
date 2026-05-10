from pycomcigan import TimeTable
from ics import Calendar, Event
from datetime import datetime, timedelta
import pytz

# ==========================
# 설정
# ==========================

SCHOOL_NAME = "부산장안고등학교"
GRADE = 1
CLASS = 2

# ==========================

PERIOD_TIMES = {
    1: ("08:30", "09:20"),
    2: ("09:30", "10:20"),
    3: ("10:30", "11:20"),
    4: ("11:30", "12:20"),
    5: ("13:20", "14:10"),
    6: ("14:20", "15:10"),
    7: ("15:20", "16:10"),
}

tz = pytz.timezone("Asia/Seoul")
calendar = Calendar()

today = datetime.now()

# 👉 "오늘 기준 이번주 월요일"
monday = today - timedelta(days=today.weekday())

tt = TimeTable(SCHOOL_NAME)

week_data = tt.timetable[GRADE][CLASS]

# ==========================
# 핵심 해결 포인트
# ==========================
# pycomcigan 구조:
# 0=월, 1=화, 2=수, 3=목, 4=금

for week_offset in range(2):  # 이번주 + 다음주

    for weekday_index, day in enumerate(week_data):

        if weekday_index >= 5:
            continue

        # 🔥 핵심: 절대 기준 고정
        current_day = monday + timedelta(
            days=weekday_index + (7 * week_offset)
        )

        for period, subject in enumerate(day, start=1):

            if not subject:
                continue

            if period not in PERIOD_TIMES:
                continue

            start_str, end_str = PERIOD_TIMES[period]

            sh, sm = map(int, start_str.split(":"))
            eh, em = map(int, end_str.split(":"))

            start_dt = tz.localize(
                datetime(current_day.year, current_day.month, current_day.day, sh, sm)
            )

            end_dt = tz.localize(
                datetime(current_day.year, current_day.month, current_day.day, eh, em)
            )

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
