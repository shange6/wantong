<template>
  <div class="base-card-wrapper">
    <el-card class="base-card-container" shadow="never">
      <div v-if="$slots['function-area']" class="table-function">
        <slot name="function-area"></slot>
      </div>

      <BaseTable v-bind="$attrs">
        <template #append-columns="slotProps">
          <slot name="append-columns" v-bind="slotProps || {}"></slot>
        </template>
      </BaseTable>

      <div v-if="$slots['pagination-area']" class="pagination-container">
        <slot name="pagination-area"></slot>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import BaseTable from "./BaseTable.vue";

// 禁用自动属性继承，改为手动 v-bind
defineOptions({
  name: "BaseCard",
  inheritAttrs: false,
});
</script>

<style scoped>
.base-card-wrapper {
  flex: 1;
  width: 100%;
  height: 100%;
  display: flex;
  overflow: hidden;
  flex-direction: column;
}

/* 核心容器：强制撑满父级高度 */
.base-card-container {
  flex: 1;
  width: 100%;
  height: 100%;
  display: flex;
  overflow: hidden;
  flex-direction: column;
}

/* 关键：强制 el-card__body 撑满并使用 flex 布局 */
:deep(.el-card__body) {
  flex: 1;
  height: 100%;
  padding: 12px;
  display: flex;
  overflow: hidden;
  flex-direction: column;
}
</style>
