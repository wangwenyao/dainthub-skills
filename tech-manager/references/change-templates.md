# 变更通知模板

变更影响分析和通知的标准模板。

---

## 一、影响分析报告

```markdown
## 变更影响分析报告

**变更来源**: [PRD更新 / 接口调整 / 需求变更]
**变更时间**: YYYY-MM-DD
**分析人**: 技术经理

---

### 变更概述

**变更内容**:
[一句话描述变更]

**变更原因**:
[为什么需要变更]

---

### 影响范围

#### 后端影响

| 影响项 | 改动类型 | 改动说明 | 优先级 |
|--------|---------|---------|--------|
| [服务/接口名] | 新增/修改/删除 | [具体改动] | P0/P1 |

#### 数据库影响

| 表名 | 变更类型 | 变更说明 | 数据迁移 |
|------|---------|---------|---------|
| [表名] | 新增字段/修改字段 | [具体变更] | 是/否 |

#### 前端影响

| 影响项 | 改动类型 | 改动说明 | 优先级 |
|--------|---------|---------|--------|
| [页面/组件名] | 新增/修改 | [具体改动] | P0/P1 |

---

### 风险评估

| 风险项 | 风险等级 | 说明 | 缓解措施 |
|--------|---------|------|---------|
| [风险描述] | 高/中/低 | [详细说明] | [应对方案] |

---

### 同步建议

**需要通知**:
- [ ] 后端开发: [具体任务]
- [ ] 前端开发: [具体任务]
- [ ] 测试: [测试范围]
- [ ] 产品: [确认事项]

**建议优先级**:
1. [优先处理项]
2. [次优先项]

---

### 时间预估

| 任务 | 预估工时 | 负责方 |
|------|---------|--------|
| [任务描述] | X人天 | 后端/前端 |
```

---

## 二、变更通知

### 接口变更通知（后端→前端）

```markdown
## 接口变更通知

**变更接口**: [接口路径]
**变更类型**: 新增/修改/删除
**变更时间**: YYYY-MM-DD
**向后兼容**: 是/否

---

### 变更详情

#### 请求参数变更

| 操作 | 字段名 | 类型 | 必填 | 说明 |
|------|--------|------|------|------|
| 新增/修改/删除 | [字段名] | [类型] | 是/否 | [说明] |

#### 返回值变更

| 操作 | 字段名 | 类型 | 说明 |
|------|--------|------|------|
| 新增/修改/删除 | [字段名] | [类型] | [说明] |

---

### 前端影响页面

- [页面1]: [影响说明]
- [页面2]: [影响说明]

---

### 联调安排

**联调时间**: YYYY-MM-DD
**联调负责人**: [姓名]
**联调环境**: [测试环境地址]

---

### 请前端确认

- [ ] 已了解变更内容
- [ ] 预计完成时间: ______
- [ ] 是否有疑问: ______
```

### 功能调整通知（前端→后端）

```markdown
## 功能调整需求

**需求来源**: [PRD / 产品反馈 / 用户反馈]
**期望完成时间**: YYYY-MM-DD

---

### 调整内容

**功能描述**:
[功能名称和描述]

**调整原因**:
[为什么需要调整]

---

### 接口需求

**接口路径**: [期望的接口路径]
**请求方式**: GET/POST/PUT/DELETE

#### 请求参数

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| [字段名] | [类型] | 是/否 | [说明] |

#### 期望返回

| 字段名 | 类型 | 说明 |
|--------|------|------|
| [字段名] | [类型] | [说明] |

---

### 使用场景

[描述前端如何使用这个接口]

---

### 请后端确认

- [ ] 是否可实现: 是/否
- [ ] 预计完成时间: ______
- [ ] 技术风险: ______
- [ ] 替代方案: ______
```

---

## 三、接口对齐报告

