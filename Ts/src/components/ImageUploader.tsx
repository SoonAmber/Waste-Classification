'use client';

import { useState, useRef } from 'react';
import Image from 'next/image';

interface ImageUploaderProps {
  onImageSelect: (file: File) => void;
  previewUrl: string | null;
}

export default function ImageUploader({ onImageSelect, previewUrl }: ImageUploaderProps) {
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(e.type !== 'dragleave');
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);
    const file = e.dataTransfer.files?.[0];
    if (file) onImageSelect(file);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) onImageSelect(file);
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Upload Image</h2>

      {previewUrl ? (
        <div>
          <div className="relative w-full h-64 bg-gray-50 rounded-lg overflow-hidden">
            <Image src={previewUrl} alt="Preview" fill className="object-contain" />
          </div>
          <button
            onClick={() => {
              onImageSelect(null as any);
              if (fileInputRef.current) fileInputRef.current.value = '';
            }}
            className="mt-4 w-full px-4 py-2 text-red-600 border border-red-300 rounded-md"
          >
            Clear
          </button>
        </div>
      ) : (
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer ${
            dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
          }`}
        >
          <div className="text-4xl mb-2">📷</div>
          <p className="text-gray-900 mb-1">Drop image here or click</p>
          <p className="text-xs text-gray-500">PNG, JPG, GIF, WebP</p>
        </div>
      )}

      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleChange}
        className="hidden"
      />
    </div>
  );
}
