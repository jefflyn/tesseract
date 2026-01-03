// 全局变量，存储 DATA_MAP 和 DISPLAY_MAP
const dataMap = DATA_MAP;
const displayMap = DISPLAY_MAP;

// 渲染某个 Tab 的表格
function renderTab(tabType) {
    const tableContainer = document.getElementById("table-container");
    tableContainer.innerHTML = '';  // 清空之前的内容

    // 获取当前 tab 的布局数据
    const rows = displayMap[tabType] || [];
    const table = document.createElement("table");

    // 为表格添加标题行
    const headerRow = document.createElement("tr");
    // 不要表头
    // for (let i = 1; i <= 6; i++) {
    //   const th = document.createElement("th");
    //   th.innerText = `Column ${i}`;
    //   headerRow.appendChild(th);
    // }
    table.appendChild(headerRow);

    // 渲染每一行
    rows.forEach(row => {
        const tr = document.createElement("tr");

        row.forEach(cellId => {
            const td = document.createElement("td");
            if (cellId && dataMap[cellId]) {
                const data = dataMap[cellId];
                td.innerText = data.title;
                td.style.cssText = data.style || '';

                // 给单元格添加点击事件
                td.onclick = () => copyContent(data);
                // 给单元格添加双击事件
                td.ondblclick = () => showModal(data);

                // 添加单元格到行
                tr.appendChild(td);
            } else {
                const td = document.createElement("td");
                tr.appendChild(td);  // 空单元格
            }
        });

        // 添加行到表格
        table.appendChild(tr);
    });

    // 将表格插入到页面
    tableContainer.appendChild(table);
}

let clickTimer = null;
const CLICK_DELAY = 220; // 点击延迟时间

/* 复制单元格内容 */
function copyContent(data) {
    if (clickTimer) return; // 防止重复点击

    clickTimer = setTimeout(() => {
        // 单击：复制
        const text = data.title;
        navigator.clipboard.writeText(text)
            .then(() => showToast(text))
            .catch(err => console.error('复制失败:', err)); // 捕获复制失败的错误
        clickTimer = null;
    }, CLICK_DELAY);
}

/* 弹窗相关功能 */
function showModal(data) {
    // 双击：取消单击逻辑
    clearTimeout(clickTimer);
    clickTimer = null;

    const modal = document.getElementById('modal');
    const modalTitle = document.getElementById('modal-title');
    const modalDetails = document.getElementById('modal-details');
    const modalSubItems = document.getElementById('modal-sub-items');

    // 弹窗标题
    modalTitle.onclick = () => {
        // 点击复制到剪贴板
        navigator.clipboard.writeText(data.title);
        showToast(data.title);
    };

    // 设置弹窗内容
    modalTitle.innerText = data.title;
    if (!data || !data.details) {
        modalDetails.innerHTML = marked.parse(''); // 使用 marked.js 将 Markdown 转换为 HTML

    } else {
        modalDetails.innerHTML = marked.parse(data.details); // 使用 marked.js 将 Markdown 转换为 HTML

    }

    // 如果有子项，渲染子项列表
    modalSubItems.innerHTML = '';
    if (data.subItems && data.subItems.length > 0) {
        data.subItems.forEach(item => {
            const li = document.createElement('li');
            li.innerText = item;
            li.onclick = () => {
                // 点击复制到剪贴板
                navigator.clipboard.writeText(item);
                showToast(`${item}`);
            };
            modalSubItems.appendChild(li);
        });
    }

    // 显示弹窗
    modal.style.display = 'block';
}

// 关闭弹窗功能
function closeModal(event) {
    // 如果点击的是背景，关闭弹窗
    if (event && event.target.id === 'modal') {
        const modal = document.getElementById('modal');
        modal.style.display = 'none';
    }
}

/* 显示 Toast 提示 */
function showToast2(text) {
    const toast = document.createElement('div');
    toast.innerText = `已复制：${text}`;
    toast.className = 'toast';
    document.body.appendChild(toast);

    // 自动消失
    setTimeout(() => {
        toast.remove();
    }, 2000);
}

function showToast(text) {
    const toast = document.getElementById('toast');
    toast.innerText = '已复制: ' + text;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 1200);
}


// Tab 切换
function showTab(tabType) {
    renderTab(tabType);
}

// 默认加载第一个 Tab
showTab(1);
