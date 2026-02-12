<template>
  <div class="search-container">
    <el-form
      ref="queryFormRef"
      :model="modelValue" 
      :inline="true"
      label-suffix=":"
      @submit.prevent="handleExecuteFilter"
    >
      <el-form-item v-if="showCode" prop="code" label="代号" style="margin-right: 15px;">
        <el-input 
            v-model="modelValue.code" 
            placeholder="请输入代号" 
            clearable 
            style="width: 100px"
            @input="onInputChange"
        />
      </el-form-item>

      <el-form-item v-if="showSpec" prop="spec" label="名称" style="margin-right: 15px;">
        <el-input 
            v-model="modelValue.spec" 
            placeholder="请输入名称" 
            clearable 
            style="width: 100px"
            @input="onInputChange"
        />
      </el-form-item>

      <el-form-item v-if="showMaterial" prop="material" label="材料/备注" style="margin-right: 15px;">
        <el-input 
            v-model="modelValue.material" 
            placeholder="输入材料备注" 
            clearable 
            style="width: 110px"
            @input="onInputChange"
        />
      </el-form-item>
      
      <el-form-item v-if="showNo" prop="no" label="合同号">
        <el-input 
            v-model="modelValue.no" 
            placeholder="请输入合同号" 
            clearable 
            style="width: 100px"
            @input="onInputChange"
        />
      </el-form-item>

      <el-form-item class="search-buttons">
        <!-- <el-button type="primary" icon="search" @click="handleExecuteFilter">查询</el-button> -->
        <el-button type="default" icon="refresh" @click="handleReset">重置</el-button>
        <slot name="extra"></slot>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const props = withDefaults(defineProps<{
  modelValue: any;
  sourceData: any[];
  showCode?: boolean;
  showSpec?: boolean;
  showMaterial?: boolean;
  showNo?: boolean;
}>(), {
  sourceData: () => [],
  showCode: true,
  showSpec: true,
  showMaterial: true,
  showNo: true
});

const emit = defineEmits(['update', 'reset']);
const queryFormRef = ref();

// --- 核心逻辑：排序 ---
const sortTableTree = (items: any[]) => {
  if (!items?.length) return;
  items.sort((a, b) => String(a.wtcode || "").localeCompare(String(b.wtcode || ""), undefined, { numeric: true }));
  items.forEach(item => item.children && sortTableTree(item.children));
};

// --- 核心逻辑：递归过滤 (含 material + remark 联合搜索) ---
const filterTreeData = (nodes: any[], query: any): any[] => {
  const qCode = (query.code || '').trim().toLowerCase();
  const qSpec = (query.spec || '').trim().toLowerCase();
  const qMat = (query.material || '').trim().toLowerCase();
  const qNo = (query.no || '').trim().toLowerCase();

  return nodes.map(node => {
    const children = node.children ? filterTreeData(node.children, query) : [];
    
    const nCode = String(node.code || "").toLowerCase();
    const nSpec = String(node.spec || "").toLowerCase();
    const nMat = String(node.material || "").toLowerCase();
    const nRem = String(node.remark || "").toLowerCase(); 
    const nNo = String(node.no || "").toLowerCase();
    
    const isMatch = (!qCode || nCode.includes(qCode)) &&
                    (!qSpec || nSpec.includes(qSpec)) &&
                    (!qMat || (nMat.includes(qMat) || nRem.includes(qMat))) &&
                    (!qNo || nNo.includes(qNo));

    return (isMatch || children.length > 0) ? { ...node, children } : null;
  }).filter(v => v !== null) as any[];
};

// 执行过滤的主函数
const handleExecuteFilter = () => {
  const filtered = filterTreeData(props.sourceData, props.modelValue);
  sortTableTree(filtered);
  emit('update', filtered);
};

// --- 输入事件处理 (带防抖) ---
let timer: ReturnType<typeof setTimeout> | null = null;
const onInputChange = () => {
  if (timer) clearTimeout(timer);
  timer = setTimeout(() => {
    handleExecuteFilter();
  }, 200); // 200ms 防抖，响应更轻快
};

// 重置逻辑
const handleReset = () => {
  Object.keys(props.modelValue).forEach(key => {
    if(key !== 'project_code') props.modelValue[key] = '';
  });
  handleExecuteFilter(); // 重置后刷新列表显示全量
  emit('reset');
};
</script>