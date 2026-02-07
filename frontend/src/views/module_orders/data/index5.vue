<!-- 菜单管理 -->
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
          <el-input v-model="queryFormData.code" placeholder="请输入编号" clearable style="width: 90px"/>
        </el-form-item>
        <el-form-item prop="spec" label="名称">
          <el-input v-model="queryFormData.spec" placeholder="请输入名称" clearable style="width: 90px"/>
        </el-form-item>
        <el-form-item prop="material" label="材料">
          <el-input v-model="queryFormData.material" placeholder="请输入材料" clearable style="width: 90px"/>
        </el-form-item>
        <el-form-item prop="remark" label="备注">
          <el-input v-model="queryFormData.remark" placeholder="请输入备注" clearable style="width: 90px"/>
        </el-form-item>
        <!-- 查询、重置、展开/收起按钮 -->
        <el-form-item class="search-buttons">
          <el-button
            v-hasPerm="['module_system:menu:query']"
            type="primary"
            icon="search"
            native-type="submit"
          >
            查询
          </el-button>
          <el-button
            v-hasPerm="['module_system:menu:query']"
            icon="refresh"
            @click="handleResetQuery"
          >
            重置
          </el-button>
          <el-button
            v-hasPerm="['module_system:menu:create']"
            type="success"
            icon="plus"
            @click="handleOpenDialog('create')"
          >
            保存
          </el-button>
          <el-button
            v-hasPerm="['module_system:menu:delete']"
            type="danger"
            icon="delete"
            :disabled="selectIds.length === 0"
            @click="handleDelete(selectIds)"
          >
            放弃
          </el-button>
          <!-- 展开/收起 -->          
        </el-form-item>
        <!-- 上传结果提示 -->
        <div v-if="uploadResult.projectName">
          <span>项目名称：{{ uploadResult.projectName }}</span>
          <span>合同号：{{ uploadResult.contractNo }}</span>
          <span>部件名称：{{ uploadResult.partName }}</span>
          <span>部件编号：{{ uploadResult.partCode }}</span>
          <span>数量：{{ uploadResult.partCount }}</span>
          <span>文件数：{{ uploadResult.pageCount }}</span>
        </div>
      </el-form>
    </div>

    <!-- 内容区域 -->
    <el-card v-if="pageTableData && pageTableData.length < 0" class="data-table">
      <!-- 功能区域 -->
      <!-- 表格区域 -->
      <el-table
        ref="dataTableRef"
        row-key="id"
        :data="pageTableData"
        :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
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
        <el-table-column type="selection" fixed min-width="55" align="center" />
        <el-table-column label="万通码" prop="wtcode" min-width="150" show-overflow-tooltip></el-table-column>
        <el-table-column label="编号" prop="code" min-width="150" show-overflow-tooltip></el-table-column>
        <el-table-column label="名称"prop="spec" min-width="150" show-overflow-tooltip></el-table-column>
        <el-table-column label="数量" prop="count" align="center" min-width="45"></el-table-column>
        <el-table-column label="材料" prop="material" align="center" min-width="100" show-overflow-tooltip></el-table-column>
        <el-table-column label="单重" prop="unit_mass" align="center" min-width="60"></el-table-column>
        <el-table-column label="总重" prop="total_mass" align="center" min-width="70"></el-table-column>
        <el-table-column label="备注" prop="remark" min-width="120" show-overflow-tooltip></el-table-column>        

      </el-table>
    </el-card>

    <!-- 空数据时显示上传组件 -->
     <el-row :gutter="20"">
      <el-col :span="8">
        <el-card class="upload-card">
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
              style="max-width: 500px;"          
            >
              <el-icon class="el-icon--upload" style="color: var(--el-color-primary)">
                <UploadFilled />
              </el-icon>
              <div class="el-upload__text">
                拖拽文件到此处或 <em>点击上传</em>
              </div>
            </el-upload>
          </div>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card class="report-card">
          <div class="report-header">文件解析结果</div>
          <div class="report-grid">      
            <div class="grid-row">
              <div class="grid-label">项目名称</div>
              <div class="grid-content font-bold">
                <em>{{ uploadResult.projectName || '--' }}</em>
              </div>
            </div>
            <el-row class="grid-row">
              <el-col :span="15" class="col-item">
                <div class="grid-label">部件名称</div>
                <div class="grid-content">{{ uploadResult.partName || '--' }}</div>
              </el-col> 
              <el-col :span="9" class="col-item">
                  <div class="grid-label border-left">合同号</div>
                  <div class="grid-content">{{ uploadResult.contractNo || '--' }}</div>
                </el-col>    
            </el-row>
            <el-row class="grid-row no-border">
              <el-col :span="12" class="col-item">
                <div class="grid-label">部件编号</div>
                <div class="grid-content">{{ uploadResult.partCode || '--' }}</div>
              </el-col>
              <el-col :span="6" class="col-item border-right">
                  <div class="grid-label border-left">数量</div>
                  <div class="grid-content">{{ uploadResult.partCount || '--' }}</div>
                </el-col>
              <el-col :span="6" class="col-item">
                <div class="grid-label border-left">文件个数</div>
                <div class="grid-content">{{ uploadResult.pageCount || '--' }}</div>
              </el-col>
            </el-row>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-card class="info-card" ref="logCardRef">
      <div class="console-header">
        <span>系统运行日志</span>
        <el-button link type="primary" size="small" @click="clearLogs">清空日志</el-button>
      </div>
      <div class="console-content">
        <div v-for="(log, index) in consoleLogs" :key="index" class="log-line">
          <span class="log-time">[{{ log.time }}]</span>
          <span :class="['log-level', `level-${log.level}`]">{{ log.level.toUpperCase() }}</span>
          <span class="log-message">{{ log.message }}</span>
        </div>
        <div v-if="consoleLogs.length === 0" class="empty-log">暂无日志信息...</div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "Data",
  inheritAttrs: false,
});

