<!-- 日志管理 -->
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
          <el-input
            v-model="queryFormData.code"
            placeholder="请输入编号"
            clearable
            class="search-input"
          />
        </el-form-item>
        <el-form-item prop="spec" label="名称">
          <el-input
            v-model="queryFormData.spec"
            placeholder="请输入名称"
            clearable
            class="search-input"
          />
        </el-form-item>
        <el-form-item prop="material" label="材料">
          <el-input
            v-model="queryFormData.material"
            placeholder="请输入材料"
            clearable
            class="search-input"
          />
        </el-form-item>
        <el-form-item prop="remark" label="备注">
          <el-input
            v-model="queryFormData.remark"
            placeholder="请输入备注"
            clearable
            class="search-input"
          />
        </el-form-item>
        <!-- 查询、重置、展开/收起按钮 -->
        <el-form-item class="search-buttons">
          <el-button
            v-hasPerm="['module_system:log:query']"
            type="primary"
            icon="search"
            native-type="submit"
          >
            查询
          </el-button>
          <el-button
            v-hasPerm="['module_system:log:query']"
            icon="refresh"
            @click="handleResetQuery"
          >
            重置
          </el-button>
        </el-form-item>
        <!-- 上传结果提示 -->
        <div v-if="uploadResult.projectName" class="info-group">
          <span class="info-item">项目名称：{{ uploadResult.projectName }}</span>
          <span class="info-item">合同号：{{ uploadResult.contractNo }}</span>
          <span class="info-item">部件名称：{{ uploadResult.partName }}</span>
          <span class="info-item">部件编号：{{ uploadResult.partCode }}</span>
          <span class="info-item">数量：{{ uploadResult.partCount }}</span>
          <span class="info-item">文件数：{{ uploadResult.pageCount }}</span>
        </div>
      </el-form>
    </div>

    <!-- 内容区域 -->
    <el-card v-if="pageTableData && pageTableData.length > 0" class="data-table">
      <!-- 表格区域：系统配置列表 -->
      <el-table
        ref="dataTableRef"
        v-loading="loading"
        :data="pageTableData"
        highlight-current-row
        class="data-table__content"
        border
        stripe
        :header-cell-style="{ textAlign: 'center' }"
        @selection-change="handleSelectionChange"
      >
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column
          label="万通码"
          prop="wtcode"
          min-width="150"
          show-overflow-tooltip
        ></el-table-column>
        <el-table-column
          label="编号"
          prop="code"
          min-width="150"
          show-overflow-tooltip
        ></el-table-column>
        <el-table-column
          label="名称"
          prop="spec"
          min-width="150"
          show-overflow-tooltip
        ></el-table-column>
        <el-table-column label="数量" prop="count" align="center" min-width="45"></el-table-column>
        <el-table-column
          label="材料"
          prop="material"
          align="center"
          min-width="100"
          show-overflow-tooltip
        ></el-table-column>
        <el-table-column
          label="单重"
          prop="unit_mass"
          align="center"
          min-width="60"
        ></el-table-column>
        <el-table-column
          label="总重"
          prop="total_mass"
          align="center"
          min-width="70"
        ></el-table-column>
        <el-table-column
          label="备注"
          prop="remark"
          min-width="120"
          show-overflow-tooltip
        ></el-table-column>
        <el-table-column label="操作" min-width="80">
          <template #default="scope">
            <el-button
              v-hasPerm="['module_system:log:delete']"
              type="danger"
              size="small"
              link
              icon="delete"
              @click="handleDelete(scope.row.id)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页区域 -->
      <template #footer>
        <pagination
          v-model:total="total"
          v-model:page="queryFormData.page_no"
          v-model:limit="queryFormData.page_size"
          @pagination="loadingData"
        />
      </template>
    </el-card>

    <!-- 空数据时显示上传组件 -->
    <el-card v-else class="upload-container">
      <div class="upload-wrapper">
        <el-upload
          ref="uploadRef"
          class="upload-demo"
          drag
          action="#"
          accept=".dwg"
          :file-list="uploadFileList"
          :auto-upload="true"
          :limit="1"
          :on-exceed="handleExceed"
          :http-request="handleHttpRequest"
          :show-file-list="false"
        >
          <el-icon class="el-icon--upload" style="color: var(--el-color-primary)">
            <UploadFilled />
          </el-icon>
          <div class="el-upload__text">
            拖拽文件到此处或
            <em>点击上传</em>
          </div>
        </el-upload>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "Data",
  inheritAttrs: false,
});

// import LogAPI, { LogTable, LogPageQuery } from "@/api/module_orders/data";
import { DataAPI } from "@/api/module_orders/data";
import { UploadFilled } from "@element-plus/icons-vue";
import UserTableSelect from "@/views/module_system/user/components/UserTableSelect.vue";
import ExportModal from "@/components/CURD/ExportModal.vue";
import JsonPretty from "@/components/JsonPretty/index.vue";
// import type { IContentConfig } from "@/components/CURD/types";
import { formatToDateTime } from "@/utils/dateUtil";
import { log } from "console";

