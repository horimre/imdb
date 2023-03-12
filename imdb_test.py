import unittest
import imdb
import pandas as pd


class TestImdb(unittest.TestCase):

    def test_best_movie(self):
        self.best_movie = {"Rank": 1, "Title": 'The Shawshank Redemption', "Rating": 9.2,
                           "Number of Ratings": 2712879, "Oscars": 0}

        result = imdb.get_info_top_n_movies(1)

        self.assertEqual(self.best_movie['Rank'], result['Rank'][0])
        self.assertEqual(self.best_movie['Title'], result['Title'][0])
        self.assertEqual(self.best_movie['Rating'], result['Rating'][0])
        self.assertGreaterEqual(result['Number of Ratings'][0], self.best_movie['Number of Ratings'])
        self.assertEqual(self.best_movie['Oscars'], result['Oscars'][0])

    def test_movie_with_oscars(self):
        self.movie = {"Rank": 2, "Title": 'The Godfather', "Rating": 9.2,
                      "Number of Ratings": 1884328, "Oscars": 3}

        result = imdb.get_info_top_n_movies(2)

        self.assertEqual(self.movie['Rank'], result['Rank'][1])
        self.assertEqual(self.movie['Title'], result['Title'][1])
        self.assertEqual(self.movie['Rating'], result['Rating'][1])
        self.assertGreaterEqual(result['Number of Ratings'][1], self.movie['Number of Ratings'])
        self.assertEqual(self.movie['Oscars'], result['Oscars'][1])

    def test_invalid_rank(self):
        with self.assertRaises(imdb.InvalidParameterException):
            imdb.get_info_top_n_movies(300)

    def test_write_df_to_csv(self):
        self.movie = {"Rank": [1], "Title": ['The Shawshank Redemption'], "Rating": [9.2], "Oscars": [0]}
        test_df = pd.DataFrame(self.movie)

        movies_df = imdb.write_to_file('Test', test_df)
        movies_df = movies_df.loc[:, movies_df.columns != 'Number of Ratings'].reset_index()

        self.assertEqual(True, test_df.equals(movies_df))


if __name__ == '__main__':
    unittest.main()
