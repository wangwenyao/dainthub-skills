# 安全规范参考

> 按需加载。适用场景：认证、授权、JWT、OAuth2、权限模型设计。

---

## 一、认证机制

### JWT Token 结构

```
Header.Payload.Signature

Header:
{
  "alg": "RS256",
  "typ": "JWT"
}

Payload:
{
  "sub": "userId",           // 主题（用户ID）
  "iss": "dainthub",         // 签发者
  "aud": "admin-api",        // 接收方
  "exp": 1704067200,         // 过期时间（时间戳）
  "iat": 1704063600,         // 签发时间
  "jti": "unique-id",        // JWT ID（用于撤销）
  "username": "admin",
  "roles": ["ADMIN", "USER"]
}
```

### Token 存储策略

| 方式 | 安全性 | 适用场景 | 说明 |
|------|-------|---------|------|
| **HttpOnly Cookie** | 高 | Web 应用 | 防 XSS，需配合 CSRF 防护 |
| **Authorization Header** | 中 | API 服务 | Bearer Token，需防 XSS |
| **LocalStorage** | 低 | 不推荐 | 易受 XSS 攻击 |

```yaml
# Token 配置
{project}:
  security:
    token:
      header: Authorization
      secret: ${JWT_SECRET}           # 环境变量注入
      expire-time: 2h                 # Access Token 过期时间
      refresh-expire-time: 7d         # Refresh Token 过期时间
      issuer: dainthub
      cookie:
        name: auth_token
        http-only: true
        secure: true                  # HTTPS 环境
        same-site: strict
```

### Token 刷新机制

```java
@Service
@Slf4j
public class TokenService {

    @Value("${${project}.security.token.expire-time}")
    private Duration expireTime;

    /**
     * 创建 Access Token
     */
    public String createAccessToken(LoginUser loginUser) {
        return JwtUtils.createToken(
                Map.of(
                    "sub", loginUser.getId().toString(),
                    "username", loginUser.getUsername(),
                    "roles", loginUser.getRoleCodes()
                ),
                expireTime
        );
    }

    /**
     * 创建 Refresh Token
     */
    public String createRefreshToken(LoginUser loginUser) {
        String jti = UUID.randomUUID().toString();
        // 存储到 Redis，用于撤销
        String key = RedisKeyConstants.REFRESH_TOKEN + jti;
        RedisUtils.set(key, loginUser.getId(), Duration.ofDays(7));

        return JwtUtils.createToken(
                Map.of("sub", loginUser.getId().toString(), "jti", jti),
                Duration.ofDays(7)
        );
    }

    /**
     * 刷新 Token（Refresh Token 换 Access Token）
     */
    public TokenRespVO refreshToken(String refreshToken) {
        // 1. 验证 Refresh Token
        Claims claims = JwtUtils.parseToken(refreshToken);
        if (claims == null) {
            throw exception(REFRESH_TOKEN_INVALID);
        }

        // 2. 检查是否已撤销
        String jti = claims.get("jti", String.class);
        String key = RedisKeyConstants.REFRESH_TOKEN + jti;
        if (!RedisUtils.hasKey(key)) {
            throw exception(REFRESH_TOKEN_REVOKED);
        }

        // 3. 获取用户信息，生成新 Token
        Long userId = Long.parseLong(claims.getSubject());
        LoginUser loginUser = userService.getLoginUser(userId);

        String newAccessToken = createAccessToken(loginUser);
        String newRefreshToken = createRefreshToken(loginUser);

        // 4. 撤销旧 Refresh Token
        RedisUtils.delete(key);

        log.info("[refreshToken][Token刷新成功，userId={}]", userId);
        return new TokenRespVO(newAccessToken, newRefreshToken);
    }

    /**
     * 登出 - 撤销 Token
     */
    public void logout(String token) {
        Claims claims = JwtUtils.parseToken(token);
        if (claims != null) {
            String jti = claims.getId();
            // 将 Access Token 加入黑名单
            long ttl = claims.getExpiration().getTime() - System.currentTimeMillis();
            if (ttl > 0) {
                RedisUtils.set(RedisKeyConstants.TOKEN_BLACKLIST + jti, "1", Duration.ofMillis(ttl));
            }
            log.info("[logout][用户登出，jti={}]", jti);
        }
    }
}
```

