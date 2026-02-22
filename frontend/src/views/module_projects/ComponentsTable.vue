<template>
  <div class="components-table" v-loading="loading">
    <MiddleTable 
      v-bind="$attrs" 
      :data="displayData" 
      :current-page="currentPage"
      :page-size="pageSize"
      @update:current-page="handlePageUpdate"
      @update:page-size="handleSizeUpdate"
    >
      <template #append-columns="{ formatWtCode }">
        <el-table-column type="selection" fixed min-width="20" align="center" />        
        <el-table-column label="万通码" prop="wtcode" min-width="100" show-overflow-tooltip>
          <template #default="{ row }">
            <span class="wtcode-text">{{ formatWtCode(row.wtcode) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="代号" prop="code" min-width="110" show-overflow-tooltip />
        <el-table-column label="名称" prop="spec" min-width="100" show-overflow-tooltip />
        <el-table-column label="数量" prop="count" min-width="40" align="center" />
        <el-table-column label="材料" prop="material" min-width="120" show-overflow-tooltip align="center" />
        <el-table-column label="单重" prop="unit_mass" min-width="60" align="center" />
        <el-table-column label="总重" prop="total_mass" min-width="70" align="center" />
        <el-table-column label="备注" prop="remark" min-width="80" show-overflow-tooltip />
        <slot name="operation-column"></slot>
      </template>
    </MiddleTable>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import MiddleTable from "./MiddleTable.vue";
import ComponentsAPI, { type ComponentsData, type ComponentsQuery } from "@/api/module_projects/components";

defineOptions({
  name: "ComponentsTable",
  inheritAttrs: false,
});

interface Props {
  data?: ComponentsData[];
  queryParams?: ComponentsQuery; 
  currentPage?: number;
  pageSize?: number;
}

const props = withDefaults(defineProps<Props>(), {
  queryParams: () => ({}),
  currentPage: 1,
  pageSize: 10,
});

const emit = defineEmits<{
  (e: 'update:currentPage', val: number): void;
  (e: 'update:pageSize', val: number): void;
  (e: 'load-data', data: ComponentsData[]): void;
}>();


// --- 状态管理 ---
const loading = ref<boolean>(false);
const internalData = ref<ComponentsData[]>([]); // 内部存储数组
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
    const res = await ComponentsAPI.getList(params || {});
    internalData.value = res.data?.data?.items || (Array.isArray(res.data.data) ? res.data.data : []) || [];
    emit('load-data', internalData.value);    
  } catch (error) {
    console.error("获取部件数据失败:", error);
    internalData.value = [];
  } finally {
    loading.value = false;
  }
};

// 事件转发逻辑
const handlePageUpdate = (val: number) => emit('update:currentPage', val);
const handleSizeUpdate = (val: number) => emit('update:pageSize', val);

// 暴露刷新方法给父组件
defineExpose({ 
  handleQuery 
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