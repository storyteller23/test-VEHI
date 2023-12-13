import requests
from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)
url = "https://swapi.dev/api/people"


def get_persons_data_with_page(page=1):
    response = requests.get(url, params={"page": page})

    response.raise_for_status()

    data = response.json()
    next_page = page + 1 if data["next"] else None
    previous_page = page - 1 if data["previous"] else None
    persons = data["results"]

    return {
        "next_page": next_page,
        "previous_page": previous_page,
        "persons": persons,
    }


@app.route("/", methods=["GET"])
def index():
    page = request.args.get("page", default=1, type=int)

    try:
        context = get_persons_data_with_page(page)
        return render_template("index.html", **context, current_page=page)
    except requests.exceptions.HTTPError as ex:
        if ex.response.status_code == 404:
            return redirect(url_for("index"))
        abort(ex.response.status_code, f"{ex}")
    except Exception as ex:
        abort(500, ex)


if __name__ == "__main__":
    app.run(debug=False, port=8000)
