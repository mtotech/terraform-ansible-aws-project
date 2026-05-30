resource "aws_db_subnet_group" "default" {
  name = "main-subnet-group"

  subnet_ids = aws_subnet.public[*].id
}

resource "aws_db_instance" "mysql" {
  allocated_storage      = 20
  engine                 = "mysql"
  engine_version         = "8.0"
  instance_class         = "db.t3.micro"

  username               = "admin"
  password               = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.default.name
  skip_final_snapshot    = true
  publicly_accessible    = false

  tags = {
    Name = "prod-mysql"
  }
}
