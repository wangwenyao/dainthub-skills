# API 设计规范参考

> 按需加载。适用场景：API 版本管理、参数校验、接口设计、响应格式。

---

## 一、API 版本管理

### 版本策略

本项目采用 **URL Path 版本策略**：`/v1/orders`、`/v2/orders`

| 策略 | 实现方式 | 推荐场景 |
|------|---------|---------|
| URL Path | `/v1/orders` | 公开 API（推荐） |
| Header | `Accept: vnd.api.v1+json` | 内部服务 |

### 版本规则

```
major 版本变更：不兼容修改（删除字段、修改类型）→ 升级版本号
minor 版本变更：兼容修改（新增字段）→ 不升级版本号
```

### 版本共存

```java
// 不同版本使用不同 Controller
@RestController
@RequestMapping("/admin-api/v1/orders")
public class OrderControllerV1 { /* v1 实现 */ }

@RestController
@RequestMapping("/admin-api/v2/orders")
public class OrderControllerV2 { /* v2 实现 */ }
```

### 版本废弃

```java
// 标记废弃（保留 3 个月）
@GetMapping("/v1/detail")
@Operation(summary = "订单详情 V1（已废弃）", deprecated = true)
@Deprecated
public CommonResult<OrderRespV1VO> getDetailV1(@RequestParam Long id) {
    response.setHeader("X-API-Deprecated", "true");
    response.setHeader("X-API-Sunset", "2024-06-01");
    return success(orderService.getDetailV1(id));
}
```

### 兼容性规则

```
兼容修改（无需升级）：
✅ 新增可选参数
✅ 新增响应字段
✅ 新增接口

不兼容修改（必须升级）：
❌ 删除字段
❌ 修改字段类型
❌ 修改字段名称
```

---

## 二、参数校验

### JSR-303 注解

```java
@Schema(description = "{entity}保存请求 VO")
@Data
public class {Entity}SaveReqVO {

    @Schema(description = "主键（更新时必传）")
    private Long id;

    @Schema(description = "名称", requiredMode = Schema.RequiredMode.REQUIRED)
    @NotBlank(message = "名称不能为空")
    @Size(min = 2, max = 64, message = "名称长度 2-64 字符")
    private String name;

    @Schema(description = "手机号")
    @Pattern(regexp = "^1[3-9]\\d{9}$", message = "手机号格式不正确")
    private String mobile;

    @Schema(description = "数量")
    @NotNull(message = "数量不能为空")
    @Positive(message = "数量必须为正数")
    private Integer quantity;

    @Schema(description = "金额")
    @DecimalMin(value = "0.01", message = "金额必须大于 0")
    private BigDecimal amount;

    @Schema(description = "标签列表")
    @Size(min = 1, max = 10, message = "标签 1-10 个")
    private List<@NotBlank String> tags;

    @Schema(description = "地址")
    @Valid  // 嵌套校验
    @NotNull
    private AddressVO address;
}
```

### 分组校验

```java
public interface CreateGroup {}
public interface UpdateGroup {}

@Schema(description = "{entity}保存请求 VO")
@Data
public class {Entity}SaveReqVO {

    @NotNull(message = "主键不能为空", groups = UpdateGroup.class)
    @Null(message = "主键必须为空", groups = CreateGroup.class)
    private Long id;
}

// Controller
@PostMapping("/create")
public CommonResult<Long> create(@Validated(CreateGroup.class) @RequestBody {Entity}SaveReqVO reqVO) { }

@PutMapping("/update")
public CommonResult<Boolean> update(@Validated(UpdateGroup.class) @RequestBody {Entity}SaveReqVO reqVO) { }
```

### 自定义枚举校验

```java
@InEnum(value = {Entity}StatusEnum.class, message = "状态值不合法")
private Integer status;
```

### 业务校验

```java
@Service
@Validated  // 启用方法级别校验
public class {Entity}ServiceImpl {

    private void validateNameUnique(Long id, String name) {
        {Entity}DO existing = {entity}Mapper.selectByName(name);
        if (existing != null && (id == null || !existing.getId().equals(id))) {
            throw exception({ENTITY}_NAME_DUPLICATE);
        }
    }
}
```

