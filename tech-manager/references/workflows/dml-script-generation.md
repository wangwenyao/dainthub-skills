# 数据库脚本生成流程

**何时使用**: 变更影响分析完成后，生成 DML 脚本（CREATE/ALTER/INSERT），供后端开发直接执行。

---

## 输入来源

从 product-manager 输出物提取：

| 输入 | 来源 | 提取内容 |
|------|------|---------|
| **ER图** | PRD 业务实体模型 | 表名、字段名、字段类型、主键、外键 |
| **实体属性定义** | PRD 实体属性表 | 字段中文名、英文名、类型、必填、说明 |
| **字段约束** | PRD 功能详细描述 | 字段长度、默认值、唯一性 |
| **业务规则** | PRD BR编号 | 约束条件、索引需求 |
| **非功能需求** | PRD 性能要求 | 查询性能 → 索引设计 |

---

## 输出格式

MySQL 8 兼容的 DML 脚本（.sql 文件）。

---

## 流程步骤

```
1. 提取表结构
   ├── 从 ER图 识别实体 → 表名
   ├── 从实体属性提取字段定义
   └── 确定主键、外键、索引

2. 设计字段属性
   ├── 从字段约束确定类型、长度、默认值
   ├── 从必填标记确定 NOT NULL
   └── 从唯一性约束确定 UNIQUE

3. 设计索引
   ├── 主键索引（PRIMARY KEY）
   ├── 外键索引（INDEX on FK）
   ├── 查询索引（根据业务规则）
   └── 唯一索引（根据唯一性约束）

4. 生成 DML 脚本
   ├── 新增表 → CREATE TABLE
   ├── 修改表 → ALTER TABLE
   └── 初始数据 → INSERT
```

---

## 表命名规范

| 规范 | 说明 | 示例 |
|------|------|------|
| 表名 | 小写+下划线，模块前缀 | `product`、`order_item` |
| 主键 | `id`，BIGINT AUTO_INCREMENT | `id BIGINT PRIMARY KEY AUTO_INCREMENT` |
| 外键 | `{表名}_id` | `category_id BIGINT` |
| 时间字段 | `{动词}_at` | `created_at`、`updated_at`、`deleted_at` |
| 状态字段 | `status` | `status TINYINT` |
| 审计字段 | 标准四字段 | `created_by`、`updated_by`、`created_at`、`updated_at` |

---

## CREATE TABLE 模板

### 标准表模板

```sql
-- ============================================
-- 表名: product
-- 用途: 商品实体（对应 PRD ER图 E001）
-- 版本: v1.0
-- 创建时间: 2026-04-15
-- ============================================

CREATE TABLE `product` (
  -- 主键
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '商品ID',
  
  -- 业务字段（从 ER图 映射）
  `name` VARCHAR(50) NOT NULL COMMENT '商品名称',
  `category_id` BIGINT NOT NULL COMMENT '分类ID',
  `price` DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT '价格',
  `stock` INT NOT NULL DEFAULT 0 COMMENT '库存',
  `status` TINYINT NOT NULL DEFAULT 0 COMMENT '状态（0草稿/1上架/2下架）',
  `images` JSON COMMENT '商品图片URL列表',
  `remark` VARCHAR(500) COMMENT '备注',
  
  -- 审计字段
  `created_by` BIGINT COMMENT '创建人',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_by` BIGINT COMMENT '更新人',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  
  -- 主键
  PRIMARY KEY (`id`),
  
  -- 外键索引
  INDEX `idx_category_id` (`category_id`),
  
  -- 业务索引（根据业务规则）
  INDEX `idx_status` (`status`),
  INDEX `idx_created_at` (`created_at`),
  
  -- 唯一索引（根据唯一性约束 BR01）
  UNIQUE INDEX `uk_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='商品表';

-- ============================================
-- 业务规则说明
-- BR01: 名称不可重复 → UNIQUE INDEX uk_name
-- BR02: 上架状态库存必须 > 0 → 应用层校验
-- ============================================
```

### 多租户表模板

```sql
CREATE TABLE `product` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '商品ID',
  
  -- 租户字段（多租户系统必需）
  `tenant_id` BIGINT NOT NULL COMMENT '租户ID',
  
  -- 业务字段
  `name` VARCHAR(50) NOT NULL COMMENT '商品名称',
  ...
  
  PRIMARY KEY (`id`),
  
  -- 租户索引（必需，用于数据隔离）
  INDEX `idx_tenant_id` (`tenant_id`),
  
  -- 租户+唯一索引（跨租户可重复）
  UNIQUE INDEX `uk_tenant_name` (`tenant_id`, `name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品表';
