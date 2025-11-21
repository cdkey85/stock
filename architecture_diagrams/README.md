# InStock量化投资系统架构文档

本目录包含InStock项目的完整架构分析和可视化图表。

## 📊 架构图列表

### 1. 系统架构图 (system_architecture)
**文件**: `system_architecture.puml` / `system_architecture.png`

**描述**: 完整的系统架构分层视图，展示了InStock系统的六大层次：
- 外部服务层：东方财富网API、MySQL数据库、券商客户端、HTTP代理
- Web服务层：Tornado Web框架、前端界面
- 任务调度层：7大定时任务模块
- 核心业务层：数据爬虫、技术指标、K线形态、选股策略、回测分析
- 交易引擎层：MainEngine、EventEngine、ClockEngine、策略加载器
- 基础设施层：数据访问层、单例管理器、公共库

**适用场景**: 项目整体架构理解、技术选型参考、系统设计文档


### 2. 核心业务调用逻辑 (core_logic_flow)
**文件**: `core_logic_flow.puml` / `core_logic_flow.png`

**描述**: 展示每日任务执行的完整流程，包括：
- 初始化阶段：数据库表结构创建
- 基础数据抓取：A股实时行情获取
- 历史数据加载：16线程并行加载历史K线
- 技术指标计算：32种指标并行计算（MACD、KDJ、BOLL、RSI等）
- K线形态识别：61种经典形态识别、CYQ筹码分布计算
- 选股策略执行：放量上涨、突破平台、回踩年线、海龟交易等11种策略
- 回测验证：计算策略成功率统计

**适用场景**: 业务流程理解、性能优化分析、任务调度设计


### 3. Web服务交互流程 (web_interaction_flow)
**文件**: `web_interaction_flow.puml` / `web_interaction_flow.png`

**描述**: Tornado Web服务的完整交互流程：
- Web服务启动：路由注册、数据库连接池创建
- 用户访问首页：HomeHandler处理
- 查看股票列表：数据表格展示、SQL查询构建
- 加载表格数据：Ajax异步加载、JSON序列化
- 查看技术指标图表：Bokeh可视化、K线图绘制
- 添加关注：数据库更新操作

**适用场景**: Web开发理解、前后端交互、API设计


### 4. 自动交易引擎架构 (trade_engine_flow)
**文件**: `trade_engine_flow.puml` / `trade_engine_flow.png`

**描述**: 完整的自动交易引擎工作流程：
- 交易服务启动：MainEngine初始化、券商客户端连接
- 策略动态加载：扫描strategies目录、实例化策略类
- 引擎启动：EventEngine事件循环、ClockEngine定时触发
- 交易时段事件循环：策略逻辑执行、买卖指令发送、持仓查询
- 策略热重载：文件变化检测、模块重新加载
- 服务关闭：策略平仓、事件引擎停止

**适用场景**: 量化交易开发、策略框架设计、自动化交易


### 5. 数据流转示意图 (data_flow)
**文件**: `data_flow.puml` / `data_flow.png`

**描述**: 系统内数据流转的完整路径：
- 数据获取：东方财富网API → HTTP代理池 → 数据爬虫
- 数据存储：原始数据存储 → MySQL基础数据表
- 数据加载：数据库 → 单例缓存池（提高查询效率）
- 数据计算：缓存池 → 计算分析层（TA-Lib、形态识别、筹码分布）
- 数据应用：分析结果 → Web服务/交易引擎 → 用户终端

**数据量级**:
- 5000+股票
- 210日历史数据
- 32种技术指标
- 61种K线形态
- 11种选股策略

**适用场景**: 数据架构设计、性能优化、缓存策略


### 6. 模块依赖关系图 (module_dependency)
**文件**: `module_dependency.puml` / `module_dependency.png`

**描述**: 详细的模块依赖关系，分为五层：
- **应用层**: web_service、trade_service、execute_daily_job
- **处理层**: dataTableHandler、dataIndicatorsHandler、HomeHandler
- **业务层**: 数据爬虫、指标计算、形态识别、选股策略、回测分析、交易引擎
- **核心层**: 单例管理、数据持久化、工具库
- **基础设施**: MySQL、东方财富网API、券商客户端

**依赖关系**:
- 实线箭头：直接依赖
- 虚线箭头：外部HTTP调用

**适用场景**: 代码重构、模块解耦、依赖分析


### 7. 技术栈总览 (tech_stack)
**文件**: `tech_stack.puml` / `tech_stack.png`

