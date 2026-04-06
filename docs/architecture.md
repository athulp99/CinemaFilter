# Architecture

## Goal

CinemaFilter is being shaped as a small ingestion pipeline:

1. Fetch raw cinema page content
2. Extract movie names and showtimes
3. Normalize the data
4. Return or store a consistent result format

## Design choices in this first branch

- `src/cinemas/` keeps each cinema chain isolated from the others
- `src/core/` coordinates the overall scraping workflow
- `src/services/openai/` isolates GPT-specific logic so it does not leak into every module
- `src/shared/` holds reusable data cleanup helpers
- `src/config/` centralizes environment handling

## Why this helps future pull requests

This layout makes it easier to keep PRs small and focused:

- one PR can add a new cinema adapter
- one PR can improve prompt design
- one PR can add storage
- one PR can expose an API without changing scraper internals

## Near-term roadmap

- Replace placeholder fetch logic with real HTTP requests
- Add HTML parsing for a single Odeon page
- Introduce tests around extraction and normalization
- Save results to a local JSON file or lightweight database

