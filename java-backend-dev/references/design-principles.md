# 设计原则与最佳实践参考

> 按需加载。适用场景：SOLID 原则、DRY/KISS、设计模式、DDD、防御性编程、架构决策。

---

## 一、设计原则定位

| 原则 | 应用程度 | 说明 |
|------|---------|------|
| **SOLID** | 适度应用 | 在 Service 层重点实践，避免过度设计 |
| **DRY** | 强制执行 | 消除重复代码，提取公共逻辑 |
| **KISS** | 强制执行 | 简单优先，避免过度抽象 |
| **设计模式** | 按需使用 | 策略模式、工厂模式、模板方法等 |
| **DDD** | 概念借鉴 | Entity/VO/Repository/领域服务，不强求聚合根 |
| **防御性编程** | 强制执行 | 输入/输出/状态/并发全面防御 |

---

## 二、SOLID 原则要点

### S - 单一职责

```java
// ❌ 违反 SRP：一个 Service 承担过多职责
public interface UserService {
    UserDO getUser(Long id);           // 查询
    Long createUser(UserSaveReqVO vo); // 命令
    String login(LoginReqVO vo);       // 认证
    void assignRole(Long userId, Long roleId); // 权限
}

// ✅ 符合 SRP：按职责拆分
public interface UserQueryService { Optional<UserDO> getUser(Long id); }
public interface UserCommandService { Long createUser(UserSaveReqVO vo); }
public interface AuthService { LoginRespVO login(LoginReqVO vo); }
```

### O - 开闭原则（策略模式）

```java
// ❌ 违反 OCP：每次新增类型都要修改方法
public BigDecimal calculateDiscount(Integer userType, BigDecimal amount) {
    if (userType == 1) return amount;                    // 普通
    else if (userType == 2) return amount.multiply("0.9"); // VIP
    else if (userType == 3) return amount.multiply("0.8"); // SVIP
    // 新增类型需要修改此处...
}

// ✅ 符合 OCP：策略模式 + 枚举
@Getter
@AllArgsConstructor
public enum UserTypeEnum {
    NORMAL (1, "普通", amount -> amount),
    VIP    (2, "VIP",  amount -> amount.multiply(new BigDecimal("0.9"))),
    SVIP   (3, "SVIP", amount -> amount.multiply(new BigDecimal("0.8")));
    
    private final Integer type;
    private final String name;
    private final Function<BigDecimal, BigDecimal> discountStrategy;
    
    public static UserTypeEnum of(Integer type) {
        return Arrays.stream(values()).filter(e -> e.type.equals(type)).findFirst().orElse(NORMAL);
    }
}

// 使用
public BigDecimal calculateDiscount(Integer userType, BigDecimal amount) {
    return UserTypeEnum.of(userType).getDiscountStrategy().apply(amount);
}
```

### L - 里氏替换 & I - 接口隔离

```java
// ✅ 小接口，易替换
public interface NotificationSender { void send(String to, String content); }

@Component
public class EmailSender implements NotificationSender { /* 邮件实现 */ }

@Component
public class SmsSender implements NotificationSender { /* 短信实现 */ }
```

### D - 依赖倒置

```java
// ❌ 违反 DIP：直接依赖具体实现
@Resource
private OrderMapper orderMapper;  // 直接依赖 MyBatis

// ✅ 符合 DIP：依赖抽象（大型项目适用）
public interface OrderRepository {
    Optional<OrderDO> findById(Long id);
    void save(OrderDO order);
}
```

---

## 三、DRY 原则

### 重复代码消除

```java
// ❌ 多个 Service 有相同校验逻辑
public void validateName(String name) {
    if (StrUtil.isBlank(name)) throw exception(NAME_EMPTY);
    if (name.length() > 64) throw exception(NAME_TOO_LONG);
}

// ✅ 提取公共工具
public final class ValidationUtils {
    public static void validateName(String name, int maxLength) {
        Preconditions.checkArgument(StrUtil.isNotBlank(name), "名称不能为空");
        Preconditions.checkArgument(name.length() <= maxLength, "名称过长");
    }
    public static void validateId(Long id) {
        Preconditions.checkArgument(id != null && id > 0, "ID必须为正数");
    }
}
```

---

## 四、KISS 原则

### 何时引入设计模式

