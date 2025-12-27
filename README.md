# 图表生成工具 (Chart Generator Tool)
[English](README_en.md)
## 简介

这是一个基于 Python 的图表生成工具，支持生成折线图、柱状图和饼状图。
该工具使用 matplotlib 作为图表渲染引擎，并集成了对象存储功能，可以将生成的图表上传到云端，返回给AI一个URL或Base64格式的数据。

默认使用 Streamable 传输。

## 功能特性

- **多种图表类型**：支持折线图、柱状图和饼状图
- **MCP 接口**：提供标准 MCP 接口供外部调用
- **存储选项**：支持上传到MinIo（同时支持七牛云OSS和阿里云OSS）或返回 Base64 编码


## 安装与配置

### 环境要求

- Python 3.7+
- matplotlib
- pandas
- numpy
- python-dotenv
- fastmcp
- minio (MinIO SDK)
- alibabacloud_oss_v2 ( 阿里云 SDK)
- qiniu (七牛云 SDK )

安装依赖：
```
pip install -r requirements.txt
```

### 配置OSS（可选）

如果未配置OSS或不可用，会自动输出Base64数据，以确保兼容性。

`.env` 文件并配置OSS相关信息：

```env
OSS_TYPE=aliyun minio qiniu

# MinIo 或 七牛云
DOMAIN=域名
BUCKET_NAME=桶名称
ACCESS_KEY=公钥
SECRET_KEY=私钥

# 阿里云
REGION=阿里云服务器地域ID（[从这里查看服务器区域对应的地域ID](https://help.aliyun.com/zh/oss/user-guide/regions-and-endpoints)）
OSS_ACCESS_KEY_ID=阿里云公钥
OSS_ACCESS_KEY_SECRET=阿里云私钥

#文件路径
PREFIX=
```


## 使用方法

### 启动服务

```bash
python main.py --host 0.0.0.0 --port 8000
```
