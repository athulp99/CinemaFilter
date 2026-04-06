# Architecture

## Goal

The app provides a small local API in front of MovieGlu so you can:

1. test sandbox credentials safely from your machine
2. inspect response shapes through stable local endpoints
3. normalize cinema/showtime data before using it elsewhere

## Request flow

1. Flask receives a local request
2. `cinemafilter/config.py` loads credentials from `.env`
3. `cinemafilter/movieglu/client.py` sends a REST request to MovieGlu
4. `cinemafilter/services/odeon.py` chooses the best Odeon cinema match
5. `cinemafilter/normalizers.py` converts upstream data into app-friendly JSON

## Why Flask here

- easy local testing with `curl` or Postman
- simple place to add more endpoints later
- clean separation between your app and MovieGlu
- useful even if you later add a frontend

## Near-term roadmap

- add JSON file export
- add more cinema routes
- add tests around matching and normalization
- support evaluation mode and sandbox mode with clearer output
