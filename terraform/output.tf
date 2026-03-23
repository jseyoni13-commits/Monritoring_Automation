output "ec2_instance_id"{
    value = aws_instance.demo_ec2.id
}

output "sns_topic_arn" {
  value = aws_sns_topic.alert.arn
}

