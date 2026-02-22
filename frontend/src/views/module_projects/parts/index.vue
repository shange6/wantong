<template>
  <div class="app-container">
    <SearchForm
      v-model="queryFormData"
      :source-data="allComponentsData"
      :show-no="false"
      @update="handleComponentsFilter"
      @reset="handleResetQuery"
    >      
      <template #extra>
        <el-button
          v-hasPerm="['module_system:menu:query']"
          type="info"
          @click="handleOpenProjectDrawer"
        >
          📂 项目
        </el-button>
        <el-button
          v-hasPerm="['module_projects:parts:query']"
          type="warning"
          @click="toggleTable"
        >
          {{ partsTableVisible ? "切换组件" : "切换零件" }}
        </el-button>
      </template>
    </SearchForm>

    <PartsTable
      v-show="partsTableVisible"
      ref="partsTableRef"
      :currentPage="paginationParts.currentPage"
      :pageSize="paginationParts.pageSize"
      @update:currentPage="(val) => paginationParts.currentPage = val"
      @update:pageSize="(val) => paginationParts.pageSize = val"
    />

    <ComponentsTable
      v-show="!partsTableVisible"
      ref="componentsTableRef"
      @row-click="handleComponentRowClick"
      :currentPage="paginationComponents.currentPage"
      :pageSize="paginationComponents.pageSize"
      @update:currentPage="(val) => paginationComponents.currentPage = val"
      @update:pageSize="(val) => paginationComponents.pageSize = val"
    />

    <ProjectsDrawerTable
      :drawerVisible="projectDrawerVisible"
      @update:drawerVisible="(val) => projectDrawerVisible = val"
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
const partsTableVisible = ref(false)
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
  return filteredComponentsData.value !== null ? filteredComponentsData.value : allComponentsData.value;
});

const partsData = computed(() => {
  return filteredPartsData.value !== null ? filteredPartsData.value : allPartsData.value;
});

// 搜索过滤
function handleComponentsFilter(filtered: any[]) {
  filteredComponentsData.value = filtered;
  paginationComponents.currentPage = 1;
}

// 行点击联动逻辑 🔗
function handleComponentRowClick(row: any) {
  selectedComponent.value = row;
  // 核心：调用 PartsTable 暴露的方法请求新数据
  partsTableRef.value?.handleQuery({
    component_wtcode: row.wtcode 
  });
  partsTableVisible.value = true
}

function handleProjectRowClick(row: any) {
  queryFormData.value.project_code = row.code;
  componentsTableRef.value?.handleQuery?.();
  partsTableVisible.value = false
}

const handleResetQuery = () => {
  filteredComponentsData.value = null;
  paginationComponents.currentPage = 1;
};

const handleOpenProjectDrawer = () => {
  projectDrawerVisible.value = !projectDrawerVisible.value;
};

// 切换表格展示
function toggleTable() {
  partsTableVisible.value = !partsTableVisible.value;
  // 切换后执行一次重置式查询，确保新表有数据
  // handleResetQuery();
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