const queryFormRef = ref();
const dataFormRef = ref();
const total = ref(0);
const selectIds = ref<number[]>([]);
const loading = ref(false);
const isExpand = ref(false);
const isExpandable = ref(true);
const uploadDialogVisible = ref(false);
const uploadRef = ref();
const uploadFileList = ref<any[]>([]);
const uploading = ref(false);
const currentPath = ref("/");

// 分页表单
const pageTableData = ref<any[]>([]);

// 导出弹窗状态和选中行数据
// const exportsDialogVisible = ref(false);
// const selectionRows = ref<LogTable[]>([]);

// 详情表单
// const formData = ref<LogTable>({});

// 分页查询参数
const queryFormData = reactive<DataPageQuery>({
  page_no: 1,
  page_size: 10,
  code: undefined,
  spec: undefined,
  material: undefined,
  remark: undefined,
});

// 上传结果状态
const uploadResult = reactive({
  message: "",
  type: "success" as "success" | "error",
  projectName: "",
  contractNo: "",
  partName: "",
  partCode: "",
  partCount: "",
  pageCount: "",
});

// 弹窗状态
const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
});

// 列表刷新
// async function handleRefresh() {
//   await loadingData();
// }

const getStatusCodeType = (code?: number) => {
  if (code === undefined) {
    return "info";
  }
  if (code >= 200 && code < 300) {
    return "success";
  } else if (code >= 300 && code < 400) {
    return "warning";
  } else if (code >= 400 && code < 500) {
    return "danger";
  } else {
    return "danger";
  }
};

const getMethodType = (method?: string) => {
  if (method === undefined) {
    return "info";
  }
  if (method === "GET") {
    return "info";
  } else if (method === "POST") {
    return "success";
  } else if (method === "PUT" || method === "PATCH") {
    return "warning";
  } else if (method === "DELETE") {
    return "danger";
  } else {
    return "info";
  }
};

// 加载表格数据
async function loadingData() {
  // loading.value = true;
  // try {
  //   const response = await LogAPI.listLog(queryFormData);
  //   pageTableData.value = response.data.data.items;
  //   total.value = response.data.data.total;
  // } catch (error: any) {
  //   console.error(error);
  // } finally {
  //   loading.value = false;
  // }
}

// 查询（重置页码后获取数据）
async function handleQuery() {
  queryFormData.page_no = 1;
  // loadingData();
}

// 选择创建人后触发查询
function handleConfirm() {
  // handleQuery();
}

// 重置查询
async function handleResetQuery() {
  queryFormRef.value.resetFields();
  queryFormData.page_no = 1;
  // loadingData();
}

// 重置表单
async function resetForm() {
  if (dataFormRef.value) {
    dataFormRef.value.resetFields();
    dataFormRef.value.clearValidate();
  }
  // formData.value.id = undefined;
}

// 行复选框选中项变化
async function handleSelectionChange(selection: any) {
  selectIds.value = selection.map((item: any) => item.id);
  // selectionRows.value = selection;
}

// 关闭弹窗
async function handleCloseDialog() {
  dialogVisible.visible = false;
  resetForm();
}

// --- 3. 删除操作（仅前端移除） ---
async function handleDelete(index: number) {
  ElMessageBox.confirm("确认删除该项数据?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  }).then(() => {
    pageTableData.value.splice(index, 1);
    total.value = pageTableData.value.length;
    ElMessage.success("已从临时列表中移除");
  });
}

// 删除、批量删除
// async function handleDelete(ids: number[]) {
//   ElMessageBox.confirm("确认删除该项数据?", "警告", {
//     confirmButtonText: "确定",
//     cancelButtonText: "取消",
//     type: "warning",
//   })
//    .then(() => {
//       // 循环处理要删除的 ID（支持单选和批量删除）
//       ids.forEach(id => {
//         // 1. 找到该 ID 在数组中的索引位置
//         const index = pageTableData.value.findIndex(item => item.id === id);

//         // 2. 如果找到了，就从数组中真实删除这一行数据
//         if (index !== -1) {
//           pageTableData.value.splice(index, 1);
//         }
//       });

//       // 3. 同步更新前端显示的总条数
//       total.value = total.value - ids.length;

//       // 4. 清空选中状态
//       selectIds.value = [];

//       ElMessage.success("前端数据已移除");
//     })
//     .catch(() => {
//       // 用户取消
//     });
// }

// onMounted(() => {
//   loadingData();
// });

// 1. 处理超出限制：当选了新文件时，替换掉旧文件
function handleExceed(files: any) {
  uploadRef.value!.clearFiles(); // 清除老文件
  const file = files[0];
  // 建议导入 genFileId，如果没有导入，可以用 Date.now() 保证唯一
  file.uid = "upload_0129_";
  uploadRef.value!.handleStart(file); // 放入队列
  // 关键：手动触发 http-request 逻辑
  uploadRef.value!.submit();
}

