import yfinance as yf
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px



######################################################################## Functions to extract financials
def get_Assets(balancesheet):

    #extract current assets
    current_Assets_columns=['Cash And Cash Equivalents','Other Short Term Investments','Accounts Receivable','Inventory','Other Current Assets','Current Assets']
    current_Assets=balancesheet[current_Assets_columns]
    #extract noncurrent assets
    non_current_Assets_columns=['Net PPE','Investments And Advances', 'Other Non Current Assets','Total Non Current Assets']
    non_current_assets=balancesheet[non_current_Assets_columns]
    #extract total assets
    total_Assets_columns=['Total Assets']
    total_Assets=balancesheet[total_Assets_columns]
    return current_Assets, non_current_assets,total_Assets

def get_Liabilities(balancesheet):
    #extract current  liabilies
    current_liabilities_columns=[  'Other Current Liabilities',
       'Current Deferred Liabilities',
       'Current Debt And Capital Lease Obligation',
       
       'Payables And Accrued Expenses','Current Liabilities'
       ]
    current_Liabilities=balancesheet[current_liabilities_columns]
    #extract noncurrent liabilities
    non_current_Liabilities_columns=[ 'Other Non Current Liabilities','Long Term Debt And Capital Lease Obligation','Total Non Current Liabilities Net Minority Interest']
    non_current_Liabilities=balancesheet[non_current_Liabilities_columns]
    # total liabilities
    total_Liabilities_columns=['Total Liabilities Net Minority Interest']
    total_Liabilities=balancesheet[total_Liabilities_columns]

    return current_Liabilities, non_current_Liabilities,total_Liabilities

def get_Equity(balancesheet):
    #extract equity
    equity_columns=['Total Equity Gross Minority Interest']
    equity=balancesheet[equity_columns]
    return equity


def extract_balance_sheet(ticker):
    stock=yf.Ticker(ticker)
# extract balance sheet for the company
    balancesheet=stock.balancesheet.T
    #extract Assets dataframes
    current_Assets, non_current_Assets,total_Assets=get_Assets(balancesheet)
    #extract Liabilities dataframes
    current_Liabilities,non_current_Liabilities,total_Liabilities=get_Liabilities(balancesheet)
    # extract equity dataframe
    total_ShareHolderEquity=get_Equity(balancesheet)
    return current_Assets, non_current_Assets,total_Assets,current_Liabilities,non_current_Liabilities,total_Liabilities,total_ShareHolderEquity





def get_TotalRevenue(ticker):
    financial=yf.Ticker(ticker)
    financial=financial.financials.T
    total_Revenue = pd.DataFrame({
    'Total Revenue': financial['Total Revenue']
    
})
    return total_Revenue


def get_Financial(ticker):
       stock=yf.Ticker(ticker)
       # extract balance sheet for the company
       financial=stock.financials.T
       financialcolumns=['Total Revenue','Gross Profit', 'Cost Of Revenue','Operating Income', 'Operating Expense','Other Non Operating Income Expenses',
       'Tax Provision', 'Pretax Income','Net Income','Diluted NI Availto Com Stockholders','Net Interest Income', 'Interest Expense', 'Interest Income',
       'Normalized Income',
       'Net Income From Continuing And Discontinued Operation',
       'Total Expenses', 
       'Diluted Average Shares', 'Basic Average Shares', 'Diluted EPS',
       'Basic EPS',
       'Other Income Expense','Tax Effect Of Unusual Items', 'Tax Rate For Calcs',
       'Normalized EBITDA',
       'Net Income From Continuing Operation Net Minority Interest',
       'Reconciled Depreciation', 'Reconciled Cost Of Revenue', 'EBITDA',
       'EBIT',]
       financial=financial[financialcolumns]
       return financial


def get_MultipleFinancial(listoftickers):
    df_list=[]
    for i in range(len(listoftickers)):
        df=get_Financial(listoftickers[i])
        df['Company'] = [listoftickers[i]] * len(df)
        df_list.append(df) 
    multiple_Financial = pd.concat(df_list, ignore_index=False)
    return multiple_Financial     


def get_CashFLow(ticker):
       stock=yf.Ticker(ticker)
       # extract balance sheet for the company
       cashflow=stock.cashflow.T
       cashflowcolumns=['Free Cash Flow', 'Repurchase Of Capital Stock', 'Repayment Of Debt',
              'Issuance Of Debt', 'Capital Expenditure','End Cash Position','Financing Cash Flow','Investing Cash Flow','Operating Cash Flow']
       cashflow=cashflow[cashflowcolumns]
       return cashflow


