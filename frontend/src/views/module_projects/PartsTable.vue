<template>
  <div v-loading="loading" class="parts-table">
    <MiddleTable
      v-bind="$attrs"
      :data="displayData"
      row-key="wtcode"
      :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
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
import { ref, computed, watch, onMounted } from "vue";
import MiddleTable from "./MiddleTable.vue";
import PartsAPI, { type PartsData, type PartsQuery } from "@/api/module_projects/parts";

defineOptions({
  name: "PartsTable",
  inheritAttrs: false,
});

interface Props {
  data?: PartsData[];
  queryParams?: PartsQuery;
  currentPage?: number;
  pageSize?: number;
}

const props = withDefaults(defineProps<Props>(), {
  queryParams: () => ({}),
  currentPage: 1,
  pageSize: 10,
});

const emit = defineEmits<{
  (e: "update:currentPage", val: number): void;
  (e: "update:pageSize", val: number): void;
  (e: "load-data", val: any[]): void;
}>();

// --- 4. 内部状态管理 ---
const loading = ref(false);
const internalData = ref<PartsData[]>([]); // 内部存储数组
const displayData = computed<PartsData[]>(() => {
  // 优先使用父组件传递的数据（支持空数组，用于显示搜索无结果）
  // 仅当 props.data 为 undefined 时，才使用内部数据
  if (props.data !== undefined) {
    if (!Array.isArray(props.data)) {
      return [];
    }
    return listToTree([...props.data]);
  }
  if (!Array.isArray(internalData.value)) {
    return [];
  }
  return listToTree([...internalData.value]);
});

/**
 * 请求 API 数据
 * @param params 符合 PartsQuery 结构的查询对象
 */
const handleQuery = async (params?: PartsQuery) => {
  loading.value = true;
  try {
    const res = await PartsAPI.getList(params || {});
    internalData.value =
      res.data?.data?.items || (Array.isArray(res.data.data) ? res.data.data : []) || [];
    emit("load-data", internalData.value); // 加载成功后向外抛出事件
  } catch (error) {
    console.error("获取零件数据失败:", error);
    internalData.value = [];
  } finally {
    loading.value = false;
  }
};

// 转换数组格式符合折叠标准
const listToTree = (data: any[]) => {
  const map: Record<string, any> = {};
  const roots: any[] = [];
  data.sort((a, b) => a.wtcode.length - b.wtcode.length || a.wtcode.localeCompare(b.wtcode));
  data.forEach((item) => {
    map[item.wtcode] = { ...item, children: [] };
  });
  data.forEach((item) => {
    const node = map[item.wtcode];
    const lastDotIndex = item.wtcode.lastIndexOf(".");
    if (lastDotIndex > -1) {
      const parentWtcode = item.wtcode.substring(0, lastDotIndex);
      if (map[parentWtcode]) {
        map[parentWtcode].children.push(node);
      } else {
        roots.push(node);
      }
    } else {
      roots.push(node);
    }
  });
  return roots;
};

const handlePageUpdate = (val: number) => emit("update:currentPage", val);
const handleSizeUpdate = (val: number) => emit("update:pageSize", val);

// 暴露刷新方法给父组件
defineExpose({
  handleQuery,
  listToTree,
});
</script>

<style scoped>
.parts-table {
  flex: 1;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>
