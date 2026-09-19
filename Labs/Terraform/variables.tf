variable "credentials" {
  description = "My Credentials"
  default     = "/Users/vikram/Projects/Learning/DataEngineering-zc/Labs/Terraform/Keys/gcp-tf-key.json"
}

variable "project" {
  description = "Project"
  default     = "terraform-docker-508716"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "demo_dataset"
}

variable "region" {
  description = "Region of Provider"
  default     = "us-east1"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "terraform-docker-508716-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}
