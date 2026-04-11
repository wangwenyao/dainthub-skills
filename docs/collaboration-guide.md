# 分布式协同开发指南

本指南定义了使用 dainthub-skills 技能链路进行分布式协同开发的完整方案，包括项目目录结构、前后端工程结构、git 工作流、版本管理和协作场景。

---

## 适用场景

- 多角色分布式协同开发（产品经理、技术经理、前端开发、后端开发）
- 不同电脑、不同 AI 会话的协作
- 基于 git 作为唯一管理文件记录方式
- 使用 dainthub-skills 技能链路：product-manager → tech-manager → java-backend-dev / vben-frontend-dev

---

## 一、项目整体目录结构

```
project/
├── docs/                              # 协同开发文档目录
│   ├── prd/                           # PRD 文档
│   │   ├── index.md                   # PRD 索引文件
│   │   ├── prd-{模块}-v{版本}.md       # 各模块 PRD
│   │   └── prd-{模块}-v{版本}-er.md    # ER 图文档
│   ├── api/                           # OpenAPI 接口规格
│   │   ├── index.md                   # API 索引文件
│   │   └── openapi-{模块}-v{版本}.yaml # OpenAPI 3.0 文档
│   ├── db/                            # 数据库脚本
│   │   ├── index.md                   # DB 索引文件
│   │   ├── dml-{模块}-v{版本}.sql      # DML 执行脚本
│   │   ├── dml-{模块}-v{版本}-rollback.sql # 回滚脚本
│   │   └── dml-{模块}-checklist-v{版本}.md # 执行清单
│   ├── wireframes/                    # 线框图 + YAML 页面规格
│   │   ├── index.md                   # 线框图索引文件
│   │   ├── wireframes-{模块}-v{版本}.html # HTML 线框图
│   │   └── wireframes-{模块}-v{版本}.yaml # YAML 页面规格
│   ├── reports/                       # 分析报告 + 验证报告 + 偏差报告
│   │   ├── index.md                   # 报告索引文件
│   │   ├── impact-{模块}-v{版本}.md    # 变更影响分析报告
│   │   ├── verify-{模块}-v{版本}.md    # 实现验证报告
│   │   └── deviation-{模块}-v{版本}.md # 偏差反馈报告
│   ├── decisions/                     # 决策记录
│   │   ├── index.md                   # 决策索引文件
│   │   └── decision-{议题}-v{版本}.md  # 产品决策记录
│   └── index.md                       # docs 总索引
│
├── backend/                           # 后端工程（Spring Boot）
│   └── （见后端工程目录结构）
│
├── frontend/                          # 前端工程（Vben Admin）
│   └── （见前端工程目录结构）
│
├── .agents/                           # AI 配置目录
│   ├── skills.json                    # 技能版本锁定（可选）
│   └── AGENTS.md                      # 项目级 AI 配置
│
├── AGENTS.md                          # 项目根目录 AI 配置
├── README.md                          # 项目说明
└── .gitignore
```

---

## 二、前端工程目录结构

基于 Vben Admin 5.x 框架：

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

## 三、后端工程目录结构

基于 Spring Boot 3 + MyBatis Plus：

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
│   │   │   │   └ mysql/
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

---

## 四、git 工作流

### 分支结构

```
main (生产)
    ↓
develop (开发)
    ↓
feature/{模块}-{版本} (功能开发)
```

### 分支命名规范

| 类型 | 命名格式 | 示例 |
|------|---------|------|
| 功能开发 | `feature/{模块}-v{版本}` | `feature/product-v1.0` |
| bug修复 | `fix/{模块}-v{版本}` | `fix/product-v1.1` |
| 技术重构 | `refactor/{模块}-v{版本}` | `refactor/product-v2.0` |

### 版本号规范

格式：`v{大版本}.{小版本}`

| 版本变更 | 规则 | 示例 |
|---------|------|------|
| 大版本 | 架构重构、重大功能变更 | v1.0 → v2.0 |
| 小版本 | 功能迭代、bug修复 | v1.0 → v1.1 |

### Commit Message 格式

```
<type>(scope): <description>

类型：
- feat: 新增功能
- fix: bug修复
- docs: 文档更新
- refactor: 重构
- test: 测试相关
- chore: 杂项

示例：
- feat(product): 新增商品列表页
- fix(trade): 修复订单状态字段类型
- docs(api): 更新 OpenAPI 文档 v1.1
```

---

## 五、文档版本管理

### 状态快照文件（优化 AI 读取）

