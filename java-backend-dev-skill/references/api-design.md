# API 设计规范参考

> 按需加载。适用场景：API 版本管理、参数校验、接口设计、响应格式。

---

## 一、API 版本管理

### 版本策略选择

| 策略 | 实现方式 | 优点 | 缺点 | 推荐场景 |
|------|---------|------|------|---------|
| **URL Path** | `/v1/orders` | 简单直观，易于缓存 | URL 耦合版本 | 公开 API、外部服务 |
| **Header** | `Accept: vnd.api.v1+json` | URL 干净 | 客户端复杂，缓存难 | 内部服务 |
| **Query** | `/orders?version=1` | 灵活 | 易被忽略 | 不推荐 |

**本项目采用 URL Path 版本策略**。

### 版本规则

```
版本号格式：v{major}

/v1/orders   → 版本 1
/v2/orders   → 版本 2

规则：
1. major 版本变更：不兼容的接口修改（删除字段、修改字段类型、修改响应结构）
2. minor 版本变更：兼容的接口修改（新增字段、新增接口、新增可选参数）→ 不升级版本号
3. 一个 major 版本内保持向后兼容
```

### 版本共存策略

```java
// 方式1：不同版本使用不同 Controller
@RestController
@RequestMapping("/admin-api/v1/orders")
@Tag(name = "管理后台 - 订单 V1")
public class OrderControllerV1 {
    // v1 实现
}

@RestController
@RequestMapping("/admin-api/v2/orders")
@Tag(name = "管理后台 - 订单 V2")
public class OrderControllerV2 {
    // v2 实现（新增字段、优化响应结构）
}

// 方式2：同一 Controller 内不同方法
@RestController
@RequestMapping("/admin-api/orders")
public class OrderController {

    @GetMapping("/v1/detail")
    @Operation(summary = "订单详情 V1（已废弃）", deprecated = true)
    @Deprecated
    public CommonResult<OrderRespV1VO> getDetailV1(@RequestParam Long id) {
        return success(orderService.getDetailV1(id));
    }

    @GetMapping("/v2/detail")
    @Operation(summary = "订单详情 V2")
    public CommonResult<OrderRespV2VO> getDetailV2(@RequestParam Long id) {
        return success(orderService.getDetailV2(id));
    }
}
```

### 版本废弃策略

```java
// Step 1：标记废弃（保留 3 个月）
@GetMapping("/v1/detail")
@Operation(summary = "订单详情 V1（已废弃，请使用 V2）", deprecated = true)
@Deprecated
public CommonResult<OrderRespV1VO> getDetailV1(@RequestParam Long id) {
    // 返回响应头提示废弃
    HttpServletResponse response = getCurrentResponse();
    response.setHeader("X-API-Deprecated", "true");
    response.setHeader("X-API-Sunset", "2024-06-01");  // 下线日期
    response.setHeader("X-API-Replacement", "/admin-api/v2/orders/detail");
    return success(orderService.getDetailV1(id));
}

// Step 2：返回警告（废弃后 1 个月）
@GetMapping("/v1/detail")
@Deprecated
public CommonResult<OrderRespV1VO> getDetailV1(@RequestParam Long id) {
    // 返回特殊响应码
    return CommonResult.warn("API_DEPRECATED", "接口已废弃，请迁移到 V2");
}

// Step 3：下线（废弃后 3 个月）
@GetMapping("/v1/detail")
@Deprecated
public CommonResult<OrderRespV1VO> getDetailV1(@RequestParam Long id) {
    throw exception(API_DEPRECATED, "接口已下线，请使用 /v2/orders/detail");
}
```

### 版本兼容性规则

```
兼容修改（无需升级版本）：
✅ 新增可选请求参数
✅ 新增响应字段
✅ 新增接口
✅ 枚举新增值

不兼容修改（必须升级版本）：
❌ 删除请求参数
❌ 删除响应字段
❌ 修改字段类型
❌ 修改字段名称
❌ 修改必填属性
❌ 修改响应结构
❌ 枚举删除值
```

---

## 二、参数校验

### JSR-303 校验注解