def get_MultipleCashFlow(listoftickers):
    df_list=[]
    for i in range(len(listoftickers)):
        df=get_CashFLow(listoftickers[i])
        df['Company'] = [listoftickers[i]] * len(df)
        df_list.append(df)
    
    multiple_CahsFlow = pd.concat(df_list, ignore_index=False)

    return multiple_CahsFlow      


def get_CompleteBalancesheet(ticker):
        
        current_Assets, non_current_Assets,total_Assets,current_Liabilities,non_current_Liabilities,total_Liabilities,total_ShareHolderEquity=extract_balance_sheet(ticker)
        result_df = pd.concat([current_Assets, non_current_Assets, total_Assets,
                          current_Liabilities, non_current_Liabilities, total_Liabilities,
                          total_ShareHolderEquity], axis=1)
        return result_df


def get_MultipleBalanceSheet(listoftickers):
    df_list=[]
    for i in range(len(listoftickers)):
        df=get_CompleteBalancesheet(listoftickers[i])
        df['Company'] = [listoftickers[i]] * len(df)
        df_list.append(df)
    
    multiple_BalanceSheets = pd.concat(df_list, ignore_index=False)

    return multiple_BalanceSheets      



######################################################################## Functions to calculate Ratios


def get_CurrentRatio(current_Assets,current_Liabilities):
    """This function calculates the Current Ratio for each year in the balance sheet
    """
    current_Ratio = pd.DataFrame({
    'Current Ratio': current_Assets['Current Assets'] / current_Liabilities['Current Liabilities'],
    
})
    return current_Ratio



def get_DebttoEquityRatio(total_Liabilities, total_ShareHolderEquity):
    """This function calculates the Debt to Equity Ratio for each year in the balance sheet"""
    
    debt_to_equity_ratio = pd.DataFrame({
        'Debt_to_Equity_Ratio': total_Liabilities['Total Liabilities Net Minority Interest'] / total_ShareHolderEquity['Total Equity Gross Minority Interest']
    })
    
    return debt_to_equity_ratio




def get_EquityMultiplierRatio(total_Assets,total_ShareHolderEquity):
    """This function calculates the equity multiplier ratio for each year in the balance sheet"""
    
    equity_multiplier_ratio = pd.DataFrame({
        'Equity_Multiplier_Ratio': total_Assets['Total Assets'] / total_ShareHolderEquity['Total Equity Gross Minority Interest']
    })
    return equity_multiplier_ratio



def get_DebttoAssetsRatio(total_Liabilities,total_Assets):
    """This function calculates the Debt to assets ratio for each year in the balance sheet"""
    
    debt_to_assets_ratio = pd.DataFrame({
        'Debt_To_Assets_Ratio':total_Liabilities['Total Liabilities Net Minority Interest'] /total_Assets['Total Assets']
    })
    return debt_to_assets_ratio





def get_WholeRatio(listoftickers):
    current_ratio_comparison,debt_to_equity_ratio_comparison,equity_multiplier_ratio_comparison,debt_to_assets_ratio_comparison,asset_turnover_ratio_comparison,cash_flow_to_net_income_Ratio_comparison,operating_cash_flow_Ratio_comparison= get_RatiosofMultipleCompanies(listoftickers)
    dfs = [current_ratio_comparison,debt_to_equity_ratio_comparison,equity_multiplier_ratio_comparison,debt_to_assets_ratio_comparison,asset_turnover_ratio_comparison,cash_flow_to_net_income_Ratio_comparison,operating_cash_flow_Ratio_comparison]
    Ratio_df = pd.concat([df.set_index('Company', append=True) for df in dfs], axis=1).reset_index('Company')
    return Ratio_df


def get_AssetTurnoverRatio(total_Revenue,total_Assets):
    """This function calculates the Asset Turnover Ratio Ratio for each year in the balance sheet
    """
    asset_turnover_Ratio = pd.DataFrame({
    'Asset Turnover Ratio': total_Revenue['Total Revenue']/ total_Assets['Total Assets']
    
})
    return asset_turnover_Ratio


def get_CashFlowtoNetIncomeRatio(cashflow,financial):
    """This function calculates the CashFlowtoNetIncomeRatio for each year in the balance sheet
    """
    cash_flow_to_net_income_Ratio = pd.DataFrame({
    'Cash Flow to Income Ratio': cashflow['Operating Cash Flow']/ financial['Net Income']
    
})
    return cash_flow_to_net_income_Ratio

def get_OperatingCashFlowRatio(cashflow,current_Liabilities):
    """This function calculates the Operating Cashflow Ratiofor each year in the balance sheet
    """
    operating_cash_flow_Ratio = pd.DataFrame({
    'Operating Cash Flow Ratio': cashflow['Operating Cash Flow']/ current_Liabilities['Current Liabilities']
    
})
    return operating_cash_flow_Ratio