**问题**：随着版本积累，index.md 文件变大，AI 拉取后需要读取多个文件，token 消耗增加。

**解决方案**：维护 `docs/status.md` 单文件快照，AI 拉取后只读这一个文件即可了解全局状态。

#### status.md 格式

```markdown
# 项目状态快照

> AI 拉取后只需读取此文件了解全局状态，无需读取各目录 index.md
> 更新时间：2026-04-11 10:30

## 各模块当前状态

| 模块 | PRD | OpenAPI | DML | 线框图 | 验证 | 偏差 | 决策 | 当前阶段 |
|------|-----|---------|-----|--------|------|------|------|---------|
| product | v1.2 ✅ | v1.2 ✅ | v1.2 ✅ | v1.2 ✅ | v1.2 ✅ | - | - | ✅ 已完成 |
| trade | v1.1 🚧 | v1.1 ✅ | v1.1 🚧 | v1.1 ✅ | - | - | - | 🚧 DML待执行 |
| user | v1.0 ✅ | v1.0 ✅ | v1.0 ✅ | v1.0 ✅ | v1.0 ❌ | v1.0 🚧 | - | 🚧 偏差待处理 |
| order | v2.0 🚧 | - | - | v2.0 🚧 | - | - | - | 🚧 PRD进行中 |

## 待处理项汇总

| 类型 | 模块 | 版本 | 文件路径 | 处理角色 |
|------|------|------|---------|---------|
| 偏差反馈 | user | v1.0 | docs/reports/deviation-user-v1.0.md | product-manager |
| DML执行 | trade | v1.1 | docs/db/dml-trade-v1.1.sql | java-backend-dev |
| PRD完成 | order | v2.0 | docs/prd/prd-order-v2.0.md | product-manager |

## 最近变更（最近 5 条）

| 时间 | 提交 | 变更内容 | 影响模块 |
|------|------|---------|---------|
| 2026-04-11 10:00 | abc123 | 新增 user 模块验证报告 | user |
| 2026-04-11 09:30 | abc122 | 更新 trade OpenAPI v1.1 | trade |
| 2026-04-11 09:00 | abc121 | 新增 order PRD v2.0 | order |
| ... | ... | ... | ... |

## 下一步任务

根据当前状态，各角色的下一步任务：

| 角色 | 任务 | 输入文件 | 输出文件 |
|------|------|---------|---------|
| product-manager | 处理 user 偏差反馈 | docs/reports/deviation-user-v1.0.md | docs/decisions/decision-user-*.md |
| java-backend-dev | 执行 trade DML | docs/db/dml-trade-v1.1.sql | 更新 status.md DML状态为 ✅ |
| product-manager | 完成 order PRD | docs/prd/prd-order-v2.0.md | PRD完成，通知 tech-manager |
```

#### 状态符号说明

| 符号 | 含义 | 后续动作 |
|------|------|---------|
| ✅ | 已完成 | 无需处理 |
| 🚧 | 进行中 | 需要继续开发/处理 |
| ❌ | 不通过 | 需要修复或偏差处理 |
| ⏸️ | 待处理 | 等待前置条件 |
| - | 无此版本 | 不涉及 |

#### 更新时机（用户显式触发）

**触发方式**：用户向 AI 发起请求，AI 执行更新。

| 触发指令 | AI 执行动作 | 适用场景 |
|---------|------------|---------|
| "更新 status.md" | 更新当前模块状态 + 最近变更 | 完成任务后 |
| "记录提交到 status.md" | 添加最近变更记录 | git commit 后 |
| "更新下一步任务" | 更新"下一步任务"表 | 任务分发/完成后 |
| "新增模块到 status.md" | 添加新模块行 | 开始新模块开发 |

**示例**：

```
用户：我完成了 product 模块的 PRD v1.2，帮我更新 status.md

AI 执行：
1. 读取 docs/status.md
2. 更新"各模块当前状态"表中 product 行：
   - PRD: v1.2 ✅
   - 当前阶段: 🚧 PRD完成，待技术分析
3. 更新"最近变更"表：添加本次提交记录
4. 更新"下一步任务"表：
   - tech-manager: 分析 product PRD → docs/prd/prd-product-v1.2.md
```

**注意**：AI 不会自动更新 status.md，需要用户显式触发。

---

#### 归档触发（用户显式触发）

**触发方式**：用户向 AI 发起请求，AI 执行归档。