import { useAppStore } from "@/store/modules/app.store";
import { useUserStore } from "@/store/modules/user.store";
import { DeviceEnum } from "@/enums/settings/device.enum";

import MenuAPI, { MenuPageQuery, MenuForm, MenuTable } from "@/api/module_system/menu";
import { MenuTypeEnum } from "@/enums/system/menu.enum";
import { formatTree } from "@/utils/common";
import { formatToDateTime } from "@/utils/dateUtil";
import { ElMessage, UploadRequestOptions, UploadFile, UploadFiles } from "element-plus";

// 日志接口定义
interface LogItem {
  time: string;
  level: "info" | "success" | "warning" | "error";
  message: string;
}

const appStore = useAppStore();
const userStore = useUserStore();

// 日志相关
const logCardRef = ref();
const consoleLogs = ref<LogItem[]>([]);
const uploadFileList = ref<UploadFile[]>([]);

// 添加日志
function appendLog(message: string, level: "info" | "success" | "warning" | "error" = "info") {
  consoleLogs.value.push({
    time: formatToDateTime(new Date()),
    level,
    message,
  });
  
  // 自动滚动到底部
  nextTick(() => {
    const cardBody = logCardRef.value?.$el.querySelector('.el-card__body');
    if (cardBody) {
      cardBody.scrollTop = cardBody.scrollHeight;
    }
  });
}

// 清空日志
function clearLogs() {
  consoleLogs.value = [];
}

// 文件超出限制
function handleExceed(files: File[], uploadFiles: UploadFiles) {
  appendLog(`选择文件数量超出限制，当前限制 1 个文件`, "warning");
  ElMessage.warning(`当前限制选择 1 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + uploadFiles.length} 个文件`);
}

