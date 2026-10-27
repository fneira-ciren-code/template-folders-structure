#' @title load_config.R
#' @author Fernando Neira-Roman
#' @description Reads the project configuration file. Example of the function
#'   to extract from the orchestrator when more than one script needs it.
#' @section load_config: Checks that the file exists and returns its content.

#' Load the project configuration
#'
#' @param path Path to the YAML config file, relative to the project root.
#' @return Named list with the config keys (SCREAMING_SNAKE_CASE).
load_config <- function(path = "config/config.yml") {
  if (!file.exists(path)) {
    stop("Run from the project root: ", path, " not found.")
  }

  config <- yaml::read_yaml(path)

  return(config)
}
