import csv
from storage.istorage import IStorage


class StorageCsv(IStorage):
    """Handles movie storage in a CSV file."""

    def __init__(self, file_path):
        """
        Initializes the StorageCsv instance with a given file path.

        Args:
            file_path (str): The path to the CSV file where movie data is stored.
        """
        self.file_path = file_path

    def _load_data(self):
        """
        Reads the CSV file and returns movie data as a dictionary.

        This method reads the CSV file, extracting movie data and storing it
        in a dictionary where the key is the movie title, and the value is a
        dictionary with rating, year, and poster information.

        Returns:
            dict: A dictionary of movies, where the key is the movie title and
                  the value is a dictionary with the movie's rating, year, and poster.
        """
        movies = {}
        try:
            with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    title = row["title"].strip()
                    movies[title] = {
                        "rating": float(row["rating"]),
                        "year": int(row["year"]),
                        "poster": row["poster"]
                    }
        except FileNotFoundError:
            pass
        return movies

    def _save_data(self, movies):
        """
        Saves movie data to the CSV file.

        This method takes a dictionary of movies and writes it back to the CSV file.

        Args:
            movies (dict): A dictionary of movies, where the key is the movie title
                           and the value is a dictionary with the movie's rating, year, and poster.
        """
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["title", "rating", "year", "poster"])
            writer.writeheader()
            for title, details in movies.items():
                writer.writerow({
                    "title": title,
                    "rating": details["rating"],
                    "year": details["year"],
                    "poster": details["poster"]
                })

    def list_movies(self):
        """
        Returns all movies as a dictionary.

        This method retrieves the movie data from the CSV file by calling
        the _load_data method and returns it.

        Returns:
            dict: A dictionary of all movies stored in the CSV file.
        """
        return self._load_data()

    def add_movie(self, title, year, rating, poster):
        """
        Adds a new movie to the CSV file.

        This method adds a new movie to the internal dictionary and saves it
        to the CSV file.

        Args:
            title (str): The title of the movie.
            year (int): The release year of the movie.
            rating (float): The rating of the movie.
            poster (str): The URL or file path to the movie poster image.
        """
        movies = self._load_data()
        movies[title.strip()] = {
            "rating": rating,
            "year": year,
            "poster": poster
        }
        self._save_data(movies)

    def delete_movie(self, title):
        """
        Deletes a movie from the CSV file.

        This method removes the specified movie by title from the internal
        dictionary and saves the updated list back to the CSV file.

        Args:
            title (str): The title of the movie to be deleted.

        Raises:
            ValueError: If the movie title is not found in the CSV.
        """
        movies = self._load_data()
        title = title.strip()
        if title in movies:
            del movies[title]
            self._save_data(movies)
        else:
            print(f"Movie '{title}' not found.")

    def update_movie(self, title, rating):
        """
        Updates the rating of a movie in the CSV file.

        This method updates the rating of an existing movie in the internal
        dictionary and saves the updated data back to the CSV file.

        Args:
            title (str): The title of the movie to be updated.
            rating (float): The new rating for the movie.

        Raises:
            ValueError: If the movie title is not found in the CSV.
        """
        movies = self._load_data()
        title = title.strip()
        if title in movies:
            movies[title]["rating"] = rating
            self._save_data(movies)
        else:
            print(f"Movie '{title}' not found.")