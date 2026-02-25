<template>
  <div class="base-table-wrapper">
    <el-table
      v-bind="filterTableAttrs"
      class="base-table-content"
      border
      height="100%"
      :header-cell-style="{ textAlign: 'center', backgroundColor: 'var(--el-fill-color-light)' }"
    >
      <template #empty>
        <el-empty :image-size="80" description="暂无数据" />
      </template>
      <slot name="append-columns"></slot>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { computed, useAttrs } from "vue";

defineOptions({
  name: "BaseTable",
  inheritAttrs: false, // 禁止属性自动挂载到根 div 上
});

const attrs = useAttrs();
const filterTableAttrs = computed(() => filterElTableAttrs(attrs));

/**
 * 严格过滤函数：只允许 ElTable 支持的属性和事件通过
 * @param attrs 原始属性对象
 * @returns 过滤后的合法 ElTable 属性对象
 */
function filterElTableAttrs(attrs: Record<string, any>): Record<string, any> {
  // Element Plus el-table 官方属性白名单
  const elTablePropKeys = [
    "data",
    "size",
    "width",
    "height",
    "max-height",
    "fit",
    "stripe",
    "border",
    "row-key",
    "context",
    "show-header",
    "show-summary",
    "sum-text",
    "summary-method",
    "row-class-name",
    "row-style",
    "cell-class-name",
    "cell-style",
    "header-row-class-name",
    "header-row-style",
    "header-cell-class-name",
    "tree-props",
    "default-expand-all",
    "expand-row-keys",
    "default-sort",
    "tooltip-effect",
    "select-on-indeterminante",
    "indent",
    "lazy",
    "load",
    "scrollbar-always-on",
  ];

  return Object.keys(attrs).reduce(
    (acc, key) => {
      // 逻辑：如果在白名单内，或者是以 'on' 开头的事件监听器，则保留
      if (elTablePropKeys.includes(key) || key.startsWith("on")) {
        acc[key] = attrs[key];
      }
      return acc;
    },
    {} as Record<string, any>
  );
}
</script>

<style scoped>
.base-table-wrapper {
  flex: 1;
  width: 100%;
  height: 100%;
  display: flex;
  overflow: hidden;
  flex-direction: column;
}
</style>
