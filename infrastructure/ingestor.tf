data "archive_file" "ingestor_source" {
    type        = "zip"
    source_dir  = "../src/services/ingestor"
    output_path = "/tmp/ingestor.zip"
}

resource "google_storage_bucket_object" "ingestor_archive" {
  content_type = "application/zip"
  bucket = google_storage_bucket.artifacts.name
  source = data.archive_file.ingestor_source.output_path

  name   = "ingestor-${data.archive_file.ingestor_source.output_md5}.zip"
}

resource "google_cloudfunctions_function" "chess_ingestor" {
  name        = "chess-ingestor"
  description = "Ingests game data from chess.com and saves to GCS"
  runtime     = "python39"

  
  source_archive_bucket = google_storage_bucket.artifacts.name
  source_archive_object = google_storage_bucket_object.ingestor_archive.name

  timeout               = 540
  available_memory_mb   = 1024
  max_instances         = 1

  entry_point           = "main"

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.scraper.id
    failure_policy {
      retry = false
    }
  }

  environment_variables = {
    DATALAKE_BUCKET = google_storage_bucket.datalake.name
  }
}
