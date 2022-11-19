import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

Bedrooms = []
Bathrooms = []
Furnishing = []
Tennants = []
Locality = []
Area = []
Price = []

headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
url = "https://www.magicbricks.com/property-for-rent/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment&cityName=Hyderabad"

def getSummaryList(house_container): 
    summary_list = []  
    summary_list_ = house_container.find_all('div',class_ = 'mb-srp__card__summary__list--item')
    for list in range(len(summary_list_)):
        label_all = summary_list_[list].find_all('div',class_ = 'mb-srp__card__summary--label')
        value_all = summary_list_[list].find_all('div',class_ = 'mb-srp__card__summary--value')

        AllLabel = [label_all[0].text for label in label_all]
        AllValue = [value_all[0].text for value in value_all]

        list_all = {
            'label': AllLabel[0],
            'value': AllValue[0]
        }
        summary_list.append(list_all)

    return summary_list

# summary_list structure
# [{'label': 'Furnishing', 'value': 'Semi-Furnished'}
# {'label': 'Tenant Preferred', 'value': 'Bachelors/Family'}
# {'label': 'Availability', 'value': 'Immediately'}
# {'label': 'Carpet Area', 'value': '1200 sqft'}
# {'label': 'Floor', 'value': '2 out of 5'}
# {'label': 'facing', 'value': 'East'}
# {'label': 'overlooking', 'value': 'Garden/Park'}
# {'label': 'Ownership', 'value': 'Freehold'}
# {'label': 'Bathroom', 'value': '2'}
# {'label': 'Balcony', 'value': '2'}]

def getItemDetails(summary_list, label, feature):
    item = next(item for item in summary_list if item["label"] == label)
    if(item['label'] == label):
        feature.append(item['value'])
    else:
        feature.append('NaN')

def house_price_scraper(url,headers):
    # count = 0
    request = Request(url, headers=headers)
    response = urlopen(request)
    html = response.read()
    html_soup = BeautifulSoup(html , 'html.parser')
    # print(html_soup.prettify())
    house_container = html_soup.find_all('div', class_ = 'mb-srp__card' )
    for container in range(len(house_container)) :
    #for container in range(28,29) :
        # print('\n count--------------------------------------', count)
        # count += 1
        summary_list = getSummaryList(house_container[container])

        #Price of the Flat
        price_div = house_container[container].find_all('div',class_ = 'mb-srp__card__price--amount')
        price_div = price_div[0].text
        price_div = price_div[1:]
        Price.append(price_div)
        # print('\n Price of the Flat: ', Price)

        # #No of Bedrooms
        bedroom_div = house_container[container].select_one("h2.mb-srp__card--title").text.strip()
        if(bedroom_div[0].isdigit()):
            bedroom_div = bedroom_div[0]
        else: 
            bedroom_div = '1'
        Bedrooms.append(bedroom_div)
        # print('\n No of Bedrooms: ', Bedrooms)

        # #No of Bathrooms
        bathroom_str='NaN'
        Bathroom_ = next(item for item in summary_list if item["label"] == "Bathroom")
        if(Bathroom_['label'] == 'Bathroom'):
            Bathrooms.append(Bathroom_['value'])
        else: 
            Bathrooms_  = house_container[container].find_all('div',class_ = 'mb-srp__card--desc--text')
            bath_str = Bathrooms_[0].text.split(',')
            substrings = ['Washrooms','washroom','bathrooms','bathroom', 'bath']
            result = []
            for i in range(1, len(bath_str)):
                if any(x in bath_str[i] for x in substrings):
                    result.append(bath_str[i])
            if(len(result)>0):
                bathroom_str = result[0]
                result[0].split(' ')
                Bathrooms.append(bathroom_str[0])
            else:
                Bathrooms.append('NaN')
        # print('\n No of Bathrooms: ',Bathrooms)

        # # Area of the house in Sqft
        Area_sqft='NaN'
        Area_       = house_container[container].find_all('div',class_ = 'mb-srp__card__summary--value')
        Area_sqft =''
        for i in range(len(Area_)):
            if 'sqft' in Area_[i].text:
                Area_sqft = Area_[i].text.split(' ')[0]
        if(len(Area_sqft)>0):
            Area.append(Area_sqft)
        else:
            Area.append(('NaN'))
        # print('\n Area of the house in Sqft: ', Area)
        
        # # Type of Furnishing i.e Semi-Furnished or Fully Furnished
        getItemDetails(summary_list,'Furnishing',Furnishing )
        # print('\n Type of Furnishing: ', Furnishing)

        # # Preferred Tennants i.e Bachelors or Family or Both
        getItemDetails(summary_list,'Tenant Preferred',Tennants)
        # print('\n Preferred Tennants: ', Tennants)

        # #Locality where the Flat is located

        Locality_0 = house_container[container].select_one("h2.mb-srp__card--title").text.strip()
        Locality_1 = Locality_0.split('Rent in')
        Locality.append(Locality_1[1])
        # print("\n Locality: ", Locality)
        
        
    # Making the Data frame out of the scraped columns
    cols = ['Bedrooms', 'Bathrooms', 'Furnishing', 'Tennants', 'Area', 'Price' ,'Locality']
    house_data = pd.DataFrame({'Bedrooms': Bedrooms, 'Bathrooms': Bathrooms, 'Furnishing': Furnishing, 'Tennants': Tennants, 'Area': Area, 'Price': Price, 'Locality':Locality}, index = np.arange(len(house_container)))[cols]

    #house_data = pd.DataFrame({'Bedrooms': Bedrooms, 'Bathrooms': Bathrooms, 'Furnishing': Furnishing, 'Area': Area, 'Price': Price}, index = np.arange(len(house_container)) )[cols]
    #house_data = pd.DataFrame({})
    return house_data

house_data = house_price_scraper(url,headers)
print('\nHOuse data count -     ',house_data.count())

house_data.to_csv('magics_brics_data.csv')