| 触发指令 | AI 执行动作 | 适用场景 |
|---------|------------|---------|
| "归档 v1.2" | 移动 v1.2 所有文档到 archive/v1.2/ | 开始新版本前 |
| "开始 v1.3，归档旧版本" | 归档当前 ✅ 版本 + 更新 index.md | 版本迭代 |
| "归档 product v1.2" | 只归档指定模块的 v1.2 | 部分归档 |

**示例**：

```
用户：开始做 product v1.3，帮我归档 v1.2

AI 执行：
1. mkdir docs/archive/v1.2/{prd,api,db,wireframes,reports,decisions}
2. mv docs/prd/prd-product-v1.2.md docs/archive/v1.2/prd/
3. mv docs/prd/prd-product-v1.2-er.md docs/archive/v1.2/prd/
4. mv docs/api/openapi-product-v1.2.yaml docs/archive/v1.2/api/
5. mv docs/db/dml-product-v1.2.sql docs/archive/v1.2/db/
6. ... 移动其他文件
7. 更新 docs/prd/index.md：
   - 移除 v1.2 行
   - 只保留 v1.3（进行中）
8. 创建 docs/archive/v1.2/index.md（归档索引）
9. 更新 docs/status.md：
   - 删除 v1.2 的"进行中版本"行
   - 更新 product 模块状态为 v1.3 🚧
```

**注意**：归档需要用户显式触发，AI 不会自动归档。

---

### 精简 index.md 格式

每个目录的 index.md 只保留最新版本 + 进行中的版本，旧版本归档。

#### 精简 index.md 模板

```markdown
# {目录名} 索引

> 当前版本 + 进行中版本，旧版本见 archive/

## 当前版本

| 文件 | 版本 | 状态 | 说明 |
|------|------|------|------|
| prd-product-v1.2.md | v1.2 | ✅ | 最新稳定版本 |

## 进行中版本

| 文件 | 版本 | 状态 | 说明 |
|------|------|------|------|
| prd-product-v1.3.md | v1.3 | 🚧 | 新增 SKU 字段 |

---

> 归档版本见 `archive/v1.0/`、`archive/v1.1/`
```

#### 归档规则（用户显式触发）

| 规则 | 说明 |
|------|------|
| 归档时机 | 版本状态变为 ✅ 后，且有新版本开始 🚧 |
| 归档位置 | `docs/archive/v{版本}/` |
| 归档内容 | 该版本的所有相关文档 |
| 触发方式 | 用户说"归档 v{版本}"或"开始新版本，归档旧版本" |
| 执行者 | AI（响应用户请求） |

**归档触发指令**：

| 用户指令 | AI 执行动作 |
|---------|------------|
| "归档 v1.2" | 移动 v1.2 所有文档到 archive/v1.2/ + 更新 index.md |
| "开始 v1.3，归档旧版本" | 归档当前 ✅ 版本 + 开始新版本 🚧 |
| "归档 product v1.2" | 只归档指定模块的 v1.2 文档 |

---

### 版本归档机制

#### 归档目录结构

```
docs/
├── archive/
│   ├── v1.0/                          # v1.0 所有文档归档
│   │   ├── prd/
│   │   │   ├── prd-product-v1.0.md
│   │   │   └── prd-product-v1.0-er.md
│   │   ├── api/
│   │   │   └── openapi-product-v1.0.yaml
│   │   ├── db/
│   │   │   ├── dml-product-v1.0.sql
│   │   │   └── dml-product-v1.0-rollback.sql
│   │   ├── wireframes/
│   │   │   ├── wireframes-product-v1.0.html
│   │   │   └── wireframes-product-v1.0.yaml
│   │   ├── reports/
│   │   │   ├── impact-product-v1.0.md
│   │   │   └── verify-product-v1.0.md
│   │   └── decisions/
│   │   │   └── decision-product-sku-v1.0.md
│   │   └── index.md                   # v1.0 归档索引
│   ├── v1.1/                          # v1.1 所有文档归档
│   │   └── ...（同上结构）
│   └── index.md                       # 归档总索引
│
├── prd/
│   ├── index.md                       # 只保留 v1.2 + v1.3
│   ├── prd-product-v1.2.md            # 最新稳定版本
│   └── prd-product-v1.3.md            # 进行中版本
│
└── status.md                          # 当前状态快照（AI 只读此文件）
```

#### 归档触发条件

| 条件 | 动作 |
|------|------|
| 新版本开始（v1.3 🚧） | 归档 v1.2 到 `archive/v1.2/` |
| 版本完成且无新版本 | 保留在 index.md（不归档） |
| 大版本变更（v2.0） | 归档所有 v1.x 到 `archive/v1.x/` |