```java
import jakarta.validation.constraints.*;
import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "管理后台 - {entity}新增/修改 Request VO")
@Data
public class {Entity}SaveReqVO {

    @Schema(description = "主键（更新时必传）", example = "1024")
    private Long id;

    // ── 字符串校验 ────────────────────────────────

    @Schema(description = "名称", requiredMode = Schema.RequiredMode.REQUIRED)
    @NotBlank(message = "名称不能为空")
    @Size(min = 2, max = 64, message = "名称长度必须在 {min}-{max} 个字符之间")
    private String name;

    @Schema(description = "邮箱")
    @Email(message = "邮箱格式不正确")
    private String email;

    @Schema(description = "手机号")
    @Pattern(regexp = "^1[3-9]\\d{9}$", message = "手机号格式不正确")
    private String mobile;

    // ── 数值校验 ──────────────────────────────────

    @Schema(description = "年龄")
    @Min(value = 0, message = "年龄不能小于 {value}")
    @Max(value = 150, message = "年龄不能超过 {value}")
    private Integer age;

    @Schema(description = "数量")
    @NotNull(message = "数量不能为空")
    @Positive(message = "数量必须为正数")
    private Integer quantity;

    @Schema(description = "金额")
    @DecimalMin(value = "0.01", message = "金额必须大于 0")
    @DecimalMax(value = "99999999.99", message = "金额超出限制")
    private BigDecimal amount;

    // ── 集合校验 ──────────────────────────────────

    @Schema(description = "标签列表")
    @NotEmpty(message = "标签列表不能为空")
    @Size(min = 1, max = 10, message = "标签数量必须在 {min}-{max} 个之间")
    private List<@NotBlank(message = "标签不能为空") String> tags;

    // ── 日期校验 ──────────────────────────────────

    @Schema(description = "开始时间")
    @NotNull(message = "开始时间不能为空")
    private LocalDateTime startTime;

    @Schema(description = "结束时间")
    @NotNull(message = "结束时间不能为空")
    private LocalDateTime endTime;

    // ── 嵌套对象校验 ──────────────────────────────

    @Schema(description = "地址信息")
    @Valid  // 启用嵌套校验
    @NotNull(message = "地址信息不能为空")
    private AddressVO address;
}
```

### 分组校验

```java
// 定义校验分组
public interface CreateGroup {}
public interface UpdateGroup {}

@Schema(description = "{entity}保存请求 VO")
@Data
public class {Entity}SaveReqVO {

    @Schema(description = "主键")
    @NotNull(message = "主键不能为空", groups = UpdateGroup.class)  // 更新时必填
    @Null(message = "主键必须为空", groups = CreateGroup.class)    // 创建时必须为空
    private Long id;

    @Schema(description = "名称")
    @NotBlank(message = "名称不能为空")
    private String name;
}

// Controller 中使用分组
@PostMapping("/create")
@Operation(summary = "创建{entity}")
public CommonResult<Long> create(@Validated(CreateGroup.class) @RequestBody {Entity}SaveReqVO reqVO) {
    return success({entity}Service.create{Entity}(reqVO));
}

@PutMapping("/update")
@Operation(summary = "更新{entity}")
public CommonResult<Boolean> update(@Validated(UpdateGroup.class) @RequestBody {Entity}SaveReqVO reqVO) {
    {entity}Service.update{Entity}(reqVO);
    return success(true);
}
```

### 自定义校验注解

```java
/**
 * 枚举值校验注解
 */
@Target({Method, Field, Parameter})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = InEnumValidator.class)
public @interface InEnum {

    String message() default "值不在有效枚举范围内";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};

    /**
     * 枚举类
     */
    Class<? extends Enum<?>> value();

    /**
     * 枚举值获取方法，默认为 "getValue"
     */
    String method() default "getValue";
}

/**
 * 枚举值校验器
 */
public class InEnumValidator implements ConstraintValidator<InEnum, Object> {

    private List<Object> values;

    @Override
    public void initialize(InEnum annotation) {
        Class<? extends Enum<?>> enumClass = annotation.value();
        String method = annotation.method();

        try {
            Method getValue = enumClass.getMethod(method);
            values = Arrays.stream(enumClass.getEnumConstants())
                    .map(e -> {
                        try {
                            return getValue.invoke(e);
                        } catch (Exception ex) {
                            throw new RuntimeException(ex);
                        }
                    })
                    .collect(Collectors.toList());
        } catch (NoSuchMethodException e) {
            throw new RuntimeException("枚举类 " + enumClass.getName() + " 不存在方法 " + method, e);
        }
    }

    @Override
    public boolean isValid(Object value, ConstraintValidatorContext context) {
        if (value == null) {
            return true;  // null 由 @NotNull/@NotBlank 处理
        }
        return values.contains(value);
    }
}

// 使用自定义注解
@Schema(description = "状态")
@InEnum(value = {Entity}StatusEnum.class, message = "状态值不合法")
private Integer status;
```