---

## 二、授权模型

### RBAC 权限模型

```
用户(User) ──M:N──> 角色(Role) ──M:N──> 权限(Permission)

权限标识格式：{module}:{entity}:{operation}

示例：
  system:user:create     # 系统模块-用户-创建
  system:user:update     # 系统模块-用户-更新
  system:user:delete     # 系统模块-用户-删除
  system:user:query      # 系统模块-用户-查询
  trade:order:approve    # 交易模块-订单-审批
```

### 权限数据库设计

```sql
-- 用户表
CREATE TABLE `system_user` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `username` varchar(30) NOT NULL COMMENT '用户名',
  `password` varchar(100) NOT NULL COMMENT '密码（BCrypt加密）',
  `status` tinyint NOT NULL DEFAULT 0 COMMENT '状态（0=正常 1=禁用）',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`)
) COMMENT '用户表';

-- 角色表
CREATE TABLE `system_role` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(30) NOT NULL COMMENT '角色名称',
  `code` varchar(30) NOT NULL COMMENT '角色标识',
  `status` tinyint NOT NULL DEFAULT 0 COMMENT '状态（0=正常 1=禁用）',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_code` (`code`)
) COMMENT '角色表';

-- 权限表
CREATE TABLE `system_permission` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '权限名称',
  `code` varchar(100) NOT NULL COMMENT '权限标识',
  `type` tinyint NOT NULL COMMENT '类型（1=菜单 2=按钮 3=接口）',
  `parent_id` bigint DEFAULT NULL COMMENT '父权限ID',
  `path` varchar(200) DEFAULT NULL COMMENT '接口路径',
  PRIMARY KEY (`id`)
) COMMENT '权限表';

-- 用户角色关联表
CREATE TABLE `system_user_role` (
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `role_id` bigint NOT NULL COMMENT '角色ID',
  PRIMARY KEY (`user_id`, `role_id`)
) COMMENT '用户角色关联表';

-- 角色权限关联表
CREATE TABLE `system_role_permission` (
  `role_id` bigint NOT NULL COMMENT '角色ID',
  `permission_id` bigint NOT NULL COMMENT '权限ID',
  PRIMARY KEY (`role_id`, `permission_id`)
) COMMENT '角色权限关联表';
```

### 权限注解使用

```java
@RestController
@RequestMapping("/admin-api/{module}/{entity}")
public class {Entity}Controller {

    @PostMapping("/create")
    @Operation(summary = "创建{entity}")
    @PreAuthorize("@ss.hasPermission('{module}:{entity}:create')")  // 权限校验
    public CommonResult<Long> create(@RequestBody {Entity}SaveReqVO reqVO) {
        return success({entity}Service.create{Entity}(reqVO));
    }

    @PutMapping("/update")
    @Operation(summary = "更新{entity}")
    @PreAuthorize("@ss.hasPermission('{module}:{entity}:update')")
    public CommonResult<Boolean> update(@RequestBody {Entity}SaveReqVO reqVO) {
        {entity}Service.update{Entity}(reqVO);
        return success(true);
    }

    @DeleteMapping("/delete")
    @Operation(summary = "删除{entity}")
    @PreAuthorize("@ss.hasPermission('{module}:{entity}:delete')")
    public CommonResult<Boolean> delete(@RequestParam Long id) {
        {entity}Service.delete{Entity}(id);
        return success(true);
    }

    @GetMapping("/get")
    @Operation(summary = "查询{entity}")
    @PreAuthorize("@ss.hasPermission('{module}:{entity}:query')")
    public CommonResult<{Entity}RespVO> get(@RequestParam Long id) {
        return success({Entity}RespVO.of(
                {entity}Service.get{Entity}OrElse(id).orElse(null)));
    }

    // 多权限满足其一即可
    @GetMapping("/export")
    @PreAuthorize("@ss.hasAnyPermission('{module}:{entity}:export', '{module}:{entity}:query')")
    public void export({Entity}PageReqVO reqVO, HttpServletResponse response) {
        // ...
    }

    // 角色校验
    @GetMapping("/admin/list")
    @PreAuthorize("@ss.hasRole('ADMIN')")
    public CommonResult<List<{Entity}RespVO>> adminList() {
        // ...
    }
}
```

### 权限校验服务

