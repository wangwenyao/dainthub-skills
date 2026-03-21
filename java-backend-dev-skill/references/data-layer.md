# MySQL & MyBatis 最佳实践参考

> 按需加载。适用场景：Mapper 设计、SQL 编写、索引优化、批量操作、分页、原子操作。

---

## 一、MySQL 字段设计规范

### 字段类型选择

```sql
-- 主键
`id`          bigint        NOT NULL AUTO_INCREMENT

-- 字符串：明确上限用 varchar
`name`        varchar(64)   NOT NULL DEFAULT ''
`remark`      varchar(500)  NOT NULL DEFAULT ''
`content`     text                               -- 富文本/不定长大字段（无法建索引）

-- 金额：decimal(19,4)，禁止 float/double（C-DATA-003）
`amount`      decimal(19,4) NOT NULL DEFAULT '0.0000'

-- 时间：datetime（C-DATA-004：范围查询用 startTime/endTime 独立字段）
`create_time` datetime      NOT NULL DEFAULT CURRENT_TIMESTAMP
`begin_time`  datetime      DEFAULT NULL
`end_time`    datetime      DEFAULT NULL

-- 状态/类型：tinyint（对应 Java Integer，节省空间）
`status`      tinyint       NOT NULL DEFAULT 0

-- 布尔：bit(1)
`deleted`     bit(1)        NOT NULL DEFAULT b'0'

-- JSON 扩展字段（MySQL 5.7.8+，存动态属性）
`extra_info`  json          DEFAULT NULL
```

### 索引设计（C-DATA-001 / C-DATA-002）

```sql
-- ✅ 普通索引，不含 deleted 字段
KEY `idx_{entity}_user_id`    (`user_id`)
KEY `idx_{entity}_status`     (`status`)
KEY `idx_{entity}_create_time`(`create_time`)

-- ✅ 复合索引：高区分度字段靠左（最左前缀原则）
KEY `idx_{entity}_user_status`(`user_id`, `status`)

-- ❌ 禁止唯一索引（C-DATA-001）
UNIQUE KEY `uk_name` (`name`)       -- 禁止，唯一性在业务层 exist{Entity}Name 校验

-- ❌ 禁止索引包含 deleted（C-DATA-002）
KEY `idx_xxx` (`user_id`, `deleted`) -- 禁止
```

**索引选择原则**：
- WHERE 高频条件、ORDER BY 字段、JOIN ON 字段考虑建索引
- 区分度低的字段（如 `status` 仅 2-5 值）不单独建索引，可作复合索引后缀
- 长字符串用前缀索引 `KEY idx_name (name(32))`
- 单表索引数量不超过 5 个

---

## 二、Mapper.xml 规范（C-DATA-006）

