import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { vault } from '../lib/api';
import { encryptPassword, decryptPassword } from '../lib/crypto';
import { Input } from '../components/Input';
import { Button } from '../components/Button';
import { Lock, Unlock, Plus, Copy, Eye, EyeOff, LayoutDashboard, Zap, ShieldCheck, Share2, Activity } from 'lucide-react';

export default function Dashboard() {
    const navigate = useNavigate();
    const [entries, setEntries] = useState([]);
    const [masterPassword, setMasterPassword] = useState('');
    const [isUnlocked, setIsUnlocked] = useState(false);
    const [loading, setLoading] = useState(false);

    // New Entry Form
    const [showAddModal, setShowAddModal] = useState(false);
    const [newSite, setNewSite] = useState('');
    const [newUrl, setNewUrl] = useState('');
    const [newPassword, setNewPassword] = useState('');

    // Visibility toggles for list
    const [visiblePasswords, setVisiblePasswords] = useState({});
    const [healthScores, setHealthScores] = useState({});

    useEffect(() => {
        const sessionKey = sessionStorage.getItem('masterPassword');
        if (sessionKey) {
            setMasterPassword(sessionKey);
            setIsUnlocked(true);
            fetchEntries();
        }
    }, []);

    const fetchEntries = async () => {
        try {
            const res = await vault.list();
            setEntries(res.data);
        } catch (err) {
            console.error(err);
            if (err.response?.status === 401) {
                localStorage.removeItem('token');
                navigate('/login');
            }
        }
    };

    const handleUnlock = (e) => {
        e.preventDefault();
        if (masterPassword.length > 0) {
            sessionStorage.setItem('masterPassword', masterPassword);
            setIsUnlocked(true);
            fetchEntries();
        }
    };

    const handleCreate = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const encryptedBlob = await encryptPassword(masterPassword, newPassword);
            await vault.create({
                site_name: newSite,
                site_url: newUrl,
                encrypted_password: encryptedBlob
            });
            setShowAddModal(false);
            setNewSite(''); setNewUrl(''); setNewPassword('');
            fetchEntries();
        } catch (err) {
            console.error("Failed to create entry", err);
            alert("Failed to save password.");
        } finally {
            setLoading(false);
        }
    };

    const toggleReveal = async (id, encryptedContent) => {
        if (visiblePasswords[id]) {
            const newState = { ...visiblePasswords };
            delete newState[id];
            setVisiblePasswords(newState);
        } else {
            try {
                const plaintext = await decryptPassword(masterPassword, encryptedContent);
                setVisiblePasswords({ ...visiblePasswords, [id]: plaintext });
            } catch (err) {
                alert("Failed to decrypt! Is your Master Password correct?");
            }
        }
    };

    const checkHealth = async (id, plaintext) => {
        try {
            const res = await vault.checkHealth(plaintext);
            setHealthScores(prev => ({ ...prev, [id]: res.data }));
        } catch (err) {
            console.error("Health check failed", err);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        sessionStorage.removeItem('masterPassword');
        navigate('/login');
    };

    if (!isUnlocked) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gray-900">
                <div className="w-full max-w-md p-8 space-y-6 bg-gray-800 rounded-xl shadow-2xl">
                    <div className="flex flex-col items-center">
                        <div className="p-3 bg-red-600 rounded-full bg-opacity-20">
                            <Lock className="w-8 h-8 text-red-500" />
                        </div>
                        <h1 className="mt-4 text-2xl font-bold">Vault Locked</h1>
                        <p className="text-gray-400">Enter your Master Password to decrypt your vault.</p>
                    </div>
                    <form onSubmit={handleUnlock} className="space-y-4">
                        <Input
                            type="password"
                            required
                            value={masterPassword}
                            onChange={(e) => setMasterPassword(e.target.value)}
                            placeholder="Master Password"
                        />
                        <Button type="submit">Unlock Vault</Button>
                    </form>
                    <div className="text-center">
                        <button onClick={handleLogout} className="text-gray-500 hover:text-white text-sm">Log out</button>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-900">
            <nav className="border-b border-gray-800 bg-gray-800/50 backdrop-blur-sm sticky top-0 z-10">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">
                        <div className="flex items-center space-x-2">
                            <LayoutDashboard className="w-6 h-6 text-indigo-500" />
                            <span className="font-bold text-xl">SecurePass</span>
                        </div>
                        <div className="flex space-x-4">
                            <Button onClick={() => navigate('/share')} className="bg-gray-700 hover:bg-gray-600 text-sm w-auto px-3">
                                <Share2 className="w-4 h-4 inline mr-1" /> Share
                            </Button>
                            <Button onClick={() => navigate('/2fa')} className="bg-gray-700 hover:bg-gray-600 text-sm w-auto px-3">
                                <ShieldCheck className="w-4 h-4 inline mr-1" /> 2FA
                            </Button>
                            <Button onClick={() => navigate('/generator')} className="bg-gray-700 hover:bg-gray-600 text-sm w-auto px-3">
                                <Zap className="w-4 h-4 inline mr-1" /> Gen
                            </Button>
                            <Button onClick={handleLogout} className="bg-red-600 hover:bg-red-700 text-sm w-auto px-3">
                                Lock
                            </Button>
                        </div>
                    </div>
                </div>
            </nav>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="flex justify-between items-center mb-8">
                    <h2 className="text-2xl font-semibold">My Vault</h2>
                    <Button onClick={() => setShowAddModal(true)} className="w-auto">
                        <Plus className="w-5 h-5 inline mr-1" /> Add New
                    </Button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {entries.map((entry) => (
                        <div key={entry.id} className="bg-gray-800 rounded-xl p-6 border border-gray-700 hover:border-indigo-500/50 transition-all shadow-lg">
                            <div className="flex justify-between items-start mb-4">
                                <div>
                                    <h3 className="text-lg font-bold text-white">{entry.site_name}</h3>
                                    <p className="text-indigo-400 text-sm truncate">{entry.site_url}</p>
                                </div>
                                <div className="p-2 bg-gray-700 rounded-lg">
                                    <Lock className="w-4 h-4 text-gray-400" />
                                </div>
                            </div>

                            <div className="relative group">
                                <div className="bg-gray-900 rounded p-3 text-sm font-mono flex flex-col justify-between min-h-[4rem]">
                                    <div className="flex justify-between items-center mb-2">
                                        <span className={visiblePasswords[entry.id] ? "text-green-400 break-all" : "text-gray-500 blur-sm select-none"}>
                                            {visiblePasswords[entry.id] || "••••••••••••••••"}
                                        </span>
                                        <button
                                            onClick={() => toggleReveal(entry.id, entry.encrypted_password || entry.encrypted_data)}
                                            className="text-gray-400 hover:text-white flex-shrink-0 ml-2"
                                        >
                                            {visiblePasswords[entry.id] ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                                        </button>
                                    </div>

                                    {visiblePasswords[entry.id] && (
                                        <div className="flex justify-end space-x-2 pt-2 border-t border-gray-800">
                                            <button
                                                onClick={() => checkHealth(entry.id, visiblePasswords[entry.id])}
                                                className="text-gray-400 hover:text-green-400 flex items-center text-xs"
                                                title="Check Health"
                                            >
                                                <Activity className="w-3 h-3 mr-1" /> Check
                                            </button>
                                            <button
                                                onClick={() => navigator.clipboard.writeText(visiblePasswords[entry.id])}
                                                className="text-gray-400 hover:text-white flex items-center text-xs"
                                                title="Copy"
                                            >
                                                <Copy className="w-3 h-3 mr-1" /> Copy
                                            </button>
                                        </div>
                                    )}
                                </div>
                            </div>

                            {healthScores[entry.id] && (
                                <div className="mt-3 bg-gray-900/50 p-2 rounded flex justify-between items-center text-xs">
                                    <span className={
                                        healthScores[entry.id].is_pwned
                                            ? "text-red-400 font-bold"
                                            : (healthScores[entry.id].score < 3 ? "text-yellow-400 font-bold" : "text-green-400 font-bold")
                                    }>
                                        {healthScores[entry.id].is_pwned
                                            ? `⚠️ PWNED! (${healthScores[entry.id].pwned_count} times)`
                                            : (healthScores[entry.id].score < 3 ? "⚠️ Weak Password" : "✅ Strong & Safe")
                                        }
                                    </span>
                                    <span className="text-gray-400">
                                        Score: <span className="text-white">{healthScores[entry.id].score}/4</span>
                                    </span>
                                </div>
                            )}
                            {healthScores[entry.id] && healthScores[entry.id].feedback && healthScores[entry.id].feedback.length > 0 && (
                                <div className="mt-2 text-xs text-gray-400 bg-gray-900/30 p-2 rounded border border-gray-700/50">
                                    <ul className="list-disc list-inside">
                                        {healthScores[entry.id].feedback.map((msg, idx) => (
                                            <li key={idx}>{msg}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    ))}

                    {entries.length === 0 && (
                        <div className="col-span-full text-center py-12 text-gray-500">
                            Your vault is empty. Add your first password!
                        </div>
                    )}
                </div>
            </main>

            {showAddModal && (
                <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
                    <div className="bg-gray-800 rounded-xl max-w-md w-full p-6 shadow-2xl border border-gray-700">
                        <h3 className="text-xl font-bold mb-4">Add to Vault</h3>
                        <form onSubmit={handleCreate} className="space-y-4">
                            <div>
                                <label className="block text-sm text-gray-400 mb-1">Site Name</label>
                                <Input required value={newSite} onChange={e => setNewSite(e.target.value)} placeholder="e.g. Gmail" />
                            </div>
                            <div>
                                <label className="block text-sm text-gray-400 mb-1">URL (Optional)</label>
                                <Input value={newUrl} onChange={e => setNewUrl(e.target.value)} placeholder="https://..." />
                            </div>
                            <div>
                                <label className="block text-sm text-gray-400 mb-1">Password</label>
                                <Input
                                    required
                                    type="password"
                                    value={newPassword}
                                    onChange={e => setNewPassword(e.target.value)}
                                    placeholder="Super Secret Password"
                                />
                                <p className="text-xs text-gray-500 mt-1">
                                    Will be encrypted with your Master Password LOCALLY before sending.
                                </p>
                            </div>
                            <div className="flex space-x-3 pt-4">
                                <Button type="button" onClick={() => setShowAddModal(false)} className="bg-gray-700 hover:bg-gray-600">Cancel</Button>
                                <Button type="submit" disabled={loading}>{loading ? 'Encrypting...' : 'Save Securely'}</Button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
