import React from 'react';
import Link from 'next/link';

const Navbar: React.FC = () => {
  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <Link href="/" className="text-xl font-bold text-gray-800">
            Algo Trading Platform
          </Link>
          <div>
            <Link href="/dashboard" className="text-gray-600 hover:text-gray-800 mr-4">
              Dashboard
            </Link>
            <Link href="/login" className="text-gray-600 hover:text-gray-800">
              Login
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

