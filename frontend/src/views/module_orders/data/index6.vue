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
          <el-input v-model="queryFormData.code" placeholder="请输入编号" clearable style="width: 100px"/>
        </el-form-item>
        <el-form-item prop="spec" label="名称">
          <el-input v-model="queryFormData.spec" placeholder="请输入名称" clearable style="width: 100px"/>
        </el-form-item>
        <el-form-item prop="material" label="材料/备注">
          <el-input v-model="queryFormData.material" placeholder="输入材料备注" clearable style="width: 110px"/>
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
          </el-button><el-button
            v-hasPerm="['module_system:menu:query']"
            type="info"
            icon="refresh"
            @click="isShow = !isShow"
          >
            切换
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
            :disabled="!tableSourceData?.data"
            @click="handleDelete()"
          >
            放弃
          </el-button>
          <!-- 展开/收起 -->          
        </el-form-item>
        <!-- 上传结果提示 -->
      </el-form>
    </div>

    <!-- 内容区域 -->
    <el-card v-if="isShow" class="data-table">
      <!-- 功能区域 -->
      <!-- 表格区域 -->
      <el-table
        ref="dataTableRef"
        row-key="wtcode"
        :data="pageTableData"
        :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
        :header-cell-style="{ textAlign: 'center' }"
        class="data-table__content"
        border
        stripe
        :default-sort="{ prop: 'wtcode', order: 'ascending' }"
        @selection-change="handleSelectionChange"
        @row-click="handleRowClick"
      >
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column type="selection" fixed min-width="55" align="center" />
        <el-table-column label="万通码" prop="wtcode" min-width="150" show-overflow-tooltip sortable>
          <template #default="{ row }">
            {{ row.wtcode?.includes('.') ? row.wtcode.slice(row.wtcode.indexOf('.') + 1) : row.wtcode }}
          </template>          
        </el-table-column>
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
     <el-row v-if="!isShow" :gutter="20"">
      <el-col :span="8">
        <el-card class="upload-card">
          <div class="upload-wrapper">
            <el-upload
              ref="uploadRef"
              class="upload-demo"
              drag
              action="#"
              accept=".dwg"
              :file-list="uploadFile"
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
            <el-row class="grid-row">
              <el-col :span="18" class="col-item">
                <div class="grid-label">项目名称</div>
                <div class="grid-content">{{ uploadResult.projectName || '--' }}</div>
              </el-col> 
              <el-col :span="6" class="col-item">
                  <div class="grid-label border-left">零件数量</div>
                  <div class="grid-content">{{ uploadResult.partCount || '--' }}</div>
                </el-col>
            </el-row>
            <el-row class="grid-row">
              <el-col :span="18" class="col-item">
                <div class="grid-label">部件名称</div>
                <div class="grid-content">{{ uploadResult.componentName || '--' }}</div>
              </el-col> 
              <el-col :span="6" class="col-item">
                  <div class="grid-label border-left">文件数量</div>
                  <div class="grid-content">{{ uploadResult.pageCount || '--' }}</div>
                </el-col>
            </el-row>
            <el-row class="grid-row no-border">
              <el-col :span="9" class="col-item">
                <div class="grid-label">部件编号</div>
                <div class="grid-content">{{ uploadResult.componentCode || '--' }}</div>
              </el-col>
              <el-col :span="9" class="col-item border-right">
                  <div class="grid-label border-left">合同编号</div>
                  <div class="grid-content">{{ uploadResult.contractNo || '--' }}</div>
                </el-col>
              <el-col :span="6" class="col-item">
                <div class="grid-label border-left">部件数量</div>
                <div class="grid-content">{{ uploadResult.componentCount || '--' }}</div>
              </el-col>
            </el-row>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <!-- 显示解析日志 -->
    <el-card v-if="!isShow" class="info-card">
      <template #header>
        <div class="card-header">
          <span>详细解析日志</span>
        </div>
      </template>
      <div 
        v-for="(text, index) in tableSourceData?.info" 
        :key="index" 
        class="text-line"
        :style="{ fontSize: '15px', color: getLogColor(text) }"
      >
        {{ text }}
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
import { DataAPI, DataPageQuery, UploadInnerData } from "@/api/module_orders/data";
import MenuAPI, { MenuPageQuery, MenuForm, MenuTable } from "@/api/module_system/menu";
import { MenuTypeEnum } from "@/enums/system/menu.enum";
import { formatTree } from "@/utils/common";
import { formatToDateTime } from "@/utils/dateUtil";
import { isHeritageClause } from "typescript";

