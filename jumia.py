import pandas as pd
import numpy as np
import requests 
from bs4 import BeautifulSoup
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time



# Initialize the WebDriver using webdriver_manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url= "https://www.jumia.co.ke/catalog/?q=offer"
driver.get(url)

Headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}

response = requests.get(url, headers=Headers)
#
soup= BeautifulSoup(response.content,'html.parser')

Product = []
for item in soup.find_all('div',class_='sku_gallery'):
    product_name = item.find('span', class_='name').text.strip()
    product_price = item.find('span', class_='price').text.strip()
    original_price = item.find('span', class_='price -old -no-special').text.strip() if item.find('span', class_='price -old -no-special') else ''
    Product.append((product_name, product_price, original_price))

df = pd.DataFrame(Product, columns =['Product_name', 'product-price', 'Original_price'])

df['product-price'] = df['product-price'].str.replace('₦', '').str.replace(',', '').astype(float)
df['Original_price'] = df['Original_price'].str.replace('₦', '').str.replace(',', '').astype(float)
df['Discount'] = df['Original_price'] - df['product-price']
df['Discount Percentage'] = (df['Discount'] / df['Original_price']) * 100

# Streamlit App
st.title('Jumia Offers')
st.dataframe(df)

st.header('Top 10 Discounts')
top_discounts = df.sort_values(by='Discount Percentage', ascending=False).head(10)
st.dataframe(top_discounts)

st.header('Search for a Product')
product_name = st.text_input('Enter product name')
if product_name:
    search_results = df[df['Name'].str.contains(product_name, case=False, na=False)]
    st.dataframe(search_results)
# Close the driver
driver.quit()


# Save to CSV
df.to_csv('jumia_offers.csv', index=False)

print("Scraping completed and data saved to 'jumia_offers.csv'")   