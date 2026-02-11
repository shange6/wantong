<!-- 项目列表 -->
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
        <el-form-item prop="code" label="编号">
          <el-input v-model="queryFormData.code" placeholder="请输入编号" clearable style="width: 100px"/>
        </el-form-item>
        <el-form-item prop="name" label="名称">
          <el-input v-model="queryFormData.name" placeholder="请输入名称" clearable style="width: 100px"/>
        </el-form-item>
        <el-form-item prop="no" label="合同号">
          <el-input v-model="queryFormData.no" placeholder="输入合同号" clearable style="width: 100px"/>
        </el-form-item>
        <!-- 查询、重置、展开/收起按钮 -->
        <el-form-item class="search-buttons">
          <el-button
            v-hasPerm="['module_projects:project:query']"
            type="primary"
            icon="search"
            native-type="submit"
          >
            查询
          </el-button>
          <el-button
            v-hasPerm="['module_projects:project:query']"
            icon="refresh"
            @click="handleResetQuery"
          >
            重置
          </el-button>
          <!-- 展开/收起 -->          
        </el-form-item>
        <!-- 上传结果提示 -->
      </el-form>
    </div>

    <!-- 内容区域 -->
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
        <el-table-column type="selection" fixed min-width="20" align="center" />
        <el-table-column label="编号" prop="code" min-width="80" align="center" show-overflow-tooltip></el-table-column>
        <el-table-column label="名称"prop="name" min-width="200" show-overflow-tooltip></el-table-column>
        <el-table-column label="合同号" prop="no" min-width="80" align="center"></el-table-column>
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
  </div>
</template>

<script setup lang="ts">

import { ref, reactive, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import ProjectAPI, { ProjectData, ProjectForm, ProjectQuery } from '@/api/module_projects/project';

defineOptions({
  name: "Project",
});

// 查询表单
const queryFormRef = ref();
const queryFormData = reactive<ProjectQuery>({
  code: undefined,
  name: undefined,
  no: undefined,
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

// 弹窗控制
const dialog = reactive({
  visible: false,
  title: "",
});
const formRef = ref();
const formData = reactive<ProjectForm>({
  id: undefined,
  code: "",
  name: "",
  no: "",
});

// 初始化
onMounted(() => {
  handleQuery();
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

// 重置查询
function handleResetQuery() {
  queryFormRef.value?.resetFields();
  pagination.page_no = 1;
  handleQuery();
}

// 表格选择
function handleSelectionChange(selection: ProjectData[]) {
  selectIds.value = selection.map((item) => item.id);
}

// 新增
function handleAdd() {
  resetForm();
  dialog.title = "新增项目";
  dialog.visible = true;
}

// 编辑
function handleEdit(row: ProjectData) {
  resetForm();
  dialog.title = "编辑项目";
  dialog.visible = true;
  Object.assign(formData, {
    id: row.id,
    code: row.code,
    name: row.name,
    no: row.no,
  });
}

// 删除
async function handleDelete(row: ProjectData) {
  try {
    await ElMessageBox.confirm(`确认删除项目 "${row.name}" 吗？`, "提示", {
      type: "warning",
      confirmButtonText: "确定",
      cancelButtonText: "取消",
    });
    await ProjectAPI.delete([row.id]);
    ElMessage.success("删除成功");
    handleQuery();
  } catch (error) {
    // Cancelled or failed
  }
}

// 批量删除
async function handleBatchDelete() {
  if (selectIds.value.length === 0) return;
  try {
    await ElMessageBox.confirm(`确认删除选中的 ${selectIds.value.length} 个项目吗？`, "提示", {
      type: "warning",
      confirmButtonText: "确定",
      cancelButtonText: "取消",
    });
    await ProjectAPI.delete(selectIds.value);
    ElMessage.success("删除成功");
    selectIds.value = [];
    handleQuery();
  } catch (error) {
    // Cancelled or failed
  }
}

// 提交表单
async function submitForm() {
  if (!formRef.value) return;
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        if (formData.id) {
          await ProjectAPI.update(formData.id, formData);
          ElMessage.success("更新成功");
        } else {
          await ProjectAPI.create(formData);
          ElMessage.success("创建成功");
        }
        dialog.visible = false;
        handleQuery();
      } catch (error) {
        // Handled by request interceptor usually
      }
    }
  });
}

// 重置表单
function resetForm() {
  formData.id = undefined;
  formData.code = "";
  formData.name = "";
  formData.no = "";
  formRef.value?.resetFields();
}
</script>

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