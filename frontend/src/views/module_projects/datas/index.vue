<!-- 数据导入 -->
<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <SearchForm
      v-model:model-value="queryFormData"
      :source-data="tableSourceData?.data || []"
      :show-no="false"
      @update="handleUpdate"
      @reset="handleResetQuery"
    >
      <template #extra>
        <el-button
          v-hasPerm="['module_projects:parts:query']"
          type="warning"
          icon="refresh"
          @click="isShow = !isShow"
        >
          {{ isShow ? "切换零件" : "切换组件" }}
        </el-button>
        <el-button
          v-hasPerm="['module_projects:datas:create']"
          type="success"
          icon="plus"
          @click="handleSaveToDB()"
        >
          保存
        </el-button>
        <el-button
          v-hasPerm="['module_projects:datas:delete']"
          type="danger"
          icon="delete"
          :disabled="!tableSourceData?.data"
          @click="handleDelete()"
        >
          放弃
        </el-button>
      </template>
    </SearchForm>

    <!-- 内容区域 -->
    <PartsTable v-show="!isShow" :data="pageTableData" />

    <!-- 空数据时显示上传组件 -->
    <el-row v-show="isShow" :gutter="20">
      <el-col :span="8">
        <el-card class="upload-card">
          <div class="upload-wrapper">
            <el-upload
              ref="uploadRef"
              class="upload-demo"
              drag
              action="#"
              accept=".dwg"
              :auto-upload="true"
              :limit="1"
              :show-file-list="false"
              :on-exceed="handleExceed"
              :http-request="handleHttpRequest"
              style="max-width: 500px"
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
      </el-col>
      <el-col :span="16">
        <el-card class="report-card">
          <div class="report-header">文件解析结果</div>
          <div class="report-grid">
            <el-row class="grid-row">
              <el-col :span="18" class="col-item">
                <div class="grid-label">项目名称</div>
                <div class="grid-content">{{ uploadResult.projectName || "--" }}</div>
              </el-col>
              <el-col :span="6" class="col-item">
                <div class="grid-label border-left">零件数量</div>
                <div class="grid-content">{{ uploadResult.partCount || "--" }}</div>
              </el-col>
            </el-row>
            <el-row class="grid-row">
              <el-col :span="18" class="col-item">
                <div class="grid-label">部件名称</div>
                <div class="grid-content">{{ uploadResult.componentName || "--" }}</div>
              </el-col>
              <el-col :span="6" class="col-item">
                <div class="grid-label border-left">文件数量</div>
                <div class="grid-content">{{ uploadResult.pageCount || "--" }}</div>
              </el-col>
            </el-row>
            <el-row class="grid-row no-border">
              <el-col :span="9" class="col-item">
                <div class="grid-label">部件编号</div>
                <div class="grid-content">{{ uploadResult.componentCode || "--" }}</div>
              </el-col>
              <el-col :span="9" class="col-item border-right">
                <div class="grid-label border-left">合同编号</div>
                <div class="grid-content">{{ uploadResult.contractNo || "--" }}</div>
              </el-col>
              <el-col :span="6" class="col-item">
                <div class="grid-label border-left">部件数量</div>
                <div class="grid-content">{{ uploadResult.componentCount || "--" }}</div>
              </el-col>
            </el-row>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <!-- 显示解析日志 -->
    <el-card v-show="isShow" class="info-card">
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
  name: "Datas",
  inheritAttrs: false,
});

import SearchForm from "../SearchForm.vue";
import { useAppStore } from "@/store/modules/app.store";
import { useUserStore } from "@/store/modules/user.store";
import DatasAPI, { DatasPageQuery, UploadInnerData } from "@/api/module_projects/datas";
import ComponentsTable from "../ComponentsTable.vue";
// import { ComponentsData } from "@/api/module_projects/components";
import PartsTable from "../PartsTable.vue";
import PartsAPI, { PartsData } from "@/api/module_projects/parts";

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
const pageTableData = ref<PartsData[] | any[]>([]);
// 1. 显式定义 tableSourceData，给它一个初始结构
const tableSourceData = ref<UploadInnerData>();

// 是否显示上传组件，文件解析结果和日志
const isShow = ref(true);

// 根据文本内容返回对应的颜色类名或直接返回颜色值
const getLogColor = (text: string) => {
  if (text.includes("错误")) {
    return "var(--el-color-primary)";
  }
};

// 更新表格数据
const handleUpdate = (val: any[]) => {
  const next = Array.isArray(val) ? val : [];
  pageTableData.value = flattenTree(next);
};

