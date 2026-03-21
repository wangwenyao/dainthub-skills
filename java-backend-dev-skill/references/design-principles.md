# 设计原则与最佳实践参考

> 按需加载。适用场景：SOLID 原则、DRY/KISS、设计模式、DDD、防御性编程、架构决策。

---

## 一、架构风格定位

### 本项目采用：务实分层架构

```
┌─────────────────────────────────────────────────────────┐
│                    Controller 层                        │
│              （接口适配、参数校验、响应组装）              │
├─────────────────────────────────────────────────────────┤
│                     Service 层                          │
│          （业务逻辑、事务编排、领域服务调用）             │
├─────────────────────────────────────────────────────────┤
│  Helper/Manager 层（可选）                              │
│        （跨实体业务规则、复杂计算逻辑）                   │
├─────────────────────────────────────────────────────────┤
│                     Mapper 层                           │
│                 （数据持久化抽象）                       │
└─────────────────────────────────────────────────────────┘
```

### 设计原则定位

| 原则 | 应用程度 | 说明 |
|------|---------|------|
| **SOLID** | 适度应用 | 在 Service 层重点实践，避免过度设计 |
| **DRY** | 强制执行 | 消除重复代码，提取公共逻辑 |
| **KISS** | 强制执行 | 简单优先，避免过度抽象 |
| **设计模式** | 按需使用 | 策略模式、工厂模式、模板方法等 |
| **DDD** | 概念借鉴 | Entity/VO/Repository/领域服务，不强求聚合根 |
| **防御性编程** | 强制执行 | 输入/输出/状态/并发全面防御 |

---

## 二、SOLID 原则实践

### S - 单一职责原则（Single Responsibility）

**核心**：一个类/方法只做一件事。

#### Service 按职责拆分

```java
// ❌ 违反 SRP：一个 Service 承担过多职责
public interface UserService {
    // 查询职责
    UserDO getUser(Long id);
    PageResult<UserDO> getUserPage(UserPageReqVO reqVO);
    
    // 命令职责
    Long createUser(UserSaveReqVO reqVO);
    void updateUser(UserSaveReqVO reqVO);
    void deleteUser(Long id);
    
    // 认证职责
    String login(LoginReqVO reqVO);
    void logout(String token);
    
    // 权限职责
    void assignRole(Long userId, Long roleId);
    List<Long> getUserRoles(Long userId);
}

// ✅ 符合 SRP：按职责拆分
public interface UserQueryService {
    Optional<UserDO> getUser(Long id);
    PageResult<UserDO> getUserPage(UserPageReqVO reqVO);
    boolean existsByUsername(String username);
}

public interface UserCommandService {
    Long createUser(UserSaveReqVO reqVO);
    void updateUser(UserSaveReqVO reqVO);
    void deleteUser(Long id);
}

public interface AuthService {
    LoginRespVO login(LoginReqVO reqVO);
    void logout(String token);
    TokenRespVO refreshToken(String refreshToken);
}

public interface UserPermissionService {
    void assignRole(Long userId, Long roleId);
    void removeRole(Long userId, Long roleId);
    Set<Long> getUserRoleIds(Long userId);
}
```

#### 方法职责单一

```java
// ❌ 违反 SRP：一个方法做多件事
public Long createOrder(OrderCreateReqVO reqVO) {
    // 创建订单
    OrderDO order = reqVO.toEntity();
    
    // 扣减库存
    for (OrderItemDO item : order.getItems()) {
        productMapper.decreaseStock(item.getProductId(), item.getQuantity());
    }
    
    // 发送通知
    notificationService.sendOrderCreatedNotification(order);
    
    // 更新统计
    statisticsService.incrementOrderCount(order.getUserId());
    
    orderMapper.insert(order);
    return order.getId();
}

// ✅ 符合 SRP：职责分离，主方法编排
public Long createOrder(OrderCreateReqVO reqVO) {
    // 1. 创建订单（主职责）
    OrderDO order = buildOrder(reqVO);
    orderMapper.insert(order);
    
    // 2. 编排副作用（事务后执行）
    publishOrderCreatedEvent(order);
    
    return order.getId();
}

private OrderDO buildOrder(OrderCreateReqVO reqVO) {
    OrderDO order = reqVO.toEntity();
    order.setOrderNo(generateOrderNo());
    return order;
}

@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
public void onOrderCreated(OrderCreatedEvent event) {
    // 库存、通知、统计在事务外处理
    inventoryService.decreaseStock(event.getOrderItems());
    notificationService.notifyOrderCreated(event.getOrderId());
    statisticsService.incrementOrderCount(event.getUserId());
}
```

### O - 开闭原则（Open/Closed）

**核心**：对扩展开放，对修改关闭。

#### 策略模式处理分支

