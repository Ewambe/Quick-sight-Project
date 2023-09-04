resource "aws_s3_bucket" "source_bucket" {
  bucket = "bucket" # Replace with your desired source bucket name
}

resource "aws_s3_bucket" "destination_bucket" {
  bucket = "bucket" # Replace with your desired destination bucket name
}