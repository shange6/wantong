<template>
  <div class="components-table-container">
    <BaseCard
      v-bind="$attrs"
      ref="dataTableRef"
      v-loading="loading"
      row-key="wtcode"
      :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
      :data="pageTableData"
      :header-cell-style="{ textAlign: 'center' }"
      class="data-table__content"
      border
      stripe
      height="100%"
      @selection-change="handleSelectionChange"
      @row-click="handleRowClick"
    ></BaseCard>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from "vue";
import BaseCard from "./BaseCard.vue";
import PartsAPI, { PartsData, PartsForm, PartsQuery } from "@/api/module_projects/parts";
import { formatTree } from "@/utils/common";

// 表格数据
const loading = ref(false); // 表格加载状态
const pageTableData = ref<PartsData[]>([]); // 渲染在表格上的树形数据
const total = ref(0); // 总条数
const selectIds = ref<number[]>([]); // 选中的行 ID 集合
const selectedId = ref<number | undefined>(undefined);
const dataTableRef = ref(); // BaseCard 的组件实例引用

const props = defineProps<{
  queryParams?: PartsQuery; // 查询参数
  tableData?: PartsData[]; // 外部传入的数据
}>();

// 监听外部数据变化
watch(
  () => props.tableData,
  (val) => {
    // 移除 val.length > 0 的判断，允许空数组更新
    if (val) {
      pageTableData.value = val;
      total.value = val.length;
      console.log("PartsTable received external data:", val);
    }
  },
  { 
    immediate: true, 
    deep: true 
  }
);

// 表单数据
const formRef = ref();
const formData = reactive<PartsForm>({
  project_code: "",
  parent_code: "",
  wtcode: "",
  code: "",
  spec: "",
  count: 0,
  material: "",
  unit_mass: 0,
  total_mass: 0,
  remark: "",
});

// 重置表单
function resetForm() {
  formRef.value?.resetFields();
  Object.assign(formData, {
    id: undefined,
    project_code: "",
    parent_code: "",
    wtcode: "",
    code: "",
    spec: "",
    count: 0,
    material: "",
    unit_mass: 0,
    total_mass: 0,
    remark: "",
  });
}
// 组件名称
defineOptions({
  name: "PartsTable",
});

const listToTree = (data: any[]) => {
  const map: Record<string, any> = {};
  const roots: any[] = [];

  // 按照 wtcode 排序，确保父节点在处理时容易找到（虽然 map 查找不依赖顺序，但排序是个好习惯）
  data.sort((a, b) => a.wtcode.length - b.wtcode.length || a.wtcode.localeCompare(b.wtcode));

  data.forEach((item) => {
    // 初始化每个节点，添加 children 数组
    map[item.wtcode] = { ...item, children: [] };
  });

  data.forEach((item) => {
    const node = map[item.wtcode];
    // 检查是否有上级。零件的 wtcode 格式通常是 'PROJECT.COMP.PART'
    const lastDotIndex = item.wtcode.lastIndexOf(".");

    if (lastDotIndex > -1) {
      const parentWtcode = item.wtcode.substring(0, lastDotIndex);
      if (map[parentWtcode]) {
        map[parentWtcode].children.push(node);
      } else {
        // 如果找不到直接父节点，可能它的父节点是组件，不在零件列表里，所以它本身是零件表的根
        roots.push(node);
      }
    } else {
      // 没有点号，说明是顶级节点
      roots.push(node);
    }
  });
  return roots;
};

// 组件挂载时查询
// onMounted(() => {
//   handleQuery();
// });

// 暴露查询方法
defineExpose({
  handleQuery,
  pageTableData,
  listToTree,
});

// 查询
async function handleQuery() {
  loading.value = true;
  try {
    const params = {
      ...props.queryParams,
      page_no: 1,
      page_size: 0, // 0 表示不分页，获取全部数据
    };
    const res = await PartsAPI.getList(params);
    // 修正路径：增加对 res.data.data.items 的兼容
    const rawData = res.data?.items || res.data?.data?.items || [];
    const totalCount = res.data?.total || res.data?.data?.total || 0;

    // 1. 更新本地显示
    pageTableData.value = listToTree(rawData);
    total.value = totalCount;

    // 2. 关键：把拿到的原始全量数据抛给父组件，让 SearchForm 有“原材料”可以过滤
    emit("load-data", rawData);
  } finally {
    loading.value = false;
  }
}

// 表格选择
function handleSelectionChange(selection: PartsData[]) {
  selectIds.value = selection.map((item) => item.id);
}

// 抛出事件
const emit = defineEmits<{
  (e: "row-click", row: PartsData): void;
  (e: "load-data", data: PartsData[]): void; // 新增：数据加载完成后传给父组件
}>();

// 表格行点击
function handleRowClick(row: PartsData) {
  // 关键：将行数据传给父组件
  emit("row-click", row);
}
</script>

<style scoped>
.components-table-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  /* margin-top: 0px; */
}
</style>
