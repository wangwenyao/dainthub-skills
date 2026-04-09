# 代码模板

> 本文件包含各分层的完整代码模板，由 SKILL.md 按需引用。
> 占位符说明：`{project}` = 项目标识符，`{module}` = 模块名，`{entity}` = 实体名（PascalCase），`{entity_snake}` = 实体名（snake_case，用于表名/URL）。

---

## DO 层（领域对象）

```java
package com.dainthub.{project}.module.{module}.dal.dataobject.{entity_snake};

// 导入顺序：JDK → 第三方 → 项目内部（各组之间空一行）
import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.*;

import java.util.Comparator;
import java.util.function.Function;

@TableName("{module}_{entity_snake}")
@Data
@EqualsAndHashCode(callSuper = true)
@ToString(callSuper = true)
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class {Entity}DO extends BaseDO {

    /** 主键 */
    @TableId(type = IdType.AUTO)
    private Long id;

    /**
     * 名称（必须写 Javadoc，说明约束范围）
     * 非空，最大 64 字符
     */
    private String name;

    /**
     * 状态
     * @see {Entity}StatusEnum
     */
    private Integer status;

    /**
     * 排序值（升序，值越小越靠前）
     */
    private Integer sortOrder;

    // ==================== 充血模型业务方法（C-ARCH-005）====================

    /**
     * 判断当前实体是否处于启用状态。
     * 仅依赖 DO 自身字段，合法的充血方法（C-ARCH-005）。
     */
    public boolean isEnabled() {
        return {Entity}StatusEnum.ENABLE.getStatus().equals(this.status);
    }

    /**
     * 将 SaveReqVO 的变更应用到当前 DO（更新场景增量覆盖）。
     * 依赖 VO 类型（非 Service/Mapper），合法（C-ARCH-005）。
     */
    public void applyUpdate({Entity}SaveReqVO reqVO) {
        this.name      = reqVO.getName();
        this.status    = reqVO.getStatus();
        this.sortOrder = reqVO.getSortOrder();
    }

    // ==================== 静态排序 Comparator（C-ARCH-006）====================

    /**
     * 按 sortOrder 升序排序（排序逻辑定义在 DO 中，C-ARCH-006）
     * 使用方式：list.sort({Entity}DO.BY_SORT_ASC)
     *          list.stream().sorted({Entity}DO.BY_SORT_ASC)
     */
    public static final Comparator<{Entity}DO> BY_SORT_ASC =
            Comparator.comparingInt({Entity}DO::getSortOrder);

    /**
     * 按 sortOrder 升序、createTime 降序的复合排序
     */
    public static final Comparator<{Entity}DO> BY_SORT_THEN_LATEST =
            Comparator.comparingInt({Entity}DO::getSortOrder)
                      .thenComparing(Comparator.comparing(BaseDO::getCreateTime).reversed());

    /**
     * 按 id 提取的 Function，用于 Collectors.toMap 等 Stream 操作
     */
    public static final Function<{Entity}DO, Long> KEY_BY_ID = {Entity}DO::getId;
}
```

---

## VO 层（含转换方法）

**转换职责（C-ARCH-003）**：VO 持有全部转换方法，Service/Controller 中不出现批量 setter。

