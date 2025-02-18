variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

variable "ami_id" {
  description = "Amazon Linux 2 AMI ID"
  type        = string
  default     = "ami-053a45fff0a704a47"  # Aktualisieren für deine Region
}

variable "instance_type" {
  description = "EC2 Instanz-Typ"
  type        = string
  default     = "t2.micro"
}

variable "key_name" {
  description = "SSH Key Name"
  type        = string
  default     = "ScreenshotGeneratorKey" 
}

