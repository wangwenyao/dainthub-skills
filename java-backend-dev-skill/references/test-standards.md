# 测试规范参考

> 按需加载。适用场景：单元测试、集成测试、Mock、测试覆盖率。

---

## 一、测试分层策略

### 测试金字塔

```
        ┌─────────┐
        │  E2E    │  少量：端到端测试（启动完整应用）
        ├─────────┤
        │ 集成测试 │  中等：Service + Mapper + 数据库
        ├─────────┤
        │ 单元测试 │  大量：纯逻辑、独立方法
        └─────────┘
```

### 各层测试职责

| 测试类型 | 测试范围 | 依赖 | 执行速度 | 适用场景 |
|---------|---------|------|---------|---------|
| 单元测试 | 单个方法/类 | Mock 外部依赖 | 毫秒级 | 业务逻辑、工具方法 |
| 集成测试 | Service + Mapper | H2 内存数据库 | 秒级 | 数据库交互、事务 |
| 切片测试 | Controller | Mock Service | 秒级 | HTTP 接口 |
| E2E 测试 | 完整应用 | 真实环境 | 分钟级 | 核心流程 |

---

## 二、单元测试规范

### 测试类命名与位置

```
src/main/java/com/dainthub/{project}/module/{module}/service/impl/{Entity}ServiceImpl.java
src/test/java/com/dainthub/{project}/module/{module}/service/impl/{Entity}ServiceImplTest.java

# 测试类命名规则
{被测类名}Test.java          // 标准命名
{被测类名}IntegrationTest.java // 集成测试
```

### 测试方法命名（中文描述业务场景）

```java
// ✅ 使用 @DisplayName 说明测试意图
@Test
@DisplayName("创建实体 - 名称重复时抛出异常")
void createEntity_nameDuplicate_throwException() {
    // ...
}

@Test
@DisplayName("创建实体 - 成功返回主键 ID")
void createEntity_success_returnId() {
    // ...
}

@Test
@DisplayName("更新实体 - 排除自身后名称唯一则成功")
void updateEntity_excludeSelfNameUnique_success() {
    // ...
}

// ❌ 禁止无意义命名
@Test
void test1() { }
@Test
void testCreate() { }  // 不明确测试什么场景
```

### AAA 模式（Arrange-Act-Assert）

```java
@Test
@DisplayName("创建实体 - 成功返回主键 ID")
void createEntity_success_returnId() {
    // ── Arrange（准备）──────────────────────────────
    {Entity}SaveReqVO reqVO = new {Entity}SaveReqVO();
    reqVO.setName("测试实体");
    reqVO.setStatus(1);
    reqVO.setSortOrder(0);

    {Entity}DO entity = reqVO.toEntity();
    entity.setId(1L);

    when({entity}Mapper.selectByName("测试实体")).thenReturn(null);
    when({entity}Mapper.insert(any())).thenAnswer(inv -> {
        {Entity}DO arg = inv.getArgument(0);
        arg.setId(1L);
        return 1;
    });

    // ── Act（执行）──────────────────────────────────
    Long result = {entity}Service.create{Entity}(reqVO);

    // ── Assert（断言）───────────────────────────────
    assertThat(result).isEqualTo(1L);
    verify({entity}Mapper).insert(any());
}

@Test
@DisplayName("创建实体 - 名称重复时抛出异常")
void createEntity_nameDuplicate_throwException() {
    // Arrange
    {Entity}SaveReqVO reqVO = new {Entity}SaveReqVO();
    reqVO.setName("重复名称");

    {Entity}DO existing = new {Entity}DO();
    existing.setId(1L);
    existing.setName("重复名称");

    when({entity}Mapper.selectByName("重复名称")).thenReturn(existing);

    // Act & Assert
    assertThatThrownBy(() -> {entity}Service.create{Entity}(reqVO))
            .isInstanceOf(ServiceException.class)
            .hasMessageContaining("{entity}名称已存在");
}
```

### Mock 规范

