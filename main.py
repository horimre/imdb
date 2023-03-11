from bs4 import BeautifulSoup
import requests
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)


class InvalidParameterException(Exception):
    def __init__(self, msg):
        self.msg = msg


def get_info_top_n_movies(n: int) -> dict:
    """
    Returns information on the top n highest rated movies based on the input parameter
        Parameters:
            n (int): number of movies to get information on (number should be between 1 and 250)
        Returns:
            basic_info (dict): dictionary containing the basic information on each movie
    """
    # input parameter validation
    if n not in range(1, 251):
        raise InvalidParameterException('Invalid parameter! Please provide an integer between 1 and 250!')

    logging.info('Process IMDB top 250 movies page')
    top250 = requests.get('https://www.imdb.com/chart/top/?ref_=nv_mp_mv250').text

    top_movies = {"Rank": [], "Title": [], "Rating": [], "Number of Ratings": [], "Oscars": []}

    soup = BeautifulSoup(top250, 'lxml')
    movies_table = soup.find('tbody', class_='lister-list')
    movies = movies_table.find_all('tr', limit=n)
    for idx, movie in enumerate(movies):

        # get the rank of the movie based on the index
        top_movies["Rank"].append(idx + 1)

        # TODO: create separate functions to get title, oscars and ratings
        for title in movie.find_all('td', class_='titleColumn'):
            # title is inside an 'a' tag
            movie_title = title.find("a").text
            top_movies["Title"].append(movie_title)

            # get oscars from the movie subpage. simulate that the request is coming from mozilla else getting HTTP 403
            movie_url = f'https://www.imdb.com{title.find("a")["href"]}'
            headers = {"user-agent": "Mozilla/5.0"}

            logging.info(f'Process "{movie_title}" movie page')
            movie_page = requests.get(movie_url, headers=headers).text

            movie_soup = BeautifulSoup(movie_page, 'lxml')
            movie_awards = movie_soup.find('a', {"aria-label": "See more awards and nominations"}).text

            number_of_oscars = 0
            if 'Won' in movie_awards:
                number_of_oscars = int(movie_awards.split()[1])

            top_movies["Oscars"].append(number_of_oscars)

        for rating in movie.find_all('td', class_='ratingColumn imdbRating'):
            # rating is inside a 'strong' tag. number of ratings has to be filtered out from the title tag
            # need to convert the values to numbers for later calculation
            top_movies["Rating"].append(float(rating.find("strong").text))
            top_movies["Number of Ratings"].append(int(rating.find("strong")['title'].split()[3].replace(',', '')))

    return top_movies


def write_to_file(name: str, dictionary: dict) -> None:
    """
    Write the content of the given dictionary to a csv file
        Parameters:
            name (str): filename to use
            dictionary (dict): dictionary containing the information on each movie
    """
    df = pd.DataFrame(dictionary).set_index('Rank')
    df.to_csv(f'{name}.csv')


if __name__ == '__main__':
    try:
        top_n_movies = get_info_top_n_movies(20)
        write_to_file('original_ratings', top_n_movies)
    except InvalidParameterException as e:
        logging.error(f'Error: {e}')

