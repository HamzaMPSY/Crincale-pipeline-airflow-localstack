terraform {
  backend "gcs" {
    bucket = "my-bucket-mpsy"        # GCS bucket name to store terraform tfstate
    prefix = "crincale-pipeline-gcp" # Update to desired prefix name. Prefix name should be unique for each Terraform project having same remote state bucket.
  }
}
