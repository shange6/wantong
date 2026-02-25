<template>
  <div class="app-container">
    <!-- 搜索表单 -->
    <SearchForm
      v-model="queryParams"
      :source-data="tableRef?.internalData || []"
      :show-no="false"
      @update="handleFilterUpdate"
    />
    <!-- 数据表格 -->
    <CreateOrderTable ref="tableRef" />
    <!-- 分页 -->
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import SearchForm from "@/views/module_projects/SearchForm.vue";
import CreateOrderTable from "../../CreateOrderTable.vue";

const queryParams = ref({
  code: "",
  spec: "",
  material: "",
});

const tableRef = ref();

const handleFilterUpdate = (data: any[]) => {
  tableRef.value?.handleFilterUpdate(data);
};
</script>

<style scoped></style>