```java
// ❌ 违反 OCP：每次新增类型都要修改方法
public BigDecimal calculateDiscount(Integer userType, BigDecimal amount) {
    if (userType == 1) {  // 普通用户
        return amount;
    } else if (userType == 2) {  // VIP
        return amount.multiply(new BigDecimal("0.9"));
    } else if (userType == 3) {  // SVIP
        return amount.multiply(new BigDecimal("0.8"));
    }
    // 新增类型需要修改此处...
    return amount;
}

// ✅ 符合 OCP：策略模式 + 枚举
public interface DiscountStrategy {
    BigDecimal apply(BigDecimal amount);
}

@Getter
@AllArgsConstructor
public enum UserTypeEnum {
    
    NORMAL (1, "普通用户", amount -> amount),
    VIP    (2, "VIP用户",  amount -> amount.multiply(new BigDecimal("0.9"))),
    SVIP   (3, "SVIP用户", amount -> amount.multiply(new BigDecimal("0.8")));
    // 新增类型只需添加枚举值，无需修改计算逻辑
    
    private final Integer type;
    private final String name;
    private final DiscountStrategy discountStrategy;
    
    public static UserTypeEnum of(Integer type) {
        return Arrays.stream(values())
                .filter(e -> e.type.equals(type))
                .findFirst()
                .orElse(NORMAL);
    }
}

// 使用
public BigDecimal calculateDiscount(Integer userType, BigDecimal amount) {
    return UserTypeEnum.of(userType).getDiscountStrategy().apply(amount);
}
```

#### 工厂模式创建对象

```java
// ❌ 违反 OCP：直接 new，新增类型需要修改
public PaymentProcessor getProcessor(String paymentType) {
    if ("alipay".equals(paymentType)) {
        return new AlipayProcessor();
    } else if ("wechat".equals(paymentType)) {
        return new WechatPayProcessor();
    }
    // 新增支付方式需要修改此处...
    throw new IllegalArgumentException("不支持的支付方式");
}

// ✅ 符合 OCP：工厂 + Spring 自动注入
@Component
public class PaymentProcessorFactory {
    
    private final Map<String, PaymentProcessor> processors;
    
    public PaymentProcessorFactory(List<PaymentProcessor> processorList) {
        this.processors = processorList.stream()
                .collect(Collectors.toMap(
                        PaymentProcessor::getType,
                        Function.identity()
                ));
    }
    
    public PaymentProcessor getProcessor(String type) {
        PaymentProcessor processor = processors.get(type);
        if (processor == null) {
            throw exception(PAYMENT_TYPE_NOT_SUPPORTED);
        }
        return processor;
    }
}

// 各处理器实现统一接口
public interface PaymentProcessor {
    String getType();
    PaymentResult pay(PaymentRequest request);
}

@Component
public class AlipayProcessor implements PaymentProcessor {
    @Override
    public String getType() { return "alipay"; }
    
    @Override
    public PaymentResult pay(PaymentRequest request) { ... }
}

@Component
public class WechatPayProcessor implements PaymentProcessor {
    @Override
    public String getType() { return "wechat"; }
    
    @Override
    public PaymentResult pay(PaymentRequest request) { ... }
}
```

### L - 里氏替换原则（Liskov Substitution）

**核心**：子类可以替换父类而不影响程序正确性。

```java
// ✅ 接口隔离：小接口，易替换
public interface NotificationSender {
    void send(String to, String content);
}

@Component
public class EmailSender implements NotificationSender {
    @Override
    public void send(String to, String content) {
        // 邮件发送实现
    }
}

@Component
public class SmsSender implements NotificationSender {
    @Override
    public void send(String to, String content) {
        // 短信发送实现
    }
}

// 任意实现都可以替换
@Service
public class NotificationService {
    
    private final Map<String, NotificationSender> senders;
    
    public void send(String channel, String to, String content) {
        NotificationSender sender = senders.get(channel);
        sender.send(to, content);  // 任意子类都能正确工作
    }
}
```

### I - 接口隔离原则（Interface Segregation）

**核心**：接口要小而专注。

```java
// ❌ 违反 ISP：大接口，客户端被迫依赖不需要的方法
public interface UserRepository {
    UserDO findById(Long id);
    void save(UserDO user);
    void delete(Long id);
    List<UserDO> findAll();
    PageResult<UserDO> findPage(PageRequest request);
    UserDO findByUsername(String username);
    void updatePassword(Long id, String password);
    void updateStatus(Long id, Integer status);
    // ... 更多方法
}

// ✅ 符合 ISP：小接口，按职责分离
public interface UserReader {
    Optional<UserDO> findById(Long id);
    Optional<UserDO> findByUsername(String username);
    PageResult<UserDO> findPage(UserPageReqVO reqVO);
}

public interface UserWriter {
    void save(UserDO user);
    void delete(Long id);
}

public interface UserPasswordUpdater {
    void updatePassword(Long id, String encodedPassword);
}

public interface UserStatusUpdater {
    void updateStatus(Long id, Integer status);
}

// 实现类可以组合
@Service
public class UserServiceImpl implements 
        UserReader, UserWriter, UserPasswordUpdater, UserStatusUpdater {
    // ...
}
```

