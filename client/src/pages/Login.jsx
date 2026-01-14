import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { auth } from '../lib/api';
import { Input } from '../components/Input';
import { Button } from '../components/Button';
import { Lock } from 'lucide-react';

export default function Login() {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const res = await auth.login(email, password);
            localStorage.setItem('token', res.data.access_token);
            navigate('/dashboard');
        } catch (err) {
            setError('Invalid credentials');
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-900">
            <div className="w-full max-w-md p-8 space-y-6 bg-gray-800 rounded-xl shadow-2xl">
                <div className="flex flex-col items-center">
                    <div className="p-3 bg-indigo-600 rounded-full bg-opacity-20">
                        <Lock className="w-8 h-8 text-indigo-500" />
                    </div>
                    <h1 className="mt-4 text-2xl font-bold">Welcome Back</h1>
                    <p className="text-gray-400">Sign in to access your vault</p>
                </div>

                {error && (
                    <div className="p-3 text-sm text-red-400 bg-red-900/30 border border-red-800 rounded">
                        {error}
                    </div>
                )}

                <form onSubmit={handleLogin} className="space-y-4">
                    <div>
                        <label className="block mb-1 text-sm font-medium text-gray-300">Email</label>
                        <Input
                            type="email"
                            required
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="you@example.com"
                        />
                    </div>
                    <div>
                        <label className="block mb-1 text-sm font-medium text-gray-300">Password</label>
                        <Input
                            type="password"
                            required
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="••••••••"
                        />
                    </div>

                    <Button type="submit">Sign In</Button>
                </form>

                <p className="text-center text-sm text-gray-400">
                    Don't have an account?{' '}
                    <Link to="/register" className="text-indigo-400 hover:text-indigo-300">
                        Sign up
                    </Link>
                </p>
            </div>
        </div>
    );
}