#### 归档执行命令

```bash
# 归档 v1.2 版本
mkdir -p docs/archive/v1.2/{prd,api,db,wireframes,reports,decisions}
mv docs/prd/prd-product-v1.2.md docs/archive/v1.2/prd/
mv docs/api/openapi-product-v1.2.yaml docs/archive/v1.2/api/
# ... 其他文档

# 更新 index.md
# 移除归档版本，只保留最新 + 进行中

# 更新 status.md
# 更新"最近变更"，添加归档记录
```

---

### 文件命名规范

| 文件类型 | 命名格式 |
|---------|---------|
| PRD | `prd-{模块}-v{版本}.md` |
| ER图 | `prd-{模块}-v{版本}-er.md` |
| OpenAPI | `openapi-{模块}-v{版本}.yaml` |
| DML执行脚本 | `dml-{模块}-v{版本}.sql` |
| DML回滚脚本 | `dml-{模块}-v{版本}-rollback.sql` |
| 执行清单 | `dml-{模块}-checklist-v{版本}.md` |
| HTML线框图 | `wireframes-{模块}-v{版本}.html` |
| YAML页面规格 | `wireframes-{模块}-v{版本}.yaml` |
| 影响分析报告 | `impact-{模块}-v{版本}.md` |
| 验证报告 | `verify-{模块}-v{版本}.md` |
| 偏差报告 | `deviation-{模块}-v{版本}.md` |
| 决策记录 | `decision-{议题}-v{版本}.md` |

### 索引文件结构

每个目录的 `index.md` 维护文件列表：

```markdown
# {目录名} 索引

| 文件 | 版本 | 状态 | 更新日期 | 说明 |
|------|------|------|---------|------|
| prd-product-v1.0.md | v1.0 | ✅ 已完成 | 2026-04-10 | 商品模块 PRD |
| prd-product-v1.1.md | v1.1 | 🚧 进行中 | 2026-04-15 | 新增 SKU 字段 |
```

---

## 六、协作场景示例

### 场景一：新增功能模块

**角色**：产品经理（电脑 A）→ 技术经理（电脑 B）→ 前端开发（电脑 C）+ 后端开发（电脑 D）

```
Step 1: 产品经理 → 输出 PRD
  - 生成：docs/prd/prd-product-v1.0.md
  - 生成：docs/prd/prd-product-v1.0-er.md
  - 生成：docs/wireframes/wireframes-product-v1.0.html
  - 生成：docs/wireframes/wireframes-product-v1.0.yaml
  - 提交：git add docs/prd/ docs/wireframes/
  - 推送：git push origin feature/product-v1.0

Step 2: 技术经理 → 拉取 → 分析 → 输出技术规格
  - 拉取：git pull origin feature/product-v1.0
  - 读取：docs/prd/prd-product-v1.0.md + docs/prd/prd-product-v1.0-er.md
  - 分析：变更影响分析
  - 生成：docs/api/openapi-product-v1.0.yaml
  - 生成：docs/db/dml-product-v1.0.sql
  - 生成：docs/db/dml-product-v1.0-rollback.sql
  - 生成：docs/db/dml-product-checklist-v1.0.md
  - 生成：docs/reports/impact-product-v1.0.md
  - 提交：git add docs/api/ docs/db/ docs/reports/
  - 推送：git push origin feature/product-v1.0

Step 3: 前端开发 + 后端开发 → 拉取 → 并行开发
  - 拉取：git pull origin feature/product-v1.0
  
  【后端开发】
  - 读取：docs/db/dml-product-v1.0.sql → 执行数据库脚本
  - 读取：docs/api/openapi-product-v1.0.yaml → Controller 接口定义
  - 开发：backend/src/main/java/.../module/product/
  - 提交：git add backend/
  
  【前端开发】
  - 读取：docs/api/openapi-product-v1.0.yaml → API 类型定义
  - 读取：docs/wireframes/wireframes-product-v1.0.yaml → 页面 Schema
  - 开发：frontend/apps/web-antd/src/views/product/
  - 提交：git add frontend/
  
  - 推送：git push origin feature/product-v1.0

Step 4: 技术经理 → 拉取 → 验证 → 偏差处理
  - 拉取：git pull origin feature/product-v1.0
  - 读取：docs/prd/prd-product-v1.0.md + backend/ + frontend/
  - 验证：实现验证
  - 生成：docs/reports/verify-product-v1.0.md
  
  【验证通过】
  - 合并：git checkout develop && git merge feature/product-v1.0
  
  【验证不通过】
  - 生成：docs/reports/deviation-product-v1.0.md
  - 提交：git add docs/reports/
  - 推送：git push origin feature/product-v1.0
  - 通知产品经理处理偏差

Step 5: 产品经理 → 拉取 → 决策 → 更新 PRD
  - 拉取：git pull origin feature/product-v1.0
  - 读取：docs/reports/deviation-product-v1.0.md
  - 决策：产品决策
  - 生成：docs/decisions/decision-product-sku-v1.0.md
  - 更新：docs/prd/prd-product-v1.1.md（如需）
  - 提交：git add docs/decisions/ docs/prd/
  - 推送：git push origin feature/product-v1.0
  
  【决策：更新 PRD】
  - 通知技术经理重新分析
  
  【决策：调整实现】
  - 通知前后端开发重新实现
```

