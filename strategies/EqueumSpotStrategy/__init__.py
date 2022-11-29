from datetime import datetime
from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils
import numpy as np
import pandas as pd
import jesse.helpers as jh
import requests


class EqueumSpotStrategy(Strategy):
        
    def before(self):
        # load equeum signal for current candle
        self.populate_equeum_signal()
    
    def should_long(self) -> bool:
        return self.equeum_trendline == 'up'

    def go_long(self):
        entry = self.price
        # no more then $100 per trade
        # position = min(self.balance, 100)
        qty = utils.size_to_qty(self.balance, entry)
        
        self.buy = qty, entry

    def should_short(self) -> bool:
        return False

    def go_short(self):
        pass
        
    def update_position(self):
        # trend went down, close long
        if self.is_long and self.equeum_trendline == 'down':
            self.liquidate()
        # trend went up, close short
        elif self.is_short and self.equeum_trendline == 'up':
            self.liquidate()

    def should_cancel_entry(self) -> bool:
        return True


    ################################################################
    # # # # # # # # # # # # #   EQUEUM   # # # # # # # # # # # # # #
    ################################################################
    
    _equeum_token = "GET YOUR TOKEN AT HTTPS://APP.EQUEUM.COM"
    
    """
    Equeum forecast for selected symbol
    Returns:
        string: trend is 'up' or 'down', 'unknown' in case of error
    """        
    @property
    def equeum_trendline(self) -> str:
        if ('trendline' in self._last_equeum):
            return self._last_equeum['trendline']
        else: return "unknown"
        
    
    def populate_equeum_signal(self):
        if(jh.is_live()):
            return self._equeum_live()
        elif (jh.is_backtesting()):
            return self._equeum_backtest()
    
    # # # # # # # # # # # # #   private   # # # # # # # # # # # # # #
    
    _last_equeum = {}
    _equeum_history = None
    _equeum_api_endpoint = "https://graphql-apis.equeum.com/resources/signals"
    _equeum_symbol_map = {
        "1000SHIB": "SHIB",
    }
    
    def _equeum_extract_symbol(self, symbol):
        ticker = symbol.split('-')[0]
        if ticker in self._equeum_symbol_map:
            return self._equeum_symbol_map[ticker]

        return ticker
    
    def _equeum_live(self):        
        # extract ticker
        ticker = self._equeum_extract_symbol(self.symbol)
            
        # request data to API
        params = {
            "timeFormat": "unix",
            "r": ticker,
            "token": self._equeum_token,
            "resFormat": "json"
        }
        
        self.log(f"equeum: requesting {self._equeum_api_endpoint} with payload: {params}")

        res = requests.get(self._equeum_api_endpoint, params)
        parsed_res = res.json()
        
        self.log(f"equeum: response: {res.status_code} = {parsed_res}")
        
        # validate response
        if ('status' in parsed_res and parsed_res['status'] == 'error'):
            self.log("Equeum Exception -> " + parsed_res['error'], "error", True)
            self._last_equeum = {}
        else: self._last_equeum = parsed_res[0]
        
        
    def _equeum_backtest(self):
        
        # load data on first run
        if (self._equeum_history is None):
            self._equeum_preload_history_data()
            
        # extract timestamp from latest candle
        last_candle = self.candles[-1]
        candle_timestamp = int(last_candle[0] / 1000)
        
        self.log(f"searching candle: {candle_timestamp}")
        
        # get equeum history data and map it to object
        self._last_equeum = self._equeum_get_signal_by_time(candle_timestamp)
        
    def _equeum_get_signal_by_time(self, timestamp):
        if timestamp in self._equeum_history:
            return self._equeum_history[timestamp]
        else: return {}
        
    def _equeum_preload_history_data(self):
        ticker = self._equeum_extract_symbol(self.symbol)
        
        # TODO: replace with real backtesting dates
        params = {
            "r": f"{ticker}",
            'from': 1640995200,
            'to': 1704067200,
            "token": self._equeum_token,
            "resFormat": "json",
            "timeFormat": "unix"
        }
        
        self.log(f"equeum: requesting: {self._equeum_api_endpoint} with payload: {params}")

        res = requests.get(self._equeum_api_endpoint, params)
        parsed_res = res.json()
        
        # validate response
        if ('status' in parsed_res and parsed_res['status'] == 'error'):
            raise Exception("Equeum Exception -> " + parsed_res['error'])
        
        # expand dataframe
        history_df = pd.DataFrame(data=parsed_res)
        self.log(f"equeum: before expand history_df.shape {history_df.shape}")
        
        history_df['date'] = pd.to_datetime(history_df['time'], unit='s', utc=True)
        history_df = history_df.set_index('date')
        history_df = history_df.asfreq(freq="1min", method='ffill')
        history_df = history_df.reset_index()
        history_df['time'] = history_df['date'].values.astype(np.int64) // 10 ** 9
        
        history_dict = history_df.to_dict(orient='records')
        
        self.log(f"equeum: after expand history_df.shape {history_df.shape}")
        
        # map response
        self._equeum_history = {}
        for eq in history_dict:
            self._equeum_history[eq['time']] = eq
        
        self.log(f"equeum: history response: {res.status_code} = {len(self._equeum_history)}")