```markdown
## 接口对齐报告

**接口路径**: [接口路径]
**对齐时间**: YYYY-MM-DD
**参与方**: 后端开发 / 前端开发

---

### 基本信息

| 项目 | 后端 | 前端 | 状态 |
|------|------|------|------|
| 接口路径 | [路径] | [路径] | ✅/❌ |
| 请求方式 | [方法] | [方法] | ✅/❌ |

---

### 请求参数对齐

| 字段名 | 后端类型 | 前端类型 | 必填 | 状态 |
|--------|---------|---------|------|------|
| [字段名] | [类型] | [类型] | 是/否 | ✅/❌ |

---

### 返回值对齐

| 字段名 | 后端类型 | 前端类型 | 状态 |
|--------|---------|---------|------|
| [字段名] | [类型] | [类型] | ✅/❌ |

---

### 对齐结论

- ✅ 接口已对齐，可并行开发
- ❌ 存在差异，需进一步沟通

### 待确认项

- [ ] [待确认内容]
```

---

## 四、验证报告

```markdown
## 实现验证报告

**PRD版本**: [版本号]
**验证时间**: YYYY-MM-DD
**验证范围**: [功能模块]

---

### 验证结果

| 维度 | 通过项 | 不通过项 | 通过率 |
|------|--------|---------|--------|
| 功能完整性 | X/Y | Z | N% |
| 接口一致性 | X/Y | Z | N% |
| 字段完整性 | X/Y | Z | N% |
| 业务规则 | X/Y | Z | N% |

---

### 问题清单

| # | 类型 | 描述 | 影响 | 负责人 | 状态 |
|---|------|------|------|--------|------|
| 1 | [类型] | [描述] | [影响] | [姓名] | 待处理 |

---

### 验证结论

- ✅ 通过验证，可进入测试
- ⚠️ 部分通过，需解决问题后进入测试
- ❌ 未通过验证，需重新开发

---

### 后续行动

| 行动项 | 负责人 | 截止时间 |
|--------|--------|----------|
| [行动内容] | [姓名] | YYYY-MM-DD |
```

---

## 五、任务分发块

### 后端任务块

```markdown
【变更任务】[任务名称]

**变更类型**: 新增功能/逻辑调整/字段变更/接口变更
**优先级**: P0/P1/P2

**改动内容**:
1. [具体改动描述]
2. [具体改动描述]

**涉及文件**:
- src/main/java/.../service/[ServiceName].java
- src/main/java/.../controller/[ControllerName].java
- src/main/java/.../entity/[EntityName].java

**接口变化**:
| 接口 | 变化类型 | 说明 |
|------|---------|------|
| GET /api/xxx | 新增/修改 | 说明 |

**数据库变化**:
| 表名 | 变化类型 | 说明 |
|------|---------|------|
| table_name | 新增字段/修改字段 | 说明 |

**注意事项**:
- [历史数据处理方式]
- [兼容性考虑]
- [性能关注点]
```

### 前端任务块

```markdown
【变更任务】[任务名称]

**变更类型**: 新增页面/页面修改/组件调整
**优先级**: P0/P1/P2

**改动内容**:
1. [具体改动描述]
2. [具体改动描述]

**涉及页面**:
- src/views/[module]/[page].vue
- src/components/[ComponentName].vue

**接口变化**:
| 接口 | 变化类型 | 说明 |
|------|---------|------|
| GET /api/xxx | 新增调用/参数变化 | 说明 |

**注意事项**:
- [交互细节]
- [状态管理]
- [边界场景]
```

---

## 六、实现偏差反馈

### 偏差反馈报告

```markdown
## 实现偏差反馈报告

**PRD版本**: [版本号]
**反馈时间**: YYYY-MM-DD
**反馈来源**: [实现验证 / 开发上报]

---

### 偏差总览

| # | 偏差描述 | 分类 | 严重等级 | PRD章节 |
|---|---------|------|---------|---------|
| 1 | [偏差简述] | 技术限制/逻辑缺陷/优化建议/约束新增 | P0/P1/P2/P3 | [章节号] |

---

### 偏差详情

#### 偏差 #1: [偏差标题]

**分类**: 技术限制型 / 逻辑缺陷型 / 优化建议型 / 约束新增型
**严重等级**: P0-阻塞 / P1-重要 / P2-一般 / P3-建议

**PRD要求**:
[PRD中的原始描述]

**实际实现/发现**:
[开发中的实际情况]

**偏差原因**:
[为什么产生偏差]

**影响评估**:
- 用户体验影响: 高/中/低/无
- 功能完整性影响: [说明]
- 后续迭代影响: [说明]

**建议方案**:
- 方案A: [描述]（推荐 ✅）
- 方案B: [描述]

---

### 请产品经理确认

| # | 偏差 | 建议方案 | 产品决策 | 备注 |
|---|------|---------|---------|------|
| 1 | [偏差简述] | [建议] | □ 接受偏差 □ 坚持PRD □ 协商调整 | |

**确认后行动**:
- [ ] PRD 更新对应章节
- [ ] 开发者已知悉最终方案
- [ ] 测试用例已同步调整
```

