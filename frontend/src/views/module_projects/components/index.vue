<template>
  <div class="app-container">
    <SearchForm 
      v-model:modelValue="queryFormData" 
      :source-data="allTableData"
      :show-no="false"
      @update="handleFilterUpdate"
      @reset="handleResetQuery"
    >
      <template #extra>
        <el-button
          v-hasPerm="['module_system:menu:query']"
          type="info"
          icon="arrow-right"
          @click="handleOpenProjectDrawer"
        >
          项目
        </el-button>
      </template>
    </SearchForm>

    <ComponentsTable 
      ref="tableRef" 
      :query-params="queryFormData"
      @load-data="handleTableLoad" 
    />

    <ProjectTable 
      ref="projectTableRef" 
      v-model:drawerVisible="projectDrawerVisible" 
      @row-click="handleProjectRowClick"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import SearchForm from '../SearchForm.vue';
import { ComponentsQuery } from '@/api/module_projects/components';
import ComponentsTable from '../ComponentsTable.vue';
import ProjectTable from '../ProjectTable.vue';

// 组件名称
defineOptions({
  name: "Components",
});

const projectDrawerVisible = ref(false);
const tableRef = ref();

// --- 数据状态管理 ---
// 存储从后端拿到的全量原始数据，作为 SearchForm 过滤的“底稿”
const allTableData = ref<any[]>([]);

// 查询表单数据
const queryFormData = reactive<ComponentsQuery>({
  project_code: undefined,
  code: undefined,
  spec: undefined,
  material: undefined,
  remark: undefined,
});

/**
 * 1. 响应 ComponentsTable 加载完成的事件
 * 当表格从后端获取到原始数据时，存入 allTableData 供 SearchForm 使用
 */
function handleTableLoad(data: any[]) {
  allTableData.value = data;
}

/**
 * 2. 响应 SearchForm 的前端过滤结果
 * 直接把过滤后的结果塞回表格组件的 pageTableData 中显示
 */
function handleFilterUpdate(filtered: any[]) {
  if (tableRef.value) {
    tableRef.value.pageTableData = filtered;
  }
}

/**
 * 初始进入页面自动加载
 */
onMounted(async () => {
  // 1. 如果有特定的默认逻辑，可以在这里给 queryFormData.project_code 赋值
  // 2. 触发 ComponentsTable 内部的 handleQuery 进行 API 请求
  if (tableRef.value) {
    await tableRef.value.handleQuery();
  }
});

/**
 * 3. 项目切换
 * 项目变了，直接调用表格的 handleQuery 去后端拉取新项目的全量数据
 */
function handleProjectRowClick(code: string) {
  queryFormData.project_code = code;
  // 调用表格内部暴露的查询方法
  tableRef.value?.handleQuery();
}

/**
 * 4. 重置查询
 * 恢复显示全量原始数据
 */
function handleResetQuery() {
  if (tableRef.value) {
    tableRef.value.pageTableData = allTableData.value;
  }
}

const handleOpenProjectDrawer = () => {
  projectDrawerVisible.value = !projectDrawerVisible.value;
};
</script>

<style scoped>
.app-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  height: 100%;
}
</style>