'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import ModelSelector from '@/components/ModelSelector';
import ImageUploader from '@/components/ImageUploader';
import PredictionResult from '@/components/PredictionResult';
import { useAuthStore } from '@/lib/auth-store';
import { apiClient } from '@/lib/api-client';
import { Model, PredictionResult as IPredictionResult } from '@/types/api';

export default function AppPage() {
  const { isAuthenticated, checkAuth } = useAuthStore();
  const router = useRouter();

  const [models, setModels] = useState<Model[]>([]);
  const [selectedModel, setSelectedModel] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [result, setResult] = useState<IPredictionResult | null>(null);

  useEffect(() => {
    checkAuth();
    if (!isAuthenticated) router.push('/login');
  }, [checkAuth, isAuthenticated, router]);

  useEffect(() => {
    const loadModels = async () => {
      const availableModels = await apiClient.getAvailableModels();
      setModels(availableModels);
    };
    if (isAuthenticated) loadModels();
  }, [isAuthenticated]);

  const handleImageSelect = (file: File | null) => {
    if (file) {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onloadend = () => setPreviewUrl(reader.result as string);
      reader.readAsDataURL(file);
    } else {
      setSelectedFile(null);
      setPreviewUrl(null);
    }
  };

  const handlePredict = async () => {
    if (selectedFile && selectedModel) {
      const prediction = await apiClient.predictImage(selectedFile, selectedModel);
      setResult(prediction);
    }
  };

  if (!isAuthenticated) return null;

  return (
    <main className="min-h-screen bg-gray-50">
      <Header />
      <div className="max-w-7xl mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Waste Classification</h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <ModelSelector
              models={models}
              selectedModel={selectedModel}
              onSelect={setSelectedModel}
            />
            <ImageUploader onImageSelect={handleImageSelect} previewUrl={previewUrl} />
            <button
              onClick={handlePredict}
              disabled={!selectedFile || !selectedModel}
              className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-blue-700"
            >
              Classify Image
            </button>
          </div>

          <div className="lg:col-span-1">
            {result ? (
              <PredictionResult result={result} />
            ) : (
              <div className="bg-white rounded-lg shadow p-6 text-center">
                <p className="text-gray-600">Upload and classify</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
