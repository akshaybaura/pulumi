import pulumi
import pulumi_aws as aws
import pulumi_awsx as awsx

def glue_connection(vpc):
##glue connection to hit api
    glue_vpc_conn = aws.glue.Connection("glue-pulumi-vpc1",name="glue-pulumi-vpc1",connection_type= "NETWORK",
        physical_connection_requirements=aws.glue.ConnectionPhysicalConnectionRequirementsArgs(
            availability_zone=aws.ec2.get_subnet(id=vpc.private_subnet_ids[0]).availability_zone,
            security_group_id_lists=[aws.ec2.get_security_group(vpc_id=vpc.vpc_id).id],
            subnet_id=vpc.private_subnet_ids[0],
        ), opts=pulumi.ResourceOptions(depends_on=[vpc]))
    return glue_vpc_conn

def glue_job(region, scripts_bucket, api_intg_output_bucket, glue_vpc_conn):
    api_integration = aws.glue.Job("api-integration-1",
        command=aws.glue.JobCommandArgs(
            name="pythonshell",
            python_version="3",
            script_location=scripts_bucket.bucket.apply(lambda bucket: f's3://{bucket}/api_integration.py'),
        ),
        connections=["glue-pulumi-vpc1"],
        default_arguments={
            "--TempDir": scripts_bucket.bucket.apply(lambda bucket:f"s3://{bucket}/temporary/"),
            "--class": "GlueApp",
            "--enable-glue-datacatalog": "true",
            "--enable-job-insights": "false",
            "--job-language": "python",
            "--prebuilt-library-option": "prebuilt-library-enable",
            "--avail_zone": region,
            "--output_bucket": api_intg_output_bucket.bucket.apply(lambda bucket:f"{bucket}")
        },
        non_overridable_arguments={
           
        },
        glue_version="1.0",
        max_capacity=0.0625,
        name="api-integration-1",
        role_arn="arn:aws:iam::797131139256:role/glue-role",#make role
        timeout=2880,
        opts=pulumi.ResourceOptions(depends_on=[glue_vpc_conn, scripts_bucket, api_intg_output_bucket]))

    return api_integration