<template>
  <div class="components-table-container">
    <BaseCard
      ref="dataTableRef"
      v-loading="loading"
      row-key="wtcode"
      :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
      :data="pageTableData"
      :header-cell-style="{ textAlign: 'center' }"
      class="data-table__content"
      border
      stripe
      height="100%"
      @selection-change="handleSelectionChange"
      @row-click="handleRowClick"
    >
      <template #pagination-area>
        <el-pagination
          v-model:current-page="pagination.page_no"
          v-model:page-size="pagination.page_size"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleQuery"
          @current-change="handleQuery"
        />
      </template>
    </BaseCard>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import BaseCard from "./BaseCard.vue";
import ComponentsAPI, {
  ComponentsData,
  ComponentsForm,
  ComponentsQuery,
} from "@/api/module_projects/components";

// 表格状态
const loading = ref(false);
const pageTableData = ref<any[]>([]); // 当前显示的树（可能是过滤后的）
const total = ref(0);
const selectIds = ref<number[]>([]);
const dataTableRef = ref();
const pagination = reactive({
  page_no: 1,
  page_size: 10,
});

const props = defineProps<{
  queryParams?: ComponentsQuery;
}>();

const emit = defineEmits<{
  (e: "row-click", row: ComponentsData): void;
  (e: "load-data", data: ComponentsData[]): void; // 新增：数据加载完成后传给父组件
}>();

// 组件名称
defineOptions({
  name: "ComponentsTable",
});

// 【关键修改点】
// 暴露 pageTableData 让父组件可以直接修改它（实现前端过滤结果的注入）
defineExpose({
  handleQuery,
  pageTableData,
  loading,
});

/**
 * 查询方法：
 * 在你的业务场景下，它负责从后端获取“原始全量数据”
 */
async function handleQuery() {
  // 如果没有项目代码，不执行查询
  // if (!props.queryParams?.project_code) return;

  loading.value = true;
  try {
    const params = {
      ...props.queryParams,
      // 如果要前端过滤，通常后端不分页，传一个很大的 page_size 或特定参数
      page_no: pagination.page_no,
      page_size: pagination.page_size,
    };
    const res = await ComponentsAPI.getList(params);
    // 修正路径：增加对 res.data.data.items 的兼容
    const rawData = res.data?.items || res.data?.data?.items || [];
    const totalCount = res.data?.total || res.data?.data?.total || 0;

    // 1. 更新本地显示
    pageTableData.value = rawData;
    total.value = totalCount;

    // 2. 关键：把拿到的原始全量数据抛给父组件，让 SearchForm 有“原材料”可以过滤
    emit("load-data", rawData);
  } finally {
    loading.value = false;
  }
}

// 表格选择
function handleSelectionChange(selection: ComponentsData[]) {
  selectIds.value = selection.map((item) => item.id);
}

// 表格行点击
function handleRowClick(row: ComponentsData) {
  emit("row-click", row);
}
</script>

<style scoped>
.components-table-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>
