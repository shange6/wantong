<template>
    <el-card class="data-table">
        <!-- 功能区域 -->
        <div class="table-function">
            <slot name="function-area"></slot>
        </div>
        <!-- 表格区域 -->
        <BaseTable v-bind="$attrs"></BaseTable>
        <!-- 分页区域 -->
        <div class="pagination-container">
            <slot name="pagination-area"></slot>
        </div>
    </el-card>
</template>

<script setup lang="ts">
import BaseTable from './BaseTable.vue'; // 引入新组件

</script>

<style scoped>

.pagination-container {
    margin-top: 10px;
    flex-shrink: 0;
    display: flex;
    justify-content: flex-end;
}

.data-table {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden; /* 防止出现双滚动条 */
}

:deep(.el-card__body) {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    padding: 10px;
}

</style>
