<template>
  <div v-loading="loading" class="list-order-table">
    <MiddleTable
      v-bind="$attrs"
      :data="displayData"
      :current-page="pagination.currentPage"
      :page-size="pagination.pageSize"
      @update:current-page="(val: number) => (pagination.currentPage = val)"
      @update:page-size="(val: number) => (pagination.pageSize = val)"
    >
      <template #append-columns>
        <el-table-column label="代号" prop="code" min-width="150" show-overflow-tooltip />
        <el-table-column label="名称" prop="spec" min-width="120" show-overflow-tooltip />
        <el-table-column label="数量" prop="count" min-width="40" align="center" />        
        <el-table-column min-width="100" align="center">
          <template #header>
            <div>下料</div>
            <div>时间/工时</div>
          </template>
          <template #default="{ row }">
              <div>{{ row.blanking_time || '-' }}</div>
              <div>{{ row.blanking_laborhour || '-' }}</div>
          </template>
        </el-table-column>

        <el-table-column min-width="100" align="center">
          <template #header>
            <div>铆焊</div>
            <div>时间/工时</div>
          </template>
          <template #default="{ row }">
              <div>{{ row.rivetweld_time || '-' }}</div>
              <div>{{ row.rivetweld_laborhour || '-' }}</div>
          </template>
        </el-table-column>

        <el-table-column min-width="100" align="center">
          <template #header>
            <div>加工</div>
            <div>时间/工时</div>
          </template>
          <template #default="{ row }">
              <div>{{ row.machine_time || '-' }}</div>
              <div>{{ row.machine_laborhour || '-' }}</div>
          </template>
        </el-table-column>

        <el-table-column min-width="100" align="center">
          <template #header>
            <div>装配</div>
            <div>时间/工时</div>
          </template>          
          <template #default="{ row }">
              <div>{{ row.fitting_time || '-' }}</div>
              <div>{{ row.fitting_laborhour || '-' }}</div>
          </template>
        </el-table-column>

        <el-table-column min-width="100" align="center">
          <template #header>
            <div>喷漆</div>
            <div>时间/工时</div>
          </template>
          <template #default="{ row }">
              <div>{{ row.painting_time || '-' }}</div>
              <div>{{ row.painting_laborhour || '-' }}</div>
          </template>
        </el-table-column>
        <el-table-column label="备注" prop="components_remark" min-width="100" show-overflow-tooltip />
        <slot name="operation-column"></slot>
      </template>
    </MiddleTable>

    <OrderDialog
      v-model="dialogVisible"
      :data="selectedRow"
      :title="dialogTitle"
      @success="handleQuery"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from "vue";
import MiddleTable from "@/views/module_projects/MiddleTable.vue";
import OrderDialog from "./OrderDialog.vue";
import OrdersAPI, { type OrdersData, type OrdersFilter } from "@/api/module_orders/orders";

defineOptions({
  name: "ListOrderTable",
  inheritAttrs: false,
});

interface Props {
  data?: OrdersData[];
  queryParams?: OrdersFilter;
}

const props = withDefaults(defineProps<Props>(), {
  queryParams: () => ({}),
});

const emit = defineEmits<{
  (e: "load-data", data: OrdersData[]): void;
}>();

// --- 状态管理 ---
const loading = ref<boolean>(false);
const internalData = ref<OrdersData[]>([]); // 原始全量数据
const filteredData = ref<OrdersData[]>([]); // 过滤后的展示数据

// 内部管理分页状态
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
});

const displayData = computed<OrdersData[]>(() => {
  // 优先使用父组件传递的数据
  if (props.data !== undefined) {
    return props.data;
  }
  return filteredData.value;
});

/**
 * 请求 API 数据
 */
const handleQuery = async (params?: OrdersFilter) => {
  loading.value = true;
  try {
    const query = {
      ...params,
      page_no: 1, // 全量获取时，页码固定为 1
      page_size: 0, // 传 0 触发后端返回全量数据
    };
    const res = await OrdersAPI.getList(query as any);
    const items = (res.data as any)?.data?.items || res.data?.items || [];
    internalData.value = items;
    filteredData.value = items; // 默认显示全量数据
    emit("load-data", items);
  } catch (error) {
    console.error("获取已排产工单列表失败:", error);
    internalData.value = [];
    filteredData.value = [];
  } finally {
    loading.value = false;
  }
};

const handleFilterUpdate = (data: any[]) => {
  filteredData.value = data;
  pagination.currentPage = 1; // 过滤后重置到第一页
};

onMounted(() => {
  // 只有当没有传入外部数据时，才主动触发内部查询
  if (props.data === undefined) {
    handleQuery(props.queryParams);
  }
});

// 暴露方法给父组件
defineExpose({
  handleQuery,
  handleFilterUpdate,
  internalData,
});

const dialogVisible = ref(false);
const dialogTitle = ref("填写工时");
const selectedRow = ref<any | null>(null);

function handleOpenDialog(row: any) {
  selectedRow.value = row;
  dialogTitle.value = "填写工时";
  dialogVisible.value = true;
}
</script>

<style scoped>
.list-order-table {
  flex: 1;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}


</style>
