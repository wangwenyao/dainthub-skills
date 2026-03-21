# Application 配置文件规范

> 本文件定义 Spring Boot YAML 配置文件的编写规范和约束。

---

## 文件结构

```
{project}-server/src/main/resources/
├── application.yaml           # 主配置：所有环境共享的行为配置
├── application-local.yaml     # 本地开发环境：数据库/Redis 地址、调试开关
├── application-dev.yaml       # 开发/测试环境：数据库/Redis 地址、线上开关
└── application-prod.yaml      # 生产环境：数据库/Redis 地址、生产开关
```

### 环境分离原则

| 配置类型 | 放置位置 | 示例 |
|---------|---------|------|
| **行为配置**（所有环境一致） | `application.yaml` | Jackson 序列化、MyBatis Plus 全局配置、Swagger、缓存策略 |
| **连接地址/凭证**（按环境变化） | `application-{profile}.yaml` | 数据库 URL/密码、Redis 地址、MQ 地址 |
| **开关配置**（按环境变化） | `application-{profile}.yaml` | Quartz 自动启动、验证码开关、演示模式、日志级别 |

**规则**：
- `application.yaml` 中 `spring.profiles.active` 默认设为 `local`
- 禁止在 `application.yaml` 中硬编码任何环境相关的连接地址或密码
- 新增 profile 文件必须遵循 `application-{env}.yaml` 命名

---

## 文件格式规范

### C-CONF-001：使用 YAML 多文档分隔符按功能分区

每个功能区域使用 `---` 分隔，并附带可视化标题注释：

```yaml
--- #################### 数据库相关配置 ####################

spring:
  datasource:
    ...

--- #################### 定时任务相关配置 ####################

spring:
  quartz:
    ...

--- #################### 消息队列相关 ####################

rocketmq:
  ...
```

**标准分区顺序**（在 `application.yaml` 中）：

1. `spring` 核心配置（application、profiles、servlet、jackson、cache）
2. `server` 配置
3. 接口文档配置（springdoc、knife4j）
4. 第三方框架配置（flowable、mybatis-plus 等）
5. 验证码配置
6. 消息队列配置
7. AI 相关配置
8. 项目自定义配置（`{project}:` 命名空间）

**标准分区顺序**（在 `application-{profile}.yaml` 中）：

1. `server.port`
2. 数据库相关配置
3. Redis 配置
4. 定时任务配置
5. 消息队列配置
6. 服务保障配置（分布式锁等）
7. 监控配置（Actuator、Spring Boot Admin）
8. 日志配置
9. 第三方服务配置（微信、支付等）
10. 项目自定义配置（`{project}:` 命名空间）

### C-CONF-002：使用 `${}` 引用消除重复

```yaml
# ✅ 正确：通过引用避免硬编码重复
{project}:
  info:
    version: 1.0.0
    base-package: com.dainthub.{project}

mybatis-plus:
  type-aliases-package: ${{project}.info.base-package}.module.*.dal.dataobject

{project}:
  codegen:
    base-package: ${{project}.info.base-package}
    db-schemas: ${spring.datasource.dynamic.datasource.master.name}

# ✅ 消息队列中引用 application name
rocketmq:
  producer:
    group: ${spring.application.name}_PRODUCER

# ❌ 错误：硬编码重复值
rocketmq:
  producer:
    group: {project}-server_PRODUCER
```

---

## 各组件配置模板

### 数据源（Druid + 动态多数据源）

