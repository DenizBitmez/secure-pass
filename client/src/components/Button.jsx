import React from 'react';
import clsx from 'clsx';
import { twMerge } from 'tailwind-merge';

export function Button({ className, children, ...props }) {
    return (
        <button
            className={twMerge(
                clsx(
                    "w-full px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg transition-colors focus:ring-2 focus:ring-indigo-500 focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed",
                    className
                )
            )}
            {...props}
        >
            {children}
        </button>
    );
}
