variable "region" {
  default = "ap-south-1"
}

variable "env" {
  default = "prod"
}

variable "instance_type" {
  default = "t3.micro"
}

variable "key_name" {
  description = "AWS Key Pair"
}

variable "db_password" {
  sensitive = true
}
