from bs4 import BeautifulSoup
import requests
import pandas as pd
import logging
import math

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
                    , datefmt='%Y/%m/%d %H:%M:%S')
logger = logging.getLogger('imdb')


class InvalidParameterException(Exception):
    def __init__(self, msg):
        self.msg = msg


def get_info_top_n_movies(n: int) -> pd.DataFrame:
    """
    Returns information on the top n highest rated movies based on the input parameter
        Parameters:
            n (int): number of movies to get information on (number should be between 1 and 250)
        Returns:
            top_movies_df (pd.DataFrame): DataFrame containing information on each movie
    """
    # input parameter validation
    if n not in range(1, 251):
        raise InvalidParameterException('Invalid parameter! Please provide an integer between 1 and 250!')

    logger.info('Processing IMDB top 250 movies page')

    url = 'https://www.imdb.com/chart/top/'
    # get the page in english to avoid different results based on geolocation
    headers = {'Accept-Language': 'en-US'}

    top250 = requests.get(url, headers=headers).text

    top_movies = {"Rank": [], "Title": [], "Rating": [], "Number of Ratings": [], "Oscars": []}

    soup = BeautifulSoup(top250, 'lxml')
    movies_table = soup.find('tbody', class_='lister-list')
    movies = movies_table.find_all('tr', limit=n)
    for idx, movie in enumerate(movies):

        # get the rank of the movie based on the index
        top_movies["Rank"].append(idx + 1)

        for title in movie.find_all('td', class_='titleColumn'):
            # title is inside an 'a' tag
            movie_title = title.find("a").text
            top_movies["Title"].append(movie_title)

            # get the number of Oscars
            number_of_oscars = get_number_of_oscars(title, movie_title)
            top_movies["Oscars"].append(number_of_oscars)

        for rating in movie.find_all('td', class_='ratingColumn imdbRating'):
            # rating is inside a 'strong' tag. number of ratings has to be filtered out from the title tag
            # need to convert the values to numbers for later calculation
            top_movies["Rating"].append(float(rating.find("strong").text))
            top_movies["Number of Ratings"].append(int(rating.find("strong")['title'].split()[3].replace(',', '')))

    top_movies_df = pd.DataFrame(top_movies).set_index('Rank')
    return top_movies_df


def get_number_of_oscars(title_td: BeautifulSoup, movie_title: str) -> int:
    """
    Get the number of Oscars won from the movie subpage.
    Simulate that the request is coming from Mozilla else getting HTTP 403
        Parameters:
            title_td (BeautifulSoup): table column containing the link to the subpage
            movie_title (str): title of the movie
        Returns:
            number_of_oscars (int): number of oscars won
    """
    number_of_oscars = 0
    movie_url = f'https://www.imdb.com{title_td.find("a")["href"]}'
    headers = {"user-agent": "Mozilla/5.0"}

    logger.info(f'Processing "{movie_title}" subpage')
    movie_page = requests.get(movie_url, headers=headers).text

    movie_soup = BeautifulSoup(movie_page, 'lxml')
    movie_awards = movie_soup.find('a', {"aria-label": "See more awards and nominations"}).text

    if 'Won' in movie_awards:
        number_of_oscars = int(movie_awards.split()[1])

    return number_of_oscars


def write_to_file(name: str, movies_df: pd.DataFrame) -> pd.DataFrame:
    """
    Write the content of the given dictionary to a csv file
        Parameters:
            name (str): filename to use
            movies_df (pd.DataFrame): DataFrame containing the information on each movie
    """
    movies_df.to_csv(f'{name}.csv')


def oscar_adjustment(row: pd.Series) -> pd.Series:
    """
    Calculate the oscar adjustment
        Parameters:
            row (pd.Series): Row of the DataFrame to transform
        Returns:
            row (pd.Series): Transformed DataFrame row
    """
    if row["Oscars"] in range(1, 3):
        row["Rating"] = row["Rating"] + 0.3
    elif row["Oscars"] in range(3, 6):
        row["Rating"] = row["Rating"] + 0.5
    elif row["Oscars"] in range(6, 11):
        row["Rating"] = row["Rating"] + 1
    elif row["Oscars"] > 10:
        row["Rating"] = row["Rating"] + 1.5

    return row


def adjust_rating_with_oscars(movies_df: pd.DataFrame) -> pd.DataFrame:
    """
    Applying the Oscar transformation
        Parameters:
            movies_df (pd.DataFrame): movies DataFrame
        Returns:
            movies_df (pd.DataFrame): Transformed movies DataFrame
    """
    movies_df = movies_df.apply(oscar_adjustment, axis='columns')
    # round rating to 1 decimal
    movies_df['Rating'] = round(movies_df['Rating'], 1)
    return movies_df


def vote_adjustment(row: pd.Series) -> pd.Series:
    """
    Calculate the vote adjustment
        Parameters:
            row (pd.Series): Row of the DataFrame to transform
        Returns:
            row (pd.Series): Transformed DataFrame row
    """
    row["Rating"] = row["Rating"] - (math.floor((row["max_votes"] - row["Number of Ratings"])/100_000)*0.1)
    return row


def adjust_rating_with_votes(movies_df: pd.DataFrame) -> pd.DataFrame:
    """
    Applying the Number Of Ratings transformation
        Parameters:
            movies_df (pd.DataFrame): movies DataFrame
        Returns:
            movies_df (pd.DataFrame): Transformed movies DataFrame
    """
    # get movie with max votes
    movies_df['max_votes'] = movies_df['Number of Ratings'].max()
    movies_df = movies_df.apply(vote_adjustment, axis='columns')

    # round rating to 1 decimal
    movies_df['Rating'] = round(movies_df['Rating'], 1)

    movies_df = movies_df.drop(['max_votes'], axis=1)
    return movies_df


def final_rank(movies_df: pd.DataFrame):

    # sort by rating
    print(movies_df.index)

    movies_df = movies_df.sort_values(by=["Rating", "Rank"], ascending=False)

    # create rank
    # movies_df['Rank'] = movies_df['Rating'].rank(ascending=False).astype(int)

    # rearrange columns
    # movies_df = movies_df[['Rank', 'Title', 'Rating', 'Number of Ratings', 'Oscars']].set_index('Rank')

    return movies_df


if __name__ == '__main__':  # pragma: no cover
    try:
        top_n_movies_df = get_info_top_n_movies(20)
        write_to_file('original_ratings', top_n_movies_df)

        oscar_adjusted_df = adjust_rating_with_oscars(top_n_movies_df)
        write_to_file('oscar_adjusted_ratings', oscar_adjusted_df)

        vote_adjusted_df = adjust_rating_with_votes(top_n_movies_df)
        write_to_file('vote_adjusted_ratings', vote_adjusted_df)

        # final_top_list_df = final_rank(vote_adjusted_df)
        # write_to_file('final_top_list', final_top_list_df)
    except InvalidParameterException as e:
        logger.error(f'Error: {e}')
