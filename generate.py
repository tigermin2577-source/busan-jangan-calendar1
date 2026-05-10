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

# 이번 주 월요일
this_monday = today - timedelta(days=today.weekday())

# 이번 주 + 다음 주
for week_offset in [0, 1]:

    tt = TimeTable(SCHOOL_NAME, week_num=week_offset)

    try:
        week_data = tt.timetable[GRADE][CLASS]
    except Exception as e:
        print(tt.timetable)
        raise Exception(f"학년/반 확인 필요: {e}")

    # 실제 날짜 계산
    base_day = this_monday + timedelta(days=7 * week_offset)

    # 월~금
    for weekday in range(1, 6):

        try:
            day = week_data[weekday]
        except:
            continue

        current_day = base_day + timedelta(days=weekday - 1)

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

            event.name = str(subject)
            event.begin = start_dt
            event.end = end_dt

            event.description = f"{GRADE}학년 {CLASS}반"

            # Apple Calendar 중복 방지
            event.uid = (
                f"{current_day.strftime('%Y%m%d')}"
                f"-{period}-{GRADE}-{CLASS}"
            )

            calendar.events.add(event)

# 저장
with open("timetable.ics", "w", encoding="utf-8") as f:
    f.writelines(calendar)

print("ICS 생성 완료")
