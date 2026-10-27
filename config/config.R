suppressPackageStartupMessages({
  library(jsonlite)
  library(dotenv)
})

dotenv::load_dot_env()

BASE_DIR <- rprojroot::find_root(rprojroot::is_git_root)
.settings <- jsonlite::fromJSON(file.path(BASE_DIR, "config", "settings.json"))

# Global Constants (SCREAMING_SNAKE_CASE)
DIR_DATA_RAW <- file.path(BASE_DIR, .settings$PATHS$DATA_RAW)
DIR_DATA_PROCESSED <- file.path(BASE_DIR, .settings$PATHS$DATA_PROCESSED)
API_SECRET_KEY <- Sys.getenv("API_SECRET_KEY", "")

list.files(full.names = TRUE, recursive = TRUE)
