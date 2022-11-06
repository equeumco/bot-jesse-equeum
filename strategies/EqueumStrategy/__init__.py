from datetime import datetime
from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils
import numpy as np
import jesse.helpers as jh
import requests


class EqueumStrategy(Strategy):
        
    def before(self):
        # load equeum signal for current candle
        self.populate_equeum_signal()
    
    def should_long(self) -> bool:
        return self.equeum_trendline == 'up'

    def go_long(self):
        entry = self.price
        # no more then $100 per trade
        position = min(self.balance, 100)
        qty = utils.size_to_qty(position, entry)
        
        self.buy = qty, entry

    def should_short(self) -> bool:
        return self.equeum_trendline == 'down'

    def go_short(self):
        entry = self.price
        # no more then $100 per trade
        position = min(self.balance, 100)
        qty = utils.size_to_qty(position, entry)
        
        self.sell = qty, entry
        
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
    
    _equeum_token = "<PUT HERE YOUR EQUEUM TOKEN>"
    
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
    _equeum_api_endpoint = "https://graphql-apis.equeum.com/tickers/"
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
            "ticker": ticker,
            "token": self._equeum_token
        }
        
        self.log(f"equeum: requesting {self._equeum_api_endpoint} with payload: {params}")

        res = requests.get(self._equeum_api_endpoint + "signals", params)
        parsed_res = res.json()
        
        # validate response
        if ('status' in parsed_res and parsed_res['status'] == 'error'):
            self.log("Equeum Exception -> " + parsed_res['error'], "error", True)
            self._last_equeum = {}
        else: self._last_equeum = parsed_res
        
        self.log(f"equeum: response: {res.status_code} = {self._last_equeum}")
        
        
    def _equeum_backtest(self):
        ticker = self._equeum_extract_symbol(self.symbol)
        
        # load data on first run
        if (self._equeum_history is None):
            self._equeum_preload_history_data()
            
        # extract timestamp from latest candle
        last_candle = self.candles[-1]
        candle_timestamp = int(last_candle[0] / 1000)
        
        # get equeum history data and map it to object
        eq_data = self._equeum_get_signal_by_time(candle_timestamp)
        if (eq_data is not None):
            self._last_equeum = {
                'trendline': 'up' if eq_data['forecast'] > 0 else 'down',
                'ticker': ticker,
                'timestamp': datetime.utcfromtimestamp(candle_timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                'lastUpdate': None,
                'duration': '', 
                'value': eq_data['forecast']
            }
        
    def _equeum_get_signal_by_time(self, timestamp):
        for e in self._equeum_history:
            if (e['time'] == timestamp):
                return e
            
        return None
        
    def _equeum_preload_history_data(self):
        ticker = self._equeum_extract_symbol(self.symbol)
        
        # request data to API
        endpoint = self._equeum_api_endpoint + "history"
        
        # TODO: replace with real backtesting dates
        params = {
            "ticker": f"{ticker}",
            'from': 1640995200,
            'to': 1704067200,
            "token": self._equeum_token
        }
        
        self.log(f"equeum: requesting: {self._equeum_api_endpoint} with payload: {params}")

        res = requests.get(endpoint, params)
        parsed_res = res.json()
        
        # validate response
        if ('status' in parsed_res and parsed_res['status'] == 'error'):
            raise Exception("Equeum Exception -> " + parsed_res['error'])
        else: self._equeum_history = np.array(parsed_res)
        
        self.log(f"equeum: history response: {res.status_code} = {self._equeum_history}")