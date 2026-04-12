# 项目整体目录结构

---

## 目录结构

```
project/
├── docs/                              # 协同开发文档目录
│   ├── prd/                           # PRD 文档
│   │   ├── index.md                   # PRD 索引文件
│   │   ├── prd-{模块}-v{版本}.md       # 各模块 PRD
│   │   └── prd-{模块}-v{版本}-er.md    # ER 图文档
│   ├── api/                           # OpenAPI 接口规格
│   │   ├── index.md                   # API 索引文件
│   │   └── openapi-{模块}-v{版本}.yaml # OpenAPI 3.0 文档
│   ├── db/                            # 数据库脚本
│   │   ├── index.md                   # DB 索引文件
│   │   ├── dml-{模块}-v{版本}.sql      # DML 执行脚本
│   │   ├── dml-{模块}-v{版本}-rollback.sql # 回滚脚本
│   │   └── dml-{模块}-checklist-v{版本}.md # 执行清单
│   ├── wireframes/                    # 线框图 + YAML 页面规格
│   │   ├── index.md                   # 线框图索引文件
│   │   ├── wireframes-{模块}-v{版本}.html # HTML 线框图
│   │   └── wireframes-{模块}-v{版本}.yaml # YAML 页面规格
│   ├── reports/                       # 分析报告 + 验证报告 + 偏差报告
│   │   ├── index.md                   # 报告索引文件
│   │   ├── impact-{模块}-v{版本}.md    # 变更影响分析报告
│   │   ├── verify-{模块}-v{版本}.md    # 实现验证报告
│   │   └── deviation-{模块}-v{版本}.md # 偏差反馈报告
│   ├── decisions/                     # 决策记录
│   │   ├── index.md                   # 决策索引文件
│   │   └── decision-{议题}-v{版本}.md  # 产品决策记录
│   ├── archive/                       # 版本归档
│   │   └── v{版本}/                   # 归档版本目录
│   ├── status.md                      # 当前状态快照（AI 只读此文件）
│   └── index.md                       # docs 总索引
│
├── backend/                           # 后端工程（Spring Boot）
│   └── （见 03-frontend-backend.md）
│
├── frontend/                          # 前端工程（Vben Admin）
│   └── （见 03-frontend-backend.md）
│
├── .agents/                           # AI 配置目录
│   ├── skills.json                    # 技能版本锁定（可选）
│   └── AGENTS.md                      # 项目级 AI 配置
│
├── AGENTS.md                          # 项目根目录 AI 配置
├── README.md                          # 项目说明
└── .gitignore
```

---

## 文件命名规范

| 文件类型 | 命名格式 |
|---------|---------|
| PRD | `prd-{模块}-v{版本}.md` |
| ER图 | `prd-{模块}-v{版本}-er.md` |
| OpenAPI | `openapi-{模块}-v{版本}.yaml` |
| DML执行脚本 | `dml-{模块}-v{版本}.sql` |
| DML回滚脚本 | `dml-{模块}-v{版本}-rollback.sql` |
| 执行清单 | `dml-{模块}-checklist-v{版本}.md` |
| HTML线框图 | `wireframes-{模块}-v{版本}.html` |
| YAML页面规格 | `wireframes-{模块}-v{版本}.yaml` |
| 影响分析报告 | `impact-{模块}-v{版本}.md` |
| 验证报告 | `verify-{模块}-v{版本}.md` |
| 偏差报告 | `deviation-{模块}-v{版本}.md` |
| 决策记录 | `decision-{议题}-v{版本}.md` |

