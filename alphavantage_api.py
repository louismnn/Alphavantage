import pandas as pd
import requests


class AlphaVantage():
    def __init__(self):
        self.api = "YOUR_API_KEY" # you can find it with this link https://www.alphavantage.co

    def time_series_intraday(self, ticker: str, interval: int, adjusted=True, extended_hours=True, month=None, outputsize="compact"):
        """
        This API returns current and 20+ years of historical intraday OHLCV time series of the equity specified, covering pre-market and post-market hours where applicable (e.g., 4:00am to 8:00pm Eastern Time for the US market). You can query both raw (as-traded) and split/dividend-adjusted intraday data from this endpoint. The OHLCV data is sometimes called "candles" in finance literature.

        ❚ Required: ticker (str)
            The name of the equity of your choice. For example: ticker=IBM

        ❚ Required: interval (int)
            Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min

        ❚ Optional: adjusted (Boll)
            By default, adjusted=true and the output time series is adjusted by historical split and dividend events. Set adjusted=false to query raw (as-traded) intraday values.

        ❚ Optional: extended_hours (Boll)
            By default, extended_hours=true and the output time series will include both the regular trading hours and the extended (pre-market and post-market) trading hours (4:00am to 8:00pm Eastern Time for the US market). Set extended_hours=false to query regular trading hours (9:30am to 4:00pm US Eastern Time) only.

        ❚ Optional: month (str)
            By default, this parameter is not set and the API will return intraday data for the most recent days of trading. You can use the month parameter (in YYYY-MM format) to query a specific month in history. For example, month=2009-01. Any month in the last 20+ years since 2000-01 (January 2000) is supported.

        ❚ Optional: outputsize (str)
            By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points in the intraday time series; full returns trailing 30 days of the most recent intraday data if the month parameter (see above) is not specified, or the full intraday data for a specific month in history if the month parameter is specified. The "compact" option is recommended if you would like to reduce the data size of each API call.
        """

        if month == None:
            my_month = ""
        else:
            my_month = f"&month={month}"

        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval={interval}min&extended_hours={extended_hours}&adjusted={adjusted}{my_month}&outputsize={outputsize}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        time_series = data[f"Time Series ({interval}min)"]
        normalized_data = []
        for date, values in time_series.items():
            normalized_data.append({
                "date": date,
                "open": values["1. open"],
                "high": values["2. high"],
                "low": values["3. low"],
                "close": values["4. close"],
                "volume": values["5. volume"],
            })

        df = pd.DataFrame.from_dict(normalized_data)
        return df
    
    def time_series_daily(self, ticker: str, outputsize="compact"):
        """
        This API returns raw (as-traded) daily time series (date, daily open, daily high, daily low, daily close, daily volume) of the global equity specified, covering 20+ years of historical data. The OHLCV data is sometimes called "candles" in finance literature. If you are also interested in split/dividend-adjusted data, please use the Daily Adjusted API, which covers adjusted close values and historical split and dividend events.
        
        ❚ Required: ticker (str)
            The name of the equity of your choice. For example: ticker=IBM

        ❚ Optional: outputsize (str)
            By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points; full returns the full-length time series of 20+ years of historical data. The "compact" option is recommended if you would like to reduce the data size of each API call.
        """
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize={outputsize}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        time_series = data["Time Series (Daily)"]
        normalized_data = []
        for date, values in time_series.items():
            normalized_data.append({
                "date": date,
                "open": values["1. open"],
                "high": values["2. high"],
                "low": values["3. low"],
                "close": values["4. close"],
                "volume": values["5. volume"],
            })

        df = pd.DataFrame.from_dict(normalized_data)
        return df
  
    def time_series_daily_adjusted(self, ticker: str, outputsize="compact"):
        """
        This API returns raw (as-traded) daily time series (date, daily open, daily high, daily low, daily close, daily volume) of the global equity specified, covering 20+ years of historical data. The OHLCV data is sometimes called "candles" in finance literature. If you are also interested in split/dividend-adjusted data, please use the Daily Adjusted API, which covers adjusted close values and historical split and dividend events.
        
        ❚ Required: ticker (str)
            The name of the equity of your choice. For example: ticker=IBM
        
        ❚ Optional: outputsize (str)
            By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points; full returns the full-length time series of 20+ years of historical data. The "compact" option is recommended if you would like to reduce the data size of each API call.
        """
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&outputsize={outputsize}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        time_series = data["Time Series (Daily)"]
        normalized_data = []
        for date, values in time_series.items():
            normalized_data.append({
                "date": date,
                "open": values["1. open"],
                "high": values["2. high"],
                "low": values["3. low"],
                "close": values["4. close"],
                "adjusted_close": values["5. adjusted close"],
                "volume": values["6. volume"],
                "dividend_amount": values["7. dividend amount"],
                "split_coefficient": values["8. split coefficient"]
            })

        df = pd.DataFrame.from_dict(normalized_data)
        return df
    
    def time_series_weekly(self, ticker: str):
        """
        This API returns weekly time series (last trading day of each week, weekly open, weekly high, weekly low, weekly close, weekly volume) of the global equity specified, covering 20+ years of historical data.
        
        ❚ Required: ticker (str)
            The name of the equity of your choice. For example: ticker=IBM
        
        ❚ Optional: outputsize (str)
            By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points; full returns the full-length time series of 20+ years of historical data. The "compact" option is recommended if you would like to reduce the data size of each API call.
        """
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={ticker}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        time_series = data["Weekly Time Series"]
        normalized_data = []
        for date, values in time_series.items():
            normalized_data.append({
                "date": date,
                "open": values["1. open"],
                "high": values["2. high"],
                "low": values["3. low"],
                "close": values["4. close"],
                "volume": values["5. volume"]
            })

        df = pd.DataFrame.from_dict(normalized_data)
        return df

    def time_series_weekly_adjusted(self, ticker: str):
        """
        This API returns weekly adjusted time series (last trading day of each week, weekly open, weekly high, weekly low, weekly close, weekly adjusted close, weekly volume, weekly dividend) of the global equity specified, covering 20+ years of historical data.
        
        ❚ Required: ticker (str)
            The name of the equity of your choice. For example: ticker=IBM
        """
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={ticker}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        time_series = data["Weekly Adjusted Time Series"]
        normalized_data = []
        for date, values in time_series.items():
            normalized_data.append({
                "date": date,
                "open": values["1. open"],
                "high": values["2. high"],
                "low": values["3. low"],
                "close": values["4. close"],
                "adjusted_close": values["5. adjusted close"],
                "volume": values["6. volume"],
                "dividend_amount": values["7. dividend amount"]
            })

        df = pd.DataFrame.from_dict(normalized_data)
        return df

    def time_series_monthly(self, ticker: str):
        """
        This API returns monthly time series (last trading day of each month, monthly open, monthly high, monthly low, monthly close, monthly volume) of the global equity specified, covering 20+ years of historical data.
        
        ❚ Required: ticker (str)
            The name of the equity of your choice. For example: ticker=IBM
        """
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={ticker}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        time_series = data["Monthly Time Series"]
        normalized_data = []
        for date, values in time_series.items():
            normalized_data.append({
                "date": date,
                "open": values["1. open"],
                "high": values["2. high"],
                "low": values["3. low"],
                "close": values["4. close"],
                "volume": values["5. volume"]
            })

        df = pd.DataFrame.from_dict(normalized_data)
        return df

    def time_series_monthly_adjusted(self, ticker: str):
        """
        This API returns monthly adjusted time series (last trading day of each month, monthly open, monthly high, monthly low, monthly close, monthly adjusted close, monthly volume, monthly dividend) of the equity specified, covering 20+ years of historical data.
        
        ❚ Required: ticker (str)
            The name of the equity of your choice. For example: ticker=IBM

        return a json file
        """
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={ticker}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        time_series = data["Monthly Adjusted Time Series"]
        normalized_data = []
        for date, values in time_series.items():
            normalized_data.append({
                "date": date,
                "open": values["1. open"],
                "high": values["2. high"],
                "low": values["3. low"],
                "close": values["4. close"],
                "adjusted_close": values["5. adjusted close"],
                "volume": values["6. volume"],
                "dividend_amount": values["7. dividend amount"]
            })

        df = pd.DataFrame.from_dict(normalized_data)
        return df

    def quote_endpoint(self, ticker: str):
        """
        This endpoint returns the latest price and volume information for a ticker of your choice. You can specify one ticker per API request.
        If you would like to query a large universe of tickers in bulk, you may want to try out our Realtime Bulk Quotes API, which accepts up to 100 tickers per API request.
        
        ❚ Required: ticker (str)
            The symbol of the global ticker of your choice. For example: symbol=IBM.
        
        return a json file
        """
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={self.api}'
        r = requests.get(url)
        return r.json()

    def realtime_bulk_quotes(self, tickers: list):
        """
        Premium function
        This API returns realtime quotes for US-traded symbols in bulk, accepting up to 100 symbols per API request and covering both regular and extended (pre-market and post-market) trading hours. You can use this endpoint as a high-throughput alternative to the Global Quote API, which accepts one symbol per API request.
        (Premium)

        ❚ Required: tickers (list)
            Up to 100 symbols separated by comma. For example: symbol=MSFT,AAPL,IBM. If more than 100 symbols are provided, only the first 100 symbols will be honored as part of the API input.
        """

        new_tickets = ",".join(tickers)
        url = f'https://www.alphavantage.co/query?function=REALTIME_BULK_QUOTES&symbol={new_tickets}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        time_series = data["data"]
        df = pd.DataFrame.from_dict(time_series)
        print(data["message"])
        return df

    def search_endpoint(self, keywords: str):
        """
        We've got you covered! The Search Endpoint returns the best-matching symbols and market information based on keywords of your choice. The search results also contain match scores that provide you with the full flexibility to develop your own search and filtering logic.
        
        ❚ Required: keywords (str)
            A text string of your choice. For example: keywords=microsoft.
        """

        url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keywords}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        time_series = data["bestMatches"]
        df = pd.DataFrame.from_dict(time_series)
        return df
    
    def global_market_open(self):
        """
        This endpoint returns the current market status (open vs. closed) of major trading venues for equities, forex, and cryptocurrencies around the world.
        """
    
        url = f'https://www.alphavantage.co/query?function=MARKET_STATUS&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        time_series = data["markets"]
        df = pd.DataFrame.from_dict(time_series)
        return df


    def realtime_options(self, ticker: str, contract="", require_greeks=False):
        """
        This API returns realtime US options data with full market coverage. Option chains are sorted by expiration dates in chronological order. Within the same expiration date, contracts are sorted by strike prices from low to high.
        (Premium)

        ❚ Required: ticker (str)
            The name of the equity of your choice. For example: ticker=IBM

        ❚ Optional: require_greeks (Bool)
            Enable greeks & implied volatility (IV) fields. By default, require_greeks=false. Set require_greeks=true to enable greeks & IVs in the API response.

        ❚ Optional: contract (str)
            The US options contract ID you would like to specify. By default, the contract parameter is not set and the entire option chain for a given symbol will be returned.
        """

        if contract != "":
            contract = f"&contract={contract}"

        url = f'https://www.alphavantage.co/query?function=REALTIME_OPTIONS&symbol={ticker}&require_greeks={require_greeks}{contract}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        time_series = data["data"]
        df = pd.DataFrame.from_dict(time_series)
        print(data["message"])
        return df

    def historical_options(self, ticker: str, date=""):
        """
        This API returns the full historical options chain for a specific symbol on a specific date, covering 15+ years of history. Implied volatility (IV) and common Greeks (e.g., delta, gamma, theta, vega, rho) are also returned. Option chains are sorted by expiration dates in chronological order. Within the same expiration date, contracts are sorted by strike prices from low to high.
        The date need to have the form YYYY-MM-DD
        If no date this will return the options from the previous session
        
        ❚ Required: ticker (str)
            The name of the equity of your choice. For example: ticker=IBM

        ❚ Optional: date (str)
            By default, the date parameter is not set and the API will return data for the previous trading session. Any date later than 2008-01-01 is accepted. For example, date=2017-11-15.
        """

        if date != "":
            date = "&date=" + date

        url = f'https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol={ticker}{date}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        time_series = data["data"]
        df = pd.DataFrame.from_dict(time_series)
        return df
    



    def market_sentiment(self, ticker="", topics="", sort="LATEST", limit=50,  time_from="", time_to=""):
        """
        Looking for market news data to train your LLM models or to augment your trading strategy? You have just found it. This API returns live and historical market news & sentiment data from a large & growing selection of premier news outlets around the world, covering stocks, cryptocurrencies, forex, and a wide range of topics such as fiscal policy, mergers & acquisitions, IPOs, etc. This API, combined with our core stock API, fundamental data, and technical indicator APIs, can provide you with a 360-degree view of the financial market and the broader economy.
        
        ❚ Optional: ticker (str)
            The stock/crypto/forex ticker of your choice. For example: ticker=IBM will filter for articles that mention the IBM ticker; ticker=COIN,CRYPTO:BTC,FOREX:USD will filter for articles that simultaneously mention Coinbase (COIN), Bitcoin (CRYPTO:BTC), and US Dollar (FOREX:USD) in their content.

        ❚ Optional: topics (str)
            The news topics of your choice. For example: topics=technology will filter for articles that write about the technology sector; topics=technology,ipo will filter for articles that simultaneously cover technology and IPO in their content. Below is the full list of supported topics:

            - Blockchain: blockchain
            - Earnings: earnings
            - IPO: ipo
            - Mergers & Acquisitions: mergers_and_acquisitions
            - Financial Markets: financial_markets
            - Economy - Fiscal Policy (e.g., tax reform, government spending): economy_fiscal
            - Economy - Monetary Policy (e.g., interest rates, inflation): economy_monetary
            - Economy - Macro/Overall: economy_macro
            - Energy & Transportation: energy_transportation
            - Finance: finance
            - Life Sciences: life_sciences
            - Manufacturing: manufacturing
            - Real Estate & Construction: real_estate
            - Retail & Wholesale: retail_wholesale
            - Technology: technology

        ❚ Optional: sort (str)
            By default, sort=LATEST and the API will return the latest articles first. You can also set sort=EARLIEST or sort=RELEVANCE based on your use case.

        ❚ Optional: limit (int)
            By default, limit=50 and the API will return up to 50 matching results. You can also set limit=1000 to output up to 1000 results.

        ❚ Optional: time_from and time_to (str)
            The time range of the news articles you are targeting, in YYYYMMDDTHHMM format. For example: time_from=20220410T0130. If time_from is specified but time_to is missing, the API will return articles published between the time_from value and the current time.
        
        example : https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=COIN,CRYPTO:BTC,FOREX:USD&time_from=20220410T0130&limit=1000&apikey=demo
        
        return a json file
        """
        if time_from != "":
            time_from = f"&time_from={time_from}"
        if time_to != "":
            time_to = f"&time_to={time_to}"
        if topics != "":
            topics = f"&topics={topics}"

        url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}{topics}&sort={sort}{time_from}{time_to}&limit={limit}&apikey={self.api}"
        r = requests.get(url)
        return r.json()
    
    def earnings_call_transcript(self, ticker: str, quarter:str):
        """
        This API returns the earnings call transcript for a given company in a specific quarter, covering over 15 years of history and enriched with LLM-based sentiment signals.

        ❚ Required: ticker (str)
            The symbol of the ticker of your choice. For example: ticker=IBM.

        ❚ Required: quarter (str)
            Fiscal quarter in YYYYQM format. For example: quarter=2024Q1. Any quarter since 2010Q1 is supported.

        example : https://www.alphavantage.co/query?function=EARNINGS_CALL_TRANSCRIPT&symbol=IBM&quarter=2024Q1&apikey=demo
        
        return a json file
        """

        my_quater = f"&quarter={quarter}"

        url = f'https://www.alphavantage.co/query?function=INSIDER_TRANSACTIONS&symbol={ticker}{my_quater}&apikey={self.api}'
        r = requests.get(url)
        return r.json()
    
    def top_gainers_losers(self):
        """
        This endpoint returns the top 20 gainers, losers, and the most active traded tickers in the US market.
        Data delayed by 15 minutes
        top_gainers_losers()[0] for top gainers
        top_gainers_losers()[1] for top losers
        top_gainers_losers()[2] for most actively traded
        """

        url = f'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        first = data["top_gainers"]
        second = data["top_losers"]
        third = data["most_actively_traded"]

        df1 = pd.DataFrame.from_dict(first)
        df2 = pd.DataFrame.from_dict(second)
        df3 = pd.DataFrame.from_dict(third)

        return df1, df2, df3

    def insider_transactions(self, ticker: int):
        """
        This API returns the latest and historical insider transactions made be key stakeholders (e.g., founders, executives, board members, etc.) of a specific company.

        ❚ Required: ticker (str)
            The symbol of the ticker of your choice. For example: ticker=IBM.
        """

        url = f'https://www.alphavantage.co/query?function=INSIDER_TRANSACTIONS&symbol={ticker}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        return df
    
    def advance_analytics(self, symbols: list, start_date: str, end_date: str, interval: str, calculation: list, HOLC="close"):
        """
        ❚ Required: SYMBOLS (list)
            A list of symbols for the calculation. It can be a comma separated list of symbols as a string. Free API keys can specify up to 5 symbols per API request. Premium API keys can specify up to 50 symbols per API request.

        ❚ Required: RANGE (str)
            This is the date range for the series being requested. By default, the date range is the full set of data for the equity history. This can be further modified by the LIMIT variable.
            To specify start & end dates for your analytics calcuation, simply add two RANGE parameters in your API request. For example: RANGE=2023-07-01&RANGE=2023-08-31 or RANGE=2020-12-01T00:04:00&RANGE=2020-12-06T23:59:59 with minute-level precision for intraday analytics. If the end date is missing, the end date is assumed to be the last trading date. In addition, you can request a full month of data by using YYYY-MM format like 2020-12. One day of intraday data can be requested by using YYYY-MM-DD format like 2020-12-06

        ❚ Optional: OHLC (str)
            This allows you to choose which open, high, low, or close field the calculation will be performed on. By default, OHLC=close. Valid values for these fields are open, high, low, close.

        ❚ Required: INTERVAL (str)
            Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, DAILY, WEEKLY, MONTHLY.

        ❚ Required: CALCULATIONS (list)
            A comma separated list of the analytics metrics you would like to calculate (limit of one for the free API):

                MIN: The minimum return (largest negative or smallest positive) for all values in the series
                MAX: The maximum return for all values in the series
                MEAN: The mean of all returns in the series
                MEDIAN: The median of all returns in the series
                CUMULATIVE_RETURN: The total return from the beginning to the end of the series range
                VARIANCE: The population variance of returns in the series range. Optionally, you can use VARIANCE(annualized=True)to normalized the output to an annual value. By default, the variance is not annualized.
                STDDEV: The population standard deviation of returns in the series range for each symbol. Optionally, you can use STDDEV(annualized=True)to normalized the output to an annual value. By default, the standard deviation is not annualized.
                MAX_DRAWDOWN: Largest peak to trough interval for each symbol in the series range
                HISTOGRAM: For each symbol, place the observed total returns in bins. By default, bins=10. Use HISTOGRAM(bins=20) to specify a custom bin value (e.g., 20).
                AUTOCORRELATION: For each symbol place, calculate the autocorrelation for the given lag (e.g., the lag in neighboring points for the autocorrelation calculation). By default, lag=1. Use AUTOCORRELATION(lag=2) to specify a custom lag value (e.g., 2).
                COVARIANCE: Returns a covariance matrix for the input symbols. Optionally, you can use COVARIANCE(annualized=True)to normalized the output to an annual value. By default, the covariance is not annualized.
                CORRELATION: Returns a correlation matrix for the input symbols, using the PEARSON method as default. You can also specify the KENDALL or SPEARMAN method through CORRELATION(method=KENDALL) or CORRELATION(method=SPEARMAN), respectively.
            
        return a json file
        """

        my_symbols = ",".join(symbols)
        my_calculation = ",".join(calculation)

        url = f'https://www.alphavantage.co/query?function=ANALYTICS_FIXED_WINDOW&SYMBOLS={my_symbols}&RANGE={start_date}&RANGE={end_date}&INTERVAL={interval}&OHLC={HOLC}&CALCULATIONS={my_calculation}&apikey={self.api}'
        r = requests.get(url)
        return r.json()

    def advanced_analytics_sliding_window(self, symbols: list, start_date: str, end_date: str, interval: str, calculation: list, window_size: int, HOLC="close"):
        """
        This endpoint returns a rich set of advanced analytics metrics (e.g., total return, variance, auto-correlation, etc.) for a given time series over sliding time windows. For example, we can calculate a moving variance over 5 years with a window of 100 points to see how the variance changes over time.

        ❚ Required: SYMBOLS (str)
            A list of symbols for the calculation. It can be a comma separated list of symbols as a string. Free API keys can specify up to 5 symbols per API request. Premium API keys can specify up to 50 symbols per API request.

        ❚ Optional: OHLC (str)
            This allows you to choose which open, high, low, or close field the calculation will be performed on. By default, OHLC=close. Valid values for these fields are open, high, low, close.

        ❚ Required: INTERVAL (str)
            Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, DAILY, WEEKLY, MONTHLY.

        ❚ Required: WINDOW_SIZE (str)
            An integer representing the size of the moving window. A hard lower boundary of 10 has been set though it is recommended to make this window larger to make sure the running calculations are statistically significant.

        ❚ Required: CALCULATIONS (str)
            A comma separated list of the analytics metrics you would like to calculate. Free API keys can specify 1 metric to be calculated per API request. Premium API keys can specify multiple metrics to be calculated simultaneously per API request.

            MEAN: The mean of all returns in the series
            MEDIAN: The median of all returns in the series
            CUMULATIVE_RETURN: The total return from the beginning to the end of the series range
            VARIANCE: The population variance of returns in the series range. Optionally, you can use VARIANCE(annualized=True)to normalized the output to an annual value. By default, the variance is not annualized.
            STDDEV: The population standard deviation of returns in the series range for each symbol. Optionally, you can use STDDEV(annualized=True)to normalized the output to an annual value. By default, the standard deviation is not annualized.
            COVARIANCE: Returns a covariance matrix for the input symbols. Optionally, you can use COVARIANCE(annualized=True)to normalized the output to an annual value. By default, the covariance is not annualized.
            CORRELATION: Returns a correlation matrix for the input symbols, using the PEARSON method as default. You can also specify the KENDALL or SPEARMAN method through CORRELATION(method=KENDALL) or CORRELATION(method=SPEARMAN), respectively.
        
        return a json file
        """

        my_symbols = ",".join(symbols)
        my_calculation = ",".join(calculation)
        my_windowsize = f"&WINDOW_SIZE={window_size}"

        url = f'https://www.alphavantage.co/query?function=ANALYTICS_SLIDING_WINDOW&SYMBOLS={my_symbols}&RANGE={start_date}&RANGE={end_date}&INTERVAL={interval}&OHLC={HOLC}{my_windowsize}&CALCULATIONS={my_calculation.upper()}&apikey={self.api}'
        r = requests.get(url)
        return r.json()
    
    def company_overview(self, ticker: str):
        """
        This API returns the company information, financial ratios, and other key metrics for the equity specified. Data is generally refreshed on the same day a company reports its latest earnings and financials.
        
        ❚ Required: ticker (str)
            The symbol of the ticker of your choice. For example: ticker=QQQ.
        
        return a json file
        """

        url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={self.api}'
        r = requests.get(url)
        return r.json()
    
    def ETF_profil(self, ticker: str):
        """
        This API returns key ETF metrics (e.g., net assets, expense ratio, and turnover), along with the corresponding ETF holdings / constituents with allocation by asset types and sectors.
       
        ❚ Required: ticker (str)
            The symbol of the ticker of your choice. For example: ticker=QQQ.
        
        ETF_profil("QQQ")[0] for sectors weight
        ETF_profil("QQQ")[1] for holdings weight
        """

        url = f'https://www.alphavantage.co/query?function=ETF_PROFILE&symbol={ticker}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df1 = pd.DataFrame.from_dict(data["sectors"])
        df2 = pd.DataFrame.from_dict(data[ "holdings"])
        return df1, df2
    
    def action_dividends(self, ticker: str):
        """
        This API returns historical and future (declared) dividend distributions.
        
        ❚ Required: symbol (str)
            The symbol of the ticker of your choice. For example: ticker=IBM.
        """

        url = f'https://www.alphavantage.co/query?function=DIVIDENDS&symbol={ticker}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        return df
    
    def actions_split(self, ticker: str):
        """
        This API returns historical split events.

        ❚ Required: symbol (str)
            The symbol of the ticker of your choice. For example: ticker=IBM.
        """

        url = f'https://www.alphavantage.co/query?function=SPLITS&symbol={ticker}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        return df

    def income_statement(self, ticker: str):
        """
        This API returns the annual and quarterly income statements for the company of interest, with normalized fields mapped to GAAP and IFRS taxonomies of the SEC. Data is generally refreshed on the same day a company reports its latest earnings and financials.
        
        ❚ Required: ticker (str)
            The symbol of the ticker of your choice. For example: ticker=IBM.
        """

        url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["annualReports"])
        df.set_index("fiscalDateEnding", inplace=True)
        return df.T
    
    def balance_sheet(self, ticker: str):
        """
        This API returns the annual and quarterly balance sheets for the company of interest, with normalized fields mapped to GAAP and IFRS taxonomies of the SEC. Data is generally refreshed on the same day a company reports its latest earnings and financials.
        
        ❚ Required: ticker (str)
            The symbol of the ticker of your choice. For example: ticker=IBM.
        """

        url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["annualReports"])
        df.set_index("fiscalDateEnding", inplace=True)
        return df.T
    
    def cash_flow(self, ticker: str):
        """
        This API returns the annual and quarterly cash flow for the company of interest, with normalized fields mapped to GAAP and IFRS taxonomies of the SEC. Data is generally refreshed on the same day a company reports its latest earnings and financials.
        
        ❚ Required: ticker
            The symbol of the ticker of your choice. For example: ticker=IBM.
        """

        url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["annualReports"])
        return df
    
    def earnings(self, ticker: str):
        """
        This API returns the annual and quarterly earnings (EPS) for the company of interest. Quarterly data also includes analyst estimates and surprise metrics.
        
        ❚ Required: ticker (str)
            The symbol of the ticker of your choice. For example: ticker=IBM.
        
        earnings("IBM")[0] for annual earnings
        earnings("IBM)[1] for quaterly earnings
        """

        url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()
        
        df1 = pd.DataFrame.from_dict(data["annualEarnings"])
        df2 = pd.DataFrame.from_dict(data["quarterlyEarnings"])
        return df1, df2

    
    def listening_delisting_status(self, date="", state=""):
        """
        This API returns a list of active or delisted US stocks and ETFs, either as of the latest trading day or at a specific time in history. The endpoint is positioned to facilitate equity research on asset lifecycle and survivorship.

        ❚ Optional: date (str)
            If no date is set, the API endpoint will return a list of active or delisted symbols as of the latest trading day. If a date is set, the API endpoint will "travel back" in time and return a list of active or delisted symbols on that particular date in history. Any YYYY-MM-DD date later than 2010-01-01 is supported. For example, date=2013-08-03

        ❚ Optional: state (str)
            By default, state=active and the API will return a list of actively traded stocks and ETFs. Set state=delisted to query a list of delisted assets.
        """
        import csv
        date = f"&date={date}"
        state = f"&state={state}"

        if date == "" and state == "":
            CSV_URL = f"https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={self.api}"
        elif date != "" and state == "":
            CSV_URL = f"https://www.alphavantage.co/query?function=LISTING_STATUS{date}&apikey={self.api}"
        elif date == "" and state != "":
            CSV_URL = f"https://www.alphavantage.co/query?function=LISTING_STATUS{state}&apikey={self.api}"
        else:
            CSV_URL = f'https://www.alphavantage.co/query?function=LISTING_STATUS{date}{state}&apikey={self.api}'

        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            df = pd.DataFrame(my_list)
            df.columns = df.iloc[0]
            df = df[1:].reset_index(drop=True)
            return df

    def earnings_calendar(self, ticker: str, horizon="3month"):
        """
        This API returns a list of company earnings expected in the next 3, 6, or 12 months.

        ❚ Optional: ticker (str)
            By default, no ticker will be set for this API. When no ticker is set, the API endpoint will return the full list of company earnings scheduled. If a ticker is set, the API endpoint will return the expected earnings for that specific ticker. For example, ticker=IBM

        ❚ Optional: horizon (int)
            By default, horizon=3month and the API will return a list of expected company earnings in the next 3 months. You may set horizon=6month or horizon=12month to query the earnings scheduled for the next 6 months or 12 months, respectively.
        """
        import csv
        CSV_URL = f'https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&symbol={ticker}&horizon={horizon}month&apikey={self.api}'

        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            df = pd.DataFrame(my_list)
            df.columns = df.iloc[0]
            df = df[1:].reset_index(drop=True)
            return df

    def IPO_calendar(self):
        """
        This API returns a list of IPOs expected in the next 3 months.
        """

        import csv
        CSV_URL = f'https://www.alphavantage.co/query?function=IPO_CALENDAR&apikey={self.api}'

        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            df = pd.DataFrame(my_list)
            df.columns = df.iloc[0]
            df = df[1:].reset_index(drop=True)
            return df

    def exchange_rate(self, from_currency: str, to_currency: str):
        """
        This API returns the realtime exchange rate for a pair of digital currency (e.g., Bitcoin) and physical currency (e.g., USD).

        ❚ Required: from_currency (str)
            The currency you would like to get the exchange rate for. It can either be a physical currency or digital/crypto currency. For example: from_currency=USD or from_currency=BTC.

        ❚ Required: to_currency (str)
            The destination currency for the exchange rate. It can either be a physical currency or digital/crypto currency. For example: to_currency=USD or to_currency=BTC.
        
        return a json file
        """

        url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()
        return data["Realtime Currency Exchange Rate"]
    
    def FX_intraday(self, from_symbol: str, to_symbol: str, interval: int, outputsize="compact"):
        """
        This API returns intraday time series (timestamp, open, high, low, close) of the FX currency pair specified, updated realtime.
        (Premium)

        ❚ Required: from_symbol (str)
            A three-letter symbol from the forex currency list. For example: from_symbol=EUR
        
        ❚ Required: to_symbol (str)
            A three-letter symbol from the forex currency list. For example: to_symbol=USD

        ❚ Required: interval (int)
            Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min

        ❚ Optional: outputsize (str)
            By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points in the intraday time series; full returns the full-length intraday time series. The "compact" option is recommended if you would like to reduce the data size of each API call.
        """
        new_outputsize = f"outputsize={outputsize}"

        url = f'https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol={from_symbol}&to_symbol={to_symbol}&interval={interval}min{new_outputsize}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        time_series = data[f"Time Series FX ({interval}min)"]
        normalized_data = []
        for date, values in time_series.items():
            normalized_data.append({
                "date": date,
                "open": values["1. open"],
                "high": values["2. high"],
                "low": values["3. low"],
                "close": values["4. close"]
            })

        df = pd.DataFrame.from_dict(normalized_data)
        return df
    
    def FX_daily(self, from_symbol: str, to_symbol: str, outputsize="compact"):
        """
        This API returns the daily time series (timestamp, open, high, low, close) of the FX currency pair specified, updated realtime.
        
        ❚ Required: from_symbol (str)
            A three-letter symbol from the forex currency list. For example: from_symbol=EUR

        ❚ Required: to_symbol (str)
            A three-letter symbol from the forex currency list. For example: to_symbol=USD

        ❚ Optional: outputsize (str)
            By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points in the daily time series; full returns the full-length daily time series. The "compact" option is recommended if you would like to reduce the data size of each API call.
        """

        url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={from_symbol}&to_symbol={to_symbol}&outputsize={outputsize}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        time_series = data["Time Series FX (Daily)"]
        normalized_data = []
        for date, values in time_series.items():
            normalized_data.append({
                "date": date,
                "open": values["1. open"],
                "high": values["2. high"],
                "low": values["3. low"],
                "close": values["4. close"]
            })

        df = pd.DataFrame.from_dict(normalized_data)
        return df
    
    def FX_weekly(self, from_symbol: str, to_symbol: str):
        """
        This API returns the weekly time series (timestamp, open, high, low, close) of the FX currency pair specified, updated realtime.
        The latest data point is the price information for the week (or partial week) containing the current trading day, updated realtime.

        ❚ Required: from_symbol (str)
            A three-letter symbol from the forex currency list. For example: from_symbol=EUR

        ❚ Required: to_symbol (str)
            A three-letter symbol from the forex currency list. For example: to_symbol=USD
        """

        url = f'https://www.alphavantage.co/query?function=FX_WEEKLY&from_symbol={from_symbol}&to_symbol={to_symbol}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        time_series = data["Time Series FX (Weekly)"]
        normalized_data = []
        for date, values in time_series.items():
            normalized_data.append({
                "date": date,
                "open": values["1. open"],
                "high": values["2. high"],
                "low": values["3. low"],
                "close": values["4. close"]
            })

        df = pd.DataFrame.from_dict(normalized_data)
        return df
    
    def FX_monthly(self, from_symbol: str, to_symbol: str):
        """
        This API returns the monthly time series (timestamp, open, high, low, close) of the FX currency pair specified, updated realtime.

        The latest data point is the prices information for the month (or partial month) containing the current trading day, updated realtime.

        ❚ Required: from_symbol (str)
            A three-letter symbol from the forex currency list. For example: from_symbol=EUR

        ❚ Required: to_symbol (str)
            A three-letter symbol from the forex currency list. For example: to_symbol=USD
        """

        url = f'https://www.alphavantage.co/query?function=FX_MONTHLY&from_symbol={from_symbol}&to_symbol={to_symbol}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        time_series = data["Time Series FX (Monthly)"]
        normalized_data = []
        for date, values in time_series.items():
            normalized_data.append({
                "date": date,
                "open": values["1. open"],
                "high": values["2. high"],
                "low": values["3. low"],
                "close": values["4. close"]
            })

        df = pd.DataFrame.from_dict(normalized_data)
        return df



    def currency_exchange_rate(self, from_symbol: str, to_symbol: str):
        """
        This API returns the realtime exchange rate for any pair of digital currency (e.g., Bitcoin) or physical currency (e.g., USD).

        ❚ Required: from_currency (str)
            The currency you would like to get the exchange rate for. It can either be a physical currency or digital/crypto currency. For example: from_currency=USD or from_currency=BTC.

        ❚ Required: to_currency (str)
            The destination currency for the exchange rate. It can either be a physical currency or digital/crypto currency. For example: to_currency=USD or to_currency=BTC.
        
        return a json file
        """

        url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_symbol}&to_currency={to_symbol}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()
        return data["Realtime Currency Exchange Rate"]
    
    def crypto_intraday(self, ticker: str, market: str, interval: int, outputsize="compact"):
        """
        This API returns intraday time series (timestamp, open, high, low, close, volume) of the cryptocurrency specified, updated realtime.
        (Premium)

        ❚ Required: ticker (str)
            The digital/crypto currency of your choice. It can be any of the currencies in the digital currency list. For example: ticker=ETH.

        ❚ Required: market (str)
            The exchange market of your choice. It can be any of the market in the market list. For example: market=USD.

        ❚ Required: interval (int)
            Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min

        ❚ Optional: outputsize (str)
            By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points in the intraday time series; full returns the full-length intraday time series. The "compact" option is recommended if you would like to reduce the data size of each API call.
        """

        url = f'https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol={ticker}&market={market}&interval={interval}min&outputsize={outputsize}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        time_series = data[f"Time Series Crypto ({interval}min)"]
        normalized_data = []
        for date, values in time_series.items():
            normalized_data.append({
                "date": date,
                "open": values["1. open"],
                "high": values["2. high"],
                "low": values["3. low"],
                "close": values["4. close"],
                "volume": values["5. volume"]
            })

        df = pd.DataFrame.from_dict(normalized_data)
        return df
    
    def digital_currency_daily(self, ticker: str, market: str):
        """
        This API returns the daily historical time series for a digital currency (e.g., BTC) traded on a specific market (e.g., EUR/Euro), refreshed daily at midnight (UTC). Prices and volumes are quoted in both the market-specific currency and USD.

        ❚ Required: ticker (str)
            The digital/crypto currency of your choice. It can be any of the currencies in the digital currency list. For example: ticker=BTC.

        ❚ Required: market (str)
            The exchange market of your choice. It can be any of the market in the market list. For example: market=EUR.
        """

        url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={ticker}&market={market}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        time_series = data["Time Series (Digital Currency Daily)"]
        normalized_data = []
        for date, values in time_series.items():
            normalized_data.append({
                "date": date,
                "open": values["1. open"],
                "high": values["2. high"],
                "low": values["3. low"],
                "close": values["4. close"],
                "volume": values["5. volume"]
            })

        df = pd.DataFrame.from_dict(normalized_data)
        return df
    
    def digital_currency_weekly(self, ticker: str, market: str):
        """
        This API returns the weekly historical time series for a digital currency (e.g., BTC) traded on a specific market (e.g., EUR/Euro), refreshed daily at midnight (UTC). Prices and volumes are quoted in both the market-specific currency and USD.

        ❚ Required: ticker (str)
            The digital/crypto currency of your choice. It can be any of the currencies in the digital currency list. For example: ticker=BTC.

        ❚ Required: market (str)
            The exchange market of your choice. It can be any of the market in the market list. For example: market=EUR.
        """

        url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_WEEKLY&symbol={ticker}&market={market}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        time_series = data["Time Series (Digital Currency Weekly)"]
        normalized_data = []
        for date, values in time_series.items():
            normalized_data.append({
                "date": date,
                "open": values["1. open"],
                "high": values["2. high"],
                "low": values["3. low"],
                "close": values["4. close"],
                "volume": values["5. volume"]
            })

        df = pd.DataFrame.from_dict(normalized_data)
        return df
    
    def digital_currency_monthly(self, ticker: str, market: str):
        """
        This API returns the monthly historical time series for a digital currency (e.g., BTC) traded on a specific market (e.g., EUR/Euro), refreshed daily at midnight (UTC). Prices and volumes are quoted in both the market-specific currency and USD.

        ❚ Required: ticker (str)
            The digital/crypto currency of your choice. It can be any of the currencies in the digital currency list. For example: ticker=BTC.

        ❚ Required: market (str)
            The exchange market of your choice. It can be any of the market in the market list. For example: market=EUR.
        """
        url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_WEEKLY&symbol={ticker}&market={market}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        time_series = data["Time Series (Digital Currency Monthly)"]
        normalized_data = []
        for date, values in time_series.items():
            normalized_data.append({
                "date": date,
                "open": values["1. open"],
                "high": values["2. high"],
                "low": values["3. low"],
                "close": values["4. close"],
                "volume": values["5. volume"]
            })

        df = pd.DataFrame.from_dict(normalized_data)
        return df



    def WTI(self, interval="monthly"):
        """
        This API returns the West Texas Intermediate (WTI) crude oil prices in daily, weekly, and monthly horizons.
        Source: U.S. Energy Information Administration, Crude Oil Prices: West Texas Intermediate (WTI) - Cushing, Oklahoma, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

        ❚ Optional: interval (str)
            By default, interval=monthly. Strings daily, weekly, and monthly are accepted.
        """

        url = f'https://www.alphavantage.co/query?function=WTI&interval={interval}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        df.columns = ["date", "value"]
        return df
    
    def BRENT(self, interval="monthly"):
        """
        This API returns the Brent (Europe) crude oil prices in daily, weekly, and monthly horizons.
        Source: U.S. Energy Information Administration, Crude Oil Prices: Brent - Europe, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

        ❚ Optional: interval (str)
            By default, interval=monthly. Strings daily, weekly, and monthly are accepted.
        """

        url = f'https://www.alphavantage.co/query?function=BRENT&interval={interval}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        df.columns = ["date", "value"]
        return df
    
    def Natural_Gas(self, interval="monthly"):
        """
        This API returns the Henry Hub natural gas spot prices in daily, weekly, and monthly horizons.
        Source: U.S. Energy Information Administration, Henry Hub Natural Gas Spot Price, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.
        
        ❚ Optional: interval (str)
            By default, interval=monthly. Strings daily, weekly, and monthly are accepted.
        """

        url = f'https://www.alphavantage.co/query?function=NATURAL_GAS&interval={interval}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        df.columns = ["date", "value"]
        return df
    
    def Copper(self, interval="monthly"):
        """
        This API returns the global price of copper in monthly, quarterly, and annual horizons.
        Source: International Monetary Fund (IMF Terms of Use), Global price of Copper, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.
        
        ❚ Optional: interval (str)
            By default, interval=monthly. Strings daily, weekly, and monthly are accepted.
        """

        url = f'https://www.alphavantage.co/query?function=COPPER&interval={interval}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        df.columns = ["date", "value"]
        return df
    
    def Aluminium(self, interval="monthly"):
        """
        This API returns the global price of aluminum in monthly, quarterly, and annual horizons.
        Source: International Monetary Fund (IMF Terms of Use), Global price of Aluminum, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.
        
        ❚ Optional: interval (str)
            By default, interval=monthly. Strings daily, weekly, and monthly are accepted.
        """

        url = f'https://www.alphavantage.co/query?function=ALUMINUM&interval={interval}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        df.columns = ["date", "value"]
        return df
    
    def Wheat(self, interval="monthly"):
        """
        This API returns the global price of wheat in monthly, quarterly, and annual horizons.
        Source: International Monetary Fund (IMF Terms of Use), Global price of Wheat, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.
        
        ❚ Optional: interval (str)
            By default, interval=monthly. Strings daily, weekly, and monthly are accepted.
        """

        url = f'https://www.alphavantage.co/query?function=WHEAT&interval={interval}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        df.columns = ["date", "value"]
        return df
    
    def Corn(self, interval="monthly"):
        """
        This API returns the global price of corn in monthly, quarterly, and annual horizons.
        Source: International Monetary Fund (IMF Terms of Use), Global price of Corn, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.
        
        ❚ Optional: interval (str)
            By default, interval=monthly. Strings daily, weekly, and monthly are accepted.
        """

        url = f'https://www.alphavantage.co/query?function=CORN&interval={interval}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        df.columns = ["date", "value"]
        return df
    
    def Cotton(self, interval="monthly"):
        """
        This API returns the global price of cotton in monthly, quarterly, and annual horizons.
        Source: International Monetary Fund (IMF Terms of Use), Global price of Cotton, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.
        
        ❚ Optional: interval (str)
            By default, interval=monthly. Strings daily, weekly, and monthly are accepted.
        """

        url = f'https://www.alphavantage.co/query?function=COTTON&interval={interval}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        df.columns = ["date", "value"]
        return df
    
    def Sugar(self, interval="monthly"):
        """
        This API returns the global price of sugar in monthly, quarterly, and annual horizons.
        Source: International Monetary Fund (IMF Terms of Use), Global price of Sugar, No. 11, World, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.
        
        ❚ Optional: interval (str)
            By default, interval=monthly. Strings daily, weekly, and monthly are accepted.
        """

        url = f'https://www.alphavantage.co/query?function=SUGAR&interval={interval}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        df.columns = ["date", "value"]
        return df
    
    def Coffee(self, interval="monthly"):
        """
        This API returns the global price of coffee in monthly, quarterly, and annual horizons.
        Source: International Monetary Fund (IMF Terms of Use), Global price of Coffee, Other Mild Arabica, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.
        
        ❚ Optional: interval (str)
            By default, interval=monthly. Strings daily, weekly, and monthly are accepted.
        """

        url = f'https://www.alphavantage.co/query?function=WTI&interval={interval}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        df.columns = ["date", "value"]
        return df

    def Price_index_all_commodities(self, interval="monthly"):
        """
        This API returns the global price index of all commodities in monthly, quarterly, and annual temporal dimensions.
        Source: International Monetary Fund (IMF Terms of Use), Global Price Index of All Commodities, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.
        
        ❚ Optional: interval (str)
            By default, interval=monthly. Strings daily, weekly, and monthly are accepted.
        """

        url = f'https://www.alphavantage.co/query?function=ALL_COMMODITIES&interval={interval}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        df.columns = ["date", "value"]
        return df



    def real_gdp(self, internal="annual"):
        """
        This API returns the annual and quarterly Real GDP of the United States.
        Source: U.S. Bureau of Economic Analysis, Real Gross Domestic Product, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

        ❚ Optional: interval (str)
            By default, interval=annual. Strings quarterly and annual are accepted.
        """
        url = f'https://www.alphavantage.co/query?function=REAL_GDP&interval={internal}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        df.columns = ["date", "value"]
        return df
    
    def real_gdp_per_capita(self):
        """
        This API returns the quarterly Real GDP per Capita data of the United States.
        Source: U.S. Bureau of Economic Analysis, Real gross domestic product per capita, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.
        """

        url = f'https://www.alphavantage.co/query?function=REAL_GDP_PER_CAPITA&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        df.columns = ["data", "value"]
        return df

    def treasury_yield(self, interval="monthly", maturity="10year"):
        """
        This API returns the daily, weekly, and monthly US treasury yield of a given maturity timeline (e.g., 5 year, 30 year, etc).
        Source: Board of Governors of the Federal Reserve System (US), Market Yield on U.S. Treasury Securities at 3-month, 2-year, 5-year, 7-year, 10-year, and 30-year Constant Maturities, Quoted on an Investment Basis, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

        ❚ Optional: interval (str)
            By default, interval=monthly. Strings daily, weekly, and monthly are accepted.

        ❚ Optional: maturity (str)
            By default, maturity=10year. Strings 3month, 2year, 5year, 7year, 10year, and 30year are accepted.
        """
        url = f'https://www.alphavantage.co/query?function=TREASURY_YIELD&interval={interval}&maturity={maturity}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        df.columns = ["date", "value"]
        return df
  
    def federal_funds_rate(self, interval="monthly"):
        """
        This API returns the daily, weekly, and monthly federal funds rate (interest rate) of the United States.
        Source: Board of Governors of the Federal Reserve System (US), Federal Funds Effective Rate, retrieved from FRED, Federal Reserve Bank of St. Louis (https://fred.stlouisfed.org/series/FEDFUNDS). This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

        ❚ Optional: interval (str)
            By default, interval=monthly. Strings daily, weekly, and monthly are accepted.
        """

        url = f'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval={interval}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        df.columns = ["date", "value"]
        return df

    def consumer_price_index(self, interval="monthly"):
        """
        This API returns the monthly and semiannual consumer price index (CPI) of the United States. CPI is widely regarded as the barometer of inflation levels in the broader economy.
        Source: U.S. Bureau of Labor Statistics, Consumer Price Index for All Urban Consumers: All Items in U.S. City Average, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

        ❚ Optional: interval (str)
            By default, interval=monthly. Strings monthly and semiannual are accepted.
        """

        url = f'https://www.alphavantage.co/query?function=CPI&interval={interval}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        df.columns = ["date", "value"]
        return df
    
    def inflation(self):
        """
        This API returns the annual inflation rates (consumer prices) of the United States
        Source: World Bank, Inflation, consumer prices for the United States, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.
        """
        url = f'https://www.alphavantage.co/query?function=INFLATION&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        df.columns = ["date", "value"]
        return df
    
    def retail_sales(self):
        """
        This API returns the monthly Advance Retail Sales: Retail Trade data of the United States.
        Source: U.S. Census Bureau, Advance Retail Sales: Retail Trade, retrieved from FRED, Federal Reserve Bank of St. Louis (https://fred.stlouisfed.org/series/RSXFSN). This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.
        """

        url = f'https://www.alphavantage.co/query?function=RETAIL_SALES&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        df.columns = ["date", "value"]
        return df

    def durables(self):
        """
        This API returns the monthly manufacturers' new orders of durable goods in the United States.
        Source: U.S. Census Bureau, Manufacturers' New Orders: Durable Goods, retrieved from FRED, Federal Reserve Bank of St. Louis (https://fred.stlouisfed.org/series/UMDMNO). This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.
        """

        url = f'https://www.alphavantage.co/query?function=DURABLES&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        df.columns = ["date", "value"]
        return df
    
    def unemployment(self):
        """
        This API returns the monthly unemployment data of the United States. The unemployment rate represents the number of unemployed as a percentage of the labor force. Labor force data are restricted to people 16 years of age and older, who currently reside in 1 of the 50 states or the District of Columbia, who do not reside in institutions (e.g., penal and mental facilities, homes for the aged), and who are not on active duty in the Armed Forces (source).
        Source: U.S. Bureau of Labor Statistics, Unemployment Rate, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.
        """

        url = f'https://www.alphavantage.co/query?function=UNEMPLOYMENT&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        df.columns = ["date", "value"]
        return df
    
    def nonfarm_payroll(self):
        """
        This API returns the monthly US All Employees: Total Nonfarm (commonly known as Total Nonfarm Payroll), a measure of the number of U.S. workers in the economy that excludes proprietors, private household employees, unpaid volunteers, farm employees, and the unincorporated self-employed.

        Source: U.S. Bureau of Labor Statistics, All Employees, Total Nonfarm, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.
        """
        url = f'https://www.alphavantage.co/query?function=NONFARM_PAYROLL&apikey={self.api}'
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame.from_dict(data["data"])
        df.columns = ["date", "value"]
        return df
