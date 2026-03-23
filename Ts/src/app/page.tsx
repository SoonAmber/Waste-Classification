'use client';

import { useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import { useAuthStore } from '@/lib/auth-store';

export default function Home() {
  const { isAuthenticated, checkAuth } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  return (
    <main className="min-h-screen bg-white">
      <Header />
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">♻ Waste Classifier</h1>
          <p className="text-lg text-gray-600 mb-8">Intelligent garbage image classification system</p>

          <div className="flex gap-4 justify-center">
            <Link href={isAuthenticated ? '/app' : '/login'}>
              <button className="px-8 py-3 bg-blue-600 text-white rounded-lg font-semibold">
                Get Started
              </button>
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
}
