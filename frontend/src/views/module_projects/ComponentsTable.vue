<template>
  <div class="components-table-container">
    <!-- 内容区域 -->
    <el-card class="data-table">
      <!-- 功能区域 -->
      <div class="table-function">
        <slot name="function-area"></slot>
      </div>

      <!-- 表格区域 -->
      <el-table
        ref="dataTableRef"
        v-loading="loading"
        row-key="wtcode"
        :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
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
        <el-table-column type="selection" fixed min-width="30" align="center" />
        <el-table-column label="万通码" prop="wtcode" min-width="70" show-overflow-tooltip>
          <template #default="{ row }">
            {{ row.wtcode?.includes('.') ? row.wtcode.slice(row.wtcode.indexOf('.') + 1) : row.wtcode }}
          </template>
        </el-table-column>
        <el-table-column label="代号" prop="code" min-width="130" show-overflow-tooltip></el-table-column>
        <el-table-column label="名称" prop="name" min-width="130" show-overflow-tooltip></el-table-column>
        <el-table-column label="数量" prop="count" align="center" min-width="40"></el-table-column>
        <el-table-column label="材料" prop="material" min-width="130" show-overflow-tooltip></el-table-column>
        <el-table-column label="单重" prop="unit_mass" align="center" min-width="60"></el-table-column>
        <el-table-column label="总重" prop="total_mass" align="center" min-width="70"></el-table-column>
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
        <el-form-item label="数量" prop="count">
          <el-input-number v-model="formData.count" :min="1" placeholder="请输入数量" style="width: 100%" />
        </el-form-item>
        <el-form-item label="材料" prop="material">
          <el-input v-model="formData.material" placeholder="请输入材料" />
        </el-form-item>
        <el-form-item label="单重" prop="unit_mass">
          <el-input-number v-model="formData.unit_mass" :min="0" :precision="2" placeholder="请输入单重" style="width: 100%" />
        </el-form-item>
        <el-form-item label="总重" prop="total_mass">
          <el-input-number v-model="formData.total_mass" :min="0" :precision="2" placeholder="请输入总重" style="width: 100%" />
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="formData.remark" placeholder="请输入备注" />
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

const props = defineProps<{
  queryParams: ComponentsQuery;
}>();

// 表格数据
const loading = ref(false);
const pageTableData = ref<ComponentsData[]>([]);
const total = ref(0);
const selectedId = ref<number | undefined>(undefined);
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

// 表单数据
const formRef = ref();
const formData = reactive<ComponentsForm>({
  project_code: "",
  wtcode: "",
  code: "",
  name: "",
  parent_code: "",
  count: 1,
  material: "",
  unit_mass: 0,
  total_mass: 0,
  remark: "",
});

// 表单校验规则
const rules = {
  project_code: [{ required: true, message: "请输入项目编号", trigger: "blur" }],
  wtcode: [{ required: true, message: "请输入万通编码", trigger: "blur" }],
  code: [{ required: true, message: "请输入组件编码", trigger: "blur" }],
  name: [{ required: true, message: "请输入组件名称", trigger: "blur" }],
  count: [{ required: true, message: "请输入组件数量", trigger: "blur" }],
  material: [{ required: true, message: "请输入材料", trigger: "blur" }],
  unit_mass: [{ required: true, message: "请输入单重", trigger: "blur" }],
  total_mass: [{ required: true, message: "请输入总重", trigger: "blur" }],
  remark: [{ required: true, message: "请输入备注", trigger: "blur" }],
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
    material: "",
    unit_mass: 0,
    total_mass: 0,
    remark: "",
  });
}

onMounted(() => {
  handleQuery();
});

// 查询
async function handleQuery() {
  loading.value = true;
  try {
    const params = {
      ...props.queryParams,
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

// 表格选择
function handleSelectionChange(selection: ComponentsData[]) {
  selectIds.value = selection.map((item) => item.id);
}

function handleRowClick(row: ComponentsData) {
  selectedId.value = row.id;
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
    material: row.material,
    unit_mass: row.unit_mass,
    total_mass: row.total_mass,
    remark: row.remark,
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

defineExpose({
  handleQuery,
  handleAdd,
  handleBatchDelete
});

</script>

<style scoped>

/* 1. 让最外层容器占据整个屏幕高度 (减去顶部导航等偏移量) */
.components-table-container {
  height: calc(100vh - 0px); /* 120px 是假设的顶部导航栏+页签的高度，根据实际情况调整 */
  display: flex;
  flex-direction: column;
  /* margin-top: 0px; */

  /* 2. 让 el-card 撑满父容器，并内部也使用 Flex 布局 */
  .data-table {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden; /* 防止出现双滚动条 */
  }

  /* 3. 重点：让 card 的 body 部分撑满 */
  :deep(.el-card__body) {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 10px; /* 保持内边距 */
    overflow: hidden;
  }

  /* 4. 让表格占据剩余的所有空间 */
  .data-table__content {
    flex: 1;
  }

  .pagination-container {
    margin-top: 10px;
    /* display: flex; */
    justify-content: flex-end;
  }

}

</style>
