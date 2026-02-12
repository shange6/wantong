<template>
  <div class="app-container">
    <SearchForm 
      v-model:modelValue="queryFormData" 
      :source-data="isShow ? allComponentsData : allPartsData"
      :show-no="false"
      @update="handleFilterUpdate"
      @reset="handleResetQuery"
    >
      <template #extra>
        <el-button
          v-hasPerm="['module_projects:parts:query']"
          type="info"
          icon="arrow-right"
          @click="handleOpenProjectDrawer"
        >
          项目
        </el-button>
        <el-button
          v-hasPerm="['module_projects:parts:query']"
          type="warning"
          icon="refresh"
          @click="toggleTable"
        >
          {{ isShow ? '切换零件' : '切换组件' }}
        </el-button>
      </template>
    </SearchForm>

    <ComponentsTable 
      v-show="isShow"
      ref="componentsTableRef" 
      :query-params="queryComponentsFormData" 
      @load-data="handleComponentsLoad"
      @row-click="handleComponentRowClick" 
    />

    <PartsTable 
      v-show="!isShow"
      ref="partsTableRef" 
      :query-params="queryPartsFormData"
      @load-data="handlePartsLoad" 
    />  

    <ProjectTable 
      ref="projectTableRef" 
      v-model:drawerVisible="projectDrawerVisible" 
      @row-click="handleProjectRowClick"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, nextTick } from 'vue';
import SearchForm from '../SearchForm.vue';
import { ComponentsQuery, ComponentsData } from '@/api/module_projects/components';
import { PartsQuery } from '@/api/module_projects/parts';
import ComponentsTable from '../ComponentsTable.vue';
import PartsTable from '../PartsTable.vue';
import ProjectTable from '../ProjectTable.vue';

defineOptions({
  name: "Parts",
});

/** ----------------------------------------------------------------
 * 1. 响应式变量与状态
 * ---------------------------------------------------------------- */
const isShow = ref(true);               // true: 组件表, false: 零件表
const projectDrawerVisible = ref(false);
const componentsTableRef = ref();
const partsTableRef = ref();

// 原始全量数据底稿 (SearchForm 需要用到)
const allComponentsData = ref<any[]>([]);
const allPartsData = ref<any[]>([]);

// 统一搜索表单数据
const queryFormData = reactive({
  code: undefined,
  spec: undefined,
  material: undefined,
});

const queryComponentsFormData = reactive<ComponentsQuery>({
  project_code: undefined,
});

const queryPartsFormData = reactive<PartsQuery>({
  project_code: undefined,
  component_wtcode: undefined,
});

/** ----------------------------------------------------------------
 * 2. 数据加载回调 (从子组件获取全量数据)
 * ---------------------------------------------------------------- */
function handleComponentsLoad(data: any[]) {
  allComponentsData.value = data;
}

function handlePartsLoad(data: any[]) {
  allPartsData.value = data;
}

/** ----------------------------------------------------------------
 * 3. 核心业务逻辑 (前端过滤与查询)
 * ---------------------------------------------------------------- */

// 响应 SearchForm 的前端过滤结果
function handleFilterUpdate(filtered: any[]) {
  if (isShow.value && componentsTableRef.value) {
    // 过滤组件表：SearchForm 已经处理好了树形结构
    componentsTableRef.value.pageTableData = filtered; 
  } else if (!isShow.value && partsTableRef.value) {
    // 过滤零件表：需要注意 PartsTable 内部使用了 listToTree
    // SearchForm 返回的是过滤后的扁平数组，需要重新转树
    partsTableRef.value.pageTableData = partsTableRef.value.listToTree(filtered);
  }
}

// 切换表格展示
function toggleTable() {
  isShow.value = !isShow.value;
  // 切换后执行一次重置式查询，确保新表有数据
  handleResetQuery();
}

// 初始加载
onMounted(async () => {
  await nextTick();
  // 默认加载组件表数据
  componentsTableRef.value?.handleQuery();
});

/** ----------------------------------------------------------------
 * 4. 交互处理
 * ---------------------------------------------------------------- */

const handleOpenProjectDrawer = () => {
  projectDrawerVisible.value = !projectDrawerVisible.value;
};

// 项目点击：触发后端真实请求
function handleProjectRowClick(code: string) {
  queryComponentsFormData.project_code = code;
  queryPartsFormData.project_code = code;
  projectDrawerVisible.value = false;
  
  // 重新从后端拉取新项目的全量数据
  if (isShow.value) {
    componentsTableRef.value?.handleQuery();
  } else {
    partsTableRef.value?.handleQuery();
  }
}

// 重置查询
function handleResetQuery() {
  // 恢复显示对应的全量底稿
  if (isShow.value && componentsTableRef.value) {
    componentsTableRef.value.pageTableData = allComponentsData.value;
  } else if (!isShow.value && partsTableRef.value) {
    partsTableRef.value.pageTableData = allPartsData.value;
  }
}

// 下钻逻辑：从组件表点击进入零件表
function handleComponentRowClick(row: ComponentsData) {
  queryPartsFormData.component_wtcode = row.wtcode; 
  isShow.value = false;
  
  // 下钻涉及到数据范围变化，通常需要重新请求后端该组件下的零件
  nextTick(() => {
    partsTableRef.value?.handleQuery();
  });
}
</script>

<style scoped>
.app-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  height: 100%;
}
</style>