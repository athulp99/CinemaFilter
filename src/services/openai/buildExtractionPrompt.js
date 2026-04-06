export function buildExtractionPrompt({ cinema, location, rawText }) {
  return [
    `You are extracting cinema listings for ${cinema}.`,
    `Location: ${location}.`,
    "Return a clean JSON array of movies and showtimes.",
    "Preserve title spelling as shown unless normalization is required separately.",
    "",
    rawText
  ].join("\n");
}

