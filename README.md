# Crincale pipeline with Airflow and GCP
Pipeline that extracts data from Crinacle's Headphone and InEarMonitor databases, inject it in BigQuery, transform it using DBT then the dashboard will be created using Metabase Dashboard. 

# Dev Steps
1. Write the scaper script and run in Airflow
2. [Install Terraform](#install-terraform) and we write a project theat will create the google cloud architecture 
3. Create the airflow connection to gcp based on this [link](https://junjiejiang94.medium.com/get-started-with-airflow-google-cloud-platform-docker-a21c46e0f797) 
4. Create a task that will upload the bronze files to gcs
5. Sanitize data with pydantic and the upload the silver files to gcs
6. Create the BigQuery Dataset using Terraform
7. Use GCSToBigQueryOperator airflow operator to inject data from GCS to BigQuery Tables
8. Install DBT and connect it to GCP locally and then write, run and test all the transformation
9. [Use Astronomer Cosmos](https://astronomer.github.io/astronomer-cosmos/getting_started/index.html) to run DBT seamlessly on airflow and translate all the nodes(dbt models and tests) to airlfow tasks
10. Work with Metabase and connect it to BigQuery and then create the Questions and the final Dashboard as showed in the image.

# Creating the Google Cloud architecture (IAC)
We will use terraform to create the GCS bucket and the BigQuery Dataset in the Google Cloud Platform, here you will find the instructions to install Terraform and gcloud sdk.
After installing gcloud, you have to connect to your google account and after that connect to terraform using gcloud.
## 1- Install Terraform
```console
$ wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
$ echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
$ sudo apt update && sudo apt install terraform
```

## 2- Install gcloud sdk

```console
$ curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-450.0.0-linux-x86_64.tar.gz
$ tar -xf google-cloud-cli-450.0.0-linux-x86_64.tar.gz
$  ./google-cloud-sdk/install.sh
$ gcloud auth application-default login --project [your project id]
```

# How to run the project i will mention it later
1. After cloning the project, make sure to create an .env file based on the .env.example file and fill the variables with the corresponding values.
2. execute the following command to create the env variables in your system
```console
$ source .env
```
3.download the keyfile.json and put in folder named gcp in your home folder "make sure to replace all of my home folder occurrence in the docker-compose.yaml file with your home folder"

4. run 

```console
$ sudo docker compose up
```

don't forget to talk about the keyfile.json and how you link it in volume