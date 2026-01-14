import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { auth } from '../lib/api';
import { Button } from '../components/Button';
import { Input } from '../components/Input';
import { QRCodeSVG } from 'qrcode.react';
import { ArrowLeft, CheckCircle, ShieldAlert } from 'lucide-react';

export default function TwoFactorSetup() {
    const navigate = useNavigate();
    const [step, setStep] = useState('init'); // init, scan, success
    const [secret, setSecret] = useState('');
    const [uri, setUri] = useState('');
    const [code, setCode] = useState('');
    const [error, setError] = useState('');

    const startSetup = async () => {
        try {
            const res = await auth.setup2FA();
            setSecret(res.data.secret);
            setUri(res.data.uri);
            setStep('scan');
            setError('');
        } catch (err) {
            setError('Failed to generate 2FA secret.');
        }
    };

    const handleVerify = async (e) => {
        e.preventDefault();
        try {
            await auth.enable2FA(secret, code);
            setStep('success');
        } catch (err) {
            setError('Invalid code. Please try again.');
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-900 text-white">
            <div className="w-full max-w-md p-8 bg-gray-800 rounded-xl shadow-2xl border border-gray-700">
                <div className="flex items-center mb-6">
                    <button onClick={() => navigate('/dashboard')} className="p-2 hover:bg-gray-700 rounded-full mr-2">
                        <ArrowLeft className="w-5 h-5" />
                    </button>
                    <h2 className="text-xl font-bold">Two-Factor Auth</h2>
                </div>

                {step === 'init' && (
                    <div className="text-center space-y-6">
                        <div className="mx-auto w-16 h-16 bg-indigo-600/20 rounded-full flex items-center justify-center">
                            <ShieldAlert className="w-8 h-8 text-indigo-500" />
                        </div>
                        <p className="text-gray-300">
                            Protect your account by adding an extra layer of security.
                            You will need an authenticator app like Google Authenticator or Authy.
                        </p>
                        <Button onClick={startSetup}>Start Setup</Button>
                    </div>
                )}

                {step === 'scan' && (
                    <div className="space-y-6">
                        <div className="flex justify-center bg-white p-4 rounded-lg">
                            {uri && <QRCodeSVG value={uri} size={192} />}
                        </div>
                        <div className="text-center">
                            <p className="text-sm text-gray-400 mb-2">Or enter manual key:</p>
                            <code className="bg-gray-900 p-2 rounded text-indigo-400 font-mono text-lg select-all">
                                {secret}
                            </code>
                        </div>

                        <form onSubmit={handleVerify} className="space-y-4 pt-4 border-t border-gray-700">
                            <p className="text-sm text-gray-300">Enter the 6-digit code from your app:</p>
                            <Input
                                value={code}
                                onChange={e => setCode(e.target.value)}
                                placeholder="123456"
                                maxLength={6}
                                className="text-center tracking-widest text-xl"
                            />
                            {error && <p className="text-red-400 text-sm">{error}</p>}
                            <Button type="submit">Enable 2FA</Button>
                        </form>
                    </div>
                )}

                {step === 'success' && (
                    <div className="text-center space-y-6">
                        <div className="mx-auto w-16 h-16 bg-green-600/20 rounded-full flex items-center justify-center">
                            <CheckCircle className="w-8 h-8 text-green-500" />
                        </div>
                        <h3 className="text-lg font-bold">2FA Enabled!</h3>
                        <p className="text-gray-300">
                            Your account is now more secure. You will be asked for a code next time you login.
                        </p>
                        <Button onClick={() => navigate('/dashboard')}>Back to Dashboard</Button>
                    </div>
                )}
            </div>
        </div>
    );
}
