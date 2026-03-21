# 测试规范参考

> 按需加载。适用场景：单元测试、集成测试、Mock、测试覆盖率。

---

## 一、测试分层策略

```
        ┌─────────┐
        │  E2E    │  少量：端到端测试（启动完整应用）
        ├─────────┤
        │ 集成测试 │  中等：Service + Mapper + 数据库
        ├─────────┤
        │ 单元测试 │  大量：纯逻辑、独立方法
        └─────────┘
```

| 测试类型 | 测试范围 | 依赖 | 速度 |
|---------|---------|------|------|
| 单元测试 | 单个方法/类 | Mock | 毫秒级 |
| 集成测试 | Service + Mapper | H2 | 秒级 |
| 切片测试 | Controller | Mock Service | 秒级 |

---

## 二、单元测试规范

### 命名与位置

```
src/test/java/com/dainthub/{project}/module/{module}/service/impl/{Entity}ServiceImplTest.java

测试方法命名：{方法名}_{场景}_{预期结果}
```

### AAA 模式

```java
@ExtendWith(MockitoExtension.class)
class {Entity}ServiceImplTest {

    @Mock
    private {Entity}Mapper {entity}Mapper;

    @InjectMocks
    private {Entity}ServiceImpl {entity}Service;

    @Test
    @DisplayName("创建实体 - 成功返回主键 ID")
    void createEntity_success_returnId() {
        // ── Arrange ────────────────────────────────
        {Entity}SaveReqVO reqVO = new {Entity}SaveReqVO();
        reqVO.setName("测试实体");
        
        when({entity}Mapper.selectByName("测试实体")).thenReturn(null);
        when({entity}Mapper.insert(any())).thenAnswer(inv -> {
            inv.getArgument(0, {Entity}DO.class).setId(1L);
            return 1;
        });

        // ── Act ──────────────────────────────────
        Long result = {entity}Service.create{Entity}(reqVO);

        // ── Assert ───────────────────────────────
        assertThat(result).isEqualTo(1L);
        verify({entity}Mapper).insert(any());
    }

    @Test
    @DisplayName("创建实体 - 名称重复时抛出异常")
    void createEntity_nameDuplicate_throwException() {
        // Arrange
        {Entity}SaveReqVO reqVO = new {Entity}SaveReqVO();
        reqVO.setName("重复名称");
        when({entity}Mapper.selectByName("重复名称")).thenReturn(new {Entity}DO());

        // Act & Assert
        assertThatThrownBy(() -> {entity}Service.create{Entity}(reqVO))
                .isInstanceOf(ServiceException.class)
                .hasMessageContaining("名称已存在");
    }
}
```

### Mock 速查

```java
// 返回值
when(mapper.selectById(1L)).thenReturn(entity);
when(mapper.selectById(any())).thenReturn(null);

// 抛异常
when(mapper.insert(any())).thenThrow(new RuntimeException("数据库异常"));

// void 方法
doNothing().when(mapper).deleteById(any());
doThrow(new RuntimeException()).when(mapper).deleteById(999L);

// 验证调用
verify(mapper).insert(any());                // 调用 1 次
verify(mapper, times(2)).selectById(any());  // 调用 2 次
verify(mapper, never()).deleteById(any());   // 从未调用

// 参数捕获
ArgumentCaptor<{Entity}DO> captor = ArgumentCaptor.forClass({Entity}DO.class);
verify(mapper).insert(captor.capture());
assertThat(captor.getValue().getName()).isEqualTo("测试");
```

---

## 三、集成测试

### H2 内存数据库

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
        {Entity}DO entity = new {Entity}DO();
        entity.setName("测试");
        entity.setStatus(1);
        {entity}Mapper.insert(entity);

        // Act
        {Entity}PageReqVO reqVO = new {Entity}PageReqVO();
        reqVO.setStatus(1);
        PageResult<{Entity}DO> result = {entity}Mapper.selectPage(reqVO);

        // Assert
        assertThat(result.getList()).hasSize(1);
    }
}
```

### 测试配置（application-test.yaml）

```yaml
spring:
  datasource:
    driver-class-name: org.h2.Driver
    url: jdbc:h2:mem:testdb;DB_CLOSE_DELAY=-1;MODE=MySQL
    username: sa
    password:
mybatis-plus:
  mapper-locations: classpath*:mapper/**/*.xml
  configuration:
    map-underscore-to-camel-case: true
