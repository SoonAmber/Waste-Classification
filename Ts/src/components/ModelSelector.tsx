'use client';

import { Model } from '@/types/api';

interface ModelSelectorProps {
  models: Model[];
  selectedModel: string | null;
  onSelect: (modelId: string) => void;
}

export default function ModelSelector({ models, selectedModel, onSelect }: ModelSelectorProps) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Select Model</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {models.map((model) => (
          <button
            key={model.id}
            onClick={() => onSelect(model.id)}
            className={`p-4 border-2 rounded-lg text-left ${
              selectedModel === model.id
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 bg-gray-50'
            }`}
          >
            <h3 className="font-semibold text-gray-900">{model.name}</h3>
            <p className="text-sm text-gray-600 mt-1">{model.description}</p>
          </button>
        ))}
      </div>
    </div>
  );
}
