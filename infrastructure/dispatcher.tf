data "archive_file" "dispatcher_source" {
    type        = "zip"
    source_dir  = "../src/services/dispatcher"
    output_path = "/tmp/dispatcher.zip"
}

resource "google_storage_bucket_object" "dispatcher_archive" {
  content_type = "application/zip"
  bucket = google_storage_bucket.artifacts.name
  source = data.archive_file.dispatcher_source.output_path

  name   = "dispatcher-${data.archive_file.dispatcher_source.output_md5}.zip"
}


resource "google_cloudfunctions_function" "chess_dispatcher" {
  name        = "chess-dispatcher"
  description = "Scrapes game data from chess.com and saves to GCS"
  runtime     = "python39"

  
  source_archive_bucket = google_storage_bucket.artifacts.name
  source_archive_object = google_storage_bucket_object.dispatcher_archive.name

  timeout               = 540
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
    DATALAKE_BUCKET = google_storage_bucket.datalake.name
    PUBSUB_TOPIC_ID = google_pubsub_topic.scraper.id
  }
}