### D - 依赖倒置原则（Dependency Inversion）

**核心**：依赖抽象，不依赖具体实现。

```java
// ❌ 违反 DIP：直接依赖具体实现
@Service
public class OrderServiceImpl {
    
    @Resource
    private OrderMapper orderMapper;  // 直接依赖 MyBatis 实现
    
    @Resource
    private RedisTemplate<String, Object> redisTemplate;  // 直接依赖 Redis
    
    // ...
}

// ✅ 符合 DIP：依赖抽象
// 定义 Repository 接口（领域层）
public interface OrderRepository {
    Optional<OrderDO> findById(Long id);
    void save(OrderDO order);
    void delete(Long id);
}

// 定义缓存接口
public interface OrderCache {
    Optional<OrderDO> get(Long id);
    void put(OrderDO order);
    void evict(Long id);
}

// 实现类（基础设施层）
@Repository
public class OrderRepositoryImpl implements OrderRepository {
    
    @Resource
    private OrderMapper orderMapper;
    
    @Override
    public Optional<OrderDO> findById(Long id) {
        return Optional.ofNullable(orderMapper.selectById(id));
    }
    
    @Override
    public void save(OrderDO order) {
        if (order.getId() == null) {
            orderMapper.insert(order);
        } else {
            orderMapper.updateById(order);
        }
    }
    
    @Override
    public void delete(Long id) {
        orderMapper.deleteById(id);
    }
}

// Service 依赖抽象
@Service
public class OrderServiceImpl implements OrderService {
    
    private final OrderRepository orderRepository;  // 接口
    private final OrderCache orderCache;            // 接口
    private final EventPublisher eventPublisher;    // 接口
    
    public OrderServiceImpl(
            OrderRepository orderRepository,
            OrderCache orderCache,
            EventPublisher eventPublisher) {
        this.orderRepository = orderRepository;
        this.orderCache = orderCache;
        this.eventPublisher = eventPublisher;
    }
    
    // ...
}
```

---

## 三、DRY 原则（Don't Repeat Yourself）

**核心**：每一项知识在系统中必须有单一、明确、权威的表示。

### 重复代码检测与消除

```java
// ❌ 重复代码：多个 Service 有相同逻辑
@Service
public class UserServiceImpl {
    public void validateName(String name) {
        if (StrUtil.isBlank(name)) {
            throw exception(NAME_EMPTY);
        }
        if (name.length() > 64) {
            throw exception(NAME_TOO_LONG);
        }
    }
}

@Service
public class ProductServiceImpl {
    public void validateName(String name) {
        if (StrUtil.isBlank(name)) {
            throw exception(NAME_EMPTY);
        }
        if (name.length() > 64) {
            throw exception(NAME_TOO_LONG);
        }
    }
}

// ✅ DRY：提取公共校验工具
public final class ValidationUtils {
    
    private ValidationUtils() {}
    
    /**
     * 校验名称（通用规则）
     */
    public static void validateName(String name, int maxLength) {
        Preconditions.checkArgument(StrUtil.isNotBlank(name), 
                "名称不能为空");
        Preconditions.checkArgument(name.length() <= maxLength, 
                "名称长度不能超过" + maxLength + "个字符");
    }
    
    /**
     * 校验 ID（通用规则）
     */
    public static void validateId(Long id) {
        Preconditions.checkArgument(id != null && id > 0, 
                "ID必须为正数");
    }
    
    /**
     * 校验分页参数
     */
    public static void validatePageParam(Integer pageNo, Integer pageSize) {
        Preconditions.checkArgument(pageNo != null && pageNo > 0, 
                "页码必须大于0");
        Preconditions.checkArgument(pageSize != null && pageSize > 0 && pageSize <= 100, 
                "每页数量必须在1-100之间");
    }
}

// 使用
@Service
public class UserServiceImpl {
    public void createUser(UserSaveReqVO reqVO) {
        ValidationUtils.validateName(reqVO.getName(), 64);
        // ...
    }
}
```

### 提取公共基类

