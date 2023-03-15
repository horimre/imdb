import unittest
import unittest.mock as mock
import imdb
import pandas as pd
import logging
import asyncio


logging.getLogger('imdb').disabled = True


class TestImdb(unittest.TestCase):

    def test_best_movie(self):
        self.movie = {"Rank": 1, "Title": 'The Shawshank Redemption', "Original Rating": 9.2,
                      "Number of Ratings": 2712879, "Oscars": 0}
        test_series = pd.Series(self.movie)

        movies_df = imdb.get_info_top_n_movies(1).reset_index()

        # convert movies_df to pd.Series
        movie = movies_df.iloc[-1]

        self.assertEqual(test_series['Rank'], movie['Rank'])
        self.assertEqual(test_series['Title'], movie['Title'])
        self.assertEqual(test_series['Original Rating'], movie['Original Rating'])
        self.assertGreaterEqual(movie['Number of Ratings'], test_series['Number of Ratings'])

    def test_get_oscars(self):
        self.movie = {"Rank": [2], "Title": ['The Godfather'], "Link": ['https://www.imdb.com/title/tt0068646/'],
                      "Original Rating": [9.2], "Number of Ratings": [1884328]}
        test_df = pd.DataFrame(self.movie)

        movies_df = asyncio.run(imdb.process_movie_pages(test_df)).reset_index()

        # get the second movie and convert to pd.Series
        movie = movies_df.iloc[-1]

        self.assertEqual(test_df.loc[0, 'Rank'], movie['Rank'])
        self.assertEqual(test_df.loc[0, 'Title'], movie['Title'])
        self.assertEqual(test_df.loc[0, 'Original Rating'], movie['Original Rating'])
        self.assertGreaterEqual(movie['Number of Ratings'], test_df.loc[0, 'Number of Ratings'])
        self.assertEqual(movie['Oscars'], 3)

    def test_invalid_param(self):
        with self.assertRaises(imdb.InvalidParameterException):
            imdb.get_info_top_n_movies(300)

    def test_write_to_file(self):
        self.movie = {"Rank": [1], "Title": ['The Shawshank Redemption'], "Original Rating": [9.2],
                      "Number of Ratings": [2712879], "Oscars": [0]}
        test_df = pd.DataFrame(self.movie)

        # mock pandas.DataFrame.to_csv method
        with mock.patch.object(test_df, "to_csv") as to_csv_mock:
            imdb.write_to_file('Test', test_df)
            to_csv_mock.assert_called_with('Test.csv')

    def test_no_oscar(self):
        self.movie = {"Rank": [1], "Title": ['The Shawshank Redemption'], "Original Rating": [9.2],
                      "Number of Ratings": [2712879], "Oscars": [0]}
        test_df = pd.DataFrame(self.movie)

        movies_df = imdb.adjust_rating_with_oscars(test_df)

        self.assertEqual(9.2, movies_df.loc[0, 'Oscar Adjusted Rating'])

    def test_2_oscars(self):
        self.movie = {"Rank": [3], "Title": ['The Dark Knight'], "Original Rating": [9.0],
                      "Number of Ratings": [2686057], "Oscars": [2]}
        test_df = pd.DataFrame(self.movie)

        movies_df = imdb.adjust_rating_with_oscars(test_df)

        self.assertEqual(9.3, movies_df.loc[0, 'Oscar Adjusted Rating'])

    def test_3_oscars(self):
        self.movie = {"Rank": [2], "Title": ['The Godfather'], "Original Rating": [9.2],
                      "Number of Ratings": [1884328], "Oscars": [3]}
        test_df = pd.DataFrame(self.movie)

        movies_df = imdb.adjust_rating_with_oscars(test_df)

        self.assertEqual(9.7, movies_df.loc[0, 'Oscar Adjusted Rating'])

    def test_6_oscars(self):
        self.movie = {"Rank": [4], "Title": ['The Godfather Part II'], "Original Rating": [9.0],
                      "Number of Ratings": [1286306], "Oscars": [6]}
        test_df = pd.DataFrame(self.movie)

        movies_df = imdb.adjust_rating_with_oscars(test_df)

        self.assertEqual(10, movies_df.loc[0, 'Oscar Adjusted Rating'])

    def test_11_oscars(self):
        self.movie = {"Rank": [7], "Title": ['The Lord of the Rings: The Return of the King'], "Original Rating": [8.9],
                      "Number of Ratings": [1867043], "Oscars": [11]}
        test_df = pd.DataFrame(self.movie)

        movies_df = imdb.adjust_rating_with_oscars(test_df)

        self.assertEqual(10.4, movies_df.loc[0, 'Oscar Adjusted Rating'])

    def test_vote_adjustment(self):
        self.movies = {"Rank": [1, 2], "Title": ['The Shawshank Redemption', 'The Godfather'], "Original Rating": [9.2, 9.2],
                       "Number of Ratings": [2712879, 1884969], "Oscars": [0, 3]}
        test_df = pd.DataFrame(self.movies)

        movies_df = imdb.adjust_rating_with_votes(test_df)

        self.assertEqual(8.4, movies_df.loc[1, 'Vote Adjusted Rating'])


if __name__ == '__main__':
    unittest.main()
