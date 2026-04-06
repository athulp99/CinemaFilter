# CinemaFilter

CinemaFilter is an early-stage project for collecting cinema listings from the web and turning them into structured movie showtime data.

The first target is `Odeon`, but the codebase is now arranged so we can add more cinema chains later without rewriting the whole app.

## Current focus

This branch sets up the project structure for:

- cinema-specific scraping modules
- GPT-assisted extraction helpers
- shared normalization utilities
- a small orchestration layer that can later become an API or scheduled job

## Project structure

```text
CinemaFilter/
├── docs/
│   └── architecture.md
├── src/
│   ├── cinemas/
│   │   └── odeon/
│   │       ├── extractShowtimes.js
│   │       └── fetchListings.js
│   ├── config/
│   │   └── env.js
│   ├── core/
│   │   └── scrapeCinemaListings.js
│   ├── services/
│   │   └── openai/
│   │       └── buildExtractionPrompt.js
│   ├── shared/
│   │   └── normalizeMovie.js
│   └── index.js
├── .env.example
├── .gitignore
├── package.json
└── README.md
```

## How the flow works

1. `src/index.js` starts a scrape run.
2. `src/core/scrapeCinemaListings.js` chooses the cinema adapter.
3. `src/cinemas/odeon/fetchListings.js` is where raw page fetching will live.
4. `src/cinemas/odeon/extractShowtimes.js` converts raw content into structured showtime entries.
5. `src/services/openai/buildExtractionPrompt.js` prepares the prompt shape for GPT-based extraction when needed.
6. `src/shared/normalizeMovie.js` keeps movie titles consistent across sources.

## Run locally

Install dependencies:

```bash
npm install
```

Run the starter flow:

```bash
npm start
```

## Environment

Copy `.env.example` to `.env` when you are ready to add real credentials.

## What this starter does today

This is still a simple first step. It does not scrape Odeon live yet.

Instead, it gives you a clean structure and a small working pipeline with placeholder data so future PRs can focus on one concern at a time:

- real page fetching
- GPT extraction
- data storage
- APIs
- scheduling

## Suggested next PRs

- Implement a real Odeon fetcher
- Add HTML parsing for a single cinema page
- Wire in the OpenAI API for extraction fallback
- Save normalized listings as JSON

