# Java 最佳实践参考

> 按需加载。适用场景：集合处理、Stream、枚举、异常、Hutool、JSON、设计模式、排序逻辑。

---

## 一、工具类规范（C-CODE-004 / C-CODE-005）

### Hutool 常用

```java
// ── 字符串 ─────────────────────────────────────
StrUtil.isBlank(str)                    // null 安全空白检查
StrUtil.format("用户 {} 操作失败", name) // 轻量占位符
StrUtil.hide(mobile, 3, 7)              // 脱敏：138****0000

// ── 集合 ─────────────────────────────────────
CollUtil.isEmpty(coll)                  // null 安全
CollUtil.split(list, 500)               // 分批处理（C-DATA-002）

// ── 时间 ─────────────────────────────────────
LocalDateTime now = LocalDateTimeUtil.now();
LocalDateTime begin = LocalDateTimeUtil.beginOfDay(LocalDate.now());
// 禁止使用 java.util.Date / Calendar / SimpleDateFormat

// ── 数字 ─────────────────────────────────────
NumberUtil.add(a, b)                    // BigDecimal 安全计算
NumberUtil.div(a, b, 4)                 // 保留 4 位小数

// ── Bean 拷贝 ───────────────────────────────
BeanUtil.copyProperties(source, target, CopyOptions.create().ignoreNullValue());
```

### JSON 工具（C-CODE-005）

```java
// ✅ 项目统一工具
String json = JsonUtils.toJsonString(object);
UserDO user = JsonUtils.parseObject(json, UserDO.class);

// ❌ 禁止直接使用 Jackson / Fastjson / Gson
```

---

## 二、集合处理

### 空集合防御

```java
// ✅ 返回空集合（禁止返回 null）
public List<OrderDO> getOrders(Long userId) {
    if (userId == null) return Collections.emptyList();
    return orderMapper.selectByUserId(userId);
}

// ✅ 批量查询前短路
public Map<Long, OrderDO> getOrderMap(Collection<Long> ids) {
    if (CollUtil.isEmpty(ids)) return Collections.emptyMap();
    return orderMapper.selectBatchIds(ids).stream()
            .collect(Collectors.toMap(OrderDO::getId, Function.identity()));
}
```

### 分批处理

```java
// ✅ Hutool CollUtil.split 分批，每批 500 条（C-DATA-002）
CollUtil.split(allIds, 500).forEach(batch -> 
    orderMapper.selectBatchIds(batch)
);

// ✅ 批量插入（BaseMapperX 内部已分批）
orderMapper.insertBatch(orderList);
```

---

## 三、Stream 最佳实践

```java
// ✅ 全部定义在目标 Bean（C-ARCH-003）
{Entity}RespVO.ofList(entities)
{Entity}RespVO.ofPage(page)
{Entity}RespVO.indexById(entities)      // Map<id, VO>

// ✅ 常用模式
// 过滤 + 提取
List<String> names = entities.stream()
        .filter({Entity}DO::isEnabled)   // 充血方法
        .map({Entity}DO::getName)
        .distinct()
        .collect(Collectors.toList());

// 防重复 key 的 toMap
Map<Long, {Entity}DO> map = entities.stream()
        .collect(Collectors.toMap({Entity}DO::getId, Function.identity(),
                (exist, newer) -> newer));  // merge：取后者

// 分组
Map<Integer, List<{Entity}DO>> byStatus = entities.stream()
        .collect(Collectors.groupingBy({Entity}DO::getStatus));
```

---

## 四、排序规范（C-ARCH-006）

### 在 DO 中定义静态 Comparator

```java
public class {Entity}DO extends BaseDO {

    // ✅ 简单字段排序
    public static final Comparator<{Entity}DO> BY_SORT_ASC =
            Comparator.comparingInt({Entity}DO::getSortOrder);

    // ✅ 复合排序
    public static final Comparator<{Entity}DO> BY_SORT_THEN_PRIORITY =
            Comparator.comparingInt({Entity}DO::getSortOrder)
                      .thenComparing({Entity}DO::getPriority, Comparator.reverseOrder());

    // ✅ 用于 toMap 的 keyFunction
    public static final Function<{Entity}DO, Long> KEY_BY_ID = {Entity}DO::getId;
}

// 使用
list.sort({Entity}DO.BY_SORT_ASC);
```

---

## 五、设计模式

### 静态工厂模式（C-ARCH-003）

```java
// ✅ 目标类持有静态工厂方法
public class {Entity}RespVO {
    public static {Entity}RespVO of({Entity}DO entity) { ... }
    public static List<{Entity}RespVO> ofList(List<{Entity}DO> entities) { ... }
    public static PageResult<{Entity}RespVO> ofPage(PageResult<{Entity}DO> page) { ... }
}

public class {Entity}SaveReqVO {
    public {Entity}DO toEntity() { ... }
}
```

### 策略模式（替代大量 if-else）