```

---

## ER图 → DML 映射规则

| ER图字段 | MySQL DML | 说明 |
|---------|----------|------|
| `id PK` | `BIGINT PRIMARY KEY AUTO_INCREMENT` | 主键自增 |
| `name VARCHAR(50)` | `VARCHAR(50)` | 字符串 |
| `price DECIMAL(10,2)` | `DECIMAL(10, 2)` | 精确数值 |
| `stock INT` | `INT` | 整数 |
| `status ENUM(0,1,2)` | `TINYINT` + COMMENT | 枚举（应用层校验） |
| `remark TEXT` | `VARCHAR(500)` 或 `TEXT` | 长文本 |
| `images JSON` | `JSON` | JSON 类型（MySQL 8） |
| `created_at DATETIME` | `DATETIME DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `NOT NULL` | `NOT NULL` | 必填 |
| `DEFAULT 0` | `DEFAULT 0` | 默认值 |
| `FK → category` | `category_id BIGINT + INDEX` | 外键 |
| `UNIQUE` | `UNIQUE INDEX` | 唯一约束 |

---

## ALTER TABLE 模板

### 新增字段

```sql
-- ============================================
-- 变更: 商品表新增库存预警字段
-- PRD版本: v1.2
-- 变更时间: 2026-04-15
-- ============================================

ALTER TABLE `product` 
  ADD COLUMN `stock_warning` INT DEFAULT 0 COMMENT '库存预警值' AFTER `stock`;

-- 历史数据处理
-- 默认值 0，无需数据迁移
```

### 修改字段

```sql
-- ============================================
-- 变更: 商品名称长度扩展至 100 字符
-- PRD版本: v1.2
-- ============================================

ALTER TABLE `product` 
  MODIFY COLUMN `name` VARCHAR(100) NOT NULL COMMENT '商品名称';

-- 注意事项
-- 需检查已有数据是否超长
-- 需同步更新唯一索引长度
```

### 新增索引

```sql
-- ============================================
-- 变更: 新增库存预警查询索引
-- 业务规则: BR03 支持按预警状态筛选
-- ============================================

ALTER TABLE `product` 
  ADD INDEX `idx_stock_warning` (`stock_warning`);
```

---

## 索引设计规范

| 索引类型 | 场景 | 示例 |
|---------|------|------|
| **主键索引** | 所有表必需 | `PRIMARY KEY (id)` |
| **外键索引** | 所有外键字段 | `INDEX idx_category_id (category_id)` |
| **查询索引** | 高频筛选字段 | `INDEX idx_status (status)` |
| **排序索引** | 高频排序字段 | `INDEX idx_created_at (created_at)` |
| **唯一索引** | 业务唯一约束 | `UNIQUE INDEX uk_name (name)` |
| **组合索引** | 多条件查询 | `INDEX idx_status_created (status, created_at)` |

### 索引命名规范

```
普通索引: idx_{字段名}
唯一索引: uk_{字段名}
组合索引: idx_{字段1}_{字段2}
```

---

## 初始数据模板

### 字典数据

```sql
-- ============================================
-- 商品状态字典
-- ============================================

INSERT INTO `sys_dict` (`dict_type`, `dict_label`, `dict_value`, `sort`, `remark`) VALUES
('product_status', '草稿', '0', 1, '商品状态'),
('product_status', '上架', '1', 2, '商品状态'),
('product_status', '下架', '2', 3, '商品状态');

-- ============================================
-- 分类初始数据
-- ============================================

INSERT INTO `product_category` (`id`, `name`, `sort`, `status`) VALUES
(1, '电子产品', 1, 1),
(2, '服装配饰', 2, 1),
(3, '家居用品', 3, 1);
```

---

## 外键关系处理

### 关联表创建

