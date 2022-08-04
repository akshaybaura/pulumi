import pulumi
import pulumi_aws as aws
import pulumi_awsx as awsx

def vpc():
##VPC creation
    vpc = awsx.ec2.Vpc("pulumi-test",cidr_block='10.2.0.0/16',subnet_specs=[
      awsx.ec2.SubnetSpecArgs(
        type=awsx.ec2.SubnetType.PRIVATE,
        cidr_mask=26,
      ),
      awsx.ec2.SubnetSpecArgs(
        type=awsx.ec2.SubnetType.PUBLIC,
        cidr_mask=26,
      )
    ], number_of_availability_zones=1)

    return vpc

def get_subnet_sg(vpc):
  subnet = aws.ec2.get_subnet(id=vpc.private_subnet_ids[0])
  security_group = aws.ec2.get_security_group(vpc_id=vpc.vpc_id)
  return subnet, security_group