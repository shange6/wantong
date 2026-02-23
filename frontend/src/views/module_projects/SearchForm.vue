<template>
  <div class="search-container">
    <el-form
      ref="queryFormRef"
      :model="modelValue"
      :inline="true"
      label-suffix=":"
      @submit.prevent="handleExecuteFilter"
    >
      <el-form-item v-if="showCode" prop="code" label="代号">
        <el-input
          :model-value="modelValue.code"
          placeholder="请输入代号"
          clearable
          style="width: 100px"
          class="search-input"
          @update:model-value="(val) => handleInput('code', val)"
        />
      </el-form-item>

      <el-form-item v-if="showSpec" prop="spec" label="名称">
        <el-input
          :model-value="modelValue.spec"
          placeholder="请输入名称"
          clearable
          style="width: 100px"
          class="search-input"
          @update:model-value="(val) => handleInput('spec', val)"
        />
      </el-form-item>

      <el-form-item v-if="showMaterial" prop="material" label="其他">
        <el-input
          :model-value="modelValue.material"
          placeholder="请输入其他"
          clearable
          style="width: 100px"
          class="search-input"
          @update:model-value="(val) => handleInput('material', val)"
        />
      </el-form-item>

      <el-form-item v-if="showNo" prop="no" label="编号">
        <el-input
          :model-value="modelValue.no"
          placeholder="请输入编号"
          clearable
          style="width: 100px"
          class="search-input"
          @update:model-value="(val) => handleInput('no', val)"
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
import { onUnmounted, toRaw, watch } from "vue";

// 1. 类型定义
interface TreeNode {
  code?: string;
  spec?: string;
  material?: string;
  remark?: string;
  no?: string;
  children?: TreeNode[]; // 依然保留可选的 children
  [key: string]: any;
}

interface QueryModel {
  code?: string;
  spec?: string;
  material?: string;
  no?: string;
}

interface Props {
  modelValue: QueryModel;
  sourceData: TreeNode[];
  showCode?: boolean;
  showSpec?: boolean;
  showMaterial?: boolean;
  showNo?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  showCode: true,
  showSpec: true,
  showMaterial: true,
  showNo: true,
});

const emit = defineEmits<{
  (e: "update", data: TreeNode[]): void;
  (e: "update:modelValue", value: QueryModel): void;
  (e: "reset"): void;
}>();

/**
 * 核心优化算法：完美兼容树形与扁平结构
 */
const filterData = (nodes: TreeNode[], query: QueryModel): TreeNode[] => {
  if (!nodes || nodes.length === 0) return [];

  // 预处理搜索关键字
  const q = {
    code: (query?.code || "").toString().trim().toLowerCase(),
    spec: (query?.spec || "").toString().trim().toLowerCase(),
    mat: (query?.material || "").toString().trim().toLowerCase(),
    no: (query?.no || "").toString().trim().toLowerCase(),
  };

  // 性能短路：无搜索条件时返回原数据
  if (!q.code && !q.spec && !q.mat && !q.no) return nodes;

  return nodes.reduce((acc, node) => {
    // 【关键修改点 1】：判断是否存在子节点
    const hasChildren = Array.isArray(node.children) && node.children.length > 0;

    // 如果有子节点，递归过滤；如果没有，返回空数组
    const filteredChildren = hasChildren ? filterData(node.children!, query) : [];

    // 属性安全提取
    const nCode = String(node.code ?? "").toLowerCase();
    const nSpec = String(node.spec ?? node.name ?? "").toLowerCase(); // spec和name有一个字段即可
    const nMat = String(node.material ?? "").toLowerCase();
    const nRem = String(node.remark ?? "").toLowerCase();
    const nNo = String(node.no ?? "").toLowerCase();

    // 匹配逻辑
    const isMatch =
      (!q.code || nCode.includes(q.code)) &&
      (!q.spec || nSpec.includes(q.spec)) &&
      (!q.mat || nMat.includes(q.mat) || nRem.includes(q.mat)) && // material和remark有一个包含关键字即可
      (!q.no || nNo.includes(q.no));

    // 【关键修改点 2】：决定是否保留节点及如何构建结构
    if (isMatch || filteredChildren.length > 0) {
      const newNode = { ...toRaw(node) };

      if (hasChildren) {
        // 如果原始数据是树形，挂载过滤后的子集
        newNode.children = filteredChildren;
      } else {
        // 如果原始数据是扁平的（没有 children 属性），确保结果中也不出现空 children 数组
        delete newNode.children;
      }

      acc.push(newNode);
    }
    return acc;
  }, [] as TreeNode[]);
};

const handleExecuteFilter = () => {
  const filtered = filterData(props.sourceData, props.modelValue);
  emit("update", filtered);
};

const handleReset = () => {
  const resetQuery: QueryModel = {
    code: undefined,
    spec: undefined,
    material: undefined,
    no: undefined,
  };

  // 1. 更新父组件的 v-model
  emit("update:modelValue", resetQuery);

  // 2. 触发父组件的 reset 事件（用于恢复全量数据等业务逻辑）
  emit("reset");

  // 3. 强制执行一次空过滤，确保表格显示完整数据
  // 注意：此时 props.modelValue 可能还未更新（取决于父组件响应速度），
  // 所以直接传空对象进行过滤
  const filtered = filterData(props.sourceData, resetQuery);
  emit("update", filtered);
};

// 如果没有 lodash，可以用下面的简易防抖函数
function debounce(fn: Function, delay: number) {
  let timer: ReturnType<typeof setTimeout> | null = null;
  return (...args: any[]) => {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => {
      fn(...args);
    }, delay);
  };
}

const handleInput = (key: keyof QueryModel, val: string) => {
  // 1. 构造最新的查询对象
  const nextQuery = { ...props.modelValue, [key]: val };
  // 2. 更新父组件的 v-model (同步状态)
  emit("update:modelValue", nextQuery);
  // 3. 【核心】立即执行过滤并通知父组件更新列表
  const filtered = filterData(props.sourceData, nextQuery);
  emit("update", filtered);
};
</script>
