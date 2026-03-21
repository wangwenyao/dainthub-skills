# DDL 模板与影响范围分析

> 本文件包含数据库 DDL 模板和变更影响范围矩阵，由 SKILL.md 按需加载。

---

## 一、DDL 模板

### 1.1 新建表

> **表名格式**：`{module}_{entity_snake}`，例如 `trade_product_sku`。

```sql
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
```

### 1.2 新增字段（存量表）

> 设默认值，避免 MDL 锁表。

```sql
ALTER TABLE `{module}_{entity_snake}`
  ADD COLUMN `{field}` {type} NOT NULL DEFAULT {default} COMMENT '{描述}'
  AFTER `{prev_field}`;
```

### 1.3 删除字段

> 确认无代码引用后执行。

```sql
ALTER TABLE `{module}_{entity_snake}` DROP COLUMN `{field}`;
```

### 1.4 字段改名

```sql
ALTER TABLE `{module}_{entity_snake}` 
  RENAME COLUMN `{old_field}` TO `{new_field}`;
```

### 1.5 字段类型/长度变更

> 评估是否需要数据迁移。

```sql
ALTER TABLE `{module}_{entity_snake}` 
  MODIFY COLUMN `{field}` {new_type} COMMENT '{描述}';
```

---

## 二、索引设计规范

| 规则 ID | 规则 | 说明 |
|---------|------|------|
| C-DATA-001 | 优先普通索引 | 唯一索引仅用于业务必须的唯一性约束 |
| C-DATA-002 | 索引不含 `deleted` | 软删除字段不参与索引 |

### 索引命名规范

```
idx_{表名简写}_{字段名}           -- 普通索引
uk_{表名简写}_{字段名}            -- 唯一索引（慎用）
```

---

## 三、影响范围矩阵

### 3.1 变更类型 → 影响文件

| 变更类型 | 影响文件 | 注意事项 |
|---------|---------|---------|
| **新增字段** | DDL · DO · VO(SaveReq+Resp) · Mapper.xml(columns) · Service(唯一性校验) | 新字段设默认值，历史数据回填评估 |
| **删除字段** | DDL · DO · VO · Mapper(columns+条件清除) · Service(清除相关校验) | 确认所有引用已清除，评估接口兼容 |
| **字段改名** | DDL(RENAME) · DO · Mapper.xml(列映射) · VO | 全局 grep 检索旧字段名 |
| **字段类型变更** | DDL(MODIFY) · DO · VO(校验注解同步) · Mapper.xml | 评估数据迁移 |
| **新增关联** | DDL(FK字段) · DO · Mapper(关联查询) · Service(级联逻辑) | N+1 风险评估 |
| **删除关联** | DDL(DROP COLUMN) · DO · Mapper · Service | 确认无遗留引用 |
| **新增接口** | Controller · Service(接口+实现) · Mapper · ErrorCode | 权限注解不能遗漏 |
| **修改接口签名** | Controller · Service接口 · ServiceImpl · VO | 评估调用方兼容性 |
| **删除接口** | Controller · Service · Mapper(若仅此方法使用) | 确认无外部调用方 |
| **枚举值变更** | 枚举类 · 数据库注释 · VO(@InEnum) · 文档 | 旧数据兼容处理 |
| **错误码变更** | ErrorCodeConstants · ServiceImpl(引用点) | 对外 API 影响评估 |
| **逻辑重构** | ServiceImpl · 单元测试 | 行为一致性验证 |
| **新增缓存** | ServiceImpl(@Cacheable) · CacheConfig | 缓存穿透/击穿防范 |
| **新增定时任务** | Job类 · JobConfig(Trigger+JobDetail) | Quartz 分布式防重 |
| **新增外部调用** | {Entity}Client · {Entity}DTO · ServiceImpl | 超时/重试/降级策略 |
| **批量操作改造** | Mapper(insertBatch/updateBatchById) · ServiceImpl | 分批大小(500)评估 |
| **性能优化** | Mapper/SQL · EXPLAIN验证 · 缓存策略 | 索引变更评估回归 |
| **配置变更** | application.yaml · application-{profile}.yaml | 所有 profile 同步 |

### 3.2 快速判断规则

```
新增字段 → DO + VO + Mapper.xml(columns片段) + 唯一性校验评估
新增接口 → Controller + Service + ErrorCode + 权限注解
性能优化 → Mapper/SQL + EXPLAIN验证 + 索引评估
缓存变更 → ServiceImpl缓存注解 + CacheConfig + 穿透防范
定时任务 → Job类 + JobConfig(Trigger+JobDetail)
外部调用 → Client类 + DTO + 超时/重试策略
```

---

## 四、字段类型规范

| 场景 | 类型 | 说明 |
|------|------|------|
| 主键 | `bigint` | 自增 |
| 金额 | `decimal(19,4)` | 禁止 float/double |
| 状态/类型 | `tinyint` | 配合枚举 |
| 名称/标题 | `varchar(64-255)` | 按业务需要 |
| 描述/内容 | `varchar(500-2000)` 或 `text` | 长文本 |
| 时间 | `datetime` | 不用 timestamp |
| JSON | `json` | MySQL 5.7+ |