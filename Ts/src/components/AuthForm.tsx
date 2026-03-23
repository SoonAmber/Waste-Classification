'use client';

import { useState } from 'react';
import { useAuthStore } from '@/lib/auth-store';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

interface AuthFormProps {
  mode: 'login' | 'register';
}

export default function AuthForm({ mode }: AuthFormProps) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const { login, register } = useAuthStore();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (mode === 'register') {
      await register(username, email, password);
      router.push('/login');
    } else {
      await login(username, password);
      router.push('/app');
    }
  };

  return (
    <div className="min-h-screen bg-blue-50 flex items-center justify-center py-12 px-4">
      <div className="max-w-md w-full bg-white rounded-lg shadow p-8">
        <h1 className="text-3xl font-bold text-center text-gray-900 mb-8">Waste Classifier</h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm text-gray-700">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>

          {mode === 'register' && (
            <div>
              <label className="block text-sm text-gray-700">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md"
              />
            </div>
          )}

          <div>
            <label className="block text-sm text-gray-700">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md font-medium"
          >
            {mode === 'login' ? 'Sign In' : 'Register'}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-600">
          {mode === 'login' ? (
            <>
              Don&apos;t have an account?{' '}
              <Link href="/register" className="text-blue-600 font-medium">
                Sign up
              </Link>
            </>
          ) : (
            <>
              Have an account?{' '}
              <Link href="/login" className="text-blue-600 font-medium">
                Sign in
              </Link>
            </>
          )}
        </p>
      </div>
    </div>
  );
}
