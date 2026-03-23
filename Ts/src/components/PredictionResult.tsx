'use client';

import { PredictionResult } from '@/types/api';

interface PredictionResultProps {
  result: PredictionResult;
}

export default function PredictionResultComponent({ result }: PredictionResultProps) {
  const percentage = (result.confidence * 100).toFixed(1);

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Prediction</h2>

      <div className="mb-6 p-6 bg-green-50 rounded-lg border border-green-200">
        <p className="text-sm text-gray-600 mb-2">Result:</p>
        <p className="text-3xl font-bold text-green-600 capitalize">{result.class_name}</p>
        <div className="mt-4">
          <div className="bg-gray-200 rounded-full h-2 overflow-hidden">
            <div
              className="bg-green-500 h-full"
              style={{ width: `${result.confidence * 100}%` }}
            />
          </div>
          <p className="text-sm text-gray-600 mt-2">Confidence: {percentage}%</p>
        </div>
      </div>

      <div className="bg-gray-50 rounded-lg p-4">
        <h3 className="font-semibold text-gray-900 mb-3">All Predictions</h3>
        <div className="space-y-2">
          {Object.entries(result.all_predictions).map(([className, confidence]) => (
            <div key={className} className="flex items-center justify-between">
              <span className="text-gray-700 capitalize">{className}</span>
              <span className="text-gray-600 text-sm">{(confidence * 100).toFixed(1)}%</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
