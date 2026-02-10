<template>
  <div class="project-table-container">
    <!-- 弹窗区域 -->
    <el-drawer
      v-model="visible"
      title="请选择项目"
      size="50%"
      append-to-body
      class="project-table-drawer"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :show-close="true"
    >
    <!-- 表格区域 -->
        <el-card class="data-table">
        <!-- 功能区域 -->
        <!-- 表格区域 -->
        <el-table
            ref="dataTableRef"
            v-loading="loading"
            :data="pageTableData"
            :header-cell-style="{ textAlign: 'center' }"
            class="data-table__content"
            border
            stripe
            @selection-change="handleSelectionChange"
        >
            <template #empty>
            <el-empty :image-size="80" description="暂无数据" />
            </template>
            <!-- <el-table-column type="selection" fixed min-width="20" align="center" /> -->
            <el-table-column label="编号" prop="code" min-width="60" align="center" show-overflow-tooltip></el-table-column>
            <el-table-column label="名称"prop="name" min-width="120" show-overflow-tooltip></el-table-column>
            <el-table-column label="合同号" prop="no" min-width="40" align="center"></el-table-column>
        </el-table>
        <!-- 分页区域 -->
        <div class="pagination-container">
            <el-pagination
            v-model:current-page="pagination.page_no"
            v-model:page-size="pagination.page_size"
            :total="total"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleQuery"
            @current-change="handleQuery"
            />
        </div>
        </el-card>

    </el-drawer>
  </div>
</template>

<script setup lang="ts">

import { ref, reactive, computed, onMounted } from 'vue';
import ProjectAPI, { ProjectData, ProjectForm, ProjectQuery } from '@/api/module_projects/project';

const props = defineProps<{ drawerVisible: boolean; }>();
const emit = defineEmits(['update:drawerVisible']);
const visible = computed({
  get: () => props.drawerVisible,
  set: (val) => emit('update:drawerVisible', val),
});

// 表格数据
const loading = ref(false);
const pageTableData = ref<ProjectData[]>([]);
const total = ref(0);
const selectIds = ref<number[]>([]);
const pagination = reactive({
  page_no: 1,
  page_size: 10,
});

// 表格选择
function handleSelectionChange(selection: ProjectData[]) {
  selectIds.value = selection.map((item) => item.id);
}


const queryFormData = reactive<ProjectQuery>({
  code: undefined,
  name: undefined,
  no: undefined,
});
// 查询
async function handleQuery() {
  loading.value = true;
  try {
    const params = {
      ...queryFormData,
      page_no: pagination.page_no,
      page_size: pagination.page_size,
    };
    const res = await ProjectAPI.getList(params);
    pageTableData.value = res.data.data.items;
    total.value = res.data.data.total;
  } finally {
    loading.value = false;
  }
}


// 初始化
onMounted(() => {
  handleQuery();
});

</script>

<style>
/* 非 scoped 样式，用于覆盖 append-to-body 的抽屉样式 */
.project-table-drawer .el-drawer__body {
  display: flex;
  flex-direction: column;
  padding: 10px;
  overflow: hidden;
}
</style>

<style scoped>

/* 让 el-card 撑满父容器 (抽屉body)，并内部也使用 Flex 布局 */
.data-table {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 防止出现双滚动条 */
}

/* 重点：让 card 的 body 部分撑满 */
:deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 10px; /* 保持内边距 */
  overflow: hidden;
}

/* 让表格占据剩余的所有空间 */
.data-table__content {
  flex: 1;
}

.pagination-container {
  margin-top: 10px;
  justify-content: flex-end;
}

</style>