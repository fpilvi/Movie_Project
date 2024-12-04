from flask import Flask, render_template, redirect, url_for
from storage_csv import StorageCsv

app = Flask(__name__)

storage = StorageCsv('data/movies.csv')


def get_movies():
    """
    Fetch movie data from the CSV storage.

    Calls the list_movies method from the StorageCsv class to retrieve all
    movie data stored in the CSV file. Returns a dictionary of movie data.

    Returns:
        dict: A dictionary containing movie data (title, rating, year, poster).
    """
    return storage.list_movies()


@app.route('/')
def home():
    """
    Home route that redirects to the movies list page.

    When a user visits the root URL '/', they are redirected to the /movies route
    to see the list of movies.

    Returns:
        RedirectResponse: A redirect to the /movies route.
    """
    return redirect(url_for('movie_list'))


@app.route('/movies')
def movie_list():
    """
    Movies list route that fetches and displays the list of movies.

    This route fetches movie data using the get_movies function and passes it
    to the movie_list.html template for rendering.

    Returns:
        str: Rendered HTML page displaying the list of movies.
    """
    movies = get_movies()
    return render_template('movie_list.html', movies=movies)


if __name__ == '__main__':
    """
    Starts the Flask application.

    Runs the Flask application in debug mode when the script is executed directly.
    """
    app.run(debug=True)