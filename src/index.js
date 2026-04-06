import { scrapeCinemaListings } from "./core/scrapeCinemaListings.js";

async function main() {
  const result = await scrapeCinemaListings({
    cinema: "odeon",
    location: "London"
  });

  console.log("CinemaFilter starter run");
  console.log(JSON.stringify(result, null, 2));
}

main().catch((error) => {
  console.error("CinemaFilter failed to run.");
  console.error(error);
  process.exitCode = 1;
});

