# Crincale pipeline with Airflow and GCP
Pipeline that extracts data from Crinacle's Headphone and InEarMonitor databases and finalizes data for a Metabase Dashboard. 

# Dev Steps
1. Write the scaper script and run in Airflow
2. [Install Terraform](#install-terraform) and we write a project theat will create the google cloud architecture 
3. Create the airflow connection to gcp based on this [link](https://junjiejiang94.medium.com/get-started-with-airflow-google-cloud-platform-docker-a21c46e0f797) 
4. Create a task that will upload the bronze files to gcs

# Install Terraform
`
$ wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
$ echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
$ sudo apt update && sudo apt install terraform
`

# Install gcloud sdk

`
$ curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-450.0.0-linux-x86_64.tar.gz
$ tar -xf google-cloud-cli-450.0.0-linux-x86_64.tar.gz
$  ./google-cloud-sdk/install.sh
$ gcloud auth application-default login --project [your project id]
`

# How to run the project i will mention it later