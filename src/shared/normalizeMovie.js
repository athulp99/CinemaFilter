export function normalizeMovieTitle(title) {
  return title.replace(/\s+/g, " ").trim();
}
