import os
import uuid
from typing import BinaryIO, Union
from io import BytesIO
from minio import Minio
from datetime import timedelta
import magic


class MinioTool:
    def __init__(self, endpoint, bucket_name, access_key, secret_key, prefix: str):
        self.client = Minio(endpoint, access_key, secret_key, secure=False)
        self.bucket_name = bucket_name
        self.prefix = prefix

    def _detect_content_type(self, data: bytes) -> str:
        """
        根据字节数据检测 MIME 类型
        """
        mime = magic.Magic(mime=True)
        content_type = mime.from_buffer(data[:2048])  # 只需前 2KB 足够识别

        # 可选：兜底策略（如果 magic 返回 application/octet-stream，可尝试根据常见图片头手动修正）
        if content_type == "application/octet-stream":
            # 简单魔数检测（增强鲁棒性）
            if data.startswith(b"\xff\xd8\xff"):
                content_type = "image/jpeg"
            elif data.startswith(b"\x89PNG\r\n\x1a\n"):
                content_type = "image/png"
            elif data.startswith(b"GIF87a") or data.startswith(b"GIF89a"):
                content_type = "image/gif"
        print("content_type:", content_type)
        return content_type

    def upload_from_memory(self, image_bytes: Union[bytes, BinaryIO], expires: int = 3600) -> str:
        key = f"{self.prefix.strip('/')}/{uuid.uuid4().hex}.png"
        print("key:", key)

        # 统一转换为 bytes 和 stream
        if isinstance(image_bytes, bytes):
            raw_data = image_bytes
            length = len(raw_data)
            image_stream = BytesIO(raw_data)
        else:
            image_bytes.seek(0)
            raw_data = image_bytes.read()
            length = len(raw_data)
            image_stream = BytesIO(raw_data)
            image_stream.seek(0)  # 重置指针

        # 自动检测 Content-Type
        content_type = self._detect_content_type(raw_data)

        # 上传到 MinIO，显式设置 content_type
        self.client.put_object(
            self.bucket_name,
            key,
            image_stream,
            length=length,
            part_size=10 * 1024 * 1024,
            content_type=content_type  # <-- 关键：传入 content_type
        )

        private_url = self.client.presigned_get_object(
            self.bucket_name,
            key,
            expires=timedelta(seconds=expires)
        )
        return private_url