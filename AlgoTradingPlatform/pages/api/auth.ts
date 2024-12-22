import type { NextApiRequest, NextApiResponse } from 'next';
import { generateSession } from '../../utils/kiteConnect';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    try {
      const { request_token } = req.body;
      const session = await generateSession(request_token);
      
      // In a real-world scenario, you'd want to store this securely, possibly in a database
      // For this MVP, we'll store it in a cookie
      res.setHeader('Set-Cookie', `access_token=${session.access_token}; HttpOnly; Path=/; Max-Age=86400`);
      
      res.status(200).json({ success: true });
    } catch (error) {
      console.error('Authentication error:', error);
      res.status(500).json({ success: false, error: 'Authentication failed' });
    }
  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}

