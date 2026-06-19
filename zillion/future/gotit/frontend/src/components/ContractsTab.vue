<template>
  <div>
    <el-button type="primary" @click="fetchContracts" :loading="loading" style="margin-right: 10px">
      获取主力合约
    </el-button>

    <el-button @click="loadContracts" style="margin-right: 10px">
      刷新
    </el-button>

    <el-checkbox v-model="showSelectedOnly" @change="loadContracts">
      仅显示选中
    </el-checkbox>

    <el-table :data="contracts" border style="margin-top: 20px">
      <el-table-column prop="symbol" label="商品代码" width="100" />
      <el-table-column prop="code" label="合约代码" width="120" />
      <el-table-column prop="ts_code" label="TS代码" width="150" />
      <el-table-column prop="main" label="主力" width="80">
        <template #default="scope">
          {{ scope.row.main === 1 ? '是' : '否' }}
        </template>
      </el-table-column>
      <el-table-column prop="low" label="最低价" width="100" />
      <el-table-column prop="high" label="最高价" width="100" />
      <el-table-column prop="selected" label="已选择" width="100">
        <template #default="scope">
          <el-checkbox
            v-model="scope.row.selected"
            @change="toggleSelect(scope.row)"
          />
        </template>
      </el-table-column>
      <el-table-column prop="create_time" label="创建时间" />
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const contracts = ref([])
const loading = ref(false)
const showSelectedOnly = ref(false)

const API_BASE = 'http://localhost:5000/api'

const fetchContracts = async () => {
  loading.value = true
  try {
    const response = await axios.post(`${API_BASE}/contracts/fetch`)
    ElMessage.success(`成功获取 ${response.data.count} 条合约信息`)
    loadContracts()
  } catch (error) {
    ElMessage.error('获取失败: ' + (error.response?.data?.error || error.message))
  } finally {
    loading.value = false
  }
}

const loadContracts = async () => {
  try {
    const params = showSelectedOnly.value ? { selected: 'true' } : {}
    const response = await axios.get(`${API_BASE}/contracts`, { params })
    contracts.value = response.data.data
  } catch (error) {
    ElMessage.error('加载失败: ' + error.message)
  }
}

const toggleSelect = async (contract) => {
  try {
    await axios.post(`${API_BASE}/contracts/${contract.code}/select`, {
      selected: contract.selected ? 1 : 0
    })
    ElMessage.success('更新成功')
  } catch (error) {
    ElMessage.error('更新失败: ' + error.message)
  }
}

onMounted(() => {
  loadContracts()
})
</script>
