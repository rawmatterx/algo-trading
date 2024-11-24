# Algo Trading Dashboard

A Streamlit-based algorithmic trading application that connects with Upstox for real-time market data and trading.

## Features
- OAuth2 authentication with Upstox
- Real-time market data visualization
- Trading interface for order placement
- Portfolio tracking
- Position management

## Setup

### Local Development
1. Clone the repository:
```bash
git clone https://github.com/yourusername/algo-trading.git
cd algo-trading
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.streamlit/secrets.toml` with your Upstox API credentials:
```toml
UPSTOX_API_KEY = "your_api_key"
UPSTOX_API_SECRET = "your_api_secret"
```

5. Run the application:
```bash
streamlit run Home.py
```

### Deployment
The application is configured for deployment on Streamlit Community Cloud:

1. Fork this repository
2. Set up your repository in Streamlit Community Cloud
3. Add your Upstox API credentials in Streamlit Cloud's secrets management
4. Deploy!

## Configuration
- Configure Upstox API credentials in Streamlit Cloud secrets
- Update redirect URI in Upstox developer console to match your Streamlit Cloud URL

## Security
- API credentials are managed through Streamlit's secrets management
- OAuth2 flow for secure authentication
- Secure token handling

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request