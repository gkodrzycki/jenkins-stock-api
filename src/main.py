import uvicorn
import yfinance as yf
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def read_root():
    # raise RuntimeError("Intentional failure to simulate health check failure")
	return {"message": "Stock API is running", "status": "ok"}


@app.get("/stock/{ticker}")
def get_stock_price(ticker: str):
	stock = yf.Ticker(ticker)
	data = stock.history(period="1d")

	if data.empty:
		raise HTTPException(status_code=404, detail="Ticker not found")

	latest_price = data["Close"].iloc[-1]
	currency = stock.info.get("currency", "USD")

	return {
		"ticker": ticker.upper(),
		"price": round(latest_price, 2),
		"currency": currency,
	}


if __name__ == "__main__":
	uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
