# Spring Boot / Redis / 并发 / 任务调度 / 外部调用最佳实践参考

> 按需加载。适用场景：事务、Spring Cache、并发、日志、幂等、线程池、定时任务、外部服务调用。

---

## 一、日志规范（C-CODE-006）

### 格式标准

```java
// 固定格式：[方法名][业务描述，key=value]
// 必须携带主要业务参数，便于生产排查

// INFO：关键业务节点（方法入口、操作成功）
log.info("[create{Entity}][开始创建，name={}]", reqVO.getName());
log.info("[create{Entity}][创建成功，id={}]", entity.getId());

// WARN：业务预期内的拒绝/跳过（重复提交、资源不足、状态不符）
log.warn("[create{Entity}][名称已存在，跳过，name={}]", name);
log.warn("[deductStock][库存不足，productId={}, required={}, available={}]",
        productId, required, stock);

// ERROR：非预期异常（必须携带 Throwable 保留堆栈，C-CODE-003）
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

    OrderDO order = get{Entity}OrElse(orderId)
            .orElseThrow(() -> exception(ORDER_NOT_EXISTS));

    // ✅ 每个重要分支打日志（C-CODE-006）
    if (OrderStatusEnum.PAID.matches(order.getStatus())) {
        log.warn("[processPayment][订单已支付，幂等返回，orderId={}]", orderId);
        return;
    }
    if (OrderStatusEnum.CANCELLED.matches(order.getStatus())) {
        log.warn("[processPayment][订单已取消，拒绝支付，orderId={}]", orderId);
        throw exception(ORDER_ALREADY_CANCELLED);
    }

    doProcess(order);
    log.info("[processPayment][处理完成，orderId={}, status={}]",
            orderId, order.getStatus());
}
```

### 禁止打印敏感信息

```java
// ❌ 禁止打印密码、手机号明文、银行卡号
log.info("用户信息：{}", userDO);  // userDO 含 password

// ✅ 脱敏打印（Hutool StrUtil.hide，C-CODE-004）
log.info("[login][用户登录，userId={}, mobile={}]",
        user.getId(), StrUtil.hide(user.getMobile(), 3, 7));
```

---

## 二、Spring 事务规范

### 基本规则

```java
// ✅ 写操作：必须指定 rollbackFor（默认只回滚 RuntimeException）
@Transactional(rollbackFor = Exception.class)
public Long create{Entity}({Entity}SaveReqVO reqVO) { ... }

// ✅ 纯读操作：不加事务（减少数据库连接占用）
public PageResult<{Entity}DO> get{Entity}Page({Entity}PageReqVO reqVO) {
    return {entity}Mapper.selectPage(reqVO);
}

// ❌ private 方法加 @Transactional（AOP 代理不生效）
@Transactional
private void doSomething() { }

// ❌ this 调用（绕过 AOP 代理）
public void methodA() {
    this.methodB();  // 事务不生效！
}

// ✅ 自注入走代理（最后手段，优先拆 Service）
@Resource
private {Entity}ServiceImpl self;
public void methodA() { self.methodB(); }
```

### 长事务防范

```java
// ❌ 事务内含耗时外部调用（HTTP/MQ/文件 IO）→ 长事务
@Transactional(rollbackFor = Exception.class)
public void create{Entity}WithNotify({Entity}SaveReqVO reqVO) {
    {entity}Mapper.insert(entity);
    httpClient.notify(entity.getId()); // 可能耗时数秒！
}

// ✅ TransactionalEventListener：事务提交后异步处理（C-ARCH-007 配合 Client）
@Transactional(rollbackFor = Exception.class)
public void create{Entity}({Entity}SaveReqVO reqVO) {
    {entity}Mapper.insert(entity);
    applicationContext.publishEvent(new {Entity}CreatedEvent(entity.getId()));
    log.info("[create{Entity}][入库成功，发布事件，id={}]", entity.getId());
}

@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
public void on{Entity}Created({Entity}CreatedEvent event) {
    log.info("[on{Entity}Created][收到事件，id={}]", event.getId());
    {entity}Client.notify(event.getId()); // 事务外，不影响主链路
}
```

---

## 三、Spring Cache（缓存规范，req 4）

### 配置 Redis 作为缓存底层

