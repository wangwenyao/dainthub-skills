# Java Backend Development Skill

单体 SpringBoot 后端开发技能，为 AI 辅助编程提供规范化的开发指导。

## 📖 项目简介

本项目是一套完整的 Java 后端开发技能定义，用于指导 AI 助手进行规范化的 Spring Boot 后端开发。覆盖全部后端开发场景：新建功能模块、实体 CRUD、字段增删改、接口变更、逻辑重构、SQL/缓存性能优化、定时任务、外部服务调用等。

## 🛠 技术栈

| 分层 | 技术 |
|------|------|
| Web | Spring Boot 3 · Spring MVC |
| 持久层 | MyBatis Plus · MySQL 8 |
| 缓存 | Spring Cache · Redis · Redisson |
| 任务调度 | Quartz |
| 工具 | Hutool · Lombok |

## 📁 项目结构

```
java-backend-dev-skill/
├── SKILL.md                           # 技能主文件（触发条件、工作流、约束总表）
└── references/                        # 参考文档目录
    ├── java-best-practices.md         # Java 最佳实践（集合、Stream、枚举、异常、设计模式）
    ├── code-templates.md              # 各分层代码模板（DO/VO/Mapper/Service/Controller）
    ├── data-layer.md                  # 数据层规范（Mapper、SQL、索引、批量操作、数据迁移）
    ├── service-layer.md               # 服务层规范（事务、缓存、定时任务、外部调用、性能验证）
    ├── maven-standards.md             # Maven 规范（模块结构、依赖管理）
    ├── application-config.md          # 配置文件规范（YAML 模板、环境分离）
    ├── test-standards.md              # 测试规范（单元测试、集成测试、Mock、覆盖率）
    ├── security-standards.md          # 安全规范（认证授权、JWT、权限模型、敏感数据）
    ├── api-design.md                  # API 设计（版本管理、参数校验、响应格式）
    └── design-principles.md           # 设计原则（SOLID、DRY/KISS、设计模式、DDD、防御性编程）
```

## 🚀 使用方式

### 适用场景

使用此技能当：
- 新建 Java 后端功能模块、实体 CRUD、查询接口、批量操作
- 字段增删改（加字段、删字段、改字段名、改字段类型/长度/默认值）
- 新增/修改/删除接口，接口签名变更，新增参数校验
- 业务逻辑重构、条件分支调整、枚举值扩展、错误码变更
- SQL 优化、N+1 消除、批量改造、并发安全改造
- 新增/调整缓存策略、新增定时任务、新增外部服务调用
- Spring Boot YAML 配置变更

不使用此技能当：
- 前端代码开发（HTML/CSS/JS/Vue/React）
- 纯运维/部署/CI/CD 配置（无 Java 代码变更）
- 纯数据库 DBA 操作（无 Java 代码变更）
- 非 SpringBoot 技术栈的后端开发

### 参考文档加载指南

执行开发任务前，根据需求类型加载对应的参考文档：

| 场景 | 加载文件 |
|------|---------|
| 集合处理、Stream、枚举、异常处理、Hutool、JSON、设计模式 | [`references/java-best-practices.md`](references/java-best-practices.md) |
| Mapper、SQL、索引设计、批量操作、MyBatis、分页、N+1、数据迁移 | [`references/data-layer.md`](references/data-layer.md) |
| 事务、Spring Cache、Redis、并发、日志、幂等、定时任务、外部调用、性能验证 | [`references/service-layer.md`](references/service-layer.md) |
| Maven、模块结构、依赖管理、pom.xml、BOM | [`references/maven-standards.md`](references/maven-standards.md) |
| 各分层代码模板（DO/VO/Mapper/Service/Controller 完整示例） | [`references/code-templates.md`](references/code-templates.md) |
| Application YAML 配置文件规范、各组件配置模板 | [`references/application-config.md`](references/application-config.md) |
| 单元测试、集成测试、Mock、测试覆盖率 | [`references/test-standards.md`](references/test-standards.md) |
| 认证授权、JWT、权限模型、密码安全、敏感数据 | [`references/security-standards.md`](references/security-standards.md) |
| API 版本管理、参数校验、响应格式、RESTful 规范 | [`references/api-design.md`](references/api-design.md) |
| SOLID、DRY/KISS、设计模式、DDD、防御性编程 | [`references/design-principles.md`](references/design-principles.md) |

