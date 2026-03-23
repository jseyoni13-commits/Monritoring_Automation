resource "aws_instance" "demo_ec2" {
  ami = "ami-0c02fb55956c7d316"
  instance_type = "t3.micro"

  tags = {
    Name = "platform-monitoring-demo"
  }
}