```java
/**
 * Spring Security 权限校验服务（@ss.xxx() 中的 ss）
 */
@Component("ss")
public class PermissionService {

    @Resource
    private PermissionApi permissionApi;

    /**
     * 判断当前用户是否拥有指定权限
     */
    public boolean hasPermission(String permission) {
        LoginUser loginUser = SecurityUtils.getLoginUser();
        if (loginUser == null) {
            return false;
        }
        return loginUser.getPermissions().contains(permission);
    }

    /**
     * 判断当前用户是否拥有任一权限
     */
    public boolean hasAnyPermission(String... permissions) {
        LoginUser loginUser = SecurityUtils.getLoginUser();
        if (loginUser == null) {
            return false;
        }
        Set<String> userPerms = loginUser.getPermissions();
        return Arrays.stream(permissions).anyMatch(userPerms::contains);
    }

    /**
     * 判断当前用户是否拥有指定角色
     */
    public boolean hasRole(String role) {
        LoginUser loginUser = SecurityUtils.getLoginUser();
        if (loginUser == null) {
            return false;
        }
        return loginUser.getRoles().contains(role);
    }

    /**
     * 判断当前用户是否拥有任一角色
     */
    public boolean hasAnyRole(String... roles) {
        LoginUser loginUser = SecurityUtils.getLoginUser();
        if (loginUser == null) {
            return false;
        }
        Set<String> userRoles = loginUser.getRoles();
        return Arrays.stream(roles).anyMatch(userRoles::contains);
    }
}
```

---

## 三、密码安全

### 密码加密（BCrypt）

```java
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

@Configuration
public class SecurityConfig {

    @Bean
    public PasswordEncoder passwordEncoder() {
        // BCrypt 强度 10（默认），每次加密结果不同
        return new BCryptPasswordEncoder();
    }
}

@Service
public class UserServiceImpl implements UserService {

    @Resource
    private PasswordEncoder passwordEncoder;

    /**
     * 用户注册 - 密码加密
     */
    public Long register(UserRegisterReqVO reqVO) {
        // ✅ BCrypt 加密
        String encodedPassword = passwordEncoder.encode(reqVO.getPassword());
        user.setPassword(encodedPassword);
        userMapper.insert(user);
        return user.getId();
    }

    /**
     * 用户登录 - 密码验证
     */
    public LoginRespVO login(LoginReqVO reqVO) {
        UserDO user = userMapper.selectByUsername(reqVO.getUsername());
        if (user == null) {
            throw exception(USER_NOT_EXISTS);
        }

        // ✅ BCrypt 验证（防时序攻击）
        if (!passwordEncoder.matches(reqVO.getPassword(), user.getPassword())) {
            throw exception(PASSWORD_ERROR);
        }

        // 生成 Token
        String token = tokenService.createAccessToken(buildLoginUser(user));
        return new LoginRespVO(token);
    }

    /**
     * 修改密码 - 验证旧密码
     */
    public void updatePassword(Long userId, String oldPassword, String newPassword) {
        UserDO user = userMapper.selectById(userId);

        // 验证旧密码
        if (!passwordEncoder.matches(oldPassword, user.getPassword())) {
            throw exception(OLD_PASSWORD_ERROR);
        }

        // 新密码不能与旧密码相同
        if (passwordEncoder.matches(newPassword, user.getPassword())) {
            throw exception(NEW_PASSWORD_SAME_AS_OLD);
        }

        // 更新密码
        user.setPassword(passwordEncoder.encode(newPassword));
        userMapper.updateById(user);

        // 撤销所有 Token
        tokenService.revokeAllTokens(userId);
    }
}
```

### 密码强度校验

