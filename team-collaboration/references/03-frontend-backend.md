# 前后端工程目录结构

---

## 前端工程（Vben Admin 5.x）

```
frontend/
├── apps/
│   └── web-antd/                      # 主应用
│       ├── src/
│       │   ├── views/                 # 页面目录
│       │   │   ├── {module}/          # 模块目录（如 product、trade）
│       │   │   │   ├── {feature}/     # 功能目录（如 list、detail）
│       │   │   │   │   ├── index.vue  # 主页面
│       │   │   │   │   ├── data.ts    # Schema 定义
│       │   │   │   │   └── modules/
│       │   │   │   │       └── form.vue # 表单弹窗
│       │   │   │   └── index.md       # 模块索引（可选）
│       │   │   └── index.md           # views 总索引（可选）
│       │   │
│       │   ├── api/                   # API 定义
│       │   │   ├── {module}/          # 模块 API
│       │   │   │   ├── {feature}.ts   # 功能 API（如 product.ts）
│       │   │   │   └── index.md       # 模块 API 索引（可选）
│       │   │   └── index.md           # API 总索引（可选）
│       │   │
│       │   ├── router/                # 路由配置
│       │   │   ├── routes/
│       │   │   │   ├── modules/       # 模块路由
│       │   │   │   │   └── {module}.ts # 模块路由定义
│       │   │   │   └── index.md       # 路由索引（可选）
│       │   │   └── index.md           # router 总索引（可选）
│       │   │
│       │   ├── preferences.ts         # 主题/布局配置
│       │   └── store/                 # 状态管理（Pinia）
│       │
│       └── tailwind.config.mjs        # Tailwind 扩展配置
│
├── packages/
│   ├── @core/ui-kit/shadcn-ui/        # UI 组件库（禁止修改）
│   └── effects/plugins/vxe-table/     # 表格组件
│
└── package.json
```

### 前端开发输出文件映射

| task_type | 输出文件路径 |
|-----------|-------------|
| `new_page` (list) | `views/{module}/{feature}/index.vue` + `data.ts` + `modules/form.vue` + `api/{module}/{feature}.ts` |
| `new_page` (form) | `views/{module}/{feature}/index.vue` + `data.ts` + `api/{module}/{feature}.ts` |
| `new_page` (detail) | `views/{module}/{feature}/index.vue` + `data.ts` + `api/{module}/{feature}.ts` |
| `theme_config` | `apps/web-antd/src/preferences.ts` + `tailwind.config.mjs` |
| `route_add` | `router/routes/modules/{module}.ts` |
| `modal_add` | `views/{module}/{feature}/modules/*.vue` |
| `field_change` | `data.ts` + `api/{module}/{feature}.ts` |

---

## 后端工程（Spring Boot 3 + MyBatis Plus）

```
backend/
├── src/main/java/com/dainthub/{project}/
│   ├── module/
│   │   ├── {module}/                  # 模块目录（如 trade、product）
│   │   │   ├── controller/
│   │   │   │   └── admin/
│   │   │   │       ├── {Entity}Controller.java
│   │   │   │       └── vo/
│   │   │   │           └── {entity_snake}/
│   │   │   │               ├── {Entity}SaveReqVO.java
│   │   │   │               ├── {Entity}PageReqVO.java
│   │   │   │               └── {Entity}RespVO.java
│   │   │   │
│   │   │   ├── service/
│   │   │   │   ├── {Entity}Service.java
│   │   │   │   └── impl/
│   │   │   │       └── {Entity}ServiceImpl.java
│   │   │   │
│   │   │   ├── dal/
│   │   │   │   ├── dataobject/
│   │   │   │   │   └── {entity_snake}/
│   │   │   │   │       └── {Entity}DO.java
│   │   │   │   └── mysql/
│   │   │   │       └── {entity_snake}/
│   │   │   │           └── {Entity}Mapper.java
│   │   │   │
│   │   │   ├── client/                # 外部服务调用（如有）
│   │   │   │   ├── {Entity}Client.java
│   │   │   │   └── dto/
│   │   │   │       └── {Entity}DTO.java
│   │   │   │
│   │   │   ├── job/                   # 定时任务（如有）
│   │   │   │   └── {Entity}SyncJob.java
│   │   │   │
│   │   │   ├── config/                # 模块配置（如有）
│   │   │   │   └── {Module}JobConfig.java
│   │   │   │
│   │   │   └── enums/
│   │   │   │   └── ErrorCodeConstants.java
│   │   │   │
│   │   │   └── package-info.java      # 模块说明（可选）
│   │   │
│   │   └── index.md                   # module 总索引（可选）
│   │
│   └── Application.java               # 启动类
│
├── src/main/resources/
│   ├── mapper/{module}/               # Mapper XML
│   │   └── {Entity}Mapper.xml
│   │
│   ├── application.yaml               # 主配置
│   ├── application-dev.yaml           # 开发环境
│   ├── application-prod.yaml          # 生产环境
│   │
│   └── db/                            # 内置数据库脚本（可选）
│       └── changelog/                 # 变更日志（与 docs/db 同步）
│
├── src/test/java/com/dainthub/{project}/
│   └── module/{module}/               # 测试代码
│       ├── service/
│       │   └── impl/
│       │   │   └── {Entity}ServiceImplTest.java
│       │   └── controller/
│       │       └── admin/
│       │           └── {Entity}ControllerTest.java
│
└── pom.xml
```

### 后端开发输出文件映射

| 需求类型 | 输出文件 |
|---------|---------|
| `new_feature` | DDL · DO · VO · Mapper[+XML] · Service+Impl · ErrorCode · Controller |
| `field_change` | ALTER DDL · DO · VO · Mapper/XML · Service |
| `interface_change` | Controller · Service · VO |
| `logic_refactor` | ServiceImpl |
| `perf_optimize` | Mapper/SQL · 索引 · 缓存 |
| `cache_change` | ServiceImpl · CacheConfig |
| `task_add` | Job · JobConfig |
| `client_add` | Client · DTO |
| `config_change` | application.yaml |

