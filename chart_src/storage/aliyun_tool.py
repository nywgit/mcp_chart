import uuid
from datetime import timedelta
import alibabacloud_oss_v2 as oss
from dotenv import load_dotenv


class AliYunTool:
    def __init__(self, region, bucket_name, prefix: str):
        # 从环境变量加载密钥
        load_dotenv()
        credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
        # 使用SDK的默认配置
        cfg = oss.config.load_default()
        cfg.credentials_provider = credentials_provider
        cfg.region = region
        self.client = oss.Client(cfg)
        self.bucket_name = bucket_name
        self.prefix = prefix

    def upload_from_memory(self, image_bytes: bytes, expires: int = 3600):
        """
        上传图片到阿里云OSS，并返回带下载 token 的私有 URL（适用于私有空间）
        :param image_bytes: 图像字节数据
        :param expires: 下载链接有效期（秒），默认 1 小时
        :return: 带 token 的可访问 URL
        """
        # 上传内存中的图片到七牛云，使用 UUID 避免冲
        key = f"{self.prefix.strip('/')}/{uuid.uuid4().hex}.png"

        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=image_bytes,
        ))
        # 生成预签名的GET请求
        pre_result = self.client.presign(
            oss.GetObjectRequest(
                bucket=self.bucket_name,  # 指定存储空间名称
                key=key,  # 指定对象键名
                response_content_disposition="attachment",  # 设置为强制下载
            ),
            expires=timedelta(seconds=expires),
        )
        print(f'pre_result: {pre_result.url}')
        return pre_result.url