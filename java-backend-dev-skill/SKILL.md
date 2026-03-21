---
name: backend-dev
description: |
  单体 SpringBoot 后端开发技能（Spring Boot 3 + MyBatis Plus + MySQL 8）。
  覆盖全部后端开发场景：新建功能模块、实体 CRUD、字段增删改、接口变更、逻辑重构、SQL/缓存性能优化、定时任务、外部服务调用。
  任何涉及 Java 后端开发的请求都必须使用此技能，包括但不限于新建模块、字段变更、接口开发、SQL 优化、缓存策略。
  即使用户没有明确说"后端开发"，只要涉及 SpringBoot/MyBatis/MySQL 相关的 Java 代码生成或修改，都应触发此技能。
  纯后端，不含前端代码。
---

# 后端代码开发技能

## 何时使用

使用此技能当：
- 用户请求新建 Java 后端功能模块、实体 CRUD、查询接口、批量操作
- 用户请求字段增删改（加字段、删字段、改字段名、改字段类型/长度/默认值）
- 用户请求新增/修改/删除接口，接口签名变更，新增参数校验
- 用户请求业务逻辑重构、条件分支调整、枚举值扩展、错误码变更
- 用户请求 SQL 优化、N+1 消除、批量改造、并发安全改造
- 用户请求新增/调整缓存策略、新增定时任务、新增外部服务调用
- 用户请求新增/修改 Spring Boot YAML 配置（数据源、Redis、缓存、Quartz、自定义配置等）
- 用户提及 `帮我实现 XXX`、`给 XXX 加字段`、`新增接口`、`优化查询`等后端开发请求

不使用此技能当：
- 前端代码开发（HTML/CSS/JS/Vue/React）
- 纯运维/部署/CI/CD 配置（无 Java 代码变更）
- 纯数据库 DBA 操作（无 Java 代码变更）
- 非 SpringBoot 技术栈的后端开发

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

执行开发任务前，**必须**根据需求类型加载对应的参考文档到上下文中：

| 场景 | 加载文件 |
|------|---------|
| 集合处理、Stream、枚举、异常处理、Hutool、JSON、设计模式、排序、静态工厂、注释规范 | `references/java-best-practices.md` |
| Mapper、SQL、SQL 片段、索引设计、批量操作、MyBatis、分页、N+1、原子操作 | `references/data-layer.md` |
| 事务、Spring Cache、缓存、Redis、并发、日志、幂等、线程池、异步、定时任务、Quartz、外部调用、Client | `references/service-layer.md` |
| Maven、模块结构、依赖管理、pom.xml、BOM | `references/maven-standards.md` |
| 各分层代码模板（DO/VO/Mapper/Service/Controller 完整示例） | `references/code-templates.md` |
| Application YAML 配置文件规范、各组件配置模板、环境分离 | `references/application-config.md` |

---

## 输入参数

执行开发任务时，需要确定以下参数：

| 参数 | 说明 | 获取方式 |
|------|------|---------|
| **需求类型** | `new_feature` / `field_change`(增删改) / `logic_refactor` / `interface_change` / `perf_optimize` / `cache_change` / `task_add` / `client_add` / `config_change` | 从用户描述自动推断 |
| **project** | 项目标识符（如 mall、oms、crm），用于包路径 `com.dainthub.{project}` | 若缺失则询问用户 |
| **module** | 业务模块名（如 trade、member），用于包路径和表名前缀 | 若缺失则询问用户 |
| **entity** | 核心实体名，PascalCase（如 Order、ProductSku），用作类名前缀 | 若缺失则询问用户 |

存量变更场景：若用户未提供现有代码，应**主动搜索项目**找到相关文件（DO/VO/Mapper/Service 等），基于实际代码做精确的 diff 式改动，而非重写全部代码。

---

## 输出清单

根据需求类型确定需要输出的文件：

| 需求类型 | 输出文件范围 |
|---------|------------|
| **new_feature** | DDL · DO · VO(SaveReq/PageReq/Resp) · Mapper[+XML] · Service+Impl · ErrorCode · Controller |
| **field_change** | ALTER DDL · DO 字段同步 · VO 字段+转换方法同步 · Mapper/XML 同步 · Service 校验逻辑同步 |
| **interface_change** | Controller 方法变更 · Service 接口+实现同步 · 新增/修改 VO |
| **logic_refactor** | ServiceImpl 逻辑变更 · 行为一致性验证 |
| **perf_optimize** | Mapper/SQL 优化 · EXPLAIN 验证 · 索引变更评估 |
| **cache_change** | ServiceImpl(@Cacheable/@CacheEvict) · CacheConfig · 缓存穿透/击穿防范 |
| **task_add** | {Entity}SyncJob.java · {Module}JobConfig.java(Trigger+JobDetail) |
| **client_add** | {Entity}Client.java · {Entity}DTO.java |
| **config_change** | application.yaml / application-{profile}.yaml 配置变更 |