### 列 SQL 片段（必须定义）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.dainthub.{project}.module.{module}.dal.mysql.{entity}.{Entity}Mapper">

    <!--
      ✅ C-DATA-006：必须定义列 SQL 片段，禁止 SELECT *
      修改字段时只需维护此一处，其他 SQL 自动生效
    -->
    <sql id="columns">
        id, name, status, sort_order,
        creator, create_time, updater, update_time, deleted
    </sql>

    <!--
      ✅ 通过 <include refid="columns"/> 引用列片段
      ✅ startTime/endTime 独立参数（C-DATA-004）
      ✅ <where> + <if> 替代手拼 WHERE 1=1
      ✅ #{} 防注入，禁止 ${}
    -->
    <select id="selectByCondition" resultType="{Entity}DO">
        SELECT <include refid="columns"/>
        FROM {module}_{entity}
        <where>
            deleted = 0
            <if test="name != null and name != ''">
                AND name LIKE CONCAT('%', #{name}, '%')
            </if>
            <if test="status != null">
                AND status = #{status}
            </if>
            <if test="startTime != null">
                AND create_time &gt;= #{startTime}
            </if>
            <if test="endTime != null">
                AND create_time &lt;= #{endTime}
            </if>
        </where>
        ORDER BY sort_order ASC, id DESC
    </select>

    <!-- ResultMap：仅当字段无法自动驼峰映射时定义 -->
    <resultMap id="StatResultMap" type="...{Entity}StatDO">
        <result column="category_id"  property="categoryId"/>
        <result column="total_count"  property="totalCount"/>
    </resultMap>

    <!--
      多表关联查询：使用表别名引用各自 columns 片段
      ✅ 参数超 3 个封装为 VO（C-CODE-007）
    -->
    <select id="selectStatByCondition" resultMap="StatResultMap">
        SELECT
            e.category_id,
            c.name AS category_name,
            COUNT(e.id) AS total_count
        FROM {module}_{entity} e
            LEFT JOIN {module}_category c ON c.id = e.category_id AND c.deleted = 0
        <where>
            e.deleted = 0
            <if test="reqVO.startTime != null">AND e.create_time &gt;= #{reqVO.startTime}</if>
            <if test="reqVO.endTime   != null">AND e.create_time &lt;= #{reqVO.endTime}</if>
            <if test="reqVO.status    != null">AND e.status = #{reqVO.status}</if>
        </where>
        GROUP BY e.category_id, c.name
        ORDER BY total_count DESC
    </select>

    <!-- 批量插入 -->
    <insert id="insertBatchCustom">
        INSERT INTO {module}_{entity} (name, status, sort_order, creator, updater)
        VALUES
        <foreach collection="list" item="item" separator=",">
            (#{item.name}, #{item.status}, #{item.sortOrder}, #{item.creator}, #{item.updater})
        </foreach>
    </insert>

    <!-- IN 查询：list 非空由调用方保证（Mapper 只做 SQL，业务校验在 Service） -->
    <select id="selectByIds" resultType="{Entity}DO">
        SELECT <include refid="columns"/>
        FROM {module}_{entity}
        WHERE deleted = 0
          AND id IN
        <foreach collection="ids" item="id" open="(" separator="," close=")">
            #{id}
        </foreach>
    </select>

    <!-- 动态更新（仅更新非空字段，存量改造常用） -->
    <update id="updateSelective">
        UPDATE {module}_{entity}
        <set>
            <if test="name      != null">name       = #{name},</if>
            <if test="status    != null">status     = #{status},</if>
            <if test="sortOrder != null">sort_order = #{sortOrder},</if>
            updater     = #{updater},
            update_time = NOW()
        </set>
        WHERE id = #{id} AND deleted = 0
    </update>

</mapper>
```

---

## 三、MyBatis Plus 使用规范

### LambdaQueryWrapperX（时间范围用独立字段）

```java
// ✅ startTime/endTime 独立字段（C-DATA-004，禁止数组/List）
default PageResult<{Entity}DO> selectPage({Entity}PageReqVO reqVO) {
    return selectPage(reqVO, new LambdaQueryWrapperX<{Entity}DO>()
            .likeIfPresent({Entity}DO::getName,       reqVO.getName())
            .eqIfPresent  ({Entity}DO::getStatus,     reqVO.getStatus())
            .geIfPresent  ({Entity}DO::getCreateTime, reqVO.getStartTime())  // >= startTime
            .leIfPresent  ({Entity}DO::getCreateTime, reqVO.getEndTime())    // <= endTime
            .orderByAsc   ({Entity}DO::getSortOrder)
            .orderByDesc  ({Entity}DO::getId));
}
```

### N+1 消除

```java
// ❌ N+1（100 条 = 101 次 DB 查询）
List<OrderDO> orders = orderMapper.selectList(null);
for (OrderDO order : orders) {
    UserDO user = userMapper.selectById(order.getUserId()); // 每次都查！
}

// ✅ 批量查询 + Map 检索（O(1)，C-DATA-005）
List<OrderDO> orders  = orderMapper.selectList(null);
Set<Long> userIds     = orders.stream().map(OrderDO::getUserId).collect(toSet());
Map<Long, UserDO> map = userMapper.selectMapByIds(userIds); // Mapper default 方法
orders.forEach(order -> {
    UserDO user = map.get(order.getUserId());
});
```

### 批量操作

```java
// ❌ 循环单条（性能极差）
for (ItemDO item : items) { itemMapper.insert(item); }

// ✅ 批量插入（BaseMapperX，内部已分批 500 条，C-DATA-005）
itemMapper.insertBatch(items);

// ✅ 批量更新
itemMapper.updateBatchById(items, 500);

// ✅ 按条件批量更新（比 updateBatchById 更高效，无需先查再改）
orderMapper.update(null,
    new LambdaUpdateWrapper<OrderDO>()
        .in(OrderDO::getId, orderIds)
        .set(OrderDO::getStatus, OrderStatusEnum.CANCELLED.getStatus()));
```

---

## 四、数据一致性

### 原子操作（库存/余额扣减）

```java
// ❌ 读-改-写：并发超卖
ProductDO p = productMapper.selectById(id);
p.setStock(p.getStock() - quantity);
productMapper.updateById(p);

// ✅ 数据库原子 UPDATE + 行数校验（C-CODE-003：用 exception()）
// Mapper XML:
// UPDATE product SET stock = stock - #{quantity}
// WHERE id = #{id} AND stock >= #{quantity} AND deleted = 0
int rows = productMapper.decreaseStock(id, quantity);
if (rows == 0) {
    log.warn("[deductStock][库存不足，productId={}, required={}]", id, quantity);
    throw exception(PRODUCT_STOCK_NOT_ENOUGH);
}
```

### 乐观锁（并发写冲突）

```java
@Version  // DO 中加 version 字段，MyBatis Plus 自动处理 CAS
private Integer version;

boolean updated = mapper.updateById(entity) > 0;
if (!updated) {
    log.warn("[update][版本冲突，id={}, version={}]", entity.getId(), entity.getVersion());
    throw exception(CONCURRENT_UPDATE_CONFLICT);
}
```

### 慢查询防范

```sql
-- ❌ 左模糊：索引失效，全表扫描
SELECT * FROM trade_order WHERE order_no LIKE '%20240101%';

-- ✅ 右模糊可用索引
SELECT id FROM trade_order WHERE order_no LIKE '2024%';

-- ❌ 函数导致索引失效
SELECT * FROM trade_order WHERE DATE(create_time) = '2024-01-01';

-- ✅ 范围代替函数
SELECT id FROM trade_order
WHERE create_time >= '2024-01-01 00:00:00'
  AND create_time <  '2024-01-02 00:00:00';

-- ❌ 隐式类型转换（字符串字段传数字，全表扫描）
WHERE mobile = 13800138000
-- ✅
WHERE mobile = '13800138000'
```
