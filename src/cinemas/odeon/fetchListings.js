export async function fetchOdeonListings({ location }) {
  return {
    source: "placeholder",
    cinema: "odeon",
    location,
    fetchedAt: new Date().toISOString(),
    rawText: `
      ODEON Demo Cinema - ${location}
      Dune: Part Two - 18:00, 21:10
      Challengers - 17:30, 20:15
      Spirited Away - 14:00
    `.trim()
  };
}