const appStore = useAppStore();
const userStore = useUserStore();

const queryFormRef = ref();
const dataTableRef = ref();
const dataFormRef = ref();
const selectIds = ref<number[]>([]);
const loading = ref(false);
const uploadRef = ref();
const uploadFile = ref<File>();
const uploadFileList = ref<any[]>([]);
const uploading = ref(false);
const currentPath = ref("/");
const total = ref(0);

const isExpand = ref(false);
const isExpandable = ref(true);

// 1. 显式定义 tableSourceData，给它一个初始结构
const tableSourceData = ref<UploadInnerData>();

// 是否显示上传组件，文件解析结果和日志
const isShow = ref(false)
// 分页表单
const pageTableData = ref<MenuTable[]>([]);

// 详情表单
const detailFormData = ref<MenuTable>({});

  // 根据文本内容返回对应的颜色类名或直接返回颜色值
const getLogColor = (text: string) => {
  if (text.includes('错误')) {  return "var(--el-color-primary)"; }
};



//  递归排序：同时处理当前层级及所有子节点的万通码排序
const sortTableTree = (items: any[]) => {
  if (!items || !items.length) return;

  // 1. 对当前层级进行排序 (localeCompare numeric:true 会自动处理 1.2 < 1.10)
  items.sort((a, b) => {
    const strA = String(a.wtcode || "");
    const strB = String(b.wtcode || "");
    return strA.localeCompare(strB, undefined, { numeric: true, sensitivity: 'base' });
  });

  // 2. 递归处理子节点
  items.forEach(item => {
    if (item.children && item.children.length > 0) {
      sortTableTree(item.children);
    }
  });
};

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
  componentName: "",
  componentCode: "",
  componentCount: "",
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
// function handleDateRangeChange(range: [Date, Date]) {
//   dateRange.value = range;
//   if (range && range.length === 2) {
//     queryFormData.created_time = [formatToDateTime(range[0]), formatToDateTime(range[1])];
//   } else {
//     queryFormData.created_time = undefined;
//   }
// }

// 列表刷新
// async function handleRefresh() {
//   loading.value = true;
//   try {
//     const response = await MenuAPI.listMenu(queryFormData);
//     pageTableData.value = response.data.data;
//   } catch (error: any) {
//     console.error(error);
//   } finally {
//     loading.value = false;
//   }
// }

// 修改菜单选项过滤逻辑，添加递归过滤函数
const filterMenuTypes = (nodes: MenuTable[]) => {
  return nodes
    .filter((node) => node.type === MenuTypeEnum.CATALOG || node.type === MenuTypeEnum.MENU)
    .map((node: any): any => ({
      ...node,
      children: node.children ? filterMenuTypes(node.children) : [],
    }));
};

