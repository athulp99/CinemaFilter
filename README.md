# CinemaFilter

CinemaFilter is a small Flask app for testing MovieGlu cinema data and returning normalized JSON for one cinema flow, starting with Odeon.

The current goal is simple: send a request to your local Flask API, let it call the MovieGlu sandbox, and get JSON back that is easier to use in your app.

## Project structure

```text
CinemaFilter/
├── cinemafilter/
│   ├── app.py
│   ├── config.py
│   ├── normalizers.py
│   ├── movieglu/
│   │   └── client.py
│   └── services/
│       └── odeon.py
├── docs/
│   └── architecture.md
├── .env.example
├── .gitignore
├── requirements.txt
└── run.py
```

## What it does

- loads MovieGlu credentials from `.env`
- exposes a local Flask API
- searches MovieGlu for cinemas
- fetches showtimes for a matched Odeon cinema
- returns normalized JSON

## Setup

1. Create a virtual environment:

```bash
python3 -m venv .venv
```

2. Activate it:

```bash
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env`

```bash
cp .env.example .env
```

5. Put your sandbox credentials into `.env`

Use the MovieGlu sandbox values:

```env
MOVIEGLU_API_BASE_URL=https://api-gate2.movieglu.com/
MOVIEGLU_CLIENT=SPES
MOVIEGLU_API_KEY=your_sandbox_key
MOVIEGLU_AUTHORIZATION=Basic your_sandbox_authorization
MOVIEGLU_TERRITORY=XX
MOVIEGLU_API_VERSION=v201
MOVIEGLU_GEOLOCATION=-22.0;14.0
MOVIEGLU_CINEMA_QUERY=odeon coventry
MOVIEGLU_CINEMA_NAME_HINT=ODEON Coventry
MOVIEGLU_SHOW_DATE=2026-04-06
```

Do not commit real credentials to Git.

If you prefer, you can also use the helper targets in [`Makefile`](/Users/athulparvelikudy/Documents/Perosnal%20Docs/Projects/CinemaFilter/Makefile):

```bash
make venv
source .venv/bin/activate
make install
make run
```

## Run the Flask app

```bash
python run.py
```

The app runs on `http://127.0.0.1:5001`.

When it starts correctly, you should expect Flask to print a local development server message and show that it is serving on port `5001`.

## Endpoints

Health check:

```bash
curl http://127.0.0.1:5001/health
```

Expected result:

```json
{
  "mode": "sandbox",
  "provider": "movieglu",
  "status": "ok",
  "territory": "XX"
}
```

Search cinemas through MovieGlu:

```bash
curl "http://127.0.0.1:5001/api/movieglu/cinemas/search?query=odeon%20coventry&limit=5"
```

Expected result:

```json
{
  "query": "odeon coventry",
  "resultCount": 1,
  "cinemas": [
    {
      "cinemaId": 1234,
      "name": "ODEON Coventry",
      "city": "Coventry",
      "distance": 0
    }
  ]
}
```

The exact values will depend on MovieGlu's sandbox data.

Get a simpler sandbox response first:

```bash
curl "http://127.0.0.1:5001/api/movieglu/films/now-showing?limit=5"
```

Expected result:

```json
{
  "resultCount": 5,
  "films": [
    {
      "filmId": 100,
      "title": "Example Film"
    }
  ]
}
```

This is the best first test because it does not depend on finding a specific cinema in the sandbox dataset.

Fetch normalized Odeon now-showing data:

```bash
curl "http://127.0.0.1:5001/api/cinemas/odeon/now-showing?query=odeon%20coventry&name_hint=ODEON%20Coventry&date=2026-04-06&location=Coventry"
```

Expected result:

```json
{
  "cinema": "odeon",
  "location": "Coventry",
  "date": "2026-04-06",
  "source": "movieglu",
  "matchedCinema": {
    "id": 1234,
    "name": "ODEON Coventry",
    "city": "Coventry",
    "distance": 0
  },
  "listingCount": 2,
  "listings": [
    {
      "filmId": 111,
      "title": "Example Film",
      "ageRatings": ["12A"],
      "showtimes": [
        {
          "format": "standard",
          "startTime": "18:00",
          "endTime": "20:15"
        }
      ]
    }
  ]
}
```

Again, the exact films and times will come from the sandbox dataset.

## Direct sandbox testing

If you want to test MovieGlu without Flask first, you can call the REST API directly:

```bash
curl -X GET "https://api-gate2.movieglu.com/cinemaLiveSearch/?query=odeon%20coventry&n=5" \
  -H "client: SPES" \
  -H "x-api-key: YOUR_SANDBOX_KEY" \
  -H "authorization: Basic YOUR_SANDBOX_AUTH" \
  -H "territory: XX" \
  -H "api-version: v201" \
  -H "geolocation: -22.0;14.0" \
  -H "device-datetime: 2026-04-06T14:00:00.000Z" \
  -H "accept: application/json"
```

## Notes

- The sandbox uses test data, not real live Coventry listings.
- The sandbox may not contain an `odeon coventry` cinema record, so cinema search can return no content even when your credentials are correct.
- The `/api/cinemas/odeon/now-showing` endpoint is designed to verify request flow and response shape first.
- Once this is working, the next step can be saving results to a file or exposing more cinema routes.
- If credentials are wrong or missing, the Flask API will return an error JSON response instead of cinema data.
