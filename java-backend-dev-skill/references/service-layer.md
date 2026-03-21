# Service 层最佳实践参考

> 按需加载。适用场景：事务、Spring Cache、并发、日志、幂等、定时任务、外部服务调用。

---

## 一、日志规范（C-CODE-006）

### 格式标准

```java
// 固定格式：[方法名][业务描述，key=value]

// INFO：关键业务节点
log.info("[create{Entity}][开始创建，name={}]", reqVO.getName());
log.info("[create{Entity}][创建成功，id={}]", entity.getId());

// WARN：业务预期内的拒绝/跳过
log.warn("[create{Entity}][名称已存在，跳过，name={}]", name);

// ERROR：非预期异常（必须携带 Throwable，C-CODE-003）
try {
    externalService.call(param);
} catch (Exception e) {
    log.error("[callExternal][调用失败，param={}]", param, e); // e 放最后！
    throw exception(EXTERNAL_SERVICE_ERROR);
}

// DEBUG：排查用，生产关闭
log.debug("[selectPage][查询条件，reqVO={}]", JsonUtils.toJsonString(reqVO));
```

### 关键分支必须打日志

```java
public void processPayment(Long orderId) {
    log.info("[processPayment][开始处理，orderId={}]", orderId);
    
    // ✅ 每个重要分支打日志
    if (OrderStatusEnum.PAID.matches(order.getStatus())) {
        log.warn("[processPayment][订单已支付，幂等返回，orderId={}]", orderId);
        return;
    }
    if (OrderStatusEnum.CANCELLED.matches(order.getStatus())) {
        log.warn("[processPayment][订单已取消，拒绝支付，orderId={}]", orderId);
        throw exception(ORDER_ALREADY_CANCELLED);
    }
    
    doProcess(order);
    log.info("[processPayment][处理完成，orderId={}]", orderId);
}
```

### 禁止打印敏感信息

```java
// ❌ 禁止打印密码、手机号明文
log.info("用户信息：{}", userDO);  // userDO 含 password

// ✅ 脱敏打印
log.info("[login][用户登录，mobile={}]", StrUtil.hide(user.getMobile(), 3, 7));
```

---

## 二、Spring 事务规范

### 基本规则

```java
// ✅ 写操作：必须指定 rollbackFor
@Transactional(rollbackFor = Exception.class)
public Long create{Entity}({Entity}SaveReqVO reqVO) { ... }

// ✅ 纯读操作：不加事务
public PageResult<{Entity}DO> get{Entity}Page({Entity}PageReqVO reqVO) {
    return {entity}Mapper.selectPage(reqVO);
}

// ❌ private 方法加 @Transactional（AOP 不生效）
// ❌ this 调用（绕过 AOP 代理）
public void methodA() { this.methodB(); }  // 事务不生效！

// ✅ 自注入走代理（最后手段）
@Resource
private {Entity}ServiceImpl self;
public void methodA() { self.methodB(); }
```

### 长事务防范

```java
// ❌ 事务内含耗时外部调用
@Transactional(rollbackFor = Exception.class)
public void create{Entity}WithNotify({Entity}SaveReqVO reqVO) {
    {entity}Mapper.insert(entity);
    httpClient.notify(entity.getId()); // 可能耗时数秒！
}

// ✅ TransactionalEventListener：事务提交后处理
@Transactional(rollbackFor = Exception.class)
public void create{Entity}({Entity}SaveReqVO reqVO) {
    {entity}Mapper.insert(entity);
    applicationContext.publishEvent(new {Entity}CreatedEvent(entity.getId()));
}

@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
public void on{Entity}Created({Entity}CreatedEvent event) {
    {entity}Client.notify(event.getId()); // 事务外，不影响主链路
}
```

---

## 三、Spring Cache

### 缓存注解使用

```java
@Service
public class {Entity}ServiceImpl {

    /**
     * 查询单条 - 直接在方法上加 @Cacheable
     * 命中缓存直接返回，未命中执行方法并回填
     */
    @Cacheable(value = "{module}:{entity}:info", key = "#id", unless = "#result == null")
    public Optional<{Entity}DO> get{Entity}OrElse(Long id) {
        return Optional.ofNullable({entity}Mapper.selectById(id));
    }

    /**
     * 分页查询 - 列表缓存
     */
    @Cacheable(value = "{module}:{entity}:page", key = "#reqVO.hashCode()", unless = "#result.list.isEmpty()")
    public PageResult<{Entity}DO> get{Entity}Page({Entity}PageReqVO reqVO) {
        return {entity}Mapper.selectPage(reqVO);
    }

    /**
     * 更新后清除缓存（删而不更，防并发写脏数据）
     */
    @Transactional(rollbackFor = Exception.class)
    @CacheEvict(value = "{module}:{entity}:info", key = "#reqVO.id")
    public void update{Entity}({Entity}SaveReqVO reqVO) {
        // ...
    }

    /**
     * 删除后清除缓存
     */
    @Transactional(rollbackFor = Exception.class)
    @CacheEvict(value = "{module}:{entity}:info", key = "#id")
    public void delete{Entity}(Long id) {
        // ...
    }

    /**
     * 批量清除列表缓存
     */
    @CacheEvict(value = "{module}:{entity}:page", allEntries = true)
    public void evict{Entity}PageCache() { }
}
```

