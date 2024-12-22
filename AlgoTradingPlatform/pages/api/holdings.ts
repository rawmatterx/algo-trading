import type { NextApiRequest, NextApiResponse } from 'next';
import { getHoldings } from '../../utils/kiteConnect';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'GET') {
    try {
      const { access_token } = req.cookies;
      
      if (!access_token) {
        return res.status(401).json({ success: false, error: 'Unauthorized' });
      }

      const holdings = await getHoldings(access_token);
      res.status(200).json({ success: true, holdings });
    } catch (error) {
      console.error('Error fetching holdings:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch holdings' });
    }
  } else {
    res.setHeader('Allow', ['GET']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}