```java
// ✅ 策略接口 + 枚举注册
@Getter
@AllArgsConstructor
public enum UserTypeEnum {
    NORMAL(1, "普通", amount -> amount.multiply("0.9")),
    VIP   (2, "VIP",  amount -> amount.multiply("0.8"));

    private final Integer type;
    private final String name;
    private final Function<BigDecimal, BigDecimal> strategy;

    public static UserTypeEnum of(Integer type) {
        return Arrays.stream(values()).filter(e -> e.type.equals(type)).findFirst().orElse(NORMAL);
    }
}

// 使用
BigDecimal discounted = UserTypeEnum.of(userType).getStrategy().apply(amount);
```

### 模板方法模式

```java
public abstract class AbstractOrderProcessor {

    public final void process(Long orderId) {
        OrderDO order = validateAndGet(orderId);  // 公共步骤
        doProcess(order);                          // 抽象步骤
        afterProcess(order);                       // 钩子
    }

    protected abstract void doProcess(OrderDO order);
    protected void afterProcess(OrderDO order) {}  // 默认空实现
}
```

### Builder 模式

```java
// ✅ Lombok @Builder（字段超过 3 个时优先）
OrderDO order = OrderDO.builder()
        .userId(userId)
        .amount(amount)
        .status(OrderStatusEnum.PENDING.getStatus())
        .build();
```

---

## 六、枚举规范（C-CODE-002）

```java
@Getter
@AllArgsConstructor
public enum {Entity}StatusEnum {

    DISABLE(0, "禁用"),
    ENABLE (1, "启用");

    private final Integer status;
    private final String name;

    public static {Entity}StatusEnum of(Integer status) {
        if (status == null) return null;
        for ({Entity}StatusEnum e : values()) {
            if (e.status.equals(status)) return e;
        }
        return null;
    }

    public boolean matches(Integer status) {
        return this.status.equals(status);
    }
}

// ✅ 使用（禁止魔法数字）
if ({Entity}StatusEnum.ENABLE.matches(entity.getStatus())) { ... }
```

---

## 七、命名与代码可读性

### 命名规范

```java
// ✅ 方法名：动词+名词
getUserById(Long id)               // 查询
existEntityByName(Long id, String name)  // 存在性校验
buildOrderItem(Order order)        // 构建

// ✅ 布尔变量用 is/has/can 前缀
boolean isEnabled = entity.isEnabled();
boolean hasChildren = ...;

// ✅ 集合/Map 命名加复数/后缀
List<OrderDO> orderList;
Map<Long, UserDO> userMap;
Set<Long> idSet;
```

### 方法长度

```java
// ✅ 单方法不超过 80 行；超过则提取私有方法
// ✅ 私有方法名即"步骤注释"
public void processOrder(Long orderId) {
    OrderDO order = validateAndGetOrder(orderId);
    applyDiscountIfEligible(order);
    deductStockAtomic(order);
    saveOrderAndPublishEvent(order);
}
```

### 常量提取

```java
// ✅ 同一字面量出现 2 次以上必须提取常量
private static final int BATCH_SIZE = 500;
private static final String CACHE_KEY_PREFIX = "{module}:{entity}:";

// ❌ 魔法数字
if (entity.getStatus() == 1) { ... }
```

---

## 八、注释规范（C-CODE-008 ~ C-CODE-012）

### 必须写的 Javadoc

| 位置 | 要求 |
|------|------|
| Service 接口 public 方法 | 功能说明 + @param + @return + @throws（C-CODE-009） |
| DO 每个字段 | 业务含义 + 约束；枚举字段加 @see（C-CODE-010） |

### Service 方法 Javadoc

```java
/**
 * 创建{entity}，返回新建主键。
 *
 * @param createReqVO 创建请求（名称不能重复）
 * @return 新建记录主键 ID
 * @throws ServiceException 名称重复时抛出
 */
Long create{Entity}({Entity}SaveReqVO createReqVO);
```

### DO 字段 Javadoc

```java
/**
 * 名称
 * 非空，最大 64 字符，同模块下唯一
 */
private String name;

/**
 * 状态
 * @see {Entity}StatusEnum
 */
private Integer status;
```

### 代码分区（C-CODE-012）

```java
public class {Entity}ServiceImpl implements {Entity}Service {

    // ==================== 写操作 ====================

    public Long create{Entity}(...) { ... }
    public void update{Entity}(...) { ... }

    // ==================== 读操作 ====================

    public Optional<{Entity}DO> get{Entity}OrElse(...) { ... }

    // ==================== 内部校验 ====================

    private boolean exist{Entity}Name(...) { ... }
}
```

---

## 九、异常处理（C-CODE-003）

```java
// ✅ 捕获具体异常
try {
    orderMapper.insert(order);
} catch (DuplicateKeyException e) {
    log.warn("[createOrder][唯一约束冲突，orderNo={}]", order.getOrderNo());
    throw exception(ORDER_NO_DUPLICATE);
}

// ✅ catch 中必须携带 Throwable 保留堆栈
try {
    externalService.call(param);
} catch (Exception e) {
    log.error("[callExternal][失败，param={}]", param, e);  // e 放最后
    throw exception(EXTERNAL_SERVICE_ERROR);
}

// ❌ 禁止
throw new RuntimeException("xxx");    // C-CODE-003 违规
catch (Exception e) { }              // 吞异常
```