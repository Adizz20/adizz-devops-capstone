variable "aws_region" {
  description = "AWS region for the EKS cluster."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Prefix used for AWS resource names and tags."
  type        = string
  default     = "adizz"
}

variable "cluster_name" {
  description = "EKS cluster name."
  type        = string
  default     = "adizz-eks"
}

variable "vpc_cidr" {
  description = "CIDR range for the EKS VPC."
  type        = string
  default     = "10.20.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDR ranges for the two public subnets."
  type        = list(string)
  default     = ["10.20.1.0/24", "10.20.2.0/24"]

  validation {
    condition     = length(var.public_subnet_cidrs) >= 2
    error_message = "At least two public subnet CIDRs are required for EKS."
  }
}

variable "kubernetes_version" {
  description = "Kubernetes version for EKS."
  type        = string
  default     = "1.35"
}

variable "node_instance_types" {
  description = "EC2 instance types for the managed node group."
  type        = list(string)
  default     = ["t3.small"]
}

variable "node_desired_size" {
  description = "Desired number of managed worker nodes."
  type        = number
  default     = 2
}

variable "node_min_size" {
  description = "Minimum number of managed worker nodes."
  type        = number
  default     = 1
}

variable "node_max_size" {
  description = "Maximum number of managed worker nodes."
  type        = number
  default     = 3
}