```yaml
spring:
  datasource:
    druid: # Druid 【监控】相关的全局配置
      web-stat-filter:
        enabled: true
      stat-view-servlet:
        enabled: true
        allow: # 设置白名单，不填则允许所有访问
        url-pattern: /druid/*
        login-username: # 控制台管理用户名和密码
        login-password:
      filter:
        stat:
          enabled: true
          log-slow-sql: true # 慢 SQL 记录
          slow-sql-millis: 100 # 慢 SQL 阈值，单位：毫秒
          merge-sql: true
        wall:
          config:
            multi-statement-allow: true
    dynamic: # 多数据源配置
      druid: # Druid 【连接池】相关的全局配置
        initial-size: 1 # 初始连接数（local 用 1，dev/prod 用 5）
        min-idle: 1 # 最小连接池数量（local 用 1，dev/prod 用 10）
        max-active: 20 # 最大连接池数量
        max-wait: 60000 # 获取连接等待超时，单位：毫秒（1 分钟）
        time-between-eviction-runs-millis: 60000 # 空闲连接检测间隔，单位：毫秒（1 分钟）
        min-evictable-idle-time-millis: 600000 # 连接最小生存时间，单位：毫秒（10 分钟）
        max-evictable-idle-time-millis: 1800000 # 连接最大生存时间，单位：毫秒（30 分钟）
        validation-query: SELECT 1 FROM DUAL # 连接有效性检测 SQL
        test-while-idle: true
        test-on-borrow: false
        test-on-return: false
      primary: master
      datasource:
        master:
          url: jdbc:mysql://{host}:{port}/{db}?useSSL=false&serverTimezone=Asia/Shanghai&allowPublicKeyRetrieval=true&nullCatalogMeansCurrent=true&rewriteBatchedStatements=true
          username: {username}
          password: {password}
```

**JDBC URL 必备参数**：

| 参数 | 值 | 说明 |
|------|-----|------|
| `useSSL` | `false` | 本地/内网不启用 SSL |
| `serverTimezone` | `Asia/Shanghai` | 统一时区 |
| `allowPublicKeyRetrieval` | `true` | MySQL 8 公钥检索 |
| `nullCatalogMeansCurrent` | `true` | 仅查询当前数据库的表 |
| `rewriteBatchedStatements` | `true` | 开启批量写入优化（配合 C-DATA-005） |

### Redis

```yaml
spring:
  data:
    redis:
      host: {host} # 地址
      port: 6379 # 端口
      database: 0 # 数据库索引（local 用 0，dev 用 1，prod 用不同值避免串数据）
      password: {password} # 密码，生产环境必须设置
      repositories:
        enabled: false # 禁用 Spring Data Redis Repository，加快启动速度
```

### Spring Cache

```yaml
spring:
  cache:
    type: REDIS
    redis:
      time-to-live: 1h # 全局默认过期时间
```

### MyBatis Plus

```yaml
mybatis-plus:
  configuration:
    map-underscore-to-camel-case: true # 下划线转驼峰（显式声明）
  global-config:
    db-config:
      id-type: NONE # 智能模式，自动适配 AUTO/INPUT
      logic-delete-value: 1 # 逻辑已删除值
      logic-not-delete-value: 0 # 逻辑未删除值
    banner: false # 关闭控制台 Banner
  type-aliases-package: ${{project}.info.base-package}.module.*.dal.dataobject
  encryptor:
    password: {加解密秘钥} # 字段加密秘钥

mybatis-plus-join:
  banner: false # 关闭 Banner
  sub-table-logic: true # 全局启用副表逻辑删除
  table-alias: t # 表别名
  logic-del-type: on # 副表逻辑删除条件位置（ON/WHERE）
```

### Jackson

```yaml
spring:
  jackson:
    serialization:
      write-dates-as-timestamps: true # Date 使用时间戳格式
      write-date-timestamps-as-nanoseconds: false # 不使用纳秒，直接毫秒（如 1611460870401）
      write-durations-as-timestamps: true # Duration 使用时间戳格式
      fail-on-empty-beans: false # 允许序列化无属性的 Bean
```

### Quartz 定时任务

