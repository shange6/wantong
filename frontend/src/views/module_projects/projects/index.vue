<template>
  <div class="app-container">
    <SearchForm
      v-model="queryFormData"
      :source-data="allTableData"
      :show-material="false"
      @update="handleFilterUpdate"
      @reset="handleResetQuery"
    />

    <ProjectsTable
      ref="projectTableRef"
      v-model:drawer-visible="projectDrawerVisible"
      :data="displayData"
      :current-page="pagination.currentPage"
      :page-size="pagination.pageSize"
      @row-click="handleProjectRowClick"
      @load-data="handleTableLoad"
      @update:current-page="(val) => (pagination.currentPage = val)"
      @update:page-size="(val) => (pagination.pageSize = val)"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from "vue";

import SearchForm from "../SearchForm.vue";
import ProjectsTable from "../ProjectsTable.vue";

defineOptions({
  name: "ProjectsIndex",
});

// --- 状态管理 ---
const projectTableRef = ref(); // 修正：与模板中的 ref 一致
const projectDrawerVisible = ref(false);

// 原始数据底稿（供 SearchForm 过滤用）
const allTableData = ref<any[]>([]);
// 过滤后的展示数据
const filteredData = ref<any[] | null>(null);

// 分页状态（必须在父组件管理，否则分页点击无效）
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
});

// 查询参数
const queryFormData = ref({
  project_code: undefined,
  code: undefined,
  spec: undefined,
  material: undefined,
  remark: undefined,
});

// 计算属性：优先显示过滤后的数据，否则显示全量数据
const displayData = computed(() => {
  return filteredData.value !== null ? filteredData.value : allTableData.value;
});

// --- 事件处理 ---

/**
 * 接收来自 ProjectTable 的 API 数据
 */
function handleTableLoad(data: any[]) {
  allTableData.value = data;
  filteredData.value = null; // 加载新数据时清空之前的过滤状态
}

/**
 * 响应 SearchForm 的前端过滤结果
 */
function handleFilterUpdate(filtered: any[]) {
  filteredData.value = filtered;
  pagination.currentPage = 1; // 过滤后自动回到第一页
}

/**
 * 重置查询：清空过滤状态
 */
function handleResetQuery() {
  filteredData.value = null;
  pagination.currentPage = 1;
}

/**
 * 项目行点击
 */
function handleProjectRowClick(row: any) {
  queryFormData.value.project_code = row.code;
  // 如果需要点击后重新请求后端：
  projectTableRef.value?.handleQuery?.();
}
</script>

<style scoped>
.app-container {
  /* 确保占满屏幕且不产生双滚动条 */
  height: 100vh;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>
