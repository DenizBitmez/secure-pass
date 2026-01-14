import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { share } from '../lib/api';
import { Button } from '../components/Button';
import { Input } from '../components/Input';
import { ArrowLeft, Clock, Link as LinkIcon, Copy } from 'lucide-react';

export default function Share() {
    const navigate = useNavigate();
    const [content, setContent] = useState('');
    const [ttl, setTtl] = useState(60);
    const [generatedLink, setGeneratedLink] = useState('');
    const [loading, setLoading] = useState(false);

    const handleCreate = async () => {
        if (!content) return;
        setLoading(true);
        try {
            // NOTE: For now we are sending plaintext to server (Server-Side Encryption for sharing)
            // To enable Client-Side ZK Sharing, we would encrypt here and send blob.
            // But the current backend implementation expects "content" string.
            const res = await share.create(content, ttl);
            const uuid = res.data.uuid;
            const link = `${window.location.origin}/share/${uuid}`;
            setGeneratedLink(link);
        } catch (err) {
            console.error(err);
            alert('Failed to create link');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-900 text-white">
            <div className="w-full max-w-lg p-8 bg-gray-800 rounded-xl shadow-2xl border border-gray-700">
                <div className="flex items-center mb-6">
                    <button onClick={() => navigate('/dashboard')} className="p-2 hover:bg-gray-700 rounded-full mr-2">
                        <ArrowLeft className="w-5 h-5" />
                    </button>
                    <h2 className="text-xl font-bold">Secure Share</h2>
                </div>

                {!generatedLink ? (
                    <div className="space-y-4">
                        <p className="text-gray-400 text-sm">
                            Create a secure, self-destructing link to share sensitive information.
                            The link will be deleted permanently after being viewed once.
                        </p>

                        <div>
                            <label className="block text-sm text-gray-300 mb-1">Secret Content</label>
                            <textarea
                                className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none text-white h-32"
                                placeholder="Enter password, API key, or secret message..."
                                value={content}
                                onChange={e => setContent(e.target.value)}
                            />
                        </div>

                        <div>
                            <label className="block text-sm text-gray-300 mb-1">Expiration (Minutes)</label>
                            <Input
                                type="number"
                                min="1"
                                max="10080"
                                value={ttl}
                                onChange={e => setTtl(e.target.value)}
                            />
                        </div>

                        <Button onClick={handleCreate} disabled={loading || !content}>
                            {loading ? 'Creating...' : 'Generate Self-Destruct Link'}
                        </Button>
                    </div>
                ) : (
                    <div className="space-y-6 animate-in fade-in zoom-in duration-300">
                        <div className="bg-green-600/20 p-4 rounded-lg flex items-start space-x-3">
                            <Clock className="w-6 h-6 text-green-500 flex-shrink-0" />
                            <div>
                                <h3 className="font-bold text-green-400">Link Ready!</h3>
                                <p className="text-sm text-green-200/70">
                                    This link will self-destruct after 1 view or {ttl} minutes.
                                </p>
                            </div>
                        </div>

                        <div className="bg-gray-900 p-4 rounded-lg flex items-center justify-between border border-gray-700">
                            <span className="text-indigo-400 truncate pr-4 text-sm font-mono">
                                {generatedLink}
                            </span>
                            <button
                                onClick={() => navigator.clipboard.writeText(generatedLink)}
                                className="text-gray-400 hover:text-white"
                            >
                                <Copy className="w-5 h-5" />
                            </button>
                        </div>

                        <Button onClick={() => { setGeneratedLink(''); setContent(''); }}>
                            Create Another
                        </Button>
                    </div>
                )}
            </div>
        </div>
    );
}
