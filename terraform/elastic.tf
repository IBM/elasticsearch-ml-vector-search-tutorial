resource "ibm_database" "esSource" {
  resource_group_id = ibm_resource_group.resource_group.id
  name              = "elastic-embeddings"
  service           = "databases-for-elasticsearch"
  plan              = "enterprise"
  # version       = "8.10"
  location      = "eu-gb"
  tags          = []
  adminpassword = var.elastic_password
}

data "ibm_database_connection" "es_connection" {
  endpoint_type = "public"
  deployment_id = ibm_database.esSource.id
  user_id       = "admin"
  user_type     = "database"
}

output "ES_URL" {
  value ="https://admin:${ibm_database.esSource.adminpassword}@${data.ibm_database_connection.es_connection.https[0].hosts[0].hostname}:${data.ibm_database_connection.es_connection.https[0].hosts[0].port}"
  sensitive = true
}