//  递归排序：同时处理当前层级及所有子节点的万通码排序
const sortTableTree = (items: any[]) => {
  if (!items || !items.length) return;

  // 1. 对当前层级进行排序 (localeCompare numeric:true 会自动处理 1.2 < 1.10)
  items.sort((a, b) => {
    const strA = String(a.wtcode || "");
    const strB = String(b.wtcode || "");
    return strA.localeCompare(strB, undefined, { numeric: true, sensitivity: "base" });
  });

  // 2. 递归处理子节点
  items.forEach((item) => {
    if (item.children && item.children.length > 0) {
      sortTableTree(item.children);
    }
  });
};

// 分页查询参数
const queryFormData = reactive<DatasPageQuery>({
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
  componentCode: "",
  componentName: "",
  componentCount: "",
  partCount: "",
  pageCount: "",
});

// 选择表格的行菜单ID
const selectedMenuId = ref<number | undefined>();

// 日期范围临时变量
const dateRange = ref<[Date, Date] | []>([]);

// 树形数据递归过滤
const filterTreeData = (nodes: any[], query: DatasPageQuery): any[] => {
  const qCode = query.code?.trim().toLowerCase();
  const qSpec = query.spec?.trim().toLowerCase();
  const qMaterial = query.material?.trim().toLowerCase();

  return nodes
    .map((node) => {
      // 1. 先递归处理子节点
      const filteredChildren = node.children ? filterTreeData(node.children, query) : [];

      // 2. 检查当前节点是否匹配
      const nCode = String(node.code || "").toLowerCase();
      const nSpec = String(node.spec || "").toLowerCase();
      const nMaterial = String(node.material || "").toLowerCase();
      const nRemark = String(node.remark || "").toLowerCase();

      const isSelfMatch =
        (!qCode || nCode.includes(qCode)) &&
        (!qSpec || nSpec.includes(qSpec)) &&
        (!qMaterial || nMaterial.includes(qMaterial) || nRemark.includes(qMaterial));

      // 3. 如果自身匹配或子节点有匹配项，则返回该节点副本
      if (isSelfMatch || filteredChildren.length > 0) {
        return { ...node, children: filteredChildren };
      }
      return null;
    })
    .filter((node): node is any => node !== null); // 4. 过滤掉不匹配的项
};

// 重置查询
async function handleResetQuery() {
  // 1. 清空查询对象：使用 keyof 确保索引安全
  (Object.keys(queryFormData) as (keyof typeof queryFormData)[]).forEach((key) => {
    queryFormData[key] = undefined;
  });

  // 2. 恢复全量数据
  const sourceData = tableSourceData.value?.data || [];
  pageTableData.value = [...sourceData];

  // 3. 排序（SearchForm 内部其实也有排序逻辑，这里保持一致即可）
  sortTableTree(pageTableData.value);
}

// 行复选框选中项变化
async function handleSelectionChange(selection: any) {
  selectIds.value = selection.map((item: any) => item.id);
}

async function deleteData() {
  // 1. 销毁原始数据源对象
  tableSourceData.value = undefined;
  // 2. 清空当前显示的表格数据
  pageTableData.value = [];
  total.value = 0;
  // 3. 重置解析结果面板
  Object.assign(uploadResult, {
    projectName: "",
    contractNo: "",
    componentName: "",
    componentCode: "",
    componentCount: "",
    partCount: "",
    pageCount: "",
  });
  // 4. 重置查询表单
  queryFormRef.value?.resetFields();
  // 5. 隐藏数据表，显示上传组件
  isShow.value = true;
}

