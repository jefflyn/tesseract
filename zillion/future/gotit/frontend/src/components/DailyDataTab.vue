<template>
  <div>
    <el-form :inline="true">
      <el-form-item label="合约代码">
        <el-input v-model="searchSymbol" placeholder="输入合约代码" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="loadDailyData">查询</el-button>
        <el-button @click="clearSearch">清空</el-button>
      </el-form-item>
    </el-form>

    <el-button type="success" @click="fetchSingleContract" style="margin-bottom: 10px">
      获取单个合约数据
    </el-button>

    <el-button type="warning" @click="updateAllContracts" :loading="updating">
      更新所有主力合约
    </el-button>

    <el-table :data="dailyData" border style="margin-top: 20px" max-height="600">
      <el-table-column prop="symbol" label="商品代码" width="100" />
      <el-table-column prop="code" label="合约代码" width="120" />
      <el-table-column prop="trade_date" label="交易日期" width="120" />
      <el-table-column prop="open" label="开盘价" width="100" />
      <el-table-column prop="high" label="最高价" width="100" />
      <el-table-column prop="low" label="最低价" width="100" />
      <el-table-column prop="close" label="收盘价" width="100" />
      <el-table-column prop="deal_vol" label="成交量" width="120" />
      <el-table-column prop="close_change" label="涨跌幅" width="100" />
    </el-table>

    <el-pagination
      v-if="total > 0"
      layout="prev, pager, next"
      :total="total"
      :page-size="pageSize"
      @current-change="handlePageChange"
      style="margin-top: 20px; justify-content: center"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const dailyData = ref([])
const searchSymbol = ref('')
const total = ref(0)
const pageSize = ref(100)
const currentPage = ref(1)
const updating = ref(false)

const API_BASE = 'http://localhost:5000/api'

const loadDailyData = async () => {
  try {
    const params = {
      limit: pageSize.value,
      offset: (currentPage.value - 1) * pageSize.value
    }

    if (searchSymbol.value) {
      params.symbol = searchSymbol.value
    }

    const response = await axios.get(`${API_BASE}/daily-data`, { params })
    dailyData.value = response.data.data
    total.value = response.data.total
  } catch (error) {
    ElMessage.error('加载失败: ' + error.message)
  }
}

const clearSearch = () => {
  searchSymbol.value = ''
  currentPage.value = 1
  loadDailyData()
}

const fetchSingleContract = async () => {
  const symbol = prompt('请输入合约代码:')
  if (!symbol) return

  try {
    const response = await axios.post(`${API_BASE}/daily-data/fetch`, {
      symbol: symbol
    })
    ElMessage.success(`成功获取 ${response.data.count} 条数据`)
    loadDailyData()
  } catch (error) {
    ElMessage.error('获取失败: ' + (error.response?.data?.error || error.message))
  }
}

const updateAllContracts = async () => {
  updating.value = true
  try {
    const response = await axios.post(`${API_BASE}/daily-data/update-all`)
    ElMessage.success(`更新完成，共更新 ${response.data.results.length} 个合约`)
    loadDailyData()
  } catch (error) {
    ElMessage.error('更新失败: ' + (error.response?.data?.error || error.message))
  } finally {
    updating.value = false
  }
}

const handlePageChange = (page) => {
  currentPage.value = page
  loadDailyData()
}

onMounted(() => {
  loadDailyData()
})
</script>
