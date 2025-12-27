import uuid
import qiniu
from dotenv import load_dotenv

class QiniuTool:
    def __init__(self, domain, bucket_name, access_key, secret_key, prefix: str = "charts"):
        """
        :param domain: 七牛云域名
        :param bucket_name: 空间名称
        :param access_key: 公钥
        :param secret_key: 私钥
        :param prefix: 文件路径 如 'charts/line'
        """
        load_dotenv()
        self.domain = domain
        self.bucket_name = bucket_name
        self.access_key = access_key
        self.secret_key = secret_key
        self.prefix = prefix
        self.qiniu_auth = qiniu.Auth(access_key, secret_key)


    def upload_from_memory(self, image_bytes: bytes, expires: int = 3600) -> str:
        """
        上传图片到七牛云，并返回带下载 token 的私有 URL（适用于私有空间）
        :param image_bytes: 图像字节数据
        :param expires: 下载链接有效期（秒），默认 1 小时
        :return: 带 token 的可访问 URL
        """

        # 上传内存中的图片到七牛云，使用 UUID 避免冲
        key = f"{self.prefix.strip('/')}/{uuid.uuid4().hex}.png"

        # 1. 上传文件
        token = self.qiniu_auth.upload_token(self.bucket_name, key, expires)
        ret, info = qiniu.put_data(token, key, image_bytes)
        if info.status_code != 200:
            raise Exception(f"上传失败: {info}")

        # 2. 生成私有下载 URL（自动带 token）
        base_url = f"{self.domain}/{ret['key']}"
        private_url = self.qiniu_auth.private_download_url(base_url, expires=expires)

        return private_url
