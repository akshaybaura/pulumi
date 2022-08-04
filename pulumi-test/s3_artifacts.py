import pulumi
import pulumi_aws as aws
import pulumi_awsx as awsx

def s3_buckets(curr_account, glue_scripts_bucket, api_op_bucket):
##s3 buckets
    scripts_bucket = aws.s3.Bucket("glue_scripts",bucket=glue_scripts_bucket.format(account=curr_account),acl="private")
    scripts_bucket_public_access_block = aws.s3.BucketPublicAccessBlock("scriptsBucketPublicAccessBlock",
        bucket=scripts_bucket.id,
        block_public_acls=True,
        block_public_policy=True,
        ignore_public_acls=True,
        restrict_public_buckets=True)
    bucketObject = aws.s3.BucketObject(
        'api_integration.py',
        bucket=scripts_bucket.id,
        key='api_integration.py',
        source=pulumi.FileAsset('api_integration.py'),
        opts=pulumi.ResourceOptions(depends_on=[scripts_bucket])
    )

    api_intg_output_bucket = aws.s3.Bucket("api_intg_output",bucket=api_op_bucket.format(account=curr_account), acl="private", 
            lifecycle_rules=[aws.s3.BucketLifecycleRuleArgs(
                enabled=True,
                expiration=aws.s3.BucketLifecycleRuleExpirationArgs(days=90)
            )])
    api_intg_output_bucket_public_access_block = aws.s3.BucketPublicAccessBlock("ApiIntgOutputBucketPublicAccessBlock",
        bucket=api_intg_output_bucket.id,
        block_public_acls=True,
        block_public_policy=True,
        ignore_public_acls=True,
        restrict_public_buckets=True,
        opts=pulumi.ResourceOptions(depends_on=[api_intg_output_bucket]))
    return scripts_bucket,api_intg_output_bucket