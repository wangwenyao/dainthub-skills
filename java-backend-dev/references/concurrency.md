# 并发安全规范

> Java 后端并发安全编程规范，涵盖线程安全、锁策略、并发集合、异步处理。

---

## 一、并发安全原则

| 原则 | 说明 |
|------|------|
| **不可变优先** | 不可变对象天然线程安全 |
| **局部变量优先** | 方法内局部变量无并发问题 |
| **线程封闭** | ThreadLocal 实现线程封闭 |
| **同步最小化** | 锁范围越小越好 |

---

## 二、线程安全策略

### 2.1 不可变对象

```java
// ✅ 正确：不可变对象，线程安全
@Data
@Builder
public final class UserSnapshot {
    private final Long id;
    private final String name;
    private final Integer status;
    
    // 无 setter，只有 getter
}
```

### 2.2 线程封闭

```java
// ✅ 正确：SimpleDateFormat 非线程安全，用 ThreadLocal
private static final ThreadLocal<SimpleDateFormat> DATE_FORMAT = 
    ThreadLocal.withInitial(() -> new SimpleDateFormat("yyyy-MM-dd"));

// 使用
String date = DATE_FORMAT.get().format(new Date());

// 请求结束清理（Web 环境）
@Override
public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler) {
    DATE_FORMAT.remove();
}
```

### 2.3 同步控制

```java
// ✅ 正确：双重检查锁定
private volatile Singleton instance;

public Singleton getInstance() {
    if (instance == null) {
        synchronized (Singleton.class) {
            if (instance == null) {
                instance = new Singleton();
            }
        }
    }
    return instance;
}

// ❌ 错误：同步方法粒度过大
public synchronized void process() {
    // 大量代码，锁范围过大
}
```

---

## 三、并发集合

### 3.1 集合选择

| 场景 | 推荐集合 | 说明 |
|------|---------|------|
| 高并发读 | `ConcurrentHashMap` | 读无锁 |
| 高并发读写 | `ConcurrentHashMap` | 分段锁 |
| 队列 | `ConcurrentLinkedQueue` | 无界队列 |
| 阻塞队列 | `ArrayBlockingQueue` | 有界队列 |
| 延迟队列 | `DelayQueue` | 延迟任务 |

### 3.2 ConcurrentHashMap 使用

```java
// ✅ 正确：computeIfPresent / computeIfAbsent 原子操作
ConcurrentMap<String, AtomicInteger> counter = new ConcurrentHashMap<>();

counter.computeIfAbsent("key", k -> new AtomicInteger(0)).incrementAndGet();

// ❌ 错误：非原子操作
Integer value = counter.get("key");
counter.put("key", value + 1); // 竞态条件
```

---

## 四、分布式锁

### 4.1 Redisson 分布式锁

```java
@Resource
private RedissonClient redissonClient;

public void processWithLock(String orderId) {
    String lockKey = "order:lock:" + orderId;
    RLock lock = redissonClient.getLock(lockKey);
    
    try {
        // 尝试获取锁，等待 10s，锁自动释放 30s
        boolean acquired = lock.tryLock(10, 30, TimeUnit.SECONDS);
        if (!acquired) {
            throw exception(ORDER_LOCK_FAILED);
        }
        
        // 业务处理
        doProcess(orderId);
        
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
        throw exception(ORDER_LOCK_INTERRUPTED);
    } finally {
        // 只释放自己持有的锁
        if (lock.isHeldByCurrentThread()) {
            lock.unlock();
        }
    }
}
```

### 4.2 分布式锁约束

| 规则 | 说明 |
|------|------|
| 必须设置超时 | 防止死锁 |
| 必须在 finally 释放 | 保证锁释放 |
| 只释放自己的锁 | `isHeldByCurrentThread()` |
| 锁粒度最小化 | 按业务 ID 加锁，不要全局锁 |

---

## 五、异步处理

### 5.1 线程池配置

```java
@Configuration
public class ThreadPoolConfig {
    
    @Bean("asyncExecutor")
    public Executor asyncExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(4);
        executor.setMaxPoolSize(16);
        executor.setQueueCapacity(1000);
        executor.setKeepAliveSeconds(60);
        executor.setThreadNamePrefix("async-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.initialize();
        return executor;
    }
}
```

### 5.2 @Async 使用

```java
@Service
public class NotificationServiceImpl {
    
    @Async("asyncExecutor")
    public void sendNotification(Long userId, String message) {
        // 异步发送通知
        // 注意：不能在事务中使用 @Async
    }
}
```

### 5.3 异步约束

| 规则 | 说明 |
|------|------|
| 禁止在事务中使用 @Async | 事务传播失效 |
| 必须指定线程池 | 避免使用默认线程池 |
| 必须配置拒绝策略 | `CallerRunsPolicy` 降级 |
| 异常必须处理 | @Async 异常不会传播到调用方 |

---

## 六、原子操作

### 6.1 AtomicInteger / AtomicLong

```java
// ✅ 正确：原子操作
private final AtomicInteger counter = new AtomicInteger(0);

public int increment() {
    return counter.incrementAndGet();
}

// ✅ 正确：CAS 更新
public boolean update(int expected, int newValue) {
    return counter.compareAndSet(expected, newValue);
}
```

### 6.2 乐观锁（数据库）

```java
// DO 中添加版本号
@Version
private Integer version;

// 更新时自动检查版本
// UPDATE ... SET version = version + 1 WHERE id = ? AND version = ?
```

---

## 七、常见并发问题

### 7.1 竞态条件

```java
// ❌ 错误：检查-执行竞态
if (user.getStatus() == Status.ENABLED) {
    // 此时状态可能已被其他线程修改
    doSomething();
}

// ✅ 正确：使用数据库乐观锁或分布式锁
```

### 7.2 死锁

```java
// ❌ 错误：嵌套锁，可能死锁
synchronized (lockA) {
    synchronized (lockB) {
        // ...
    }
}

// ✅ 正确：统一锁顺序，或使用 tryLock 超时
```

### 7.3 内存可见性

```java
// ❌ 错误：状态变化对其他线程不可见
private boolean running = true;

// ✅ 正确：使用 volatile
private volatile boolean running = true;
```

---

## 八、并发约束

| ID | 规则 |
|----|------|
| C-CONC-001 | 共享可变状态必须同步 |
| C-CONC-002 | 禁止使用 `new Thread()` 创建线程，必须用线程池 |
| C-CONC-003 | 分布式锁必须设置超时时间 |
| C-CONC-004 | 锁必须在 finally 块中释放 |
| C-CONC-005 | @Async 方法必须指定线程池 |
| C-CONC-006 | 禁止在事务方法中调用 @Async 方法 |
| C-CONC-007 | SimpleDateFormat 必须用 ThreadLocal 包装 |
| C-CONC-008 | ConcurrentHashMap 的复合操作必须用原子方法 |