#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, request, render_template
app = Flask(__name__)


import random
#Utilities for expressing natural time
import datetime
from dateutil.relativedelta import relativedelta


# In[11]:


import json
import requests
import pandas as pd
from datetime import datetime


# In[12]:



glarp = []
for i in range(1,100):
    url = "http://cateringdata.parliament.uk/api/Outlets/{}/2020-02-20/1".format(i)
    r = requests.get(url)
    b = r.content.decode('utf-8')
    if b == '{"Message":"An error has occurred."}':
        pass
    else:
        #print(url)
        #pprint.pprint(b)
        glarp.append(url)
print(glarp)


# In[17]:


currentdate = datetime.today().strftime('%Y-%m-%d')
glarp = ['http://cateringdata.parliament.uk/api/Outlets/1/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/3/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/5/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/21/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/23/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/29/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/30/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/31/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/32/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/33/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/34/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/35/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/36/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/37/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/38/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/39/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/40/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/41/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/42/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/43/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/44/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/45/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/46/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/47/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/48/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/49/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/50/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/51/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/52/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/55/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/56/{0}/1', 'http://cateringdata.parliament.uk/api/Outlets/57/{0}/1']
glarp = [x.replace("{0}",currentdate) for x in glarp]


# In[22]:


outlets = []
for i in glarp:
    url = i
    r = requests.get(url)
    b = r.json()
    print(b)
    outlets.append(b)
    
    


# In[31]:


eatery = []
menuitem = []
menuitemnotes = []
mitemprice = []
for o in outlets:
    try: 
        for i in o['OpeningData']['Days'][0]['Sittings']:
            if i['MealType']['Description'] in ("Lunch", "Open"):
                for l in i['MenuItems']:
                    eatery.append(o['OpeningData']['OutletName'])
                    menuitem.append(l['Description'])
                    menuitemnotes.append(l['Notes'])
                    mitemprice.append(l['Price'])
    except:
        pass


# In[32]:


print(len(eatery))
print(len(menuitem))


# In[39]:


df = pd.DataFrame(list(zip(eatery, menuitem, menuitemnotes, mitemprice)), columns=["eateries","menu items", "menu item notes", "price"])
df = df.sort_values('eateries')
df


# In[ ]:


@app.route("/")
def hello():
    return render_template('index.html', tables=[df.to_html(classes='data', header="true")])


# In[ ]:


if __name__ == "__main__":
    app.debug = True
    app.run(port=5005, use_reloader=False)