| 场景 | 是否引入 | 说明 |
|------|---------|------|
| 2 种分支判断 | 不引入 | if-else 足够 |
| 3+ 种分支判断 | 策略模式 | 枚举 + 策略 |
| 创建逻辑复杂/可扩展 | 工厂模式 | Spring 自动注入 |
| 流程固定，步骤可变 | 模板方法 | 骨架 + 钩子 |
| 跨多实体的业务规则 | Helper 类 | 领域服务 |

```java
// ✅ 适度设计：场景驱动

// 简单条件 → 不引入模式
public String getStatusLabel(Integer status) {
    return status == 1 ? "启用" : "禁用";
}

// 多条件判断 → 策略模式
public BigDecimal calculateDiscount(UserTypeEnum userType, BigDecimal amount) {
    return userType.getDiscountStrategy().apply(amount);
}

// 创建逻辑有变化 → 工厂模式
@Component
public class PaymentProcessorFactory {
    private final Map<String, PaymentProcessor> processors;
    // Spring 自动注入所有实现，新增支付方式只需加 @Component
}

// 跨实体计算 → Helper 类
@Component
public class OrderPricingHelper {
    public BigDecimal calculateTotalPrice(List<OrderItemDO> items) { /* 跨 Order 和 OrderItem */ }
}
```

---

## 五、常用设计模式

### 模板方法模式

```java
public abstract class AbstractImportService<T> {
    
    public final ImportResult importData(MultipartFile file) {
        List<T> dataList = parseFile(file);           // 子类实现
        ImportValidationResult result = validateData(dataList); // 子类实现
        if (result.hasError()) return ImportResult.failure(result.getErrors());
        int savedCount = saveData(dataList);          // 子类实现
        afterImport(dataList);                        // 钩子，可选
        return ImportResult.success(savedCount);
    }
    
    protected abstract List<T> parseFile(MultipartFile file);
    protected abstract ImportValidationResult validateData(List<T> dataList);
    protected abstract int saveData(List<T> dataList);
    protected void afterImport(List<T> dataList) {}   // 默认空实现
}
```

### 观察者模式（Spring Event）

```java
// 发布事件
@Transactional(rollbackFor = Exception.class)
public Long createOrder(OrderCreateReqVO reqVO) {
    orderMapper.insert(order);
    eventPublisher.publishEvent(new OrderCreatedEvent(this, order.getId()));
    return order.getId();
}

// 监听事件（事务后执行）
@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
public void onOrderCreated(OrderCreatedEvent event) {
    inventoryService.decreaseStock(event.getProductIds());
    notificationService.notifyOrderCreated(event.getOrderId());
}
```

---

## 六、DDD 概念映射

| DDD 概念 | 本项目映射 | 说明 |
|---------|-----------|------|
| Entity | DO | 有唯一标识，状态可变 |
| Value Object | VO（部分） | 无标识，不可变 |
| Aggregate | Service 方法边界 | 一致性边界 |
| Domain Service | Helper/Manager | 跨实体业务规则 |
| Repository | Mapper | 持久化抽象 |
| Domain Event | Event + EventListener | 解耦副作用 |

### 领域服务（Helper）

```java
/**
 * 跨实体业务规则 → 提取到 Helper
 */
@Component
public class OrderPricingHelper {
    
    public BigDecimal calculateTotalPrice(List<OrderItemDO> items) {
        if (CollUtil.isEmpty(items)) return BigDecimal.ZERO;
        return items.stream()
                .map(item -> item.getPrice().multiply(new BigDecimal(item.getQuantity())))
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
    
    public BigDecimal calculateDiscountedPrice(List<OrderItemDO> items, UserTypeEnum userType) {
        return userType.getDiscountStrategy().apply(calculateTotalPrice(items));
    }
}
```

---

## 七、防御性编程

### 输入防御

```java
@Override
@Transactional(rollbackFor = Exception.class)
public Long createOrder(OrderCreateReqVO reqVO) {
    // 1. 非空防御
    Objects.requireNonNull(reqVO, "订单请求不能为空");
    
    // 2. 前置条件
    Preconditions.checkArgument(reqVO.getUserId() != null && reqVO.getUserId() > 0, "用户ID无效");
    Preconditions.checkArgument(CollUtil.isNotEmpty(reqVO.getItems()), "订单明细不能为空");
    
    // 3. 边界值
    Preconditions.checkArgument(reqVO.getItems().size() <= 100, "明细数量超限");
    
    // 4. 关联数据
    UserDO user = userService.getById(reqVO.getUserId())
            .orElseThrow(() -> exception(USER_NOT_EXISTS));
    Preconditions.checkState(UserStatusEnum.ENABLED.matches(user.getStatus()), "用户已禁用");
    
    // 核心逻辑...
}
```

