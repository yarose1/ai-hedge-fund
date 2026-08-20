import pandas as pd

from hedge_fund.data.client import FDClient


class FakeOpenBBResult:
    def to_df(self):
        return pd.DataFrame(
            [
                {
                    "open": 100.0,
                    "high": 105.0,
                    "low": 99.0,
                    "close": 104.0,
                    "volume": 123456,
                },
                {
                    "open": 104.0,
                    "high": 108.0,
                    "low": 103.0,
                    "close": 107.0,
                    "volume": 234567,
                },
            ],
            index=pd.to_datetime(["2026-08-17", "2026-08-18"]),
        )


def test_get_prices_uses_openbb(monkeypatch):
   

    def fake_historical(**kwargs):
        assert kwargs["symbol"] == "AAPL"
        assert kwargs["start_date"] == "2026-08-17"
        assert kwargs["end_date"] == "2026-08-18"
        assert kwargs["interval"] == "1d"
        assert kwargs["provider"] == "yfinance"
        return FakeOpenBBResult()

    monkeypatch.setattr(
    "hedge_fund.data.client._openbb_historical",
    fake_historical,
    )

    prices = FDClient().get_prices(
        "AAPL",
        "2026-08-17",
        "2026-08-18",
    )

    assert len(prices) == 2

    assert prices[0].open == 100.0
    assert prices[0].close == 104.0
    assert prices[0].high == 105.0
    assert prices[0].low == 99.0
    assert prices[0].volume == 123456
    assert prices[0].time == "2026-08-17"

    assert prices[1].close == 107.0
    assert prices[1].volume == 234567
    assert prices[1].time == "2026-08-18"
