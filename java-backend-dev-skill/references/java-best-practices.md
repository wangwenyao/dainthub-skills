# Java 最佳实践参考

> 按需加载。适用场景：集合处理、Stream、枚举、异常、Hutool、JSON、设计模式、排序逻辑。

---

## 一、工具类使用规范（C-CODE-004 / C-CODE-005）

### Hutool Core 统一工具集

```java
// ── 字符串（StrUtil）──────────────────────────────────────
StrUtil.isBlank(str)               // null 安全空白检查（含空格）
StrUtil.isNotBlank(str)
StrUtil.format("用户 {} 操作失败", name) // 轻量占位符，禁用 String.format
StrUtil.toUnderlineCase(str)       // 驼峰 → 下划线
StrUtil.toCamelCase(str)           // 下划线 → 驼峰
StrUtil.padPre(str, 6, '0')        // 左补零
StrUtil.hide(mobile, 3, 7)         // 脱敏：138****0000

// ── 集合（CollUtil）─────────────────────────────────────
CollUtil.isEmpty(coll)             // null 安全
CollUtil.isNotEmpty(coll)
CollUtil.newHashSet(e1, e2, e3)    // 快速构造 Set
CollUtil.split(list, 500)          // 分批，批量操作必用

// ── Map（MapUtil）──────────────────────────────────────
MapUtil.isEmpty(map)
MapUtil.newHashMap(size)           // 指定初始容量

// ── 时间（LocalDateTimeUtil / DateUtil）─────────────────
LocalDateTime now   = LocalDateTimeUtil.now();
LocalDateTime begin = LocalDateTimeUtil.beginOfDay(LocalDate.now());
LocalDateTime end   = LocalDateTimeUtil.endOfDay(LocalDate.now());
// 格式化
String s = LocalDateTimeUtil.format(now, DatePattern.NORM_DATETIME_PATTERN);
// 解析
LocalDateTime dt = LocalDateTimeUtil.parse("2024-01-01 00:00:00");
// 时间差
long days = LocalDateTimeUtil.between(start, end, ChronoUnit.DAYS);
// 禁止使用 java.util.Date / Calendar / SimpleDateFormat

// ── 数字（NumberUtil）──────────────────────────────────
NumberUtil.add(a, b)               // BigDecimal 安全加（避免精度问题）
NumberUtil.mul(a, b)
NumberUtil.div(a, b, 4)           // 保留 4 位小数

// ── 断言（Assert）──────────────────────────────────────
Assert.notNull(obj, "obj 不能为 null");
Assert.notBlank(str, "str 不能为空白");
Assert.isTrue(cond, "条件不满足：{}", detail);

// ── 随机（RandomUtil）──────────────────────────────────
RandomUtil.randomInt(0, 600)       // [0,600) 随机整数，缓存过期抖动常用
RandomUtil.randomString(16)        // 随机字母数字串

// ── Bean 拷贝（BeanUtil）──────────────────────────────
// 简单场景可用；复杂映射在 Bean 的 of()/toEntity() 中处理（C-ARCH-003）
BeanUtil.copyProperties(source, target,
        CopyOptions.create().ignoreNullValue());
```

### JSON 工具（C-CODE-005）

```java
import com.dainthub.{project}.framework.common.util.json.JsonUtils;

// ✅ 序列化
String json = JsonUtils.toJsonString(object);

// ✅ 反序列化
UserDO user        = JsonUtils.parseObject(json, UserDO.class);
List<UserDO> users = JsonUtils.parseArray(json, UserDO.class);

// ❌ 禁止直接使用 Jackson / Fastjson / Gson
new ObjectMapper().writeValueAsString(obj);
JSON.toJSONString(obj);
```

---

## 二、集合处理规范

### 空集合与 null 防御

```java
// ✅ 返回空集合（禁止返回 null，调用方无需 null 判断）
public List<OrderDO> getOrders(Long userId) {
    if (userId == null) {
        return Collections.emptyList();
    }
    return orderMapper.selectByUserId(userId);
}

// ✅ 批量查询前短路
public Map<Long, OrderDO> getOrderMap(Collection<Long> ids) {
    if (CollUtil.isEmpty(ids)) {
        return Collections.emptyMap();
    }
    return orderMapper.selectBatchIds(ids).stream()
            .collect(Collectors.toMap(OrderDO::getId, Function.identity()));
}
```