```java
package com.dainthub.{project}.module.{module}.controller.admin.vo.{entity_snake};

// ① 创建/更新请求 VO
@Schema(description = "管理后台 - {entity}新增/修改 Request VO")
@Data
public class {Entity}SaveReqVO {

    @Schema(description = "主键（更新时必传，创建时不传）", example = "1024")
    private Long id;

    @Schema(description = "名称", requiredMode = Schema.RequiredMode.REQUIRED)
    @NotBlank(message = "名称不能为空")
    @Size(max = 64, message = "名称长度不能超过 64 个字符")
    private String name;

    @Schema(description = "状态（0=禁用 1=启用）", requiredMode = Schema.RequiredMode.REQUIRED)
    @NotNull(message = "状态不能为空")
    private Integer status;

    @Schema(description = "排序值", example = "0")
    @NotNull(message = "排序值不能为空")
    private Integer sortOrder;

    /**
     * 转换为新建 DO（C-ARCH-003，命名 toEntity，C-CODE-001：无数组）
     */
    public {Entity}DO toEntity() {
        {Entity}DO entity = new {Entity}DO();
        entity.setName(this.name);
        entity.setStatus(this.status);
        entity.setSortOrder(this.sortOrder);
        return entity;
    }
}

// ② 分页查询请求 VO
@Schema(description = "管理后台 - {entity}分页查询 Request VO")
@Data
@EqualsAndHashCode(callSuper = true)
public class {Entity}PageReqVO extends PageParam {

    @Schema(description = "名称（模糊匹配）")
    private String name;

    @Schema(description = "状态")
    private Integer status;

    /**
     * 创建时间范围-开始
     */
    @Schema(description = "创建时间-开始")
    private LocalDateTime startTime;

    /**
     * 创建时间范围-结束
     */
    @Schema(description = "创建时间-结束")
    private LocalDateTime endTime;
}

// ③ 响应 VO（持有 DO→VO 转换方法，C-ARCH-003）
@Schema(description = "管理后台 - {entity}响应 VO")
@Data
public class {Entity}RespVO {

    @Schema(description = "主键", example = "1024")
    private Long id;

    @Schema(description = "名称")
    private String name;

    @Schema(description = "状态（0=禁用 1=启用）")
    private Integer status;

    @Schema(description = "排序值")
    private Integer sortOrder;

    @Schema(description = "创建时间")
    private LocalDateTime createTime;

    /** 单条转换（null 安全） */
    public static {Entity}RespVO of({Entity}DO entity) {
        if (entity == null) {
            return null;
        }
        {Entity}RespVO vo = new {Entity}RespVO();
        vo.setId(entity.getId());
        vo.setName(entity.getName());
        vo.setStatus(entity.getStatus());
        vo.setSortOrder(entity.getSortOrder());
        vo.setCreateTime(entity.getCreateTime());
        return vo;
    }

    /**
     * 列表转换（Stream 静态方法定义在 Bean 中，C-ARCH-003）
     * Hutool CollUtil 防 null/empty（C-CODE-004）
     */
    public static List<{Entity}RespVO> ofList(List<{Entity}DO> entities) {
        if (CollUtil.isEmpty(entities)) {
            return Collections.emptyList();
        }
        return entities.stream()
                .map({Entity}RespVO::of)
                .collect(Collectors.toList());
    }

    /** 按 DO 排序后转换（使用 DO 的静态 Comparator，C-ARCH-006） */
    public static List<{Entity}RespVO> ofListSorted(List<{Entity}DO> entities) {
        if (CollUtil.isEmpty(entities)) {
            return Collections.emptyList();
        }
        return entities.stream()
                .sorted({Entity}DO.BY_SORT_ASC)
                .map({Entity}RespVO::of)
                .collect(Collectors.toList());
    }

    /** 分页转换 */
    public static PageResult<{Entity}RespVO> ofPage(PageResult<{Entity}DO> page) {
        return new PageResult<>(ofList(page.getList()), page.getTotal());
    }

    /** 按 id 索引的 Map（O(1) 检索，避免 N+1） */
    public static Map<Long, {Entity}RespVO> indexById(List<{Entity}DO> entities) {
        if (CollUtil.isEmpty(entities)) {
            return Collections.emptyMap();
        }
        return entities.stream()
                .map({Entity}RespVO::of)
                .collect(Collectors.toMap({Entity}RespVO::getId, Function.identity()));
    }
}
```

---

## Mapper 层

