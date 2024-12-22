import { useEffect } from 'react';
import { useRouter } from 'next/router';

export default function Callback() {
  const router = useRouter();

  useEffect(() => {
    const { request_token } = router.query;
    if (request_token) {
      // Send the request token to your backend to generate a session
      fetch('/api/auth', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ request_token }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            router.push('/dashboard');
          } else {
            console.error('Authentication failed');
            router.push('/login');
          }
        })
        .catch((error) => {
          console.error('Error during authentication:', error);
          router.push('/login');
        });
    }
  }, [router]);

  return (
    <div className="flex justify-center items-center h-screen">
      <p className="text-xl">Authenticating...</p>
    </div>
  );
}

