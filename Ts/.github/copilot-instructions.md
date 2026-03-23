# TypeScript + React Next.js 项目设置

本项目使用 Next.js、TypeScript、Tailwind CSS、ESLint 和 Prettier 构建。

## 项目结构

```
.
├── src/
│   ├── pages/          # 页面组件
│   ├── components/     # 可复用组件
│   ├── styles/        # 全局样式
│   └── types/         # TypeScript 类型定义
├── public/            # 静态资源
├── .eslintrc.json     # ESLint 配置
├── .prettierrc         # Prettier 配置
├── tailwind.config.js  # Tailwind CSS 配置
└── tsconfig.json       # TypeScript 配置
```

## 快速开始

1. 安装依赖：`npm install`
2. 启动开发服务器：`npm run dev`
3. 打开 http://localhost:3000 查看页面

## 配置说明

- **TypeScript**: 启用 strict 模式，确保类型安全
- **ESLint**: 包含 Next.js 最佳实践和 TypeScript 规则
- **Prettier**: 自动代码格式化
- **Tailwind CSS**: 实用优先的 CSS 框架
