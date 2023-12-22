# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

#pip install pyparsing

import pandas as pd
import panel as pn
from panel.interact import interact
pn.extension('tabulator')
import numpy as np
import hvplot.pandas 
import holoviews as hv 
from holoviews import opts 
hv.extension('bokeh')

# +
## loading or uploading the dataset into Jupyter notebook

df =pd.read_csv('/Users/yaabenewaa/Documents/Documents - YAA’s MacBook Air/Dataset/Auto Sales data.csv')
print("DataFrame created successfully:", df.head())

df.rename(columns={'ORDERNUMBER':'ORDER_NUMBER',
                   'QUANTITYORDERED':'QUANTITY_ORDERED',
                   'PRICEEACH':'PRICE_EACH',
                   'ORDERLINENUMBER':'ORDER_LINE_NUMBER',
                   'ORDERDATE':'ORDER_DATE',
                   'PRODUCTLINE':'PRODUCT_LINE',
                   'DEALSIZE':'DEAL_SIZE'}, inplace=True)

print("DataFrame after renaming columns:", df.head())

# +
## Performing Data cleaning 

df.drop_duplicates(inplace=True)
# -

df.isnull().sum()

# +
# This code is used to identify columns associated with the dataset

df.columns
# -

df['ORDER_DATE'] = pd.to_datetime(df['ORDER_DATE'])

df.dtypes

df['COUNTRY'].unique()

# +
# This syntax is used to create an interactive widget which will be used through out the code 

idf = df.interactive()
Year_Slider = pn.widgets.IntSlider(name='Date_slider', 
                                    start=2018, 
                                    end=2020, 
                                    value=2018)

Year_Slider

# -

Year_varables = pn.widgets.Select(name='SALES ACROSS THE YEARS FILTER', 
                                  options=['SALES', 'MSRP','QUANTITY_ORDERED'])

# +
countries = ['USA', 'France', 'Norway', 'Australia', 'Finland', 'UK', 'Spain',
       'Sweden', 'Singapore', 'Canada', 'Japan', 'Italy', 'Denmark',
       'Belgium', 'Philippines', 'Germany', 'Switzerland', 'Ireland']

Year_varables_pipeline = (
    idf[
        (idf.ORDER_DATE.dt.year <=Year_Slider) &
        (idf.COUNTRY.isin(countries))
    ]
    .groupby(['ORDER_DATE'])[Year_varables].sum()
    .to_frame()
    .reset_index()
    .reset_index(drop=True)

)
# -

Year_varables_pipeline

# +
# Plotting interactive hvplot in line chart

Year_plot = Year_varables_pipeline.hvplot(kind='line', x='ORDER_DATE',
                                y=Year_varables,
                                title='AUTOMOBILE SALES ACROSS THE YEARS 2018 AND 2020 ',
                                width=600,
                                height = 360,
                                
                            )
Year_plot
# -

df['PRODUCT_LINE'].unique()

Product_varables = pn.widgets.Select(name='PRODUCT LINE FILTER', 
                                  options=['SALES', 'DAYS_SINCE_LASTORDER',])

# +
product = ['Motorcycles', 'Classic Cars', 'Trucks and Buses', 
           'Vintage Cars','Planes', 'Ships', 'Trains']

Product_varables_pipeline = (
    idf[
        (idf.ORDER_DATE.dt.year <=Year_Slider) &
        (idf.PRODUCT_LINE.isin(product))
    ]
    .groupby(['PRODUCT_LINE'])[Product_varables].mean().sort_values(ascending=False)
    .to_frame()
    .reset_index()
    .reset_index(drop=True)

)

# +
# Plotting interactive hvplot in bar chart

Product_plot = Product_varables_pipeline.hvplot(kind='bar', x='PRODUCT_LINE',
                                y=Product_varables,
                                title='SALES MADE ACROSS THE YEARS',
                                width=620,
                                height = 460,
                                rot = 90
                                
                            )
                                
Product_plot
# -

df['PRICE_EACH'].unique()

# +
Price_range = list(range(1,250))

Price_varables_pipeline = (
    idf[
        (idf.ORDER_DATE.dt.year <=Year_Slider) &
        (~(idf.PRICE_EACH.isin(Price_range)))
    ]
    .groupby(['PRICE_EACH','SALES','DEAL_SIZE'])
    .size()
    .to_frame(name='count')
    .reset_index()
 
    
)


# +
# Plotting interactive hvplot using  scatter diagram

Scatterplot = Price_varables_pipeline.hvplot(x='PRICE_EACH', 
                                            y='SALES', 
                                            size=4.5, kind="scatter",
                                            by='DEAL_SIZE',
                                            legend='top_left', 
                                            height=360,
                                            title='SCATTER PLOT DISPLAYING THE DEAL SIZE ACROSS YEARS',
                                            width=600)

Scatterplot
# -

df.columns

bar_varables = pn.widgets.Select(name='COUNTRY SALES FILTER', 
                                  options=['SALES','QUANTITY_ORDERED','DAYS_SINCE_LASTORDER','MSRP'])

# +
countries = ['USA', 'France', 'Norway', 'Australia', 'Finland', 'UK', 'Spain',
       'Sweden', 'Singapore', 'Canada', 'Japan', 'Italy', 'Denmark',
       'Belgium', 'Philippines', 'Germany', 'Switzerland', 'Ireland']