```java
// ✅ DRY：公共逻辑抽取到基类
public abstract class BaseServiceImpl<DO, Mapper extends BaseMapperX<DO>> {
    
    @Resource
    protected Mapper mapper;
    
    /**
     * 通用单条查询
     */
    public Optional<DO> getById(Long id) {
        return Optional.ofNullable(mapper.selectById(id));
    }
    
    /**
     * 通用分页查询
     */
    public PageResult<DO> getPage(PageReqVO reqVO) {
        return mapper.selectPage(reqVO);
    }
    
    /**
     * 通用保存（新增或更新）
     */
    @Transactional(rollbackFor = Exception.class)
    public void save(DO entity) {
        if (getId(entity) == null) {
            mapper.insert(entity);
        } else {
            mapper.updateById(entity);
        }
    }
    
    /**
     * 通用删除
     */
    @Transactional(rollbackFor = Exception.class)
    public void delete(Long id) {
        mapper.deleteById(id);
    }
    
    /**
     * 子类实现：获取实体 ID
     */
    protected abstract Long getId(DO entity);
}

// 子类继承
@Service
public class ProductServiceImpl 
        extends BaseServiceImpl<ProductDO, ProductMapper> 
        implements ProductService {
    
    @Override
    protected Long getId(ProductDO entity) {
        return entity.getId();
    }
    
    // 只需实现特定业务逻辑
}
```

---

## 四、KISS 原则（Keep It Simple, Stupid）

**核心**：保持简单，避免过度设计。

### 简单优先原则

```java
// ❌ 过度设计：不必要的抽象层
public class OrderFactory {
    private final OrderBuilderFactory orderBuilderFactory;
    private final OrderBuilderDirector orderBuilderDirector;
    
    public OrderDO createOrder(OrderCreateReqVO reqVO) {
        OrderBuilder builder = orderBuilderFactory.createBuilder(reqVO.getType());
        return orderBuilderDirector.construct(builder, reqVO);
    }
}

// ✅ KISS：简单直接
@Service
public class OrderServiceImpl {
    
    public Long createOrder(OrderCreateReqVO reqVO) {
        // 直接转换，无需工厂
        OrderDO order = reqVO.toEntity();
        order.setOrderNo(generateOrderNo());
        orderMapper.insert(order);
        return order.getId();
    }
}
```

### 何时引入设计模式

| 场景 | 是否引入模式 | 说明 |
|------|------------|------|
| 2 种分支判断 | 不引入 | if-else 足够 |
| 3+ 种分支判断 | 引入策略模式 | 枚举 + 策略 |
| 创建逻辑复杂 | 引入工厂模式 | 统一创建入口 |
| 流程固定，步骤可变 | 引入模板方法 | 骨架 + 钩子 |
| 跨多个实体的业务规则 | 引入 Helper 类 | 领域服务 |

```java
// ✅ 适度设计：场景驱动

// 场景1：简单条件 → 不引入模式
public String getStatusLabel(Integer status) {
    return status == 1 ? "启用" : "禁用";
}

// 场景2：多条件判断 → 策略模式
public BigDecimal calculateDiscount(UserTypeEnum userType, BigDecimal amount) {
    return userType.getDiscountStrategy().apply(amount);
}

// 场景3：创建逻辑有变化 → 工厂模式
@Component
public class PaymentProcessorFactory {
    private final Map<String, PaymentProcessor> processors;
    // Spring 自动注入所有实现
}

// 场景4：跨实体计算 → Helper 类
@Component
public class OrderPricingHelper {
    public BigDecimal calculateTotalPrice(OrderDO order, List<OrderItemDO> items) {
        // 跨 Order 和 OrderItem 的计算逻辑
    }
}
```

---

## 五、设计模式实践

### 常用设计模式速查

| 模式 | 适用场景 | 本项目应用 |
|------|---------|-----------|
| **策略模式** | 多种算法/规则切换 | 折扣计算、支付方式、通知渠道 |
| **工厂模式** | 创建逻辑复杂或可扩展 | 处理器工厂、解析器工厂 |
| **模板方法** | 流程固定，步骤可变 | 导入导出、审批流程 |
| **观察者模式** | 事件驱动的解耦 | 订单创建后通知、库存扣减 |
| **Builder 模式** | 复杂对象构建 | DO 构建（Lombok @Builder） |
| **静态工厂** | 简单对象创建/转换 | VO.of()、DO.toEntity() |

### 模板方法模式