// 放弃当前数据：销毁对象、清空表格、切换视图
async function handleDelete() {
  try {
    // 1. 二次确认，防止误操作
    await ElMessageBox.confirm("确定要放弃当前解析的数据吗？未保存的数据将会丢失。", "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
    // 2. 执行删除操作
    await deleteData();
    // 3. 提示用户操作成功
    ElMessage.success("已放弃当前数据");
  } catch (error) {
    // 用户取消操作，不做处理
  }
}

//  树转平级数组函数
const flattenTree = (tree: any[]): any[] => {
  let result: any[] = [];
  tree.forEach((node) => {
    // 解构：提取出数据，剔除 children
    const { children, ...itemData } = node;
    result.push(itemData);
    if (children && children.length > 0) {
      result = result.concat(flattenTree(children));
    }
  });
  return result;
};

// 保存到数据库逻辑
async function handleSaveToDB() {
  if (!pageTableData.value.length) {
    ElMessage.warning("暂无解析数据可保存");
    return;
  }

  try {
    await ElMessageBox.confirm("确认将当前解析结果保存至数据库？", "操作确认", {
      type: "success",
      confirmButtonText: "立即保存",
    });

    loading.value = true;

    // 1. 获取扁平化后的数据
    const flatDetails = flattenTree(pageTableData.value);

    // 2. 组装后端要求的完整报文
    const payload = {
      // 这里的字段名（如 project_name）建议根据后端文档调整
      projects: {
        code: uploadResult.componentCode.substring(0, uploadResult.componentCode.lastIndexOf(".")),
        name: uploadResult.projectName,
        no: uploadResult.contractNo,
      },
      components: {
        project_code: uploadResult.componentCode.substring(
          0,
          uploadResult.componentCode.lastIndexOf(".")
        ),
        wtcode: flatDetails[0]["wtcode"],
        code: flatDetails[0]["code"],
        spec: flatDetails[0]["spec"],
        count: flatDetails[0]["count"],
        material: flatDetails[0]["material"],
        unit_mass: flatDetails[0]["unit_mass"],
        total_mass: flatDetails[0]["total_mass"],
        remark: flatDetails[0]["remark"],
      },
      parts: flatDetails,
    };
    if (payload.components.project_code.includes(".")) {
      throw new Error("导入数据必须是部件，不能是组件或零件");
    } else {
      // 3. 提交
      const res = await DatasAPI.saveDatas(payload);
    }
  } catch (error: any) {
    if (error !== "cancel") {
      ElMessage.error(error.message || "保存失败");
    }
  } finally {
    loading.value = false;
  }
}

// 当用户选择新文件上传时，直接替换掉旧的
function handleExceed(files: File[]) {
  // 清除组件内部状态
  uploadRef.value!.clearFiles();
  const file = files[0] as any;
  file.uid = "upload_"; // 固定UID
  uploadRef.value!.handleStart(file);
  // 立即触发 http-request
  uploadRef.value!.submit();
}

// 执行上传函数
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
    const res = await DatasAPI.uploadFile(formData);
    // 4. 直接取值（无任何判断，直接拿后端返回的表格数组）
    tableSourceData.value = res.data.data;
    // 5. 将后端返回的提示信息绑定到 el-alert
    const { 项目名称, 合同号, 部件名称, 部件编号, 数量, 文件个数, 零件数量 } = res.data?.data ?? {};
    uploadResult.projectName = 项目名称 ?? "";
    uploadResult.contractNo = 合同号 ?? "";
    uploadResult.componentName = 部件名称 ?? "";
    uploadResult.componentCode = 部件编号 ?? "";
    uploadResult.componentCount = 数量 ?? "";
    uploadResult.pageCount = String(文件个数) ?? "";
    uploadResult.partCount = String(零件数量) ?? "";
    // 6. 直接将后端数据添加到表格（前置追加，保持原有顺序）
    const data = [...(tableSourceData.value?.data || [])];
    // 7. 执行递归排序
    // sortTableTree(data);
    // // 8. 赋值给分页数据
    // console.log(data)
    pageTableData.value = flattenTree(data);
    // 9. 更新表格总条数
    total.value = pageTableData.value.length;
    // 10. 自动切换到表格视图
    // isShow.value = false;
  } catch (error) {
    console.error("上传失败:", error);
  } finally {
    uploadRef.value?.clearFiles();
    uploading.value = false;
  }
}
</script>

<style lang="scss" scoped>
/* 卡片基础间距 */
.upload-card,
.report-card {
  height: 230px;
}

/* 标题样式 */
.report-header {
  text-align: center;
  margin-bottom: 20px;
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
  // overflow: hidden;
}

/* 标签样式 (灰色区域) */
.grid-label {
  width: 100px;
  min-width: 100px;
  padding: 12px;
  text-align: center;
  border-right: 1px solid var(--el-border-color);
  background-color: var(--el-border-color-extra-light);
}

/* 内容样式 (白色区域) */
.grid-content {
  // flex: 1;
  padding: 10px;
  color: var(--el-color-primary);
  display: flex;
  align-items: center;
  min-width: 0px;
  white-space: nowrap;
  text-overflow: ellipsis;
}

/* 辅助功能类 */
.border-left {
  border-left: 1px solid var(--el-border-color);
}
.info-card {
  flex: 1;
  margin-top: 10px;
  overflow: auto;
}
</style>
