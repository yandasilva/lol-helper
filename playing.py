#!/usr/bin/python -tt
#-----------------------------------------------------------------------------------------
#Imports
#-----------------------------------------------------------------------------------------
import re, requests, bs4, sys
from termcolor import colored

#-----------------------------------------------------------------------------------------
#Scraps counter data from a Champion.gg HTML page
#-----------------------------------------------------------------------------------------
def scrap_counter_data(champion):

  #Requests the Champion.gg page of the desired champion
  page = requests.get('http://www.lolcounter.com/champions/' + champion)
  
  #Checks the page status and raises an exception in case of an error e.g. 404
  try:
    page.raise_for_status()
  except Exception as exc:
    print 'There was an error fetching champion data.\nMake sure you pass a valid champion name.'
    sys.exit(1)
  
  #Creates Beautiful Soup object using the champion page
  page_soup = bs4.BeautifulSoup(page.text, 'lxml')
  
  #Extracts and prints matchup name from page_soup
  elements = page_soup.find('div', {'class' : 'champion-stats'})
  champion =  elements.find('div', {'class' : 'name'}).string
  print colored('Your matchup: ' + champion, 'magenta', attrs=['bold'])
  print
  
  #Extracts and prints champs who counter the matchup from page_soup
  print colored(champion + ' is weak against: ', 'cyan', attrs=['bold'])
  elements = page_soup.find('div', {'class' : 'weak-block'})
  elements = elements.find_all('div', class_=re.compile(r'champ-block( \w+)?'))
  for champ in elements:
    print '\t' + champ.find('div', {'class':'name'}).string
  print
  
  #Extracts and prints champs who the matchup counters from page_soup
  print colored(champion + ' is strong against: ', 'cyan', attrs=['bold'])
  elements = page_soup.find('div', {'class' : 'strong-block'})
  elements = elements.find_all('div', class_=re.compile(r'champ-block( \w+)?'))
  for champ in elements:
    print '\t' + champ.find('div', {'class':'name'}).string
  print
  
#-----------------------------------------------------------------------------------------
#Scraps champion data from a Champion.gg HTML page
#-----------------------------------------------------------------------------------------
def scrap_champion_data(champion, pos):
  
  #Requests the Champion.gg page of the desired champion
  page = requests.get('http://www.champion.gg/champion/' + champion)
  
  #Checks the page status and raises an exception in case of an error e.g. 404
  try:
    page.raise_for_status()
  except Exception as exc:
    print 'There was an error fetching champion data.\nMake sure you pass a valid champion name.'
    sys.exit(1)
  
  #Creates Beautiful Soup object using the champion page
  page_soup = bs4.BeautifulSoup(page.text, 'lxml')
  
  #Extracts and prints champion name from page_soup
  elements = page_soup.find('div', {'class' : 'col-xs-12 col-sm-3 col-md-2 champion-profile'})
  champion =  elements.find('h1').string
  print colored('Your champion: ' + champion, 'magenta', attrs=['bold'])
  print


  #Extracts and prints runes from page_soup
  print colored('Runes: ', 'cyan', attrs=['bold'])
  elements = page_soup.find_all('div', {'class' : 'rune-collection'})
  elements = elements[pos].find_all('div', {'class' : 'rune-type-area'})
  for rune in elements:
    print '\t' + rune.find('strong').string + ' ' + rune.find('span').string
  print
  
  #Extracts and prints masteries from page_soup
  print colored('Mastaries: ', 'cyan', attrs=['bold'])
  elements = page_soup.find_all('div', {'class' : 'mastery-container clearfix'})
  elements = elements[pos].find_all('div', class_=re.compile(r'mastery\d'))
  for mastery_tree in elements:
    print '\t' + mastery_tree.find('div', {'class' : 'mastery-header'}).string.strip()
  print
    
  #Extracts and prints summoner spells from page_soup
  print colored('Summoner spells: ', 'cyan', attrs=['bold'])
  elements = page_soup.find_all('div', {'class' : 'summoner-wrapper'})
  elements = elements[pos].find_all('img')
  print '\t' + ' and '.join([img['tooltip'] for img in elements]) + '\n'
  
  #Extracts and prints skill order from page_soup
  print colored('Skill order: ', 'cyan', attrs=['bold'])
  elements = page_soup.find_all('div', {'class' : 'skill-order clearfix'})
  elements = elements[pos].find_all('div', {'class' : 'skill'})
  del elements[0]
  skill_keys = ['Q', 'W', 'E', 'R']
  skill_order = [None] * 18
  for i in range(len(elements)):
    levels = elements[i].find_all('div')
    del levels[0]
    for j in range(len(levels)):
      if levels[j]['class'][0] == 'selected':
        skill_order[j] = skill_keys[i]
  print '\t' + ' > '.join(skill_order) + '\n'
  
  #Extracts and prints starter items from page_soup
  print colored('Starting items: ', 'cyan', attrs=['bold'])
  elements = page_soup.find('div', {'class' : 'col-xs-12 col-sm-12 col-md-5'})
  elements = elements.find_all('div', {'class' : 'build-wrapper'})
  for item in elements[pos].find_all('a'):
    print '\t' + re.sub(r'.+\/', '', item['href'])
  print
  
  #Extracts and prints core build from page_soup
  print colored('Core build (in order of purchase):', 'cyan', attrs=['bold'])
  elements = page_soup.find('div', {'class' : 'col-xs-12 col-sm-12 col-md-7'})
  elements = elements.find_all('div', {'class' : 'build-wrapper'})
  for item in elements[pos].find_all('a'):
    print '\t' + re.sub(r'.+\/', '', item['href'])
  print
  

#-----------------------------------------------------------------------------------------
#Main function
#-----------------------------------------------------------------------------------------
def main():
  args = sys.argv[1:]
  
  #Throws exception on invalid usage
  if not args:
    print 'Usage: [--against] [--winrate] <champion name>'
    sys.exit(1)
  
  #Checks if the script was run using the --against argument
  against = False
  if args[0] == '--against':
    against = True
    del args[0]
  
  #Checks if the script was run using the --winrate argument
  pos = 0
  if args[0] == '--winrate':
    pos = 1
    del args[0]
    
  #Removes non-word characters from champion name
  champion = re.sub(r'\W', '', args[0]).lower()
  
  #Calls appropriate function according to args
  if against:
    scrap_counter_data(champion)
  else:
    scrap_champion_data(champion, pos)

#-----------------------------------------------------------------------------------------
#Main function call
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
  main()