resource "google_artifact_registry_repository" "scraper" {
  repository_id = "chess-scraper"
  description   = "Houses the chess scraper package"

  format = "python"

  project  = var.project_id
  location = var.region
}