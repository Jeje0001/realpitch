import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv

load_dotenv()

# Initialize S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

def upload_file_to_s3(file_obj, filename, content_type):
    try:
        s3.upload_fileobj(
            Fileobj=file_obj,
            Bucket=os.getenv("S3_BUCKET"),
            Key=filename,
            ExtraArgs={
                "ContentType": content_type,
                "ACL": "public-read"
            }
        )
        url = f"https://{os.getenv('S3_BUCKET')}.s3.amazonaws.com/{filename}"
        return {"success": True, "url": url}
    except (BotoCoreError, ClientError) as e:
        print("Upload failed:", e)
        return {"success": False, "error": str(e)}