```

### 事务回滚

```java
@SpringBootTest
@Transactional  // 测试结束后自动回滚
class {Entity}ServiceIntegrationTest {

    @Resource
    private {Entity}Service {entity}Service;

    @Test
    void createEntity_success() {
        Long id = {entity}Service.create{Entity}(reqVO);
        assertThat({entity}Service.get{Entity}OrElse(id)).isPresent();
        // 测试结束后自动回滚
    }
}
```

---

## 四、Controller 切片测试

```java
@WebMvcTest({Entity}Controller.class)
class {Entity}ControllerTest {

    @Resource
    private MockMvc mockMvc;

    @MockBean
    private {Entity}Service {entity}Service;

    @Test
    @DisplayName("创建接口 - 成功")
    void createEntity_success() throws Exception {
        when({entity}Service.create{Entity}(any())).thenReturn(1L);

        mockMvc.perform(post("/admin-api/{module}/{entity}/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(JsonUtils.toJsonString(reqVO)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(0))
                .andExpect(jsonPath("$.data").value(1));
    }

    @Test
    @DisplayName("创建接口 - 参数校验失败")
    void createEntity_validationFail() throws Exception {
        // name 为空
        mockMvc.perform(post("/admin-api/{module}/{entity}/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{}"))
                .andExpect(status().isBadRequest());
    }
}
```

---

## 五、测试覆盖率

### 标准

| 模块 | 行覆盖率 | 分支覆盖率 |
|------|---------|-----------|
| Service | ≥ 80% | ≥ 70% |
| Mapper | ≥ 60% | ≥ 50% |
| Controller | ≥ 70% | ≥ 60% |
| 工具类 | ≥ 90% | ≥ 80% |

### Jacoco 配置

```xml
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.11</version>
    <executions>
        <execution>
            <goals><goal>prepare-agent</goal></goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>test</phase>
            <goals><goal>report</goal></goals>
        </execution>
    </executions>
</plugin>
```

```bash
mvn clean test jacoco:report
# 报告：target/site/jacoco/index.html
```

---

## 六、测试数据构造

```java
public final class TestDataFactory {

    private TestDataFactory() {}

    public static {Entity}DO createEntity() {
        return createEntity("默认名称");
    }

    public static {Entity}DO createEntity(String name) {
        {Entity}DO entity = new {Entity}DO();
        entity.setName(name);
        entity.setStatus(1);
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

```java
// ── 空值/边界值 ────────────────────────────────
@Test @DisplayName("参数为 null 时抛出异常")
@Test @DisplayName("空集合返回空结果")
@Test @DisplayName("ID = 0 时返回不存在")

// ── 边界条件 ────────────────────────────────
@Test @DisplayName("字符串最大长度时处理正确")
@Test @DisplayName("分页 pageNo = 1 时返回第一页")

// ── 异常场景 ────────────────────────────────
@Test @DisplayName("数据库连接失败时抛出异常")
@Test @DisplayName("唯一约束冲突时转为业务异常")

// ── 并发场景 ────────────────────────────────
@Test @DisplayName("并发创建同名称实体 - 仅一个成功")
```

### 参数化测试

```java
@ParameterizedTest
@CsvSource({
    "1, '实体A', true",    // 有效
    "2, '', false",        // 名称为空
})
@DisplayName("创建实体 - 参数化验证")
void createEntity_parameterized(Long id, String name, boolean expectSuccess) {
    // ...
}

@ParameterizedTest
@ValueSource(ints = {0, 1, 100, Integer.MAX_VALUE})
@DisplayName("排序值边界测试")
void sortOrder_boundary(int sortOrder) { }
```

---

## 八、测试自检清单

```
命名：
□ 测试类：{被测类}Test.java
□ @DisplayName 中文描述
□ 方法命名：{方法名}_{场景}_{预期结果}

结构：
□ AAA 模式（Arrange-Act-Assert）
□ 一个测试只验证一个场景
□ 测试方法不超过 30 行

Mock：
□ 外部依赖用 @Mock
□ 不 Mock 被测类本身
□ verify 关键方法调用

断言：
□ 使用 AssertJ（assertThat）
□ 异常用 assertThatThrownBy

覆盖率：
□ Service ≥ 80%
□ 边界条件有覆盖
```

---

## 九、常用依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>

<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>test</scope>
</dependency>

<dependency>
    <groupId>org.assertj</groupId>
    <artifactId>assertj-core</artifactId>
    <version>3.25.1</version>
    <scope>test</scope>
</dependency>
```