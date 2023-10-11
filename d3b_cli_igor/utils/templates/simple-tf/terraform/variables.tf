#Variables goes here
variable "environment" {
    description = "Environment name"
    default="{{ environment }}"
}

variable "region" {
    description = "AWS Region"
    default="{{ region }}"
}

variable "image_tag" {
    description = "Docker Image Tag in ECR"
}

variable "project" {
    description = "{{ project }}"
}
