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
        <el-form-item prop="project_code" label="项目">
          <el-select
            v-model="queryFormData.project_code"
            placeholder="请选择项目"
            style="width: 150px"
            clearable
            filterable
          >
            <el-option
              v-for="item in projectList"
              :key="item.id"
              :label="item.name"
              :value="item.code"
            />
          </el-select>
        </el-form-item>
        <el-form-item prop="wtcode" label="万通码">
          <el-input v-model="queryFormData.wtcode" placeholder="输入万通码" clearable style="width: 100px"/>
        </el-form-item>
        <el-form-item prop="code" label="代号">
          <el-input v-model="queryFormData.code" placeholder="输入代号" clearable style="width: 100px"/>
        </el-form-item>
        <el-form-item prop="name" label="名称">
          <el-input v-model="queryFormData.name" placeholder="输入名称" clearable style="width: 100px"/>
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
          <!-- 展开/收起 -->          
        </el-form-item>
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
        @row-click="handleRowClick"
      >
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column type="selection" fixed min-width="40" align="center" />
        <el-table-column label="万通码" prop="wtcode" min-width="100" show-overflow-tooltip></el-table-column>
        <el-table-column label="代号" prop="code" min-width="100" show-overflow-tooltip></el-table-column>
        <el-table-column label="名称" prop="name" min-width="150" show-overflow-tooltip></el-table-column>
        <el-table-column label="数量" prop="count" align="center" min-width="40"></el-table-column>
        <el-table-column label="单重" prop="unit_mass" align="center" min-width="50"></el-table-column>
        <el-table-column label="总重" prop="total_mass" align="center" min-width="60"></el-table-column>
        <el-table-column label="备注" prop="remark" min-width="100" show-overflow-tooltip></el-table-column>
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

    <!-- 新增/编辑弹窗 -->
    <el-dialog
      v-model="dialog.visible"
      :title="dialog.title"
      width="500px"
      append-to-body
      @close="resetForm"
    >
      <el-form ref="formRef" :model="formData" :rules="rules" label-width="100px">
        <el-form-item label="项目编号" prop="project_code">
          <el-input v-model="formData.project_code" placeholder="请输入项目编号" />
        </el-form-item>
        <el-form-item label="万通编码" prop="wtcode">
          <el-input v-model="formData.wtcode" placeholder="请输入万通编码" :disabled="!!formData.id" />
        </el-form-item>
        <el-form-item label="组件编码" prop="code">
          <el-input v-model="formData.code" placeholder="请输入组件编码" />
        </el-form-item>
        <el-form-item label="组件名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入组件名称" />
        </el-form-item>
        <el-form-item label="父级编码" prop="parent_code">
          <el-input v-model="formData.parent_code" placeholder="请输入父级编码" />
        </el-form-item>
        <el-form-item label="组件数量" prop="count">
          <el-input-number v-model="formData.count" :min="1" placeholder="请输入组件数量" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialog.visible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import ComponentsAPI, { ComponentsData, ComponentsForm, ComponentsQuery } from '@/api/module_projects/components';
import ProjectAPI, { ProjectData } from '@/api/module_projects/project';

defineOptions({
  name: "Components",
});

// 查询表单
const queryFormRef = ref();
const queryFormData = reactive<ComponentsQuery>({
  project_code: undefined,
  wtcode: undefined,
  code: undefined,
  name: undefined,
});

// 表格数据
const loading = ref(false);
const pageTableData = ref<ComponentsData[]>([]);
const total = ref(0);
const selectIds = ref<number[]>([]);
const pagination = reactive({
  page_no: 1,
  page_size: 10,
});

// 项目列表
const projectList = ref<ProjectData[]>([]);

// 获取项目列表
async function getProjectList() {
  try {
    const res = await ProjectAPI.getList({ page_no: 1, page_size: 100 });
    projectList.value = res.data.data.items;
  } catch (error) {
    console.error("获取项目列表失败:", error);
  }
}

// 弹窗控制
const dialog = reactive({
  visible: false,
  title: "",
});

// 表单数据
const formRef = ref();
const formData = reactive<ComponentsForm>({
  project_code: "",
  wtcode: "",
  code: "",
  name: "",
  parent_code: "",
  count: 1,
});

// 表单校验规则
const rules = {
  project_code: [{ required: true, message: "请输入项目编号", trigger: "blur" }],
  wtcode: [{ required: true, message: "请输入万通编码", trigger: "blur" }],
  code: [{ required: true, message: "请输入组件编码", trigger: "blur" }],
  name: [{ required: true, message: "请输入组件名称", trigger: "blur" }],
  count: [{ required: true, message: "请输入组件数量", trigger: "blur" }],
};

// 重置表单
function resetForm() {
  formRef.value?.resetFields();
  Object.assign(formData, {
    id: undefined,
    project_code: "",
    wtcode: "",
    code: "",
    name: "",
    parent_code: "",
    count: 1,
  });
}

onMounted(() => {
  getProjectList();
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
    const res = await ComponentsAPI.getList(params);
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
function handleSelectionChange(selection: ComponentsData[]) {
  selectIds.value = selection.map((item) => item.id);
}

// 行点击
function handleRowClick(row: ComponentsData) {
  console.log("Row clicked:", row);
}

// 新增
function handleAdd() {
  resetForm();
  dialog.title = "新增部件";
  dialog.visible = true;
}

// 编辑
function handleEdit(row: ComponentsData) {
  resetForm();
  dialog.title = "编辑部件";
  dialog.visible = true;
  Object.assign(formData, {
    id: row.id,
    project_code: row.project_code,
    wtcode: row.wtcode,
    code: row.code,
    name: row.name,
    parent_code: row.parent_code,
    count: row.count,
  });
}

// 删除
async function handleDelete(row: ComponentsData) {
  try {
    await ElMessageBox.confirm(`确认删除部件 "${row.name}" 吗？`, "提示", {
      type: "warning",
      confirmButtonText: "确定",
      cancelButtonText: "取消",
    });
    await ComponentsAPI.delete([row.id]);
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
    await ElMessageBox.confirm(`确认删除选中的 ${selectIds.value.length} 个部件吗？`, "提示", {
      type: "warning",
      confirmButtonText: "确定",
      cancelButtonText: "取消",
    });
    await ComponentsAPI.delete(selectIds.value);
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
          await ComponentsAPI.update(formData.id, formData);
          ElMessage.success("更新成功");
        } else {
          await ComponentsAPI.create(formData);
          ElMessage.success("创建成功");
        }
        dialog.visible = false;
        handleQuery();
      } catch (error) {
        // Error handled by request interceptor
      }
    }
  });
}
</script>

<style scoped>
.search-container {
  margin-bottom: 20px;
}
.data-table {
  margin-bottom: 20px;
}
.table-function {
  margin-bottom: 10px;
}
.pagination-container {
  margin-top: 15px;
  display: flex;
  justify-content: flex-end;
}
</style>
