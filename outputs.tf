output "s3_bucket_name" {
  description = "Name des S3-Buckets"
  value       = aws_s3_bucket.screenshot_bucket.id
}

output "ec2_public_ip" {
  description = "Öffentliche IP der EC2-Instanz"
  value       = aws_instance.screenshot_server.public_ip
}

