# 技术栈图标库（SimpleIcons）

> 基于 [SimpleIcons](https://simpleicons.org/) CDN 的技术栈图标，适用于功能架构图、技术栈展示图。

---

## 一、使用方式

通过 `image` 属性引用 SimpleIcons CDN：

```xml
<mxCell style="image;html=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;
        strokeColor=none;fillColor=none;labelBackgroundColor=none;
        image=https://cdn.simpleicons.org/{icon-name}/{hex-color};"
        value="React" vertex="1" parent="1">
  <mxGeometry width="60" height="60" x="100" y="100" as="geometry"/>
</mxCell>
```

### URL 格式

```
https://cdn.simpleicons.org/{icon-name}/{hex-color}
```

| 参数 | 说明 | 示例 |
|------|------|------|
| `{icon-name}` | 图标名称（小写，空格用点代替） | `react`、`vuedotjs`、`nextdotjs` |
| `{hex-color}` | 图标颜色（可选，6位十六进制） | `61DAFB`（React 蓝）、`4FC08D`（Vue 绿） |

### 必要属性

| 属性 | 值 | 说明 |
|------|-----|------|
| `strokeColor` | `none` | 无描边 |
| `fillColor` | `none` | 无填充（颜色由 image URL 控制） |
| `verticalLabelPosition` | `bottom` | 标签在图标下方 |
| `verticalAlign` | `top` | 标签顶部对齐 |
| `width` / `height` | 通常 `60` | 图标尺寸 |

---

## 二、前端技术栈

### 基础技术

| 技术 | icon-name | 颜色 | 完整 URL |
|------|-----------|------|----------|
| HTML5 | `html5` | `E34F26` | `https://cdn.simpleicons.org/html5/E34F26` |
| CSS3 | `css` | `1572B6` | `https://cdn.simpleicons.org/css/1572B6` |
| JavaScript | `javascript` | `F7DF1E` | `https://cdn.simpleicons.org/javascript/F7DF1E` |
| TypeScript | `typescript` | `3178C6` | `https://cdn.simpleicons.org/typescript/3178C6` |

### 框架

| 技术 | icon-name | 颜色 | 完整 URL |
|------|-----------|------|----------|
| React | `react` | `61DAFB` | `https://cdn.simpleicons.org/react/61DAFB` |
| Vue.js | `vuedotjs` | `4FC08D` | `https://cdn.simpleicons.org/vuedotjs/4FC08D` |
| Next.js | `nextdotjs` | `000000` | `https://cdn.simpleicons.org/nextdotjs/000000` |
| Svelte | `svelte` | `FF3E00` | `https://cdn.simpleicons.org/svelte/FF3E00` |
| Angular | `angular` | `DD0031` | `https://cdn.simpleicons.org/angular/DD0031` |

### 样式/构建

| 技术 | icon-name | 颜色 | 完整 URL |
|------|-----------|------|----------|
| Sass | `sass` | `CC6699` | `https://cdn.simpleicons.org/sass/CC6699` |
| Tailwind CSS | `tailwindcss` | `06B6D4` | `https://cdn.simpleicons.org/tailwindcss/06B6D4` |
| Webpack | `webpack` | `8DD6F9` | `https://cdn.simpleicons.org/webpack/8DD6F9` |
| Vite | `vite` | `646CFF` | `https://cdn.simpleicons.org/vite/646CFF` |

### 工具库

| 技术 | icon-name | 颜色 | 完整 URL |
|------|-----------|------|----------|
| Axios | `axios` | `5A29E4` | `https://cdn.simpleicons.org/axios/5A29E4` |

---

## 三、后端技术栈

### Java 生态

| 技术 | icon-name | 颜色 | 完整 URL |
|------|-----------|------|----------|
| Spring Boot | `springboot` | `6DB33F` | `https://cdn.simpleicons.org/springboot/6DB33F` |
| Spring | `spring` | `6DB33F` | `https://cdn.simpleicons.org/spring/6DB33F` |
| Spring Security | `springsecurity` | `6DB33F` | `https://cdn.simpleicons.org/springsecurity/6DB33F` |
| Maven | `apachemaven` | `C71A36` | `https://cdn.simpleicons.org/apachemaven/C71A36` |
| Gradle | `gradle` | `02303A` | `https://cdn.simpleicons.org/gradle/02303A` |

### 运行时/语言

| 技术 | icon-name | 颜色 | 完整 URL |
|------|-----------|------|----------|
| Node.js | `nodedotjs` | `339933` | `https://cdn.simpleicons.org/nodedotjs/339933` |
| Python | `python` | `3776AB` | `https://cdn.simpleicons.org/python/3776AB` |
| Go | `go` | `00ADD8` | `https://cdn.simpleicons.org/go/00ADD8` |
| Rust | `rust` | `000000` | `https://cdn.simpleicons.org/rust/000000` |
| Java | `openjdk` | `437291` | `https://cdn.simpleicons.org/openjdk/437291` |

### Web 框架

| 技术 | icon-name | 颜色 | 完整 URL |
|------|-----------|------|----------|
| Django | `django` | `092E20` | `https://cdn.simpleicons.org/django/092E20` |
| FastAPI | `fastapi` | `009688` | `https://cdn.simpleicons.org/fastapi/009688` |
| Flask | `flask` | `000000` | `https://cdn.simpleicons.org/flask/000000` |
| Express | `express` | `000000` | `https://cdn.simpleicons.org/express/000000` |
| NestJS | `nestjs` | `E0234E` | `https://cdn.simpleicons.org/nestjs/E0234E` |

### API

| 技术 | icon-name | 颜色 | 完整 URL |
|------|-----------|------|----------|
| GraphQL | `graphql` | `E10098` | `https://cdn.simpleicons.org/graphql/E10098` |
| OpenAPI | `openapiinitiative` | `6BA539` | `https://cdn.simpleicons.org/openapiinitiative/6BA539` |
| Nginx | `nginx` | `009639` | `https://cdn.simpleicons.org/nginx/009639` |

---

## 四、数据库

### 关系型

| 技术 | icon-name | 颜色 | 完整 URL |
|------|-----------|------|----------|
| MySQL | `mysql` | `4479A1` | `https://cdn.simpleicons.org/mysql/4479A1` |
| PostgreSQL | `postgresql` | `4169E1` | `https://cdn.simpleicons.org/postgresql/4169E1` |
| MariaDB | `mariadb` | `003545` | `https://cdn.simpleicons.org/mariadb/003545` |
| SQLite | `sqlite` | `003B57` | `https://cdn.simpleicons.org/sqlite/003B57` |

### NoSQL

| 技术 | icon-name | 颜色 | 完整 URL |
|------|-----------|------|----------|
| MongoDB | `mongodb` | `47A248` | `https://cdn.simpleicons.org/mongodb/47A248` |
| Redis | `redis` | `FF4438` | `https://cdn.simpleicons.org/redis/FF4438` |
| Elasticsearch | `elasticsearch` | `005571` | `https://cdn.simpleicons.org/elasticsearch/005571` |
| Cassandra | `apachecassandra` | `1287B1` | `https://cdn.simpleicons.org/apachecassandra/1287B1` |
| Neo4j | `neo4j` | `4581C3` | `https://cdn.simpleicons.org/neo4j/4581C3` |

### 数据仓库/分析

| 技术 | icon-name | 颜色 | 完整 URL |
|------|-----------|------|----------|
| ClickHouse | `clickhouse` | `FFCC01` | `https://cdn.simpleicons.org/clickhouse/FFCC01` |
| InfluxDB | `influxdb` | `22ADF6` | `https://cdn.simpleicons.org/influxdb/22ADF6` |

---

## 五、消息队列

| 技术 | icon-name | 颜色 | 完整 URL |
|------|-----------|------|----------|
| Kafka | `apachekafka` | `231F20` | `https://cdn.simpleicons.org/apachekafka/231F20` |
| RocketMQ | `apacherocketmq` | `D77310` | `https://cdn.simpleicons.org/apacherocketmq/D77310` |
| RabbitMQ | `rabbitmq` | `FF6600` | `https://cdn.simpleicons.org/rabbitmq/FF6600` |
| Pulsar | `apachepulsar` | `188FFF` | `https://cdn.simpleicons.org/apachepulsar/188FFF` |

---

## 六、监控与可观测

| 技术 | icon-name | 颜色 | 完整 URL |
|------|-----------|------|----------|
| Prometheus | `prometheus` | `E6522C` | `https://cdn.simpleicons.org/prometheus/E6522C` |
| Grafana | `grafana` | `F46800` | `https://cdn.simpleicons.org/grafana/F46800` |
| Kibana | `kibana` | `005571` | `https://cdn.simpleicons.org/kibana/005571` |
| Logstash | `logstash` | `005571` | `https://cdn.simpleicons.org/logstash/005571` |
| Consul | `consul` | `F24C53` | `https://cdn.simpleicons.org/consul/F24C53` |

---

## 七、大数据

| 技术 | icon-name | 颜色 | 完整 URL |
|------|-----------|------|----------|
| Flink | `apacheflink` | `E6526A` | `https://cdn.simpleicons.org/apacheflink/E6526A` |
| Spark | `apachespark` | `E25A1C` | `https://cdn.simpleicons.org/apachespark/E25A1C` |
| Hadoop | `apachehadoop` | `66CCFF` | `https://cdn.simpleicons.org/apachehadoop/66CCFF` |
| Doris | `apachedoris` | `1660E8` | `https://cdn.simpleicons.org/apachedoris/1660E8` |
| HBase | `apachehbase` | `AE1B1E` | `https://cdn.simpleicons.org/apachehbase/AE1B1E` |
| Airflow | `apacheairflow` | `017CEE` | `https://cdn.simpleicons.org/apacheairflow/017CEE` |
| Superset | `apachesuperset` | `F24C53` | `https://cdn.simpleicons.org/apachesuperset/F24C53` |

---

## 八、DevOps 与云原生

| 技术 | icon-name | 颜色 | 完整 URL |
|------|-----------|------|----------|
| Docker | `docker` | `2496ED` | `https://cdn.simpleicons.org/docker/2496ED` |
| Kubernetes | `kubernetes` | `326CE5` | `https://cdn.simpleicons.org/kubernetes/326CE5` |
| Jenkins | `jenkins` | `D24939` | `https://cdn.simpleicons.org/jenkins/D24939` |
| Ansible | `ansible` | `EE0000` | `https://cdn.simpleicons.org/ansible/EE0000` |
| Helm | `helm` | `0F1689` | `https://cdn.simpleicons.org/helm/0F1689` |
| Harbor | `harbor` | `60B932` | `https://cdn.simpleicons.org/harbor/60B932` |
| Terraform | `terraform` | `7B42BC` | `https://cdn.simpleicons.org/terraform/7B42BC` |

---

## 九、开发工具

| 技术 | icon-name | 颜色 | 完整 URL |
|------|-----------|------|----------|
| Git | `git` | `F05032` | `https://cdn.simpleicons.org/git/F05032` |
| GitHub | `github` | `181717` | `https://cdn.simpleicons.org/github/181717` |
| GitLab | `gitlab` | `FC6D26` | `https://cdn.simpleicons.org/gitlab/FC6D26` |
| Postman | `postman` | `FF6C37` | `https://cdn.simpleicons.org/postman/FF6C37` |
| VS Code | `visualstudiocode` | `007ACC` | `https://cdn.simpleicons.org/visualstudiocode/007ACC` |

---

## 十、移动端

| 技术 | icon-name | 颜色 | 完整 URL |
|------|-----------|------|----------|
| Android | `android` | `34A853` | `https://cdn.simpleicons.org/android/34A853` |
| iOS / Swift | `swift` | `F05138` | `https://cdn.simpleicons.org/swift/F05138` |
| Flutter | `flutter` | `02569B` | `https://cdn.simpleicons.org/flutter/02569B` |
| Kotlin | `kotlin` | `7F52FF` | `https://cdn.simpleicons.org/kotlin/7F52FF` |
| React Native | `react` | `61DAFB` | `https://cdn.simpleicons.org/react/61DAFB` |
| Ionic | `ionic` | `3880FF` | `https://cdn.simpleicons.org/ionic/3880FF` |

---

## 十一、操作系统与工具

| 技术 | icon-name | 颜色 | 完整 URL |
|------|-----------|------|----------|
| Linux | `linux` | `FCC624` | `https://cdn.simpleicons.org/linux/FCC624` |
| Ubuntu | `ubuntu` | `E95420` | `https://cdn.simpleicons.org/ubuntu/E95420` |
| Bash | `gnubash` | `4EAA25` | `https://cdn.simpleicons.org/gnubash/4EAA25` |
| Vim | `vim` | `019733` | `https://cdn.simpleicons.org/vim/019733` |
| Figma | `figma` | `F24E1E` | `https://cdn.simpleicons.org/figma/F24E1E` |
| Markdown | `markdown` | `000000` | `https://cdn.simpleicons.org/markdown/000000` |

---

## 十二、完整图标示例

```xml
<!-- React 图标 -->
<mxCell id="react-icon" style="image;html=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;strokeColor=none;fillColor=none;labelBackgroundColor=none;image=https://cdn.simpleicons.org/react/61DAFB;" value="React" vertex="1" parent="1">
  <mxGeometry width="60" height="60" x="100" y="100" as="geometry"/>
</mxCell>

<!-- Spring Boot 图标 -->
<mxCell id="springboot-icon" style="image;html=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;strokeColor=none;fillColor=none;labelBackgroundColor=none;image=https://cdn.simpleicons.org/springboot/6DB33F;" value="Spring Boot" vertex="1" parent="1">
  <mxGeometry width="60" height="60" x="200" y="100" as="geometry"/>
</mxCell>

<!-- MySQL 图标 -->
<mxCell id="mysql-icon" style="image;html=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;strokeColor=none;fillColor=none;labelBackgroundColor=none;image=https://cdn.simpleicons.org/mysql/4479A1;" value="MySQL" vertex="1" parent="1">
  <mxGeometry width="60" height="60" x="300" y="100" as="geometry"/>
</mxCell>

<!-- Kubernetes 图标 -->
<mxCell id="k8s-icon" style="image;html=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;strokeColor=none;fillColor=none;labelBackgroundColor=none;image=https://cdn.simpleicons.org/kubernetes/326CE5;" value="Kubernetes" vertex="1" parent="1">
  <mxGeometry width="60" height="60" x="400" y="100" as="geometry"/>
</mxCell>
```

---

## 十三、查找更多图标

1. 访问 [SimpleIcons 官网](https://simpleicons.org/)
2. 搜索技术名称
3. 复制图标名称和颜色值
4. 拼接 URL：`https://cdn.simpleicons.org/{name}/{color}`

---

## 十四、与云厂商图标配合使用

SimpleIcons 技术栈图标与云厂商图标（阿里云/AWS/GCP/Azure）配合使用时：

| 场景 | 推荐图标来源 |
|------|-------------|
| 云资源（ECS、RDS、OSS 等） | 云厂商内置图标 |
| 技术栈（Spring、React、MySQL 等） | SimpleIcons |
| 中间件（Kafka、Redis 等） | SimpleIcons 或云厂商图标 |
| 容器/编排（Docker、K8s） | SimpleIcons 或 mxgraph.kubernetes |