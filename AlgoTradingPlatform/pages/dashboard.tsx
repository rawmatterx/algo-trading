import { useState, useEffect } from 'react';
import Layout from '../components/Layout';

interface Holding {
  tradingsymbol: string;
  quantity: number;
  average_price: number;
  last_price: number;
  pnl: number;
}

export default function Dashboard() {
  const [holdings, setHoldings] = useState<Holding[]>([]);

  useEffect(() => {
    fetch('/api/holdings')
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setHoldings(data.holdings);
        } else {
          console.error('Failed to fetch holdings');
        }
      })
      .catch((error) => {
        console.error('Error fetching holdings:', error);
      });
  }, []);

  return (
    <Layout>
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
      <div className="bg-white shadow-md rounded-lg overflow-hidden">
        <table className="min-w-full">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Symbol</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantity</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Avg Price</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Last Price</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">P&L</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {holdings.map((holding) => (
              <tr key={holding.tradingsymbol}>
                <td className="px-6 py-4 whitespace-nowrap">{holding.tradingsymbol}</td>
                <td className="px-6 py-4 whitespace-nowrap">{holding.quantity}</td>
                <td className="px-6 py-4 whitespace-nowrap">{holding.average_price.toFixed(2)}</td>
                <td className="px-6 py-4 whitespace-nowrap">{holding.last_price.toFixed(2)}</td>
                <td className="px-6 py-4 whitespace-nowrap">{holding.pnl.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Layout>
  );
}

