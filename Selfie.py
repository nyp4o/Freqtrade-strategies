# --- Hyperopt buy_params as generated/placed by Freqtrade optimizer ---
buy_params = {
        "adx_entry_long_thresh": 15,
        "adx_exit_short_thresh": 17,
        "adx_period": 7,
        "bbands_std": 2.336,
        "bbands_window": 10,
        "cci_entry_long_thresh": -119,
        "cci_exit_short_thresh": -146,
        "cci_period": 17,
        "macd_fast": 10,
        "macd_signal": 6,
        "macd_slow": 14,
        "mfi_entry_long_thresh": 39,
        "mfi_exit_short_thresh": 30,
        "mfi_period": 13,
        "rsi_entry_long_thresh": 36,
        "rsi_exit_short_thresh": 15,
        "rsi_period": 11,
        "sar_af": 0.01,
        "sar_max": 0.27,
        "stoch_d": 3,
        "stoch_k": 14,
        "use_adx_mode": 1,
        "use_bbands_mode": 14,
        "use_cci_mode": 0,
        "use_htsine_mode": 4,
        "use_macd_mode": 1,
        "use_mfi_mode": 7,
        "use_rsi_mode": 5,
        "use_sar_mode": 9,
        "use_stoch_mode": 14,
        "adx_entry_short_thresh": 22,
        "adx_exit_long_thresh": 16,
        "cci_entry_short_thresh": 125,
        "cci_exit_long_thresh": 60,
        "mfi_entry_short_thresh": 80,
        "mfi_exit_long_thresh": 70,
        "rsi_entry_short_thresh": 62,
        "rsi_exit_long_thresh": 71,
        "leverage_opt": 1
}

# --- Optimization global switches ---
Indicator_optimize = True
Optimize_use = True

from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta
import numpy as np
from freqtrade.strategy import IntParameter, DecimalParameter
from datetime import datetime


