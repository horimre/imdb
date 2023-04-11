import pytest
from src import imdb
import pandas as pd
import logging
import asyncio
import unittest.mock as mock

logging.getLogger('imdb').disabled = True


@pytest.fixture()
def shawshank_redemption():
    return pd.DataFrame({"Rank": [1], "Title": ['The Shawshank Redemption'],
                         "Link": ['https://www.imdb.com/title/tt0111161/'], "Original Rating": [9.2],
                         "Number of Ratings": [2712879], "Oscars": [0]})


@pytest.fixture()
def godfather():
    return pd.DataFrame({"Rank": [2], "Title": ['The Godfather'], "Link": ['https://www.imdb.com/title/tt0068646/'],
                         "Original Rating": [9.2], "Number of Ratings": [1884328], "Oscars": [3]})


@pytest.fixture()
def dark_knight():
    return pd.DataFrame({"Rank": [3], "Title": ['The Dark Knight'], "Original Rating": [9.0],
                         "Number of Ratings": [2686057], "Oscars": [2]})


@pytest.fixture()
def godfather2():
    return pd.DataFrame({"Rank": [4], "Title": ['The Godfather Part II'], "Original Rating": [9.0],
                         "Number of Ratings": [1286306], "Oscars": [6]})


@pytest.fixture()
def lotr3():
    return pd.DataFrame({"Rank": [7], "Title": ['The Lord of the Rings: The Return of the King'],
                         "Original Rating": [8.9], "Number of Ratings": [1867043], "Oscars": [11]})


def test_invalid_param():
    with pytest.raises(imdb.InvalidParameterException):
        imdb.get_info_top_n_movies(300)


def test_best_movie(shawshank_redemption):
    movies_df = imdb.get_info_top_n_movies(1).reset_index()

    # convert movies_df to pd.Series
    movie = movies_df.iloc[-1]

    assert shawshank_redemption.loc[0, 'Rank'] == movie['Rank']
    assert shawshank_redemption.loc[0, 'Title'] == movie['Title']
    assert shawshank_redemption.loc[0, 'Original Rating'] == movie['Original Rating']
    assert movie['Number of Ratings'] >= shawshank_redemption.loc[0, 'Number of Ratings']


def test_get_oscars(godfather):

    movies_df = asyncio.run(imdb.process_movie_pages(godfather)).reset_index()

    # get the second movie and convert to pd.Series
    movie = movies_df.iloc[-1]

    assert godfather.loc[0, 'Rank'] == movie['Rank']
    assert godfather.loc[0, 'Title'] == movie['Title']
    assert godfather.loc[0, 'Original Rating'] == movie['Original Rating']
    assert movie['Number of Ratings'] >= godfather.loc[0, 'Number of Ratings']
    assert movie['Oscars'] == 3


def test_write_to_file(godfather):
    # mock pandas.DataFrame.to_csv method
    with mock.patch.object(godfather, "to_csv") as to_csv_mock:
        imdb.write_to_file('Test', godfather)
        to_csv_mock.assert_called_with('Test.csv')


def test_no_oscar(shawshank_redemption):
    movies_df = imdb.adjust_rating_with_oscars(shawshank_redemption)

    assert 9.2 == movies_df.loc[0, 'Oscar Adjusted Rating']


def test_2_oscars(dark_knight):
    movies_df = imdb.adjust_rating_with_oscars(dark_knight)

    assert 9.3 == movies_df.loc[0, 'Oscar Adjusted Rating']


def test_3_oscars(godfather):
    movies_df = imdb.adjust_rating_with_oscars(godfather)

    assert 9.7 == movies_df.loc[0, 'Oscar Adjusted Rating']


def test_6_oscars(godfather2):
    movies_df = imdb.adjust_rating_with_oscars(godfather2)

    assert 10 == movies_df.loc[0, 'Oscar Adjusted Rating']


def test_11_oscars(lotr3):
    movies_df = imdb.adjust_rating_with_oscars(lotr3)

    assert 10.4 == movies_df.loc[0, 'Oscar Adjusted Rating']


def test_vote_adjustment(shawshank_redemption, godfather):
    test_df = pd.concat([shawshank_redemption, godfather]).reset_index()
    movies_df = imdb.adjust_rating_with_votes(test_df)

    assert 8.4 == movies_df.loc[1, 'Vote Adjusted Rating']
