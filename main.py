from movie_app import MovieApp
from storage_csv import StorageCsv

def main():
    """
    The main function that initializes the movie app and runs it.

    It creates an instance of the StorageCsv class to handle data
    storage and passes it to the MovieApp class. The MovieApp instance
    is then run to start the application.
    """
    storage = StorageCsv('data/movies.csv')

    movie_app = MovieApp(storage)

    movie_app.run()

if __name__ == "__main__":
    main()