### 场景二：字段变更

**角色**：产品经理 → 技术经理 → 后端开发 + 前端开发

```
Step 1: 产品经理 → 提出字段变更需求
  - 更新：docs/prd/prd-product-v1.1.md
  - 提交：git add docs/prd/

Step 2: 技术经理 → 分析影响
  - 读取：docs/prd/prd-product-v1.1.md
  - 分析：字段变更影响（数据库 + DO + VO + Mapper + Service + Controller + 前端 Schema）
  - 生成：docs/db/dml-product-v1.1.sql（ALTER TABLE）
  - 生成：docs/db/dml-product-v1.1-rollback.sql
  - 生成：docs/reports/impact-product-v1.1.md
  - 更新：docs/api/openapi-product-v1.1.yaml（字段变更）
  - 提交：git add docs/db/ docs/api/ docs/reports/

Step 3: 后端开发 + 前端开发 → 执行变更
  - 拉取最新 docs/
  
  【后端开发】
  - 执行：docs/db/dml-product-v1.1.sql
  - 更新：DO · VO · Mapper.xml · Service · Controller
  
  【前端开发】
  - 更新：data.ts（Schema 字段）
  - 更新：api/product.ts（接口参数）

Step 4: 技术经理 → 验证字段变更
  - 验证：字段完整性、类型一致性、历史数据处理
```

---

## 七、AI 配置建议

### 项目级 AGENTS.md 示例

```markdown
# 项目 AI 配置

## 技能锁定

使用以下技能版本：

| Skill | 版本 | 来源 |
|-------|------|------|
| product-manager | v2.1 | dainthub-skills |
| tech-manager | v2.1 | dainthub-skills |
| java-backend-dev | v1.0 | dainthub-skills |
| vben-frontend-dev | v2.0 | dainthub-skills |

## 协作约定

- PRD 输出目录：docs/prd/
- OpenAPI 输出目录：docs/api/
- DML 输出目录：docs/db/
- 前端工程：frontend/
- 后端工程：backend/

## 版本同步

每次开发前：
1. git pull 获取最新 docs/
2. 读取 docs/status.md 了解当前状态（单文件，无需读取多个 index.md）
3. 根据 status.md 中的"下一步任务"确认当前任务
4. 开发完成后更新 status.md

## 参考文档

- 分布式协同开发指南：docs/collaboration-guide.md
```

### 技能版本锁定（可选）

`.agents/skills.json`：

```json
{
  "skills": {
    "product-manager": {
      "source": "dainthub-skills",
      "version": "v2.1"
    },
    "tech-manager": {
      "source": "dainthub-skills",
      "version": "v2.1"
    },
    "java-backend-dev": {
      "source": "dainthub-skills",
      "version": "v1.0"
    },
    "vben-frontend-dev": {
      "source": "dainthub-skills",
      "version": "v2.0"
    }
  }
}
```

---

## 八、技能链路协作关系

```
product-manager
       ↓ docs/prd/ + docs/wireframes/ + docs/status.md
       
tech-manager
       ↓ docs/api/ + docs/db/ + docs/reports/ + docs/status.md
       ↓ 任务分发（携带文档路径）
       
       ┌────────────────┴────────────────┐
       ↓                                 ↓
java-backend-dev                   vben-frontend-dev
（读取 docs/status.md + docs/db/ + docs/api/）  （读取 docs/status.md + docs/api/ + docs/wireframes/）
       ↓                                 ↓
       └─── backend/ ────────── frontend/ ────┘
                        ↓
                 tech-manager 实现验证
                        ↓
                 docs/reports/verify-{模块}-v{版本}.md
                        ↓
                 偏差反馈 → product-manager 决策
                        ↓
                 docs/decisions/ + docs/prd/ + docs/status.md 更新
```

