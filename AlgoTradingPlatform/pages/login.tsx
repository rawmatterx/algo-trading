import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { getLoginURL } from '../utils/kiteConnect';

export default function Login() {
  const router = useRouter();

  useEffect(() => {
    const loginURL = getLoginURL();
    router.push(loginURL);
  }, [router]);

  return (
    <div className="flex justify-center items-center h-screen">
      <p className="text-xl">Redirecting to Zerodha login...</p>
    </div>
  );
}