```java
import static org.mockito.Mockito.*;
import static org.assertj.core.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
class {Entity}ServiceImplTest {

    @Mock
    private {Entity}Mapper {entity}Mapper;

    @InjectMocks
    private {Entity}ServiceImpl {entity}Service;

    // ── Mock 返回值 ──────────────────────────────
    when({entity}Mapper.selectById(1L)).thenReturn(entity);
    when({entity}Mapper.selectById(any())).thenReturn(null);
    when({entity}Mapper.selectByName("不存在")).thenReturn(null);

    // ── Mock 抛异常 ──────────────────────────────
    when({entity}Mapper.insert(any()))
            .thenThrow(new RuntimeException("数据库异常"));

    // ── Mock void 方法 ───────────────────────────
    doNothing().when({entity}Mapper).deleteById(any());
    doThrow(new RuntimeException("删除失败"))
            .when({entity}Mapper).deleteById(999L);

    // ── Mock 批量操作 ────────────────────────────
    when({entity}Mapper.selectBatchIds(anyCollection()))
            .thenReturn(Arrays.asList(entity1, entity2));

    // ── 验证调用 ────────────────────────────────
    verify({entity}Mapper).insert(any());           // 调用了 1 次
    verify({entity}Mapper, times(2)).selectById(any()); // 调用了 2 次
    verify({entity}Mapper, never()).deleteById(any()); // 从未调用
    verifyNoMoreInteractions({entity}Mapper);       // 无其他调用

    // ── 参数捕获 ────────────────────────────────
    ArgumentCaptor<{Entity}DO> captor = ArgumentCaptor.forClass({Entity}DO.class);
    verify({entity}Mapper).insert(captor.capture());
    assertThat(captor.getValue().getName()).isEqualTo("测试实体");
}
```

---

## 三、集成测试规范

### 使用 H2 内存数据库

```java
@MybatisTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@TestPropertySource(locations = "classpath:application-test.yaml")
class {Entity}MapperIntegrationTest {

    @Resource
    private {Entity}Mapper {entity}Mapper;

    @Test
    @DisplayName("分页查询 - 条件过滤正确")
    void selectPage_withCondition_returnFiltered() {
        // Arrange
        {Entity}DO entity1 = new {Entity}DO();
        entity1.setName("实体A");
        entity1.setStatus(1);
        {entity}Mapper.insert(entity1);

        {Entity}DO entity2 = new {Entity}DO();
        entity2.setName("实体B");
        entity2.setStatus(0);
        {entity}Mapper.insert(entity2);

        // Act
        {Entity}PageReqVO reqVO = new {Entity}PageReqVO();
        reqVO.setStatus(1);
        PageResult<{Entity}DO> result = {entity}Mapper.selectPage(reqVO);

        // Assert
        assertThat(result.getList()).hasSize(1);
        assertThat(result.getList().get(0).getName()).isEqualTo("实体A");
    }
}
```

### 测试配置文件（application-test.yaml）

```yaml
spring:
  datasource:
    driver-class-name: org.h2.Driver
    url: jdbc:h2:mem:testdb;DB_CLOSE_DELAY=-1;MODE=MySQL
    username: sa
    password:
mybatis-plus:
  configuration:
    map-underscore-to-camel-case: true
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
  mapper-locations: classpath*:mapper/**/*.xml
  type-aliases-package: com.dainthub.{project}.module.*.dal.dataobject
  global-config:
    db-config:
      logic-delete-field: deleted
      logic-delete-value: 1
      logic-not-delete-value: 0
  sql:
    init:
      mode: always
      schema-locations: classpath:schema.sql
      data-locations: classpath:data.sql
```

### 事务回滚测试

```java
@SpringBootTest
@Transactional  // 测试结束后自动回滚
class {Entity}ServiceIntegrationTest {

    @Resource
    private {Entity}Service {entity}Service;

    @Test
    @DisplayName("创建实体 - 事务回滚验证")
    void createEntity_transactionRollback() {
        // Arrange
        {Entity}SaveReqVO reqVO = new {Entity}SaveReqVO();
        reqVO.setName("测试实体");

        // Act
        Long id = {entity}Service.create{Entity}(reqVO);

        // Assert - 测试内可见
        assertThat({entity}Service.get{Entity}OrElse(id)).isPresent();

        // 测试结束后自动回滚，数据库无残留
    }

    @Test
    @DisplayName("批量插入 - 分批处理正确")
    @Commit  // 明确提交（不回滚）
    void insertBatch_largeList_splitCorrectly() {
        // 仅用于验证批量插入逻辑
    }
}
```

---

## 四、Controller 切片测试

### MockMvc 测试

