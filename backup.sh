# 백업을 저장할 디렉토리 경로
BACKUP_DIR=/usr/src/app/db

# 현재 날짜를 백업 파일 이름으로 사용
BACKUP_FILE="$BACKUP_DIR/db_backup_$(date +'%Y%m%d').sql.gz"

# Docker 컨테이너에서 PostgreSQL 백업 실행
docker exec db pg_dump -U poko_db_user_prod -d poko_db_prod | gzip > $BACKUP_FILE