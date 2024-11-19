from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    # S3 내의 파일 저장 위치 설정
    location = 'media'
    # 동일 이름 파일 업로드 시 덮어쓰지 않음
    file_overwrite = False
