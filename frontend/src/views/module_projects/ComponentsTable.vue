<template>
    <div class="components-table-container">
        <BaseCard
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
        >
            <template #pagination-area>
                <el-pagination
                    v-model:current-page="pagination.page_no"
                    v-model:page-size="pagination.page_size"
                    :total="total"
                    :page-sizes="[10, 20, 50, 100]"
                    layout="total, sizes, prev, pager, next, jumper"
                    @size-change="handleQuery"
                    @current-change="handleQuery"
                />
            </template>
        </BaseCard>
    </div>
</template>

<script setup lang="ts">

import { ref, reactive, onMounted, watch } from 'vue';
import BaseCard  from './BaseCard.vue';
import ComponentsAPI, { ComponentsData, ComponentsForm, ComponentsQuery } from '@/api/module_projects/components';

// 表格数据
const loading = ref(false);             // 表格加载状态
const pageTableData = ref<any[]>([]);   // 渲染在表格上的树形数据
const total = ref(0);                   // 总条数
const selectIds = ref<number[]>([]);    // 选中的行 ID 集合
const selectedId = ref<number | undefined>(undefined);
const dataTableRef = ref();             // BaseCard 的组件实例引用
const pagination = reactive({           // 分页参数
  page_no: 1,
  page_size: 10,
});

const props = defineProps<{
  queryParams?: ComponentsQuery;        // 查询参数
}>();

// 表单数据
const formRef = ref();
const formData = reactive<ComponentsForm>({
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
  name: "ComponentsTable",
});

// 组件挂载时查询
onMounted(() => {
  handleQuery();
});

// 暴露查询方法
defineExpose({
  handleQuery,
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

// 抛出事件
const emit = defineEmits<{
  (e: 'row-click', row: ComponentsData): void
}>();

// 表格行点击
function handleRowClick(row: ComponentsData) {
  // 关键：将行数据传给父组件
  emit('row-click', row);
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
