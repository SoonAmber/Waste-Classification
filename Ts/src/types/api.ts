// API 响应类型
export interface User {
  id: number;
  username: string;
  email: string;
  created_at: string;
  updated_at: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
  user: User;
}

export interface PredictionResult {
  class_name: string;
  confidence: number;
  all_predictions: Record<string, number>;
}

export interface Model {
  id: string;
  name: string;
  description: string;
}

export interface PredictionResponse {
  models: Model[];
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface ApiError {
  detail: string;
}
