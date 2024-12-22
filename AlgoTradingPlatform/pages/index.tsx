import Layout from '../components/Layout';
import Link from 'next/link';

export default function Home() {
  return (
    <Layout>
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Welcome to Algo Trading Platform</h1>
        <p className="text-xl mb-8">Get started by logging in to your Zerodha account.</p>
        <Link href="/login" className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">
          Login with Zerodha
        </Link>
      </div>
    </Layout>
  );
}

