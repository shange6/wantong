<template>
  <div v-loading="loading" class="create-order-table">
    <ListCreateLaborhourTable
      :data="filteredData"
      :current-page="pagination.currentPage"
      :page-size="pagination.pageSize"
      v-bind="$attrs"
      @update:current-page="(val: number) => (pagination.currentPage = val)"
      @update:page-size="(val: number) => (pagination.pageSize = val)"
    >
      <template #operation-column>
        <el-table-column fixed="right" label="操作" align="center" min-width="60">
          <template #default="scope">
            <el-button
              v-hasPerm="['module_orders:order:create']"
              type="primary"
              size="small"
              link
              icon="plus"
              @click="handleOpenDialog(scope.row)"
            >
              工时
            </el-button>
          </template>
        </el-table-column>
      </template>
    </ListCreateLaborhourTable>

    <LaborhourDialog
      v-model="dialogVisible"
      :data="selectedRow"
      :title="dialogTitle"
      @success="handleQuery"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import ListCreateLaborhourTable from "@/views/module_orders/ListCreateLaborhourTable.vue";
import LaborhourDialog from "./LaborhourDialog.vue";
import OrdersAPI from "@/api/module_orders/orders";

defineOptions({
  name: "CreateLaborhourTable",
  inheritAttrs: false,
});

interface Props {
  queryParams?: Record<string, any>;
}

const props = withDefaults(defineProps<Props>(), {
  queryParams: () => ({}),
});

const emit = defineEmits<{
  (e: "load-data", data: any[]): void;
}>();

const loading = ref(false);
const internalData = ref<any[]>([]);
const filteredData = ref<any[]>([]);

// 内部管理分页状态
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
});

/**
 * 请求 API 数据
 * @param params 查询对象
 */
const handleQuery = async (params?: Record<string, any>) => {
  loading.value = true;
  try {
    const query = {
      page_no: 1, // 全量获取时，页码固定为 1
      page_size: 0, // 传 0 触发后端返回全量数据
      ...(props.queryParams || {}),
      ...(params || {}),
    };
    const res = await OrdersAPI.getUnLaborhourList(query);
    internalData.value = res.data?.data?.items || res.data?.items || [];
    filteredData.value = internalData.value; // 默认显示全量数据
    emit("load-data", internalData.value);
  } catch (error) {
    console.error("获取待填写工时列表失败:", error);
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

// 暴露刷新方法给父组件
defineExpose({
  handleQuery,
  handleFilterUpdate,
  internalData,
});

const dialogVisible = ref(false);
const dialogTitle = ref("填写工时");
const selectedRow = ref<any | null>(null);

async function handleOpenDialog(row: any) {
  selectedRow.value = row;
  dialogVisible.value = true;
}

onMounted(() => {
  handleQuery();
});

</script>

<style scoped>
.create-order-table {
  flex: 1;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>
