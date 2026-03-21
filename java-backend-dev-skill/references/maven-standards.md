# Maven 模块与依赖规范参考

> 按需加载。适用场景：新建模块、添加依赖、pom.xml 结构设计。

---

## 一、项目模块结构

```
{project}-parent/                              # 顶层 BOM，管理所有版本
├── pom.xml                                    # packaging=pom，dependencyManagement
│
├── {project}-dependencies/                    # 第三方依赖版本锁定（BOM）
│   └── pom.xml
│
├── {project}-framework/                       # 框架通用能力
│   ├── {project}-common/                      # 公共实体、工具（无 Spring 依赖）
│   ├── {project}-spring-boot-starter-mybatis/
│   ├── {project}-spring-boot-starter-redis/
│   ├── {project}-spring-boot-starter-web/
│   └── {project}-spring-boot-starter-security/
│
├── {project}-module-system/                   # 系统管理模块（聚合）
│   ├── pom.xml                                # packaging=pom
│   └── {project}-module-system-biz/           # ✅ 业务实现（前缀为 {project}，非 dainthub）
│       └── pom.xml
│
├── {project}-module-{module}/                 # 业务模块（命名规范同上）
│   ├── pom.xml
│   └── {project}-module-{module}-biz/         # ✅ artifactId 规则：{project}-module-{module}-biz
│       └── pom.xml
│
└── {project}-server/                          # 启动模块（汇聚所有 biz 模块）
    └── pom.xml
```

> **命名规则**：业务实现子模块 artifactId = `{project}-module-{module}-biz`，`{project}` 为实际项目名（如 mall、oms），不固定为 dainthub。

---

## 二、顶层 Parent POM

```xml
<!-- {project}-parent/pom.xml -->
<project>
    <groupId>com.dainthub.{project}</groupId>
    <artifactId>{project}-parent</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <packaging>pom</packaging>

    <properties>
        <!-- ✅ Java 21（LTS，req 2）-->
        <java.version>21</java.version>
        <maven.compiler.source>${java.version}</maven.compiler.source>
        <maven.compiler.target>${java.version}</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>

        <!-- 核心框架版本（集中管理，禁止在子模块覆盖）-->
        <spring-boot.version>3.3.11</spring-boot.version>
        <mybatis-plus.version>3.5.7</mybatis-plus.version>
        <hutool.version>5.8.29</hutool.version>
        <redisson.version>3.32.0</redisson.version>
        <quartz.version>2.3.2</quartz.version>
        <knife4j.version>4.5.0</knife4j.version>
    </properties>

    <modules>
        <module>{project}-dependencies</module>
        <module>{project}-framework</module>
        <module>{project}-module-system</module>
        <module>{project}-module-{module}</module>
        <module>{project}-server</module>
    </modules>

    <dependencyManagement>
        <dependencies>
            <!-- Spring Boot BOM -->
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-dependencies</artifactId>
                <version>${spring-boot.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
            <!-- 项目内部 BOM -->
            <dependency>
                <groupId>com.dainthub.{project}</groupId>
                <artifactId>{project}-dependencies</artifactId>
                <version>${project.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>
</project>
```

---

## 三、业务模块 POM

```xml
<!-- {project}-module-{module}/pom.xml（聚合）-->
<project>
    <parent>
        <groupId>com.dainthub.{project}</groupId>
        <artifactId>{project}-parent</artifactId>
        <version>1.0.0-SNAPSHOT</version>
    </parent>

    <artifactId>{project}-module-{module}</artifactId>
    <packaging>pom</packaging>

    <modules>
        <!-- ✅ 业务实现子模块命名：{project}-module-{module}-biz -->
        <module>{project}-module-{module}-biz</module>
    </modules>
</project>

<!-- {project}-module-{module}-biz/pom.xml（业务实现）-->
<project>
    <parent>
        <groupId>com.dainthub.{project}</groupId>
        <artifactId>{project}-module-{module}</artifactId>
        <version>1.0.0-SNAPSHOT</version>
    </parent>

    <!-- ✅ artifactId 规则：{project}-module-{module}-biz -->
    <artifactId>{project}-module-{module}-biz</artifactId>
    <packaging>jar</packaging>

    <dependencies>
        <!-- 框架 starter（按需引入）-->
        <dependency>
            <groupId>com.dainthub.{project}</groupId>
            <artifactId>{project}-spring-boot-starter-mybatis</artifactId>
        </dependency>
        <dependency>
            <groupId>com.dainthub.{project}</groupId>
            <artifactId>{project}-spring-boot-starter-redis</artifactId>
        </dependency>
        <dependency>
            <groupId>com.dainthub.{project}</groupId>
            <artifactId>{project}-spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>com.dainthub.{project}</groupId>
            <artifactId>{project}-spring-boot-starter-security</artifactId>
        </dependency>

        <!-- 定时任务（需要时引入）-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-quartz</artifactId>
        </dependency>

        <!-- 跨模块依赖（禁止循环依赖）-->
        <dependency>
            <groupId>com.dainthub.{project}</groupId>
            <!-- ✅ 依赖其他模块时，artifactId 遵循 {project}-module-{module}-biz 规则 -->
            <artifactId>{project}-module-system-biz</artifactId>
        </dependency>
    </dependencies>
</project>
```

