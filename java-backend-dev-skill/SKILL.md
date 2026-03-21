---
name: backend-dev
description: |
  单体 SpringBoot 后端开发（Spring Boot 3 + MyBatis Plus + MySQL 8）。
  触发：新建模块/实体CRUD/字段变更/接口开发/SQL优化/缓存/定时任务/外部调用。
  纯后端，不含前端。
---

# 后端代码开发技能

## 何时使用

适用场景：
- 新建功能模块、实体 CRUD、查询接口、批量操作
- 字段增删改（加字段、删字段、改字段名/类型/长度/默认值）
- 接口新增/修改/删除、接口签名变更、参数校验
- 业务逻辑重构、枚举扩展、错误码变更
- SQL 优化、N+1 消除、批量改造、并发安全改造
- 缓存策略调整、定时任务、外部服务调用
- Spring Boot YAML 配置变更

不适用：
- 前端代码（HTML/CSS/JS/Vue/React）
- 纯运维/部署/CI/CD 配置
- 纯数据库 DBA 操作
- 非 SpringBoot 技术栈

---

## 技术栈

| 分层 | 技术 |
|------|------|
| Web | Spring Boot 3 · Spring MVC |
| 持久层 | MyBatis Plus · MySQL 8 |
| 缓存 | Spring Cache · Redis · Redisson |
| 任务调度 | Quartz |
| 工具 | Hutool · Lombok |

---

## 参考文档

根据需求类型加载：

1. **必须**：`code-templates.md`
2. **按需**：
   - 字段变更/SQL → `data-layer.md` + `ddl-templates.md`
   - 缓存/事务 → `service-layer.md`
   - 并发 → `concurrency.md`
   - 接口 → `api-design.md`
   - 配置 → `application-config.md`
   - 测试 → `test-standards.md`
3. **可选**：`design-principles.md`, `maven-standards.md`

### 文档索引

| 场景 | 文件 |
|------|------|
| 集合/Stream/枚举/异常/Hutool/JSON | `java-best-practices.md` |
| Mapper/SQL/索引/批量操作/N+1 | `data-layer.md` |
| 事务/缓存/Redis/日志/幂等/定时任务 | `service-layer.md` |
| Maven/依赖管理/pom.xml | `maven-standards.md` |
| DO/VO/Mapper/Service/Controller 模板 | `code-templates.md` |
| YAML 配置/环境分离 | `application-config.md` |
| 单元测试/集成测试/Mock | `test-standards.md` |
| API 版本/参数校验/响应格式 | `api-design.md` |
| SOLID/DRY/KISS/设计模式 | `design-principles.md` |
| DDL 模板/字段类型 | `ddl-templates.md` |
| 并发/线程安全/分布式锁 | `concurrency.md` |

---

## 输入参数

| 参数 | 说明 |
|------|------|
| **需求类型** | `new_feature` / `field_change` / `interface_change` / `logic_refactor` / `perf_optimize` / `cache_change` / `task_add` / `client_add` / `config_change` |
| **project** | 项目标识符（如 mall），用于包路径 `com.dainthub.{project}` |
| **module** | 模块名（如 trade），用于包路径和表名前缀 |
| **entity** | 实体名，PascalCase（如 Order），用作类名前缀 |

### 需求类型优先级

```
new_feature > interface_change > field_change > cache_change > task_add > client_add > config_change > logic_refactor > perf_optimize
```

### 组合场景

| 请求 | 类型 | 输出 |
|------|------|------|
| "新建商品模块" | `new_feature` | 完整模块 |
| "加字段+新接口" | `interface_change` | 含字段变更 |
| "优化查询" | `perf_optimize` | SQL/索引/缓存 |
| "新增定时任务" | `task_add` | Job/JobConfig |

> 存量变更：主动搜索相关文件，基于实际代码做 diff 式改动，而非重写。

---

## 输出清单

| 类型 | 输出文件 |
|------|---------|
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

## 约束总表（Constraints）

> 违反任何一条均视为规范错误。

### 架构约束 (C-ARCH)

| ID | 规则 |
|----|------|
| C-ARCH-001 | Controller 入参/出参只用 VO，禁止 DO |
| C-ARCH-002 | 数据库读写仅在 Mapper 层，Service 禁止构造 Wrapper |
| C-ARCH-003 | Bean 转换在目标 Bean 静态方法（`of`/`toEntity`） |
| C-ARCH-004 | 单条查询返回 `Optional<DO>`，列表/分页返回集合 |
| C-ARCH-005 | DO 可有业务方法，但禁止注入 Service/Mapper |
| C-ARCH-006 | 排序用 DO/ServiceImpl 静态 Comparator |
| C-ARCH-007 | 外部调用封装在 `{Entity}Client` |

