# 质量门控清单

> 代码生成前后逐条自检。

---

## 架构层

```
□ [C-ARCH-001] Controller 参数/返回值无 DO
□ [C-ARCH-002] Service 层无 Wrapper 构造
□ [C-ARCH-003] 转换方法在目标 Bean，无批量 setter
□ [C-ARCH-004] 单条查询返回 Optional<DO>；列表/分页返回集合
□ [C-ARCH-005] DO 业务方法无 Service/Mapper 依赖
□ [C-ARCH-006] 排序用 DO/ServiceImpl 静态 Comparator
□ [C-ARCH-007] 外部调用封装在 {Entity}Client
```

---

## 代码规范

```
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
```

---

## 数据层

```
□ [C-DATA-001] UNIQUE KEY 仅用于业务必须的唯一性约束（如用户名、手机号）
□ [C-DATA-002] 批量操作用 insertBatch/updateBatchById
□ [C-DATA-003] Mapper.xml 定义 <sql id="columns"> 片段，SELECT 通过 <include> 引用
```

---

## 配置文件（涉及 YAML 变更时检查）

```
□ [C-CONF-001] 功能分区有 --- 分隔符和标题注释
□ [C-CONF-002] 重复值用 ${} 引用
□ [C-CONF-003] 环境相关配置只在 profile 文件中
□ [C-CONF-004] JDBC URL 参数齐全
□ [C-CONF-005] 自定义配置在 {project}: 命名空间下
□ [C-CONF-006] 所有 profile 文件（local/dev/prod）已同步
□ [C-CONF-007] 无硬编码明文密码（生产环境）
```

---

## 安全（涉及认证/授权/敏感数据时检查）

```
□ [C-SEC-001] 密码用 BCrypt 加密
□ [C-SEC-002] Token 有效期 ≤ 2h
□ [C-SEC-003] 敏感字段（手机号、邮箱）脱敏存储或加密
□ [C-SEC-004] SQL 用 #{} 防注入，禁止 ${}
□ [C-SEC-005] 接口有权限注解 @PreAuthorize
□ [C-SEC-006] 日志不打印敏感信息（密码、token）
□ [C-SEC-007] 外部调用有超时配置
□ [C-SEC-008] 文件上传校验类型和大小
□ [C-SEC-009] XSS 风险字段（用户输入）做转义
□ [C-SEC-010] CSRF 保护（如有需要）
```

---

## 设计原则

```
□ [C-DESIGN-001] 方法职责单一，一个方法只做一件事
□ [C-DESIGN-002] 分支判断超过 3 种时使用策略模式
□ [C-DESIGN-003] 重复代码出现 2 次以上必须提取
□ [C-DESIGN-004] 仅依赖 DO 自身字段的方法放在 DO
□ [C-DESIGN-005] 跨多个实体的业务规则抽取到 Helper
□ [C-DESIGN-006] 公共方法必须有输入防御
□ [C-DESIGN-007] 查询方法永不返回 null
□ [C-DESIGN-008] 状态变更必须有状态机校验
□ [C-DESIGN-009] 使用 @Resource 注入，禁止 @Autowired
□ [C-DESIGN-010] 优先简单实现，避免过度抽象
```