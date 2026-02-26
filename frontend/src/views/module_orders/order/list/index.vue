<template>
  <div class="app-container">
    <!-- 搜索表单 -->
    <SearchForm
      v-model="queryParams"
      :source-data="tableRef?.internalData || []"
      :show-no="false"
      :show-material="false"
      @update="handleFilterUpdate"
      @reset="handleFilterReset"
    />
    <!-- 数据表格 -->
    <ListOrderTable ref="tableRef" />
    <!-- 分页 -->
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import SearchForm from "@/views/module_projects/SearchForm.vue";
import ListOrderTable from "../../ListOrderTable.vue";

const queryParams = ref({
  code: "",
  spec: "",
  material: "",
});

const tableRef = ref();

const handleFilterUpdate = (data: any[]) => {
  tableRef.value?.handleFilterUpdate(data);
};

const handleFilterReset = () => {
  tableRef.value?.handleFilterUpdate(tableRef.value?.internalData || []);
};
</script>

<style scoped></style>