### 代码规范约束 (C-CODE)

| ID | 规则 |
|----|------|
| C-CODE-001~003 | 禁止数组类型，禁止魔法数字，禁止 RuntimeException |
| C-CODE-004~005 | 工具类用 Hutool，JSON 用 JsonUtils |
| C-CODE-006~007 | 关键分支有日志，方法参数>3 封装为 VO |
| C-CODE-008~012 | Javadoc 用中文，注释说"为什么"，代码用分区格式 |

### 数据层约束 (C-DATA)

| ID | 规则 |
|----|------|
| C-DATA-001 | UNIQUE KEY 仅用于业务必须的唯一性约束 |
| C-DATA-002 | 批量操作用 insertBatch/updateBatchById |
| C-DATA-003 | Mapper.xml 定义 `<sql id="columns">` 片段 |

### 配置约束 (C-CONF)

| ID | 规则 |
|----|------|
| C-CONF-001~007 | YAML 分区注释，环境配置分离，禁止硬编码密码 |

### 安全约束 (C-SEC)

| ID | 规则 |
|----|------|
| C-SEC-001~010 | 密码 BCrypt，Token ≤2h，敏感字段加密，SQL 用 #{} |

### 设计原则约束 (C-DESIGN)

| ID | 规则 |
|----|------|
| C-DESIGN-001~010 | 方法职责单一，分支>3 用策略模式，禁止 null 返回 |

> 详细约束说明 → 各 references 文件

---

## 开发工作流

### Step 0：影响范围分析（存量变更必做）

```
变更类型                影响文件范围                                         注意事项
─────────────────────────────────────────────────────────────────────────────────
新增字段            DDL(ALTER)·DO·VO(SaveReq+Resp)·Mapper.xml(columns片段)   新字段设默认值，防锁表
                    Service(唯一性校验)                                       历史数据回填评估
删除字段            DDL(ALTER)·DO·VO·Mapper(columns片段+条件清除)             确认所有引用已清除
                    Service(清除相关校验逻辑)                                  评估是否破坏接口兼容
字段改名            DDL(RENAME COLUMN)·DO·Mapper.xml(列映射)·VO               全局 grep 检索旧字段名
字段类型/长度变更   DDL(MODIFY)·DO·VO(校验注解同步)·Mapper.xml                评估是否需要数据迁移
新增关联关系        DDL(新增 FK 字段)·DO·Mapper(关联查询)·Service(级联逻辑)   N+1 风险评估
删除关联关系        DDL(DROP COLUMN)·DO·Mapper·Service(移除级联逻辑)           确认无遗留引用
新增接口            Controller·Service(接口+实现)·Mapper·ErrorCode             权限注解不能遗漏
修改接口签名        Controller·Service接口·ServiceImpl·VO(新增/修改)           评估调用方兼容性
删除接口            Controller·Service·Mapper(若仅此方法使用)                  确认无外部调用方
枚举值新增/变更     枚举类·数据库注释·VO(校验注解@InEnum)·文档                  旧数据兼容处理
错误码变更          ErrorCodeConstants·ServiceImpl(引用点)                     对外 API 影响评估
逻辑重构            ServiceImpl·单元测试                                        行为一致性验证
新增缓存            ServiceImpl(@Cacheable/@CacheEvict)·CacheConfig             缓存穿透/击穿防范
新增定时任务        Job类·JobConfig(Trigger+JobDetail)                          Quartz 分布式防重
新增外部调用        {Entity}Client·{Entity}DTO·ServiceImpl                      超时/重试/降级策略
批量操作改造        Mapper(insertBatch/updateBatchById)·ServiceImpl             分批大小(500)评估
性能优化            Mapper/SQL·EXPLAIN 验证·缓存策略                           索引变更评估回归
新增/修改配置       application.yaml·application-{profile}.yaml               所有 profile 同步
```

### Step 1：包路径与命名规范

> **命名规则**：类名用 PascalCase（如 `ProductSku`），表名/包名/URL 用 snake_case（如 `product_sku`）。

```
com.dainthub.{project}.module.{module}
  ├── controller
  │   └── admin
  │       ├── {Entity}Controller.java
  │       └── vo
  │           └── {entity_snake}
  │               ├── {Entity}SaveReqVO.java
  │               ├── {Entity}PageReqVO.java
  │               └── {Entity}RespVO.java
  ├── service
  │   ├── {Entity}Service.java
  │   └── impl
  │       └── {Entity}ServiceImpl.java
  ├── dal
  │   ├── dataobject
  │   │   └── {entity_snake}
  │   │       └── {Entity}DO.java
  │   └── mysql
  │       └── {entity_snake}
  │           └── {Entity}Mapper.java
  ├── client                            # 外部服务调用（如有）
  │   ├── {Entity}Client.java
  │   └── dto
  │       └── {Entity}DTO.java
  ├── job                               # 定时任务（如有）
  │   └── {Entity}SyncJob.java
  ├── config                            # 模块配置（如有）
  │   └── {Module}JobConfig.java
  └── enums
      └── ErrorCodeConstants.java
```

