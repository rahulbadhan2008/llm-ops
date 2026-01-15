# DynamoDB for Short-term Memory
resource "aws_dynamodb_table" "history" {
  name           = "UserChatHistory"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "UserId"
  range_key      = "Timestamp"

  attribute {
    name = "UserId"
    type = "S"
  }

  attribute {
    name = "Timestamp"
    type = "S"
  }

  ttl {
    attribute_name = "TTL"
    enabled        = true
  }
}

# S3 for Long-term Memory
resource "aws_s3_bucket" "long_term" {
  bucket = "${var.project_name}-long-term-memory"
}

# Elasticache for Redis (Temp Memory)
resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "${var.project_name}-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                = 6379
}

# Amazon OpenSearch (Managed)
resource "aws_opensearch_domain" "main" {
  domain_name    = "${var.project_name}-os"
  engine_version = "OpenSearch_2.11"

  cluster_config {
    instance_type = "t3.small.search"
  }

  ebs_options {
    ebs_enabled = true
    volume_size = 10
  }
}
