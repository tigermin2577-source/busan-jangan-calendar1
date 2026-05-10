from pycomcigan import TimeTable
from ics import Calendar, Event
from datetime import datetime, timedelta
import pytz

# ==========================
# 여기만 수정
# ==========================

SCHOOL_NAME = "부산장안고등학교"

GRADE = 1
CLASS = 5

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

tt = TimeTable(SCHOOL_NAME)

# 학년/반 체크
grade_data = (
    tt.timetable.get(GRADE)
    or tt.timetable.get(str(GRADE))
)

if not grade_data:
    print(tt.timetable)
    raise Exception("학년 없음")

week_data = (
    grade_data.get(CLASS)
    or grade_data.get(str(CLASS))
)

if not week_data:
    print(grade_data)
    raise Exception("반 없음")

today = datetime.now()

monday = today - timedelta(days=today.weekday())

for weekday, day in enumerate(week_data):

    current_day = monday + timedelta(days=weekday)

    for period, subject in enumerate(day, start=1):

        if not subject:
            continue

        if period not in PERIOD_TIMES:
            continue

        start_str, end_str = PERIOD_TIMES[period]

        sh, sm = map(int, start_str.split(":"))
        eh, em = map(int, end_str.split(":"))

        start_dt = tz.localize(
            datetime(
                current_day.year,
                current_day.month,
                current_day.day,
                sh,
                sm,
            )
        )

        end_dt = tz.localize(
            datetime(
                current_day.year,
                current_day.month,
                current_day.day,
                eh,
                em,
            )
        )

        event = Event()

        event.name = subject
        event.begin = start_dt
        event.end = end_dt

        event.description = f"{GRADE}학년 {CLASS}반"

        # Apple Calendar 중복 방지용
        event.uid = f"{current_day}-{period}-{GRADE}-{CLASS}"

        calendar.events.add(event)

with open("timetable.ics", "w", encoding="utf-8") as f:
    f.writelines(calendar)

print("ICS 생성 완료")
