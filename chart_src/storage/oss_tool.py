import os
from dotenv import load_dotenv
from chart_src.storage import QiniuTool
from chart_src.storage import AliYunTool
from chart_src.storage import MinioTool


def get_oss_tool():
    # 获取环境变量
    load_dotenv()
    oss_type = os.getenv("OSS_TYPE", '')
    domain = os.getenv("DOMAIN", '')
    bucket_name = os.getenv("BUCKET_NAME", '')
    access_key = os.getenv("ACCESS_KEY", '')
    secret_key = os.getenv("SECRET_KEY", '')

    region = os.getenv("REGION", '')
    prefix = os.getenv("PREFIX", '')

    if oss_type == '':
        return None

    storage_tool = None
    # 对象存储工具
    if oss_type == 'minio':
        return  MinioTool(domain, bucket_name, access_key, secret_key, prefix)
    if oss_type == 'aliyun':
        return AliYunTool(region, bucket_name, prefix)
    else:
        return QiniuTool(domain, bucket_name, access_key, secret_key, prefix)
