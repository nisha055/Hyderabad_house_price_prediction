import sys
sys.path.append('/usr/local/lib/python3.9/site-packages')
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
import re

headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
url = "https://www.commonfloor.com/hyderabad-property/for-rent/apartment-ht?page="

#----------------------------grayBg_list----------------------------
# [{'label': 'Carpet Area', 'value': '2320'},
# {'label': 'Available From', 'value': 'ReadyToMove'},
# {'label': 'Floor', 'value': '9'},
# {'label': 'Bathrooms', 'value': '3'}]
def getGrayBgData(house_container): 
    summary_list = []  
    summary_list_ = house_container.find_all('div',class_ = 'graybg')
    for list in range(len(summary_list_)):
        label_all = summary_list_[list].find_all('div',class_ = 'infodata')

        for label in label_all:
            label = label.text.strip('\n').split('\n')
            list_all = {
            'label':label[0],
            'value': label[len(label)-1].replace(' ', '').split('sq.ft')[0]
            }
            summary_list.append(list_all)
    return summary_list

#----------------------------AmenitiesList----------------------------
# ['Parking', 'PowerBackup', 'SwimmingPool', 'Security']
def getInfoLineDetails(house_container):
    ul_list = []  
    li_list = []
    summary_list_ = house_container.find_all('div',class_ = 'infoline')
    for list in range(len(summary_list_)):
        #get all amenities
        ul_list = summary_list_[list].find_all('ul',class_ = 'i_l')
        ul_list = ul_list[0].text.strip('\n').replace(' ', '').split('\n')
       #get amenities not available 
        li_list = summary_list_[list].find_all('li', class_ = 'na')
        if(li_list):
            li_list = li_list[0].text.strip('\n').replace(' ', '').split('\n')
        else:
            li_list = []
    
    ul_list[:] = [x for x in ul_list if x]
    #get amenities available 
    li_list_s = set(li_list)
    AmenitiesList= [x for x in ul_list if x in li_list_s]
    return AmenitiesList
#----------------------------Check if Amenities----------------------------
def appendToAmenities(feature , featureList, amenitiesList):
    if feature in amenitiesList:
        featureList.append(1)
    else: featureList.append(0)

#----------------------------Get Flat features----------------------------
def house_features(url,headers):
    count = 0
    request = Request(url, headers=headers)
    response = urlopen(request)
    html = response.read()
    html_soup = BeautifulSoup(html , 'html.parser')
    house_container = html_soup.find_all('div', class_ = 'snb-tile' )

    for container in range(len(house_container)) :
    # for container in range(1):
        count += 1

        #----------------------------Price of the Flat----------------------------
        price_div = house_container[container].find_all('div',class_ = 'p_section')
        price_div  = price_div[0].text.strip('\n')
        Price.append(price_div)

        #----------------------------Title Div to get features----------------------------
        title_div = house_container[container].find_all('div',class_ = 'st_title')
        title_div = title_div[0].text.strip('\n')
        title_div = title_div.split('\n')[0]

        #----------------------------No of Bedrooms----------------------------
        bedroom_div = re.findall('[0-9]+', title_div)[0]
        Bedrooms.append(bedroom_div)

        #----------------------------Locality where the Flat is located----------------------------
        locality_div = title_div.split(' ')
        locality_div = locality_div[locality_div.index('in')+1:]
        locality_div = ' '.join(locality_div)
        Locality.append(locality_div)

        #----------------------------Type of Furnishing i.e Semi-Furnished or Fully Furnished----------------------------
        furnishing_ = title_div.split(' ')
        mapping = {value: index for index, value in enumerate(furnishing_)}
        index_ = mapping.get('Furnished', 0)
        if (index_ != 0) :
            furnishing_ = furnishing_[furnishing_.index('Furnished')-1:furnishing_.index('Furnished')+1]
        else:
            furnishing_ = ['NaN']
        furnishing_ = ' '.join(furnishing_)
        Furnishing.append(furnishing_)

        #----------------------------Features of Flat----------------------------
        features_list = getGrayBgData(house_container[container])

        #----------------------------Area of the house in Sqft----------------------------
        Area_= []
        Area_ = list(filter(lambda list: list['label'] == 'Carpet Area', features_list))
        if len(Area_) :
            Area_ = Area_[0]['value']
        else: Area_ = 'NaN'
        Area.append(Area_)

        #----------------------------No of Bathrooms----------------------------
        Bathrooms_= []
        Bathrooms_ = list(filter(lambda list: list['label'] == 'Bathrooms', features_list))
        if len(Bathrooms_) :
            Bathrooms_ = Bathrooms_[0]['value']
        else: Bathrooms_ = 'NaN'
        Bathrooms.append(Bathrooms_)

        #----------------------------Amenities List----------------------------
        amenitiesList = getInfoLineDetails(house_container[container])
        
        #----------------------------Parking Available----------------------------
        appendToAmenities('Parking' , Parking, amenitiesList)

        #----------------------------Power Backup available----------------------------
        appendToAmenities('PowerBackup' , Power, amenitiesList)
       
        #----------------------------Swimming Pool----------------------------
        appendToAmenities('SwimmingPool' , Pool, amenitiesList)

        #----------------------------Security----------------------------
        appendToAmenities('Security' , Security, amenitiesList)

    cols = ['Bedrooms', 'Bathrooms', 'Furnishing', 'Area', 'Price','Locality', 'Parking', 'Power' , 'Pool', 'Security']
    house_data = pd.DataFrame({'Bedrooms': Bedrooms,'Bathrooms': Bathrooms, 'Furnishing': Furnishing, 'Area': Area,'Price': Price,'Locality':Locality , 'Parking': Parking , 'Power': Power, 'Pool': Pool, 'Security': Security})[cols]
    return house_data

Bedrooms = []
Bathrooms = []
Furnishing = []
Locality = []
Area = []
Price = []
Parking = []
Power= []
Pool= []
Security=[]

for i in range(1,300):
    print(i)
    url_ = url+str(i)
    house_data = house_features(url_,headers)

# house_data = house_features(url,headers)
print('\nHOuse data count -     ',house_data.size)
print('\nHOuse data info -     \n',house_data.info)

house_data.to_csv('common_floor_data_300.csv')