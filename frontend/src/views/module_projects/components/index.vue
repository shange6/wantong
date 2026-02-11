<!-- 部件列表 -->
<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <div class="search-container">
      <el-form
        ref="queryFormRef"
        :model="queryFormData"
        :inline="true"
        label-suffix=":"
        @submit.prevent="handleQuery"
      >

        <el-form-item prop="code" label="代号">
          <el-input v-model="queryFormData.code" placeholder="输入代号" clearable style="width: 100px"/>
        </el-form-item>
        <el-form-item prop="spec" label="规格">
          <el-input v-model="queryFormData.spec" placeholder="输入规格" clearable style="width: 100px"/>
        </el-form-item>
        <el-form-item prop="material" label="材料/备注">
          <el-input v-model="queryFormData.material" placeholder="输入材料/备注" clearable style="width: 100px"/>
        </el-form-item>
        <!-- 查询、重置、展开/收起按钮 -->
        <el-form-item class="search-buttons">
          <el-button
            v-hasPerm="['module_projects:components:query']"
            type="primary"
            icon="search"
            native-type="submit"
          >
            查询
          </el-button>
          <el-button
            v-hasPerm="['module_projects:components:query']"
            icon="refresh"
            @click="handleResetQuery"
          >
            重置
          </el-button>
          <el-button
            v-hasPerm="['module_system:menu:query']"
            type="info"
            icon="refresh"
            @click="handleOpenProjectDrawer"
          >
            项目
          </el-button>
          <!-- 展开/收起 -->          
        </el-form-item>
      </el-form>
    </div>
    <!-- 内容区域 (封装为组件) -->
    <ComponentsTable ref="tableRef" :query-params="queryFormData" />
    <ProjectTable ref="projectTableRef" v-model:drawerVisible="projectDrawerVisible" @row-click="handleProjectRowClick"/>
  </div>
</template>

<script setup lang="ts">

import { ref, reactive, onMounted } from 'vue';
import { ComponentsQuery } from '@/api/module_projects/components';
import ComponentsTable from '../ComponentsTable.vue';
import ProjectTable from '../ProjectTable.vue';

const projectDrawerVisible = ref(false);

// 新增：抽离点击事件，加日志
const handleOpenProjectDrawer = () => {
  console.log("点击了项目按钮，修改前：", projectDrawerVisible.value); // 日志1
  projectDrawerVisible.value = !projectDrawerVisible.value;
  console.log("点击了项目按钮，修改后：", projectDrawerVisible.value); // 日志2
};
 
// 组件名称
defineOptions({
  name: "Components1",
});

// 查询表单
const queryFormRef = ref();
const queryFormData = reactive<ComponentsQuery>({
  project_code: undefined,
  // wtcode: undefined,
  code: undefined,
  spec: undefined,
  material: undefined,
  remark: undefined,
});

// 表格组件引用
const tableRef = ref();

// 查询
function handleQuery() {
  tableRef.value?.handleQuery();
}

// 项目表格行点击
function handleProjectRowClick(code: string) {
  queryFormData.project_code = code;
  handleQuery();
}

// 重置查询
function handleResetQuery() {
  queryFormRef.value?.resetFields();

  handleQuery();
}

</script>

<style scoped>

</style>
