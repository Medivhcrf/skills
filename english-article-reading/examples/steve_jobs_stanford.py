# -*- coding: utf-8 -*-
"""示例内容模块：Steve Jobs 2005 斯坦福大学毕业典礼演讲。

用法:
    python3 build_article.py examples/steve_jobs_stanford.py /tmp/out.html
"""
import data_a, data_b, data_c, data_d

TITLE = 'Stay Hungry. Stay Foolish.'
SUB = 'Steve Jobs · 2005 斯坦福大学毕业典礼演讲 · 2005.6.12'
DATE = '2026 年 9 月 22 日'
BACKGROUND = '2005 年 6 月 12 日，史蒂夫·乔布斯（Steve Jobs）在斯坦福大学第 114 届毕业典礼上发表这篇演讲。此前一年他刚被诊断出胰腺癌（后证实可手术治愈），因此三个故事谈的正是他一生最重要的三件事：<b>退学与书法课</b>（connecting the dots）、<b>被苹果解雇与东山再起</b>（love and loss）、<b>面对死亡</b>（death）。<br>\n全篇语言<b>极简、口语化</b>，却用“把点连起来”“砖头敲头”“死亡是生命最好的发明”等比喻层层推进；反复出现的祈使句（<span class="refrain settle">Don\'t settle</span>、<span class="refrain hungry">Stay Hungry. Stay Foolish.</span>）构成节奏，结尾两句成为英语世界最著名的祝词之一。它也是“如何用三个故事讲清一生”的教科书范本。'
TIPS_INTRO = '乔布斯的演讲像“讲给朋友听的故事”，不是背诵稿：<b>语速中等偏慢</b>，短句多、停顿多，缩略形式密集；三段故事各有一个情绪转折，讲完一个故事会明显“落定”再进入下一个。建议按以下步骤练：'
FOOTER = 'Stay Hungry. Stay Foolish. · Steve Jobs 2005 Stanford ｜ 全文精读 + 词源 + 修辞 + 跟读 ｜ 👋'

EXTRA_CSS = """
  .refrain.hungry { background:#fde68a; color:#78350f; }
  .refrain.settle { background:#fecaca; color:#7f1d1d; }
  .refrain.dots   { background:#bfdbfe; color:#1e40af; }
"""

PARAS = data_a.PARAS + data_b.PARAS + data_c.PARAS + data_d.PARAS

VOCAB = [('①', 'honored', '/ˈɒnəd/', '拉丁 <b>honor</b>「荣誉、尊敬」', "感到荣幸（I'm honored to… 正式场合的谦敬开场）"),
 ('②', 'commencement', '/kəˈmensmənt/', '拉丁 <b>com-</b>「一起」+ <b>initiare</b>「开始」→「共同开启」', '毕业典礼——学业告一段落、人生新阶段“开始”'),
 ('③', 'naively', '/naɪˈiːvli/', '拉丁 <b>nativus</b>「天生的、自然的」（与 native 同族）→ 未谙世事', '天真地——选了和斯坦福一样贵的学校，事后看很傻'),
 ('④', 'tuition', '/tjuˈɪʃn/', '拉丁 <b>tueri</b>「看护、保护」→ 原指“监护之责”', '学费——父母把一生积蓄都花在这上面'),
 ('⑤', 'intuition', '/ˌɪntjuˈɪʃn/', '拉丁 <b>in-</b>「向内」+ <b>tueri</b>「看」→「内在的注视」', '直觉——不靠推理、内心直接给出的判断'),
 ('⑥', 'calligraphy', '/kəˈlɪɡrəfi/', '希腊 <b>kallos</b>「美」+ <b>graphein</b>「写」→「美的书写」', '书法——里德学院那门改变 Mac 字体的课'),
 ('⑦', 'serif', '/ˈserɪf/', '荷兰语 <b>schreef</b>「一笔、刻线」', '衬线——字母笔画末端的装饰短线（sans-serif 即“无衬线”）'),
 ('⑧', 'typography', '/taɪˈpɒɡrəfi/', '希腊 <b>typos</b>「印记、字形」+ <b>graphein</b>「写」', '排版——Mac 首创的优美字体排印'),
 ('⑨', 'destiny', '/ˈdestəni/', '拉丁 <b>destinare</b>「固定、确定」→ 早已定下的事', '命运——“相信点什么：直觉、命运、人生、因果”'),
 ('⑩', 'karma', '/ˈkɑːmə/', '梵语 <b>karman</b>「行为、业」', '因果、业力——乔布斯列举的“可信仰之物”之一'),
 ('⑪', 'entrepreneur', '/ˌɒntrəprəˈnɜː/', '法语 <b>entreprendre</b>「承担、着手去做」', '企业家——敢于扛起风险去开创的人'),
 ('⑫', 'baton', '/ˈbætɒn/', '法语 <b>bâton</b>「棍、杖」', '接力棒——“我觉得自己把传给下一代企业家的接力棒掉了”'),
 ('⑬', 'devastating', '/ˈdevəsteɪtɪŋ/', '拉丁 <b>de-</b>「彻底」+ <b>vastare</b>「使荒芜」', '毁灭性的——被自己创办的公司开除时的心情'),
 ('⑭', 'renaissance', '/rɪˈneɪsns/', '法语 <b>re-</b>「再」+ <b>naissance</b>「出生」→「重生」', '复兴——NeXT 技术成为苹果重生的核心'),
 ('⑮', 'dogma', '/ˈdɒɡmə/', '希腊 <b>dogma</b>「意见、信条」', '教条——“别被教条困住，那是别人思考的结论”'),
 ('⑯', 'endoscope', '/ˈendəskəʊp/', '希腊 <b>endon</b>「内」+ <b>skopein</b>「看」', '内窥镜——从喉咙伸入体内取活检的管子'),
 ('⑰', 'pancreas', '/ˈpæŋkriəs/', '希腊 <b>pan</b>「全」+ <b>kreas</b>「肉」→「全肉之腺」', '胰腺——他被查出肿瘤的器官'),
 ('⑱', 'biopsy', '/ˈbaɪɒpsi/', '希腊 <b>bios</b>「生命」+ <b>opsis</b>「看」', '活检——取活体组织检验'),
 ('⑲', 'sedated', '/sɪˈdeɪtɪd/', '拉丁 <b>sedare</b>「使平静、安抚」', '被镇静的——做内窥镜时的麻醉状态'),
 ('⑳', 'incurable', '/ɪnˈkjʊərəbl/', '拉丁 <b>in-</b>「不」+ <b>curare</b>「治疗、关心」', '无法治愈的——医生最初的判断'),
 ('㉑', 'intellectual', '/ˌɪntəˈlektʃuəl/', '拉丁 <b>inter-</b>「之间」+ <b>legere</b>「挑选、读」→「在万物间挑选辨别的能力」', '智力的——“死亡从纯粹概念变成切身体会”'),
 ('㉒', 'idealistic', '/ˌaɪdiəˈlɪstɪk/', '希腊 <b>idea</b>「形象、理念」', '理想主义的——《全球概览》的气质'),
 ('㉓', 'adventurous', '/ədˈventʃərəs/', '拉丁 <b>ad-</b>「向」+ <b>venire</b>「来」→「迎向将要到来之事」', '爱冒险的——“如果你够胆，就会在乡间小路搭车”'),
 ('㉔', 'farewell', '/ˌfeəˈwel/', '中古英语 <b>fare</b>「行、走」+ <b>well</b>「好」→「走好」', '告别——《全球概览》停刊时的临别寄语')]

