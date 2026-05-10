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

# 👉 기준: "이번 주 월요일 00:00"
this_monday = (today - timedelta(days=today.weekday())).replace(
    hour=0, minute=0, second=0, microsecond=0
)

# ==========================
# 핵심 수정 포인트
# ==========================
# pycomcigan week_num은 "주차 기준이 흔들림"
# → 그래서 완전히 무시하고 "날짜로만 계산"

tt = TimeTable(SCHOOL_NAME)

try:
    week_data = tt.timetable[GRADE][CLASS]
except Exception:
    print(tt.timetable)
    raise Exception("학년/반 확인 필요")

# ==========================
# 시간표 생성 (이번주 + 다음주)
# ==========================
for week_offset in range(2):  # 0=이번주, 1=다음주

    for weekday_index, day in enumerate(week_data):

        if weekday_index >= 5:
            continue

        # 🔥 핵심: 주 + 요일을 직접 합산
        current_day = this_monday + timedelta(
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

            # 중복 방지
            event.uid = f"{current_day:%Y%m%d}-{period}-{GRADE}-{CLASS}"

            calendar.events.add(event)

# ==========================
# 저장
# ==========================
with open("timetable.ics", "w", encoding="utf-8") as f:
    f.writelines(calendar)

print("ICS 생성 완료")