---

## 九、拉取同步流程（优化版）

当 git pull 获取最新变更后，**只读取 docs/status.md** 即可了解全局状态：

### Step 1：检查变更

```bash
git pull origin {branch}
git log --oneline -5           # 查看最近提交
```

### Step 2：读取状态快照（关键优化）

**只读取 `docs/status.md` 一个文件**，无需读取多个 index.md：

```markdown
# AI 拉取后动作：
1. 读取 docs/status.md（单文件，包含全局状态）
2. 查看"各模块当前状态"表 → 了解所有模块状态
3. 查看"待处理项汇总"表 → 确认自己需要处理的任务
4. 查看"下一步任务"表 → 确认具体输入/输出文件路径
```

### Step 3：各 Skill 拉取后动作

根据 status.md 中的"待处理项汇总"和"下一步任务"，执行对应动作：

#### product-manager 拉取后

| status.md 显示 | 动作 |
|---------------|------|
| 偏差反馈 🚧 | 读取对应 deviation 文件 → 执行偏差处理 |
| PRD 🚧 进行中 | 继续完成 PRD |
| 无待处理项 | 等待新需求 |

#### tech-manager 拉取后

| status.md 显示 | 动作 |
|---------------|------|
| PRD 🚧 → 新版本 | 读取 PRD → 变更分析 → OpenAPI + DML |
| 决策 🚧 → 需重新实现 | 重新分发任务 |
| 验证 ❌ | 等待偏差处理完成 |
| 无待处理项 | 等待开发完成触发验证 |

#### java-backend-dev 拉取后

| status.md 显示 | 动作 |
|---------------|------|
| DML 🚧 待执行 | 读取 DML 文件 → 执行脚本 → 更新 status.md |
| OpenAPI 有更新 | 读取 OpenAPI → 更新代码 |
| 无待处理项 | 继续当前开发 |

#### vben-frontend-dev 拉取后

| status.md 显示 | 动作 |
|---------------|------|
| 线框图 🚧 有更新 | 读取 YAML/HTML → 更新 Schema |
| OpenAPI 有更新 | 读取 OpenAPI → 更新 API |
| 无待处理项 | 继续当前开发 |

### Step 4：更新 status.md

完成任务后，更新 status.md：

| 完成的任务 | 更新内容 |
|----------|---------|
| 文档状态变更 | 更新"各模块当前状态"表中的状态符号 |
| 新增待处理项 | 添加到"待处理项汇总"表 |
| 任务完成 | 更新"下一步任务"表 |
| 提交代码 | 更新"最近变更"表 |

### 拉取同步检查清单（精简版）

每次 git pull 后，AI 只需：

- [ ] `git log --oneline -5` 了解最近提交
- [ ] `读取 docs/status.md`（单文件，替代多个 index.md）
- [ ] 查看"待处理项汇总"确认自己需要处理的任务
- [ ] 查看"下一步任务"确认输入/输出文件路径
- [ ] 执行任务
- [ ] 更新 docs/status.md

---

## 十、检查清单

### 开发前检查

- [ ] git pull 获取最新代码
- [ ] 读取 docs/status.md 了解当前状态（单文件）
- [ ] 确认技能版本（检查 .agents/skills.json）
- [ ] 根据 status.md 中的"下一步任务"确认输入文件

### 开发后检查

- [ ] 代码已提交到正确分支
- [ ] 更新 docs/status.md（状态变更 + 最近变更）
- [ ] 如有归档需求，执行版本归档
- [ ] 运行测试验证
- [ ] git push 推送变更

### 合并前检查

- [ ] docs/status.md 中验证状态为 ✅
- [ ] 偏差报告已处理（status.md 中无 🚧 偏差）
- [ ] 决策记录已生成（docs/decisions/）
- [ ] 冲突已解决
- [ ] git merge 到 develop

---

## 版本

- v1.3
- 更新: 2026-04-11
- 新增: 触发执行说明（用户显式触发 status.md 更新和归档）
- v1.2: status.md 状态快照机制、精简 index.md 格式、版本归档机制
- v1.1: 拉取同步流程、状态流转图
- v1.0: 完整分布式协同开发方案、前后端工程目录结构、git 工作流