bar_varables_pipeline = (
    idf[
        (idf.ORDER_DATE.dt.year <=Year_Slider) &
        (idf.COUNTRY.isin(countries))
    ]
    .groupby(['COUNTRY'])[bar_varables].sum().sort_values(ascending=False)
    .to_frame()
    .reset_index()
    .reset_index(drop=True)

)

# +
# Plotting of interactive hvplot using bar chart

bar_plot = bar_varables_pipeline.hvplot(kind='bar', x='COUNTRY',
                                y=bar_varables,
                                title='AUTOMOBILE SALES ACROSS COUNTRIES',
                                width=620,
                                height = 460,
                                rot = 90
                                
                            )
bar_plot
# -

df.columns

df['CITY'].unique()

# +
# Calculating the mean os sale and saving it as mean_of_sale

df['MEAN_OF_SALES']=df['SALES'].mean().astype(int)


# +
# Calculating the max os sale and saving it as max_of_sale

df['MAX_OF_SALE']=df['SALES'].max()
df['MAX_OF_SALE']=df['MAX_OF_SALE'].astype(int)

# +
# Calculating the min os sale and saving it as min_of_sale

df['MIN_OF_SALES']=df['SALES'].min()
df['MIN_OF_SALES']=df['MIN_OF_SALES'].astype(int)
# -

status = pn.widgets.Select(name='TABLE FILTER', options=['SALES','MEAN_OF_SALES','MAX_OF_SALE','MIN_OF_SALES'])


# +
cities = ['NYC', 'Reims', 'Paris', 'Pasadena', 'Burlingame', 'Lille',
       'Bergen', 'Melbourne', 'Newark', 'Bridgewater', 'Nantes',
       'Cambridge', 'Helsinki', 'Stavern', 'Allentown', 'Salzburg',
       'Chatswood', 'New Bedford', 'Liverpool', 'Madrid', 'Lule',
       'Singapore', 'South Brisbane', 'Philadelphia', 'Lyon', 'Vancouver',
       'Burbank', 'New Haven', 'Minato-ku', 'Torino', 'Boras',
       'Versailles', 'San Rafael', 'Nashua', 'Brickhaven', 'North Sydney',
       'Montreal', 'Osaka', 'White Plains', 'Kobenhavn', 'London',
       'Toulouse', 'Barcelona', 'San Diego', 'Bruxelles', 'Tsawassen',
       'Boston', 'Cowes', 'Oulu', 'San Jose', 'Graz', 'Makati City',
       'Marseille', 'Koln', 'Gensve', 'Reggio Emilia', 'Frankfurt',
       'Espoo', 'Dublin', 'Manchester', 'Aaarhus', 'Glendale', 'Sevilla',
       'Brisbane', 'Strasbourg', 'Las Vegas', 'Oslo', 'Bergamo',
       'Glen Waverly', 'Munich', 'Charleroi']

city_status_pipeline = (
    idf[
        (idf.ORDER_DATE.dt.year <= Year_Slider) &
        (idf.CITY.isin(cities))   
    ]
    .groupby('CITY')[status].sum().sort_values(ascending=False)
    .to_frame()
    .reset_index()
    .reset_index(drop=True)
)

# +
# Plotting interactive hvplot using bar chart

status_plot = city_status_pipeline.hvplot(x='CITY',kind='bar',
                                          size=9,
                                          y=status,
                                          title = 'CITIES AND THIER AUTOMOBILE SALES',
                                          rot=90,
                                          width=620,
                                          height = 460
                                    
                                         )
status_plot

# +
# Plotting interactive hvplot using table

status_table = city_status_pipeline.pipe(pn.widgets.Tabulator,
                                        pagination = 'remote',
                                        page_size=11,
                                        sizing_mode='stretch_width'
                                     
                                        )
status_table

# +
# Finally the interactive dashboard

template = pn.template.FastListTemplate(
    theme='default',
    title='AUTOMOBILE SALES DASHBOARD',
    sidebar=[
        pn.pane.Markdown("## A LIITLE BIT ABOUT THE DATASET USED"),
        pn.pane.Markdown("#### 'Analyzing automobile sales from 2018 to 2020, the dataset explores purchasing patterns across countries and cities. This comprehensive study delves into consumer preferences, market trends, and regional variations, offering a nuanced understanding of the dynamic automotive landscape. By dissecting this data, valuable insights emerge, guiding strategic decisions and optimizing sales approaches. The dataset meticulous analysis informs the industry on factors influencing performance, enabling a proactive response to market dynamics. Beyond raw numbers, it unveils a narrative of consumer behavior, empowering stakeholders to refine strategies and elevate overall performance in the ever-evolving realm of automobile sales."),
        pn.pane.JPG('/Users/yaabenewaa/Documents/Documents - YAA’s MacBook Air/Datasets/images.jpeg', sizing_mode='scale_both', height=200),
        pn.pane.Markdown("## FILTERS"),
        Year_Slider,
        status,Year_varables,Product_varables,bar_varables
    ],
    main=[
        pn.Row(
            pn.Column(status_table),
            pn.Column(Year_plot),
            
           
        ), 
        pn.Row(
            pn.Column(status_plot),
            pn.Column(Scatterplot.panel(width=600), margin=(136,100)),
            
        ),
         pn.Row(
            pn.Column(Product_plot),
            pn.Column(bar_plot)),
    ],
    accent_base_color="#8d5524",
    header_background="#454545",
)

# Display the template
#template.show()
template.servable();

# -