### 手动校验

```java
@Service
@Validated  // 启用方法级别校验
public class {Entity}ServiceImpl implements {Entity}Service {

    /**
     * 业务校验：名称唯一性
     */
    private void validateNameUnique(Long id, String name) {
        {Entity}DO existing = {entity}Mapper.selectByName(name);
        if (existing != null && (id == null || !existing.getId().equals(id))) {
            throw exception({ENTITY}_NAME_DUPLICATE);
        }
    }

    /**
     * 方法参数校验（需 @Validated）
     */
    public void updateStatus(@NotNull(message = "ID不能为空") Long id,
                             @Min(value = 0, message = "状态值不合法") @Max(value = 1, message = "状态值不合法") Integer status) {
        // ...
    }
}
```

### 时间范围校验

```java
/**
 * 时间范围校验注解
 */
@Target({Type})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = TimeRangeValidator.class)
public @interface ValidTimeRange {

    String message() default "开始时间不能晚于结束时间";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};

    String startTimeField() default "startTime";

    String endTimeField() default "endTime";
}

/**
 * 时间范围校验器
 */
public class TimeRangeValidator implements ConstraintValidator<ValidTimeRange, Object> {

    private String startTimeField;
    private String endTimeField;

    @Override
    public void initialize(ValidTimeRange annotation) {
        this.startTimeField = annotation.startTimeField();
        this.endTimeField = annotation.endTimeField();
    }

    @Override
    public boolean isValid(Object obj, ConstraintValidatorContext context) {
        try {
            BeanWrapper beanWrapper = new BeanWrapperImpl(obj);
            LocalDateTime startTime = (LocalDateTime) beanWrapper.getPropertyValue(startTimeField);
            LocalDateTime endTime = (LocalDateTime) beanWrapper.getPropertyValue(endTimeField);

            if (startTime == null || endTime == null) {
                return true;  // null 由其他注解处理
            }

            return !startTime.isAfter(endTime);
        } catch (Exception e) {
            return false;
        }
    }
}

// 使用
@ValidTimeRange(message = "创建时间范围：开始时间不能晚于结束时间")
@Schema(description = "{entity}分页查询请求 VO")
@Data
public class {Entity}PageReqVO extends PageParam {

    @Schema(description = "创建时间-开始")
    private LocalDateTime startTime;

    @Schema(description = "创建时间-结束")
    private LocalDateTime endTime;
}
```

---

## 三、响应格式规范

### 统一响应结构

```java
/**
 * 通用响应结果
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class CommonResult<T> {

    /** 状态码（0=成功，非0=失败） */
    private Integer code;

    /** 消息 */
    private String msg;

    /** 数据 */
    private T data;

    /** 时间戳 */
    private Long timestamp;

    public static <T> CommonResult<T> success(T data) {
        return new CommonResult<>(0, "success", data, System.currentTimeMillis());
    }

    public static <T> CommonResult<T> success() {
        return success(null);
    }

    public static <T> CommonResult<T> error(Integer code, String msg) {
        return new CommonResult<>(code, msg, null, System.currentTimeMillis());
    }

    public static <T> CommonResult<T> error(ErrorCode errorCode) {
        return error(errorCode.getCode(), errorCode.getMsg());
    }

    public static <T> CommonResult<T> warn(String msg) {
        return new CommonResult<>(CommonCodeEnum.WARN.getCode(), msg, null, System.currentTimeMillis());
    }
}
```

### 分页响应结构

