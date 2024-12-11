import random
from movie_api import get_movie_details


class MovieApp:
    """A simple app for managing and interacting with movies."""

    def __init__(self, storage):
        """Set up the app with a storage system to manage movies."""
        self._storage = storage

    def _command_generate_website(self):
        """Create a website with the current list of movies."""
        try:
            template_path = 'static/index_template.html'
            try:
                with open(template_path, 'r') as template_file:
                    template = template_file.read()
            except FileNotFoundError:
                print(f"Error: Template file '{template_path}' not found.")
                return

            movie_grid = ""
            movies = self._storage.list_movies()

            if movies:
                for title, movie in movies.items():
                    movie_grid += f"""
                    <div class="movie-item">
                        <img src="{movie['poster']}" alt="{title} Poster">
                        <h2>{title}</h2>
                        <p>{movie['year']}</p>
                        <p>Rating: {movie['rating']}</p>
                    </div>
                    """

            html_content = template.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

            with open('templates/movie_list.html', 'w') as output_file:
                output_file.write(html_content)

            print("Website was generated successfully. CLICK -> http://127.0.0.1:5000")

        except Exception as e:
            print(f"Error generating website: {e}")

    def _command_list_movies(self):
        """Show all movies currently in storage."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies available.")
        else:
            print("Movies in your collection:")
            for title, movie in movies.items():
                print(f"{title} - {movie['rating']} - {movie['year']}")

    def _command_add_movie(self):
        """Add a new movie to the collection using the OMDb API."""
        title = input("Enter movie title: ")
        movie_details = get_movie_details(title)

        if "Error" not in movie_details:
            print(f"Movie found: {movie_details['Title']} ({movie_details['Year']})")
            print(f"Rating: {movie_details.get('imdbRating', 'N/A')}")

            self._storage.add_movie(
                movie_details['Title'],
                movie_details['Year'],
                movie_details.get('imdbRating', 'N/A'),
                movie_details.get('Poster', "No Poster Available")
            )
            print(f"Movie '{movie_details['Title']}' added.")
        else:
            print(f"Error: {movie_details['Error']}")

    def _command_delete_movie(self):
        """Prompts the user to delete a movie from the storage system."""
        title = input("Enter the title of the movie to delete: ").strip().lower()
        movies = self._storage.list_movies()

        for movie_title in movies.keys():
            if movie_title.strip().lower() == title:
                self._storage.delete_movie(movie_title)
                print(f"Movie '{movie_title}' deleted.")
                return

        print(f"Movie '{title}' not found.")

    def _command_update_movie(self):
        """Update the rating of a specific movie."""
        title = input("Enter movie title to update: ").strip()
        rating = float(input("Enter new rating: "))

        for movie_title in self._storage.list_movies().keys():
            if movie_title.strip().lower() == title.strip().lower():
                self._storage.update_movie(movie_title, rating)
                print(f"Movie '{movie_title}' rating updated to {rating}.")
                break
        else:
            print(f"Movie '{title}' not found.")

    def _command_movie_stats(self):
        """Show statistics about the movies (total count, average rating, best, and worst movie)."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies to calculate statistics for.")
            return

        total_rating = 0
        count = len(movies)
        for movie in movies.values():
            total_rating += float(movie["rating"])

        average_rating = total_rating / count if count > 0 else 0

        best_movies = []
        worst_movies = []
        max_rating = max(float(movie["rating"]) for movie in movies.values())
        min_rating = min(float(movie["rating"]) for movie in movies.values())

        for title, movie in movies.items():
            if float(movie["rating"]) == max_rating:
                best_movies.append(title)
            if float(movie["rating"]) == min_rating:
                worst_movies.append(title)

        print(f"Total Movies: {count}")
        print(f"Average Rating: {average_rating:.2f}")
        print(f"Best Movie: {', '.join(best_movies)} (Rating: {max_rating})")
        print(f"Worst Movie: {', '.join(worst_movies)} (Rating: {min_rating})")

    def _command_random_movie(self):
        """Pick and show a random movie from the collection."""
        movies = self._storage.list_movies()

        if not movies:
            print("No movies available.")
        else:
            random_movie_title = random.choice(list(movies.keys()))
            movie_details = get_movie_details(random_movie_title)

            if "Error" not in movie_details:
                title = movie_details.get('Title', 'N/A')
                year = movie_details.get('Year', 'N/A')
                rating = movie_details.get('imdbRating', 'N/A')

                print(f"Random Movie: {title} ({year})")
                print(f"Rating: {rating}")


            else:
                print(f"Error: {movie_details['Error']}")

    def _command_search_movie(self):
        """Find movies that match part of the title."""
        title_part = input("Enter part of the movie title to search: ").lower()
        movies = self._storage.list_movies()
        matching_movies = {title: movie for title, movie in movies.items() if title_part in title.lower()}

        if matching_movies:
            print(f"Found {len(matching_movies)} result(s):")
            for idx, (title, movie) in enumerate(matching_movies.items(), start=1):
                print(f"{idx}. {title} ({movie['year']})")
        else:
            print("No matching movies found.")

    def _command_sorted_by_rating(self):
        """Show movies sorted by their rating."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies available.")
        else:
            sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
            for title, movie in sorted_movies:
                print(f"Title: {title}, Year: {movie['year']}, Rating: {movie['rating']}")

    def _print_menu(self):
        """Display the main menu for the user."""
        print("\nWelcome to the Movie App!")
        print("0. Exit")
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("4. Update movie")
        print("5. Stats")
        print("6. Random movie")
        print("7. Search movie")
        print("8. Movies sorted by rating")
        print("9. Generate website")

    def run(self):
        """Start the app and wait for user input."""
        while True:
            self._print_menu()
            choice = input("Select an option (1-9): ")
            if choice == "1":
                self._command_list_movies()
            elif choice == "2":
                self._command_add_movie()
            elif choice == "3":
                self._command_delete_movie()
            elif choice == "4":
                self._command_update_movie()
            elif choice == "5":
                self._command_movie_stats()
            elif choice == "6":
                self._command_random_movie()
            elif choice == "7":
                self._command_search_movie()
            elif choice == "8":
                self._command_sorted_by_rating()
            elif choice == "9":
                self._command_generate_website()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")
