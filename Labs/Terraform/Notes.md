Terraform is used to create/tear down/manage your infrastructure using code(Infrastructure as Code aka IaaC)

This allows your infrastructure decisions to be auditable, version controlled, and repeatable

You can install terraform on your host machine using homebrew and you can then link it to your provider by looking through documentation for boilerplate code

Once you have terraform installed, you can initialize a repository using `terraform init`


Here is an example of a GCP template from Hashicorp:

```
provider "google" {
    project = "my-project-id"
    region = "us-central1"
}

provider "google" { 
    project = "terraform-docker-508716"
    region = "us-east1" 
}
```

In GCP, you would have to create a Service account, add permissions to it from IAM, and then download the Key as a json.

The permissions we used in this lab include:
- `BigQuery Admin`
- `Storage Admin`
- `Compute Admin`

You can include the path to your json key in the .tf config file, or you could also store it under the variable `GOOGLE_CREDENTIALS` like-
```
echo GOOGLE_CREDENTIALS=#path to your key
```

Expand your .tf file to create services as you like; in this lab we created a storage bucket. Boiler plate code can be lifted from documentation.

```
resource "google_storage_bucket" "#nickname of bucket" {
  name = "#unique bucket name"
  location = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 3
    }
    action {
      type = "Delete"
    }
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}
```

To show what your terraform config does when run, you can do `terraform plan`

If that looks good, you can run `terraform apply`

This builds everything in your main.tf file and tracks it in a state file called `terraform.tfstate`

To tear it down, you can run `terraform destroy`

This collapses all of the services in your provider that were mentioned in the .tf file and it also empties the tfstate file's metadata

---

In the second part of the lab, we created a BigQuery dataset

We also created variables using a file called `variables.tf`

This file contains variables that you can reference in your .tf files. The most simple way to define a variables is as follows:

```
variable "#variable-name" {
  description = "#description"
  default     = "#default values of this variable"
}
```

You can then reference this in your .tf file as `var.#variable-name`

*One Caviat: When referencing file paths in your main.tf file, you can wrap the path or the variable containing the path with a `file(#path)`*