### 集合初始化

```java
// ✅ 已知大小时指定初始容量，避免频繁扩容
List<String> list = new ArrayList<>(sourceList.size());
Map<Long, String> map = MapUtil.newHashMap(expectedSize);

// ✅ 不可变集合（只读场景）
List<String> fixed = List.of("A", "B", "C");
```

### 分批处理（大集合必用）

```java
// ✅ Hutool CollUtil.split 分批，每批 500 条（C-DATA-005）
CollUtil.split(allIds, 500).forEach(batch ->
    orderMapper.selectBatchIds(batch)
);

// ✅ 批量插入（BaseMapperX 内部已分批）
orderMapper.insertBatch(orderList);
```

---

## 三、Stream 最佳实践

**原则**：涉及 Bean 的流式处理（转换、分组、索引、排序），以静态方法定义在该 Bean 中（C-ARCH-003）。

```java
// ✅ 全部定义在目标 Bean（以 RespVO 为例，详见 SKILL.md Step 4）
{Entity}RespVO.ofList(entities)
{Entity}RespVO.ofListSorted(entities)   // 带排序
{Entity}RespVO.ofPage(page)
{Entity}RespVO.indexById(entities)      // Map<id, VO>

// ✅ 常用模式
// 过滤 + 提取
List<String> names = entities.stream()
        .filter({Entity}DO::isEnabled)          // 充血方法（C-ARCH-005）
        .map({Entity}DO::getName)
        .distinct()
        .sorted()
        .collect(Collectors.toList());

// 防重复 key 的 toMap
Map<Long, {Entity}DO> map = entities.stream()
        .collect(Collectors.toMap({Entity}DO::getId, Function.identity(),
                (exist, newer) -> newer));       // merge：取后者

// 分组
Map<Integer, List<{Entity}DO>> byStatus = entities.stream()
        .collect(Collectors.groupingBy({Entity}DO::getStatus));

// 分组计数
Map<Integer, Long> countByStatus = entities.stream()
        .collect(Collectors.groupingBy({Entity}DO::getStatus, Collectors.counting()));
```

---

## 四、排序规范（C-ARCH-006）

### 在 DO 中定义静态 Comparator（优先）

```java
public class {Entity}DO extends BaseDO {

    private Integer sortOrder;
    private Integer priority;

    // ✅ 简单字段排序：定义在 DO 内，语义清晰，复用方便
    public static final Comparator<{Entity}DO> BY_SORT_ASC =
            Comparator.comparingInt({Entity}DO::getSortOrder);

    public static final Comparator<{Entity}DO> BY_PRIORITY_DESC =
            Comparator.comparing({Entity}DO::getPriority, Comparator.reverseOrder());

    // ✅ 复合排序（sortOrder 升序，priority 降序）
    public static final Comparator<{Entity}DO> BY_SORT_THEN_PRIORITY =
            Comparator.comparingInt({Entity}DO::getSortOrder)
                      .thenComparing({Entity}DO::getPriority, Comparator.reverseOrder());

    // ✅ 用于 Collectors.toMap 的 keyFunction
    public static final Function<{Entity}DO, Long>    KEY_BY_ID   = {Entity}DO::getId;
    public static final Function<{Entity}DO, Integer> KEY_BY_SORT = {Entity}DO::getSortOrder;
}

// 使用方式（语义清晰，无匿名 lambda）
list.sort({Entity}DO.BY_SORT_ASC);
list.stream().sorted({Entity}DO.BY_SORT_THEN_PRIORITY).collect(toList());
```

### 在 ServiceImpl 中定义静态 Comparator（依赖多个 DO 类型时）

```java
@Service
@Slf4j
public class {Entity}ServiceImpl implements {Entity}Service {

    // ✅ 跨 DO 类型的复合排序：定义在 ServiceImpl 静态字段
    private static final Comparator<{Entity}DO> BY_CATEGORY_THEN_SORT =
            Comparator.comparingLong({Entity}DO::getCategoryId)
                      .thenComparingInt({Entity}DO::getSortOrder);

    // ❌ 禁止在方法内匿名构造排序逻辑
    // list.sort((a, b) -> a.getSortOrder() - b.getSortOrder()); // 每次调用都创建对象
}
```