---

## 三、响应格式

### 统一响应结构

```java
@Data
public class CommonResult<T> {
    private Integer code;    // 0=成功，非0=失败
    private String msg;
    private T data;
    private Long timestamp;

    public static <T> CommonResult<T> success(T data) {
        return new CommonResult<>(0, "success", data, System.currentTimeMillis());
    }

    public static <T> CommonResult<T> error(ErrorCode errorCode) {
        return new CommonResult<>(errorCode.getCode(), errorCode.getMsg(), null, System.currentTimeMillis());
    }
}
```

### 分页响应

```java
@Data
public class PageResult<T> {
    private List<T> list;
    private Long total;

    public static <T> PageResult<T> of(List<T> list, Long total) {
        return new PageResult<>(list, total);
    }

    public static <T> PageResult<T> empty() {
        return new PageResult<>(Collections.emptyList(), 0L);
    }
}
```

### 错误码规范

```java
/**
 * 错误码规则：1 + 模块3位 + 业务3位
 * 模块码：system=001, member=002, trade=005
 */
public interface ErrorCodeConstants {

    // 通用错误
    ErrorCode BAD_REQUEST    = new ErrorCode(1000000, "请求参数不正确");
    ErrorCode UNAUTHORIZED   = new ErrorCode(1000001, "未登录或登录已过期");
    ErrorCode FORBIDDEN      = new ErrorCode(1000002, "无权限访问");

    // 业务错误
    ErrorCode {ENTITY}_NOT_EXISTS     = new ErrorCode(1{MODULE_CODE}001, "{entity}不存在");
    ErrorCode {ENTITY}_NAME_DUPLICATE = new ErrorCode(1{MODULE_CODE}002, "{entity}名称已存在");
}
```

---

## 四、RESTful 规范

```java
// ✅ RESTful 设计
GET    /admin-api/{module}/{entity}          // 列表查询
GET    /admin-api/{module}/{entity}/{id}     // 详情查询
POST   /admin-api/{module}/{entity}          // 创建
PUT    /admin-api/{module}/{entity}/{id}     // 更新
DELETE /admin-api/{module}/{entity}/{id}     // 删除

// ✅ 批量操作
POST   /admin-api/{module}/{entity}/batch-create
DELETE /admin-api/{module}/{entity}/batch-delete

// ✅ 状态变更
PUT    /admin-api/{module}/{entity}/{id}/status

// ✅ 特殊操作
POST   /admin-api/orders/{id}/cancel
```

### 接口文档注解

```java
@RestController
@Tag(name = "管理后台 - {entity}")
@RequestMapping("/admin-api/{module}/{entity}")
@Validated
public class {Entity}Controller {

    @Operation(summary = "创建{entity}")
    @PostMapping("/create")
    @PreAuthorize("@ss.hasPermission('{module}:{entity}:create')")
    public CommonResult<Long> create(@Valid @RequestBody {Entity}SaveReqVO reqVO) {
        return success({entity}Service.create{Entity}(reqVO));
    }

    @Operation(summary = "分页查询{entity}")
    @GetMapping("/page")
    public CommonResult<PageResult<{Entity}RespVO>> getPage(@Valid {Entity}PageReqVO pageReqVO) {
        return success({Entity}RespVO.ofPage({entity}Service.get{Entity}Page(pageReqVO)));
    }
}
```

---

## 五、API 自检清单

```
版本管理：
□ 不兼容修改是否升级版本？
□ 旧版本是否标记 @Deprecated？

参数校验：
□ 必填参数有 @NotNull/@NotBlank？
□ 字符串有长度限制？
□ 数值有范围限制？
□ 嵌套对象有 @Valid？

响应格式：
□ 使用 CommonResult 包装？
□ 错误码符合规范？

安全：
□ 写接口有 @PreAuthorize？

文档：
□ 有 @Operation 描述？
□ 有 @Parameter 说明？
```