### 输出防御

```java
// 单条查询：永不返回 null
public Optional<OrderDO> getOrder(Long id) {
    if (id == null || id <= 0) return Optional.empty();
    return Optional.ofNullable(orderMapper.selectById(id));
}

// 列表查询：永不返回 null
public List<OrderDO> getOrdersByUserId(Long userId) {
    if (userId == null || userId <= 0) return Collections.emptyList();
    List<OrderDO> orders = orderMapper.selectByUserId(userId);
    return orders != null ? orders : Collections.emptyList();
}
```

### 状态防御

```java
@Getter
@AllArgsConstructor
public enum OrderStatusEnum {
    PENDING(0), PAID(1), SHIPPED(2), COMPLETED(3), CANCELLED(4);
    
    private final Integer status;
    
    // 状态转换规则
    private static final Map<OrderStatusEnum, Set<OrderStatusEnum>> ALLOWED = Map.of(
        PENDING,   Set.of(PAID, CANCELLED),
        PAID,      Set.of(SHIPPED, CANCELLED),
        SHIPPED,   Set.of(COMPLETED),
        COMPLETED, Set.of(),
        CANCELLED, Set.of()
    );
    
    public boolean canTransitionTo(OrderStatusEnum target) {
        return ALLOWED.getOrDefault(this, Set.of()).contains(target);
    }
}

// 使用
if (!currentStatus.canTransitionTo(OrderStatusEnum.PAID)) {
    throw exception(ORDER_STATUS_NOT_ALLOW_PAY);
}
```

---

## 八、架构决策指南

### 业务方法放哪里？

```
是否仅依赖 DO 自身字段？
  ├─ 是 → DO 方法（isEnabled(), isValid()）
  └─ 否 → 是否需要查询其他数据？
          ├─ 是 → Service 方法
          └─ 否 → 是否跨多个实体类型？
                  ├─ 是 → Helper 类
                  └─ 否 → Service 方法
```

### 是否需要设计模式？

```
分支判断有几种？
  ├─ 1-2 种 → if-else 足够
  └─ 3+ 种 → 策略模式 + 枚举

创建逻辑是否复杂/可扩展？
  ├─ 简单 → 直接 new 或 Builder
  └─ 复杂 → 工厂模式

流程是否固定但步骤可变？
  ├─ 是 → 模板方法模式
  └─ 否 → 不引入

是否需要解耦后续动作？
  ├─ 是 → 观察者模式（Spring Event）
  └─ 否 → 直接调用
```

---

## 九、设计原则约束

| ID | 规则 |
|----|------|
| C-DESIGN-001 | Service 方法职责单一，一个方法只做一件事 |
| C-DESIGN-002 | 分支判断超过 3 种时使用策略模式 |
| C-DESIGN-003 | 重复代码出现 2 次以上必须提取 |
| C-DESIGN-004 | 仅依赖 DO 自身字段的方法放在 DO |
| C-DESIGN-005 | 跨多个实体的业务规则抽取到 Helper |
| C-DESIGN-006 | 公共方法必须有输入防御 |
| C-DESIGN-007 | 查询方法永不返回 null |
| C-DESIGN-008 | 状态变更必须有状态机校验 |
| C-DESIGN-009 | 使用 @Resource 注入，禁止 @Autowired |
| C-DESIGN-010 | 优先简单实现，避免过度抽象 |

---

## 十、设计自检清单

```
SOLID：
□ Service 是否按职责拆分？
□ 方法是否职责单一？
□ 分支判断是否用策略模式？

DRY：
□ 是否有重复代码？
□ 公共逻辑是否提取？
□ 是否有魔法数字？

KISS：
□ 是否过度设计？
□ 能否更简单？

防御性编程：
□ 输入是否校验？
□ 输出是否永不 null？
□ 状态转换是否合法？
□ 并发是否有锁保护？
```