def get_RatiosofMultipleCompanies(listoftickers):
    """The purpose of this function is to calculate the different ratios for a series of companies and concatenate the results
    """
    #create empty list to store the different dfs of ratios
    current_ratio_list=[]
    debt_to_equity_ratio_list=[]
    equity_multiplier_ratio_list=[]
    debt_to_assets_ratio_list=[]
    asset_turnover_Ratio_list=[]
    cash_flow_to_net_income_Ratio_list=[]
    operating_cash_flow_Ratio_list=[]
    for i in range(len(listoftickers)):
        #generate balance sheets for each ticker
       
        current_Assets, non_current_Assets,total_Assets,current_Liabilities,non_current_Liabilities,total_Liabilities,total_ShareHolderEquity=extract_balance_sheet(listoftickers[i])
        total_Revenue=get_TotalRevenue(listoftickers[i])
        financial=get_Financial(listoftickers[i])
        cashflow=get_CashFLow(listoftickers[i])
        
        #get ratios
        current_Ratio=get_CurrentRatio(current_Assets,current_Liabilities)
        debt_to_equity_Ratio=get_DebttoEquityRatio(total_Liabilities, total_ShareHolderEquity)
        equity_multiplier_Ratio= get_EquityMultiplierRatio(total_Assets,total_ShareHolderEquity)
        debt_to_assets_Ratio= get_DebttoAssetsRatio(total_Liabilities,total_Assets)
        asset_turnover_Ratio=get_AssetTurnoverRatio(total_Revenue,total_Assets)
        cash_flow_to_net_income_Ratio=get_CashFlowtoNetIncomeRatio(cashflow,financial)
        operating_cash_flow_Ratio=get_OperatingCashFlowRatio(cashflow,current_Liabilities)
        #generate new column to identify the company's ratios
        current_Ratio['Company'] = [listoftickers[i]] * len(current_Ratio)
        current_ratio_list.append(current_Ratio)
        debt_to_equity_Ratio['Company'] = [listoftickers[i]] * len(current_Ratio)
        debt_to_equity_ratio_list.append(debt_to_equity_Ratio)
        equity_multiplier_Ratio['Company'] = [listoftickers[i]] * len(current_Ratio)
        equity_multiplier_ratio_list.append(equity_multiplier_Ratio)
        debt_to_assets_Ratio['Company'] = [listoftickers[i]] * len(current_Ratio)
        debt_to_assets_ratio_list.append(debt_to_assets_Ratio)
        asset_turnover_Ratio['Company'] = [listoftickers[i]] * len(current_Ratio)
        asset_turnover_Ratio_list.append(asset_turnover_Ratio)
        cash_flow_to_net_income_Ratio['Company'] = [listoftickers[i]] * len(current_Ratio)
        cash_flow_to_net_income_Ratio_list.append(cash_flow_to_net_income_Ratio)
        operating_cash_flow_Ratio['Company'] = [listoftickers[i]] * len(current_Ratio)
        operating_cash_flow_Ratio_list.append(operating_cash_flow_Ratio)



    #concat all dfs of every ratio
    current_ratio_comparison = pd.concat(current_ratio_list, ignore_index=False)
    debt_to_equity_ratio_comparison = pd.concat(debt_to_equity_ratio_list, ignore_index=False)
    equity_multiplier_ratio_comparison = pd.concat(equity_multiplier_ratio_list, ignore_index=False)
    debt_to_assets_ratio_comparison=pd.concat(debt_to_assets_ratio_list, ignore_index=False)
    asset_turnover_ratio_comparison=pd.concat(asset_turnover_Ratio_list, ignore_index=False)
    cash_flow_to_net_income_Ratio_comparison=pd.concat(cash_flow_to_net_income_Ratio_list, ignore_index=False)
    operating_cash_flow_Ratio_comparison=pd.concat(operating_cash_flow_Ratio_list, ignore_index=False)


    return current_ratio_comparison,debt_to_equity_ratio_comparison,equity_multiplier_ratio_comparison,debt_to_assets_ratio_comparison,asset_turnover_ratio_comparison,cash_flow_to_net_income_Ratio_comparison,operating_cash_flow_Ratio_comparison

