import requests
import boto3
import sys
from awsglue.utils import getResolvedOptions

args = getResolvedOptions(sys.argv, ['avail_zone','output_bucket'])

s3_client=boto3.client('s3',region_name=args['avail_zone'])
data = requests.get('http://universities.hipolabs.com/search?country=India').json()

s3_client.put_object(Body=str(data), Bucket=args['output_bucket'], Key='api_Data.txt')
