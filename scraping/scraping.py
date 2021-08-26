import requests
from bs4 import BeautifulSoup, SoupStrainer

class Scraping:
  """ Scrapes the data from fbref.com: competitions, seasons, matchweeks, and games.
  Provides a function that catches all the data needed.

  @url string: URL of fbref.com
  @data list: all the data stored in a list of combinations of dictionaries and lists.
  """

  def __init__(self, url):
    self.url = url
    self.data = []

  # Get the requests object from the URL
  def get_url_response(self):
    url_competitions = self.url + "/en/comps"
    response = requests.get(url_competitions)
    return response

  # Returns the name and the link of each competition
  def set_competitions(self):
    response = self.get_url_response()
    if response.ok:
      strainer = SoupStrainer('table', {'id': 'comps_club'})
      soup = BeautifulSoup(response.text, 'lxml', parse_only=strainer)
      
      tbody_comp = soup.find('tbody')
      th_comp = tbody_comp.find_all('th')
      
      name_comp = []
      link_comp = []

      for i in th_comp:
        if i.text != 'Big 5 European Leagues Combined':
          name_comp.append(i.text)
          link_c = self.url+i.find('a', href=True)['href']
          link_comp.append(link_c)

      return dict(zip(name_comp, link_comp))

  # For a given competition, returns a dictionary {name of the season: link}
  def set_seasons_per_comp(self, link_comp):
    response_comp = requests.get(link_comp)
    if response_comp.ok:
      strainer = SoupStrainer('table', {'id': 'seasons'})
      soup = BeautifulSoup(response_comp.text, 'lxml', parse_only=strainer)

      tbody_season = soup.find('tbody')
      th_season = tbody_season.find_all('th')
      td_teams = tbody_season.find_all('td', attrs={'data-stat': 'num_squads'})

      name_season = []
      link_season = []
      num_squads_season = []
      values = []

      for i in th_season:
        name_season.append(i.text)
        link_s = self.url+i.find('a', href=True)['href']
        link_season.append(link_s)
      for i in td_teams:
        num_squads_season.append(int(i.text))
      for i in range(len(link_season)):
        values.append([link_season[i], num_squads_season[i]])

      return dict(zip(name_season, values))

  # Returns the link of the table that contains the link of each season recorded
  def get_scores_and_fixtures(self, link):
    response_s_f = requests.get(link)
    if response_s_f.ok:
      strainer = SoupStrainer('li', {'class': 'full '})
      soup = BeautifulSoup(response_s_f.text, 'lxml', parse_only=strainer)
      link_s_f = soup.find('a', href=True)['href']

      return self.url+link_s_f

  # Returns all the games of a given matchweek
  def set_games_per_matchweek(self, soup, matchweek, n_games):
    games = []
    n = 0
    for i in soup.findAll('tr'):
      try:
        try:
          tag = i.find('td', attrs={'data-stat': 'gameweek'}).text
        except:
          tag = i.find('th', attrs={'data-stat': 'gameweek'}).text
        if int(tag) == matchweek:
          n += 1
          score_tag = i.find('td', attrs={'data-stat': 'score'}).find('a', href=True)

          score = score_tag.text.replace('–', '-')
          link_game = self.url+score_tag['href']
          home = i.find('td', attrs={'data-stat': 'squad_a'}).find('a', href=True).text
          away = i.find('td', attrs={'data-stat': 'squad_b'}).find('a', href=True).text
          date = i.find('td', attrs={'data-stat': 'date'}).find('a', href=True).text

          games.append({'score': score, 'link': link_game, 'home': home, 'away': away, 'date': date})
        if n == n_games:
          break
      except:
        pass

    return games

  # Returns a list of dictionaries {week: list of the corresponding games}
  def set_matchweeks_per_season(self, n_teams, link_s_f):
    n_matchweeks = (n_teams*2-2)
    n_games = int(n_teams/2)

    list_games = []
    response_g = requests.get(link_s_f)
    if response_g.ok:
      strainer = SoupStrainer('tbody')
      soup = BeautifulSoup(response_g.text, 'lxml', parse_only=strainer)

      for i in range(1,n_matchweeks+1):
        list_games.append({'week': i,
                          'games': self.set_games_per_matchweek(soup, i, n_games)})

      return list_games

  # Set all the data needed
  def set_data(self):
    for competition, link_comp in self.set_competitions().items():
      print(competition)
      dict_competitions = {'name': competition, 'seasons': []}
      for season, values in self.set_seasons_per_comp(link_comp).items():
        dict_competitions['seasons'].append({'name': season, 'matchweeks': self.set_matchweeks_per_season(values[1], self.get_scores_and_fixtures(values[0]))})
      self.data.append(dict_competitions)

  # Returns a list of all the competitions. List.
  def get_competitions(self):
    return [document['name'] for document in self.data]

  # Returns all the seasons recorded for a given competition. List of season names.
  def get_seasons_per_comp(self, indice):
    return [season['name'] for season in self.data[indice]['seasons']]
  
  # Returns all the seasons of all the competitions
  def get_seasons(self):
    return dict(zip(self.get_competitions(), \
      [self.get_seasons_per_comp(i) for i in range(len(self.data))]))

  # Returns all the matchweeks of a given season, of a given competition. Dictionary {name of the season: list of matchweeks}.
  def get_matchweek_per_season(self, i_comp, j_season):
    season = self.data[i_comp]['seasons'][j_season]
    return {season['name']: [i['week'] for i in season['matchweeks']]}

  # Returns all the matchweeks of all the seasons, of a given competition. Dictionary {comp: [{name_season: [matchweeks]}]}.
  def get_matchweek_per_comp(self, i_comp):
    comp = self.data[i_comp]
    seasons = [self.get_matchweek_per_season(i_comp, j_season) for j_season in range(len(comp['seasons']))]
    return {comp['name']: seasons}
  
  # Returns all the matchweeks of all the seasons of all the competitions.
  def get_matchweeks(self):
    return [self.get_matchweek_per_comp(i_comp) for i_comp in range(len(self.data))]

  # Returns everything we have. Will be used to fill the MongoDB.
  def get_data(self):
    return self.data