---

## 约束总表（Constraints）

> 约束编号贯穿所有参考文件，违反任何一条均视为规范错误。

### 架构约束

| ID | 规则 |
|----|------|
| C-ARCH-001 | DO 不得作为 Controller 方法的入参或出参；必须使用 VO |
| C-ARCH-002 | 数据库读写**仅**在 Mapper 层；Service 层禁止构造 Wrapper 或直接调用非接口方法 |
| C-ARCH-003 | Bean 之间的转换逻辑定义在**目标 Bean** 的静态工厂方法（`of`/`toEntity`）中；Service/Controller 不出现批量 `setXxx` |
| C-ARCH-004 | Service 接口查询单条返回 `Optional<DO>`（调用方决定是否抛异常）；查询列表/分页直接返回集合。禁止跨层暴露 Mapper |
| C-ARCH-005 | DO 可定义业务方法（充血模型）和静态 Comparator/Function；方法实现不得注入或调用 Service/Mapper |
| C-ARCH-006 | 排序、比较等数据结构逻辑优先在 DO 中定义静态 `Comparator`；若依赖多个 DO 类型则在 ServiceImpl 中定义静态 `Comparator`；禁止在 Service 方法内匿名构造排序逻辑 |
| C-ARCH-007 | 所有外部服务调用（HTTP/RPC 等）封装在 `{Entity}Client` 类中；Service 层只调用 Client 接口，不直接使用 RestTemplate/WebClient |

### 代码规范约束

| ID | 规则 |
|----|------|
| C-CODE-001 | 禁止使用数组类型（`T[]`）作为方法参数或返回值；统一使用 `List<T>` |
| C-CODE-002 | 禁止魔法数字；状态/类型字段必须有对应枚举 |
| C-CODE-003 | 禁止 `throw new RuntimeException` 或其子类；统一使用 `ServiceExceptionUtil.exception(ErrorCode)` |
| C-CODE-004 | 工具类统一使用 Hutool（`cn.hutool.*`）；禁止重复造轮子 |
| C-CODE-005 | JSON 序列化/反序列化统一使用 `com.dainthub.{project}.framework.common.util.json.JsonUtils` |
| C-CODE-006 | 关键逻辑分支必须打印日志；日志格式为 `[方法名][描述，key=value]`，必须携带主要业务参数 |
| C-CODE-007 | Controller/Service/Mapper 方法参数超过 3 个时，必须封装为 VO 或 DO 对象传参 |
| C-CODE-008 | 所有 Javadoc 和代码注释使用**中文**编写 |
| C-CODE-009 | Service 接口的每个 `public` 方法必须写 Javadoc，包含：功能说明、`@param`、`@return`、`@throws`（如有） |
| C-CODE-010 | DO 的每个字段必须写 Javadoc，说明业务含义和约束（如取值范围、长度、是否非空）；枚举字段用 `@see` 指向枚举类 |
| C-CODE-011 | 行内注释说明**为什么**这么做，不说**做了什么**；禁止翻译式注释（如 `// 将 status 设为 0`） |
| C-CODE-012 | 代码分区使用 `// ==================== 分区标题 ====================` 格式，用于 DO 充血方法、ServiceImpl 读写操作等逻辑分组 |

### 数据层约束

| ID | 规则 |
|----|------|
| C-DATA-001 | 索引只创建普通索引（`KEY`）；禁止创建唯一索引（`UNIQUE KEY`），唯一性由业务层 `exist{Entity}Name` 校验 |
| C-DATA-002 | 索引字段中不包含 `deleted` 字段 |
| C-DATA-003 | 金额字段使用 `decimal(19,4)`；禁止 `float`/`double` |
| C-DATA-004 | 时间范围查询条件使用 `startTime` / `endTime` 两个独立字段（`LocalDateTime` 类型），禁止用数组或 `List` |
| C-DATA-005 | 批量操作使用 `insertBatch` / `updateBatchById`；禁止循环单条操作 |
| C-DATA-006 | Mapper.xml 必须定义 `<sql id="columns">` 列片段；`SELECT` 语句通过 `<include refid="columns"/>` 引用，禁止 `SELECT *` |

### 配置文件约束

