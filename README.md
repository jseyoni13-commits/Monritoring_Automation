# Platform Monitoring and Automated Remediation

## Overview

This project demonstrates a monitoring and automated remediation workflow for detecting and responding to slow API responses in a web application.

The system monitors application logs using **Sumo Logic**. When slow responses are detected for the `/api/data` endpoint, an automated remediation workflow is triggered using **AWS Lambda**, which restarts the affected EC2 instance and sends a notification via **Amazon SNS**.

The infrastructure for the remediation components is defined using **Terraform**, enabling reproducible and automated deployment.

---

# Architecture
Application Logs
↓
Sumo Logic Monitoring
↓
Alert Condition
↓
AWS Lambda Automation
↓
EC2 Instance Reboot
↓
SNS Notification (Email)


---

# Project Structure
monitoring/
│
├── lambda_function/
│ └── lambda_function.py
│
├── terraform/
│ ├── main.tf
│ ├── ec2.tf
│ ├── iam.tf
│ ├── lambda.tf
│ ├── sns.tf
│ └── outputs.tf
│
├── sumo_logic_query.txt
├── README.md
└── recordings/


---

# Part 1 — Sumo Logic Monitoring

## Objective

Detect slow API responses for the endpoint:

/api/data


Alert if:

- response time > **3 seconds**
- more than **5 occurrences**
- within a **10 minute window**

---

## Sumo Logic Query
_sourceCategory=prod/webapp
| json field=_raw "path", "response_time_ms", "instance_id"
| where path = "/api/data" and response_time_ms > 3000
| timeslice 10m
| count as slow_request_count by _timeslice, instance_id
| where slow_request_count > 5
| fields _timeslice, instance_id, slow_request_count


---

## Query Explanation

| Step | Purpose |
|-----|------|
Filter logs | `_sourceCategory=prod/webapp`
Parse JSON fields | Extract `path`, `response_time_ms`, `instance_id`
Filter endpoint | Only `/api/data`
Latency threshold | Response time > 3000 ms
Time window | Group logs into 10 minute slices
Count events | Count slow requests
Alert condition | Trigger if count > 5

---

## Alert Configuration

Scheduled Search settings:

| Setting | Value |
|------|------|
Search Name | `api-data-slow-response-alert`
Run Frequency | Every 15 minutes
Time Range | Last 15 minutes
Trigger Condition | If results > 0
Notification | Email

Note: The Sumo Logic free environment enforces a minimum 15 minute schedule interval.

---

# Part 2 — AWS Lambda Automated Remediation

## Objective

When the alert condition is met, an automated remediation process should:

1. Restart the affected EC2 instance
2. Log the action in CloudWatch
3. Send a notification to operations via SNS

---

## Lambda Implementation

The Lambda function is implemented in Python using the AWS SDK (`boto3`).

Responsibilities:

- reboot EC2 instance
- send SNS notification
- log execution events

---

## Lambda Code

Located in:
lambda_function/lambda_function.py


Main logic:
Retrieve EC2 instance ID from environment variables

Call EC2 reboot API

Publish message to SNS topic

Log actions for auditability


---

## Environment Variables

| Variable | Purpose |
|------|------|
EC2_INSTANCE_ID | Target instance to restart |
SNS_TOPIC_ARN | Notification topic |

---

## Testing the Function

The Lambda function can be tested using the AWS console with a simple test event:
{}


Expected outcome:

- EC2 instance reboot initiated
- SNS notification email received
- CloudWatch logs created

---

# Part 3 — Terraform Infrastructure

Terraform is used to provision the infrastructure required for the remediation workflow.

---

## Resources Provisioned

Terraform creates the following AWS resources:

| Resource | Purpose |
|------|------|
EC2 Instance | Target instance for remediation |
SNS Topic | Notification system |
Lambda Function | Automation logic |
IAM Role | Permissions for Lambda |
SNS Subscription | Email notification |

---

## Terraform Files

| File | Purpose |
|------|------|
main.tf | AWS provider configuration |
ec2.tf | EC2 instance |
sns.tf | SNS topic and subscription |
iam.tf | Lambda execution role and policies |
lambda.tf | Lambda deployment |
outputs.tf | Output values |

---

## Terraform Deployment

Initialize Terraform:
terraform init


Review deployment plan:
terraform plan


Apply infrastructure:
terraform apply


Destroy resources after testing:
terraform destroy


---

# Security Considerations

The Lambda execution role follows the principle of **least privilege**, allowing only the required actions:

- `ec2:RebootInstances`
- `sns:Publish`
- CloudWatch logging

---

# Future Improvements

Possible enhancements for production environments:

- integrate Sumo Logic alerts directly with Lambda via webhook
- add remediation cooldown logic
- implement EC2 health checks before reboot
- integrate with incident management systems
- use Auto Scaling instead of instance reboot

---

# Summary

This solution demonstrates a monitoring-driven remediation workflow combining:

- Observability (Sumo Logic)
- Automation (AWS Lambda)
- Infrastructure as Code (Terraform)

The system automatically detects slow API responses and triggers corrective actions to restore service health while notifying operations teams.