```java
/**
 * 分页结果
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class PageResult<T> {

    /** 数据列表 */
    private List<T> list;

    /** 总数 */
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
 * 错误码规则：
 * - 格式：1 + 模块3位 + 业务3位
 * - 模块码：system=001, member=002, infra=003, product=004, trade=005
 *
 * 示例：
 * - 1001001 = 系统模块-用户不存在
 * - 1005001 = 交易模块-订单不存在
 */
public interface ErrorCodeConstants {

    // ── 通用错误（1-000-xxx）───────────────────────
    ErrorCode BAD_REQUEST         = new ErrorCode(1000000, "请求参数不正确");
    ErrorCode UNAUTHORIZED        = new ErrorCode(1000001, "未登录或登录已过期");
    ErrorCode FORBIDDEN           = new ErrorCode(1000002, "无权限访问");
    ErrorCode NOT_FOUND           = new ErrorCode(1000003, "请求资源不存在");
    ErrorCode METHOD_NOT_ALLOWED  = new ErrorCode(1000004, "请求方法不允许");
    ErrorCode INTERNAL_ERROR      = new ErrorCode(1000005, "系统异常");

    // ── 系统模块（1-001-xxx）───────────────────────
    ErrorCode USER_NOT_EXISTS     = new ErrorCode(1001001, "用户不存在");
    ErrorCode USER_PASSWORD_ERROR = new ErrorCode(1001002, "密码错误");
    ErrorCode USER_DISABLED       = new ErrorCode(1001003, "用户已被禁用");

    // ── 业务模块（1-xxx-xxx）───────────────────────
    ErrorCode {ENTITY}_NOT_EXISTS     = new ErrorCode(1{MODULE_CODE}001, "{entity}不存在");
    ErrorCode {ENTITY}_NAME_DUPLICATE = new ErrorCode(1{MODULE_CODE}002, "{entity}名称已存在");
}
```

---

## 四、API 设计最佳实践

### RESTful 规范

```java
// ✅ 正确的 RESTful 设计
GET    /admin-api/{module}/{entity}         // 列表查询
GET    /admin-api/{module}/{entity}/{id}    // 详情查询
POST   /admin-api/{module}/{entity}         // 创建
PUT    /admin-api/{module}/{entity}/{id}    // 更新（全量）
PATCH  /admin-api/{module}/{entity}/{id}    // 更新（部分）
DELETE /admin-api/{module}/{entity}/{id}    // 删除

// ✅ 批量操作
POST   /admin-api/{module}/{entity}/batch-create    // 批量创建
DELETE /admin-api/{module}/{entity}/batch-delete    // 批量删除

// ✅ 状态变更
PUT    /admin-api/{module}/{entity}/{id}/status    // 更新状态

// ✅ 特殊操作
POST   /admin-api/orders/{id}/cancel              // 取消订单
POST   /admin-api/orders/{id}/approve             // 审批订单
```

### 接口文档注解

```java
@RestController
@Tag(name = "管理后台 - {entity}")
@RequestMapping("/admin-api/{module}/{entity}")
@Validated
public class {Entity}Controller {

    @Operation(summary = "创建{entity}", description = "创建新的{entity}记录")
    @Parameter(name = "id", description = "主键", required = true, example = "1024")
    @ApiResponse(responseCode = "200", description = "成功")
    @ApiResponse(responseCode = "400", description = "参数错误")
    @ApiResponse(responseCode = "401", description = "未登录")
    @ApiResponse(responseCode = "403", description = "无权限")
    @PostMapping("/create")
    @PreAuthorize("@ss.hasPermission('{module}:{entity}:create')")
    public CommonResult<Long> create(
            @Valid @RequestBody {Entity}SaveReqVO reqVO) {
        return success({entity}Service.create{Entity}(reqVO));
    }

    @Operation(summary = "分页查询{entity}")
    @GetMapping("/page")
    public CommonResult<PageResult<{Entity}RespVO>> getPage(
            @Valid {Entity}PageReqVO pageReqVO) {
        return success({Entity}RespVO.ofPage(
                {entity}Service.get{Entity}Page(pageReqVO)));
    }
}
```

### API 自检清单

```
版本管理：
□ 是否需要新增版本（不兼容修改）？
□ 旧版本是否标记 @Deprecated？
□ 是否设置了 Sunset 响应头？

参数校验：
□ 必填参数是否有 @NotNull/@NotBlank？
□ 字符串是否有长度限制？
□ 数值是否有范围限制？
□ 嵌套对象是否有 @Valid？
□ 自定义校验是否实现？

响应格式：
□ 是否使用 CommonResult 包装？
□ 错误码是否符合规范？
□ 分页是否使用 PageResult？

安全：
□ 写接口是否有 @PreAuthorize？
□ 权限标识格式是否正确？

文档：
□ 是否有 @Operation 描述？
□ 是否有 @Parameter 说明？
□ 是否有 @ApiResponse 定义？
```