<template>
  <el-descriptions :column="5" border class="components-info">
    <el-descriptions-item
      label="万通码"
      :span="4"
      label-class-name="item-label"
      class-name="item-content"
    >
      <el-text type="primary" bold>{{ data?.wtcode || "-" }}</el-text>
    </el-descriptions-item>
    <el-descriptions-item label="数量" label-class-name="item-label" class-name="item-content narrow-col">
      <el-text type="primary" bold>{{ data?.count ?? "-" }}</el-text>
    </el-descriptions-item>
    <el-descriptions-item
      label="代号"
      :span="4"
      label-class-name="item-label"
      class-name="item-content"
    >
      <el-text type="primary" bold>{{ data?.code || "-" }}</el-text>
    </el-descriptions-item>
    <el-descriptions-item label="材料" label-class-name="item-label" class-name="item-content narrow-col">
      <el-text type="primary" bold>{{ data?.material || "-" }}</el-text>
    </el-descriptions-item>
    <el-descriptions-item
      label="名称"
      :span="4"
      label-class-name="item-label"
      class-name="item-content"
    >
      <el-text type="primary" bold>{{ data?.spec || "-" }}</el-text>
    </el-descriptions-item>
    <el-descriptions-item label="单重" label-class-name="item-label" class-name="item-content narrow-col">
      <el-text type="primary" bold>{{ data?.unit_mass ?? "-" }}</el-text>
    </el-descriptions-item>
    <el-descriptions-item
      label="备注"
      :span="4"
      label-class-name="item-label"
      class-name="item-content"
    >
      <el-text type="primary" bold>{{ data?.remark || "-" }}</el-text>
    </el-descriptions-item>
    <el-descriptions-item label="总重" label-class-name="item-label" class-name="item-content narrow-col">
      <el-text type="primary" bold>{{ data?.total_mass ?? "-" }}</el-text>
    </el-descriptions-item>
  </el-descriptions>
</template>

<script setup lang="ts">
defineProps<{
  data: any;
}>();
</script>

<style scoped>
/* 强制固定布局，打破浏览器的“自适应”计算，确保比例绝对恒定 */
:deep(.el-descriptions__body table) {
  table-layout: fixed !important;
  width: 100% !important;
}

:deep(.item-label) {
  width: 70px !important;
  text-align: right !important;
}

:deep(.narrow-col) {
  width: 120px !important; /* 强制锁定右侧数值列的宽度，不再随内容长短而变 */
}
</style>
