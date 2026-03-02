<template>
  <div class="app-container">
    <SearchForm
      v-model="queryFormData"
      :source-data="partsTableVisible ? allPartsData : allComponentsData"
      :show-no="false"
      @update="handleFilterUpdate"
      @reset="handleFilterReset"
    >
      <template #extra>
        <el-button
          v-hasPerm="['module_system:menu:query']"
          type="info"
          @click="handleOpenProjectDrawer"
        >
          📂 项目
        </el-button>
        <el-button v-hasPerm="['module_projects:parts:query']" type="warning" @click="toggleTable">
          {{ partsTableVisible ? "切换组件" : "切换BOM" }}
        </el-button>
      </template>
    </SearchForm>

    <PartsTable
      v-show="partsTableVisible"
      ref="partsTableRef"
      :data="partsData"
      :current-page="paginationParts.currentPage"
      :page-size="paginationParts.pageSize"
      @load-data="handlePartsLoad"
      @update:current-page="(val: number) => (paginationParts.currentPage = val)"
      @update:page-size="(val: number) => (paginationParts.pageSize = val)"
    />

    <ComponentsTable
      v-show="!partsTableVisible"
      ref="componentsTableRef"
      :data="componentsData"
      :current-page="paginationComponents.currentPage"
      :page-size="paginationComponents.pageSize"
      @row-click="handleComponentRowClick"
      @load-data="handleComponentsLoad"
      @update:current-page="(val: number) => (paginationComponents.currentPage = val)"
      @update:page-size="(val: number) => (paginationComponents.pageSize = val)"
    />

    <ProjectsDrawerTable
      :drawer-visible="projectDrawerVisible"
      @update:drawer-visible="(val) => (projectDrawerVisible = val)"
      @row-click="handleProjectRowClick"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from "vue";
import SearchForm from "../SearchForm.vue";
import PartsTable from "../PartsTable.vue";
import ComponentsTable from "../ComponentsTable.vue";
import ProjectsDrawerTable from "../ProjectsDrawerTable.vue";

defineOptions({ name: "ProjectsIndex" });

// --- 1. 引用定义 (Refs) ---
const componentsTableRef = ref();
const partsTableRef = ref();
const partsTableVisible = ref(false);
const projectDrawerVisible = ref(false);

// --- 2. 状态管理 (State) ---
const selectedComponent = ref<any>(null);

// 组件表状态
const allComponentsData = ref<any[]>([]);
const filteredComponentsData = ref<any[] | null>(null);
const paginationComponents = reactive({ currentPage: 1, pageSize: 10 });

// 零件表状态
const allPartsData = ref<any[]>([]);
const filteredPartsData = ref<any[] | null>(null);
const paginationParts = reactive({ currentPage: 1, pageSize: 10 });

// 查询参数
const queryFormData = ref({
  project_code: undefined,
  code: undefined,
  spec: undefined,
  material: undefined,
  remark: undefined,
});

// --- 3. 数据展示逻辑 (Computed) ---
const componentsData = computed(() => {
  return filteredComponentsData.value !== null
    ? filteredComponentsData.value
    : allComponentsData.value;
});

const partsData = computed(() => {
  return filteredPartsData.value !== null ? filteredPartsData.value : allPartsData.value;
});

// 搜索过滤
function handleFilterUpdate(filtered: any[]) {
  if (partsTableVisible.value) {
    // 如果当前在看零件表
    filteredPartsData.value = filtered;
    paginationParts.currentPage = 1;
  } else {
    // 如果当前在看组件表
    filteredComponentsData.value = filtered;
    paginationComponents.currentPage = 1;
  }
}

// 行点击联动逻辑 🔗
function handleComponentRowClick(row: any) {
  selectedComponent.value = row;
  // 核心：调用 PartsTable 暴露的方法请求新数据
  partsTableRef.value?.handleQuery({
    component_wtcode: row.wtcode,
  });
  partsTableVisible.value = true;
}

function handleProjectRowClick(row: any) {
  // queryFormData.value.project_code = undefined;
  // queryFormData.value.code = row.code; // 这里的 row.code 是项目的代号，不应该赋值给搜索框的代号
  componentsTableRef.value?.handleQuery?.({ code: row.code });
}

const handleFilterReset = () => {
  if (partsTableVisible.value) {
    filteredPartsData.value = null;
    paginationParts.currentPage = 1;
  } else {
    filteredComponentsData.value = null;
    paginationComponents.currentPage = 1;
  }
};

const handleOpenProjectDrawer = () => {
  projectDrawerVisible.value = !projectDrawerVisible.value;
};

// 切换表格展示
function toggleTable() {
  partsTableVisible.value = !partsTableVisible.value;
}

/**
 * 处理组件表加载的数据
 * 当 ComponentsTable 完成 API 请求后触发
 */
function handleComponentsLoad(data: any[]) {
  // 1. 存储全量数据，供 SearchForm 作为搜索源
  allComponentsData.value = data;
  // 2. 加载新数据时，清空之前的过滤结果，恢复显示全量
  filteredComponentsData.value = null;
  // 3. 重置分页到第一页
  paginationComponents.currentPage = 1;
}

/**
 * 处理零件表加载的数据
 * 当 PartsTable 完成 API 请求后触发
 */
function handlePartsLoad(data: any[]) {
  // 1. 存储全量数据
  allPartsData.value = data;
  // 2. 清空过滤状态
  filteredPartsData.value = null;
  // 3. 重置分页
  paginationParts.currentPage = 1;
}
</script>

<style scoped>
.app-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>