// 树形数据递归过滤
const filterTreeData = (nodes: any[], query: DataPageQuery): any[] => {
  if (!nodes || nodes.length === 0) return [];
  
  const result: any[] = [];
  const qCode = query.code?.trim().toLowerCase();
  const qSpec = query.spec?.trim().toLowerCase();
  const qMaterial = query.material?.trim().toLowerCase();
  
  for (const node of nodes) {
    const nCode = (node.code || "").toString().toLowerCase();
    const nSpec = (node.spec || "").toString().toLowerCase();
    const nMaterial = (node.material || "").toString().toLowerCase();
    const nRemark = (node.remark || "").toString().toLowerCase();
    
    const matchCode = !qCode || nCode.includes(qCode);
    const matchSpec = !qSpec || nSpec.includes(qSpec);
    // 匹配材料 OR 备注
    const matchMaterial = !qMaterial || nMaterial.includes(qMaterial) || nRemark.includes(qMaterial);
    
    const isSelfMatch = matchCode && matchSpec && matchMaterial;
    
    // 递归过滤子节点
    const filteredChildren = filterTreeData(node.children || [], query);
    const hasMatchingChildren = filteredChildren.length > 0;
    
    if (isSelfMatch || hasMatchingChildren) {
      const newNode = { ...node };
      // 保留匹配的子节点路径
      newNode.children = filteredChildren;
      result.push(newNode);
    }
  }
  return result;
};

// 查询（前端过滤）
async function handleQuery() {
  loading.value = true;
  try {
    const sourceData = tableSourceData.value?.data || [];
    
    // 如果没有源数据，清空表格
    if (sourceData.length === 0) {
      pageTableData.value = [];
      total.value = 0;
      return;
    }

    // 1. 过滤
    const filtered = filterTreeData(sourceData, queryFormData);
    
    // 2. 排序
    sortTableTree(filtered);
    
    pageTableData.value = filtered;
    total.value = filtered.length;
    
    // 如果有筛选结果，切换到表格视图
    if (filtered.length > 0 && !isShow.value) {
      isShow.value = true;
    }
  } finally {
    loading.value = false;
  }
}

// 重置查询
async function handleResetQuery() {
  queryFormRef.value?.resetFields();
  dateRange.value = [];
  
  // 触发查询（此时条件为空，即恢复全量数据）
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

// 放弃当前数据：销毁对象、清空表格、切换视图
async function handleDelete() {

  try {
    // 1. 二次确认，防止误操作
    await ElMessageBox.confirm(
      "确定要放弃当前解析的数据吗？未保存的数据将会丢失。",
      "警告",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }
    );

    // 2. 销毁原始数据源对象
    tableSourceData.value = undefined;

    // 3. 清空当前显示的表格数据
    pageTableData.value = [];
    total.value = 0;

    // 4. 重置解析结果面板
    Object.assign(uploadResult, {
      projectName: "",
      contractNo: "",
      componentName: "",
      componentCode: "",
      componentCount: "",
      partCount: "",
      pageCount: "",
    });

    // 5. 重置查询表单
    queryFormRef.value?.resetFields();

    // 6. 隐藏数据表，显示上传组件
    isShow.value = false;

    ElMessage.success("已清空当前数据");
  } catch (error) {
    // 用户取消操作，不做处理
  }
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
    tableSourceData.value = res.data.data;  
    // 5. 将后端返回的提示信息绑定到 el-alert
    const { 项目名称, 合同号, 部件名称, 部件编号, 数量, 文件个数, 零件数量 } = res.data?.data ?? {}
    uploadResult.projectName = 项目名称 ?? '';
    uploadResult.contractNo = 合同号 ?? '';
    uploadResult.componentName = 部件名称 ?? '';
    uploadResult.componentCode = 部件编号 ?? '';
    uploadResult.componentCount = 数量 ?? '';
    uploadResult.pageCount = String(文件个数) ?? '';
    uploadResult.partCount = String(零件数量) ?? '';
    // 6. 直接将后端数据添加到表格（前置追加，保持原有顺序）
    const data = [...(tableSourceData.value?.data || [])];
    // 7. 执行递归排序
    sortTableTree(data);
    // 8. 赋值给分页数据
    pageTableData.value = data;
    // 9. 更新表格总条数
    total.value = pageTableData.value.length;

  } catch (error) {
    console.error("上传失败:", error);
  } finally {
    uploadRef.value?.clearFiles();
    uploading.value = false;
  }
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
  color: var(--el-color-primary);
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
  overflow: auto;
}


</style>