RHET = [('1',
  '三段式与“三”的魔力 Rule of Three',
  '🗣 <b>整篇的骨架就是“三”。</b>开篇即宣告 “I want to tell you <b>three stories</b>”，随后三段故事各自用一句话点题（<i>connecting the dots / love and loss / '
  'death</i>）。英语修辞里，三个并列项最稳、最好记，金句也常成三：<span class="refrain settle">Don\'t settle</span> 反复三次；<span class="refrain hungry">Stay Hungry. '
  'Stay Foolish.</span> 结尾连说两遍。<b>三，是这篇演讲的节拍器。</b>',
  '朗读时把每个“三”的最后一项放慢、压低，制造落定感。'),
 ('2',
  '反复与排比 Anaphora / Repetition',
  '🔁 乔布斯靠<b>重复句式</b>攒力量：<br>· “You have to <b>trust</b> that the dots will somehow connect… You have to <b>trust</b> in something…”<br>· '
  "“<b>If I had never</b> dropped in… <b>If I had never</b> dropped out…”<br>· “<b>Don't</b> waste it… <b>Don't</b> be trapped… "
  "<b>Don't</b> let the noise…”（连用三个祈使否定）<br>· “It means to… <b>It means to</b>… <b>It means to</b>…”（解释 “prepare to die”）",
  '把每轮重复念得比上一轮更重、更慢，最后一次几乎是“砸”下来。'),
 ('3',
  '隐喻 Metaphor（贯穿全篇的意象）',
  '🖼 乔布斯把抽象的人生讲成看得见的画面：<br>· <b>connecting the dots</b>（把点连起来）——过去无法预知、回头看才成图；<br>· <b>hit you in the head with a '
  'brick</b>（拿砖头敲你脑袋）——生活的重击；<br>· <b>awful tasting medicine</b>（难吃的药）——被开除虽苦却是必需；<br>· <b>dropped the baton</b>（掉了接力棒）——辜负上一代企业家；<br>· '
  "<b>Death is … Life's change agent</b>（死亡是生命的“变革代理人”）——清除旧物、给新生让路。",
  '念到隐喻词（dots / brick / medicine / baton）时放慢加重，让画面先成型。'),
 ('4',
  '对偶 Antithesis',
  '⚖️ 成对的反义并置，张力拉满：<br>· “the <b>heaviness</b> of being successful was replaced by the <b>lightness</b> of being a beginner”（成功之重 ↔ '
  '新手之轻）<br>· “Death is very likely the single <b>best invention</b> of Life”（死亡 ↔ 生命）<br>· “<b>Stay Hungry. Stay Foolish.</b>”（饥饿 ↔ '
  '愚直，两个祈使句对举成联）',
  '对比的两端都重读，中间稍停，让落差听得出来。'),
 ('5',
  '引喻与递进收束 Allusion & Climax',
  '📖 乔布斯用三处“引用”把个人故事接到更大的传统上：17 岁读到的那句 <i>“If you live each day as if it was your last…”</i>、少年时代的《全球概览》(The Whole Earth '
  'Catalog)、以及它停刊时印在封底的临别语 <span class="refrain hungry">Stay Hungry. Stay Foolish.</span>。<br>结尾由“我”转向“你们”：<i>And now, as you graduate to '
  'begin anew, I wish that for you</i>——把祝福递到听众手里，全篇情绪在此登顶。',
  '最后两句当作全篇最高音，逐句升高、放慢，然后干脆收住。')]