**资源文件**：`resources/mapper/{module}/{Entity}Mapper.xml`

### Step 2：DDL 设计

> **表名格式**：`{module}_{entity_snake}`，例如 `trade_product_sku`。
> **完整 DDL 模板 & 影响范围矩阵** → `references/ddl-templates.md`

**快速判断**：
```
新增字段 → DO + VO + Mapper.xml(columns片段)
新增接口 → Controller + Service + ErrorCode
性能优化 → Mapper/SQL + 索引评估
```

### Step 3-8：分层代码模板

> 加载 `references/code-templates.md` 获取 DO / VO / Mapper / ErrorCode / Service / Controller 的完整代码模板。

各分层模板要点速查：

| 分层 | 关键规范 |
|------|---------|
| **DO** | 充血模型业务方法(C-ARCH-005) · 静态 Comparator(C-ARCH-006) · 静态 Function |
| **VO** | 转换方法在目标 Bean(C-ARCH-003) · `toEntity`/`of`/`ofList`/`ofPage`/`indexById` |
| **Mapper** | 简单查询用 default 方法 · 复杂查询用 XML · `<sql id="columns">`(C-DATA-003) · 条件构造在 Mapper 层(C-ARCH-002) |
| **ErrorCode** | interface(字段默认 `public static final`) · 错误码 = `1` + 模块3位码 + 业务序号3位 |
| **Service** | 单条查询返回 `Optional<DO>`(C-ARCH-004) · `@Transactional(rollbackFor=Exception.class)` · 唯一性校验用 `exist{Entity}Name` |
| **Controller** | 入参/出参只用 VO(C-ARCH-001) · `@PreAuthorize` 权限注解 · 单条查询"不存在"异常可在 Controller 抛出（因 Service 返回 Optional，由调用方决定处理方式） |

---

## 质量门控（Quality Gates）

生成代码前，逐条自检：

```
架构层：
□ [C-ARCH-001] Controller 参数/返回值无 DO
□ [C-ARCH-002] Service 层无 Wrapper 构造
□ [C-ARCH-003] 转换方法在目标 Bean，无批量 setter
□ [C-ARCH-004] 单条查询返回 Optional<DO>；列表/分页返回集合
□ [C-ARCH-005] DO 业务方法无 Service/Mapper 依赖
□ [C-ARCH-006] 排序用 DO/ServiceImpl 静态 Comparator
□ [C-ARCH-007] 外部调用封装在 {Entity}Client

代码规范：
□ [C-CODE-001] 无数组类型
□ [C-CODE-002] 无魔法数字，状态/类型有枚举
□ [C-CODE-003] 无 RuntimeException，统一用 ServiceExceptionUtil.exception()
□ [C-CODE-004] 工具类用 Hutool
□ [C-CODE-005] JSON 用 JsonUtils
□ [C-CODE-006] 关键分支有日志，携带业务参数
□ [C-CODE-007] 方法参数 >3 个时封装为 VO/DO
□ [C-CODE-008] Javadoc 和注释使用中文
□ [C-CODE-009] Service 接口 public 方法有 Javadoc（含 @param/@return/@throws）
□ [C-CODE-010] DO 字段有 Javadoc（业务含义+约束，枚举字段 @see）
□ [C-CODE-011] 行内注释说"为什么"，不说"做什么"
□ [C-CODE-012] 代码分区用 // ========== 分区标题 ========== 格式

数据层：
□ [C-DATA-001] UNIQUE KEY 仅用于业务必须的唯一性约束（如用户名、手机号）
□ [C-DATA-002] 批量操作用 insertBatch/updateBatchById
□ [C-DATA-003] Mapper.xml 定义 <sql id="columns"> 片段，SELECT 通过 <include> 引用

配置文件（涉及 YAML 变更时检查）：
□ [C-CONF-001] 功能分区有 --- 分隔符和标题注释
□ [C-CONF-002] 重复值用 ${} 引用
□ [C-CONF-003] 环境相关配置只在 profile 文件中
□ [C-CONF-004] JDBC URL 参数齐全
□ [C-CONF-005] 自定义配置在 {project}: 命名空间下
□ [C-CONF-006] 所有 profile 文件（local/dev/prod）已同步
□ [C-CONF-007] 无硬编码明文密码（生产环境）
```