```sql
-- ============================================
-- 商品分类表（product_category）
-- ============================================

CREATE TABLE `product_category` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '分类ID',
  `name` VARCHAR(50) NOT NULL COMMENT '分类名称',
  `parent_id` BIGINT DEFAULT 0 COMMENT '父分类ID（树形结构）',
  `sort` INT DEFAULT 0 COMMENT '排序',
  `status` TINYINT NOT NULL DEFAULT 1 COMMENT '状态（1启用/0禁用）',
  
  PRIMARY KEY (`id`),
  INDEX `idx_parent_id` (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品分类表';

-- ============================================
-- 商品表外键说明
-- category_id 关联 product_category.id
-- 不使用 FOREIGN KEY CONSTRAINT（建议应用层控制）
-- ============================================
```

---

## 历史数据处理模板

### 新增字段默认值

```sql
-- ============================================
-- 历史数据处理: stock_warning 默认值
-- ============================================

-- 方案1: 默认值（推荐）
ALTER TABLE `product` 
  ADD COLUMN `stock_warning` INT DEFAULT 0 COMMENT '库存预警值';

-- 无需额外处理，历史数据自动填充默认值 0

-- ============================================
-- 方案2: 根据现有数据计算（如需要）
-- ============================================

ALTER TABLE `product` 
  ADD COLUMN `stock_warning` INT COMMENT '库存预警值';

-- 更新历史数据
UPDATE `product` 
  SET `stock_warning` = FLOOR(`stock` * 0.1)  -- 库存的 10% 作为预警值
  WHERE `stock_warning` IS NULL;
```

### 状态值迁移

```sql
-- ============================================
-- 状态枚举变更: 旧状态映射到新状态
-- ============================================

-- 旧状态: 0=禁用, 1=启用
-- 新状态: 0=草稿, 1=上架, 2=下架

UPDATE `product` 
  SET `status` = CASE 
    WHEN `status` = 0 THEN 0  -- 禁用 → 草稿
    WHEN `status` = 1 THEN 1  -- 启用 → 上架
  END;
```

---

## 输出文件命名

```
dml-[模块名]-v[版本].sql

示例：
dml-product-v1.0.sql        -- 新增模块
dml-product-v1.2.sql        -- 版本更新
dml-product-category-v1.0.sql
```

---

## 输出检查清单

```
☐ 表名符合命名规范（小写+下划线）
☐ 主键为 id BIGINT AUTO_INCREMENT
☐ 外键字段命名为 {表名}_id
☐ 所有字段有 COMMENT 说明
☐ 审计字段完整（created_by/at, updated_by/at）
☐ 外键字段有索引
☐ 高频查询字段有索引
☐ 唯一约束有 UNIQUE INDEX
☐ 字段类型与 ER图 一致
☐ 必填字段有 NOT NULL
☐ 默认值已设置
☐ 历史数据处理方案明确
```

---

## 变更日志机制

### 变更日志表

创建数据库变更日志表，记录每次执行的 SQL：

```sql
-- ============================================
-- 数据库变更日志表
-- ============================================

CREATE TABLE `db_change_log` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `change_id` VARCHAR(50) NOT NULL COMMENT '变更编号（如 P001-v1.2-field-add）',
  `module` VARCHAR(50) NOT NULL COMMENT '模块名',
  `table_name` VARCHAR(100) NOT NULL COMMENT '表名',
  `change_type` VARCHAR(20) NOT NULL COMMENT '变更类型（CREATE/ALTER_FIELD/ALTER_INDEX/DATA_MIGRATION）',
  `sql_content` TEXT NOT NULL COMMENT '执行的 SQL',
  `rollback_sql` TEXT COMMENT '回滚 SQL',
  `prerequisite` VARCHAR(200) COMMENT '前置依赖（变更ID）',
  `status` TINYINT NOT NULL DEFAULT 0 COMMENT '状态（0待执行/1已执行/2已回滚/3执行失败）',
  `executed_by` BIGINT COMMENT '执行人',
  `executed_at` DATETIME COMMENT '执行时间',
  `remark` VARCHAR(500) COMMENT '备注',
  
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uk_change_id` (`change_id`),
  INDEX `idx_table_name` (`table_name`),
  INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='数据库变更日志';
```

### 变更记录模板

每次 ALTER 执行后，记录变更日志：

```sql
-- ============================================
-- 记录变更日志
-- ============================================

