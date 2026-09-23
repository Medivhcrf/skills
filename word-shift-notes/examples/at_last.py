# -*- coding: utf-8 -*-
"""内容模块示例：at last / finally / in the end / eventually —— 都译「最后」。

这份文件既是首篇成品的数据源，也是 SKILL.md「内容模块格式」的活例子。
改字段 → 跑 build_shift.py → 出 HTML。所有字段按 HTML 处理。
"""

TITLE = '<span class="en">Free at last!</span> —— 是「终于自由了」还是「最后还是自由了」'
SUB = "at last / finally / in the end / eventually：都译成「最后」，为什么只有 at last 是「终于」"
DATE = "2026-09-23"
SLUG = "at-last"
KICKER = "词义错位 · 英文原义 × 汉语对应词"
META = "释义取自 Vocabulary.com ｜ 词源取自 etymonline"

VERDICT = '首选译法：<b>终于自由了！</b>——不是「最后还是自由了」。'
PUNCH = ('<b>at last ≠ 最后</b>。last 的词根是 <b>late</b>，本义是「最晚、最迟」，'
         '不是序数「最后一名」。所以 at last 的重点是「久等之后可算到了」＝<b>终于</b>。')

SENSES = [
    ("at last",
     "as the end result of a succession or process",
     "synonyms: at long last, finally, in the end, ultimately",
     "只有 1 个义项，<b>没有「排列在最后」这层意思</b>。at last 是感叹，几乎总带情绪。",
     "https://www.vocabulary.com/dictionary/at%20last"),
    ("finally",
     "① as the end result of a succession or process　② after an unspecified period of time "
     "or an especially long delay　③ the item at the end",
     "③ 的同义词：in conclusion, last, lastly",
     "三个词里<b>只有它能在列举时用</b>：Finally, I'd like to thank…。"
     "「最后（一点）」这个义项是 at last 完全没有的。",
     "https://www.vocabulary.com/dictionary/finally"),
    ("eventually",
     "after an unspecified period of time or an especially long delay",
     '释义原文还有一句：<i>“refers to an unspecific time when something will be completed, '
     'and it usually suggests it won\'t be done soon.”</i>',
     "几乎<b>不含情感</b>，常配将来时。多译「最终 / 总有一天」，不要一律译「终于」。",
     "https://www.vocabulary.com/dictionary/eventually"),
    ("in the end",
     "① as the end result of a succession or process　② after a very lengthy period of time",
     "② 的同义词：in the long run",
     "强调「几经周折，到头来」，是总结性、理性口吻，常与 after all 呼应。"
     "<b>汉语「最后还是」对应的是它，不是 at last。</b>",
     "https://www.vocabulary.com/dictionary/in%20the%20end"),
]

ETYM = [
    ("at (the) last",
     "约 <b>1200 年</b>出现 <i>at (the) last</i>；<i>at long last</i> 是 <b>1520s</b>",
     "「在最后（那一刻）」；long 版直接把「漫长的等待」写进了字面"),
    ("last (adj.)",
     "古英语 <b>latost</b>「slowest, latest」，是 <i>læt</i>（late）的<b>最高级</b>",
     "底层语义是「最晚 / 最迟」——<b>不是序数</b>"),
    ("finally",
     "final 约 14c ← 晚期拉丁 <i>finalis</i> ← 拉丁 <b>finis</b>",
     "finis =「边界、界限」→「终点、结束」（finish / fine / finance 同源）"),
    ("eventually",
     "1670s ← eventual（1610s「pertaining to events」）← 拉丁 <b>evenire</b>",
     "evenire =「to come out, happen, result」；"
     "「ultimately resulting」这个义项<b>迟至 1823 年</b>才确立"),
    ("in the end",
     "end ← 古英语 <i>ende</i> ← PIE <i>*antjo</i> ← 词根 <b>*ant-</b>「front, forehead」",
     "原义竟是「the opposite side」（对面那一头），后才引申为「末端、结局」"),
]

ETYM_QUOTE = (
    'last (adj.) c. 1200 — "latest, final, following all others," a contraction of Old English '
    '<b>latost</b> "slowest, latest," <b>superlative of læt</b> "slow, late" … '
    'Phrase <b>at (the) last</b> is from c. 1200; extended form <b>long last</b> is from 1520s.',
    "etymonline · last（2026-09-23 取）",
)

INSIGHT = """
<p><b>错位不在翻译，在概念。</b>英语的 last 是一个「晚」的词，汉语的「最后」是一个「序数」的词。
两者经常重叠，但底层不是一回事——一旦不重叠，译文就偏了。</p>

<div class="box">
  <b>左证一：last night = 昨晚。</b>不是「最后一晚」。<br>
  <b>左证二：the last time I saw her</b> 可能指「我最近一次见她」。
  etymonline 自己都说：<i>“latest would be more correct, but idiom rules.”</i>
</div>

<p>所以 <code>at last</code> 的字面是「<b>到了最晚（不能再晚）的那一刻</b>」，
同时含「晚」和「到了」两件事——正好就是汉语「<b>终于</b>」。
而汉语「最后」天生没有「晚 / 久等」这一层，用它去代 at last 就必然丢掉情绪与时间感。</p>

<div class="box amber">
  <b>为什么这句特别有名：</b><code>Free at last!</code> 出自美国黑人灵歌 <i>Free at Last</i>，
  被马丁·路德·金 1963 年《我有一个梦想》结尾引用
  （<i>Free at last! Free at last! Thank God Almighty, we are free at last!</i>）。
  它是<b>呼喊</b>，不是叙述——这也反过来证明它对应「终于」，不对应「最后还是」。
</div>
"""

DUTY = [
    ("at last",
     "at the last moment of a long wait；情绪性解脱",
     "终于、可算",
     "① 不能用于列举　② 一般用于<b>已发生</b>的事：<i>He will come at last</i> 很别扭"),
    ("finally",
     "三义：结果 / 久等 / 列举末项",
     "终于；最后（一点）",
     "只有它能用于列举，也能写「最后我要说……」"),
    ("in the end",
     "the end result of a process，含「几经周折，到头来」",
     "最后还是、结果",
     "总结性、理性口吻；常与 after all 呼应"),
    ("eventually",
     "at an unspecified later time；释义明说 “won't be done soon”",
     "最终、总有一天、后来",
     "常配将来时；<b>近乎不含情感</b>，所以多译「最终」而非「终于」"),
]

RULES = [
    '见到「最后」先分两种：是<b>「排在末尾」</b>（序数），还是<b>「久等可算到了」</b>（lateness）？'
    '前者用 finally / in the end，后者才是 at last。',
    '查一个词的语义核心，去看它词源里的<b>比较级 / 最高级</b>：'
    'last ← late（最晚），所以它永远带「晚」；汉语对应词没有这层，就必然错位。',
    '词典把几个词互列为同义词，只说明「大意相通」，<b>不说明能互换</b>——'
    '差别在义项数、语域和时态限制上。',
    'at last 只用在「已发生 + 感叹」的场合；谈将来用 eventually / in the end。',
]

FOOTER = ('释义引自 Vocabulary.com（Longman / Oxford / Cambridge 页面有反爬，未能直取）；'
          '词源引自 etymonline。<br>返回 <a href="../index.html">英语学习站</a> · 章节：词义错位')
