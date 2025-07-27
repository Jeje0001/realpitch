from config.s3_config import s3

def test_connection():
    try:
        response = s3.list_buckets()
        print("✅ S3 connection successful. Buckets:")
        for bucket in response['Buckets']:
            print("-", bucket['Name'])
    except Exception as e:
        print("❌ S3 connection failed:", str(e))

test_connection()