// 自定义上传处理
async function handleHttpRequest(options: UploadRequestOptions) {
  const { file } = options;
  appendLog(`开始处理文件: ${file.name}`, "info");
  appendLog(`文件大小: ${(file.size / 1024).toFixed(2)} KB`, "info");
  
  try {
    // 模拟上传和后端处理过程
    appendLog("正在上传文件到服务器...", "info");
    
    // 这里替换为真实的 API 调用
    // const formData = new FormData();
    // formData.append('file', file);
    // const res = await uploadApi(formData);
    
    // 模拟延迟
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    appendLog("文件上传成功，正在解析...", "info");
    
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 模拟后端返回的数据
    const mockResponse = {
      projectName: "示例项目A",
      contractNo: "HT-2023-001",
      partName: "连接板",
      partCode: "P-001",
      partCount: "120",
      pageCount: "5"
    };
    
    // 更新结果显示
    Object.assign(uploadResult, mockResponse);
    
    appendLog(`文件解析完成! 部件名称: ${mockResponse.partName}`, "success");
    appendLog(`后端处理完毕，状态: 正常`, "success");
    
  } catch (error) {
    appendLog(`处理失败: ${error}`, "error");
    options.onError(error as any);
  }
}

const queryFormRef = ref();
const dataFormRef = ref();
const selectIds = ref<number[]>([]);
const loading = ref(false);

const isExpand = ref(false);
const isExpandable = ref(true);

// 分页表单
const pageTableData = ref<MenuTable[]>([]);

// 详情表单
const detailFormData = ref<MenuTable>({});

// 分页查询参数
const queryFormData = reactive<MenuPageQuery>({
  name: undefined,
  status: undefined,
  created_time: undefined,
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

// 编辑表单
const formData = reactive<MenuForm>({
  id: undefined,
  name: undefined,
  type: MenuTypeEnum.CATALOG,
  icon: undefined,
  order: 999,
  permission: "",
  route_name: "",
  route_path: "",
  component_path: undefined,
  redirect: undefined,
  parent_id: undefined,
  keep_alive: false,
  hidden: false,
  always_show: false,
  title: "",
  params: undefined,
  affix: false,
  status: "0",
  description: undefined,
});

// 弹窗状态
const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
});

const drawerSize = computed(() => (appStore.device === DeviceEnum.DESKTOP ? "600px" : "90%"));

// 顶级菜单下拉选项
const menuOptions = ref<OptionType[]>([]);

// 表单验证规则
const rules = reactive({
  name: [
    { required: true, message: "请输入菜单名称", trigger: "blur" },
    { min: 2, max: 50, message: "长度 2 到 50 个字符", trigger: "blur" },
  ],
  parent_id: [{ required: true, message: "请选择父级菜单", trigger: "blur" }],
  type: [{ required: true, message: "请选择菜单类型", trigger: "blur" }],
  order: [{ required: true, message: "请输入排序", trigger: "blur" }],
  permission: [{ required: true, message: "请输入权限标识", trigger: "blur" }],
  route_name: [{ required: true, message: "请输入路由名称", trigger: "blur" }],
  route_path: [
    { required: true, message: "请输入路由路径", trigger: "blur" },
    {
      validator: (rule: any, value: string, callback: any) => {
        if (value && !value.startsWith("/")) {
          callback(new Error("目录和菜单路由必须以/开头"));
        } else {
          callback();
        }
      },
      trigger: "blur",
    },
  ],
  component_path: [{ required: true, message: "请输入组件路径", trigger: "blur" }],
  title: [
    { required: true, message: "请输入菜单标题", trigger: "blur" },
    { min: 2, max: 50, message: "长度 2 到 50 个字符", trigger: "blur" },
  ],
  keep_alive: [{ required: true, message: "请选择是否缓存", trigger: "change" }],
  hidden: [{ required: true, message: "请选择是否隐藏", trigger: "change" }],
  always_show: [{ required: true, message: "请选择始终显示", trigger: "change" }],
  status: [{ required: true, message: "请选择状态", trigger: "change" }],
});

// 选择表格的行菜单ID
const selectedMenuId = ref<number | undefined>();

// 日期范围临时变量
const dateRange = ref<[Date, Date] | []>([]);

// 处理日期范围变化
function handleDateRangeChange(range: [Date, Date]) {
  dateRange.value = range;
  if (range && range.length === 2) {
    queryFormData.created_time = [formatToDateTime(range[0]), formatToDateTime(range[1])];
  } else {
    queryFormData.created_time = undefined;
  }
}