```java
/**
 * 导入模板：定义骨架，子类实现差异步骤
 */
public abstract class AbstractImportService<T> {
    
    /**
     * 模板方法：导入流程固定
     */
    public final ImportResult importData(MultipartFile file) {
        log.info("[importData][开始导入，fileName={}]", file.getOriginalFilename());
        
        // 1. 解析文件（子类实现）
        List<T> dataList = parseFile(file);
        
        // 2. 校验数据（子类实现）
        ImportValidationResult validationResult = validateData(dataList);
        if (validationResult.hasError()) {
            return ImportResult.failure(validationResult.getErrors());
        }
        
        // 3. 保存数据（子类实现）
        int savedCount = saveData(dataList);
        
        // 4. 后置处理（钩子，子类可选实现）
        afterImport(dataList);
        
        log.info("[importData][导入完成，totalCount={}]", savedCount);
        return ImportResult.success(savedCount);
    }
    
    // 抽象方法：子类必须实现
    protected abstract List<T> parseFile(MultipartFile file);
    protected abstract ImportValidationResult validateData(List<T> dataList);
    protected abstract int saveData(List<T> dataList);
    
    // 钩子方法：子类可选实现
    protected void afterImport(List<T> dataList) {
        // 默认空实现
    }
}

// 子类实现
@Service
public class UserImportService extends AbstractImportService<UserImportVO> {
    
    @Override
    protected List<UserImportVO> parseFile(MultipartFile file) {
        return ExcelUtils.read(file, UserImportVO.class);
    }
    
    @Override
    protected ImportValidationResult validateData(List<UserImportVO> dataList) {
        // 用户特定校验逻辑
    }
    
    @Override
    protected int saveData(List<UserImportVO> dataList) {
        // 用户保存逻辑
    }
    
    @Override
    protected void afterImport(List<UserImportVO> dataList) {
        // 发送通知
        notificationService.notifyUserImportCompleted(dataList.size());
    }
}
```

### 观察者模式（Spring Event）

```java
// 定义事件
public class OrderCreatedEvent extends ApplicationEvent {
    
    private final Long orderId;
    private final Long userId;
    private final List<Long> productIds;
    
    public OrderCreatedEvent(Object source, Long orderId, Long userId, List<Long> productIds) {
        super(source);
        this.orderId = orderId;
        this.userId = userId;
        this.productIds = productIds;
    }
    
    // getters...
}

// 发布事件
@Service
public class OrderServiceImpl {
    
    @Resource
    private ApplicationEventPublisher eventPublisher;
    
    @Transactional(rollbackFor = Exception.class)
    public Long createOrder(OrderCreateReqVO reqVO) {
        OrderDO order = reqVO.toEntity();
        orderMapper.insert(order);
        
        // 发布事件（事务提交后处理）
        eventPublisher.publishEvent(new OrderCreatedEvent(
                this, order.getId(), order.getUserId(), productIds));
        
        return order.getId();
    }
}

// 监听事件（事务后执行）
@Component
@Slf4j
public class OrderEventListener {
    
    @Resource
    private InventoryService inventoryService;
    
    @Resource
    private NotificationService notificationService;
    
    @Resource
    private StatisticsService statisticsService;
    
    /**
     * 扣减库存
     */
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void onOrderCreatedForInventory(OrderCreatedEvent event) {
        log.info("[onOrderCreatedForInventory][扣减库存，orderId={}]", event.getOrderId());
        inventoryService.decreaseStock(event.getProductIds());
    }
    
    /**
     * 发送通知
     */
    @Async
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void onOrderCreatedForNotification(OrderCreatedEvent event) {
        log.info("[onOrderCreatedForNotification][发送通知，orderId={}]", event.getOrderId());
        notificationService.sendOrderCreatedNotification(event.getUserId(), event.getOrderId());
    }
    
    /**
     * 更新统计
     */
    @Async
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void onOrderCreatedForStatistics(OrderCreatedEvent event) {
        log.info("[onOrderCreatedForStatistics][更新统计，orderId={}]", event.getOrderId());
        statisticsService.incrementOrderCount(event.getUserId());
    }
}
```

---

## 六、DDD 概念映射

### 概念映射表

| DDD 概念 | 本项目映射 | 说明 |
|---------|-----------|------|
| **Entity（实体）** | DO | 有唯一标识，状态可变 |
| **Value Object（值对象）** | VO（部分） | 无标识，不可变 |
| **Aggregate（聚合）** | Service 方法边界 | 一致性边界，一起持久化 |
| **Aggregate Root（聚合根）** | 主 DO | 外部只能通过聚合根访问 |
| **Domain Service（领域服务）** | Helper/Manager 类 | 跨实体业务规则 |
| **Repository（仓储）** | Mapper（或 Repository 接口） | 持久化抽象 |
| **Application Service（应用服务）** | Service | 用例编排 |
| **Domain Event（领域事件）** | Event 类 + EventListener | 解耦副作用 |
| **Bounded Context（限界上下文）** | Module 模块 | 业务边界 |

### 聚合设计示例

