# Chart Generator Tool
[中文](README.md)

## Introduction

This is a Python-based chart generation tool that supports generating line charts, bar charts, and pie charts. The tool uses matplotlib as the chart rendering engine and integrates MinIO object storage functionality (supporting Qiniu Cloud OSS and Alibaba Cloud OSS simultaneously), which can upload generated charts to the cloud and return a URL or Base64 format data to AI.

By default, Streamable transmission is used.

## Features

- **Multiple Chart Types**: Supports line charts, bar charts, and pie charts
- **MCP Interface**: Provides standard MCP interface for external calls
- **Storage Options**: Supports uploading to MinIO (with simultaneous support for Qiniu Cloud OSS and Alibaba Cloud OSS) or returning Base64 encoding

## Installation and Configuration

### Requirements

- Python 3.7+
- matplotlib
- pandas
- numpy
- python-dotenv
- fastmcp
- minio (MinIO SDK)
- alibabacloud_oss_v2 (Alibaba Cloud SDK)
- qiniu (Qiniu Cloud SDK)

Install dependencies:
```
pip install -r requirements.txt
```


### Configure OSS (Optional)

If OSS is not configured or unavailable, Base64 data will be automatically output to ensure compatibility.

Create a `.env` file and configure OSS related information:


```env
OSS_TYPE=aliyun minio qiniu

# MinIO or Qiniu OSS
DOMAIN=domain
BUCKET_NAME=bucket name
ACCESS_KEY=public key
SECRET_KEY=private key

# Alibaba Cloud
REGION=Alibaba Cloud region ID ([view the region ID corresponding to the server region here](https://help.aliyun.com/zh/oss/user-guide/regions-and-endpoints))
OSS_ACCESS_KEY_ID=Alibaba Cloud public key
OSS_ACCESS_KEY_SECRET=Alibaba Cloud private key

# File path
PREFIX=

```


## Usage

### Start the Service

```bash
python main.py --host 0.0.0.0 --port 8000
```
