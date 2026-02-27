<template>
  <div v-loading="loading" class="projects-table">
    <MiddleTable
      v-bind="$attrs"
      :data="displayData"
      :current-page="pagination.currentPage"
      :page-size="pagination.pageSize"
      @row-click="handleRowClick"
      @update:current-page="(val: number) => (pagination.currentPage = val)"
      @update:page-size="(val: number) => (pagination.pageSize = val)"
    >
      <template #append-columns="{ formatWtCode }">
        <el-table-column type="selection" fixed width="40" align="center" />
        <el-table-column
          label="代号"
          prop="code"
          min-width="90"
          show-overflow-tooltip
          align="center"
        />
        <el-table-column label="名称" prop="name" min-width="300" show-overflow-tooltip />
        <el-table-column
          label="合同号"
          prop="no"
          min-width="80"
          show-overflow-tooltip
          align="center"
        />
        <slot name="operation-column"></slot>
      </template>
    </MiddleTable>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from "vue";
import MiddleTable from "./MiddleTable.vue";
import ProjectsAPI, { type ProjectsData, type ProjectsQuery } from "@/api/module_projects/projects";

interface Props {
  data?: ProjectsData[]; // 使用 API 定义的项目数据类型
}

const props = defineProps<Props>();

const emit = defineEmits<{
  (e: "row-click", row: ProjectsData): void;
  (e: "load-data", data: ProjectsData[]): void;
}>();

defineOptions({
  name: "ProjectsTable",
  inheritAttrs: false,
});

// --- 状态管理 ---
const loading = ref<boolean>(false);
const internalData = ref<ProjectsData[]>([]); // 内部存储数组

// 内部管理分页状态
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
});

const displayData = computed<ProjectsData[]>(() => {
  // 优先使用父组件传递的数据（支持空数组，用于显示搜索无结果）
  // 仅当 props.data 为 undefined 时，才使用内部数据
  if (props.data !== undefined) {
    return props.data;
  }
  return internalData.value;
});

/**
 * 请求 API 数据
 * @param params 符合 ProjectsQuery 结构的查询对象
 */
const handleQuery = async (params?: ProjectsQuery) => {
  loading.value = true;
  try {
    const query = {
      ...params,
      page_no: 1, // 全量获取时，页码固定为 1
      page_size: 0, // 传 0 触发后端返回全量数据
    };
    const res = await ProjectsAPI.getList(query);

    // 兼容后端返回结构 { data: { items: [], total: 0 } }
    const rawData =
      res.data?.data?.items || (Array.isArray(res.data.data) ? res.data.data : []) || [];
    internalData.value = rawData;
    emit("load-data", rawData);
  } catch (error) {
    console.error("获取项目数据失败:", error);
    internalData.value = [];
  } finally {
    loading.value = false;
  }
};

const handleRowClick = (row: ProjectsData) => {
  // emit("row-click", row);
};

onMounted(() => {
  // 只有当没有传入外部数据时，才主动触发内部查询
  // if (props.data === undefined) {
    handleQuery();
  // }
});

// 暴露刷新方法给父组件
defineExpose({
  handleQuery,
});
</script>

<style scoped>
.projects-table {
  flex: 1;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>