```java
@WebMvcTest({Entity}Controller.class)
@Import({Entity}ServiceImpl.class)
class {Entity}ControllerTest {

    @Resource
    private MockMvc mockMvc;

    @MockBean
    private {Entity}Service {entity}Service;

    @Test
    @DisplayName("创建实体接口 - 成功返回 ID")
    void createEntity_success() throws Exception {
        // Arrange
        {Entity}SaveReqVO reqVO = new {Entity}SaveReqVO();
        reqVO.setName("测试实体");
        reqVO.setStatus(1);

        when({entity}Service.create{Entity}(any())).thenReturn(1L);

        // Act & Assert
        mockMvc.perform(post("/admin-api/{module}/{entity}/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(JsonUtils.toJsonString(reqVO)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(0))
                .andExpect(jsonPath("$.data").value(1));
    }

    @Test
    @DisplayName("创建实体接口 - 参数校验失败")
    void createEntity_validationFail() throws Exception {
        // Arrange
        {Entity}SaveReqVO reqVO = new {Entity}SaveReqVO();
        // name 为空，违反 @NotBlank

        // Act & Assert
        mockMvc.perform(post("/admin-api/{module}/{entity}/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(JsonUtils.toJsonString(reqVO)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value(400))
                .andExpect(jsonPath("$.msg").exists());
    }

    @Test
    @DisplayName("分页查询接口 - 返回分页数据")
    void getEntityPage_success() throws Exception {
        // Arrange
        {Entity}DO entity = new {Entity}DO();
        entity.setId(1L);
        entity.setName("测试实体");

        PageResult<{Entity}DO> page = new PageResult<>(List.of(entity), 1L);
        when({entity}Service.get{Entity}Page(any())).thenReturn(page);

        // Act & Assert
        mockMvc.perform(get("/admin-api/{module}/{entity}/page")
                        .param("pageNo", "1")
                        .param("pageSize", "10"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(0))
                .andExpect(jsonPath("$.data.list").isArray())
                .andExpect(jsonPath("$.data.list[0].name").value("测试实体"));
    }
}
```

---

## 五、测试覆盖率要求

### 覆盖率标准

| 模块类型 | 行覆盖率 | 分支覆盖率 | 要求 |
|---------|---------|-----------|------|
| Service 业务层 | ≥ 80% | ≥ 70% | 必须 |
| Mapper 数据层 | ≥ 60% | ≥ 50% | 建议 |
| Controller 层 | ≥ 70% | ≥ 60% | 建议 |
| 工具类 | ≥ 90% | ≥ 80% | 必须 |

### Jacoco 配置

```xml
<!-- pom.xml -->
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.11</version>
    <executions>
        <execution>
            <goals>
                <goal>prepare-agent</goal>
            </goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>test</phase>
            <goals>
                <goal>report</goal>
            </goals>
        </execution>
        <execution>
            <id>check</id>
            <goals>
                <goal>check</goal>
            </goals>
            <configuration>
                <rules>
                    <rule>
                        <element>BUNDLE</element>
                        <limits>
                            <limit>
                                <counter>LINE</counter>
                                <value>COVEREDRATIO</value>
                                <minimum>0.80</minimum>
                            </limit>
                            <limit>
                                <counter>BRANCH</counter>
                                <value>COVEREDRATIO</value>
                                <minimum>0.70</minimum>
                            </limit>
                        </limits>
                    </rule>
                </rules>
            </configuration>
        </execution>
    </executions>
</plugin>
```

### 覆盖率报告生成

```bash
# 运行测试并生成报告
mvn clean test jacoco:report

# 报告位置
target/site/jacoco/index.html
```

---

## 六、测试数据构造

### 使用 Builder 模式

```java
@Test
@DisplayName("创建订单 - 高价值订单触发审批")
void createOrder_highValue_triggerApproval() {
    // Arrange - 使用 Builder 构造测试数据
    OrderDO order = OrderDO.builder()
            .userId(1L)
            .productId(100L)
            .amount(new BigDecimal("10000.00"))  // 高价值
            .status(OrderStatusEnum.PENDING.getStatus())
            .build();

    // Act
    orderService.createOrder(order);

    // Assert
    verify(approvalClient).submitApproval(any());
}
```

### 测试数据工厂

