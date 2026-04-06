from ..movieglu.client import MovieGluClient
from ..normalizers import normalize_movieglu_showtimes


def score_cinema_match(cinema, hint):
    normalized_hint = hint.lower()
    cinema_name = (cinema.get("cinema_name") or "").lower()
    city = (cinema.get("city") or "").lower()
    score = 0

    if "odeon" in cinema_name:
        score += 5

    if normalized_hint in cinema_name:
        score += 8

    for word in normalized_hint.split():
        if word in cinema_name:
            score += 2
        if word in city:
            score += 1

    distance = cinema.get("distance")
    if isinstance(distance, (int, float)):
        score -= distance / 100

    return score


def pick_best_cinema_match(cinemas, cinema_name_hint):
    ranked = sorted(
        cinemas,
        key=lambda cinema: score_cinema_match(cinema, cinema_name_hint),
        reverse=True,
    )
    return ranked[0] if ranked else None


def get_odeon_now_showing(settings, location, cinema_query, cinema_name_hint, show_date):
    client = MovieGluClient(settings)
    search_payload = client.search_cinemas(query=cinema_query, limit=10)
    cinemas = search_payload.get("cinemas", [])
    matched_cinema = pick_best_cinema_match(cinemas, cinema_name_hint)

    if not matched_cinema:
        raise ValueError(f"No matching Odeon cinema found for query: {cinema_query}")

    showtimes_payload = client.get_cinema_showtimes(
        cinema_id=matched_cinema.get("cinema_id"),
        show_date=show_date,
        sort="alphabetical",
    )

    return normalize_movieglu_showtimes(
        cinema="odeon",
        location=location,
        show_date=show_date,
        matched_cinema=matched_cinema,
        payload=showtimes_payload,
    )
