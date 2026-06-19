<template>
  <div id="app">
    <el-container>
      <el-header>
        <h1>期货数据管理系统</h1>
      </el-header>

      <el-main>
        <el-tabs v-model="activeTab">
          <el-tab-pane label="基本信息" name="basics">
            <BasicsTab />
          </el-tab-pane>

          <el-tab-pane label="合约管理" name="contracts">
            <ContractsTab />
          </el-tab-pane>

          <el-tab-pane label="日K数据" name="daily">
            <DailyDataTab />
          </el-tab-pane>
        </el-tabs>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import BasicsTab from './components/BasicsTab.vue'
import ContractsTab from './components/ContractsTab.vue'
import DailyDataTab from './components/DailyDataTab.vue'

const activeTab = ref('basics')
</script>

<style>
#app {
  font-family: Arial, sans-serif;
}

.el-header {
  background-color: #409eff;
  color: white;
  display: flex;
  align-items: center;
}

.el-header h1 {
  margin: 0;
}
</style>