```java
// 在 framework 层或模块 config 中统一配置
@Configuration
@EnableCaching
public class RedisCacheConfig {

    @Bean
    public CacheManager cacheManager(RedisConnectionFactory factory) {
        // 默认缓存配置
        RedisCacheConfiguration defaultConfig = RedisCacheConfiguration
                .defaultCacheConfig()
                .entryTtl(Duration.ofHours(1))
                // 使用 JsonUtils 序列化（C-CODE-005），可读性好、支持泛型
                .serializeValuesWith(RedisSerializationContext.SerializationPair
                        .fromSerializer(new GenericJackson2JsonRedisSerializer()))
                .disableCachingNullValues();

        // 按 cacheNames 定制不同 TTL
        Map<String, RedisCacheConfiguration> configMap = new HashMap<>();
        configMap.put("{module}:{entity}:info",
                defaultConfig.entryTtl(Duration.ofHours(2)));
        configMap.put("{module}:{entity}:list",
                defaultConfig.entryTtl(Duration.ofMinutes(30)));

        return RedisCacheManager.builder(factory)
                .cacheDefaults(defaultConfig)
                .withInitialCacheConfigurations(configMap)
                .build();
    }
}
```

### 缓存注解使用规范

```java
@Service
@Slf4j
public class {Entity}ServiceImpl implements {Entity}Service {

    /**
     * 从缓存获取单条实体（C-CODE-006：命名 get{Entity}FromCache）
     * @Cacheable：命中缓存直接返回，未命中执行方法并回填
     */
    @Cacheable(value = "{module}:{entity}:info", key = "#id",
               unless = "#result == null")  // null 值不缓存，防穿透
    public {Entity}DO get{Entity}FromCache(Long id) {
        log.debug("[get{Entity}FromCache][缓存未命中，查 DB，id={}]", id);
        return {entity}Mapper.selectById(id);
    }

    /**
     * 更新后清除缓存（删而不更，防并发写脏数据）
     * @CacheEvict：方法执行成功后删除对应缓存
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    @CacheEvict(value = "{module}:{entity}:info", key = "#reqVO.id")
    public void update{Entity}({Entity}SaveReqVO reqVO) {
        log.info("[update{Entity}][开始更新，id={}]", reqVO.getId());
        {Entity}DO entity = get{Entity}OrElse(reqVO.getId())
                .orElseThrow(() -> exception({ENTITY}_NOT_EXISTS));
        if (exist{Entity}Name(reqVO.getId(), reqVO.getName())) {
            throw exception({ENTITY}_NAME_DUPLICATE);
        }
        entity.applyUpdate(reqVO);
        {entity}Mapper.updateById(entity);
        log.info("[update{Entity}][更新成功，id={}]", entity.getId());
    }

    /**
     * 删除后清除缓存
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    @CacheEvict(value = "{module}:{entity}:info", key = "#id")
    public void delete{Entity}(Long id) {
        log.info("[delete{Entity}][开始删除，id={}]", id);
        get{Entity}OrElse(id).orElseThrow(() -> exception({ENTITY}_NOT_EXISTS));
        {entity}Mapper.deleteById(id);
        log.info("[delete{Entity}][删除成功，id={}]", id);
    }

    /**
     * 缓存列表（不常变化的枚举类数据适用）
     * @CacheEvict(allEntries = true) 用于批量清除同 value 下所有缓存
     */
    @Cacheable(value = "{module}:{entity}:list", key = "#status")
    public List<{Entity}DO> get{Entity}ListByStatus(Integer status) {
        return {entity}Mapper.selectListByStatus(status);
    }

    @CacheEvict(value = "{module}:{entity}:list", allEntries = true)
    public void evict{Entity}ListCache() {
        log.info("[evict{Entity}ListCache][清除列表缓存]");
    }
}
```

### 缓存防穿透（大量无效 key 请求）

```java
// ✅ unless = "#result == null" 避免缓存 null（@Cacheable 内置）
@Cacheable(value = "{module}:{entity}:info", key = "#id", unless = "#result == null")
public {Entity}DO get{Entity}FromCache(Long id) { ... }

// ✅ 布隆过滤器（高并发场景，Spring Cache 不内置，需单独实现）
// 在 Service 入口提前过滤必然不存在的 id
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
        // tryLock：等待 3s，持锁 30s（C-CODE-003：不用 RuntimeException）
        acquired = lock.tryLock(3, 30, TimeUnit.SECONDS);
        if (!acquired) {
            log.warn("[processPayment][正在处理中，orderId={}]", orderId);
            throw exception(ORDER_PROCESSING);
        }
        log.info("[processPayment][获取锁，orderId={}]", orderId);
        doProcessPayment(orderId);
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
        log.error("[processPayment][等待锁中断，orderId={}]", orderId, e);
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
// ✅ Redis Token（原子 setIfAbsent）
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

### 原子操作

```java
// ✅ 库存原子扣减（详见 data-layer.md）
int rows = productMapper.decreaseStock(id, quantity);
if (rows == 0) {
    throw exception(PRODUCT_STOCK_NOT_ENOUGH); // C-CODE-003
}
```

---

## 五、定时任务（Quartz）

### Job 实现

```java
package com.dainthub.{project}.module.{module}.job;

