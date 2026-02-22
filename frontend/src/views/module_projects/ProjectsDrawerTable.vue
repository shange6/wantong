<template>
  <div class="projects-table" v-loading="loading">
    <el-drawer
      v-model="drawerVisible"
      title="请选择项目"
      size="50%"
      append-to-body
      class="project-table-drawer"
      :close-on-click-modal="true"
      :close-on-press-escape="true"
      :show-close="true"
    >
      <div class="drawer-content-wrapper">
        <MiddleTable 
        v-bind="$attrs" 
        :data="displayData" 
        :current-page="pagination.currentPage"
        :page-size="pagination.pageSize"
        @row-click="handleRowClick"
        @update:current-page="(val) => pagination.currentPage = val"
        @update:page-size="(val) => pagination.pageSize = val"
        >
          <template #append-columns="{ formatWtCode }">
              <el-table-column type="selection" fixed width="40" align="center" />
              <el-table-column label="代号" prop="code" min-width="70" show-overflow-tooltip align="center" />
              <el-table-column label="名称" prop="name" min-width="120" show-overflow-tooltip />
              <el-table-column label="合同号" prop="no" min-width="40" show-overflow-tooltip align="center" />
              <slot name="operation-column"></slot>
          </template>
        </MiddleTable>
      </div>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, reactive, watch } from "vue";
import MiddleTable from "./MiddleTable.vue";
import ProjectsAPI, { type ProjectsData, type ProjectsQuery } from "@/api/module_projects/projects";

defineOptions({
  name: "ProjectsDrawerTable",
  inheritAttrs: false,
});

interface Props {
  drawerVisible: boolean;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  (e: 'row-click', row: ProjectsData): void;
  (e: 'update:drawerVisible', val:boolean): void;
}>();

// --- 状态管理 ---
const loading = ref<boolean>(false);
const internalData = ref<ProjectsData[]>([]); 

// 内部维护分页
const pagination = reactive({
  currentPage: 1,
  pageSize: 10
});

const displayData = computed<ProjectsData[]>(() => {
  return internalData.value;
});

const drawerVisible = computed({
  get: () => props.drawerVisible,
  set: (val) => emit("update:drawerVisible", val),
});

/**
 * 请求 API 数据
 */
const handleQuery = async (params?: ProjectsQuery) => {
  loading.value = true;
  try {
    const res = await ProjectsAPI.getList(params || {});
    // 兼容后端返回结构
    const rawData = res.data?.data?.items || (Array.isArray(res.data.data) ? res.data.data : []) || [];  
    internalData.value = rawData;
  } catch (error) {
    console.error("获取项目数据失败:", error);
    internalData.value = [];
  } finally {
    loading.value = false;
  }
};

// 监听抽屉打开，自动刷新数据
watch(() => props.drawerVisible, (val) => {
  if (val) {
    handleQuery();
  }
});

// 暴露刷新方法
defineExpose({ 
  handleQuery 
});

onMounted(() => {
  // 初始可以不加载，等打开抽屉再加载，或者预加载
  // handleQuery();
});

const handleRowClick = (row: ProjectsData) => {
  emit('row-click', row);
  // 选择后自动关闭抽屉
  emit('update:drawerVisible', false);
};
</script>

<style scoped>
/* 宿主容器不需要占位，因为是弹窗 */
.projects-table {
  width: 0;
  height: 0;
  overflow: hidden;
}

/* 抽屉内部容器 */
.drawer-content-wrapper {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>
<style>
/* 全局样式覆盖 el-drawer__body 以支持 flex */
.project-table-drawer .el-drawer__body {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>