// 3. 真正的执行上传函数
async function handleHttpRequest(options: any) {
  try {
    uploading.value = true;
    // 1. 准备后端需要的 FormData
    const formData = new FormData();
    // 注意：'file' 必须和后端 FastAPI 定义的参数名一致
    formData.append("file", options.file);
    // 2. 路径处理（如果有的话）
    const targetPath = currentPath.value === "/" ? "" : currentPath.value;
    formData.append("target_path", targetPath);
    // 3. 调用你项目封装好的 API (这里会经过 axios 拦截器，自动带上 Token)
    const res = await DataAPI.uploadFile(formData);
    // 4. 直接取值（无任何判断，直接拿后端返回的表格数组）
    const tableSourceData = res.data.data.data;
    // tableSourceData.forEach((item, index) => {
    //   console.log(item["code"]); // index从0开始，+1为自然行号
    // });

    // 4. 数据处理：给每一行加唯一id（删除用）+ 部分字段转数字（优化显示）
    const formatTableData = tableSourceData.map((item) => ({
      ...item,
      id: Date.now() + Math.floor(Math.random() * 1000), // 生成唯一id
      count: item.count ? Number(item.count) : 0, // 字符串转数字
      unit_mass: item.unit_mass ? Number(item.unit_mass) : 0,
      total_mass: item.total_mass ? Number(item.total_mass) : 0,
    }));

    // 5. 将后端返回的提示信息绑定到 el-alert
    // const msg = res.data.data.项目名称 + res.data.data.合同号 + res.data.data.部件名称 + res.data.data.部件编号 + res.data.data.数量
    const { 项目名称, 合同号, 部件名称, 部件编号, 数量, 文件个数 } = res.data?.data ?? {};
    // const msg = `项目名称：${项目名称 ?? ''}     合同号：${合同号 ?? ''}    部件名称：${部件名称 ?? ''}    部件编号：${部件编号 ?? ''}    数量：${数量 ?? ''}`
    // uploadResult.message = msg;
    uploadResult.projectName = 项目名称 ?? "";
    uploadResult.contractNo = 合同号 ?? "";
    uploadResult.partName = 部件名称 ?? "";
    uploadResult.partCode = 部件编号 ?? "";
    uploadResult.partCount = 数量 ?? "";
    uploadResult.pageCount = String(文件个数) ?? "";

    // 6. 直接将后端数据添加到表格（前置追加，保持原有顺序）
    pageTableData.value = [...formatTableData, ...pageTableData.value];
    // 7. 更新表格总条数
    total.value = pageTableData.value.length;
  } catch (error) {
    console.error("上传失败:", error);
  } finally {
    uploadRef.value?.clearFiles();
    uploading.value = false;
  }
}
</script>

<style lang="scss" scoped>
.search-input {
  width: 120px !important;
}

.app-container {
  /* 确保父容器铺满全屏，并使用 Flex 布局 */
  height: calc(100vh - 84px); /* 84px 通常是顶部导航栏的高度，根据实际情况调整 */
  display: flex;
  flex-direction: column;
}

.data-table {
  /* 1. 确保 Card 容器本身是伸展的 */
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 防止出现双滚动条 */
  height: 100%;

  /* 2. 穿透修改 el-card__body，将其设为 Flex 布局 */
  :deep(.el-card__body) {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    padding: 0;
  }

  /* 3. 让表格占据 body 的 100% */
  .data-table__content {
    flex: 1 !important; /* 强制占据所有剩余空间 */
    height: 100% !important;
  }
}

.upload-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;

  :deep(.el-card__body) {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: flex-start;
  }
}

.upload-wrapper {
  width: 100%;
  max-width: 500px;
  text-align: center;
  margin-top: 20px;
}

.upload-actions {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

/* 调整上传虚框的样式 */
:deep(.el-upload-dragger) {
  /* 1. 调整线宽 (border-width) */
  border-width: 2px;
  /* 2. 调整线型 (dashed 是虚线，solid 是实线) */
  border-style: dashed;
  /* 3. 调整颜色 (可以改成你喜欢的颜色) */
  border-color: var(--el-color-primary);
  /* 4. 可选：调整悬停时的背景颜色 */
  &:hover {
    // border-color: var(--el-color-primary-light-8);
    background-color: var(--el-color-primary-light-8);
  }
}

.upload-alert {
  margin-top: 0px;
  :deep(.el-alert__title) {
    color: var(--el-text-color-primary) !important;
  }
  :deep(.el-alert__description) {
    color: var(--el-text-color-primary) !important;
  }
}

.info-group {
  // margin-top: 0px;
  // display: flex;
  // gap: 20px;
  // font-size: 14px;
  // color: var(--el-text-color-regular);
  // padding-left: 0px; /* Slight indent to align with alert text if needed, or just left align */
}
</style>
