// 在这里定义项目中使用的 TypeScript 类型
export interface User {
  id: string
  name: string
  email: string
}

export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
}