### 偏差决策通知（产品确认后）

```markdown
## 偏差决策通知

**决策时间**: YYYY-MM-DD
**决策人**: [产品经理姓名]

### 决策结果

| # | 偏差 | 决策 | 影响 |
|---|------|------|------|
| 1 | [偏差简述] | 接受/坚持PRD/协商调整 | [对开发的影响] |

### 需要开发者执行

- [ ] [具体行动项]

### PRD更新记录

| 章节 | 更新内容 | 更新原因 |
|------|---------|---------|
| [章节号] | [修改内容] | 偏差#[编号]决策 |
```

---

## 七、完整变更报告（含任务分发）

```markdown
## 变更影响分析报告

**变更来源**: [PRD更新 / 接口调整 / 需求变更]
**变更时间**: YYYY-MM-DD

### 变更概述
[变更内容描述]

### 影响范围

#### 后端影响
| 影响项 | 改动类型 | 改动说明 |
|--------|---------|---------|
| [服务/接口] | 新增/修改 | [说明] |

#### 前端影响
| 影响项 | 改动类型 | 改动说明 |
|--------|---------|---------|
| [页面/组件] | 新增/修改 | [说明] |

### 风险评估
| 风险项 | 风险等级 | 缓解措施 |
|--------|---------|---------|
| [风险] | 高/中/低 | [措施] |

---

## 📋 任务分发

### 后端任务

【变更任务】[后端任务名称]

**变更类型**: [类型]
**优先级**: P0

**改动内容**:
1. [改动项]
2. [改动项]

**涉及文件**:
- [文件路径]

**接口变化**:
- [接口]: [变化]

**注意事项**:
- [注意点]

---

### 前端任务

【变更任务】[前端任务名称]

**变更类型**: [类型]
**优先级**: P0

**改动内容**:
1. [改动项]
2. [改动项]

**涉及页面**:
- [页面路径]

**接口变化**:
- [接口]: [变化]

**注意事项**:
- [注意点]
```

---

## 八、OpenAPI 接口规格

### 接口规格文档模板

```yaml
openapi: 3.0.3
info:
  title: [模块名] API
  version: 1.0.0
  description: |-
    功能模块: [模块名]
    PRD版本: [版本号]
    生成时间: YYYY-MM-DD

servers:
  - url: /api
    description: API 服务

tags:
  - name: [模块名]
    description: [模块用途]

paths:
  /{module}/page:
    get:
      tags:
        - [模块名]
      summary: [功能名称]列表分页查询
      description: |-
        功能ID: [功能ID]
        
        业务规则:
        - [BR编号]: [规则描述]
      operationId: [getModulePage]
      parameters:
        - name: pageNo
          in: query
          required: true
          schema:
            type: integer
            minimum: 1
            default: 1
        - name: pageSize
          in: query
          required: true
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
      responses:
        '200':
          content:
            application/json:
              schema:
                type: object
                required: [list, total]
                properties:
                  list:
                    type: array
                    items:
                      $ref: '#/components/schemas/[Entity]'
                  total:
                    type: integer

components:
  schemas:
    [Entity]:
      type: object
      properties:
        id:
          type: integer
          description: [实体ID]
        name:
          type: string
          maxLength: [长度]
          description: [字段描述]
        status:
          type: integer
          enum: [0, 1, 2]
          x-enum-labels:
            0: [状态1]
            1: [状态2]
            2: [状态3]
```

### 接口清单表格

