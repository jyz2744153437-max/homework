/**
 * WOS 数据解析与指标计算脚本
 *
 * 功能：
 * 1. 解析 WOS Plain Text 格式
 * 2. 计算发文量趋势、h-index、核心作者/机构/期刊
 * 3. 输出统计表格
 */

const fs = require('fs');
const path = require('path');

// === 配置 ===
const DATA_DIR = path.join(__dirname, '..', 'Data');
const OUTPUT_DIR = path.join(__dirname, '..', 'outputs');

// === WOS 解析器 ===

function parseWOSFile(filepath) {
    const content = fs.readFileSync(filepath, 'utf-8');
    const records = [];
    let current = {};

    const lines = content.split('\n');

    for (const line of lines) {
        const trimmed = line.trimEnd();

        // 跳过文件头
        if (trimmed.startsWith('FN ') || trimmed.startsWith('VR ')) {
            continue;
        }

        // 记录结束
        if (trimmed === 'ER') {
            if (Object.keys(current).length > 0) {
                records.push(current);
            }
            current = {};
            continue;
        }

        // 解析字段
        if (trimmed.length >= 3 && trimmed[2] === ' ') {
            const tag = trimmed.substring(0, 2);
            const value = trimmed.substring(3).trim();

            if (current[tag]) {
                // 多值字段
                if (Array.isArray(current[tag])) {
                    current[tag].push(value);
                } else {
                    current[tag] = [current[tag], value];
                }
            } else {
                current[tag] = value;
            }
        } else if (trimmed.startsWith('   ') && Object.keys(current).length > 0) {
            // 续行
            const tags = Object.keys(current);
            const lastTag = tags[tags.length - 1];
            if (Array.isArray(current[lastTag])) {
                current[lastTag][current[lastTag].length - 1] += ' ' + trimmed.trim();
            } else {
                current[lastTag] += ' ' + trimmed.trim();
            }
        }
    }

    return records;
}

function parseAllWOSFiles() {
    const allRecords = [];
    const files = ['download_1-500.txt', 'download_501-643.txt'];

    for (const filename of files) {
        const filepath = path.join(DATA_DIR, filename);
        if (fs.existsSync(filepath)) {
            const records = parseWOSFile(filepath);
            allRecords.push(...records);
            console.log(`解析 ${filename}: ${records.length} 条记录`);
        }
    }

    console.log(`总计: ${allRecords.length} 条记录`);
    return allRecords;
}

// === 指标计算 ===

function calcYearlyPublication(records) {
    const yearCounts = {};

    for (const r of records) {
        const py = r.PY;
        if (py) {
            const year = parseInt(py);
            yearCounts[year] = (yearCounts[year] || 0) + 1;
        }
    }

    return Object.entries(yearCounts)
        .map(([year, count]) => ({ year: parseInt(year), count }))
        .sort((a, b) => a.year - b.year);
}

function calcDocumentTypes(records) {
    const dtCounts = {};

    for (const r of records) {
        const dt = r.DT || 'Unknown';
        dtCounts[dt] = (dtCounts[dt] || 0) + 1;
    }

    return Object.entries(dtCounts)
        .map(([type, count]) => ({ type, count }))
        .sort((a, b) => b.count - a.count);
}

function calcJournalDistribution(records, topN = 20) {
    const journalCounts = {};

    for (const r of records) {
        const so = r.SO;
        if (so) {
            journalCounts[so] = (journalCounts[so] || 0) + 1;
        }
    }

    return Object.entries(journalCounts)
        .map(([journal, count]) => ({ journal, count }))
        .sort((a, b) => b.count - a.count)
        .slice(0, topN);
}

function extractAuthors(record) {
    const au = record.AU;
    if (Array.isArray(au)) {
        return au;
    } else if (au) {
        return au.split(';').map(a => a.trim()).filter(a => a);
    }
    return [];
}

function extractInstitutions(record) {
    const c1 = record.C1;
    const institutions = new Set();

    const text = Array.isArray(c1) ? c1.join(' ') : c1 || '';

    // 匹配机构名 - 提取方括号后的机构部分
    const regex = /\[([^\]]+)\]\s*([^,\[\]]+)/g;
    let match;

    while ((match = regex.exec(text)) !== null) {
        let inst = match[2].trim();
        // 清理
        inst = inst.replace(/\s+/g, ' ');
        // 只保留机构名（到第一个逗号）
        const commaIdx = inst.indexOf(',');
        if (commaIdx > 0) {
            inst = inst.substring(0, commaIdx).trim();
        }
        if (inst.length > 3) {
            institutions.add(inst);
        }
    }

    return Array.from(institutions);
}

