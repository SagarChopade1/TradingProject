import pandas as pd
import asyncio

class Candle:
    def __init__(self, id, open, high, low, close, date):
        self.id = id
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.date = date

    def to_dict(self):

        return {
            "id": self.id.isoformat(),
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "date": self.date.isoformat() if self.date else None
        }
async def process_csv(file, timeframe):
    # Read CSV file into DataFrame
    df = pd.read_csv(file)
    # Assuming CSV columns are ['id', 'date', 'time', 'open', 'high', 'low', 'close', 'volume']
    # Convert 'date' and 'time' to a single DateTime column for easier processing
    df['DateTime'] = pd.to_datetime(df['DATE'].astype(str) + ' ' + df['TIME'])

    # Resample data to the specified timeframe
    resampled_df = df.resample(f'{timeframe}T', on='DateTime').agg({
        'OPEN': 'first',
        'HIGH': 'max',
        'LOW': 'min',
        'CLOSE': 'last'
    })

    # Convert resampled DataFrame to list of Candle objects
    candles = [Candle(idx, row['OPEN'], row['HIGH'], row['LOW'], row['CLOSE'], idx) for idx, row in resampled_df.iterrows()]

    return candles


