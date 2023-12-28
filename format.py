import pandas as pd
import re

result_df = pd.read_csv('cad-scrap-results.csv')
result_df['cardName']=result_df['cardName'].str.title().str.strip()
result_df = result_df.sort_values(by='cardName')

bank_mapping = {
    'American Express': 'Amex',
    'Bmo': 'BMO',
    'Brim': 'Brim',
    'Cibc': 'CIBC',
    'Td': 'TD',
    'Manulifebank': 'Manulife',
    'Mbna': 'MBNA',
    'National Bank': 'NBC',
    'Neo': 'Neo',
    'Presidents Choice': 'PC Financial',
    'Rbc': 'RBC',
    'Tangerine': 'Tangerine',
    'Scotiabank': 'Scotiabank',
    'Simplii': 'Simplii',
    'Vancity': 'Vancity'}

cpp_mapping = {
    'aeroplan': 0.021,
    'air miles': 0.01053, 
    'aventura': 0.0125, 
    'avion': 0.0233, 
    'avios': 0.02,
    'bmo rewards': 0.0067,
    'canadian tire money': 1, 
    'cash back': 1, 
    'mbna rewards': 0.01,
    'marriott bonvoy': 0.008, 
    'membership rewards': 0.022, 
    'pc optimum': 0.001, 
    'scene': 0.01,
    'td rewards': 0.005, 
    'westjet dollars': 1
}

def determine_bank(card_name):
    if "Scotiabank" in card_name:
        return "Scotiabank"
    elif "American Express" in card_name:
        return "Amex"
    for bank in bank_mapping:
        if bank in card_name:
            return bank_mapping[bank]
    return "Others"

def calculate_return(row):
    try:
        if row['Reward Program'] in ['Canadian Tire Money', 'Cash Back', 'Westjet Dollars']:
            return ((row['WB Pts'] + row['AF/Rebate'])/ row['MSR']) * 100
        else:
            return ((row['WB Pts'] + row['Spend Pts']) * row['cpp'] + row['AF/Rebate']) / row['MSR'] * 100
    except ZeroDivisionError:
        return ((row['WB Pts'] + row['Spend Pts']) * row['cpp'] + row['AF/Rebate']) * 100

def format_bank_rewards(df):
    df1 = pd.DataFrame()

    df1['Institution'] = df['cardName'].apply(determine_bank)
    df1['Card Name'] = df['cardName']

    scotia_rows = df1['Institution'] == 'Scotiabank'
    non_scotia_rows = df1['Institution'] != 'Scotiabank'

    for bank, abbreviation in bank_mapping.items():
        df1.loc[scotia_rows, 'Card Name'] = df1.loc[scotia_rows, 'Card Name'].str.replace('American Express', 'Amex')
        df1.loc[scotia_rows, 'Card Name'] = df1.loc[scotia_rows, 'Card Name'].str.replace('Scotiabank', '').str.strip()
        df1.loc[non_scotia_rows, 'Card Name'] = df1.loc[non_scotia_rows, 'Card Name'].str.replace(bank, '').str.strip()
    
    df1 = df1[df1['Institution'] != 'Vancity']

    df1['FYF'] = df['annualFee'].str.contains('(FYF)', case=False)
    df1['AF'] = df['annualFee'].replace([r'\(FYF\)', r'\$'], ['', ''], regex=True).astype(float)

    df1[['WB Pts', 'Reward Program']] = df['cardReward'].str.extract(r'([\d,]+)\s*([a-zA-Z\s]+)').fillna(value={0: '0', 1: ''})
    df1['Reward Program'] = df1['Reward Program'].str.title().str.strip()
    df1['WB Pts'] = df1['WB Pts'].str.replace(',', '').astype(int)
    df1['Rebate'] = df['cardReward'].str.extract(r'\$\s*(\d+)').fillna(0).astype(int)
    df1['AF/Rebate'] = df1.apply(lambda row: row['Rebate'] if row['FYF'] else row['Rebate'] - row['AF'], axis=1)

    df1['MSR'] = df['minSpend'].replace(to_replace=[r'\$', ','], value='', regex=True).astype(int)
    df1['Spend Pts'] = df1['MSR']

    df1['cpp'] = df1['Reward Program'].str.strip().str.lower().map(cpp_mapping)
    df1['cpp'] = df1['cpp'].fillna(0)

    df1['% Return'] = df1.apply(calculate_return, axis=1)
    df1['$ Return'] = df1.apply(lambda row: (row['% Return'] / 100) * row['MSR'] if row['MSR'] != 0 else (row['% Return'] / 100), axis=1)

    df1['$ Return'] = df1['$ Return'].map('${:,.2f}'.format)
    df1['% Return'] = df1['% Return'].map('{:.2f}%'.format)

    return df1

if __name__ == "__main__":
    formatted_df = format_bank_rewards(result_df)
    formatted_df.to_csv('formatted_file.csv', index=False)