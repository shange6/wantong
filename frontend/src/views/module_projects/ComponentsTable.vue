<template>
  <div v-loading="loading" class="components-table">
    <MiddleTable
      v-bind="$attrs"
      :data="displayData"
      :current-page="pagination.currentPage"
      :page-size="pagination.pageSize"
      @update:current-page="(val: number) => (pagination.currentPage = val)"
      @update:page-size="(val: number) => (pagination.pageSize = val)"
    >
      <template #append-columns="{ formatWtCode }">
        <el-table-column type="selection" fixed min-width="20" align="center" />
        <el-table-column label="万通码" prop="wtcode" min-width="100" show-overflow-tooltip>
          <!-- <template #default="{ row }">
            <span class="wtcode-text">{{ formatWtCode(row.wtcode) }}</span>
          </template> -->
        </el-table-column>
        <el-table-column label="代号" prop="code" min-width="110" show-overflow-tooltip />
        <el-table-column label="名称" prop="spec" min-width="100" show-overflow-tooltip />
        <el-table-column label="数量" prop="count" min-width="40" align="center" />
        <el-table-column
          label="材料"
          prop="material"
          min-width="120"
          show-overflow-tooltip
          align="center"
        />
        <el-table-column label="单重" prop="unit_mass" min-width="60" align="center" />
        <el-table-column label="总重" prop="total_mass" min-width="70" align="center" />
        <el-table-column label="备注" prop="remark" min-width="80" show-overflow-tooltip />
        <slot name="operation-column"></slot>
      </template>
    </MiddleTable>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from "vue";
import MiddleTable from "./MiddleTable.vue";
import ComponentsAPI, {
  type ComponentsData,
  type ComponentsQuery,
} from "@/api/module_projects/components";

defineOptions({
  name: "ComponentsTable",
  inheritAttrs: false,
});

interface Props {
  data?: ComponentsData[];
  queryParams?: ComponentsQuery;
}

const props = withDefaults(defineProps<Props>(), {
  queryParams: () => ({}),
});

const emit = defineEmits<{
  (e: "load-data", data: ComponentsData[]): void;
}>();

// --- 状态管理 ---
const loading = ref<boolean>(false);
const internalData = ref<ComponentsData[]>([]); // 内部存储数组

// 内部管理分页状态
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
});

const displayData = computed<ComponentsData[]>(() => {
  // 优先使用父组件传递的数据（支持空数组，用于显示搜索无结果）
  // 仅当 props.data 为 undefined 时，才使用内部数据
  if (props.data !== undefined) {
    return props.data;
  }
  return internalData.value;
});

/**
 * 请求 API 数据
 * @param params 符合 ComponentsQuery 结构的查询对象
 */
const handleQuery = async (params?: ComponentsQuery) => {
  loading.value = true;
  try {
    const query = {
      ...params,
      page_no: 1, // 全量获取时，页码固定为 1
      page_size: 0, // 传 0 触发后端返回全量数据
    };
    const res = await ComponentsAPI.getList(query);
    internalData.value =
      res.data?.data?.items || (Array.isArray(res.data.data) ? res.data.data : []) || [];
    emit("load-data", internalData.value);
  } catch (error) {
    console.error("获取部件数据失败:", error);
    internalData.value = [];
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  // 只有当没有传入外部数据时，才主动触发内部查询
  if (props.data === undefined) {
    handleQuery(props.queryParams);
  }
});

// 暴露刷新方法给父组件
defineExpose({
  handleQuery,
});
</script>

<style scoped>
.components-table {
  flex: 1;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>
