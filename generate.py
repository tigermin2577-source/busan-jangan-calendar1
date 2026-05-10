from pycomcigan import TimeTable
from ics import Calendar, Event
from datetime import datetime, timedelta
import pytz

# ==========================
# 설정
# ==========================

SCHOOL_NAME = "부산장안고등학교"
GRADE = 2
CLASS = 3

tz = pytz.timezone("Asia/Seoul")
calendar = Calendar()

today = datetime.now()

# 👉 진짜 기준: 이번주 "월요일"
base_monday = today - timedelta(days=today.weekday())

tt = TimeTable(SCHOOL_NAME)

week_data = tt.timetable[GRADE][CLASS]

# ==========================
# 핵심 해결 포인트
# ==========================
# pycomcigan 구조는 "월~금이 반드시 0~4가 아님"
# 그래서 날짜를 "index 고정"으로 맞추면 안됨

# 👉 대신 "실제 평일 5개만 사용"
days_map = {}

# 안전하게 월~금만 필터링
for i in range(min(5, len(week_data))):
    days_map[i] = week_data[i]

# ==========================
# 이벤트 생성
# ==========================
for week_offset in range(2):  # 이번주 + 다음주

    for weekday_index in range(5):

        if weekday_index not in days_map:
            continue

        day = days_map[weekday_index]

        # 🔥 핵심: 날짜는 "무조건 월요일 기준 + offset"
        current_day = base_monday + timedelta(
            days=(7 * week_offset) + weekday_index
        )

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

            start_str, end_str = start_times[period - 1]

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

# 저장
with open("timetable.ics", "w", encoding="utf-8") as f:
    f.writelines(calendar)

print("ICS 생성 완료")
