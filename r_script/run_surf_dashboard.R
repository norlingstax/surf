library(rmarkdown)
library(here)

py <- Sys.which("python")
if (py == "") stop("Python not found on PATH")

cat("Running Python data pipeline...\n")

res <- system2(
  py,
  args = c(shQuote(here("main.py"))),
  stdout = TRUE,
  stderr = TRUE
)

cat(paste(res, collapse = "\n"), "\n")

if (!is.null(attr(res, "status")) && attr(res, "status") != 0) {
  stop("Python pipeline failed. Dashboard not launched.")
}

cat("Launching dashboard...\n")

rmarkdown::run(here("r_script", "surf_dashboard.Rmd"))