```java
/**
 * 订单聚合：Order（聚合根）+ OrderItem
 * 一致性规则：订单和明细必须一起创建/删除
 */
@Service
public class OrderServiceImpl implements OrderService {
    
    @Resource
    private OrderMapper orderMapper;
    
    @Resource
    private OrderItemMapper orderItemMapper;
    
    @Resource
    private OrderPricingHelper orderPricingHelper;  // 领域服务
    
    /**
     * 创建订单（聚合内一致性）
     */
    @Transactional(rollbackFor = Exception.class)
    public Long createOrder(OrderCreateReqVO reqVO) {
        // 1. 构建聚合根
        OrderDO order = OrderDO.builder()
                .orderNo(generateOrderNo())
                .userId(reqVO.getUserId())
                .status(OrderStatusEnum.PENDING.getStatus())
                .build();
        
        // 2. 构建聚合内实体
        List<OrderItemDO> items = reqVO.getItems().stream()
                .map(this::buildOrderItem)
                .collect(Collectors.toList());
        
        // 3. 领域服务计算总价（跨实体规则）
        BigDecimal totalAmount = orderPricingHelper.calculateTotalPrice(items);
        order.setTotalAmount(totalAmount);
        
        // 4. 聚合内一致性：一起持久化
        orderMapper.insert(order);
        items.forEach(item -> item.setOrderId(order.getId()));
        orderItemMapper.insertBatch(items);
        
        // 5. 发布领域事件
        eventPublisher.publishEvent(new OrderCreatedEvent(
                this, order.getId(), order.getUserId(), items));
        
        return order.getId();
    }
    
    /**
     * 取消订单（聚合内一致性）
     */
    @Transactional(rollbackFor = Exception.class)
    public void cancelOrder(Long orderId) {
        // 1. 加载聚合
        OrderDO order = orderMapper.selectById(orderId);
        if (order == null) {
            throw exception(ORDER_NOT_EXISTS);
        }
        
        // 2. 状态校验
        if (!OrderStatusEnum.PENDING.matches(order.getStatus())) {
            throw exception(ORDER_STATUS_NOT_ALLOW_CANCEL);
        }
        
        // 3. 聚合内一致性：订单和明细一起删除
        order.setStatus(OrderStatusEnum.CANCELLED.getStatus());
        orderMapper.updateById(order);
        orderItemMapper.deleteByOrderId(orderId);
        
        // 4. 发布领域事件
        eventPublisher.publishEvent(new OrderCancelledEvent(this, orderId));
    }
}

/**
 * 领域服务：跨实体业务规则
 */
@Component
public class OrderPricingHelper {
    
    /**
     * 计算订单总价（跨 OrderItem 的业务规则）
     */
    public BigDecimal calculateTotalPrice(List<OrderItemDO> items) {
        if (CollUtil.isEmpty(items)) {
            return BigDecimal.ZERO;
        }
        
        return items.stream()
                .map(item -> item.getPrice().multiply(new BigDecimal(item.getQuantity())))
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
    
    /**
     * 计算折扣后价格（跨商品类型和用户等级）
     */
    public BigDecimal calculateDiscountedPrice(List<OrderItemDO> items, 
                                               UserTypeEnum userType) {
        BigDecimal subtotal = calculateTotalPrice(items);
        return userType.getDiscountStrategy().apply(subtotal);
    }
}
```

---

## 七、防御性编程

### 输入防御

```java
@Service
public class OrderServiceImpl implements OrderService {
    
    /**
     * 创建订单 - 输入防御示例
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public Long createOrder(OrderCreateReqVO reqVO) {
        // ── 1. 参数非空防御 ───────────────────────────
        Objects.requireNonNull(reqVO, "订单请求不能为空");
        
        // ── 2. 业务前置条件 ───────────────────────────
        Preconditions.checkArgument(reqVO.getUserId() != null && reqVO.getUserId() > 0,
                "用户ID必须为正数");
        
        Preconditions.checkArgument(CollUtil.isNotEmpty(reqVO.getItems()),
                "订单明细不能为空");
        
        // ── 3. 边界值校验 ─────────────────────────────
        Preconditions.checkArgument(reqVO.getItems().size() <= 100,
                "订单明细数量不能超过100");
        
        // ── 4. 关联数据校验 ───────────────────────────
        UserDO user = userService.getById(reqVO.getUserId())
                .orElseThrow(() -> exception(USER_NOT_EXISTS));
        
        Preconditions.checkState(UserStatusEnum.ENABLED.matches(user.getStatus()),
                "用户已被禁用");
        
        // ── 5. 业务规则校验 ───────────────────────────
        List<Long> productIds = reqVO.getItems().stream()
                .map(OrderItemReqVO::getProductId)
                .collect(Collectors.toList());
        
        Map<Long, ProductDO> productMap = productService.getProductMap(productIds);
        Preconditions.checkState(productMap.size() == productIds.size(),
                "部分商品不存在");
        
        // ── 核心业务逻辑 ──────────────────────────────
        OrderDO order = buildOrder(reqVO, user, productMap);
        orderMapper.insert(order);
        
        return order.getId();
    }
}
```