**描述**: 完整的技术栈和工具链展示：
- **Python核心生态**: pandas、numpy、TA-Lib、bokeh
- **Web服务技术栈**: Tornado、Bootstrap、jQuery、DataTables
- **数据持久化技术栈**: PyMySQL、SQLAlchemy、torndb、MySQL
- **数据采集技术栈**: requests、beautifulsoup4、py_mini_racer、代理池
- **自动交易技术栈**: easytrader、Tesseract OCR
- **辅助工具**: pycryptodome、Supervisor、Docker
- **开发工具链**: Git、requirements.txt、运行脚本

**性能指标**:
- 单次任务耗时: 约4分钟
- 并发线程数: 16
- 股票数量: 5000+
- 历史数据: 210日

**适用场景**: 技术选型、环境搭建、依赖管理


## 🛠️ 如何使用

### 在线渲染PlantUML
```bash
cd architecture_diagrams
python render_multi_servers.py <puml文件> <输出png文件>
```

**示例**:
```bash
python render_multi_servers.py system_architecture.puml system_architecture.png
```

### 查看PNG图片
直接打开对应的`.png`文件即可查看高清架构图。

### 编辑PUML文件
使用任何文本编辑器打开`.puml`文件进行编辑，然后重新渲染即可。


## 📋 技术要点总结

### 核心技术栈
- **Web框架**: Tornado 6.5.1
- **数据处理**: pandas 2.3.1, numpy 2.3.1
- **技术指标**: TA-Lib 0.6.4
- **数据库**: MySQL + SQLAlchemy 2.0.41 + PyMySQL 1.1.1
- **自动交易**: easytrader 0.23.7
- **可视化**: bokeh 3.6.2

### 设计模式
- **单例模式**: singleton_type元类实现，确保全局唯一实例
- **观察者模式**: EventEngine事件驱动架构
- **模板方法模式**: run_template统一任务执行框架
- **策略模式**: 11种选股策略动态加载

### 性能优化
- **并发处理**: ThreadPoolExecutor(16 workers)
- **数据缓存**: 单例缓存池减少数据库查询
- **批量操作**: pandas批量数据处理
- **连接池**: 数据库连接池复用

### 关键流程时序
1. **数据库初始化** (init_job)
2. **基础数据抓取** (basic_data_daily_job) - 约1分钟
3. **并行计算阶段** - 约2分钟
   - 指标计算 (indicators_data_daily_job)
   - 形态识别 (klinepattern_data_daily_job)
   - 策略选股 (strategy_data_daily_job)
4. **回测分析** (backtest_data_daily_job) - 约30秒
5. **收盘后数据** (basic_data_after_close_daily_job) - 约30秒

**总耗时**: 约4分钟（全量5000+股票）


## 📝 架构特点

### 1. 分层架构
清晰的六层架构设计，职责分明，易于维护和扩展。

### 2. 事件驱动
交易引擎采用事件驱动架构，支持策略热重载，无需重启服务。

### 3. 并行计算
充分利用多线程并行处理，提高数据处理效率。

### 4. 单例缓存
核心数据使用单例模式缓存，减少数据库压力，提升查询速度。

### 5. 模块化设计
功能模块高度解耦，每个模块可独立运行和测试。

### 6. 可扩展性
- 爬虫模块：可轻松添加新的数据源
- 指标计算：基于TA-Lib，可扩展自定义指标
- 选股策略：策略文件动态加载，支持热更新
- Web界面：Tornado异步框架，支持高并发


## 🎯 应用场景

### 开发人员
- 快速理解项目架构
- 定位模块和功能
- 进行代码重构和优化

### 运维人员
- 了解系统部署架构
- 监控关键流程节点
- 排查性能问题

### 产品经理
- 理解业务流程
- 评估功能实现成本
- 规划产品迭代

### 新成员
- 快速上手项目
- 理解技术选型
- 学习设计模式应用


## 📚 相关文档
- 项目README: `../README.md`
- 使用文档: `../instock/trade/usage.md`
- 配置文件: `../instock/config/trade_client.json`


## 🔗 在线渲染服务
渲染工具支持以下PlantUML服务器：
1. PlantUML官方服务器 (HTTPS)
2. PlantUML官方服务器 (HTTP)
3. PlantUML.com备用服务器
4. Kroki.io（支持更大图片）

如在线渲染失败，可简化PUML内容或使用本地Java渲染。