## 📋 核心约束速查

### 架构约束

| ID | 规则 |
|----|------|
| C-ARCH-001 | DO 不得作为 Controller 方法的入参或出参；必须使用 VO |
| C-ARCH-002 | 数据库读写仅在 Mapper 层；Service 层禁止构造 Wrapper |
| C-ARCH-003 | Bean 转换逻辑定义在目标 Bean 的静态工厂方法中 |
| C-ARCH-004 | Service 单条查询返回 `Optional<DO>`，列表/分页返回集合 |
| C-ARCH-005 | DO 可定义业务方法（充血模型），但不得注入 Service/Mapper |
| C-ARCH-006 | 排序逻辑优先在 DO 中定义静态 Comparator |
| C-ARCH-007 | 外部服务调用封装在 `{Entity}Client` 类中 |

### 代码规范约束

| ID | 规则 |
|----|------|
| C-CODE-001 | 禁止使用数组类型，统一使用 `List<T>` |
| C-CODE-002 | 禁止魔法数字，状态/类型字段必须有对应枚举 |
| C-CODE-003 | 禁止 `throw new RuntimeException`，统一使用 `ServiceExceptionUtil.exception()` |
| C-CODE-004 | 工具类统一使用 Hutool |
| C-CODE-005 | JSON 序列化统一使用项目 JsonUtils |
| C-CODE-006 | 关键逻辑分支必须打印日志，携带业务参数 |
| C-CODE-007 | 方法参数超过 3 个时，封装为 VO 或 DO 对象 |
| C-CODE-008 | 所有 Javadoc 和代码注释使用中文编写 |

### 数据层约束

| ID | 规则 |
|----|------|
| C-DATA-001 | UNIQUE KEY 仅用于业务必须的唯一性约束 |
| C-DATA-002 | 批量操作使用 `insertBatch`/`updateBatchById` |
| C-DATA-003 | Mapper.xml 必须定义 `<sql id="columns">` 列片段 |

## 📦 输出清单

根据需求类型确定输出文件范围：

| 需求类型 | 输出文件范围 |
|---------|------------|
| new_feature | DDL · DO · VO · Mapper[+XML] · Service+Impl · ErrorCode · Controller |
| field_change | ALTER DDL · DO 字段同步 · VO 字段同步 · Mapper/XML 同步 |
| interface_change | Controller 方法变更 · Service 接口+实现同步 · 新增/修改 VO |
| logic_refactor | ServiceImpl 逻辑变更 |
| perf_optimize | Mapper/SQL 优化 · EXPLAIN 验证 · 索引变更评估 |
| cache_change | ServiceImpl 缓存注解 · CacheConfig |
| task_add | Job 类 · JobConfig |
| client_add | Client 类 · DTO |
| config_change | application.yaml 配置变更 |

## 🏗️ 包路径规范

```
com.dainthub.{project}.module.{module}
  ├── controller.admin
  │   ├── {Entity}Controller.java
  │   └── vo.{entity_snake}
  │       ├── {Entity}SaveReqVO.java
  │       ├── {Entity}PageReqVO.java
  │       └── {Entity}RespVO.java
  ├── service
  │   ├── {Entity}Service.java
  │   └── impl.{Entity}ServiceImpl.java
  ├── dal
  │   ├── dataobject.{entity_snake}.{Entity}DO.java
  │   └── mysql.{entity_snake}.{Entity}Mapper.java
  ├── client                            # 外部服务调用
  └── enums.ErrorCodeConstants.java
```

**资源文件**：`resources/mapper/{module}/{Entity}Mapper.xml`

## 📝 开发工作流

1. **影响范围分析** - 存量变更必做，确定影响文件范围
2. **包路径与命名规范** - 类名 PascalCase，表名/包名 snake_case
3. **DDL 设计** - 表名格式 `{module}_{entity_snake}`
4. **分层代码生成** - 按模板生成 DO/VO/Mapper/Service/Controller
5. **质量门控检查** - 逐条自检约束规则

## 📄 许可证

本项目仅供内部开发参考使用。
