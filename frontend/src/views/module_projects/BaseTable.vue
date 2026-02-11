<template>
    <!-- 表格区域 -->
    <el-table v-bind="$attrs" >
        <template #empty>
            <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column type="selection" fixed min-width="30" align="center" />
        <el-table-column label="万通码" prop="wtcode" min-width="100" show-overflow-tooltip>
            <template #default="{ row }">
            {{ row.wtcode?.includes('.') ? row.wtcode.slice(row.wtcode.indexOf('.') + 1) : row.wtcode }}
            </template>
        </el-table-column>
        <el-table-column label="代号" prop="code" min-width="130" show-overflow-tooltip></el-table-column>
        <el-table-column label="名称" prop="spec" min-width="130" show-overflow-tooltip></el-table-column>
        <el-table-column label="数量" prop="count" align="center" min-width="40"></el-table-column>
        <el-table-column label="材料" prop="material" min-width="130" show-overflow-tooltip></el-table-column>
        <el-table-column label="单重" prop="unit_mass" align="center" min-width="60"></el-table-column>
        <el-table-column label="总重" prop="total_mass" align="center" min-width="70"></el-table-column>
        <el-table-column label="备注" prop="remark" min-width="100" show-overflow-tooltip></el-table-column>
    </el-table>
</template>

<script setup lang="ts">

// 无需额外脚本，attrs 自动透传

</script>

<style scoped>

</style>