function extractCountries(record) {
    const c1 = record.C1;
    const countries = new Set();

    const text = Array.isArray(c1) ? c1.join(' ') : c1 || '';
    const textLower = text.toLowerCase();

    const countryMap = {
        'peoples r china': 'China',
        'p r china': 'China',
        'pr china': 'China',
        'china': 'China',
        'usa': 'USA',
        'united states': 'USA',
        'u s a': 'USA',
        'japan': 'Japan',
        'south korea': 'South Korea',
        'korea': 'South Korea',
        'germany': 'Germany',
        'france': 'France',
        'uk': 'UK',
        'england': 'UK',
        'scotland': 'UK',
        'taiwan': 'Taiwan',
        'hong kong': 'Hong Kong',
        'singapore': 'Singapore',
        'india': 'India',
        'australia': 'Australia',
        'canada': 'Canada',
        'netherlands': 'Netherlands',
        'switzerland': 'Switzerland',
        'italy': 'Italy',
        'spain': 'Spain',
        'brazil': 'Brazil',
        'russia': 'Russia',
        'poland': 'Poland',
        'sweden': 'Sweden',
        'norway': 'Norway',
        'belgium': 'Belgium',
        'austria': 'Austria',
        'denmark': 'Denmark',
        'finland': 'Finland',
        'ireland': 'Ireland'
    };

    for (const [keyword, country] of Object.entries(countryMap)) {
        if (textLower.includes(keyword)) {
            countries.add(country);
        }
    }

    return Array.from(countries);
}

function calcAuthorStats(records, topN = 20) {
    const authorCounts = {};
    const authorCitations = {};

    for (const r of records) {
        const authors = extractAuthors(r);
        const tc = parseInt(r.TC) || 0;

        for (const author of authors) {
            authorCounts[author] = (authorCounts[author] || 0) + 1;
            authorCitations[author] = (authorCitations[author] || 0) + tc;
        }
    }

    const sorted = Object.entries(authorCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, topN);

    return sorted.map(([author, count]) => ({
        author,
        publications: count,
        totalCitations: authorCitations[author] || 0,
        avgCitations: count > 0 ? Math.round((authorCitations[author] || 0) / count * 100) / 100 : 0
    }));
}

function calcInstitutionStats(records, topN = 20) {
    const instCounts = {};

    for (const r of records) {
        const insts = extractInstitutions(r);
        for (const inst of insts) {
            instCounts[inst] = (instCounts[inst] || 0) + 1;
        }
    }

    return Object.entries(instCounts)
        .map(([institution, count]) => ({ institution, count }))
        .sort((a, b) => b.count - a.count)
        .slice(0, topN);
}

function calcCountryStats(records, topN = 15) {
    const countryCounts = {};

    for (const r of records) {
        const countries = extractCountries(r);
        for (const country of countries) {
            countryCounts[country] = (countryCounts[country] || 0) + 1;
        }
    }

    return Object.entries(countryCounts)
        .map(([country, count]) => ({ country, count }))
        .sort((a, b) => b.count - a.count)
        .slice(0, topN);
}

function calcHIndex(records) {
    const citations = records
        .map(r => parseInt(r.TC) || 0)
        .sort((a, b) => b - a);

    let h = 0;
    for (let i = 0; i < citations.length; i++) {
        if (citations[i] >= i + 1) {
            h = i + 1;
        } else {
            break;
        }
    }

    return h;
}

function calcCitationStats(records) {
    const citations = records.map(r => parseInt(r.TC) || 0);
    const n = citations.length;

    if (n === 0) {
        return { total: 0, mean: 0, median: 0, max: 0, zeroCount: 0, zeroRatio: 0 };
    }

    citations.sort((a, b) => a - b);

    const total = citations.reduce((a, b) => a + b, 0);
    const zeroCount = citations.filter(c => c === 0).length;

    return {
        total,
        mean: Math.round(total / n * 100) / 100,
        median: n % 2 === 1 ? citations[Math.floor(n / 2)] : (citations[n / 2 - 1] + citations[n / 2]) / 2,
        max: citations[n - 1],
        zeroCount,
        zeroRatio: Math.round(zeroCount / n * 1000) / 10
    };
}

function calcKeywordStats(records, topN = 30) {
    const kwCounts = {};

    for (const r of records) {
        // 作者关键词
        const de = Array.isArray(r.DE) ? r.DE.join(';') : r.DE || '';
        // 扩展关键词
        const id = Array.isArray(r.ID) ? r.ID.join(';') : r.ID || '';

        const allKw = (de + ';' + id).split(';');

        for (const kw of allKw) {
            const trimmed = kw.trim();
            if (trimmed) {
                kwCounts[trimmed] = (kwCounts[trimmed] || 0) + 1;
            }
        }
    }

    return Object.entries(kwCounts)
        .map(([keyword, count]) => ({ keyword, count }))
        .sort((a, b) => b.count - a.count)
        .slice(0, topN);
}

