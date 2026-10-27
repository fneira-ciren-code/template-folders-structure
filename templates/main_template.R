#' @title main.R
#' @author Fernando Neira-Roman
#' @description Thin orchestrator: loads config and functions, runs the
#'   pipeline. Run from the project root.
#' @section main: No functions defined here; all logic lives in
#'   src/functions/.

library(purrr)
library(readr)
library(yaml)

# Config -----------------------------------------------------------------------
# Single read of config/config.yml (SSOT, read-only). When another script needs
# it (for example a report in src/reports/), copy templates/load_config.R to
# src/functions/ and call load_config(). Keys are read as CONFIG$PATH_DATA_RAW,
# CONFIG$PATH_OUTPUTS_TABLES, and so on.
if (!file.exists("config/config.yml")) {
  stop("Run from the project root: config/config.yml not found.")
}

CONFIG <- yaml::read_yaml("config/config.yml")
if (file.exists(".env")) {
  readRenviron(".env")
}

# Load functions ---------------------------------------------------------------
# Sources every file in src/functions/. Each file defines one function with
# the same name, so `src/functions/function_name.R` -> `function_name()`.
list.files("src/functions", pattern = "\\.R$", full.names = TRUE) |>
  purrr::walk(source)

# Input (I/O at the edge) ------------------------------------------------------
input_files <- list.files(
  CONFIG$PATH_DATA_RAW,
  pattern = "\\.csv$",
  full.names = TRUE
)
stopifnot(length(input_files) > 0)

raw_list <- purrr::map(input_files, readr::read_csv)

# Call functions ---------------------------------------------------------------
# 1. Single call
result <- function_name(raw_list[[1]])

# 2. Vectorised call over many inputs (one result per input file)
result_list <- purrr::map(raw_list, function_name)

# Alternative call patterns (not executed; copy out as needed) -----------------
if (FALSE) {
  # 3. Call with extra arguments (anonymous function fixes the extra ones)
  result_list <- purrr::map(raw_list, \(x) function_name(x, k = 3))

  # 4. Chaining several functions, one step per line
  result <- raw_list[[1]] |>
    clean_data() |>
    function_name()
}

# Output (I/O at the edge) -----------------------------------------------------
output_files <- file.path(
  CONFIG$PATH_OUTPUTS_TABLES,
  basename(input_files)
)
purrr::walk2(result_list, output_files, readr::write_csv)
