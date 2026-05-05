#!/usr/bin/env node

/**
 * 可复现分析管道
 *
 * 一键生成所有分析结果：
 *   node run_pipeline.js
 *
 * 功能：
 * 1. 解析 WOS 数据
 * 2. 计算文献计量指标
 * 3. 输出统计报告
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname);

console.log('='.repeat(60));
console.log('Transformer-Semiconductor-Bibliometrics 分析管道');
console.log('='.repeat(60));

// Step 1: 检查数据文件
console.log('\n[Step 1] 检查数据文件...');
const dataDir = path.join(ROOT, 'Data');
const dataFiles = ['download_1-500.txt', 'download_501-643.txt'];
let dataOk = true;

for (const f of dataFiles) {
    const fp = path.join(dataDir, f);
    if (fs.existsSync(fp)) {
        const size = fs.statSync(fp).size;
        console.log(`  ✅ ${f} (${(size / 1024 / 1024).toFixed(1)} MB)`);
    } else {
        console.log(`  ❌ ${f} 不存在`);
        dataOk = false;
    }
}

if (!dataOk) {
    console.log('\n错误: 数据文件缺失，请先从 WOS 导出数据');
    process.exit(1);
}

// Step 2: 运行指标计算
console.log('\n[Step 2] 运行指标计算...');
try {
    execSync('node src/metrics_calculator.js', { cwd: ROOT, stdio: 'inherit' });
    console.log('  ✅ 指标计算完成');
} catch (e) {
    console.log('  ❌ 指标计算失败:', e.message);
}

// Step 3: 检查输出
console.log('\n[Step 3] 检查输出文件...');
const outputDir = path.join(ROOT, 'outputs');
const expectedOutputs = ['metrics_report.md'];

for (const f of expectedOutputs) {
    const fp = path.join(outputDir, f);
    if (fs.existsSync(fp)) {
        console.log(`  ✅ ${f}`);
    } else {
        console.log(`  ❌ ${f} 未生成`);
    }
}

// Step 4: 检查文档完整性
console.log('\n[Step 4] 检查文档完整性...');
const docs = [
    ['Data/field_dictionary.md', '字段字典'],
    ['Data/README.md', '数据说明'],
    ['reports/data_quality.md', '数据质量报告'],
    ['reports/methodology.md', '研究方法论'],
    ['reports/metrics_spec.md', '指标规范'],
    ['reports/screening_rule.md', '筛选规则'],
    ['reports/novelty_search_v0.md', '查新报告'],
    ['reports/prisma_flowchart.md', 'PRISMA 流程图'],
    ['config/query.yaml', '检索式配置'],
    ['docs/data_model.md', '图数据模型'],
    ['docs/project_outline.md', '项目大纲'],
    ['baseline/params.md', 'CiteSpace 参数'],
    ['baseline/tool_selection.md', '工具选型'],
];

for (const [fp, name] of docs) {
    const fullPath = path.join(ROOT, fp);
    if (fs.existsSync(fullPath)) {
        console.log(`  ✅ ${name} (${fp})`);
    } else {
        console.log(`  ❌ ${name} (${fp}) 缺失`);
    }
}

// Step 5: 提示 CiteSpace 操作
console.log('\n[Step 5] 需手动完成的 CiteSpace 分析...');
const citespaceTasks = [
    '共被引网络分析 → 输出共被引图 + 聚类标签表',
    '突现检测 → 输出 Burst 列表',
    '关键词时间线分析 → 输出 Timeline 图',
    '文献耦合分析 → 输出耦合网络图',
    '合作网络分析 → 输出作者/机构合作图',
    '阈值敏感性对照实验',
];

for (const task of citespaceTasks) {
    console.log(`  📋 ${task}`);
}

console.log('\n' + '='.repeat(60));
console.log('管道执行完成！');
console.log('='.repeat(60));
