
# coding: utf-8

# ## Ground Reponse Times

# In[ ]:


import numpy as np
import pandas as pd
import csv


# In[ ]:


import googlemaps
from googlemaps import convert
from googlemaps.directions import directions
from datetime import datetime

gmaps = googlemaps.Client(key='***')

## Read in csv
address_list = pd.read_csv('~/Downloads/Addresses.csv')


# In[ ]:


def get_directions(identifier, origin, destination):
    directions_result = directions(client = gmaps, 
                      origin = origin, 
                      destination = destination,
                      mode="driving", alternatives=False)

    ## Parse out from JSON
    distance = directions_result[0]['legs'][0]['distance']['value']/1609.34 ## Miles
    duration = directions_result[0]['legs'][0]['duration']['value']/60 ## Minutes
    start_address = directions_result[0]['legs'][0]['start_address']
    end_address = directions_result[0]['legs'][0]['end_address']
    start_location_lat = directions_result[0]['legs'][0]['start_location']['lat']
    start_location_long = directions_result[0]['legs'][0]['start_location']['lng']
    end_location_lat = directions_result[0]['legs'][0]['end_location']['lat']
    end_location_long = directions_result[0]['legs'][0]['end_location']['lng']
    
    ## Create a dataframe of the values
    directions_DF = pd.DataFrame(data = {'id': identifier,
                                   'origin': origin,
                                   'destination': destination,
                                   'distance': distance,
                                   'duration': duration,
                                   'start_address': start_address,
                                   'end_address': end_address,
                                   'start_location_lat': start_location_lat,
                                   'start_location_long': start_location_long,
                                   'end_location_lat': end_location_lat,
                                   'end_location_long': end_location_long},
                           columns = ['id','origin','destination','distance','duration','start_address','end_address','start_location_lat',
                                      'start_location_long','end_location_lat','end_location_long'], index=[identifier])
    return(directions_DF)


# In[ ]:


directions_full = pd.DataFrame()


# In[ ]:


for i in range(len(address_list)):
        print(address_list.origin[i])
        try:
            directions_df = get_directions(identifier = address_list.unique_id[i],
                                           origin = address_list.origin[i],
                                           destination = address_list.destination[i])
            directions_full = directions_full.append(pd.DataFrame(data = directions_df))
        except:
            print("This address could not be found")

directions_full = directions_full.reset_index(drop=True)


# In[ ]:


directions_full.head()


# In[ ]:


directions_full.to_csv(path_or_buf = "~/Downloads/Google_Address_Distances.csv")

