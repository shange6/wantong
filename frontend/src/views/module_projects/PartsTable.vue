<template>
  <div v-loading="loading" class="parts-table">
    <MiddleTable
      v-bind="$attrs"
      :data="displayData"
      row-key="wtcode"
      :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
      :current-page="pagination.currentPage"
      :page-size="pagination.pageSize"
      @update:current-page="(val) => (pagination.currentPage = val)"
      @update:page-size="(val) => (pagination.pageSize = val)"
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
import { ref, reactive, computed, watch, onMounted } from "vue";
import MiddleTable from "./MiddleTable.vue";
import PartsAPI, { type PartsData, type PartsQuery } from "@/api/module_projects/parts";

defineOptions({
  name: "PartsTable",
  inheritAttrs: false,
});

interface Props {
  data?: PartsData[];
  queryParams?: PartsQuery;
}

const props = withDefaults(defineProps<Props>(), {
  queryParams: () => ({}),
});

const emit = defineEmits<{
  (e: "load-data", val: any[]): void;
}>();

// --- 4. 内部状态管理 ---
const loading = ref(false);
const internalData = ref<PartsData[]>([]); // 内部存储数组

// 内部管理分页状态
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
});

const displayData = computed<PartsData[]>(() => {
  // 1. 获取基础数据
  let rawData: PartsData[] = [];
  if (props.data !== undefined) {
    rawData = Array.isArray(props.data) ? [...props.data] : [];
  } else {
    rawData = Array.isArray(internalData.value) ? [...internalData.value] : [];
  }

  // 2. 检查数据是否已经是树形结构（如果包含 children 且有值，说明已经被处理过）
  const isAlreadyTree = rawData.some((item) => Array.isArray(item.children) && item.children.length > 0);

  if (isAlreadyTree) {
    return rawData;
  }

  // 3. 转换为树形结构
  return listToTree(rawData);
});

/**
 * 请求 API 数据
 * @param params 符合 PartsQuery 结构的查询对象
 */
const handleQuery = async (params?: PartsQuery) => {
  loading.value = true;
  try {
    const query = {
      ...params,
      page_no: 1, // 全量获取时，页码固定为 1
      page_size: 0, // 传 0 触发后端返回全量数据
    };
    const res = await PartsAPI.getList(query);
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

// --- 5. 辅助方法：列表转树形结构 ---
function listToTree(data: PartsData[]): PartsData[] {
  const map: Record<string, PartsData> = {};
  const tree: PartsData[] = [];

  data.sort((a, b) => a.wtcode.length - b.wtcode.length);

  data.forEach((item) => {
    map[item.wtcode] = { ...item, children: [] };
  });

  data.forEach((item) => {
    const lastDotIndex = item.wtcode.lastIndexOf(".");
    if (lastDotIndex > -1) {
      const parentCode = item.wtcode.substring(0, lastDotIndex);
      if (map[parentCode]) {
        map[parentCode].children?.push(map[item.wtcode]);
      } else {
        tree.push(map[item.wtcode]);
      }
    } else {
      tree.push(map[item.wtcode]);
    }
  });

  return tree;
}

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
.parts-table {
  flex: 1;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>
