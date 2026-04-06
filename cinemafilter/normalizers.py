def normalize_movie_title(title):
    return " ".join((title or "").split())


def normalize_age_ratings(value):
    if isinstance(value, list):
        return value

    if not value:
        return []

    return [value]


def flatten_showings(showings):
    if not isinstance(showings, dict):
        return []

    flattened = []

    for format_name, format_details in showings.items():
        times = format_details.get("times", []) if isinstance(format_details, dict) else []

        for show in times:
            flattened.append(
                {
                    "format": format_name,
                    "startTime": show.get("start_time") or show.get("time"),
                    "endTime": show.get("end_time"),
                }
            )

    return flattened


def normalize_movieglu_showtimes(cinema, location, show_date, matched_cinema, payload):
    films = payload.get("films", []) if isinstance(payload, dict) else []

    return {
        "cinema": cinema,
        "location": location,
        "date": show_date,
        "source": "movieglu",
        "matchedCinema": {
            "id": matched_cinema.get("cinema_id"),
            "name": matched_cinema.get("cinema_name"),
            "city": matched_cinema.get("city"),
            "distance": matched_cinema.get("distance"),
        },
        "listingCount": len(films),
        "listings": [
            {
                "filmId": film.get("film_id"),
                "title": normalize_movie_title(film.get("film_name", "")),
                "ageRatings": normalize_age_ratings(film.get("age_rating")),
                "showtimes": flatten_showings(film.get("showings")),
            }
            for film in films
        ],
    }