def get_RelativeDifferenceofRatio(listoftickers):
    """The purpose of this function is to calculate the relative difference of a series of companies by year to compare how each performed in the difference metrics in comparison
    to each other"""
    current_ratio_comparison,debt_to_equity_ratio_comparison,equity_multiplier_ratio_comparison,debt_to_assets_ratio_comparison,asset_turnover_ratio_comparison,cash_flow_to_net_income_Ratio_comparison,operating_cash_flow_Ratio_comparison= get_RatiosofMultipleCompanies(listoftickers)
    dflist=[current_ratio_comparison,debt_to_equity_ratio_comparison,equity_multiplier_ratio_comparison,debt_to_assets_ratio_comparison,asset_turnover_ratio_comparison,cash_flow_to_net_income_Ratio_comparison,operating_cash_flow_Ratio_comparison]
    ratio_list=['Current Ratio','Debt_to_Equity_Ratio','Equity_Multiplier_Ratio','Debt_To_Assets_Ratio','Asset Turnover Ratio','Cash Flow to Income Ratio', 'Operating Cash Flow Ratio']
    new_df_list=[]
    for i in range(len(dflist)):
        df=dflist[i]
        df['Year'] = df.index.year
        df['Comparison Ratio']=df.groupby('Year')[ratio_list[i]].transform('mean')
        df["Relative_Difference"]=(df[ratio_list[i]]/df['Comparison Ratio'])-1
        new_df_list.append(df)
    
    current_ratio_relative_difference=new_df_list[0]
    debt_to_equity_ratio_relative_difference=new_df_list[1]
    equity_multiplier_ratio_relative_difference=new_df_list[2]
    debt_to_assets_ratio_relative_difference=new_df_list[3]
    asset_turnover_ratio_relative_difference=new_df_list[4]
    cash_flow_to_net_income_relative_difference=new_df_list[5]
    operating_cash_flow_Ratio_relative_difference=new_df_list[5]



    return current_ratio_relative_difference,debt_to_equity_ratio_relative_difference,equity_multiplier_ratio_relative_difference,debt_to_assets_ratio_relative_difference,asset_turnover_ratio_relative_difference,cash_flow_to_net_income_relative_difference,operating_cash_flow_Ratio_relative_difference


def get_GrossProfitMargin(financial):
    """This function calculates the Gross Profit Margin for each year in the balance sheet
    """
    gross_profit_Margin = pd.DataFrame({
    'Gross Profit Margin': (financial['Gross Profit']/ financial['Total Revenue'])*100
    
})
    return gross_profit_Margin

def get_OperatingProfit_Margin(financial):
    """This function calculates the Operating Profit Margin for each year in the balance sheet
    """
    operating_profit_Margin = pd.DataFrame({
    'Operating Profit Margin': (financial['EBIT']/ financial['Total Revenue'])*100
    
})
    return operating_profit_Margin


def get_MultipleProfitabilityRatios(listoftickers):
    
    listofdfs=[]
    for i in range(len(listoftickers)):
        financial=get_Financial(listoftickers[i])
        gross_profit_Margin=get_GrossProfitMargin(financial)
        gross_profit_Margin = gross_profit_Margin.sort_index()
        gross_profit_Margin['Gross Profit Margin YoY Change']=round(gross_profit_Margin['Gross Profit Margin'].pct_change() * 100,2)
        operating_profit_Margin=get_OperatingProfit_Margin(financial)
        operating_profit_Margin = operating_profit_Margin.sort_index()
        operating_profit_Margin['Operating Profit Margin YoY Change'] = round(operating_profit_Margin['Operating Profit Margin'].pct_change() * 100,2)
        operating_profit_Margin['Company'] = [listoftickers[i]] * len(operating_profit_Margin)
        df=pd.concat([operating_profit_Margin,gross_profit_Margin],axis=1)
        listofdfs.append(df)
    
    profitabilityRatios = pd.concat(listofdfs, axis=0)
    return profitabilityRatios


def get_RankingTableProfitability(profitability):
    df = profitability.sort_index()
    # Extract the last two years
    last_two_years = df[df.index >= (df.index.max() - pd.DateOffset(years=2))]
    # Calculate the mean Gross Profit Margin YoY Change for each company
    gross_proffitmean_yoy_change_by_company = last_two_years.groupby('Company')['Gross Profit Margin YoY Change'].mean()
    gross_proffitmean_yoy_change_by_company = gross_proffitmean_yoy_change_by_company.reset_index()
    gross_proffitmean_yoy_change_by_company = gross_proffitmean_yoy_change_by_company.sort_values(by='Gross Profit Margin YoY Change', ascending=False)
    operating_proffitmean_yoy_change_by_company=last_two_years.groupby('Company')['Operating Profit Margin YoY Change'].mean()
    operating_proffitmean_yoy_change_by_company = operating_proffitmean_yoy_change_by_company.reset_index()
    operating_proffitmean_yoy_change_by_company = operating_proffitmean_yoy_change_by_company.sort_values(by='Operating Profit Margin YoY Change', ascending=False)

    return gross_proffitmean_yoy_change_by_company,operating_proffitmean_yoy_change_by_company
    