```java
/**
 * 密码强度校验
 * 规则：至少8位，包含大小写字母、数字、特殊字符中的3种
 */
public class PasswordValidator {

    private static final Pattern LOWER = Pattern.compile("[a-z]");
    private static final Pattern UPPER = Pattern.compile("[A-Z]");
    private static final Pattern DIGIT = Pattern.compile("[0-9]");
    private static final Pattern SPECIAL = Pattern.compile("[!@#$%^&*()_+\\-=\\[\\]{};':\"\\\\|,.<>/?]");

    public static boolean isValid(String password) {
        if (password == null || password.length() < 8 || password.length() > 32) {
            return false;
        }

        int count = 0;
        if (LOWER.matcher(password).find()) count++;
        if (UPPER.matcher(password).find()) count++;
        if (DIGIT.matcher(password).find()) count++;
        if (SPECIAL.matcher(password).find()) count++;

        return count >= 3;
    }
}

// 使用
@Test
void testPasswordStrength() {
    assertThat(PasswordValidator.isValid("Abc123!@")).isTrue();   // 满足4种
    assertThat(PasswordValidator.isValid("Abc12345")).isTrue();   // 满足3种
    assertThat(PasswordValidator.isValid("abc12345")).isFalse();  // 仅2种
    assertThat(PasswordValidator.isValid("12345678")).isFalse();  // 仅1种
}
```

---

## 四、敏感数据保护

### 数据脱敏

```java
/**
 * 敏感数据脱敏工具
 */
public final class SensitiveDataUtils {

    private SensitiveDataUtils() {}

    /**
     * 手机号脱敏：138****0000
     */
    public static String maskMobile(String mobile) {
        if (StrUtil.isBlank(mobile) || mobile.length() < 7) {
            return mobile;
        }
        return mobile.substring(0, 3) + "****" + mobile.substring(mobile.length() - 4);
    }

    /**
     * 身份证脱敏：110***********1234
     */
    public static String maskIdCard(String idCard) {
        if (StrUtil.isBlank(idCard) || idCard.length() < 8) {
            return idCard;
        }
        return idCard.substring(0, 3) + "***********" + idCard.substring(idCard.length() - 4);
    }

    /**
     * 银行卡脱敏：6222 **** **** 1234
     */
    public static String maskBankCard(String bankCard) {
        if (StrUtil.isBlank(bankCard) || bankCard.length() < 8) {
            return bankCard;
        }
        return bankCard.substring(0, 4) + " **** **** " + bankCard.substring(bankCard.length() - 4);
    }

    /**
     * 邮箱脱敏：a***@example.com
     */
    public static String maskEmail(String email) {
        if (StrUtil.isBlank(email) || !email.contains("@")) {
            return email;
        }
        int atIndex = email.indexOf("@");
        if (atIndex <= 1) {
            return email;
        }
        return email.charAt(0) + "***" + email.substring(atIndex);
    }

    /**
     * 姓名脱敏：张*
     */
    public static String maskName(String name) {
        if (StrUtil.isBlank(name)) {
            return name;
        }
        return name.charAt(0) + StrUtil.repeat("*", name.length() - 1);
    }
}
```

### 敏感字段加密存储

```java
/**
 * 使用 MyBatis Plus 字段加密
 */
@TableName("system_user")
@Data
public class UserDO extends BaseDO {

    private Long id;

    private String username;

    /**
     * 手机号（加密存储）
     */
    @TableField(typeHandler = EncryptTypeHandler.class)
    private String mobile;

    /**
     * 身份证号（加密存储）
     */
    @TableField(typeHandler = EncryptTypeHandler.class)
    private String idCard;
}

/**
 * 加密类型处理器
 */
@Slf4j
public class EncryptTypeHandler extends BaseTypeHandler<String> {

    private static final String SECRET_KEY = "your-secret-key-16"; // 16字节

    @Override
    public void setNonNullParameter(PreparedStatement ps, int i, String parameter, JdbcType jdbcType)
            throws SQLException {
        // AES 加密
        ps.setString(i, SecureUtil.aes(SECRET_KEY.getBytes()).encryptHex(parameter));
    }

    @Override
    public String getNullableResult(ResultSet rs, String columnName) throws SQLException {
        String value = rs.getString(columnName);
        if (StrUtil.isBlank(value)) {
            return value;
        }
        // AES 解密
        return SecureUtil.aes(SECRET_KEY.getBytes()).decryptStr(value);
    }
}
```

---

## 五、安全约束

### 安全约束总表

