import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { share } from '../lib/api';
import { Button } from '../components/Button';
import { Eye, Bomb, AlertTriangle } from 'lucide-react';

export default function ShareView() {
    const { uuid } = useParams();
    const [content, setContent] = useState('');
    const [error, setError] = useState('');
    const [revealed, setRevealed] = useState(false);
    const [loading, setLoading] = useState(false);

    const handleReveal = async () => {
        setLoading(true);
        try {
            const res = await share.get(uuid);
            setContent(res.data.content); // Backend decrypts and returns content
            setRevealed(true);
        } catch (err) {
            if (err.response?.status === 404) {
                setError('This link does not exist or has already been destroyed.');
            } else {
                setError('Failed to retrieve secret.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-950 text-white p-4">
            <div className="w-full max-w-lg p-8 bg-gray-900 rounded-xl shadow-2xl border border-gray-800 text-center">

                <div className="mx-auto w-16 h-16 bg-indigo-600/20 rounded-full flex items-center justify-center mb-6">
                    <Bomb className="w-8 h-8 text-indigo-500" />
                </div>

                <h1 className="text-2xl font-bold mb-2">SecurePass Share</h1>

                {!revealed && !error && (
                    <div className="space-y-6">
                        <p className="text-gray-400">
                            You have received a secure, self-destructing message.
                        </p>
                        <div className="bg-yellow-900/20 border border-yellow-700/50 p-4 rounded-lg text-left flex items-start space-x-3">
                            <AlertTriangle className="w-6 h-6 text-yellow-500 flex-shrink-0" />
                            <p className="text-sm text-yellow-200/80">
                                Warning: This message will be <strong>permanently deleted</strong> from our servers immediately after you view it. You cannot view it a second time.
                            </p>
                        </div>
                        <Button onClick={handleReveal} disabled={loading} className="bg-indigo-600 hover:bg-indigo-500 text-lg py-3">
                            {loading ? 'Decrypting...' : 'Reveal Secret'}
                        </Button>
                    </div>
                )}

                {revealed && (
                    <div className="space-y-6 animate-in fade-in zoom-in">
                        <h2 className="text-green-400 font-semibold mb-2">Decrypted Content:</h2>
                        <div className="bg-gray-800 p-6 rounded-lg border border-gray-700 font-mono text-left break-all select-all shadow-inner">
                            {content}
                        </div>
                        <p className="text-sm text-gray-500 italic">
                            This message has been destroyed from the server.
                        </p>
                    </div>
                )}

                {error && (
                    <div className="space-y-4">
                        <h3 className="text-xl font-bold text-red-500">Link Expired</h3>
                        <p className="text-gray-400">{error}</p>
                    </div>
                )}
            </div>
        </div>
    );
}
