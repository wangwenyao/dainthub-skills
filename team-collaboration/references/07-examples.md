# 协作场景示例

---

## 场景一：新增功能模块

**角色**：产品经理 → 技术经理 → 前端开发 + 后端开发

```
Step 1: 产品经理 → 输出 PRD
  - 生成：docs/prd/prd-product-v1.0.md
  - 生成：docs/prd/prd-product-v1.0-er.md
  - 生成：docs/wireframes/wireframes-product-v1.0.yaml
  - 更新：docs/status.md（新增模块行）
  - 提交：git add docs/prd/ docs/wireframes/ docs/status.md

Step 2: 技术经理 → 拉取 → 分析 → 输出技术规格
  - 拉取：git pull
  - 读取：docs/status.md → 查看"下一步任务"
  - 读取：docs/prd/prd-product-v1.0.md + docs/prd/prd-product-v1.0-er.md
  - 生成：docs/api/openapi-product-v1.0.yaml
  - 生成：docs/db/dml-product-v1.0.sql
  - 生成：docs/reports/impact-product-v1.0.md
  - 更新：docs/status.md（更新状态）
  - 提交：git add docs/api/ docs/db/ docs/reports/ docs/status.md

Step 3: 前端开发 + 后端开发 → 拉取 → 并行开发
  - 拉取：git pull
  - 读取：docs/status.md → 查看"下一步任务"
  
  【后端开发】
  - 执行：docs/db/dml-product-v1.0.sql
  - 读取：docs/api/openapi-product-v1.0.yaml
  - 开发：backend/src/main/java/.../module/product/
  
  【前端开发】
  - 读取：docs/api/openapi-product-v1.0.yaml
  - 读取：docs/wireframes/wireframes-product-v1.0.yaml
  - 开发：frontend/apps/web-antd/src/views/product/
  
  - 更新：docs/status.md（开发完成）
  - 提交：git add backend/ frontend/ docs/status.md

Step 4: 技术经理 → 拉取 → 验证
  - 拉取：git pull
  - 读取：docs/status.md → 查看"下一步任务"
  - 读取：docs/prd/ + backend/ + frontend/
  - 验证：实现验证
  - 生成：docs/reports/verify-product-v1.0.md
  - 更新：docs/status.md（验证状态）
  
  【验证通过】
  - 合并：git merge feature/product-v1.0
  
  【验证不通过】
  - 生成：docs/reports/deviation-product-v1.0.md
  - 更新：docs/status.md（偏差 🚧）
  - 提交：git add docs/reports/ docs/status.md

Step 5: 产品经理 → 拉取 → 决策
  - 拉取：git pull
  - 读取：docs/status.md → 查看"待处理项汇总"
  - 读取：docs/reports/deviation-product-v1.0.md
  - 决策：产品决策
  - 生成：docs/decisions/decision-product-sku-v1.0.md
  - 更新：docs/status.md（决策 ✅）
  - 提交：git add docs/decisions/ docs/status.md
```

---

## 场景二：字段变更

```
Step 1: 产品经理 → 提出字段变更需求
  - 更新：docs/prd/prd-product-v1.1.md
  - 更新：docs/status.md（PRD 🚧）

Step 2: 技术经理 → 分析影响
  - 读取：docs/prd/prd-product-v1.1.md
  - 分析：字段变更影响
  - 生成：docs/db/dml-product-v1.1.sql
  - 更新：docs/api/openapi-product-v1.1.yaml
  - 更新：docs/status.md（OpenAPI ✅ DML 🚧）

Step 3: 后端开发 + 前端开发 → 执行变更
  - 读取：docs/status.md → 查看"下一步任务"
  
  【后端开发】
  - 执行：docs/db/dml-product-v1.1.sql
  - 更新：DO · VO · Mapper.xml · Service · Controller
  
  【前端开发】
  - 更新：data.ts + api/product.ts
  
  - 更新：docs/status.md（开发 ✅）

Step 4: 技术经理 → 验证字段变更
  - 验证：字段完整性、类型一致性
  - 更新：docs/status.md（验证 ✅）
```