```java
package com.dainthub.{project}.module.{module}.dal.mysql.{entity_snake};

@Mapper
public interface {Entity}Mapper extends BaseMapperX<{Entity}DO> {

    // ---- 简单查询：default 方法（单表，条件简单）----

    /**
     * 分页查询（条件构造在 Mapper，Service 只传 VO — C-ARCH-002）
     */
    default PageResult<{Entity}DO> selectPage({Entity}PageReqVO reqVO) {
        return selectPage(reqVO, new LambdaQueryWrapperX<{Entity}DO>()
                .likeIfPresent({Entity}DO::getName, reqVO.getName())
                .eqIfPresent({Entity}DO::getStatus, reqVO.getStatus())
                .geIfPresent({Entity}DO::getCreateTime, reqVO.getStartTime())
                .leIfPresent({Entity}DO::getCreateTime, reqVO.getEndTime())
                .orderByAsc({Entity}DO::getSortOrder)
                .orderByDesc({Entity}DO::getId));
    }

    /**
     * 按名称精确查询（用于 exist{Entity}Name 唯一性校验）
     */
    default {Entity}DO selectByName(String name) {
        return selectOne({Entity}DO::getName, name);
    }

    /**
     * 按 ID 批量查询，返回 Map 方便 O(1) 检索，避免 N+1（C-DATA-002）
     */
    default Map<Long, {Entity}DO> selectMapByIds(Collection<Long> ids) {
        if (CollUtil.isEmpty(ids)) {
            return Collections.emptyMap();
        }
        return selectBatchIds(ids).stream()
                .collect(Collectors.toMap({Entity}DO::getId, Function.identity()));
    }

    // ---- 复杂查询：XML 实现（多表 JOIN / GROUP BY / 子查询）----

    /**
     * 自定义关联统计查询（实现见 Mapper.xml）
     * 参数超 3 个时封装为 VO 传入（C-CODE-007）
     */
    List<{Entity}StatDO> selectStatByCondition({Entity}StatQueryReqVO reqVO);
}
```

**Mapper.xml（复杂查询，C-DATA-003）**：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.dainthub.{project}.module.{module}.dal.mysql.{entity_snake}.{Entity}Mapper">