import org.quartz.DisallowConcurrentExecution;
import org.quartz.Job;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;

/**
 * {entity} 数据同步定时任务
 * @DisallowConcurrentExecution：Quartz 内置分布式防重（同一 Job 同一时刻只执行一次）
 */
@Component
@DisallowConcurrentExecution
@Slf4j
public class {Entity}SyncJob implements Job {

    @Resource
    private {Entity}Service {entity}Service;

    @Override
    public void execute(JobExecutionContext context) throws JobExecutionException {
        log.info("[{Entity}SyncJob][开始执行，fireTime={}]",
                LocalDateTimeUtil.format(LocalDateTimeUtil.of(context.getFireTime()),
                        DatePattern.NORM_DATETIME_PATTERN));
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

### Job 配置（Trigger + JobDetail）

```java
package com.dainthub.{project}.module.{module}.config;

@Configuration
public class {Module}JobConfig {

    /**
     * JobDetail：定义 Job 的元数据（storeDurably=true 使 Job 在无 Trigger 时也保留）
     */
    @Bean
    public JobDetail {entity}SyncJobDetail() {
        return JobBuilder.newJob({Entity}SyncJob.class)
                .withIdentity("{entity}SyncJob", "{module}")
                .withDescription("{entity} 数据同步任务")
                .storeDurably()
                .build();
    }

    /**
     * Trigger：定义触发规则
     * 示例：每天凌晨 2 点执行
     */
    @Bean
    public Trigger {entity}SyncTrigger(JobDetail {entity}SyncJobDetail) {
        return TriggerBuilder.newTrigger()
                .forJob({entity}SyncJobDetail)
                .withIdentity("{entity}SyncTrigger", "{module}")
                .withSchedule(CronScheduleBuilder.cronSchedule("0 0 2 * * ?")
                        .withMisfireHandlingInstructionDoNothing()) // 错过不补偿
                .build();
    }
}
```

---

## 六、外部服务调用（{Entity}Client，C-ARCH-007）

### Client 类规范

```java
package com.dainthub.{project}.module.{module}.client;

/**
 * {entity} 外部服务调用客户端。
 * 所有外部 HTTP/RPC 调用封装在此，Service 层只调用此接口，
 * 不直接使用 RestTemplate/WebClient（C-ARCH-007）。
 */
@Component
@Slf4j
public class {Entity}Client {

    @Resource
    private RestTemplate restTemplate;  // 或 WebClient、Feign Client

    @Value("${dainthub.client.{entity}.base-url}")
    private String baseUrl;

    /**
     * 查询外部 {entity} 信息
     *
     * @param id 外部系统的 ID
     * @return Optional.empty() 表示外部资源不存在（非异常）
     */
    public Optional<{Entity}DTO> get{Entity}(Long id) {
        String url = baseUrl + "/{entity}/" + id;
        log.info("[{Entity}Client][get{Entity}][请求外部服务，id={}, url={}]", id, url);
        try {
            ResponseEntity<{Entity}DTO> response =
                    restTemplate.getForEntity(url, {Entity}DTO.class);
            log.info("[{Entity}Client][get{Entity}][调用成功，id={}, status={}]",
                    id, response.getStatusCode());
            return Optional.ofNullable(response.getBody());
        } catch (HttpClientErrorException.NotFound e) {
            // 404 不是异常，是正常的"不存在"语义（C-CODE-003：不抛 RuntimeException）
            log.warn("[{Entity}Client][get{Entity}][外部资源不存在，id={}]", id);
            return Optional.empty();
        } catch (Exception e) {
            log.error("[{Entity}Client][get{Entity}][调用失败，id={}, url={}]", id, url, e);
            throw exception(EXTERNAL_{ENTITY}_SERVICE_ERROR);  // C-CODE-003
        }
    }

    /**
     * 通知外部系统（带重试机制）
     * 参数超 3 个时封装为 DTO（C-CODE-007）
     */
    public void notify{Entity}({Entity}NotifyDTO notifyDTO) {
        log.info("[{Entity}Client][notify{Entity}][发送通知，id={}, type={}]",
                notifyDTO.getId(), notifyDTO.getType());
        try {
            restTemplate.postForEntity(baseUrl + "/{entity}/notify",
                    notifyDTO, Void.class);
            log.info("[{Entity}Client][notify{Entity}][通知成功，id={}]", notifyDTO.getId());
        } catch (Exception e) {
            log.error("[{Entity}Client][notify{Entity}][通知失败，id={}]",
                    notifyDTO.getId(), e);
            throw exception(EXTERNAL_{ENTITY}_NOTIFY_ERROR);
        }
    }
}
```

### DTO 规范（外部服务数据结构）

```java
package com.dainthub.{project}.module.{module}.client.dto;

/**
 * {entity} 外部服务响应 DTO。
 * 注意：DTO 字段与外部系统保持一致，不受内部 DO 字段规范约束。
 * 内部使用时需在 Service 层转换为 DO 或 VO。
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class {Entity}DTO {

    /** 外部系统主键（可能与内部 id 不同） */
    private String externalId;

    private String name;
    private Integer status;

    /** 转换为内部 DO（转换方法在 DTO 中，C-ARCH-003） */
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
new Thread(() -> doSomething()).start();

// ✅ @Async + 命名线程池
@Async("commonExecutor")
public CompletableFuture<Void> asyncNotify(Long id) {
    log.info("[asyncNotify][异步通知，id={}]", id);
    {entity}Client.notify{Entity}(new {Entity}NotifyDTO(id, "CREATED"));
    return CompletableFuture.completedFuture(null);
}

// ✅ CompletableFuture 并行执行独立任务
CompletableFuture<UserDO>        userFuture  =
        CompletableFuture.supplyAsync(() -> userService.getUser(userId), executor);
CompletableFuture<List<OrderDO>> orderFuture =
        CompletableFuture.supplyAsync(() -> orderService.getUserOrders(userId), executor);
try {
    CompletableFuture.allOf(userFuture, orderFuture).join();
    UserDO user       = userFuture.get();
    List<OrderDO> orders = orderFuture.get();
    log.info("[buildDetail][并行查询完成，userId={}, orderCount={}]",
            userId, orders.size());
} catch (ExecutionException e) {
    log.error("[buildDetail][并行查询异常，userId={}]", userId, e);
    throw exception(BUILD_DETAIL_ERROR);
}
```

---

## 八、性能自检清单

```
事务层：
□ 写操作有 @Transactional(rollbackFor = Exception.class)
□ 纯读操作无事务
□ 事务方法为 public（非 private）
□ 无 this 内部调用事务方法
□ 事务内无 HTTP/MQ/文件 IO 等耗时外部调用

日志层：
□ 写操作入口 INFO 日志，携带关键参数
□ 写操作完成 INFO 日志，携带主键
□ 业务拒绝分支 WARN 日志
□ catch 中 ERROR 日志，Throwable 放最后
□ 无敏感信息明文（密码、手机号等）
□ 无 C-CODE-003 违规（无 RuntimeException）

缓存层：
□ 热点查询加 @Cacheable
□ 写后 @CacheEvict，删而不更
□ unless = "#result == null" 防穿透
□ cacheNames 在 RedisCacheConfig 中定制 TTL

并发层：
□ 共享资源有分布式锁或原子操作
□ 幂等接口有 Redis Token
□ 定时任务有 @DisallowConcurrentExecution

外部调用层：
□ 所有外部调用封装在 {Entity}Client（C-ARCH-007）
□ 404 返回 Optional.empty()，非异常
□ 有超时配置（RestTemplate connectTimeout / readTimeout）
□ 日志携带 url 和业务参数
```

---

## 九、性能验证模板

### EXPLAIN 结果解读

```sql
-- 执行计划分析
EXPLAIN SELECT id, name, status FROM {module}_{entity}
WHERE status = 1 AND create_time >= '2024-01-01' ORDER BY id DESC LIMIT 100;

-- 关键指标解读
```

| 字段 | 关注点 | 优化建议 |
|------|-------|---------|
| **type** | ALL=全表扫描，index=索引扫描，range=范围扫描，ref=索引查找，const=常量 | 避免 ALL，争取 range 及以上 |
| **key** | 实际使用的索引 | NULL 表示未走索引 |
| **rows** | 预估扫描行数 | 越小越好，理想值 < 1000 |
| **Extra** | Using filesort=额外排序，Using temporary=临时表 | 避免 filesort 和 temporary |

```sql
-- ✅ 良好的执行计划
-- type: ref，key: idx_status，rows: 100，Extra: NULL

-- ❌ 需要优化的执行计划
-- type: ALL，key: NULL，rows: 1000000，Extra: Using where; Using filesort
```

### 索引效果验证

```sql
-- 强制使用索引测试
SELECT id, name FROM {module}_{entity} FORCE INDEX (idx_create_time)
WHERE create_time >= '2024-01-01';

-- 禁用索引测试（对比性能）
SELECT id, name FROM {module}_{entity} IGNORE INDEX (idx_create_time)
WHERE create_time >= '2024-01-01';

-- 查看索引基数（区分度）
SHOW INDEX FROM {module}_{entity};

-- Cardinality 越高，索引效果越好
-- Cardinality / 总行数 > 0.1 表示区分度良好
```

### 缓存效果验证

```java
/**
 * 缓存命中率监控
 */
@Component
@Slf4j
public class CacheMonitor {

    @Resource
    private RedisTemplate<String, Object> redisTemplate;

    /**
     * 检查缓存命中率
     */
    public void checkCacheHitRate(String cacheName) {
        // Redis INFO 命令获取统计
        Properties info = redisTemplate.getRequiredConnectionFactory()
                .getConnection().serverCommands().info("stats");

        long hits = Long.parseLong(info.getProperty("keyspace_hits", "0"));
        long misses = Long.parseLong(info.getProperty("keyspace_misses", "0"));
        long total = hits + misses;

        double hitRate = total > 0 ? (double) hits / total * 100 : 0;

        log.info("[checkCacheHitRate][缓存命中率={}%，hits={}，misses={}]",
                String.format("%.2f", hitRate), hits, misses);

        // 命中率低于 80% 需要优化
        if (hitRate < 80) {
            log.warn("[checkCacheHitRate][缓存命中率过低，建议检查缓存策略]");
        }
    }
}
```

### 慢查询分析

```sql
-- 开启慢查询日志（MySQL 配置）
slow_query_log = 1
long_query_time = 1  -- 超过 1 秒记录
slow_query_log_file = /var/log/mysql/slow.log

-- 分析慢查询日志
mysqldumpslow -s t /var/log/mysql/slow.log | head -20

-- 常见慢查询模式
-- 1. 全表扫描：type=ALL
-- 2. 索引失效：key=NULL
-- 3. 大结果集：rows 过大
-- 4. 额外排序：Using filesort
-- 5. 临时表：Using temporary
```

### 性能基准测试

```java
/**
 * 性能基准测试（简单版）
 */
@Test
@DisplayName("性能基准 - 分页查询响应时间")
void performanceBenchmark_pageQuery() {
    // 准备测试数据
    {Entity}PageReqVO reqVO = new {Entity}PageReqVO();
    reqVO.setPageNo(1);
    reqVO.setPageSize(20);

    // 预热（JIT 编译）
    for (int i = 0; i < 5; i++) {
        {entity}Service.get{Entity}Page(reqVO);
    }

    // 正式测试
    int iterations = 100;
    long totalTime = 0;
    long maxTime = 0;
    long minTime = Long.MAX_VALUE;

    for (int i = 0; i < iterations; i++) {
        long start = System.currentTimeMillis();
        {entity}Service.get{Entity}Page(reqVO);
        long elapsed = System.currentTimeMillis() - start;

        totalTime += elapsed;
        maxTime = Math.max(maxTime, elapsed);
        minTime = Math.min(minTime, elapsed);
    }

    double avgTime = (double) totalTime / iterations;

    log.info("性能测试结果：平均={}ms，最大={}ms，最小={}ms",
            String.format("%.2f", avgTime), maxTime, minTime);

    // 性能基准：分页查询平均响应 < 100ms
    assertThat(avgTime).isLessThan(100.0);
}
```

### 性能优化验证流程

```
1. 问题发现
   □ 慢查询日志告警
   □ 监控面板响应时间异常
   □ 用户反馈页面卡顿

2. 问题定位
   □ 使用 EXPLAIN 分析执行计划
   □ 检查是否走索引
   □ 检查扫描行数
   □ 检查是否有额外排序/临时表

3. 方案设计
   □ 新增/优化索引
   □ 改写 SQL
   □ 引入缓存
   □ 分库分表（极端情况）

4. 方案实施
   □ 测试环境验证
   □ 灰度发布
   □ 监控指标对比

5. 效果验证
   □ EXPLAIN 对比
   □ 响应时间对比
   □ 慢查询数量对比
   □ 缓存命中率
```

### 性能验收标准

| 指标 | 标准 | 说明 |
|------|------|------|
| 分页查询响应时间 | < 100ms | 含数据库查询 |
| 单条查询响应时间 | < 50ms | 主键查询 |
| 写操作响应时间 | < 200ms | 含事务提交 |
| 慢查询数量 | 0 | 无超过 1s 的查询 |
| 缓存命中率 | > 80% | 热点数据 |
| 数据库 CPU | < 50% | 正常负载 |
| 数据库连接池使用率 | < 80% | 峰值时段 |
