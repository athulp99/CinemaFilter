import { getEnv } from "../config/env.js";
import { extractOdeonShowtimes } from "../cinemas/odeon/extractShowtimes.js";
import { fetchOdeonListings } from "../cinemas/odeon/fetchListings.js";

export async function scrapeCinemaListings({ cinema, location }) {
  const env = getEnv();

  if (cinema !== "odeon") {
    throw new Error(`Unsupported cinema: ${cinema}`);
  }

  const rawSource = await fetchOdeonListings({ location });
  const listings = extractOdeonShowtimes({
    location,
    rawSource,
    hasOpenAiKey: Boolean(env.openAiApiKey)
  });

  return {
    cinema,
    location,
    listingCount: listings.length,
    listings
  };
}

