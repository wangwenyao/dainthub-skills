# 接口规格生成流程

**何时使用**: 变更影响分析完成后，生成符合 OpenAPI 3.0 规范的接口文档，供前后端开发直接使用。

---

## 输入来源

从 product-manager 输出物提取：

| 输入 | 来源 | 提取内容 |
|------|------|---------|
| **功能清单** | PRD 功能架构 | 功能 → 接口用途映射 |
| **ER图 + 实体属性** | PRD 业务实体模型 | 实体字段 → 接口参数/返回值 |
| **字段约束** | PRD 功能详细描述 | 约束规则 → 参数校验 |
| **业务规则** | PRD BR编号 | 规则 → 接口描述说明 |
| **非功能需求** | PRD 性能/安全 | 响应时间限制、权限要求 |
| **YAML 页面规格** | 线框图 YAML | 前端调用的接口清单 |

---

## 输出格式

符合 OpenAPI 3.0.3 规范的 YAML/JSON 文档。

---

## 流程步骤

```
1. 提取接口清单
   ├── 从功能清单识别 CRUD 操作
   ├── 从 YAML 页面规格识别前端调用接口
   └── 确定接口路径、方法、用途

2. 定义请求参数
   ├── 从 ER图 实体属性提取字段
   ├── 从字段约束确定类型、必填、校验规则
   └── 区分路径参数、查询参数、请求体

3. 定义返回值
   ├── 从 ER图 提取返回字段
   ├── 确定分页格式（list + total）
   └── 定义错误响应格式

4. 生成 OpenAPI 文档
   └── 输出 openapi.yaml 文件
```

---

## 接口路径命名规范

### RESTful 规范

| 操作 | 方法 | 路径 | 示例 |
|------|------|------|------|
| 分页查询 | GET | `/api/{module}/page` | `/api/product/page` |
| 详情查询 | GET | `/api/{module}/{id}` | `/api/product/{id}` |
| 创建 | POST | `/api/{module}/create` | `/api/product/create` |
| 更新 | PUT | `/api/{module}/update` | `/api/product/update` |
| 删除 | DELETE | `/api/{module}/delete` | `/api/product/delete` |
| 批量删除 | DELETE | `/api/{module}/batch-delete` | `/api/product/batch-delete` |
| 导出 | GET | `/api/{module}/export` | `/api/product/export` |
| 导入 | POST | `/api/{module}/import` | `/api/product/import` |

---

## OpenAPI 文档模板

### 分页查询接口

```yaml
/api/product/page:
  get:
    tags:
      - 商品管理
    summary: 商品列表分页查询
    description: |-
      功能ID: F0101 商品列表
      
      业务规则:
      - BR01: 支持按名称模糊搜索
      - BR02: 支持按状态筛选（草稿/上架/下架）
      
      性能要求:
      - 响应时间 ≤ 500ms（P95）
      - 分页上限 100 条
    operationId: getProductPage
    parameters:
      - name: pageNo
        in: query
        description: 页码
        required: true
        schema:
          type: integer
          minimum: 1
          default: 1
      - name: pageSize
        in: query
        description: 每页条数
        required: true
        schema:
          type: integer
          minimum: 1
          maximum: 100
          default: 20
      - name: name
        in: query
        description: 商品名称（模糊搜索）
        required: false
        schema:
          type: string
          maxLength: 50
      - name: categoryId
        in: query
        description: 商品分类ID
        required: false
        schema:
          type: integer
      - name: status
        in: query
        description: 状态（0草稿/1上架/2下架）
        required: false
        schema:
          type: integer
          enum: [0, 1, 2]
      - name: createdAt
        in: query
        description: 创建时间范围
        required: false
        schema:
          type: array
          items:
            type: string
            format: date-time
          minItems: 2
          maxItems: 2
    responses:
      '200':
        description: 成功
        content:
          application/json:
            schema:
              type: object
              required: [list, total]
              properties:
                list:
                  type: array
                  items:
                    $ref: '#/components/schemas/Product'
                total:
                  type: integer
                  description: 总条数
      '400':
        $ref: '#/components/responses/BadRequest'
      '401':
        $ref: '#/components/responses/Unauthorized'
```

### 创建接口

```yaml
/api/product/create:
  post:
    tags:
      - 商品管理
    summary: 新增商品
    description: |-
      功能ID: F0102 新增商品
      
      业务规则:
      - BR01: 名称不可重复，需唯一性校验
      - BR02: 上架状态时库存必须 > 0
      
      权限要求:
      - system:product:create
    operationId: createProduct
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ProductCreateRequest'
    responses:
      '200':
        description: 成功
        content:
          application/json:
            schema:
              type: object
              properties:
                productId:
                  type: integer
                  description: 新增的商品ID
      '400':
        $ref: '#/components/responses/BadRequest'
```

### 详情查询接口

