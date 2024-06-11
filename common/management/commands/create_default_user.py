from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import CustomUser


class Command(BaseCommand):
    help = "Create users automatically"

    def add_arguments(self, parser):
        parser.add_argument("user_count", type=int, help="Number of users to create")

    def handle(self, *args, **options):
        user_count = options["user_count"]
        for i in range(1, user_count + 1):
            if i <= 9:
                username = f"poko0{i}"
            else:
                username = f"poko{i}"
            password = "poko0000!"  # 패스워드 설정
            email = f"{username}@example.com"
            # 사용자 생성
            user = CustomUser.objects.create_user(
                username=username, email=email, password=password
            )
            self.stdout.write(self.style.SUCCESS(f"사용자 {username}가 생성되었습니다."))