class Selfie(IStrategy):


    INTERFACE_VERSION = 3
    minimal_roi = {
        "0": 0.02,
        "10": 0.01,
        "60": 0
    }
    stoploss = -0.1
    timeframe = '5m'

    # Битова маска: 1=Long, 2=Short, 4=Entry, 8=Exit

    use_rsi_mode = IntParameter(0, 15, default=buy_params['use_rsi_mode'], space="buy", optimize=Optimize_use)
    use_macd_mode = IntParameter(0, 15, default=buy_params['use_macd_mode'], space="buy", optimize=Optimize_use)
    use_stoch_mode = IntParameter(0, 15, default=buy_params['use_stoch_mode'], space="buy", optimize=Optimize_use)
    use_bbands_mode = IntParameter(0, 15, default=buy_params['use_bbands_mode'], space="buy", optimize=Optimize_use)
    use_adx_mode = IntParameter(0, 15, default=buy_params['use_adx_mode'], space="buy", optimize=Optimize_use)
    use_mfi_mode = IntParameter(0, 15, default=buy_params['use_mfi_mode'], space="buy", optimize=Optimize_use)
    use_cci_mode = IntParameter(0, 15, default=buy_params['use_cci_mode'], space="buy", optimize=Optimize_use)
    use_sar_mode = IntParameter(0, 15, default=buy_params['use_sar_mode'], space="buy", optimize=Optimize_use)
    use_htsine_mode = IntParameter(0, 15, default=buy_params['use_htsine_mode'], space="buy", optimize=Optimize_use)

        # RSI (по-стегнати граници за скалпинг)
    rsi_period = IntParameter(7, 16, default=buy_params['rsi_period'], space="buy", optimize=Indicator_optimize)
    rsi_entry_long_thresh = IntParameter(30, 45, default=buy_params['rsi_entry_long_thresh'], space="buy", optimize=Indicator_optimize)
    rsi_exit_long_thresh = IntParameter(55, 75, default=buy_params['rsi_exit_long_thresh'], space="sell", optimize=Indicator_optimize)
    rsi_entry_short_thresh = IntParameter(60, 80, default=buy_params['rsi_entry_short_thresh'], space="sell", optimize=Indicator_optimize)
    rsi_exit_short_thresh = IntParameter(15, 40, default=buy_params['rsi_exit_short_thresh'], space="buy", optimize=Indicator_optimize)

    # MACD (по-реактивен за скалпинг)
    macd_fast = IntParameter(6, 14, default=buy_params['macd_fast'], space="buy", optimize=Indicator_optimize)
    macd_slow = IntParameter(12, 24, default=buy_params['macd_slow'], space="buy", optimize=Indicator_optimize)
    macd_signal = IntParameter(5, 10, default=buy_params['macd_signal'], space="buy", optimize=Indicator_optimize)

    # Stochastic
    stoch_k = IntParameter(5, 14, default=buy_params['stoch_k'], space="buy", optimize=Indicator_optimize)
    stoch_d = IntParameter(3, 7, default=buy_params['stoch_d'], space="buy", optimize=Indicator_optimize)

    # Bollinger Bands
    bbands_window = IntParameter(10, 22, default=buy_params['bbands_window'], space="buy", optimize=Indicator_optimize)
    bbands_std = DecimalParameter(1.5, 2.5, default=buy_params['bbands_std'], space="buy", optimize=Indicator_optimize)

    # ADX
    adx_period = IntParameter(7, 14, default=buy_params['adx_period'], space="buy", optimize=Indicator_optimize)
    adx_entry_long_thresh = IntParameter(10, 25, default=buy_params['adx_entry_long_thresh'], space="buy", optimize=Indicator_optimize)
    adx_exit_long_thresh = IntParameter(10, 25, default=buy_params['adx_exit_long_thresh'], space="sell", optimize=Indicator_optimize)
    adx_entry_short_thresh = IntParameter(10, 25, default=buy_params['adx_entry_short_thresh'], space="sell", optimize=Indicator_optimize)
    adx_exit_short_thresh = IntParameter(10, 25, default=buy_params['adx_exit_short_thresh'], space="buy", optimize=Indicator_optimize)

    # MFI
    mfi_period = IntParameter(7, 16, default=buy_params['mfi_period'], space="buy", optimize=Indicator_optimize)
    mfi_entry_long_thresh = IntParameter(20, 40, default=buy_params['mfi_entry_long_thresh'], space="buy", optimize=Indicator_optimize)
    mfi_exit_long_thresh = IntParameter(60, 80, default=buy_params['mfi_exit_long_thresh'], space="sell", optimize=Indicator_optimize)
    mfi_entry_short_thresh = IntParameter(60, 80, default=buy_params['mfi_entry_short_thresh'], space="sell", optimize=Indicator_optimize)
    mfi_exit_short_thresh = IntParameter(20, 40, default=buy_params['mfi_exit_short_thresh'], space="buy", optimize=Indicator_optimize)

    # CCI
    cci_period = IntParameter(7, 20, default=buy_params['cci_period'], space="buy", optimize=Indicator_optimize)
    cci_entry_long_thresh = IntParameter(-150, -50, default=buy_params['cci_entry_long_thresh'], space="buy", optimize=Indicator_optimize)
    cci_exit_long_thresh = IntParameter(50, 150, default=buy_params['cci_exit_long_thresh'], space="sell", optimize=Indicator_optimize)
    cci_entry_short_thresh = IntParameter(50, 150, default=buy_params['cci_entry_short_thresh'], space="sell", optimize=Indicator_optimize)
    cci_exit_short_thresh = IntParameter(-150, -50, default=buy_params['cci_exit_short_thresh'], space="buy", optimize=Indicator_optimize)

    # SAR
    sar_af = DecimalParameter(0.01, 0.05, default=buy_params['sar_af'], decimals=2, space="buy", optimize=Indicator_optimize)
    sar_max = DecimalParameter(0.1, 0.3, default=buy_params['sar_max'], decimals=2, space="buy", optimize=Indicator_optimize)

    leverage_opt = IntParameter(1, 5, default=buy_params["leverage_opt"], space="buy", optimize=Indicator_optimize)

    @property
    def protections(self):
        return [
            {
                "method": "CooldownPeriod",
                "stop_duration_candles": 2  # само 10 минути пауза
            },
            {
                "method": "MaxDrawdown",
                "lookback_period_candles": 24,  # 2 часа назад
                "trade_limit": 10,
                "stop_duration_candles": 2,  # 10 минути стоп след drawdown
                "max_allowed_drawdown": 0.15  # по-строго за скалпинг
            },
            {
                "method": "StoplossGuard",
                "lookback_period_candles": 12,  # 1 час назад
                "trade_limit": 2,
                "stop_duration_candles": 2,
                "only_per_pair": True  # по-добре само за всяка двойка
            },
            {
                "method": "LowProfitPairs",
                "lookback_period_candles": 3,  # 15 мин назад
                "trade_limit": 2,
                "stop_duration_candles": 20,  # 100 минути стоп
                "required_profit": 0.01  # 1% е по-реалистично за скалпинг
            },
            {
                "method": "LowProfitPairs",
                "lookback_period_candles": 24,  # 2 часа
                "trade_limit": 4,
                "stop_duration_candles": 2,  # 10 минути
                "required_profit": 0.005  # 0.5% за по-мек филтър
            }
        ]

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI
        if self.use_rsi_mode.value > 0:
            # noinspection PyUnresolvedReferences
            dataframe["rsi"] = ta.RSI(dataframe, timeperiod=self.rsi_period.value)
        # MACD
        if self.use_macd_mode.value > 0:
            # noinspection PyUnresolvedReferences
            macd = ta.MACD(
                dataframe,
                fastperiod=self.macd_fast.value,
                slowperiod=self.macd_slow.value,
                signalperiod=self.macd_signal.value
            )
            dataframe["macd"] = macd["macd"]
            dataframe["macdsignal"] = macd["macdsignal"]
        # Stochastic
        if self.use_stoch_mode.value > 0:
            # noinspection PyUnresolvedReferences
            stoch = ta.STOCHF(
                dataframe,
                fastk_period=self.stoch_k.value,
                fastd_period=self.stoch_d.value,
                fastd_matype=0
            )
            dataframe["fastk"] = stoch["fastk"]
            dataframe["fastd"] = stoch["fastd"]
        # Bollinger Bands
        if self.use_bbands_mode.value > 0:
            bbands = self.calculate_bollinger_bands(
                dataframe,
                window=self.bbands_window.value,
                stds=self.bbands_std.value
            )
            dataframe["bb_upperband"] = bbands["upper"]
            dataframe["bb_lowerband"] = bbands["lower"]
            dataframe["bb_middleband"] = bbands["mid"]
        # ADX
        if self.use_adx_mode.value > 0:
            # noinspection PyUnresolvedReferences
            dataframe["adx"] = ta.ADX(dataframe, timeperiod=self.adx_period.value)
        # MFI
        if self.use_mfi_mode.value > 0:
            # noinspection PyUnresolvedReferences
            dataframe["mfi"] = ta.MFI(dataframe, timeperiod=self.mfi_period.value)
        # CCI
        if self.use_cci_mode.value > 0:
            # noinspection PyUnresolvedReferences
            dataframe["cci"] = ta.CCI(dataframe, timeperiod=self.cci_period.value)
        # SAR
        if self.use_sar_mode.value > 0:
            # noinspection PyUnresolvedReferences
            dataframe["sar"] = ta.SAR(
                dataframe,
                acceleration=self.sar_af.value,
                maximum=self.sar_max.value
            )
        # HTSINE
        if self.use_htsine_mode.value > 0:
            # noinspection PyUnresolvedReferences
            htsine = ta.HT_SINE(dataframe)
            dataframe["htsine"] = htsine["sine"]
            dataframe["htleadsine"] = htsine["leadsine"]
        return dataframe

    @staticmethod
    def calculate_bollinger_bands(dataframe: DataFrame, window: int, stds: float):
        tp = (dataframe["high"] + dataframe["low"] + dataframe["close"]) / 3
        mid = tp.rolling(window).mean()
        std = tp.rolling(window).std()
        upper = mid + stds * std
        lower = mid - stds * std
        return {"mid": mid, "upper": upper, "lower": lower}

    # noinspection PyUnusedLocal
    def build_entry_conditions_long(self, dataframe: DataFrame, metadata: dict) -> list:
        conditions = []
        if (self.use_rsi_mode.value & 1) and (self.use_rsi_mode.value & 4):
            conditions.append(dataframe["rsi"] < self.rsi_entry_long_thresh.value)
        if (self.use_macd_mode.value & 1) and (self.use_macd_mode.value & 4):
            conditions.append(dataframe["macd"] > dataframe["macdsignal"])
        if (self.use_stoch_mode.value & 1) and (self.use_stoch_mode.value & 4):
            conditions.append((dataframe["fastk"] < 30) & (dataframe["fastd"] < 30))
        if (self.use_bbands_mode.value & 1) and (self.use_bbands_mode.value & 4):
            conditions.append(dataframe["close"] < dataframe["bb_lowerband"])
        if (self.use_adx_mode.value & 1) and (self.use_adx_mode.value & 4):
            conditions.append(dataframe["adx"] > self.adx_entry_long_thresh.value)
        if (self.use_mfi_mode.value & 1) and (self.use_mfi_mode.value & 4):
            conditions.append(dataframe["mfi"] < self.mfi_entry_long_thresh.value)
        if (self.use_cci_mode.value & 1) and (self.use_cci_mode.value & 4):
            conditions.append(dataframe["cci"] < self.cci_entry_long_thresh.value)
        if (self.use_sar_mode.value & 1) and (self.use_sar_mode.value & 4):
            conditions.append(dataframe["sar"] > dataframe["close"])
        if (self.use_htsine_mode.value & 1) and (self.use_htsine_mode.value & 4):
            conditions.append(dataframe["htsine"] < dataframe["htleadsine"])
        return conditions

    # noinspection PyUnusedLocal
    def build_exit_conditions_long(self, dataframe: DataFrame, metadata: dict) -> list:
        conditions = []
        if (self.use_rsi_mode.value & 1) and (self.use_rsi_mode.value & 8):
            conditions.append(dataframe["rsi"] > self.rsi_exit_long_thresh.value)
        if (self.use_macd_mode.value & 1) and (self.use_macd_mode.value & 8):
            conditions.append(dataframe["macd"] < dataframe["macdsignal"])
        if (self.use_stoch_mode.value & 1) and (self.use_stoch_mode.value & 8):
            conditions.append((dataframe["fastk"] > 70) & (dataframe["fastd"] > 70))
        if (self.use_bbands_mode.value & 1) and (self.use_bbands_mode.value & 8):
            conditions.append(dataframe["close"] > dataframe["bb_upperband"])
        if (self.use_adx_mode.value & 1) and (self.use_adx_mode.value & 8):
            conditions.append(dataframe["adx"] < self.adx_exit_long_thresh.value)
        if (self.use_mfi_mode.value & 1) and (self.use_mfi_mode.value & 8):
            conditions.append(dataframe["mfi"] > self.mfi_exit_long_thresh.value)
        if (self.use_cci_mode.value & 1) and (self.use_cci_mode.value & 8):
            conditions.append(dataframe["cci"] > self.cci_exit_long_thresh.value)
        if (self.use_sar_mode.value & 1) and (self.use_sar_mode.value & 8):
            conditions.append(dataframe["sar"] < dataframe["close"])
        if (self.use_htsine_mode.value & 1) and (self.use_htsine_mode.value & 8):
            conditions.append(dataframe["htsine"] > dataframe["htleadsine"])
        return conditions

    # noinspection PyUnusedLocal
    def build_entry_conditions_short(self, dataframe: DataFrame, metadata: dict) -> list:
        conditions = []
        if (self.use_rsi_mode.value & 2) and (self.use_rsi_mode.value & 4):
            conditions.append(dataframe["rsi"] > self.rsi_entry_short_thresh.value)
        if (self.use_macd_mode.value & 2) and (self.use_macd_mode.value & 4):
            conditions.append(dataframe["macd"] < dataframe["macdsignal"])
        if (self.use_stoch_mode.value & 2) and (self.use_stoch_mode.value & 4):
            conditions.append((dataframe["fastk"] > 70) & (dataframe["fastd"] > 70))
        if (self.use_bbands_mode.value & 2) and (self.use_bbands_mode.value & 4):
            conditions.append(dataframe["close"] > dataframe["bb_upperband"])
        if (self.use_adx_mode.value & 2) and (self.use_adx_mode.value & 4):
            conditions.append(dataframe["adx"] > self.adx_entry_short_thresh.value)
        if (self.use_mfi_mode.value & 2) and (self.use_mfi_mode.value & 4):
            conditions.append(dataframe["mfi"] > self.mfi_entry_short_thresh.value)
        if (self.use_cci_mode.value & 2) and (self.use_cci_mode.value & 4):
            conditions.append(dataframe["cci"] > self.cci_entry_short_thresh.value)
        if (self.use_sar_mode.value & 2) and (self.use_sar_mode.value & 4):
            conditions.append(dataframe["sar"] > dataframe["close"])
        if (self.use_htsine_mode.value & 2) and (self.use_htsine_mode.value & 4):
            conditions.append(dataframe["htsine"] > dataframe["htleadsine"])
        return conditions

    # noinspection PyUnusedLocal
    def build_exit_conditions_short(self, dataframe: DataFrame, metadata: dict)  -> list:
        conditions = []
        if (self.use_rsi_mode.value & 2) and (self.use_rsi_mode.value & 8):
            conditions.append(dataframe["rsi"] < self.rsi_exit_short_thresh.value)
        if (self.use_macd_mode.value & 2) and (self.use_macd_mode.value & 8):
            conditions.append(dataframe["macd"] > dataframe["macdsignal"])
        if (self.use_stoch_mode.value & 2) and (self.use_stoch_mode.value & 8):
            conditions.append((dataframe["fastk"] < 30) & (dataframe["fastd"] < 30))
        if (self.use_bbands_mode.value & 2) and (self.use_bbands_mode.value & 8):
            conditions.append(dataframe["close"] < dataframe["bb_lowerband"])
        if (self.use_adx_mode.value & 2) and (self.use_adx_mode.value & 8):
            conditions.append(dataframe["adx"] < self.adx_exit_short_thresh.value)
        if (self.use_mfi_mode.value & 2) and (self.use_mfi_mode.value & 8):
            conditions.append(dataframe["mfi"] < self.mfi_exit_short_thresh.value)
        if (self.use_cci_mode.value & 2) and (self.use_cci_mode.value & 8):
            conditions.append(dataframe["cci"] < self.cci_exit_short_thresh.value)
        if (self.use_sar_mode.value & 2) and (self.use_sar_mode.value & 8):
            conditions.append(dataframe["sar"] < dataframe["close"])
        if (self.use_htsine_mode.value & 2) and (self.use_htsine_mode.value & 8):
            conditions.append(dataframe["htsine"] < dataframe["htleadsine"])
        return conditions

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        long_conditions = self.build_entry_conditions_long(dataframe, metadata)
        short_conditions = self.build_entry_conditions_short(dataframe, metadata)
        if long_conditions:
            dataframe.loc[np.all(long_conditions, axis=0), 'enter_long'] = 1
        if short_conditions:
            dataframe.loc[np.all(short_conditions, axis=0), 'enter_short'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        long_exit_conditions = self.build_exit_conditions_long(dataframe, metadata)
        short_exit_conditions = self.build_exit_conditions_short(dataframe, metadata)
        if long_exit_conditions:
            dataframe.loc[np.all(long_exit_conditions, axis=0), 'exit_long'] = 1
        if short_exit_conditions:
            dataframe.loc[np.all(short_exit_conditions, axis=0), 'exit_short'] = 1
        return dataframe

    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                 proposed_leverage: float, max_leverage: float, entry_tag: str, side: str,
                 **kwargs) -> float:
        return float(self.leverage_opt.value)

    def custom_stoploss(self, pair: str, trade, current_time, current_rate, current_profit, after_fill, **kwargs):
        if not trade:
            return self.stoploss

        # Трейлващ стоп към break-even
        if current_profit > 0.01:  # при 1% печалба
            return max(-0.002, self.stoploss)  # стоп на -0.2%
        if current_profit > 0.005:  # при 0.5% печалба
            return max(-0.003, self.stoploss)  # стоп на -0.3%
        return self.stoploss