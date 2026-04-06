import { buildExtractionPrompt } from "../../services/openai/buildExtractionPrompt.js";
import { normalizeMovieTitle } from "../../shared/normalizeMovie.js";

export function extractOdeonShowtimes({ location, rawSource, hasOpenAiKey }) {
  const prompt = buildExtractionPrompt({
    cinema: "odeon",
    location,
    rawText: rawSource.rawText
  });

  void prompt;

  return rawSource.rawText
    .split("\n")
    .slice(1)
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => {
      const [titlePart, timesPart] = line.split(" - ");
      const showtimes = (timesPart || "")
        .split(",")
        .map((time) => time.trim())
        .filter(Boolean);

      return {
        movieTitle: normalizeMovieTitle(titlePart),
        showtimes,
        extractionMethod: hasOpenAiKey ? "placeholder-with-openai-ready-structure" : "rule-based-placeholder"
      };
    });
}