```yaml
spring:
  quartz:
    auto-startup: true # local 环境建议 false，dev/prod 设 true
    scheduler-name: schedulerName # Scheduler 名字
    job-store-type: jdbc # 使用数据库存储 Job
    wait-for-jobs-to-complete-on-shutdown: true # 关闭时等待任务完成
    properties:
      org:
        quartz:
          scheduler:
            instanceName: schedulerName
            instanceId: AUTO # 自动生成实例 ID
          jobStore:
            class: org.springframework.scheduling.quartz.LocalDataSourceJobStore
            isClustered: true # 集群模式
            clusterCheckinInterval: 15000 # 集群检查频率，单位：毫秒（15 秒）
            misfireThreshold: 60000 # misfire 阈值，单位：毫秒
          threadPool:
            threadCount: 25 # 线程池大小
            threadPriority: 5 # 线程优先级
            class: org.quartz.simpl.SimpleThreadPool
    jdbc:
      initialize-schema: NEVER # 手动创建表结构，不自动初始化
```

### 日志

```yaml
logging:
  file:
    name: /opt/app/logs/${spring.application.name}.log # 日志文件路径
  level:
    # 按模块配置 Mapper 日志级别，方便调试 SQL
    com.dainthub.{project}.module.{module}.dal.mysql: debug
    # 高频写入的 Mapper 单独设为 INFO，避免日志爆炸
    com.dainthub.{project}.module.infra.dal.mysql.logger.ApiErrorLogMapper: INFO
```

### 接口文档（SpringDoc + Knife4j）

```yaml
springdoc:
  api-docs:
    enabled: true
    path: /v3/api-docs
  swagger-ui:
    enabled: true
    path: /swagger-ui
  default-flat-param-object: true # 参数对象扁平化展示

knife4j:
  enable: true
  setting:
    language: zh_cn
```

### 项目自定义配置命名空间

所有项目自定义配置统一使用 `{project}:` 命名空间：

```yaml
{project}:
  info:
    version: 1.0.0
    base-package: com.dainthub.{project}
  web:
    admin-ui:
      url: http://dashboard.{project}.dainthub.com
  xss:
    enable: false
    exclude-urls:
      - ${spring.boot.admin.context-path}/**
  security:
    permit-all_urls:
      - /admin-api/mp/open/**
  websocket:
    enable: true
    path: /infra/ws
    sender-type: local # 可选值：local / redis / rocketmq / kafka / rabbitmq
  tenant:
    enable: true
    ignore-urls:
      - /jmreport/*
    ignore-tables: []
    ignore-caches:
      - user_role_ids
      - oauth_client
```

---

## 配置约束总表

| ID | 规则 |
|----|------|
| C-CONF-001 | YAML 文件使用 `---` 多文档分隔符按功能分区，每区必须有 `## 区域标题 ##` 注释 |
| C-CONF-002 | 跨配置项的重复值必须使用 `${}` 引用消除重复 |
| C-CONF-003 | 环境相关配置（地址/凭证/开关）只能出现在 `application-{profile}.yaml` 中，禁止写入 `application.yaml` |
| C-CONF-004 | JDBC URL 必须包含 `useSSL=false&serverTimezone=Asia/Shanghai&allowPublicKeyRetrieval=true&nullCatalogMeansCurrent=true&rewriteBatchedStatements=true` |
| C-CONF-005 | 项目自定义配置统一使用 `{project}:` 命名空间，禁止使用顶层自定义 key |
| C-CONF-006 | 新增配置项后必须同步更新所有 profile 文件（local/dev/prod），保持 key 结构一致 |
| C-CONF-007 | 禁止在配置文件中硬编码明文密码用于生产环境；生产环境使用环境变量 `${DB_PASSWORD}` 或配置中心 |

---

## 新增模块配置 Checklist

当新增业务模块涉及配置变更时，逐项检查：

```
□ 新增配置是行为配置还是环境配置？放对文件了吗？
□ 有重复值吗？是否用 ${} 引用了？
□ 所有 profile 文件（local/dev/prod）都同步了吗？
□ 自定义配置是否在 {project}: 命名空间下？
□ 数据库 URL 参数齐全吗？
□ 日志级别配置了新模块的 Mapper 包路径吗？
```
