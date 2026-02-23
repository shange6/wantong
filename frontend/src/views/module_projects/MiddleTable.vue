<template>
  <div class="middle-card-wrapper">
    <BaseCard v-bind="filterOtherAttrs" :data="displayData" @row-click="handleRowClick">
      <template #function-area>
        <slot name="function-area"></slot>
      </template>

      <template #append-columns="slotProps">
        <slot name="append-columns" v-bind="slotProps || {}" :format-wt-code="formatWtCode"></slot>
      </template>

      <template #pagination-area>
        <el-pagination
          v-if="fullData.length > 0 && !$attrs['row-key']"
          :current-page="currentPage"
          :page-size="pageSize"
          :total="fullData.length"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          background
          class="pagination-container"
          @update:current-page="handleCurrentPageUpdate"
          @update:page-size="handlePageSizeUpdate"
        />
      </template>
    </BaseCard>
  </div>
</template>

<script setup lang="ts">
import { useAttrs, computed } from "vue";
import BaseCard from "./BaseCard.vue";

interface Props {
  data?: any[];
  currentPage?: number;
  pageSize?: number;
}

const props = withDefaults(defineProps<Props>(), {
  data: () => [],
  currentPage: 1,
  pageSize: 10,
});

const fullData = computed(() => {
  // 增加强制判定，如果不是数组则返回空数组，防止 .slice 崩溃
  return Array.isArray(props.data) ? props.data : [];
});

// 【新增】显式定义插槽类型
const slots = defineSlots<{
  // 这里的名字必须和模板中 <slot name=\"...\"> 的名字完全一致
  "append-columns"(props: { formatWtCode: (code?: string) => string }): any;
  "function-area"(props: {}): any;
}>();

const emit = defineEmits<{
  (e: "update:currentPage", val: number): void;
  (e: "update:pageSize", val: number): void;
  (e: "row-click", row: any): void; // 声明行点击事件给父组件
}>();

defineOptions({
  name: "MiddleTable",
  inheritAttrs: false,
});

// 前端分页切片逻辑
const displayData = computed(() => {
  const data = fullData.value;
  // 如果是树形数据（通常 row-key 存在时），或者是某些特定场景，
  // 简单的 slice 分页会破坏树结构（如果父节点在上一页，子节点在下一页，则无法展开）。
  // 暂时保留切片逻辑，但如果需要树形折叠，必须一次性给 el-table 所有数据，
  // 或者自行实现“树形分页”算法。

  // 检查是否传入了 row-key（作为树形数据的特征之一）
  if (attrs["row-key"]) {
    return data; // 如果是树形表，直接返回全量数据，交给 el-table 自身处理（或者不分页）
  }

  const start = (props.currentPage - 1) * props.pageSize;
  const end = start + props.pageSize;
  return data.slice(start, end);
});

const handleCurrentPageUpdate = (val: number) => emit("update:currentPage", val);
const handlePageSizeUpdate = (val: number) => emit("update:pageSize", val);
const handleRowClick = (row: any) => emit("row-click", row);

/**
 * 格式化函数：依然保留在子组件，但通过插槽暴露给父组件使用
 */
const formatWtCode = (wtcode?: string): string => {
  if (!wtcode) return "-";
  const dotIndex = wtcode.indexOf(".");
  return dotIndex !== -1 ? wtcode.substring(dotIndex + 1) : wtcode;
};

const attrs = useAttrs();
// 2. 移除重复的 hook 调用，直接处理 attrs
const filterOtherAttrs = computed(() => {
  const result = { ...attrs };
  // 这里的删除逻辑已经足够，无需依赖 useTableAttrs 的二次处理
  const toDelete = ["data", "currentPage", "pageSize", "class", "style"];
  toDelete.forEach((key) => delete result[key]);
  return result;
});
</script>

<style scoped>
.middle-card-wrapper {
  flex: 1;
  width: 100%;
  height: 100%;
  display: flex;
  overflow: hidden;
  flex-direction: column;
}

.pagination-container {
  margin-top: 12px;
  margin-right: 12px;
  justify-content: flex-end;
}
</style>