// === 报告生成 ===

function generateReport(records) {
    const lines = [];

    lines.push('# 文献计量指标统计报告\n');
    lines.push(`> 分析日期: 2026-05-01`);
    lines.push(`> 总记录数: ${records.length}\n`);

    // 1. 年度发文量
    lines.push('## 1. 年度发文量趋势\n');
    lines.push('| 年份 | 发文量 | 增长率 |');
    lines.push('|---|---|---|');

    const yearly = calcYearlyPublication(records);
    let prevCount = null;

    for (const { year, count } of yearly) {
        let growth = '-';
        if (prevCount !== null && prevCount > 0) {
            const g = ((count - prevCount) / prevCount * 100).toFixed(1);
            growth = count > prevCount ? `+${g}%` : `${g}%`;
        }
        lines.push(`| ${year} | ${count} | ${growth} |`);
        prevCount = count;
    }

    // 2. 文献类型
    lines.push('\n## 2. 文献类型分布\n');
    lines.push('| 类型 | 数量 | 占比 |');
    lines.push('|---|---|---|');

    for (const { type, count } of calcDocumentTypes(records)) {
        const ratio = (count / records.length * 100).toFixed(1);
        lines.push(`| ${type} | ${count} | ${ratio}% |`);
    }

    // 3. 被引统计
    lines.push('\n## 3. 被引统计\n');
    const citeStats = calcCitationStats(records);
    lines.push(`- 总被引次数: ${citeStats.total}`);
    lines.push(`- 篇均被引: ${citeStats.mean}`);
    lines.push(`- 被引中位数: ${citeStats.median}`);
    lines.push(`- 最高被引: ${citeStats.max}`);
    lines.push(`- 零被引文献: ${citeStats.zeroCount} (${citeStats.zeroRatio}%)`);
    lines.push(`- 整体 h-index: ${calcHIndex(records)}`);

    // 4. 核心期刊
    lines.push('\n## 4. 核心期刊 (Top 20)\n');
    lines.push('| 期刊 | 发文量 |');
    lines.push('|---|---|');

    for (const { journal, count } of calcJournalDistribution(records)) {
        lines.push(`| ${journal} | ${count} |`);
    }

    // 5. 核心作者
    lines.push('\n## 5. 核心作者 (Top 20)\n');
    lines.push('| 作者 | 发文量 | 总被引 | 篇均被引 |');
    lines.push('|---|---|---|---|');

    for (const stat of calcAuthorStats(records)) {
        lines.push(`| ${stat.author} | ${stat.publications} | ${stat.totalCitations} | ${stat.avgCitations} |`);
    }

    // 6. 核心机构
    lines.push('\n## 6. 核心机构 (Top 20)\n');
    lines.push('| 机构 | 发文量 |');
    lines.push('|---|---|');

    for (const { institution, count } of calcInstitutionStats(records)) {
        lines.push(`| ${institution} | ${count} |`);
    }

    // 7. 国家分布
    lines.push('\n## 7. 国家/地区分布 (Top 15)\n');
    lines.push('| 国家/地区 | 发文量 |');
    lines.push('|---|---|');

    for (const { country, count } of calcCountryStats(records)) {
        lines.push(`| ${country} | ${count} |`);
    }

    // 8. 高频关键词
    lines.push('\n## 8. 高频关键词 (Top 30)\n');
    lines.push('| 关键词 | 频次 |');
    lines.push('|---|---|');

    for (const { keyword, count } of calcKeywordStats(records)) {
        lines.push(`| ${keyword} | ${count} |`);
    }

    return lines.join('\n');
}

// === 主函数 ===

function main() {
    console.log('='.repeat(50));
    console.log('WOS 文献计量指标计算');
    console.log('='.repeat(50));

    // 解析数据
    const records = parseAllWOSFiles();

    if (records.length === 0) {
        console.log('错误: 未找到数据文件');
        return;
    }

    // 生成报告
    const report = generateReport(records);

    // 保存报告
    if (!fs.existsSync(OUTPUT_DIR)) {
        fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    }

    const outputFile = path.join(OUTPUT_DIR, 'metrics_report.md');
    fs.writeFileSync(outputFile, report, 'utf-8');

    console.log(`\n报告已保存到: ${outputFile}`);

    // 输出到控制台
    console.log('\n' + '='.repeat(50));
    console.log(report);
}

main();
