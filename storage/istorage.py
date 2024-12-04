from abc import ABC, abstractmethod

class IStorage(ABC):
    """
    Abstract base class for storage systems, providing a blueprint for handling movie data.

    Subclasses should implement the following methods to provide specific storage solutions
    (e.g., CSV, JSON).
    """

    @abstractmethod
    def list_movies(self):
        """
        Lists all movies stored in the storage system.

        Returns:
            dict: A dictionary where keys are movie titles and values are movie details
                  (e.g., rating, year, poster).
        """
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """
        Adds a new movie to the storage system.

        Args:
            title (str): The title of the movie.
            year (int): The release year of the movie.
            rating (float): The IMDB rating of the movie.
            poster (str): URL or path to the movie's poster.
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Deletes a movie from the storage system.

        Args:
            title (str): The title of the movie to be deleted.
        """
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """
        Updates the rating of an existing movie in the storage system.

        Args:
            title (str): The title of the movie to be updated.
            rating (float): The new IMDB rating for the movie.
        """
        pass