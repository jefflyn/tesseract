<template>
  <div>
    <el-button type="primary" @click="fetchBasics" :loading="loading">
      获取基本信息
    </el-button>

    <el-table :data="basics" border style="margin-top: 20px">
      <el-table-column prop="symbol" label="商品代号" width="100" />
      <el-table-column prop="name" label="商品名" width="150" />
      <el-table-column prop="type" label="分类" width="100" />
      <el-table-column prop="exchange" label="交易所" width="120" />
      <el-table-column prop="amount" label="合同单位" width="100" />
      <el-table-column prop="unit" label="单位" width="80" />
      <el-table-column prop="step" label="每跳点数" width="100" />
      <el-table-column prop="profit" label="每跳毛利" width="100" />
      <el-table-column prop="night" label="夜盘" width="80">
        <template #default="scope">
          {{ scope.row.night === 1 ? '是' : scope.row.night === 0 ? '否' : '-' }}
        </template>
      </el-table-column>
      <el-table-column prop="update_time" label="更新时间" />
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const basics = ref([])
const loading = ref(false)

const API_BASE = 'http://localhost:5000/api'

const fetchBasics = async () => {
  loading.value = true
  try {
    const response = await axios.post(`${API_BASE}/basics/fetch`)
    ElMessage.success(`成功获取 ${response.data.count} 条基本信息`)
    loadBasics()
  } catch (error) {
    ElMessage.error('获取失败: ' + (error.response?.data?.error || error.message))
  } finally {
    loading.value = false
  }
}

const loadBasics = async () => {
  try {
    const response = await axios.get(`${API_BASE}/basics`)
    basics.value = response.data.data
  } catch (error) {
    ElMessage.error('加载失败: ' + error.message)
  }
}

onMounted(() => {
  loadBasics()
})
</script>
