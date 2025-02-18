provider "aws" {
  region = var.aws_region
}

# Zufällige ID für den S3-Bucket-Namen, um Kollisionen zu vermeiden
resource "random_id" "bucket_id" {
  byte_length = 4
}

# S3 Bucket für Screenshots
resource "aws_s3_bucket" "screenshot_bucket" {
  bucket = "screenshot-bucket-${random_id.bucket_id.hex}"
}

# Security Group für EC2 (öffnet Port 8000 für Flask)
resource "aws_security_group" "web_sg" {
  name_prefix = "web-sg"
  
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2-Instanz mit Python-Webserver
resource "aws_instance" "screenshot_server" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              apt update -y
              apt install -y python3 python3-pip
              pip3 install flask selenium boto3
              EOF

  tags = {
    Name = "Screenshot-Server"
  }
}