### 缓存配置

```java
@Configuration
@EnableCaching
public class RedisCacheConfig {

    @Bean
    public CacheManager cacheManager(RedisConnectionFactory factory) {
        RedisCacheConfiguration defaultConfig = RedisCacheConfiguration
                .defaultCacheConfig()
                .entryTtl(Duration.ofHours(1))
                .serializeValuesWith(RedisSerializationContext.SerializationPair
                        .fromSerializer(new GenericJackson2JsonRedisSerializer()))
                .disableCachingNullValues();

        // 按 cacheNames 定制 TTL
        Map<String, RedisCacheConfiguration> configMap = new HashMap<>();
        configMap.put("{module}:{entity}:info", defaultConfig.entryTtl(Duration.ofHours(2)));

        return RedisCacheManager.builder(factory)
                .cacheDefaults(defaultConfig)
                .withInitialCacheConfigurations(configMap)
                .build();
    }
}
```

---

## 四、并发控制

### 分布式锁（Redisson）

```java
@Resource
private RedissonClient redissonClient;

public void processPayment(Long orderId) {
    String lockKey = "{project}:order:pay:" + orderId;
    RLock lock = redissonClient.getLock(lockKey);
    boolean acquired = false;
    try {
        acquired = lock.tryLock(3, 30, TimeUnit.SECONDS);  // 等3s，持锁30s
        if (!acquired) {
            log.warn("[processPayment][正在处理中，orderId={}]", orderId);
            throw exception(ORDER_PROCESSING);
        }
        doProcessPayment(orderId);
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
        throw exception(ORDER_PROCESS_ERROR);
    } finally {
        if (acquired && lock.isHeldByCurrentThread()) {
            lock.unlock();
        }
    }
}
```

### 接口幂等

```java
public void submitOrder(String idempotentToken, {Entity}SaveReqVO reqVO) {
    String key = "{project}:idempotent:{entity}:" + idempotentToken;
    Boolean isFirst = RedisUtils.setIfAbsent(key, "1", Duration.ofMinutes(10));
    if (!Boolean.TRUE.equals(isFirst)) {
        log.warn("[submitOrder][重复提交，token={}]", idempotentToken);
        throw exception(ORDER_SUBMITTED_DUPLICATE);
    }
    create{Entity}(reqVO);
}
```

---

## 五、定时任务（Quartz）

### Job 实现

```java
@Component
@DisallowConcurrentExecution  // 分布式防重
@Slf4j
public class {Entity}SyncJob implements Job {

    @Resource
    private {Entity}Service {entity}Service;

    @Override
    public void execute(JobExecutionContext context) throws JobExecutionException {
        log.info("[{Entity}SyncJob][开始执行]");
        try {
            {entity}Service.sync{Entity}();
            log.info("[{Entity}SyncJob][执行完成]");
        } catch (Exception e) {
            log.error("[{Entity}SyncJob][执行异常]", e);
            throw new JobExecutionException(e);
        }
    }
}
```

### Job 配置

```java
@Configuration
public class {Module}JobConfig {

    @Bean
    public JobDetail {entity}SyncJobDetail() {
        return JobBuilder.newJob({Entity}SyncJob.class)
                .withIdentity("{entity}SyncJob", "{module}")
                .storeDurably()
                .build();
    }

    @Bean
    public Trigger {entity}SyncTrigger(JobDetail {entity}SyncJobDetail) {
        return TriggerBuilder.newTrigger()
                .forJob({entity}SyncJobDetail)
                .withSchedule(CronScheduleBuilder.cronSchedule("0 0 2 * * ?")
                        .withMisfireHandlingInstructionDoNothing())
                .build();
    }
}
```

---

## 六、外部服务调用（{Entity}Client，C-ARCH-007）

### Client 类

