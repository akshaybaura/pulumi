import pulumi
import pulumi_aws as aws
import pulumi_awsx as awsx
import vpc_artifacts
import glue_artifacts
import s3_artifacts

aws_config = pulumi.Config('aws')
region = aws_config.require('region')

config = pulumi.Config()
glue_scripts_bucket = config.require('glue_scripts_bucket')
api_op_bucket = config.require('api_op_bucket')
currentID = aws.get_caller_identity()
curr_account = currentID.account_id


vpc = vpc_artifacts.vpc()

network_connection = glue_artifacts.glue_connection(vpc)
                
scripts_bucket,api_intg_output_bucket = s3_artifacts.s3_buckets(curr_account, glue_scripts_bucket, api_op_bucket)

glue_artifacts.glue_job(region, scripts_bucket, api_intg_output_bucket, network_connection)