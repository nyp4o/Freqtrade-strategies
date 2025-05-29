import logging
from freqtrade.strategy.interface import IStrategy
from freqtrade.strategy import IntParameter, DecimalParameter, CategoricalParameter
from freqtrade.persistence import Trade
from pandas import DataFrame
import talib.abstract as ta
import numpy as np

logger = logging.getLogger(__name__)

class Best5(IStrategy):

    timeframe = '5m'

    can_short = True
    stoploss = -0.99  # 99% stoploss
    minimal_roi = {
        "0": 0.01  # 1% ROI
    }
    exit_profit_only = False  # Only exit when in profit
    exit_profit_offset = 0.0  # Offset for profit-only exits
    startup_candle_count: int = 30
    ignore_roi_if_entry_signal = True

    trailing_stop = False  # This should be a direct boolean
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.015
    trailing_only_offset_is_reached = False  # This should be a direct boolean

    # Store the parameters for hyperopt but don't use them directly in the above settings
    trailing_stop_opt = CategoricalParameter([True, False], default=False, space='buy', optimize=True)
    trailing_stop_positive_opt = DecimalParameter(0.01, 0.10, default=0.02, decimals=3, space='buy', optimize=True)
    trailing_stop_positive_offset_opt = DecimalParameter(0.01, 0.15, default=0.03, decimals=3, space='buy', optimize=True)
    trailing_only_offset_is_reached_opt = CategoricalParameter([True, False], default=False, space='buy', optimize=True)

    leverage_opt = IntParameter(low=2, high=5, default=3, space='buy', optimize=True)

    fast_ma_length = IntParameter(low=5, high=15, default=7, space='buy', optimize=True)
    slow_ma_length = IntParameter(low=16, high=40, default=25, space='buy', optimize=True)
    rsi_length = IntParameter(low=7, high=14, default=10, space='buy', optimize=True)

    macd_fast = IntParameter(8, 12, default=10, space='buy', optimize=True)
    macd_slow = IntParameter(16, 26, default=20, space='buy', optimize=True)
    macd_signal = IntParameter(5, 9, default=7, space='buy', optimize=True)

    fisher_rsi_threshold_long = DecimalParameter(-0.6, -0.2, default=-0.4, space='buy', optimize=True)
    fisher_rsi_threshold_short = DecimalParameter(0.2, 0.6, default=0.4, space='sell', optimize=True)

    sar_enabled = CategoricalParameter([True, False], default=True, space='sell', optimize=True)

    rsi_buy_threshold = IntParameter(low=20, high=35, default=28, space='buy', optimize=True)
    rsi_sell_threshold = IntParameter(low=65, high=80, default=72, space='sell', optimize=True)


    def leverage(
            self, pair: str, current_time, current_rate: float, proposed_leverage: float, max_leverage: float,
            side: str, **kwargs
    ) -> float:
        selected_leverage = min(self.leverage_opt.value, max_leverage)
        return float(selected_leverage)

    # -------------------------------------------------------------------------
    # 7) Populate Indicators
    # -------------------------------------------------------------------------
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Calculate technical indicators: SMA (fast/slow), RSI.
        """
        dataframe['fast_sma'] = ta.SMA(dataframe, timeperiod=int(self.fast_ma_length.value))
        dataframe['slow_sma'] = ta.SMA(dataframe, timeperiod=int(self.slow_ma_length.value))
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=int(self.rsi_length.value))

        macd = ta.MACD(dataframe, fastperiod=self.macd_fast.value, slowperiod=self.macd_slow.value,
                       signalperiod=self.macd_signal.value)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macd'] - macd['macdsignal']

        # Fisher RSI
        rsi = dataframe['rsi']
        rsi_scaled = 0.1 * (rsi - 50)
        fisher = (np.exp(2 * rsi_scaled) - 1) / (np.exp(2 * rsi_scaled) + 1)
        dataframe['fisher_rsi'] = fisher

        # SAR
        dataframe['sar'] = ta.SAR(dataframe)


        return dataframe

    # -------------------------------------------------------------------------
    # 8) Entry Signal Logic (Long / Short)
    # -------------------------------------------------------------------------
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Determine when to open a long or short position based on SMA and RSI signals.
        """
        long_conditions = (
                (dataframe['fast_sma'] > dataframe['slow_sma']) &
                (dataframe['rsi'] < self.rsi_buy_threshold.value) &
                (dataframe['macdhist'] > 0) &
                (dataframe['macd'] > dataframe['macdsignal']) &  # <--- ново
                (dataframe['fisher_rsi'] < self.fisher_rsi_threshold_long.value) &
                ((dataframe['close'] - dataframe['open']).abs() > 0.001 * dataframe['close'])
        )

        short_conditions = (
                (dataframe['fast_sma'] < dataframe['slow_sma']) &
                (dataframe['rsi'] > self.rsi_sell_threshold.value) &
                (dataframe['macdhist'] < 0) &
                (dataframe['macd'] < dataframe['macdsignal']) &  # <--- ново
                (dataframe['fisher_rsi'] > self.fisher_rsi_threshold_short.value) &
                ((dataframe['close'] - dataframe['open']).abs() > 0.001 * dataframe['close'])
        )

        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[short_conditions, 'enter_short'] = 1

        return dataframe

    # -------------------------------------------------------------------------
    # 9) Exit Signal Logic (Sell / Cover)
    # -------------------------------------------------------------------------
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Determine when to exit a long or short position based on reversed conditions.
        """
        dataframe['exit_long'] = 0
        dataframe['exit_short'] = 0

        long_exit_conditions = (
                (dataframe['fast_sma'] < dataframe['slow_sma']) &
                (
                        (dataframe['rsi'] > self.rsi_sell_threshold.value) |
                        (self.sar_enabled.value and dataframe['sar'] > dataframe['close']) |  # Коригирано
                        (dataframe['fisher_rsi'] > 0.7)
                )
        )

        short_exit_conditions = (
                (dataframe['fast_sma'] > dataframe['slow_sma']) &
                (
                        (dataframe['rsi'] < self.rsi_buy_threshold.value) |
                        (self.sar_enabled.value and dataframe['sar'] < dataframe['close']) |  # Коригирано
                        (dataframe['fisher_rsi'] < -0.7)
                )
        )

        dataframe.loc[long_exit_conditions, 'exit_long'] = 1
        dataframe.loc[short_exit_conditions, 'exit_short'] = 1

        return dataframe

    # -------------------------------------------------------------------------
    # 10) confirm_trade_exit (Corrected to avoid exit_reason conflict)
    # -------------------------------------------------------------------------
    def confirm_trade_exit(
            self,
            pair: str,
            trade: Trade,
            order_type: str,
            amount: float,
            rate: float,
            time_in_force: str,
            exit_reason: str,
            **kwargs
    ) -> bool:
        """
        Confirm the exit before placing the order.
        Overridden to avoid duplicate 'exit_reason' errors.
        """
        # Optionally add custom checks here.
        # Example: If you wanted to disallow exit under certain conditions,
        # you'd return False. For standard usage, just call the parent method.
        return super().confirm_trade_exit(
            pair=pair,
            trade=trade,
            order_type=order_type,
            amount=amount,
            rate=rate,
            time_in_force=time_in_force,
            exit_reason=exit_reason,
            **kwargs
        )

    # -------------------------------------------------------------------------
    # 11) custom_stoploss (Optional Trailing Logic)
    # -------------------------------------------------------------------------
    def custom_stoploss(
            self,
            pair: str,
            trade: Trade,
            current_time,
            current_rate: float,
            current_profit: float,
            **kwargs
    ) -> float:
        """
        Customize the stoploss if trailing_stop_opt is enabled. Otherwise, use a fixed stop.
        Returning 1 indicates no immediate stoploss override (Freqtrade will handle trailing).
        """
        if self.trailing_stop_opt.value:
            # Defer to built-in trailing stop parameters.
            return 1
        else:
            # Use a fixed stoploss of -0.02.
            return float(self.stoploss)

    # -------------------------------------------------------------------------
    # 12) bot_start (Optional Logging)
    # -------------------------------------------------------------------------
    def bot_start(self, **kwargs) -> None:
        """
        Called at bot start. Use this to assign the hyperopt values to the actual parameters.
        """
        super().bot_start(**kwargs)

        # Assign hyperopt values to actual trailing stop parameters
        self.trailing_stop = self.trailing_stop_opt.value
        self.trailing_stop_positive = self.trailing_stop_positive_opt.value
        self.trailing_stop_positive_offset = self.trailing_stop_positive_offset_opt.value
        self.trailing_only_offset_is_reached = self.trailing_only_offset_is_reached_opt.value

        # Log parameters
        logger.info("Final Strategy Parameters:")
        logger.info(f"  timeframe            = {self.timeframe}")
        logger.info(f"  trailing_stop        = {self.trailing_stop}")
        if self.trailing_stop:
            logger.info(f"    trailing_stop_positive        = {self.trailing_stop_positive}")
            logger.info(f"    trailing_stop_positive_offset = {self.trailing_stop_positive_offset}")
            logger.info(f"    trailing_only_offset_is_reached = {self.trailing_only_offset_is_reached}")
        logger.info(f"  leverage            = {self.leverage_opt.value}")
        logger.info(f"  fast_ma_length      = {self.fast_ma_length.value}")
        logger.info(f"  slow_ma_length      = {self.slow_ma_length.value}")
        logger.info(f"  rsi_length          = {self.rsi_length.value}")
        logger.info(f"  rsi_buy_threshold   = {self.rsi_buy_threshold.value}")
        logger.info(f"  rsi_sell_threshold  = {self.rsi_sell_threshold.value}")