```yaml
/api/product/{id}:
  get:
    tags:
      - 商品管理
    summary: 商品详情查询
    operationId: getProduct
    parameters:
      - name: id
        in: path
        description: 商品ID
        required: true
        schema:
          type: integer
    responses:
      '200':
        description: 成功
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ProductDetail'
      '404':
        description: 商品不存在
```

---

## Schema 定义模板

### 实体 Schema（从 ER图 映射）

```yaml
components:
  schemas:
    Product:
      type: object
      properties:
        id:
          type: integer
          description: 商品ID
        name:
          type: string
          maxLength: 50
          description: 商品名称
        categoryId:
          type: integer
          description: 分类ID
        categoryName:
          type: string
          description: 分类名称（冗余字段）
        price:
          type: number
          format: decimal
          description: 价格
        stock:
          type: integer
          description: 库存
        status:
          type: integer
          enum: [0, 1, 2]
          description: 状态（0草稿/1上架/2下架）
          x-enum-labels:
            0: 草稿
            1: 上架
            2: 下架
        images:
          type: array
          items:
            type: string
            format: uri
          maxItems: 5
          description: 商品图片URL列表
        remark:
          type: string
          maxLength: 500
          description: 备注
        createdAt:
          type: string
          format: date-time
          description: 创建时间
        updatedAt:
          type: string
          format: date-time
          description: 更新时间
```

### 创建请求 Schema（必填字段）

```yaml
    ProductCreateRequest:
      type: object
      required:
        - name
        - categoryId
        - price
        - stock
        - status
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 50
          description: 商品名称（1-50字符）
        categoryId:
          type: integer
          description: 分类ID（必填）
        price:
          type: number
          minimum: 0
          description: 价格（≥0）
        stock:
          type: integer
          minimum: 0
          description: 库存（≥0）
        status:
          type: integer
          enum: [0, 1, 2]
          default: 0
          description: 状态（默认草稿）
        images:
          type: array
          items:
            type: string
          maxItems: 5
          description: 商品图片（≤5张）
        remark:
          type: string
          maxLength: 500
          description: 备注（≤500字符）
```

### 更新请求 Schema

```yaml
    ProductUpdateRequest:
      type: object
      required:
        - id
      properties:
        id:
          type: integer
          description: 商品ID（必填）
        name:
          type: string
          minLength: 1
          maxLength: 50
        categoryId:
          type: integer
        price:
          type: number
          minimum: 0
        stock:
          type: integer
          minimum: 0
        status:
          type: integer
          enum: [0, 1, 2]
        images:
          type: array
          items:
            type: string
          maxItems: 5
        remark:
          type: string
          maxLength: 500
```

---

## 响应模板

### 标准响应

```yaml
components:
  responses:
    BadRequest:
      description: 请求参数错误
      content:
        application/json:
          schema:
            type: object
            properties:
              code:
                type: integer
                example: 400
              message:
                type: string
                example: 参数校验失败
              errors:
                type: array
                items:
                  type: object
                  properties:
                    field:
                      type: string
                    message:
                      type: string
    Unauthorized:
      description: 未授权
      content:
        application/json:
          schema:
            type: object
            properties:
              code:
                type: integer
                example: 401
              message:
                type: string
                example: 请先登录
    Forbidden:
      description: 无权限
      content:
        application/json:
          schema:
            type: object
            properties:
              code:
                type: integer
                example: 403
              message:
                type: string
                example: 无操作权限
    NotFound:
      description: 资源不存在
      content:
        application/json:
          schema:
            type: object
            properties:
              code:
                type: integer
                example: 404
              message:
                type: string
                example: 数据不存在
```

---

## ER图 → Schema 映射规则

| ER图字段 | OpenAPI Schema | 说明 |
|---------|---------------|------|
| `id PK` | `type: integer` | 主键 |
| `name VARCHAR(50)` | `type: string, maxLength: 50` | 字符串 |
| `price DECIMAL(10,2)` | `type: number` | 数字 |
| `status ENUM(0,1,2)` | `type: integer, enum: [0,1,2]` | 枚举 |
| `remark TEXT` | `type: string, maxLength: 500` | 长文本 |
| `created_at DATETIME` | `type: string, format: date-time` | 时间 |
| `images JSON` | `type: array` | 数组 |
| `NOT NULL` | `required: true` | 必填 |
| `DEFAULT 0` | `default: 0` | 默认值 |

---

## 输出文件命名

```
openapi-[模块名]-v[版本].yaml

示例：
openapi-product-v1.0.yaml
openapi-order-v1.0.yaml
```

---

## 输出检查清单

```
☐ 接口路径符合 RESTful 规范
☐ 每个接口有 summary 和 description
☐ description 包含功能ID和业务规则
☐ 请求参数有类型、必填、约束
☐ 返回值有完整的 Schema 定义
☐ 分页接口返回 list + total 格式
☐ 错误响应使用标准模板
☐ Schema 从 ER图 正确映射
☐ 字段约束与 PRD 一致
```