### 输出防御

```java
@Service
public class OrderServiceImpl implements OrderService {
    
    /**
     * 查询单条 - 输出防御
     */
    @Override
    public Optional<OrderDO> getOrder(Long id) {
        // 防御性返回：永不返回 null
        if (id == null || id <= 0) {
            return Optional.empty();
        }
        return Optional.ofNullable(orderMapper.selectById(id));
    }
    
    /**
     * 查询列表 - 输出防御
     */
    @Override
    public List<OrderDO> getOrdersByUserId(Long userId) {
        // 防御性返回：永不返回 null
        if (userId == null || userId <= 0) {
            return Collections.emptyList();
        }
        List<OrderDO> orders = orderMapper.selectByUserId(userId);
        return orders != null ? orders : Collections.emptyList();
    }
    
    /**
     * 查询分页 - 输出防御
     */
    @Override
    public PageResult<OrderDO> getOrderPage(OrderPageReqVO reqVO) {
        // 参数防御
        if (reqVO == null) {
            reqVO = new OrderPageReqVO();
        }
        if (reqVO.getPageNo() == null || reqVO.getPageNo() <= 0) {
            reqVO.setPageNo(1);
        }
        if (reqVO.getPageSize() == null || reqVO.getPageSize() <= 0) {
            reqVO.setPageSize(10);
        }
        
        PageResult<OrderDO> result = orderMapper.selectPage(reqVO);
        return result != null ? result : PageResult.empty();
    }
}
```

### 状态防御

```java
/**
 * 订单状态机（防御非法状态转换）
 */
@Getter
@AllArgsConstructor
public enum OrderStatusEnum {
    
    PENDING   (0, "待支付"),
    PAID      (1, "已支付"),
    SHIPPED   (2, "已发货"),
    COMPLETED (3, "已完成"),
    CANCELLED (4, "已取消");
    
    private final Integer status;
    private final String name;
    
    /**
     * 状态转换规则（防御非法转换）
     */
    private static final Map<OrderStatusEnum, Set<OrderStatusEnum>> ALLOWED_TRANSITIONS = Map.of(
            PENDING,   Set.of(PAID, CANCELLED),
            PAID,      Set.of(SHIPPED, CANCELLED),
            SHIPPED,   Set.of(COMPLETED),
            COMPLETED, Set.of(),
            CANCELLED, Set.of()
    );
    
    /**
     * 检查是否可以转换到目标状态
     */
    public boolean canTransitionTo(OrderStatusEnum target) {
        return ALLOWED_TRANSITIONS.getOrDefault(this, Set.of()).contains(target);
    }
    
    public static OrderStatusEnum of(Integer status) {
        return Arrays.stream(values())
                .filter(e -> e.status.equals(status))
                .findFirst()
                .orElse(null);
    }
}

// Service 中使用状态防御
@Service
public class OrderServiceImpl {
    
    @Override
    @Transactional(rollbackFor = Exception.class)
    public void payOrder(Long orderId) {
        OrderDO order = getOrder(orderId)
                .orElseThrow(() -> exception(ORDER_NOT_EXISTS));
        
        OrderStatusEnum currentStatus = OrderStatusEnum.of(order.getStatus());
        OrderStatusEnum targetStatus = OrderStatusEnum.PAID;
        
        // 状态防御：检查是否允许转换
        if (!currentStatus.canTransitionTo(targetStatus)) {
            log.warn("[payOrder][状态不允许支付，orderId={}, currentStatus={}]",
                    orderId, currentStatus);
            throw exception(ORDER_STATUS_NOT_ALLOW_PAY);
        }
        
        order.setStatus(targetStatus.getStatus());
        orderMapper.updateById(order);
    }
}
```

### 并发防御

```java
@Service
public class OrderServiceImpl {
    
    @Resource
    private RedissonClient redissonClient;
    
    /**
     * 支付订单 - 并发防御
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public void payOrder(Long orderId, PaymentReqVO reqVO) {
        String lockKey = "order:pay:" + orderId;
        RLock lock = redissonClient.getLock(lockKey);
        
        boolean acquired = false;
        try {
            // 分布式锁防御
            acquired = lock.tryLock(3, 30, TimeUnit.SECONDS);
            if (!acquired) {
                log.warn("[payOrder][获取锁失败，orderId={}]", orderId);
                throw exception(ORDER_PROCESSING);
            }
            
            // 执行支付逻辑
            doPayOrder(orderId, reqVO);
            
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw exception(ORDER_PAY_ERROR);
        } finally {
            if (acquired && lock.isHeldByCurrentThread()) {
                lock.unlock();
            }
        }
    }
    
    /**
     * 更新订单 - 乐观锁防御
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public void updateOrder(OrderUpdateReqVO reqVO) {
        OrderDO order = getOrder(reqVO.getId())
                .orElseThrow(() -> exception(ORDER_NOT_EXISTS));
        
        // 应用更新
        order.applyUpdate(reqVO);
        
        // 乐观锁更新（DO 中有 @Version 字段）
        boolean updated = orderMapper.updateById(order) > 0;
        if (!updated) {
            log.warn("[updateOrder][乐观锁冲突，orderId={}, version={}]",
                    order.getId(), order.getVersion());
            throw exception(CONCURRENT_UPDATE_CONFLICT);
        }
    }
}
```

