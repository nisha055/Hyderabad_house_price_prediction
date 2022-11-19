import pandas as pd
import numpy as np

#---------------------------Read CSV with pandas----------------------------
df = pd.read_csv(r'common_floor_data_300.csv')

#---------------------------Remove duplicate rows----------------------------
cols = ['Bedrooms', 'Bathrooms', 'Furnishing', 'Area', 'Price','Locality', 'Parking', 'Power' , 'Pool', 'Security']
df_data= df.drop_duplicates(subset=cols, keep='first')
df_data.drop("Unnamed: 0", axis=1, inplace=True)
df_data.index.name='index'
df_data.reset_index(drop=True, inplace=True)

def priceCleaning(price):
    price = price.replace(',','').strip(' ')
    checkPrice = 'L' in price
    finalPrice = price
    if checkPrice:
        finalPrice = int(float(price.replace('L','').strip(' '))*100000)
    elif 'Call For Price' in price: 
        finalPrice = 1000
    else: 
        finalPrice = int(price)
    # finalPrice = float(finalPrice)/10000
    # print(i, 'i---', finalPrice)
    df_data.at[i,'Price'] = finalPrice

def furnishingCleaning(furnishing):
    if pd.isnull(furnishing):
        furn_val = 0
    elif furnishing == 'Semi Furnished':
        furn_val = 2
    elif furnishing == 'Fully Furnished':
        furn_val = 3
    else: 
        furn_val = 1
    df_data.at[i,'Furnishing'] = furn_val

for i , row in df_data.iterrows():
    #----------------------------Price column cleaning-------------------------------
    price = row.Price
    priceCleaning(price)

    #----------------------------Furnishing column cleaning-------------------------------
    # Not Furnished/ Unknown - 0
    # Semi Furnished - 1
    # Fully Furnished - 2
    furnishing = row.Furnishing
    furnishingCleaning(furnishing)

    #----------------------------Area ,Bathroom, Bedroom column cleaning-------------------------------
    area = row.Area
    if pd.isnull(area):
        area_val = 0
    else: area_val = area
    df_data.at[i,'Area'] = area_val

    bedroom = row.Bedrooms
    if pd.isnull(bedroom):
        bedroom_val = 0
    else: bedroom_val = bedroom
    df_data.at[i,'Bedrooms'] = bedroom_val

    bathroom = row.Bathrooms
    if (pd.isnull(bathroom) or bathroom == '-'):
        bathroom_val = bedroom
    else: bathroom_val = bathroom
    df_data.at[i,'Bathrooms'] = bathroom_val

    

# for p in df_data['Furnishing']:
#     print(p)

# print(df_data)
#---------------------------Write to CSV with pandas----------------------------
df_data.to_csv(r'common_floor_cleanData.csv', index=False)