```markdown
## 接口清单

| 接口路径 | 方法 | 功能ID | 用途 | 前端调用 |
|---------|------|--------|------|---------|
| GET /api/{module}/page | GET | F0101 | 分页查询 | 列表页 |
| GET /api/{module}/{id} | GET | F0102 | 详情查询 | 详情页 |
| POST /api/{module}/create | POST | F0103 | 创建 | 表单弹窗 |
| PUT /api/{module}/update | PUT | F0104 | 更新 | 表单弹窗 |
| DELETE /api/{module}/delete | DELETE | F0105 | 删除 | 行操作 |
```

---

## 九、DML 脚本

### CREATE TABLE 模板

```sql
-- ============================================
-- 表名: {table_name}
-- 用途: {用途描述}
-- 功能ID: {功能ID}
-- PRD版本: {版本号}
-- ============================================

CREATE TABLE `{table_name}` (
  -- 主键
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  
  -- 业务字段（从 ER图 映射）
  `name` VARCHAR(50) NOT NULL COMMENT '{字段用途}',
  `status` TINYINT NOT NULL DEFAULT 0 COMMENT '状态（0{状态1}/1{状态2}/2{状态3})',
  
  -- 审计字段
  `created_by` BIGINT COMMENT '创建人',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_by` BIGINT COMMENT '更新人',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  
  -- 主键
  PRIMARY KEY (`id`),
  
  -- 业务索引
  INDEX `idx_status` (`status`),
  
  -- 唯一索引（根据业务规则）
  -- UNIQUE INDEX `uk_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='{表用途}';

-- ============================================
-- 业务规则说明
-- [BR编号]: [规则描述] → [索引/约束说明]
-- ============================================
```

### ALTER TABLE 模板

```sql
-- ============================================
-- 变更: {变更描述}
-- PRD版本: {版本号}
-- 变更时间: YYYY-MM-DD
-- ============================================

ALTER TABLE `{table_name}` 
  ADD COLUMN `{new_field}` {类型} DEFAULT {默认值} COMMENT '{用途}' AFTER `{字段位置}`;

-- 历史数据处理
-- [处理方案说明]
```

### 数据库变更清单

```markdown
## 数据库变更清单

| 表名 | 变更类型 | 变更说明 | 历史数据处理 | 执行顺序 |
|------|---------|---------|-------------|---------|
| {table_name} | 新增表 | {说明} | 无 | 1 |
| {table_name} | 新增字段 | {说明} | 默认值填充 | 2 |
| {table_name} | 修改字段 | {说明} | 需检查超长 | 3 |
| {table_name} | 新增索引 | {说明} | 无 | 4 |
```

---

## 十、完整技术输出（含接口规格+DML）

```markdown
## 技术输出物清单

### 1. 影响分析报告
见上方"变更影响分析报告"模板

### 2. OpenAPI 接口规格
- 文件: openapi-{模块名}-v{版本}.yaml
- 用途: 前后端接口定义一致

### 3. DML 脚本
- 文件: dml-{模块名}-v{版本}.sql
- 用途: 后端数据库变更

### 4. 任务块
- 后端任务块（包含 DML 文件引用）
- 前端任务块（包含 OpenAPI 文件引用）

### 5. 接口对齐报告
- 基于 OpenAPI 文档进行对齐确认
```

---

## 十一、变更日志

### 变更日志表（db_change_log）

```sql
CREATE TABLE `db_change_log` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `change_id` VARCHAR(50) NOT NULL COMMENT '变更编号',
  `module` VARCHAR(50) NOT NULL COMMENT '模块名',
  `table_name` VARCHAR(100) NOT NULL COMMENT '表名',
  `change_type` VARCHAR(20) NOT NULL COMMENT '变更类型',
  `sql_content` TEXT NOT NULL COMMENT '执行的 SQL',
  `rollback_sql` TEXT COMMENT '回滚 SQL',
  `prerequisite` VARCHAR(200) COMMENT '前置依赖',
  `status` TINYINT NOT NULL DEFAULT 0 COMMENT '状态',
  `executed_by` BIGINT COMMENT '执行人',
  `executed_at` DATETIME COMMENT '执行时间',
  `remark` VARCHAR(500) COMMENT '备注',
  
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uk_change_id` (`change_id`),
  INDEX `idx_table_name` (`table_name`),
  INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='数据库变更日志';
