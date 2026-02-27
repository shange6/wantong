<template>
  <div class="app-container">
    <!-- 搜索表单 -->
    <SearchForm
      v-model="queryFormData"
      :source-data="tableRef?.internalData || []"
      :show-no="false"
      @update="handleFilterUpdate"
      @reset="handleFilterReset"
    />
    <!-- 数据表格 -->
    <CreateOrderTable ref="tableRef" />
    <!-- 分页 -->
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import SearchForm from "@/views/module_projects/SearchForm.vue";
import CreateOrderTable from "@/views/module_orders/CreateOrderTable.vue";

const tableRef = ref();

// 查询参数
const queryFormData = ref({
  code: undefined,
  spec: undefined,
  material: undefined,
});

/**
 * 响应 SearchForm 的前端过滤结果
 */
function handleFilterUpdate(filtered: any[]) {
  tableRef.value?.handleFilterUpdate(filtered);
}

/**
 * 重置查询：恢复全量显示
 */
function handleFilterReset() {
  tableRef.value?.handleFilterUpdate(tableRef.value?.internalData || []);
}
</script>

<style scoped></style>