def get_MultipleLiquidityRatios(listoftickers):
    listofdfs=[]
    for i in range(len(listoftickers)):
        current_Assets, non_current_Assets,total_Assets,current_Liabilities,non_current_Liabilities,total_Liabilities,total_ShareHolderEquity=extract_balance_sheet(listoftickers[i])
        cashflow=get_CashFLow(listoftickers[i])
        current_Ratio=get_CurrentRatio(current_Assets,current_Liabilities)
        current_Ratio = current_Ratio.sort_index()
        current_Ratio['Current Ratio YoY Change']=round(current_Ratio['Current Ratio'].pct_change() * 100,2)
        operating_cash_flow_Ratio=get_OperatingCashFlowRatio(cashflow,current_Liabilities)
        operating_cash_flow_Ratio = operating_cash_flow_Ratio.sort_index()
        operating_cash_flow_Ratio['Operating Cash Flow Ratio YoY Change']=round(operating_cash_flow_Ratio['Operating Cash Flow Ratio'].pct_change() * 100,2)
        operating_cash_flow_Ratio['Company'] = [listoftickers[i]] * len(operating_cash_flow_Ratio)
        df=pd.concat([current_Ratio,operating_cash_flow_Ratio],axis=1)
        listofdfs.append(df)        
    liquidityRatios = pd.concat(listofdfs, axis=0)
    return liquidityRatios


def get_RankingTableLiquidity(liquidity):
    df = liquidity.sort_index()
    # Extract the last two years
    last_two_years = df[df.index >= (df.index.max() - pd.DateOffset(years=2))]
    # Calculate the mean Gross Profit Margin YoY Change for each company
    current_ratio_Ranking = last_two_years.groupby('Company')['Current Ratio'].mean()
    current_ratio_Ranking = current_ratio_Ranking.reset_index()
    current_ratio_Ranking = current_ratio_Ranking.sort_values(by='Current Ratio', ascending=False)
    operating_cash_flow_ratio_Ranking=last_two_years.groupby('Company')['Operating Cash Flow Ratio'].mean()
    operating_cash_flow_ratio_Ranking = operating_cash_flow_ratio_Ranking.reset_index()
    operating_cash_flow_ratio_Ranking = operating_cash_flow_ratio_Ranking.sort_values(by='Operating Cash Flow Ratio', ascending=False)
    return current_ratio_Ranking,operating_cash_flow_ratio_Ranking

def get_MultipleEfficiencyRatios(listoftickers):
    listofdfs=[]
    for i in range(len(listoftickers)):
        cashflow=get_CashFLow(listoftickers[i])
        financial=get_Financial(listoftickers[i])

        cash_flow_to_net_income_Ratio=get_CashFlowtoNetIncomeRatio(cashflow,financial)
        cash_flow_to_net_income_Ratio = cash_flow_to_net_income_Ratio.sort_index()
        cash_flow_to_net_income_Ratio['Cash Flow to Income Ratio YoY Change']=round(cash_flow_to_net_income_Ratio['Cash Flow to Income Ratio'].pct_change() * 100,2)
        cash_flow_to_net_income_Ratio['Company'] = [listoftickers[i]] * len(cash_flow_to_net_income_Ratio)
        listofdfs.append(cash_flow_to_net_income_Ratio)

    efficiency = pd.concat(listofdfs, axis=0)
    return efficiency

def get_RankingTableEfficiency(efficiency):
    df = efficiency.sort_index()
    # Extract the last two years
    last_two_years = df[df.index >= (df.index.max() - pd.DateOffset(years=2))]
    # Calculate the mean Gross Profit Margin YoY Change for each company
    cash_flow_to_net_income_Ratio_Ranking = last_two_years.groupby('Company')['Cash Flow to Income Ratio'].mean()
    cash_flow_to_net_income_Ratio_Ranking = cash_flow_to_net_income_Ratio_Ranking.reset_index()
    cash_flow_to_net_income_Ratio_Ranking = cash_flow_to_net_income_Ratio_Ranking.sort_values(by='Cash Flow to Income Ratio', ascending=False)

    asset_turnover_Ratio_Ranking=last_two_years.groupby('Company')['Cash Flow to Income Ratio YoY Change'].mean()
    asset_turnover_Ratio_Ranking = asset_turnover_Ratio_Ranking.reset_index()
    asset_turnover_Ratio_Ranking = asset_turnover_Ratio_Ranking.sort_values(by='Cash Flow to Income Ratio YoY Change', ascending=False)
    return cash_flow_to_net_income_Ratio_Ranking,asset_turnover_Ratio_Ranking
    