---

## 五、设计模式最佳实践

### 1. 静态工厂模式（C-ARCH-003 核心实现）

```java
// ✅ 目标类持有静态工厂方法（代替构造器，语义清晰）
public class {Entity}RespVO {
    // 单条：of(source)
    public static {Entity}RespVO of({Entity}DO entity) { ... }
    // 批量：ofList(sources)
    public static List<{Entity}RespVO> ofList(List<{Entity}DO> entities) { ... }
    // 分页：ofPage(page)
    public static PageResult<{Entity}RespVO> ofPage(PageResult<{Entity}DO> page) { ... }
}

// SaveReqVO：toEntity（"转为目标类型"的语义）
public class {Entity}SaveReqVO {
    public {Entity}DO toEntity() { ... }
}
```

### 2. 策略模式（替代大量 if-else 的业务分支）

```java
// ❌ 大量 if-else（每增加类型都要修改此方法）
public BigDecimal calcDiscount(Integer userType, BigDecimal amount) {
    if (userType == 1) return amount.multiply(new BigDecimal("0.9"));
    if (userType == 2) return amount.multiply(new BigDecimal("0.8"));
    return amount;
}

// ✅ 策略接口 + 枚举注册（开闭原则：新增类型只加枚举值）
public interface DiscountStrategy {
    BigDecimal calc(BigDecimal amount);
}

@Getter
@AllArgsConstructor
public enum UserTypeEnum {
    NORMAL(1, "普通用户", amount -> amount.multiply(new BigDecimal("0.9"))),
    VIP   (2, "VIP用户",  amount -> amount.multiply(new BigDecimal("0.8")));

    private final Integer     type;
    private final String      name;
    private final DiscountStrategy strategy;

    public static UserTypeEnum of(Integer type) {
        return Arrays.stream(values())
                .filter(e -> e.type.equals(type))
                .findFirst()
                .orElseThrow(() -> new IllegalArgumentException("未知用户类型：" + type));
    }
}

// 使用（无 if-else，直接委托）
BigDecimal discounted = UserTypeEnum.of(userType).getStrategy().calc(amount);
```

### 3. 模板方法模式（标准化处理流程，变化点由子类实现）

```java
// ✅ 抽象基类定义骨架，子类实现差异步骤
public abstract class AbstractOrderProcessor {

    /** 模板方法：处理流程固定，各步骤可扩展 */
    public final void process(Long orderId) {
        log.info("[process][开始处理，orderId={}]", orderId);
        OrderDO order = validateAndGet(orderId);    // 公共步骤
        doProcess(order);                            // 抽象步骤，子类实现
        afterProcess(order);                         // 钩子，子类可选覆盖
        log.info("[process][处理完成，orderId={}]", orderId);
    }

    protected abstract void doProcess(OrderDO order);

    protected void afterProcess(OrderDO order) {
        // 默认空实现，子类按需覆盖
    }
}
```

### 4. Builder 模式（字段超过 3 个时优先用 @Builder）

```java
// ✅ Lombok @Builder 自动生成（禁止多参数构造器传入，避免参数顺序混淆）
OrderDO order = OrderDO.builder()
        .userId(userId)
        .productId(productId)
        .amount(amount)
        .status(OrderStatusEnum.PENDING.getStatus())
        .build();

// ✅ 链式构建 + 条件赋值（Optional 配合）
String cityName = Optional.ofNullable(user)
        .map(UserDO::getAddress)
        .map(AddressDO::getCity)
        .orElse("未知城市");
```

### 5. 观察者模式（事务后异步解耦，详见 service-layer.md）