---

## 八、架构决策指南

### 业务方法放哪里？

```
业务逻辑应该放在哪里？

┌─────────────────────────────────────────────────────┐
│ 是否仅依赖 DO 自身字段？                              │
│   ├─ 是 → DO 方法                                    │
│   │     示例：isEnabled(), isValid(), isExpired()    │
│   │                                                  │
│   └─ 否 → 是否需要查询其他数据？                      │
│           ├─ 是 → Service 方法                        │
│           │     示例：createOrder(), cancelOrder()   │
│           │                                          │
│           └─ 否 → 是否跨多个实体类型？                │
│                   ├─ 是 → Helper 类（领域服务）       │
│                   │     示例：OrderPricingHelper     │
│                   │                                  │
│                   └─ 否 → Service 方法               │
└─────────────────────────────────────────────────────┘
```

### 是否需要设计模式？

```
是否引入设计模式？

┌─────────────────────────────────────────────────────┐
│ 分支判断有几种？                                      │
│   ├─ 1-2 种 → 不引入，if-else 足够                   │
│   │                                                  │
│   └─ 3+ 种 → 策略模式 + 枚举                         │
│                                                      │
│ 创建逻辑是否复杂？                                    │
│   ├─ 简单（直接 new 或 Builder）→ 不引入            │
│   │                                                  │
│   └─ 复杂/可扩展 → 工厂模式                          │
│                                                      │
│ 流程是否固定但步骤可变？                              │
│   ├─ 是 → 模板方法模式                              │
│   │                                                  │
│   └─ 否 → 不引入                                    │
│                                                      │
│ 是否需要解耦后续动作？                                │
│   ├─ 是 → 观察者模式（Spring Event）                │
│   │                                                  │
│   └─ 否 → 直接调用                                  │
└─────────────────────────────────────────────────────┘
```

---

## 九、设计原则约束

### 约束总表

| ID | 规则 |
|----|------|
| C-DESIGN-001 | Service 方法职责单一，一个方法只做一件事 |
| C-DESIGN-002 | 分支判断超过 3 种时使用策略模式，禁止多层 if-else |
| C-DESIGN-003 | 重复代码出现 2 次以上必须提取公共方法或工具类 |
| C-DESIGN-004 | 仅依赖 DO 自身字段的方法放在 DO；需要外部依赖的放在 Service |
| C-DESIGN-005 | 跨多个实体的业务规则抽取到 Helper 类 |
| C-DESIGN-006 | 所有公共方法必须有输入防御（非空、边界值校验） |
| C-DESIGN-007 | 查询方法永不返回 null，单条用 Optional，列表用空集合 |
| C-DESIGN-008 | 状态变更必须有状态机校验，禁止非法状态转换 |
| C-DESIGN-009 | 依赖注入使用构造器注入，禁止 @Resource 字段注入（测试友好） |
| C-DESIGN-010 | 优先选择简单实现，避免过度抽象 |

---

## 十、设计原则自检清单

```
SOLID 原则：
□ Service 是否按职责拆分（查询/命令分离）？
□ 方法是否职责单一（一个方法做一件事）？
□ 分支判断是否用策略模式处理？
□ 是否依赖接口而非具体实现？

DRY 原则：
□ 是否有重复代码（相同逻辑出现 2 次）？
□ 公共逻辑是否提取到工具类或基类？
□ 是否有硬编码的魔法数字/字符串？

KISS 原则：
□ 是否有过度设计的抽象层？
□ 能否用更简单的方式实现？
□ 设计模式是否真的有必要？

设计模式：
□ 策略模式：3+ 种分支判断是否用枚举+策略？
□ 工厂模式：创建逻辑是否可扩展？
□ 模板方法：固定流程是否抽取骨架？
□ 观察者：副作用是否解耦？

DDD 概念：
□ 聚合内一致性是否保证？
□ 跨实体规则是否抽取到 Helper？
□ 领域事件是否用于解耦？

防御性编程：
□ 输入是否做非空、边界值校验？
□ 输出是否永不返回 null？
□ 状态转换是否合法？
□ 并发场景是否有锁保护？
```