INSERT INTO `db_change_log` (
  `change_id`, `module`, `table_name`, `change_type`, 
  `sql_content`, `rollback_sql`, `status`, `executed_by`, `executed_at`
) VALUES (
  'P001-v1.2-stock_warning-add',  -- 变更编号
  'product',                       -- 模块名
  'product',                       -- 表名
  'ALTER_FIELD',                   -- 变更类型
  'ALTER TABLE `product` ADD COLUMN `stock_warning` INT DEFAULT 0 COMMENT ''库存预警值'' AFTER `stock`;',  -- 执行 SQL
  'ALTER TABLE `product` DROP COLUMN `stock_warning`;',  -- 回滚 SQL
  1,                               -- 已执行
  1,                               -- 执行人ID
  NOW()                            -- 执行时间
);
```

---

## 回滚脚本生成

### 回滚 SQL 规则

| 变更类型 | 回滚 SQL | 示例 |
|---------|---------|------|
| **新增字段** | DROP COLUMN | `ALTER TABLE product DROP COLUMN stock_warning;` |
| **修改字段** | MODIFY 回原定义 | `ALTER TABLE product MODIFY COLUMN name VARCHAR(50);` |
| **新增索引** | DROP INDEX | `ALTER TABLE product DROP INDEX idx_stock_warning;` |
| **新增表** | DROP TABLE | `DROP TABLE IF EXISTS product;` |
| **删除字段** | 无（需备份恢复） | — |
| **数据迁移** | 备份恢复 | 从备份表恢复 |

### 回滚脚本文件

每个 DML 脚本配套生成回滚脚本：

```
dml-product-v1.2.sql          -- 正向执行脚本
dml-product-v1.2-rollback.sql -- 回滚脚本
```

**回滚脚本模板**：

```sql
-- ============================================
-- 回滚脚本: dml-product-v1.2-rollback.sql
-- 版本: v1.2 → v1.1
-- 说明: 回滚商品表新增库存预警字段
-- ============================================

-- 检查前置条件
-- 确保字段存在才能回滚
SELECT COUNT(*) FROM information_schema.COLUMNS 
  WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'product' 
  AND COLUMN_NAME = 'stock_warning';

-- 回滚变更 #1: 删除库存预警字段
ALTER TABLE `product` DROP COLUMN `stock_warning`;

-- 记录回滚日志
INSERT INTO `db_change_log` (
  `change_id`, `module`, `table_name`, `change_type`, 
  `sql_content`, `rollback_sql`, `status`, `remark`
) VALUES (
  'P001-v1.2-stock_warning-add',
  'product',
  'product',
  'ALTER_FIELD',
  'ROLLBACK: ALTER TABLE product DROP COLUMN stock_warning',
  NULL,
  2,  -- 已回滚
  '回滚 v1.2 变更'
);

-- ============================================
-- 回滚完成检查
-- ============================================

SELECT COUNT(*) FROM information_schema.COLUMNS 
  WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'product' 
  AND COLUMN_NAME = 'stock_warning';  -- 应返回 0
```

---

## 执行清单模板

### DML 执行清单

生成 DBA 执行清单，包含执行顺序、依赖关系、检查项：

```markdown
## DML 执行清单

**模块**: 商品管理
**版本**: v1.2
**生成时间**: 2026-04-15
**执行环境**: 测试环境 / 生产环境

---

### 执行顺序

| 序号 | 变更ID | 变更类型 | SQL 文件 | 前置依赖 | 预估耗时 | 检查项 |
|------|--------|---------|---------|---------|---------|--------|
| 1 | P001-v1.2-table-create | 新增表 | dml-product-v1.2.sql#L1-30 | 无 | 1s | 表不存在 |
| 2 | P001-v1.2-field-add | 新增字段 | dml-product-v1.2.sql#L31-40 | #1 | 2s | 表存在、字段不存在 |
| 3 | P001-v1.2-index-add | 新增索引 | dml-product-v1.2.sql#L41-45 | #2 | 5s | 字段存在、索引不存在 |
| 4 | P001-v1.2-data-init | 数据初始化 | dml-product-v1.2.sql#L46-50 | #3 | 3s | 表有数据 |

---

### 执行检查清单

#### 执行前检查

```
□ 确认执行环境（测试/生产）
□ 备份相关表数据（生产环境必须）
□ 检查表是否存在
□ 检查字段是否已存在（避免重复执行）
□ 检查索引是否已存在
□ 确认执行人权限
□ 通知相关人员
```

#### 执行中检查

```
□ 每条 SQL 执行后检查返回结果
□ 记录执行时间
□ 检查是否有 ERROR
□ 检查是否有 WARNING
```

#### 执行后验证