```java
@Component
@Slf4j
public class {Entity}Client {

    @Resource
    private RestTemplate restTemplate;

    @Value("${dainthub.client.{entity}.base-url}")
    private String baseUrl;

    /**
     * 查询外部资源，404 返回 Optional.empty()
     */
    public Optional<{Entity}DTO> get{Entity}(Long id) {
        String url = baseUrl + "/{entity}/" + id;
        log.info("[get{Entity}][请求，id={}, url={}]", id, url);
        try {
            ResponseEntity<{Entity}DTO> response = restTemplate.getForEntity(url, {Entity}DTO.class);
            return Optional.ofNullable(response.getBody());
        } catch (HttpClientErrorException.NotFound e) {
            log.warn("[get{Entity}][外部资源不存在，id={}]", id);
            return Optional.empty();
        } catch (Exception e) {
            log.error("[get{Entity}][调用失败，id={}]", id, e);
            throw exception(EXTERNAL_{ENTITY}_SERVICE_ERROR);
        }
    }

    /**
     * 通知外部系统
     */
    public void notify{Entity}({Entity}NotifyDTO notifyDTO) {
        log.info("[notify{Entity}][发送通知，id={}]", notifyDTO.getId());
        try {
            restTemplate.postForEntity(baseUrl + "/{entity}/notify", notifyDTO, Void.class);
        } catch (Exception e) {
            log.error("[notify{Entity}][通知失败]", e);
            throw exception(EXTERNAL_{ENTITY}_NOTIFY_ERROR);
        }
    }
}
```

### DTO 规范

```java
/**
 * 外部服务 DTO，字段与外部系统一致
 */
@Data
public class {Entity}DTO {
    private String externalId;
    private String name;
    private Integer status;

    /** 转换为内部 DO（C-ARCH-003） */
    public {Entity}DO toEntity() {
        {Entity}DO entity = new {Entity}DO();
        entity.setName(this.name);
        entity.setStatus(this.status);
        return entity;
    }
}
```

---

## 七、异步与线程池

```java
// ❌ 禁止直接 new Thread() 或 Executors 无界队列

// ✅ @Async + 命名线程池
@Async("commonExecutor")
public CompletableFuture<Void> asyncNotify(Long id) {
    {entity}Client.notify{Entity}(new {Entity}NotifyDTO(id, "CREATED"));
    return CompletableFuture.completedFuture(null);
}

// ✅ CompletableFuture 并行执行
CompletableFuture<UserDO> userFuture = 
        CompletableFuture.supplyAsync(() -> userService.getUser(userId), executor);
CompletableFuture<List<OrderDO>> orderFuture = 
        CompletableFuture.supplyAsync(() -> orderService.getUserOrders(userId), executor);

CompletableFuture.allOf(userFuture, orderFuture).join();
UserDO user = userFuture.get();
List<OrderDO> orders = orderFuture.get();
```

---

## 八、性能验证

### EXPLAIN 结果解读

| 字段 | 关注点 | 优化建议 |
|------|-------|---------|
| **type** | ALL=全表扫描 | 避免 ALL，争取 range 及以上 |
| **key** | 实际使用的索引 | NULL 表示未走索引 |
| **rows** | 预估扫描行数 | 越小越好，理想值 < 1000 |
| **Extra** | filesort/temporary | 避免 |

```sql
-- ✅ 良好的执行计划
-- type: ref，key: idx_status，rows: 100

-- ❌ 需要优化
-- type: ALL，key: NULL，rows: 1000000，Extra: Using filesort
```

### 慢查询分析

```sql
-- 开启慢查询日志
slow_query_log = 1
long_query_time = 1  -- 超过 1 秒记录

-- 分析慢查询日志
mysqldumpslow -s t /var/log/mysql/slow.log | head -20
```

---

## 九、自检清单

```
事务：
□ 写操作有 @Transactional(rollbackFor = Exception.class)
□ 纯读操作无事务
□ 事务方法为 public
□ 无 this 内部调用
□ 事务内无耗时外部调用

日志：
□ 写操作入口/完成有 INFO 日志
□ 业务拒绝分支有 WARN 日志
□ catch 中 ERROR 日志，Throwable 放最后
□ 无敏感信息明文

缓存：
□ 热点查询加 @Cacheable
□ 写后 @CacheEvict
□ unless = "#result == null" 防穿透

并发：
□ 共享资源有分布式锁
□ 幂等接口有 Redis Token
□ 定时任务有 @DisallowConcurrentExecution

外部调用：
□ 封装在 {Entity}Client
□ 404 返回 Optional.empty()
□ 有超时配置
```