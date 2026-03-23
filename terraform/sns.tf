resource "aws_sns_topic" "alert" {
    name = "platform-monitoring-alerts"
}

resource "aws_sns_topic_subscription" "email_alerts" {
  topic_arn = aws_sns_topic.alert.arn
  protocol = "email"
  endpoint = "jseyoni13@gmail.com"
}