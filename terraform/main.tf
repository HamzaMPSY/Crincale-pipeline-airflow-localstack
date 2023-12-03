# Specify the GCP Provider
provider "google" {
  project = var.project_id
  region  = var.region
}

# Create a GCS Bucket
resource "google_storage_bucket" "my_bucket" {
  name     = var.bucket_name
  location = var.region
}

resource "google_bigquery_dataset" "my_dataset" {
  dataset_id    = var.dataset_id
  friendly_name = var.friendly_name
}