# Streamlit Functions

def plot_multiple_columns_lines(df, columns_to_plot):
    # Get unique values in the 'company' column
    companies = df['Company'].unique()

    # Create a new DataFrame for Plotly Express
    plotly_df = pd.DataFrame()

    # Add columns for Plotly Express DataFrame
    for company in companies:
        for column in columns_to_plot:
            company_df = df[(df['Company'] == company) & (df[column])]
            plotly_df = pd.concat([plotly_df, pd.DataFrame({
                'Date': company_df.index,
                'Company - Column': [f"{company} - {column}"] * len(company_df),
                'Value': company_df[column].tolist()
            })])

    # Create an interactive line chart using Plotly Express
    fig = px.line(plotly_df, x='Date', y='Value', color='Company - Column', labels={'Value': 'Price'}, markers=True,  # Add markers to the lines
                  line_shape='linear')

    # Set layout options for better aesthetics
    fig.update_layout(
        title='Balance Sheet Trend Graph',
        xaxis_title='Date',
        yaxis_title='Value',
        legend_title='Company - Balance Sheet Attribute',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(l=0, r=0, t=40, b=0),
        template='xgridoff'  # You can change the template as per your preference
    )

    # Show the Plotly Express figure using Streamlit
    st.plotly_chart(fig)



@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')




def generate_tabs(selected_ticker_symbols):

    balance_sheet_tab, financials_tab, cash_flow_tab = st.tabs(["Balance Sheet", "Financials", "Cash Flow"])

    with balance_sheet_tab:
    
        # Balance Sheet Subsection
        st.subheader("Balance Sheet Information")
        Balance_Sheet=get_MultipleBalanceSheet(selected_ticker_symbols)
        # generate graph of basic information in a balance sheet
        selected_columns = st.multiselect('Please select which Attributes of the Balance Sheet you wish to plot:', Balance_Sheet.columns.tolist(), default=['Total Assets','Total Liabilities Net Minority Interest'])
        # Plot line chart
        if selected_columns:
            plot_multiple_columns_lines(Balance_Sheet,selected_columns)

        balance_sheet_csv = convert_df(Balance_Sheet)

        st.download_button(
            label="Download Balance Sheet as CSV",
            data=balance_sheet_csv,
            file_name='BalanceSheet.csv',
            mime='text/csv',
        )

    with financials_tab:
        # Balance Sheet Subsection
        st.subheader("Financial Statement Information")
        financial_statement=get_MultipleFinancial(selected_ticker_symbols)
        # generate graph of basic information in a balance sheet
        selected_columns_financial = st.multiselect('Please select which Attributes of the Financial Statement you wish to plot:', financial_statement.columns.tolist(), default=['Net Income','Cost Of Revenue'])
        # Plot line chart
        if selected_columns_financial:
            plot_multiple_columns_lines(financial_statement,selected_columns_financial)

        financial_statement_csv = convert_df(financial_statement)

        st.download_button(
            label="Download Financial Statement as CSV",
            data=financial_statement_csv,
            file_name='FinancialStatement.csv',
            mime='text/csv',
        )

    with cash_flow_tab:
            # Balance Sheet Subsection
        st.subheader("Cash Flow Statement Information")
        cash_flow_statement=get_MultipleCashFlow(selected_ticker_symbols)
        # generate graph of basic information in a balance sheet
        selected_columns_cash_flow = st.multiselect('Please select which Attributes of the Cash Flow Statement you wish to plot:', cash_flow_statement.columns.tolist(), default=['Free Cash Flow','Operating Cash Flow'])
        # Plot line chart
        if selected_columns_cash_flow:
            plot_multiple_columns_lines(cash_flow_statement,selected_columns_cash_flow)

        cash_flow_statement_csv = convert_df(cash_flow_statement)

        st.download_button(
            label="Download Cash FLow Statement as CSV",
            data=cash_flow_statement_csv,
            file_name='CashFlowStatement.csv',
            mime='text/csv',
        )