<!--
       C-DATA-003：统一定义列 SQL 片段，所有 SELECT 通过 <include> 引用
       禁止在各 SQL 语句中直接写列名或 SELECT *
    -->
    <sql id="columns">
        id, name, status, sort_order,
        creator, create_time, updater, update_time, deleted
    </sql>

    <!-- ResultMap：仅在字段名无法自动驼峰映射时定义 -->
    <resultMap id="StatResultMap" type="...{Entity}StatDO">
        <result column="category_id"  property="categoryId"/>
        <result column="total_count"  property="totalCount"/>
    </resultMap>

    <!--
      使用 <include refid="columns"/> 引用列片段
      <where> + <if> 替代手拼 WHERE 1=1
      #{} 防注入，禁止 ${}
    -->
    <select id="selectStatByCondition" resultMap="StatResultMap">
        SELECT
            e.category_id,
            COUNT(e.id) AS total_count
        FROM {module}_{entity_snake} e
            LEFT JOIN {module}_category c ON c.id = e.category_id AND c.deleted = 0
        <where>
            e.deleted = 0
            <if test="reqVO.startTime != null">AND e.create_time &gt;= #{reqVO.startTime}</if>
            <if test="reqVO.endTime   != null">AND e.create_time &lt;= #{reqVO.endTime}</if>
            <if test="reqVO.status    != null">AND e.status = #{reqVO.status}</if>
        </where>
        GROUP BY e.category_id
        ORDER BY total_count DESC
    </select>

    <!-- 单表查询复用 columns 片段示例 -->
    <select id="selectByCondition" resultType="{Entity}DO">
        SELECT <include refid="columns"/>
        FROM {module}_{entity_snake}
        <where>
            deleted = 0
            <if test="name != null and name != ''">AND name LIKE CONCAT('%', #{name}, '%')</if>
        </where>
    </select>

</mapper>
```

---

## ErrorCode 定义

```java
package com.dainthub.{project}.module.{module}.enums;

import static com.dainthub.{project}.framework.common.exception.util.ServiceExceptionUtil.exception;

/**
 * 错误码规则：1 + 模块3位码 + 业务序号3位
 * 模块码示例：system=001, infra=002, member=004, product=005, trade=010
 *
 * 使用 interface 而非 class：字段默认 public static final，无需显式修饰符。
 */
public interface ErrorCodeConstants {

    ErrorCode {ENTITY}_NOT_EXISTS     = new ErrorCode(1_{MODULE_CODE}_001, "{entity}不存在");
    ErrorCode {ENTITY}_NAME_DUPLICATE = new ErrorCode(1_{MODULE_CODE}_002, "{entity}名称已存在");
    ErrorCode {ENTITY}_HAS_CHILDREN   = new ErrorCode(1_{MODULE_CODE}_003, "存在关联数据，无法删除");
}
```

---

## Service 层

```java
package com.dainthub.{project}.module.{module}.service;

public interface {Entity}Service {

    /** 创建{entity}，返回新建主键 */
    Long create{Entity}({Entity}SaveReqVO createReqVO);

    void update{Entity}({Entity}SaveReqVO updateReqVO);

    void delete{Entity}(Long id);

    /**
     * 查询单条，返回 Optional。
     * - 查询单条用 Optional<DO>，调用方自行决定是否抛异常（C-ARCH-004）
     * - 查询列表/分页直接返回集合，不用 Optional 包装
     */
    Optional<{Entity}DO> get{Entity}OrElse(Long id);

    PageResult<{Entity}DO> get{Entity}Page({Entity}PageReqVO pageReqVO);
}

// -------- ServiceImpl --------
package com.dainthub.{project}.module.{module}.service.impl;

@Service
@Validated
@Slf4j
public class {Entity}ServiceImpl implements {Entity}Service {

    @Resource
    private {Entity}Mapper {entity}Mapper;

    // ==================== 静态 Comparator（跨多 DO 类型的排序，C-ARCH-006）====================
    // 若排序仅涉及当前 DO，优先用 {Entity}DO.BY_SORT_ASC
    // 此处示例：按 status 降序，再按 sortOrder 升序（跨字段复合排序定义在 ServiceImpl）
    private static final Comparator<{Entity}DO> BY_STATUS_DESC_THEN_SORT =
            Comparator.comparing({Entity}DO::getStatus, Comparator.reverseOrder())
                      .thenComparingInt({Entity}DO::getSortOrder);

    // ==================== 写操作 ====================

    @Override
    @Transactional(rollbackFor = Exception.class)
    public Long create{Entity}(@Valid {Entity}SaveReqVO reqVO) {
        log.info("[create{Entity}][开始创建，name={}]", reqVO.getName());
        // 1. 唯一性校验（id=null 表示新建场景，C-CODE-003：统一用 exception()）
        if (exist{Entity}Name(null, reqVO.getName())) {
            log.warn("[create{Entity}][名称已存在，name={}]", reqVO.getName());
            throw exception({ENTITY}_NAME_DUPLICATE);
        }
        // 2. 转换 & 持久化（toEntity 在 VO 中，C-ARCH-003）
        {Entity}DO entity = reqVO.toEntity();
        {entity}Mapper.insert(entity);
        log.info("[create{Entity}][创建成功，id={}]", entity.getId());
        return entity.getId();
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void update{Entity}(@Valid {Entity}SaveReqVO reqVO) {
        log.info("[update{Entity}][开始更新，id={}]", reqVO.getId());
        // 1. 校验存在（C-CODE-003）
        {Entity}DO entity = get{Entity}OrElse(reqVO.getId())
                .orElseThrow(() -> exception({ENTITY}_NOT_EXISTS));
        // 2. 唯一性校验（排除自身，id 非 null，C-CODE-003）
        if (exist{Entity}Name(reqVO.getId(), reqVO.getName())) {
            log.warn("[update{Entity}][名称已被占用，id={}, name={}]",
                    reqVO.getId(), reqVO.getName());
            throw exception({ENTITY}_NAME_DUPLICATE);
        }
        // 3. 应用变更（充血方法 applyUpdate，C-ARCH-005）
        entity.applyUpdate(reqVO);
        {entity}Mapper.updateById(entity);
        log.info("[update{Entity}][更新成功，id={}]", entity.getId());
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void delete{Entity}(Long id) {
        log.info("[delete{Entity}][开始删除，id={}]", id);
        get{Entity}OrElse(id).orElseThrow(() -> exception({ENTITY}_NOT_EXISTS));
        {entity}Mapper.deleteById(id);
        log.info("[delete{Entity}][删除成功，id={}]", id);
    }

    // ==================== 读操作 ====================

    @Override
    public Optional<{Entity}DO> get{Entity}OrElse(Long id) {
        return Optional.ofNullable({entity}Mapper.selectById(id));
    }

    @Override
    public PageResult<{Entity}DO> get{Entity}Page({Entity}PageReqVO pageReqVO) {
        return {entity}Mapper.selectPage(pageReqVO);
    }

    // ==================== 内部校验（private）====================

    /**
     * 校验名称是否已被占用。
     *
     * @param id   更新场景传当前记录 ID（排除自身）；新建场景传 {@code null}
     * @param name 待校验名称
     * @return {@code true} 表示名称已被其他记录占用
     */
    private boolean exist{Entity}Name(Long id, String name) {
        {Entity}DO existing = {entity}Mapper.selectByName(name);
        if (existing == null) {
            return false;
        }
        // 更新场景：与自身记录同名则不算重复
        return id == null || !existing.getId().equals(id);
    }
}
```

---

## Controller 层

```java
package com.dainthub.{project}.module.{module}.controller.admin;

@Tag(name = "管理后台 - {entity描述}")
@RestController
@RequestMapping("/admin-api/{module}/{entity-path}")
@Validated
public class {Entity}Controller {

    @Resource
    private {Entity}Service {entity}Service;

    @PostMapping("/create")
    @Operation(summary = "创建{entity描述}")
    @PreAuthorize("@ss.hasPermission('{module}:{entity}:create')")
    @OperateLog(type = CREATE)
    public CommonResult<Long> create{Entity}(@Valid @RequestBody {Entity}SaveReqVO reqVO) {
        return success({entity}Service.create{Entity}(reqVO));
    }

    @PutMapping("/update")
    @Operation(summary = "更新{entity描述}")
    @PreAuthorize("@ss.hasPermission('{module}:{entity}:update')")
    @OperateLog(type = UPDATE)
    public CommonResult<Boolean> update{Entity}(@Valid @RequestBody {Entity}SaveReqVO reqVO) {
        {entity}Service.update{Entity}(reqVO);
        return success(true);
    }

    @DeleteMapping("/delete")
    @Operation(summary = "删除{entity描述}")
    @Parameter(name = "id", description = "编号", required = true)
    @PreAuthorize("@ss.hasPermission('{module}:{entity}:delete')")
    @OperateLog(type = DELETE)
    public CommonResult<Boolean> delete{Entity}(@RequestParam("id") Long id) {
        {entity}Service.delete{Entity}(id);
        return success(true);
    }

    @GetMapping("/get")
    @Operation(summary = "获得{entity描述}详情")
    @Parameter(name = "id", description = "编号", required = true)
    @PreAuthorize("@ss.hasPermission('{module}:{entity}:query')")
    public CommonResult<{Entity}RespVO> get{Entity}(@RequestParam("id") Long id) {
        // 单条查询的"不存在"异常在 Controller 抛出：
        // 因为 Service 返回 Optional，由调用方决定如何处理（C-ARCH-004）
        return success(
            {entity}Service.get{Entity}OrElse(id)
                .map({Entity}RespVO::of)
                .orElseThrow(() -> exception({ENTITY}_NOT_EXISTS))
        );
    }

    @GetMapping("/page")
    @Operation(summary = "获得{entity描述}分页")
    @PreAuthorize("@ss.hasPermission('{module}:{entity}:query')")
    public CommonResult<PageResult<{Entity}RespVO>> get{Entity}Page(
            @Valid {Entity}PageReqVO pageReqVO) {
        return success({Entity}RespVO.ofPage(
                {entity}Service.get{Entity}Page(pageReqVO)));
    }

    @GetMapping("/export-excel")
    @Operation(summary = "导出{entity描述} Excel")
    @PreAuthorize("@ss.hasPermission('{module}:{entity}:export')")
    @OperateLog(type = EXPORT)
    public void export{Entity}Excel(@Valid {Entity}PageReqVO pageReqVO,
                                     HttpServletResponse response) throws IOException {
        pageReqVO.setPageSize(PAGE_SIZE_NONE);
        List<{Entity}DO> list = {entity}Service.get{Entity}Page(pageReqVO).getList();
        ExcelUtils.write(response, "{entity}.xls", "数据",
                {Entity}RespVO.class, {Entity}RespVO.ofList(list));
    }
}
```
