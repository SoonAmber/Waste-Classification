'use client';

import Link from 'next/link';
import { useAuthStore } from '@/lib/auth-store';
import { useRouter } from 'next/navigation';

export default function Header() {
  const { user, isAuthenticated, logout } = useAuthStore();
  const router = useRouter();

  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  return (
    <header className="bg-blue-600 text-white shadow sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link href="/" className="text-xl font-bold">
            ♻ Waste Classifier
          </Link>

          <nav className="hidden md:flex space-x-8">
            <Link href="/">Home</Link>
            {isAuthenticated && <Link href="/app">Classify</Link>}
          </nav>

          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <span className="text-sm">{user?.username}</span>
                <button
                  onClick={handleLogout}
                  className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded text-sm"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link href="/login" className="text-sm">
                  Login
                </Link>
                <Link href="/register" className="bg-white text-blue-600 px-4 py-2 rounded text-sm">
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