---

## 四、依赖版本锁定（BOM）

```xml
<!-- {project}-dependencies/pom.xml -->
<dependencyManagement>
    <dependencies>
        <!-- MyBatis Plus（Spring Boot 3 用 spring-boot3 包）-->
        <dependency>
            <groupId>com.baomidou</groupId>
            <artifactId>mybatis-plus-spring-boot3-starter</artifactId>
            <version>${mybatis-plus.version}</version>
        </dependency>

        <!-- Hutool（按需引入子模块，或全量引入 hutool-all）-->
        <dependency>
            <groupId>cn.hutool</groupId>
            <artifactId>hutool-all</artifactId>
            <version>${hutool.version}</version>
        </dependency>

        <!-- Redisson -->
        <dependency>
            <groupId>org.redisson</groupId>
            <artifactId>redisson-spring-boot-starter</artifactId>
            <version>${redisson.version}</version>
        </dependency>

        <!-- Quartz（Spring Boot starter 已包含版本管理，此处仅示意）-->
        <dependency>
            <groupId>org.quartz-scheduler</groupId>
            <artifactId>quartz</artifactId>
            <version>${quartz.version}</version>
        </dependency>

        <!-- API 文档 -->
        <dependency>
            <groupId>com.github.xiaoymin</groupId>
            <artifactId>knife4j-openapi3-jakarta-spring-boot-starter</artifactId>
            <version>${knife4j.version}</version>
        </dependency>
    </dependencies>
</dependencyManagement>
```

---

## 五、依赖引入原则

```
✅ 版本必须在 dependencyManagement（parent 或 BOM 模块）中锁定
✅ 子模块引入依赖不写 <version>（由 BOM 统一管理）
✅ 仅引入当前模块实际需要的依赖
✅ 测试依赖加 <scope>test</scope>
✅ 仅编译期需要的依赖加 <scope>provided</scope>
✅ Lombok 加 <optional>true</optional>（不传递给下游）

❌ 禁止子模块覆盖 parent 已定义的版本号
❌ 禁止重复引入功能相同的库（如同时引 Fastjson 和 Jackson）
❌ 禁止业务模块直接继承 spring-boot-starter-parent（只有顶层 parent 继承）
❌ 禁止循环模块依赖
```

---

## 六、常用依赖速查

```xml
<!-- 参数校验 -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>

<!-- Lombok（编译期，optional）-->
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <optional>true</optional>
</dependency>

<!-- OpenAPI 3 注解 -->
<dependency>
    <groupId>io.swagger.core.v3</groupId>
    <artifactId>swagger-annotations-jakarta</artifactId>
</dependency>

<!-- 单元测试 -->
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
```

---

## 七、构建插件规范

```xml
<build>
    <plugins>
        <!-- 编译插件：Java 21 + Lombok 注解处理器 -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <configuration>
                <source>${java.version}</source>
                <target>${java.version}</target>
                <annotationProcessorPaths>
                    <path>
                        <groupId>org.projectlombok</groupId>
                        <artifactId>lombok</artifactId>
                    </path>
                </annotationProcessorPaths>
            </configuration>
        </plugin>

        <!--
          spring-boot-maven-plugin：只在 {project}-server 启动模块配置
          业务 biz 模块不配置此插件，否则会打出不可被其他模块引用的 fat jar
        -->
    </plugins>
</build>
```

---

## 八、模块 artifactId 命名规范速查

| 模块类型 | artifactId 规则 | 示例（project=mall）|
|---------|----------------|-------------------|
| 顶层 parent | `{project}-parent` | `mall-parent` |
| 依赖 BOM | `{project}-dependencies` | `mall-dependencies` |
| 公共模块 | `{project}-common` | `mall-common` |
| 框架 starter | `{project}-spring-boot-starter-{cap}` | `mall-spring-boot-starter-redis` |
| 业务模块聚合 | `{project}-module-{module}` | `mall-module-trade` |
| **业务模块实现** | **`{project}-module-{module}-biz`** | **`mall-module-trade-biz`** |
| 启动模块 | `{project}-server` | `mall-server` |
