resource "google_storage_bucket" "datalake" {
  name = "chess-application-datalake"
  location = "US"
}

resource "google_storage_bucket" "artifacts" {
  name = "chess-application-artifacts"
  location = "US"
}