// 列表刷新
async function handleRefresh() {
  loading.value = true;
  try {
    const response = await MenuAPI.listMenu(queryFormData);
    pageTableData.value = response.data.data;
  } catch (error: any) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

// 修改菜单选项过滤逻辑，添加递归过滤函数
const filterMenuTypes = (nodes: MenuTable[]) => {
  return nodes
    .filter((node) => node.type === MenuTypeEnum.CATALOG || node.type === MenuTypeEnum.MENU)
    .map((node: any): any => ({
      ...node,
      children: node.children ? filterMenuTypes(node.children) : [],
    }));
};

// 加载表格数据
async function loadingData() {
  loading.value = true;
  try {
    const response = await MenuAPI.listMenu(queryFormData);
    pageTableData.value = response.data.data;
    // 加载菜单选项，只显示目录、菜单
    menuOptions.value = formatTree(filterMenuTypes(response.data.data));
  } catch (error: any) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

// 查询（重置页码后获取数据）
async function handleQuery() {
  loadingData();
}

// 重置查询
async function handleResetQuery() {
  queryFormRef.value.resetFields();
  // 额外清空日期范围与时间查询参数
  dateRange.value = [];
  queryFormData.created_time = undefined;
  handleQuery();
}

// 定义初始表单数据常量
const initialFormData: MenuForm = {
  id: undefined,
  name: undefined,
  type: MenuTypeEnum.MENU,
  icon: undefined,
  order: 1,
  permission: "",
  route_name: "",
  route_path: "",
  component_path: "",
  redirect: "",
  parent_id: undefined,
  keep_alive: false,
  hidden: false,
  always_show: false,
  title: "",
  params: [] as { key: string; value: string }[],
  affix: false,
  status: "0",
  description: undefined,
};

// 重置表单
async function resetForm() {
  if (dataFormRef.value) {
    dataFormRef.value.resetFields();
    dataFormRef.value.clearValidate();
  }
  // 完全重置 formData 为初始状态
  Object.assign(formData, initialFormData);
}

// 行复选框选中项变化
async function handleSelectionChange(selection: any) {
  selectIds.value = selection.map((item: any) => item.id);
}

// 行点击事件
async function handleRowClick(row: MenuTable) {
  selectedMenuId.value = row.id;
}

// 关闭弹窗
async function handleCloseDialog() {
  dialogVisible.visible = false;
  resetForm();
}

//打开弹窗
async function handleOpenDialog(
  type: "create" | "update" | "detail",
  id?: number,
  parentId?: number
) {
  dialogVisible.type = type;
  if (id) {
    const response = await MenuAPI.detailMenu(id);
    if (type === "detail") {
      dialogVisible.title = "菜单详情";
      Object.assign(detailFormData.value, response.data.data);
    } else if (type === "update") {
      dialogVisible.title = "修改菜单";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增菜单";
    // 重置表单为初始状态
    Object.assign(formData, initialFormData);
    // 设置父级部门
    if (parentId) {
      formData.parent_id = parentId;
    }
  }
  dialogVisible.visible = true;
}

// 菜单类型切换
function handleMenuTypeChange() {
  // 如果菜单类型改变
  if (formData.type !== formData.type) {
    if (formData.type === MenuTypeEnum.MENU) {
      // 目录切换到菜单时，清空组件路径
      formData.component_path = "";
    }
  }
}

// 提交表单
async function handleSubmit() {
  // 表单校验
  dataFormRef.value.validate(async (valid: any) => {
    if (valid) {
      loading.value = true;
      // 根据弹窗传入的参数(deatil\create\update)判断走什么逻辑
      const id = formData.id;
      try {
        if (id) {
          await MenuAPI.updateMenu(id, formData);
        } else {
          await MenuAPI.createMenu(formData);
        }
        await userStore.getUserInfo();
        dialogVisible.visible = false;
        resetForm();
        handleResetQuery();
      } catch (error: any) {
        console.error(error);
      } finally {
        loading.value = false;
      }
    }
  });
}

// 删除、批量删除
async function handleDelete(ids: number[]) {
  ElMessageBox.confirm("确认删除该项数据?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        loading.value = true;
        await MenuAPI.deleteMenu(ids);
        await userStore.getUserInfo();
        handleResetQuery();
      } catch (error: any) {
        console.error(error);
      } finally {
        loading.value = false;
      }
    })
    .catch(() => {
      ElMessageBox.close();
    });
}

// 批量启用/停用
async function handleMoreClick(status: string) {
  ElMessageBox.confirm(`确认${status === "0" ? "启用" : "停用"}该项数据?`, "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        loading.value = true;
        await MenuAPI.batchMenu({ ids: selectIds.value, status });
        handleResetQuery();
      } catch (error: any) {
        console.error(error);
      } finally {
        loading.value = false;
      }
    })
    .catch(() => {
      ElMessageBox.close();
    });
}

