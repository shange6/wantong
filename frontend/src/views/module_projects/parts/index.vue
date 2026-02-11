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
            v-hasPerm="['module_projects:parts:query']"
            type="primary"
            icon="search"
            native-type="submit"
          >
            查询
          </el-button>
          <el-button
            v-hasPerm="['module_projects:parts:query']"
            icon="refresh"
            @click="handleResetQuery"
          >
            重置
          </el-button>
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
            icon="refresh"
            @click="isShow = !isShow"
          >
            切换
          </el-button>
          <!-- 展开/收起 -->          
        </el-form-item>
      </el-form>
    </div>
    <!-- 内容区域 (封装为组件) -->
    <ComponentsTable ref="componentsTableRef" v-show="isShow" :query-params="queryComponentsFormData" @row-click="handleComponentRowClick" />
    <PartsTable ref="partsTableRef" v-show="!isShow" :query-params="queryPartsFormData" />  
    <ProjectTable ref="projectTableRef" v-model:drawerVisible="projectDrawerVisible" @row-click="handleProjectRowClick"/>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, nextTick } from 'vue';
import { ComponentsQuery, ComponentsData } from '@/api/module_projects/components';
import { PartsQuery } from '@/api/module_projects/parts';
// 引入业务组件
import ComponentsTable from '../ComponentsTable.vue'; // 组件表格（树形）
import PartsTable from '../PartsTable.vue';           // 零件表格
import ProjectTable from '../ProjectTable.vue';       // 项目选择侧边栏/弹窗

defineOptions({
  name: "Parts", // 命名组件，利于 Keep-alive 缓存
});

/** ----------------------------------------------------------------
 * 1. 响应式变量声明 (Refs & States)
 * ---------------------------------------------------------------- */

// UI 控制状态
const isShow = ref(true);               // 切换显示：true 展示组件表，false 展示零件表
const projectDrawerVisible = ref(false); // 控制项目选择侧边栏的显示/隐藏

// 组件实例引用 (用于调用子组件暴露的方法)
const componentsTableRef = ref();       // 对应 ComponentsTable 实例
const partsTableRef = ref();            // 对应 PartsTable 实例
const projectTableRef = ref();          // 对应 ProjectTable 实例

// 搜索表单引用
const queryFormRef = ref();             // 顶层搜索表单的引用

/** ----------------------------------------------------------------
 * 2. 查询参数管理 (Query Data)
 * ---------------------------------------------------------------- */

// 统一的表单数据源 (双向绑定到 el-input)
const queryFormData = reactive({
  code: undefined,
  spec: undefined,
  material: undefined,
  wtcode: undefined,
});

// 计算属性或同步逻辑：将顶层表单数据同步到两个子表的查询对象中
// 组件表查询参数
const queryComponentsFormData = reactive<ComponentsQuery>({
  project_code: undefined,
  code: undefined,
  spec: undefined,
  material: undefined,
});

// 零件表查询参数
const queryPartsFormData = reactive<PartsQuery>({
  project_code: undefined,
  code: undefined,
  spec: undefined,
  material: undefined,
});

/** ----------------------------------------------------------------
 * 3. 核心业务逻辑 (Business Logic)
 * ---------------------------------------------------------------- */

/**
 * 执行查询操作
 * 触发当前可见表格组件的内部查询方法
 */
function handleQuery() {
  // 同步主表单数据到子表参数对象
  Object.assign(queryComponentsFormData, queryFormData);
  Object.assign(queryPartsFormData, queryFormData);

  // nextTick 确保在切换 DOM 后能拿到正确的实例
  nextTick(() => {
    if (isShow.value) {
      componentsTableRef.value?.handleQuery();
    } else {
      partsTableRef.value?.handleQuery();
    }
  });
}

/**
 * 重置查询条件
 * 清空表单并重新触发查询
 */
function handleResetQuery() {
  if (!queryFormRef.value) return;
  queryFormRef.value.resetFields(); // 重置表单校验与数据
  
  // 清空 reactive 对象中的自定义字段
  queryFormData.code = undefined;
  queryFormData.spec = undefined;
  queryFormData.material = undefined;

  handleQuery();
}

/** ----------------------------------------------------------------
 * 4. 交互事件处理 (Event Handlers)
 * ---------------------------------------------------------------- */

/**
 * 打开/关闭项目选择器
 */
const handleOpenProjectDrawer = () => {
  projectDrawerVisible.value = !projectDrawerVisible.value;
};

/**
 * 处理项目行点击事件
 * @param code 从 ProjectTable 传回的项目编号
 */
function handleProjectRowClick(code: string) {
  // 设置全局项目过滤条件
  queryComponentsFormData.project_code = code;
  queryPartsFormData.project_code = code;
  
  // 提示：通常选择项目后会自动关闭抽屉
  projectDrawerVisible.value = false;
  
  // 执行查询
  handleQuery();
}

/**
 * 处理组件表格行点击 (跳转逻辑)
 * @param row 选中的组件行数据
 */
function handleComponentRowClick(row: ComponentsData) {
  console.log("下钻到零件：", row.wtcode);
  
  // 1. 设置零件表的查询过滤条件（关联组件的万通码）
  // 恢复使用 component_wtcode，并加上日志观察
  console.log("Setting component_wtcode:", row.wtcode);
  queryPartsFormData.component_wtcode = row.wtcode; 
  queryPartsFormData.wtcode = undefined; 
  
  // 2. 切换显示模式到零件表
  isShow.value = false;
  
  // 3. 异步触发零件表查询
  nextTick(() => {
    partsTableRef.value?.handleQuery();
  });
}

</script>
