import React from 'react';
import clsx from 'clsx';
import { twMerge } from 'tailwind-merge';

export function Input({ className, ...props }) {
    return (
        <input
            className={twMerge(
                clsx(
                    "w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none text-white placeholder-gray-400",
                    className
                )
            )}
            {...props}
        />
    );
}
