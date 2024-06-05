import random
from datetime import datetime, timedelta

import pytz
from faker import Faker
from tqdm import tqdm

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from blog.models import Post, Comment
from checking.models import Member, Attendance
from report.models import UserCheck, MemberCheck

fake = Faker(locale="ko_KR")
User = get_user_model()


# BaseCommand를 상속
# python manage.py create_fake_data
class Command(BaseCommand):
    def handle(self, *args, **options):
        user_list = []
        post_list = []
        comment_list = []

        for __ in tqdm(range(2), desc="교사 생성"):
            username = fake.email().split("@")[0]
            password = username  # 이후 API 테스트할 때, 인증을 위해 유저명으로 암호 설정
            birthday = fake.date_between()
            full_name = fake.name()
            email = f"{username}@example.com"
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                birth_date=birthday,
                full_name=full_name,
            )
            user_list.append(user)

        member_list = []
        grade_list = ["중1", "중2", "중3", "고1", "고2", "고3"]
        gender_list = ["남", "여"]

        for __ in tqdm(range(2), desc="학생 생성"):
            teacher = random.choice(user_list)
            name = fake.name()
            grade = random.choice(grade_list)
            gender = random.choice(gender_list)
            member = Member.objects.create(
                teacher=teacher, name=name, grade=grade, gender=gender
            )
            member_list.append(member)

        # 하나님 앞에서
        worship_choice = [(0, "불참"), (1, "1부 예배"), (2, "2부 예배"), (3, "3부 예배")]
        qt_choice = [
            (0, "0회"),
            (1, "1회"),
            (2, "2회"),
            (3, "3회"),
            (4, "4회"),
            (5, "5회"),
            (6, "6회"),
            (7, "7회"),
        ]

        def get_random_sunday(start_date, end_date, timezone):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            while True:
                random_date = fake.date_between(
                    start_date=start_date, end_date=end_date
                )
                if random_date.weekday() == 6:  # 6은 일요일을 나타냅니다.
                    # datetime.date 객체를 datetime.datetime 객체로 변환
                    random_datetime = datetime.combine(random_date, datetime.min.time())
                    # 타임존을 추가하여 datetime 객체로 반환
                    return timezone.localize(random_datetime)

        start_date = "2023-05-01"
        end_date = "2023-05-31"
        timezone = pytz.timezone("Asia/Seoul")
        date_list = []
        for __ in tqdm(range(2), desc="하나님 앞에서 생성"):
            teacher = random.choice(user_list)
            pray_youth = fake.paragraph(nb_sentences=5, variable_nb_sentences=True)
            pray_group = fake.paragraph(nb_sentences=5, variable_nb_sentences=True)
            pray_user = fake.paragraph(nb_sentences=5, variable_nb_sentences=True)
            pray_emergency = fake.paragraph(nb_sentences=5, variable_nb_sentences=True)
            issue = fake.paragraph(nb_sentences=5, variable_nb_sentences=True)
            meeting = fake.boolean()
            worship = random.choice([choice[0] for choice in worship_choice])
            qt = random.choice([choice[0] for choice in qt_choice])
            date = get_random_sunday(start_date, end_date, timezone)
            # title = fake.sentence(nb_words=6, variable_nb_words=True)[:100]  # 짧은 텍스트

            post = UserCheck(
                teacher=teacher,
                pray_youth=pray_youth,
                pray_group=pray_group,
                pray_user=pray_user,
                pray_emergency=pray_emergency,
                issue=issue,
                worship=worship,
                qt=qt,
                meeting=meeting,
                date=date,
            )
            post_list.append(post)
            date_list.append(date)

        print(f"{len(post_list)}개의 하나님 앞에서 저장 중 ...")
        UserCheck.objects.bulk_create(post_list)

        # 출석 생성
        attendance_list = ["출석", "결석"]
        for __ in tqdm(range(2), desc="출석 생성"):
            name = random.choice(member_list)
            attendance = random.choice(attendance_list)
            date = random.choice(date_list)
            Attendance.objects.create(
                name=name,
                attendance=attendance,
                date=date,
            )

        # 양육일지
        member_check_list = []
        for __ in tqdm(range(2), desc="양육일지 생성"):
            name = random.choice(member_list)
            gqs = fake.boolean()
            status = fake.paragraph(nb_sentences=5, variable_nb_sentences=True)
            pray_member = fake.paragraph(nb_sentences=5, variable_nb_sentences=True)
            date = random.choice(date_list)
            member_check = MemberCheck(
                name=name,
                gqs=gqs,
                status=status,
                pray_member=pray_member,
                date=date,
            )
            member_check_list.append(member_check)

        print(f"{len(member_check_list)}개의 양육일지 저장 중 ...")
        MemberCheck.objects.bulk_create(member_check_list)

        # 댓글 생성
        # for __ in tqdm(range(10000), desc="댓글 생성"):
        #     post = random.choice(post_list)
        #     message = fake.sentence(nb_words=10, variable_nb_words=True)
        #     comment = Comment(
        #         post=post,
        #         message=message,
        #     )
        #     comment_list.append(comment)
        #
        # print(f"{len(comment_list)}개의 댓글 저장 중 ...")
        # Comment.objects.bulk_create(comment_list)
