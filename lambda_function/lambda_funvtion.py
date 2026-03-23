import json
import os
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.client("ec2")
sns = boto3.client("sns")

INSTANCE_ID = os.environ.get("EC2_INSTANCE_ID")
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")

def lambda_handler(event, context):

    try:
        logger.info(f"Rebooting EC2 instance: {INSTANCE_ID}")

        ec2.reboot_instances(
            InstanceIds=[INSTANCE_ID]
        )

        message = f"EC2 instance {INSTANCE_ID} reboot initiated by monitoring automation."

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="EC2 Reboot Triggered",
            Message=message
        )

        logger.info("SNS notification sent")

        return {
            "statusCode": 200,
            "body": json.dumps(message)
        }

    except Exception as e:
        logger.error(str(e))
        raise