```

### 变更日志记录

```sql
INSERT INTO `db_change_log` (
  `change_id`, `module`, `table_name`, `change_type`, 
  `sql_content`, `rollback_sql`, `status`, `executed_at`
) VALUES (
  '{变更编号}',
  '{模块名}',
  '{表名}',
  '{变更类型}',
  '{执行SQL}',
  '{回滚SQL}',
  1,  -- 已执行
  NOW()
);
```

---

## 十二、回滚脚本

### 回滚脚本模板

```sql
-- ============================================
-- 回滚脚本: dml-{模块}-v{版本}-rollback.sql
-- 版本: v{新版本} → v{旧版本}
-- ============================================

-- 回滚变更 #N
ALTER TABLE `{table_name}` DROP COLUMN `{field_name}`;

-- 记录回滚日志
INSERT INTO `db_change_log` (
  `change_id`, `module`, `table_name`, `change_type`, 
  `sql_content`, `rollback_sql`, `status`, `remark`
) VALUES (
  '{变更编号}',
  '{模块}',
  '{表名}',
  '{变更类型}',
  'ROLLBACK: {回滚SQL}',
  NULL,
  2,  -- 已回滚
  '回滚 v{版本} 变更'
);
```

### 回滚 SQL 规则表

| 变更类型 | 回滚 SQL |
|---------|---------|
| 新增字段 | `ALTER TABLE {table} DROP COLUMN {field};` |
| 修改字段 | `ALTER TABLE {table} MODIFY COLUMN {field} {原定义};` |
| 新增索引 | `ALTER TABLE {table} DROP INDEX {index};` |
| 新增表 | `DROP TABLE IF EXISTS {table};` |

---

## 十三、DML 执行清单

```markdown
## DML 执行清单

**模块**: {模块名}
**版本**: v{版本}
**生成时间**: YYYY-MM-DD
**执行环境**: 测试环境 / 生产环境

---

### 执行顺序

| 序号 | 变更ID | 变更类型 | SQL位置 | 前置依赖 | 检查项 |
|------|--------|---------|---------|---------|--------|
| 1 | {id} | 新增表 | L1-30 | 无 | 表不存在 |
| 2 | {id} | 新增字段 | L31-40 | #1 | 字段不存在 |
| 3 | {id} | 新增索引 | L41-45 | #2 | 索引不存在 |

---

### 执行检查清单

**执行前**:
- [ ] 确认执行环境
- [ ] 备份相关表数据（生产必须）
- [ ] 检查表/字段/索引状态
- [ ] 确认执行人权限

**执行后**:
- [ ] 验证变更成功
- [ ] 验证业务功能正常
- [ ] 记录变更日志

---

### 回滚方案

按逆序执行回滚脚本: `dml-{模块}-v{版本}-rollback.sql`
```

---

## 十四、DML 执行脚本（含检查点）

```sql
-- ============================================
-- DML 执行脚本（含自动检查）
-- 模块: {module}
-- 版本: v{version}
-- ============================================

-- ============================================
-- 变更 #1: {变更描述}
-- 变更ID: {change_id}
-- ============================================

-- 前置检查
SELECT IF(COUNT(*) = 0, 'PASS', 'FAIL: 已存在') AS result
  FROM information_schema.COLUMNS 
  WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = '{table}' 
  AND COLUMN_NAME = '{field}';

-- 执行变更
ALTER TABLE `{table}` ADD COLUMN `{field}` {定义};

-- 后置检查
SELECT IF(COUNT(*) = 1, 'PASS', 'FAIL: 未添加') AS result
  FROM information_schema.COLUMNS 
  WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = '{table}' 
  AND COLUMN_NAME = '{field}';

-- 记录变更日志
INSERT INTO `db_change_log` (
  `change_id`, `module`, `table_name`, `change_type`, 
  `sql_content`, `rollback_sql`, `status`, `executed_at`
) VALUES (
  '{change_id}', '{module}', '{table}', 'ALTER_FIELD',
  '{执行SQL}', '{回滚SQL}', 1, NOW()
);

-- ============================================
-- 执行完成汇总
-- ============================================
SELECT COUNT(*) AS executed_count
FROM `db_change_log` 
WHERE `change_id` LIKE '{module}-v{version}-%' AND `status` = 1;
```