resource "google_pubsub_topic" "daily" {
  name = "daily"
}

resource "google_cloud_scheduler_job" "daily" {
  name     = "daily"
  schedule = "0 0 * * *"
  region   = var.region

  pubsub_target {
    topic_name = google_pubsub_topic.daily.id
    attributes = {
      "frequency" = "daily"
    }
  }
}