```
□ 验证表结构变更成功
□ 验证字段已添加
□ 验证索引已创建
□ 验证初始数据已插入
□ 验证业务功能正常
□ 记录变更日志
```

---

### 回滚方案

若执行失败，按以下顺序回滚：

| 序号 | 回滚SQL | 文件 |
|------|---------|------|
| 3 | DROP INDEX | dml-product-v1.2-rollback.sql#L20 |
| 2 | DROP COLUMN | dml-product-v1.2-rollback.sql#L15 |
| 1 | DROP TABLE | dml-product-v1.2-rollback.sql#L10 |

**注意**: 回滚需按逆序执行
```

---

## DML 文件组织规范

### 文件命名规范

```
dml-{模块名}-v{版本}.sql           -- 正向脚本
dml-{模块名}-v{版本}-rollback.sql  -- 回滚脚本
dml-{模块名}-checklist-v{版本}.md  -- 执行清单
```

### 文件结构规范

```sql
-- ============================================
-- 文件头部信息
-- ============================================
-- 模块名: {module}
-- 版本: {version}
-- 功能ID: {功能ID列表}
-- PRD版本: {PRD版本}
-- 生成时间: YYYY-MM-DD
-- 执行环境: 测试/生产
-- ============================================

-- ============================================
-- 变更清单
-- ============================================
-- #1: 新增表 {table_name}
-- #2: 新增字段 {field_name}
-- #3: 新增索引 {index_name}
-- #4: 数据迁移
-- ============================================

-- ============================================
-- 变更 #1: 新增表
-- ============================================
-- 变更ID: {change_id}
-- 前置依赖: 无
-- 回滚SQL: DROP TABLE IF EXISTS {table_name};
-- ============================================

CREATE TABLE ...;

-- ============================================
-- 变更 #1 检查点
-- ============================================
SELECT COUNT(*) FROM information_schema.TABLES 
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = '{table_name}';
-- 预期结果: 1

-- ============================================
-- 变更 #2: 新增字段
-- ============================================
...

-- ============================================
-- 执行完成
-- ============================================
-- 记录变更日志
INSERT INTO db_change_log ...
```

---

## 执行脚本模板（含检查点）

```sql
-- ============================================
-- DML 执行脚本（含自动检查）
-- 模块: product
-- 版本: v1.2
-- ============================================

-- 开启事务（可选，生产环境建议单条执行）
-- START TRANSACTION;

-- ============================================
-- 变更 #1: 新增库存预警字段
-- 变更ID: P001-v1.2-stock_warning-add
-- 前置检查: 字段不存在
-- ============================================

-- 前置检查
SELECT '前置检查: stock_warning 字段应不存在' AS step;
SELECT IF(COUNT(*) = 0, 'PASS', 'FAIL: 字段已存在') AS result
  FROM information_schema.COLUMNS 
  WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'product' 
  AND COLUMN_NAME = 'stock_warning';

-- 执行变更
ALTER TABLE `product` 
  ADD COLUMN `stock_warning` INT DEFAULT 0 COMMENT '库存预警值' AFTER `stock`;

-- 后置检查
SELECT '后置检查: stock_warning 字段应存在' AS step;
SELECT IF(COUNT(*) = 1, 'PASS', 'FAIL: 字段未添加') AS result
  FROM information_schema.COLUMNS 
  WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'product' 
  AND COLUMN_NAME = 'stock_warning';

-- 记录变更日志
INSERT INTO `db_change_log` (
  `change_id`, `module`, `table_name`, `change_type`, 
  `sql_content`, `rollback_sql`, `status`, `executed_at`
) VALUES (
  'P001-v1.2-stock_warning-add',
  'product',
  'product',
  'ALTER_FIELD',
  'ALTER TABLE `product` ADD COLUMN `stock_warning` INT DEFAULT 0 COMMENT ''库存预警值'' AFTER `stock`;',
  'ALTER TABLE `product` DROP COLUMN `stock_warning`;',
  1,
  NOW()
);

-- ============================================
-- 变更 #2: 新增索引
-- ============================================

...

-- 提交事务
-- COMMIT;

-- ============================================
-- 执行完成汇总
-- ============================================
SELECT 
  CONCAT('执行完成: ', COUNT(*), ' 条变更已执行') AS summary
FROM `db_change_log` 
WHERE `change_id` LIKE 'P001-v1.2-%' AND `status` = 1;
```

