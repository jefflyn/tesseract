// app.js

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
        td.onclick = () => showModal(data);

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

// 显示弹窗
function showModal(data) {
  document.getElementById("modal-title").innerText = data.title;
  document.getElementById("modal-details").innerText = data.details;

  // 清空并渲染 subItems
  const subItemsList = document.getElementById("modal-sub-items");
  subItemsList.innerHTML = '';
  data.subItems.forEach(item => {
    const li = document.createElement("li");
    li.innerText = item;
    li.onclick = () => {
      // 点击复制到剪贴板
      navigator.clipboard.writeText(item);
      alert(`已复制：${item}`);
    };
    subItemsList.appendChild(li);
  });

  // 显示弹窗
  document.getElementById("modal").style.display = "block";
}

// 关闭弹窗
function closeModal() {
  document.getElementById("modal").style.display = "none";
}

// Tab 切换
function showTab(tabType) {
  renderTab(tabType);
}

// 默认加载第一个 Tab
showTab(1);