onMounted(() => {
  handleQuery();
});
</script>

<style lang="scss" scoped>
.app-container {
  height: calc(100vh - 84px);
  display: flex;
  flex-direction: column;
}

.data-table {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  
  // :deep(.el-card__body) {
  //   flex: 1;
  //   display: flex;
  //   flex-direction: column;
  //   overflow: hidden;
  // }

  .data-table__content {
    flex: 1;
    height: 100%;
  }
}

/* 卡片基础间距 */
.upload-card,
.report-card {
  height: 230px;
}

// .report-card {
//   height: 225px;
//   // --grid-border-color: #ebeef5;
//   // --label-bg-color: #f5f7fa;
// }

/* 标题样式 */
.report-header {
  text-align: center;
  // font-size: 16px;
  // font-weight: bold;
  margin-bottom: 20px;
  // color: #303133;
}

/* 网格总容器：控制外边框 */
.report-grid {
  border: 1px solid var(--el-border-color);
  font-size: 14px;
}

/* 行样式 */
.grid-row {
  display: flex;
  border-bottom: 1px solid var(--el-border-color);
}

.grid-row.no-border {
  border-bottom: none;
}

/* 列内元素布局 */
.col-item {
  display: flex;
}

/* 标签样式 (灰色区域) */
.grid-label {
  width: 100px;
  min-width: 100px;
  background-color: var(--el-border-color-extra-light);
  padding: 12px;
  text-align: center;
  // font-weight: bold;
  // color: #606266;
  border-right: 1px solid var(--el-border-color);
  // display: flex;
  // align-items: center;
  // justify-content: center;
}

/* 内容样式 (白色区域) */
.grid-content {
  // flex: 1;
  padding: 12px;
  // color: #303133;
  display: flex;
  align-items: center;
}

/* 辅助功能类 */
.border-left { border-left: 1px solid var(--el-border-color); }
// .font-bold { font-weight: bold; }
// .divider { margin: 0 10px; color: #dcdfe6; }
// .highlight { font-weight: bold; color: #409eff; }

// .code-style {
//   color: #cf4444;
//   font-family: 'Consolas', 'Monaco', monospace;
//   font-weight: bold;
// }
.info-card {
  flex: 1;
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  overflow: hidden; // 卡片本身不滚动

  :deep(.el-card__body) {
    flex: 1;
    overflow-y: auto; // 内容区域滚动
    padding: 10px;
    background-color: #1e1e1e; // 黑色背景，模拟控制台
    color: #d4d4d4; // 浅灰色文字
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  }
}

.console-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 8px;
  margin-bottom: 8px;
  border-bottom: 1px solid #333;
  color: #fff;
  font-weight: bold;
}

.console-content {
  font-size: 13px;
  line-height: 1.5;
}

.log-line {
  margin-bottom: 4px;
  word-break: break-all;
}

.log-time {
  color: #888;
  margin-right: 8px;
}

.log-level {
  display: inline-block;
  width: 60px;
  font-weight: bold;
  margin-right: 8px;
  
  &.level-info { color: #409eff; }
  &.level-success { color: #67c23a; }
  &.level-warning { color: #e6a23c; }
  &.level-error { color: #f56c6c; }
}

.log-message {
  color: #d4d4d4;
}

.empty-log {
  color: #666;
  text-align: center;
  margin-top: 20px;
  font-style: italic;
}


</style>
