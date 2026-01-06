function initGrid(rows = 5) {
  const grid = document.getElementById('layoutGrid');
  grid.innerHTML = '';

  for (let r = 0; r < rows * 6; r++) {
    const cell = document.createElement('div');
    cell.className = 'grid-cell';
    grid.appendChild(cell);
  }

  new Sortable(grid, {
    group: 'nav',
    animation: 150
  });
}

function loadLayout(data) {
  data.forEach(item => {
    const index = (item.row - 1) * 6 + (item.col - 1);
    const cell = document.querySelectorAll('.grid-cell')[index];
    cell.innerText = item.title;
    cell.dataset.id = item.id;
  });
}


function renderDataList(list) {
  const panel = document.getElementById('dataPanel');
  panel.innerHTML = '';

  list.forEach(item => {
    const div = document.createElement('div');
    div.className = 'data-item';
    div.dataset.id = item.id;
    div.innerText = item.title;
    panel.appendChild(div);
  });

  new Sortable(panel, {
    group: { name: 'nav', pull: 'clone', put: false },
    sort: false
  });
}

function saveLayout() {
  const cells = document.querySelectorAll('.grid-cell');
  const payload = [];

  cells.forEach((cell, index) => {
    if (!cell.dataset.id) return;

    payload.push({
      type: currentType,
      row: Math.floor(index / 6) + 1,
      col: (index % 6) + 1,
      dataId: cell.dataset.id
    });
  });

  fetch('/api/nav/layout/save', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
}