| ID | 规则 |
|----|------|
| C-SEC-001 | 密码必须使用 BCrypt 加密存储，禁止明文或 MD5 |
| C-SEC-002 | Token 有效期不超过 2 小时，Refresh Token 不超过 7 天 |
| C-SEC-003 | 敏感字段（手机号、身份证、银行卡）必须加密存储 |
| C-SEC-004 | 敏感数据返回前端前必须脱敏（日志、接口响应） |
| C-SEC-005 | 所有写操作接口必须有权限校验（@PreAuthorize） |
| C-SEC-006 | 密码强度：至少8位，包含大小写字母、数字、特殊字符中的3种 |
| C-SEC-007 | 登录失败超过5次锁定账户15分钟（防暴力破解） |
| C-SEC-008 | JWT Secret 必须从环境变量注入，禁止硬编码 |
| C-SEC-009 | 生产环境必须使用 HTTPS，Cookie 设置 Secure 属性 |
| C-SEC-010 | SQL 查询禁止拼接用户输入，必须使用 `#{}` 预编译 |

### 安全自检清单

```
认证层：
□ 密码使用 BCrypt 加密
□ Token 有效期配置合理
□ Refresh Token 机制可用
□ 登出后 Token 撤销

授权层：
□ 所有写接口有 @PreAuthorize
□ 权限标识格式正确（{module}:{entity}:{operation}）
□ 角色权限数据初始化完整

数据安全：
□ 敏感字段加密存储
□ 敏感数据返回前脱敏
□ 日志不含密码明文
□ 生产环境禁用测试账号

防护措施：
□ 登录失败次数限制
□ 验证码机制可用
□ SQL 注入防护（预编译）
□ XSS 防护（输出转义）
```

---

## 六、常见安全漏洞防护

### SQL 注入

```java
// ❌ 错误：拼接 SQL
@Select("SELECT * FROM user WHERE name = '" + name + "'")
UserDO selectByName(String name);

// ✅ 正确：预编译参数
@Select("SELECT * FROM user WHERE name = #{name}")
UserDO selectByName(String name);

// ✅ XML 中使用 #{} 而非 ${}
<select id="selectByName" resultType="UserDO">
    SELECT * FROM user WHERE name = #{name}  <!-- 安全 -->
</select>

// ⚠️ ${} 仅用于动态表名/列名（非用户输入）
<select id="selectByTable" resultType="UserDO">
    SELECT * FROM ${tableName} WHERE status = 1
</select>
```

### XSS 攻击

```java
// ✅ 输出转义（前端）
// 使用 Vue/React 自动转义，或使用 DOMPurify

// ✅ 后端存储前过滤
import org.jsoup.Jsoup;
import org.jsoup.safety.Safelist;

public class XssUtils {

    /**
     * 清理 HTML 标签，只保留安全标签
     */
    public static String cleanHtml(String html) {
        return Jsoup.clean(html, Safelist.relaxed());
    }

    /**
     * 清除所有 HTML 标签
     */
    public static String stripHtml(String html) {
        return Jsoup.clean(html, Safelist.none());
    }
}
```

### CSRF 攻击

```java
// 方式1：Spring Security CSRF 防护（默认开启）
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.csrf(csrf -> csrf
                .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
        );
        return http.build();
    }
}

// 方式2：前后端分离使用 Token 认证，天然防 CSRF
// Token 存储在 HttpOnly Cookie 中，每次请求携带
```

### 越权访问

```java
// ❌ 错误：直接使用用户传入的 ID
@GetMapping("/order/detail")
public CommonResult<OrderRespVO> getOrderDetail(@RequestParam Long orderId) {
    return success(orderService.getById(orderId));  // 可能越权！
}

// ✅ 正确：校验数据归属
@GetMapping("/order/detail")
public CommonResult<OrderRespVO> getOrderDetail(@RequestParam Long orderId) {
    Long currentUserId = SecurityUtils.getLoginUser().getId();
    OrderDO order = orderService.getById(orderId);

    // 校验数据归属
    if (!order.getUserId().equals(currentUserId)) {
        throw exception(ORDER_NOT_EXISTS);  // 返回不存在而非无权限
    }

    return success(OrderRespVO.of(order));
}

// ✅ 数据层自动过滤
@Mapper
public interface OrderMapper extends BaseMapperX<OrderDO> {

    /**
     * 查询用户的订单（自动过滤 userId）
     */
    default OrderDO selectUserOrder(Long userId, Long orderId) {
        return selectOne(new LambdaQueryWrapper<OrderDO>()
                .eq(OrderDO::getId, orderId)
                .eq(OrderDO::getUserId, userId));  // 自动归属校验
    }
}
```