```java
// 事务提交后触发（解耦主流程与后续动作）
applicationContext.publishEvent(new {Entity}CreatedEvent(entity.getId()));

@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
public void on{Entity}Created({Entity}CreatedEvent event) {
    // 通知、统计、缓存预热等（事务外执行）
}
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
    private final String  name;

    /** 反查（找不到返回 null，让调用方决定处理策略） */
    public static {Entity}StatusEnum of(Integer status) {
        if (status == null) return null;
        for ({Entity}StatusEnum e : values()) {
            if (e.status.equals(status)) return e;
        }
        return null;
    }

    /** 匹配判断（DO 充血方法常用，C-ARCH-005） */
    public boolean matches(Integer status) {
        return this.status.equals(status);
    }
}

// ✅ 使用（禁止魔法数字，C-CODE-002）
if ({Entity}StatusEnum.ENABLE.matches(entity.getStatus())) { ... }
entity.setStatus({Entity}StatusEnum.DISABLE.getStatus());
```

---

## 七、代码可读性规范（Alibaba 规约精选）

### 命名

```java
// ✅ 方法名：动词+名词，清晰表达意图
getUserById(Long id)              // 查询
existEntityByName(Long id, String name)  // 存在性校验（返回 boolean，C-ARCH-003 命名）
buildOrderItem(Order order)       // 构建
calcDiscount(BigDecimal amount)   // 计算

// ✅ 布尔变量用 is/has/can 前缀
boolean isEnabled  = entity.isEnabled();
boolean hasChildren = ...;
boolean canDelete  = ...;

// ✅ 集合/Map 命名加复数/后缀
List<OrderDO>       orderList;
Map<Long, UserDO>   userMap;
Set<Long>           idSet;

// ❌ 禁止无意义命名
String a, b, tmp, data, obj, result2;
```

### 方法与类长度

```java
// ✅ 单方法不超过 80 行；超过则提取有意义名称的私有方法
// ✅ 单类不超过 500 行；超过则按职责拆分

// ✅ 私有方法名即"步骤注释"（代替方法体内大段注释）
public void processOrder(Long orderId) {
    OrderDO order = validateAndGetOrder(orderId);   // 步骤1
    applyDiscountIfEligible(order);                  // 步骤2
    deductStockAtomic(order);                        // 步骤3
    saveOrderAndPublishEvent(order);                 // 步骤4
}
```

### 常量与魔法数字

```java
// ✅ 同一字面量出现 2 次以上必须提取常量
private static final int    BATCH_SIZE      = 500;
private static final String CACHE_KEY_PREFIX = "{module}:{entity}:";
private static final long   LOCK_HOLD_SEC   = 30L;

// ✅ 业务状态枚举替代数字
if ({Entity}StatusEnum.ENABLE.matches(entity.getStatus())) { ... }
// ❌
if (entity.getStatus() == 1) { ... }
```

### 注释规范（C-CODE-008 ~ C-CODE-012）

> **核心原则**：所有 Javadoc 和代码注释使用**中文**编写（C-CODE-008）。

#### Javadoc：必须写的场景

| 位置 | 是否必须 | 要求 |
|------|---------|------|
| Service 接口 `public` 方法 | **必须** | 功能说明 + `@param` + `@return` + `@throws`（C-CODE-009） |
| DO 每个字段 | **必须** | 业务含义 + 约束（取值范围/长度/是否非空）；枚举字段加 `@see`（C-CODE-010） |
| Controller `public` 方法 | 不必须 | 已有 `@Operation(summary=...)` 注解替代 |
| Mapper `default` 方法 | 建议 | 说明查询用途和关键条件 |
| `private` 方法 | 建议 | 逻辑复杂或参数语义不明时写 |

#### Service 接口方法 Javadoc（C-CODE-009）

```java
// ✅ 正确：完整的中文 Javadoc
/**
 * 创建{entity}，返回新建主键。
 *
 * @param createReqVO 创建请求（名称不能重复）
 * @return 新建记录主键 ID
 * @throws ServiceException 名称重复时抛出 {@link ErrorCodeConstants#{ENTITY}_NAME_DUPLICATE}
 */
Long create{Entity}({Entity}SaveReqVO createReqVO);

/**
 * 查询单条{entity}。
 * 存在则返回 {@code Optional.of(entity)}，不存在返回 {@code Optional.empty()}。
 * 调用方自行决定是否抛出异常（C-ARCH-004）。
 *
 * @param id 主键
 * @return {entity}对象，可能为空
 */
Optional<{Entity}DO> get{Entity}OrElse(Long id);

// ❌ 错误：无 Javadoc
void update{Entity}({Entity}SaveReqVO updateReqVO);

// ❌ 错误：英文注释
/** Create entity and return id. */
Long create{Entity}({Entity}SaveReqVO createReqVO);
```

