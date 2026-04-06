from flask import Flask, jsonify, request

from .config import get_settings
from .movieglu.client import MovieGluClient, MovieGluError
from .services.odeon import get_odeon_now_showing


def create_app():
    app = Flask(__name__)

    @app.get("/health")
    def health():
        settings = get_settings()
        return jsonify(
            {
                "status": "ok",
                "provider": "movieglu",
                "territory": settings.movieglu_territory,
                "mode": "sandbox" if settings.movieglu_territory == "XX" else "evaluation",
            }
        )

    @app.get("/api/movieglu/cinemas/search")
    def search_cinemas():
        settings = get_settings()
        query = request.args.get("query", settings.movieglu_cinema_query)
        limit = int(request.args.get("limit", 5))
        client = MovieGluClient(settings)

        try:
            payload = client.search_cinemas(query=query, limit=limit)
        except MovieGluError as error:
            return jsonify({"error": str(error)}), 502

        cinemas = payload.get("cinemas", [])

        return jsonify(
            {
                "query": query,
                "resultCount": len(cinemas),
                "cinemas": [
                    {
                        "cinemaId": cinema.get("cinema_id"),
                        "name": cinema.get("cinema_name"),
                        "city": cinema.get("city"),
                        "distance": cinema.get("distance"),
                    }
                    for cinema in cinemas
                ],
            }
        )

    @app.get("/api/movieglu/films/now-showing")
    def films_now_showing():
        settings = get_settings()
        limit = int(request.args.get("limit", 10))
        client = MovieGluClient(settings)

        try:
            payload = client.get_films_now_showing(limit=limit)
        except MovieGluError as error:
            return jsonify({"error": str(error)}), 502

        films = payload.get("films", [])

        return jsonify(
            {
                "resultCount": len(films),
                "films": [
                    {
                        "filmId": film.get("film_id"),
                        "title": film.get("film_name"),
                    }
                    for film in films
                ],
            }
        )

    @app.get("/api/cinemas/odeon/now-showing")
    def odeon_now_showing():
        settings = get_settings()
        query = request.args.get("query", settings.movieglu_cinema_query)
        name_hint = request.args.get("name_hint", settings.movieglu_cinema_name_hint)
        show_date = request.args.get("date", settings.movieglu_show_date)
        location = request.args.get("location", "Coventry")

        try:
            result = get_odeon_now_showing(
                settings=settings,
                location=location,
                cinema_query=query,
                cinema_name_hint=name_hint,
                show_date=show_date,
            )
        except MovieGluError as error:
            return jsonify({"error": str(error)}), 502
        except ValueError as error:
            return jsonify({"error": str(error)}), 404

        return jsonify(result)

    return app