TIPS = [('① 先听再跟', '先完整听一遍原声（约 15 分钟），标出每段故事的一句话主题和情绪转折点。'),
 ('② 口语化不等于随便', "乔布斯大量用缩略（I'm / don't / you've）和短句，跟读时保持“说话”的松弛感，不要念成朗读腔。"),
 ('③ 三连句练节奏', "把 “Don't waste it… Don't be trapped… Don't let the noise…” 和 “It means to…” 各念 5 遍，一次比一次更重。"),
 ('④ 长句切意群',
  "如 “Remembering that I'll be dead soon / is the most important tool / I've ever encountered / to help me make the big choices in life.” "
  '按斜线停顿换气。'),
 ('⑤ 讲故事的语气', '三段故事用“讲给朋友听”的语调：设置悬念处稍停，抖出结论时降调落定（如 “And then I got fired.”）。'),
 ('⑥ 结尾飙高', '“Stay Hungry. Stay Foolish.” 连说两遍，第二遍更慢更重；“Thank you all very much.” 干脆收尾。')]

QUOTES = [('A',
  "You've got to find what you love. … If you haven't found it yet, keep looking — and don't settle.",
  '💎 全篇最被传诵的劝勉：把“爱”当作职业选择的第一原则，末尾 <span class="refrain settle">don\'t settle</span> 三个词收得极重。'),
 ('B', "Your time is limited, so don't waste it living someone else's life.", "💎 短句 + 祈使，直击人心；“living someone else's life” 是极精准的动名词短语。"),
 ('C',
  'Remembering that you are going to die is the best way I know to avoid the trap of thinking you have something to lose. You are already '
  'naked.',
  '💎 用死亡反衬自由：naked（赤条条）与 lose（失去）构成对偶，一句点醒。'),
 ('D', 'The only way to do great work is to love what you do.', '💎 “the only way to … is to …” 是英语里最好用的“唯一途径”句型。'),
 ('E', 'Stay Hungry. Stay Foolish.', '💎 英语演讲最著名的结尾之一：两个祈使句、四个词，对偶 + 反复，念完余音不散。')]

QUIZ_MATCH = [('1. calligraphy', 'a. 希腊「内」+「看」——看进体内'),
 ('2. endoscope', 'b. 希腊「美」+「写」——美的书写'),
 ('3. entrepreneur', 'c. 法语「承担、着手去做」'),
 ('4. renaissance', 'd. 希腊「全」+「肉」——全肉之腺'),
 ('5. pancreas', 'e. 法语「再」+「出生」——重生'),
 ('6. biopsy', 'f. 拉丁「使平静、安抚」'),
 ('7. sedated', 'g. 梵语「行为、业」'),
 ('8. karma', 'h. 希腊「生命」+「看」——看活体组织')]

QUIZ_RHET = ["“Don't waste it… Don't be trapped… Don't let the noise…” —— <b>___</b>",
 '“connecting the dots” —— <b>___</b>',
 '“the heaviness of being successful was replaced by the lightness of being a beginner” —— <b>___</b>',
 '“Stay Hungry. Stay Foolish.” —— <b>___</b> + <b>___</b>',
 '“If I had never dropped in… If I had never dropped out…” —— <b>___</b>']

QUIZ_FILL = ['Your work is going to fill a large part of your life, and the only way to be truly satisfied is to do what you believe is <b>___</b>.',
 "If you haven't found it yet, keep looking — and don't <b>___</b>.",
 'Remembering that you are going to die is the best way I know to avoid the trap of thinking you have something to <b>___</b>.',
 'And now, as you graduate to begin anew, I wish that for you: <b>___</b>. <b>___</b>.']

ANSWERS = ('<span class="atitle">练习一</span>\u30001-b ｜ 2-a ｜ 3-c ｜ 4-e ｜ 5-d ｜ 6-h ｜ 7-f ｜ 8-g<br>\n'
 '<span class="atitle">练习二</span>\u30001 A（排比） ｜ 2 C（隐喻） ｜ 3 B（对偶） ｜ 4 B + A（对偶 + 反复） ｜ 5 A（排比）<br>\n'
 '<span class="atitle">练习三</span>\u30001 great work ｜ 2 settle ｜ 3 lose ｜ 4 Stay Hungry / Stay Foolish')