```java
/**
 * 测试数据工厂 - 统一构造测试数据
 */
public final class TestDataFactory {

    private TestDataFactory() {}

    public static {Entity}DO createEntity() {
        return createEntity("默认名称");
    }

    public static {Entity}DO createEntity(String name) {
        {Entity}DO entity = new {Entity}DO();
        entity.setName(name);
        entity.setStatus(1);
        entity.setSortOrder(0);
        return entity;
    }

    public static {Entity}DO createEntity(Long id, String name) {
        {Entity}DO entity = createEntity(name);
        entity.setId(id);
        return entity;
    }

    public static List<{Entity}DO> createEntities(int count) {
        return IntStream.range(0, count)
                .mapToObj(i -> createEntity("实体" + i))
                .collect(Collectors.toList());
    }

    public static {Entity}SaveReqVO createSaveReqVO() {
        {Entity}SaveReqVO vo = new {Entity}SaveReqVO();
        vo.setName("测试实体");
        vo.setStatus(1);
        vo.setSortOrder(0);
        return vo;
    }
}

// 使用
@Test
void test() {
    {Entity}DO entity = TestDataFactory.createEntity("测试");
    List<{Entity}DO> entities = TestDataFactory.createEntities(10);
}
```

---

## 七、边界条件测试清单

### 必测场景

```java
// ── 空值/边界值 ────────────────────────────────
@Test @DisplayName("参数为 null 时抛出异常")
@Test @DisplayName("空集合返回空结果")
@Test @DisplayName("ID = 0 时返回不存在")
@Test @DisplayName("ID = Long.MAX_VALUE 时处理正确")

// ── 边界条件 ────────────────────────────────
@Test @DisplayName("字符串最大长度时处理正确")
@Test @DisplayName("金额为 0 时处理正确")
@Test @DisplayName("分页 pageNo = 1 时返回第一页")
@Test @DisplayName("分页 pageSize = 0 时使用默认值")

// ── 异常场景 ────────────────────────────────
@Test @DisplayName("数据库连接失败时抛出异常")
@Test @DisplayName("唯一约束冲突时转为业务异常")
@Test @DisplayName("外部服务超时时降级处理")

// ── 并发场景 ────────────────────────────────
@Test @DisplayName("并发创建同名称实体 - 仅一个成功")
@Test @DisplayName("乐观锁版本冲突 - 重试成功")
```

### 参数化测试

```java
@ParameterizedTest
@CsvSource({
    "1, '实体A', true",     // 有效
    "2, '', false",          // 名称为空
    "3, 'AAAAAAAAAA...64', true",  // 最大长度
})
@DisplayName("创建实体 - 参数化验证")
void createEntity_parameterized(Long id, String name, boolean expectSuccess) {
    {Entity}SaveReqVO reqVO = new {Entity}SaveReqVO();
    reqVO.setId(id);
    reqVO.setName(name);

    if (expectSuccess) {
        assertThatCode(() -> {entity}Service.create{Entity}(reqVO))
                .doesNotThrowAnyException();
    } else {
        assertThatThrownBy(() -> {entity}Service.create{Entity}(reqVO))
                .isInstanceOf(ServiceException.class);
    }
}

@ParameterizedTest
@ValueSource(ints = {0, 1, 2, 100, Integer.MAX_VALUE})
@DisplayName("排序值边界测试")
void sortOrder_boundary(int sortOrder) {
    {Entity}DO entity = TestDataFactory.createEntity();
    entity.setSortOrder(sortOrder);
    // 验证排序逻辑
}
```

---

## 八、测试自检清单

```
命名规范：
□ 测试类命名：{被测类}Test.java
□ 测试方法使用 @DisplayName 中文描述
□ 测试方法命名：{方法名}_{场景}_{预期结果}

结构规范：
□ 使用 AAA 模式（Arrange-Act-Assert）
□ 一个测试方法只验证一个场景
□ 测试方法不超过 30 行

Mock 规范：
□ 外部依赖使用 @Mock
□ 不 Mock 被测类本身
□ 验证关键方法调用（verify）

断言规范：
□ 使用 AssertJ 流式断言（assertThat）
□ 断言信息清晰（as("描述")）
□ 异常断言使用 assertThatThrownBy

覆盖率规范：
□ Service 层行覆盖率 ≥ 80%
□ 关键分支均有测试
□ 边界条件有覆盖

数据规范：
□ 使用测试数据工厂构造数据
□ 测试数据不依赖执行顺序
□ 测试结束后数据清理（@Transactional 自动回滚）
```

---

## 九、常用测试依赖

```xml
<!-- 测试依赖 -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>

<!-- H2 内存数据库 -->
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>test</scope>
</dependency>

<!-- AssertJ 流式断言 -->
<dependency>
    <groupId>org.assertj</groupId>
    <artifactId>assertj-core</artifactId>
    <version>3.25.1</version>
    <scope>test</scope>
</dependency>

<!-- 参数化测试 -->
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter-params</artifactId>
    <scope>test</scope>
</dependency>
```