| ID | 规则 |
|----|------|
| C-CONF-001 | YAML 文件使用 `---` 多文档分隔符按功能分区，每区必须有 `## 区域标题 ##` 注释 |
| C-CONF-002 | 跨配置项的重复值必须使用 `${}` 引用消除重复 |
| C-CONF-003 | 环境相关配置（地址/凭证/开关）只能出现在 `application-{profile}.yaml`，禁止写入 `application.yaml` |
| C-CONF-004 | JDBC URL 必须包含 `useSSL=false&serverTimezone=Asia/Shanghai&allowPublicKeyRetrieval=true&nullCatalogMeansCurrent=true&rewriteBatchedStatements=true` |
| C-CONF-005 | 项目自定义配置统一使用 `{project}:` 命名空间，禁止顶层自定义 key |
| C-CONF-006 | 新增配置项后必须同步更新所有 profile 文件（local/dev/prod），保持 key 结构一致 |
| C-CONF-007 | 禁止在配置文件中硬编码明文密码用于生产环境；生产环境使用环境变量或配置中心 |

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

```sql
-- 新建表
CREATE TABLE `{module}_{entity_snake}` (
  `id`          bigint       NOT NULL AUTO_INCREMENT             COMMENT '主键',
  `name`        varchar(64)  NOT NULL DEFAULT ''                 COMMENT '名称',
  `status`      tinyint      NOT NULL DEFAULT 0                  COMMENT '状态（0=禁用 1=启用）',
  `sort_order`  int          NOT NULL DEFAULT 0                  COMMENT '排序值（升序）',
  -- 公共字段（固定顺序）
  `creator`     varchar(64)  NOT NULL DEFAULT ''                 COMMENT '创建者',
  `create_time` datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT '创建时间',
  `updater`     varchar(64)  NOT NULL DEFAULT ''                 COMMENT '更新者',
  `update_time` datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP
                             ON UPDATE CURRENT_TIMESTAMP         COMMENT '更新时间',
  `deleted`     bit(1)       NOT NULL DEFAULT b'0'               COMMENT '是否删除',
  PRIMARY KEY (`id`),
  -- 普通索引，不含 deleted（C-DATA-001/002）
  KEY `idx_{entity_snake}_status` (`status`),
  KEY `idx_{entity_snake}_create_time` (`create_time`)
) ENGINE = InnoDB COMMENT = '{entity 中文描述}';

-- 存量新增字段（设默认值，避免 MDL 锁表）
ALTER TABLE `{module}_{entity_snake}`
  ADD COLUMN `{field}` {type} NOT NULL DEFAULT {default} COMMENT '{描述}'
  AFTER `{prev_field}`;

-- 存量删除字段（确认无代码引用后执行）
ALTER TABLE `{module}_{entity_snake}` DROP COLUMN `{field}`;
```

### Step 3-8：分层代码模板

> 加载 `references/code-templates.md` 获取 DO / VO / Mapper / ErrorCode / Service / Controller 的完整代码模板。

各分层模板要点速查：

| 分层 | 关键规范 |
|------|---------|
| **DO** | 充血模型业务方法(C-ARCH-005) · 静态 Comparator(C-ARCH-006) · 静态 Function |
| **VO** | 转换方法在目标 Bean(C-ARCH-003) · `toEntity`/`of`/`ofList`/`ofPage`/`indexById` · 时间范围用独立字段(C-DATA-004) |
| **Mapper** | 简单查询用 default 方法 · 复杂查询用 XML · `<sql id="columns">`(C-DATA-006) · 条件构造在 Mapper 层(C-ARCH-002) |
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
□ [C-DATA-001] 无 UNIQUE KEY
□ [C-DATA-002] 索引字段无 deleted
□ [C-DATA-003] 金额用 decimal(19,4)
□ [C-DATA-004] 时间范围用 startTime/endTime 独立字段
□ [C-DATA-005] 批量操作用 insertBatch/updateBatchById
□ [C-DATA-006] Mapper.xml 定义 <sql id="columns"> 片段，SELECT 通过 <include> 引用

配置文件（涉及 YAML 变更时检查）：
□ [C-CONF-001] 功能分区有 --- 分隔符和标题注释
□ [C-CONF-002] 重复值用 ${} 引用
□ [C-CONF-003] 环境相关配置只在 profile 文件中
□ [C-CONF-004] JDBC URL 参数齐全
□ [C-CONF-005] 自定义配置在 {project}: 命名空间下
□ [C-CONF-006] 所有 profile 文件（local/dev/prod）已同步
□ [C-CONF-007] 无硬编码明文密码（生产环境）
```
