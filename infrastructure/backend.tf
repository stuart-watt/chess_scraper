terraform {
 backend "gcs" {
   bucket  = "my-terraform-stacks"
   prefix  = "chess_scraper"
 }
}