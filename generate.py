from pycomcigan import TimeTable
from ics import Calendar, Event
from datetime import datetime, timedelta
import pytz

# ==========================
# 여기만 수정
# ==========================

SCHOOL_NAME = "부산장안고등학교"

GRADE = 1
CLASS = 2

# ==========================

PERIOD_TIMES = {
    1: ("08:40", "09:30"),
    2: ("09:40", "10:30"),
    3: ("10:40", "11:30"),
    4: ("11:40", "12:30"),
    5: ("13:30", "14:20"),
    6: ("14:40", "15:30"),
    7: ("15:40", "16:30"),
}

tz = pytz.timezone("Asia/Seoul")

calendar = Calendar()

today = datetime.now()

monday = today - timedelta(days=today.isoweekday() - 1)

# ==========================
# 시간표 가져오기
# ==========================

tt = TimeTable(SCHOOL_NAME)
week_data = tt.timetable[GRADE][CLASS]

# ==========================
# 날짜 생성 (핵심 안정 구조)
# ==========================

for day_index in range(5):  # 월~금 고정

    current_day = monday + timedelta(days=day_index)
    day = week_data[day_index]

    for period, subject in enumerate(day, start=1):

        if not subject:
            continue

        if period not in PERIOD_TIMES:
            continue

        start_str, end_str = PERIOD_TIMES[period]
        sh, sm = map(int, start_str.split(":"))
        eh, em = map(int, end_str.split(":"))

        start_dt = tz.localize(datetime(
            current_day.year,
            current_day.month,
            current_day.day,
            sh,
            sm
        ))

        end_dt = tz.localize(datetime(
            current_day.year,
            current_day.month,
            current_day.day,
            eh,
            em
        ))

        event = Event()
        event.name = str(subject)
        event.begin = start_dt
        event.end = end_dt
        event.description = f"{GRADE}학년 {CLASS}반"

        # 🔥 중복 방지 (완전 안정)
        event.uid = f"{current_day:%Y%m%d}-{period}-{GRADE}-{CLASS}"

        calendar.events.add(event)

# ==========================
# 저장
# ==========================

with open("timetable.ics", "w", encoding="utf-8") as f:
    f.writelines(calendar)

print("ICS 생성 완료")