#### DO 字段 Javadoc（C-CODE-010）

```java
// ✅ 正确：说明业务含义 + 约束
/** 主键 */
@TableId(type = IdType.AUTO)
private Long id;

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

/**
 * 排序值（升序，值越小越靠前）
 */
private Integer sortOrder;

/**
 * 总金额
 * decimal(19,4)，单位：元
 */
private BigDecimal totalAmount;

// ❌ 错误：无 Javadoc
private String name;

// ❌ 错误：翻译式注释，没有业务含义
/** 名称字段 */
private String name;
```

#### 行内注释（C-CODE-011）

```java
// ✅ 说明"为什么"
// 逻辑删除：标记不可用，保留历史数据用于审计
entity.setDeleted(true);

// ✅ 说明业务背景
// 更新场景：与自身记录同名则不算重复
return id == null || !existing.getId().equals(id);

// ❌ 翻译式注释：重复代码含义，无附加信息
// 将 status 设为 0
entity.setStatus(0);

// ❌ 无意义注释
// 调用 insert 方法
mapper.insert(entity);
```

#### 代码分区（C-CODE-012）

```java
public class {Entity}DO extends BaseDO {

    // ==================== 字段 ====================

    private Long id;
    private String name;

    // ==================== 充血模型业务方法（C-ARCH-005）====================

    public boolean isEnabled() { ... }
    public void applyUpdate({Entity}SaveReqVO reqVO) { ... }

    // ==================== 静态排序 Comparator（C-ARCH-006）====================

    public static final Comparator<{Entity}DO> BY_SORT_ASC = ...;
}

public class {Entity}ServiceImpl implements {Entity}Service {

    // ==================== 写操作 ====================

    public Long create{Entity}(...) { ... }
    public void update{Entity}(...) { ... }
    public void delete{Entity}(...) { ... }

    // ==================== 读操作 ====================

    public Optional<{Entity}DO> get{Entity}OrElse(...) { ... }
    public PageResult<{Entity}DO> get{Entity}Page(...) { ... }

    // ==================== 内部校验（private）====================

    private boolean exist{Entity}Name(...) { ... }
}
```

### 条件简化

```java
// ✅ 提前 return（减少嵌套）
public void process(OrderDO order) {
    if (order == null) return;
    if (!order.isEnabled()) return;
    // 核心逻辑...
}

// ✅ 复杂条件命名为布尔变量（超过 2 个 && / || 时必须提取）
boolean isHighValue = NumberUtil.isGreater(order.getAmount(), HIGH_VALUE_THRESHOLD);
boolean isVipUser   = UserTypeEnum.VIP.matches(user.getType());
if (isHighValue && isVipUser) {
    applyPremiumDiscount(order);
}

// ✅ 三元表达式只用于简单赋值，禁止嵌套
String label = order.isEnabled() ? "启用" : "禁用";
```

### 异常处理（C-CODE-003 扩展）

```java
// ✅ 捕获具体异常，不用 catch (Exception e) 一把抓（Alibaba 规约）
try {
    orderMapper.insert(order);
} catch (DuplicateKeyException e) {
    // 数据库约束冲突 → 转为业务异常（C-CODE-003）
    log.warn("[createOrder][数据库唯一约束冲突，orderNo={}]", order.getOrderNo());
    throw exception(ORDER_NO_DUPLICATE);
}

// ✅ catch 中必须携带 Throwable 保留堆栈
try {
    externalService.call(param);
} catch (Exception e) {
    log.error("[callExternal][外部服务失败，param={}]", param, e);  // e 放最后
    throw exception(EXTERNAL_SERVICE_ERROR);   // C-CODE-003
}

// ❌ 禁止
throw new RuntimeException("xxx");     // C-CODE-003 违规
catch (Exception e) { }               // 吞异常
catch (Exception e) { log.error(e.getMessage()); }  // 丢失堆栈
```
