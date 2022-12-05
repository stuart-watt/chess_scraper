data "archive_file" "source" {
    type        = "zip"
    source_dir  = "../src/scraper"
    output_path = "/tmp/scraper.zip"
}

resource "google_storage_bucket_object" "function_archive" {
  content_type = "application/zip"
  bucket = google_storage_bucket.artifacts.name
  source = data.archive_file.source.output_path

  name   = "scraper-${data.archive_file.source.output_md5}.zip"
}


resource "google_cloudfunctions_function" "chess_scraper" {
  name        = "chess-scraper"
  description = "Scrapes game data from chess.com and saves to GCS"
  runtime     = "python39"

  
  source_archive_bucket = google_storage_bucket.artifacts.name
  source_archive_object = google_storage_bucket_object.function_archive.name

  timeout               = 120
  available_memory_mb   = 1024
  max_instances         = 1

  entry_point           = "main"

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.daily.id
    failure_policy {
      retry = false
    }
  }

  environment_variables = {
    USERNAME        = "samwise_gambit"
    DATALAKE_BUCKET = google_storage_bucket.datalake.name
  }

}