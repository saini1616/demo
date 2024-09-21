import streamlit as st
import requests

# Replace with your actual Fixer.io API key
API_KEY = '758a064deff411664f17a22fd097aff7'
BASE_URL = f'http://data.fixer.io/api/latest?access_key={API_KEY}'


# Function to fetch conversion factor from Fixer.io
def fetch_conversion_factor(source, target, amount):
    # Fetch the latest rates
    response = requests.get(BASE_URL).json()

    if response['success']:
        rates = response['rates']
        if source not in rates or target not in rates:
            st.error('Currency not available in the rates.')
            return None, None

        # Convert source amount to EUR (if source is not EUR)
        if source != 'EUR':
            amount_in_eur = amount / rates[source]
        else:
            amount_in_eur = amount

        # Convert EUR to target currency
        converted_amount = amount_in_eur * rates[target]
        return round(converted_amount, 2), rates[target]
    else:
        st.error('Failed to retrieve exchange rate')
        return None, None


# Streamlit app interface
st.title('Currency Converter')

# Input fields for source currency, target currency, and amount
source_currency = st.selectbox('Source Currency', ['INR', 'USD', 'EUR', 'GBP', 'JPY'])
target_currency = st.selectbox('Target Currency', ['USD', 'INR', 'EUR', 'GBP', 'JPY'])
amount = st.number_input('Amount', min_value=0.0, value=500.0)

# Conversion button
if st.button('Convert'):
    # Fetch the conversion rate
    converted_amount, conversion_rate = fetch_conversion_factor(source_currency, target_currency, amount)

    if converted_amount:
        st.success(f'{amount} {source_currency} is {converted_amount} {target_currency}.')
        st.info(f'Conversion rate: 1 {source_currency} = {conversion_rate} {target_currency}')
    else:
        st.error('Conversion failed. Please try again.')
