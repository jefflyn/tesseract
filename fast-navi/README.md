**工具架构**

SQLite (nav.db)
↓
FastAPI
↓
editor.html
↓
generate.py
↓
静态 index.html

**使用步骤**

1. 先启动 uvicorn backend_fastapi:app --reload --port 8000
2. 打开editor_v2.html编辑布局，数据存储在<pre><code>sqlite</code></pre>
3. 知识库内容通过sqlite数据库管理
4. 执行fast-navi/utils/export_js_data.py，生成页面数据data.js，包含页面布局和知识库数据
5. 本地浏览器打开fast-navi/kbm-nav/kbm-index.html即可，其他设备浏览可以把数据拷贝到fast-navi/kbm-nav/kbm-index-standalone.html，浏览器打开