def generate_ratio_tabs(selected_ticker_symbols):
    st.header("Important Ratio Information")
    Profitability_Ratios,Liquidity_Ratios ,Efficiency_Ratios,Whole_Ratio = st.tabs(["Profitability Ratios","Liquidity Ratios" ,"Efficiency Ratios","Complete Ratio Sheet"])

    with Profitability_Ratios:
        st.subheader("Profitability Ratio Information")
        profitability_Ratios=get_MultipleProfitabilityRatios(selected_ticker_symbols)
        profitability_list=profitability_Ratios.columns.tolist()
        if 'Company' in profitability_list:
            profitability_list.remove('Company')

        selected_columns_profitability = st.multiselect('Please select which Ratios you wish to plot:',profitability_list, default=['Operating Profit Margin','Gross Profit Margin'])
        # Plot line chart
        if selected_columns_profitability:
            plot_multiple_columns_lines(profitability_Ratios,selected_columns_profitability)


        gross_proffitmean_yoy_change_by_company,operating_proffitmean_yoy_change_by_company=get_RankingTableProfitability(profitability_Ratios)
        gross_tab,operating_tab = st.tabs(["Gross Profit Margin Ranking", "Operating Profit Margin Ranking"])
        with gross_tab:
            st.header("Gross Profit Margin Ranking")
            st.write("In the following table you will see the ranking of the companies that performed the best in the last two years according to the Gross Profit Margin")
            st.latex(r'Gross Profit Margin= \frac{Gross Profit}{Revnue}')
            st.write('The gross profit margin looks at the company’s profitability of production. It reveals whether a business sells its products at higher prices than their actual cost. The higher the gross margin, the more money there is to cover other expenses.')
            st.subheader('Ranked from Best Performing to Worse Performing')
            st.table(gross_proffitmean_yoy_change_by_company)

        with operating_tab:
            st.header("Operating Profit Margin Ranking")
            st.write("In the following table you will see the ranking of the companies that performed the best in the last two years according to the Operating Profit Margin")
            st.latex(r'Operating Profit Margin= \frac{EBIT}{Revnue}')
            st.write('The operating profit margin—earnings before interest and taxes (EBIT)—examines the business model’s profitability after accounting for production costs and running the business.The higher the operating margin, the more profit there is—after taxes—to cover financial obligations, reinvest in the business, and distribute dividends to owners.')
            st.subheader('Ranked from Best Performing to Worse Performing')
            st.table(operating_proffitmean_yoy_change_by_company)

        profitability_df_csv = convert_df(profitability_Ratios)
        st.download_button(
            label="Download Profitability Ratio Sheet as CSV",
            data=profitability_df_csv,
            file_name='ProfitabilityRatioSheet.csv',
            mime='text/csv',
        )
    with Liquidity_Ratios:
        st.subheader("Liquidity Ratio Information")
        liquidity_Ratios=get_MultipleLiquidityRatios(selected_ticker_symbols)
        liquidity_list=liquidity_Ratios.columns.tolist()
        if 'Company' in liquidity_list:
            liquidity_list.remove('Company')

        selected_columns_liquidity = st.multiselect('Please select which Ratios you wish to plot:',liquidity_list, default=['Current Ratio','Operating Cash Flow Ratio'])
        # Plot line chart
        if selected_columns_liquidity:
            plot_multiple_columns_lines(liquidity_Ratios,selected_columns_liquidity)


        current_ratio_Ranking,operating_cash_flow_ratio_Ranking=get_RankingTableLiquidity(liquidity_Ratios)

        current_ratio_tab,operating_cash_flow_ratio_tab = st.tabs(["Current Ratio Ranking", "Operating Cash Flow Ratio Ranking"])
        with current_ratio_tab:
            st.header("Current Ratio Margin Ranking")
            st.write("In the following table you will see the ranking of the companies that performed the best in the last two years according to the Current Ratio.")
            st.latex(r'Current Ratio= \frac{Current Assets}{Current Liabilities}')
            st.write('The current ratio measures a company’s ability to pay current, or short-term, liabilities (debts and payables) with its current, or short-term, assets, such as cash, inventory, and receivables.In many cases, a company with a current ratio of less than 1.00 does not have the capital on hand to meet its short-term obligations if they were all due at once, while a current ratio greater than 1.00 indicates that the company has the financial resources to remain solvent in the short term. ')
            st.subheader('Ranked from Best Performing to Worse Performing')
            st.table(current_ratio_Ranking)

        with operating_cash_flow_ratio_tab:
            st.header("Operating Cash Flow Ratio Ranking")
            st.write("In the following table you will see the ranking of the companies that performed the best in the last two years according to the Operating Cash Flow Ratio")
            st.latex(r'Operating Cash Flow Ratio= \frac{Operating Cash Flow}{Current Liabilities}')
            st.write('The operating cash flow ratio is a measure of the number of times a company can pay off current debts with cash generated within the same period. A high number, greater than one, indicates that a company has generated more cash in a period than what is needed to pay off its current liabilities.An operating cash flow ratio of less than one indicates the opposite—the firm has not generated enough cash to cover its current liabilities. To investors and analysts, a low ratio could mean that the firm needs more capital.')
            st.subheader('Ranked from Best Performing to Worse Performing')
            st.table(operating_cash_flow_ratio_Ranking)


        liquidity_df_csv = convert_df(liquidity_Ratios)
        st.download_button(
            label="Download Liquidity Ratio Sheet as CSV",
            data=liquidity_df_csv,
            file_name='LiquidityRatioSheet.csv',
            mime='text/csv',
        )

    with Efficiency_Ratios:
        st.subheader("Efficiency Ratio Information")
        efficiency_Ratios=get_MultipleEfficiencyRatios(selected_ticker_symbols)
        efficiency_list=efficiency_Ratios.columns.tolist()

        if 'Company' in efficiency_list:
            efficiency_list.remove('Company')

        selected_columns_efficiency = st.multiselect('Please select which Ratios you wish to plot:',efficiency_list, default=['Cash Flow to Income Ratio'])
        # Plot line chart
        if selected_columns_efficiency:
            plot_multiple_columns_lines(efficiency_Ratios,selected_columns_efficiency)


        cash_flow_to_net_income_Ratio_Ranking,cash_flow_to_net_income_Ratio_RankingYoY=get_RankingTableEfficiency(efficiency_Ratios)

        cash_flow_to_net_income_ratio_tab,cash_flow_to_net_income_ratio_YOY_tab = st.tabs(["Cash Flow to Income Ratio Ranking","Cash Flow to Income Ratio Ranking Most Improved"])
        with cash_flow_to_net_income_ratio_tab:
            st.header("Cash Flow to Income Ratio Ranking")
            st.write("In the following table you will see the ranking of the companies that performed the best in the last two years according to the Cash Flow to Income Ratio.")
            st.latex(r'Cash Flow to Net Income Ratio= \frac{Operating Cash Flow}{Net Income}')
            st.write('The Cash Flow to Income Ratio, also known as the Cash Flow Coverage Ratio, assesses the relationship between a companys operating cash flow and its net income. It provides insights into how well a company can convert its reported profits into actual cash flow. A ratio greater than 1 suggests that the company generates more cash from its operations than is reflected in its net income. This can be seen as a positive indicator, indicating that the companys reported profits are being supported by strong operating cash flow. A ratio below 1 may indicate that the company is not generating as much cash from its operations as it reports in net income. This could be a signal that non-cash items (such as depreciation or changes in working capital) are significantly impacting reported profits.')
            st.subheader('Ranked from Best Performing to Worse Performing')
            st.table(cash_flow_to_net_income_Ratio_Ranking)

        with cash_flow_to_net_income_ratio_YOY_tab:
            st.header("Cash Flow to Income Ratio YoY Ranking")
            st.write("In the following table you will see the ranking of the companies that have become more efficient in the last two years according to the Cash Flow to Income Ratio.")
            st.latex(r'Cash Flow to Net Income Ratio= \frac{Operating Cash Flow}{Net Income}')
            st.write('The Cash Flow to Income Ratio, also known as the Cash Flow Coverage Ratio, assesses the relationship between a companys operating cash flow and its net income. It provides insights into how well a company can convert its reported profits into actual cash flow. A ratio greater than 1 suggests that the company generates more cash from its operations than is reflected in its net income. This can be seen as a positive indicator, indicating that the companys reported profits are being supported by strong operating cash flow. A ratio below 1 may indicate that the company is not generating as much cash from its operations as it reports in net income. This could be a signal that non-cash items (such as depreciation or changes in working capital) are significantly impacting reported profits.')
            st.subheader('Ranked from Best Performing to Worse Performing')
            st.table(cash_flow_to_net_income_Ratio_RankingYoY)

        efficiency_df_csv = convert_df(efficiency_Ratios)
        st.download_button(
            label="Download Efficiency Ratio Sheet as CSV",
            data=efficiency_df_csv,
            file_name='EfficiencyRatioSheet.csv',
            mime='text/csv',
        )

    with Whole_Ratio:
        st.subheader("Complete Ratio Sheet Information")
        Ratio_df=get_WholeRatio(selected_ticker_symbols)

        ratio_list=Ratio_df.columns.tolist()
        if 'Company' in ratio_list:
            ratio_list.remove('Company')
        selected_columns_ratio = st.multiselect('Please select which Ratios you wish to plot:',ratio_list, default=['Current Ratio','Equity_Multiplier_Ratio'])
        # Plot line chart
        if selected_columns_ratio:
            plot_multiple_columns_lines(Ratio_df,selected_columns_ratio)

        ratio_df_csv = convert_df(Ratio_df)

        st.download_button(
            label="Download Complete Ratio Sheet as CSV",
            data=ratio_df_csv,
            file_name='RatioSheet.csv',
            mime='text/csv',
        )

        st.divider()
