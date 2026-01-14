import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { generator } from '../lib/api';
import { Button } from '../components/Button';
import { ArrowLeft, Copy, RefreshCw } from 'lucide-react';

export default function Generator() {
    const navigate = useNavigate();
    const [password, setPassword] = useState('');
    const [length, setLength] = useState(16);
    const [options, setOptions] = useState({
        uppercase: true,
        digits: true,
        symbols: true
    });
    const [loading, setLoading] = useState(false);

    const generate = async () => {
        setLoading(true);
        try {
            const res = await generator.generate({
                length,
                ...options
            });
            setPassword(res.data.password);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const copyToClipboard = () => {
        if (password) {
            navigator.clipboard.writeText(password);
            // Could show toast here
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-900 text-white">
            <div className="w-full max-w-md p-8 bg-gray-800 rounded-xl shadow-2xl border border-gray-700">
                <div className="flex items-center mb-6">
                    <button onClick={() => navigate('/dashboard')} className="p-2 hover:bg-gray-700 rounded-full mr-2">
                        <ArrowLeft className="w-5 h-5" />
                    </button>
                    <h2 className="text-xl font-bold">Password Generator</h2>
                </div>

                <div className="bg-gray-900 p-4 rounded-lg mb-6 flex justify-between items-center h-16 border border-gray-700">
                    <span className="font-mono text-lg truncate pr-4 text-green-400">
                        {password || 'Click Generate'}
                    </span>
                    <button onClick={copyToClipboard} className="text-gray-400 hover:text-white" title="Copy">
                        <Copy className="w-5 h-5" />
                    </button>
                </div>

                <div className="space-y-6">
                    <div>
                        <label className="block text-sm text-gray-400 mb-2">Length: {length}</label>
                        <input
                            type="range"
                            min="8"
                            max="64"
                            value={length}
                            onChange={(e) => setLength(parseInt(e.target.value))}
                            className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
                        />
                    </div>

                    <div className="flex justify-between">
                        <label className="flex items-center space-x-2 cursor-pointer">
                            <input
                                type="checkbox"
                                checked={options.uppercase}
                                onChange={e => setOptions({ ...options, uppercase: e.target.checked })}
                                className="rounded bg-gray-700 border-gray-600 text-indigo-600 focus:ring-indigo-500"
                            />
                            <span>A-Z</span>
                        </label>
                        <label className="flex items-center space-x-2 cursor-pointer">
                            <input
                                type="checkbox"
                                checked={options.digits}
                                onChange={e => setOptions({ ...options, digits: e.target.checked })}
                                className="rounded bg-gray-700 border-gray-600 text-indigo-600 focus:ring-indigo-500"
                            />
                            <span>0-9</span>
                        </label>
                        <label className="flex items-center space-x-2 cursor-pointer">
                            <input
                                type="checkbox"
                                checked={options.symbols}
                                onChange={e => setOptions({ ...options, symbols: e.target.checked })}
                                className="rounded bg-gray-700 border-gray-600 text-indigo-600 focus:ring-indigo-500"
                            />
                            <span>!@#</span>
                        </label>
                    </div>

                    <Button onClick={generate} disabled={loading} className="py-3 flex justify-center items-center">
                        <RefreshCw className={`w-5 h-5 mr-2 ${loading ? 'animate-spin' : ''}`} />
                        Generate Strong Password
                    </Button>
                </div>
            </div>
        </div>
    );
}
