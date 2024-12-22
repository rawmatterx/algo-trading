import KiteConnect from 'kiteconnect';

const kite = new KiteConnect({
  api_key: process.env.KITE_API_KEY,
});

export const getLoginURL = () => {
  return kite.getLoginURL();
};

export const generateSession = async (requestToken: string) => {
  try {
    const response = await kite.generateSession(requestToken, process.env.KITE_API_SECRET);
    return response;
  } catch (error) {
    console.error('Error generating session:', error);
    throw error;
  }
};

export const getHoldings = async (accessToken: string) => {
  try {
    kite.setAccessToken(accessToken);
    const holdings = await kite.getHoldings();
    return holdings;
  } catch (error) {
    console.error('Error fetching holdings:', error);
    throw error;
  }
};

