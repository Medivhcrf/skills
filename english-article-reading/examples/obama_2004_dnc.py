# -*- coding: utf-8 -*-
"""奥巴马 2004 民主党全国大会主题演讲《无畏的希望》——内容模块主文件。

正文数据按段落分在 obama_data_a..d.py（长文分文件，便于维护）。
用法：
    python3 build_article.py examples/obama_2004_dnc.py <输出.html>
"""
import obama_data_a as A
import obama_data_b as B
import obama_data_c as C
import obama_data_d as D

TITLE = "The Audacity of Hope"
SUB = "Barack Obama · 2004 民主党全国大会主题演讲 · 2004.7.27 波士顿"
DATE = "2026 年 9 月 22 日"

BACKGROUND = (
    "2004 年 7 月 27 日，还是伊利诺伊州参议员候选人的<b>巴拉克·奥巴马</b>"
    "在波士顿的民主党全国大会上做主题演讲。此前全国几乎没人认识他；"
    "这一夜之后，他成了美国政治的中心人物——四年后当选总统。"
    "<br><br>"
    "演讲的骨架是一条<b>个人故事线</b>：肯尼亚放羊的祖父、堪萨斯的外祖父母、"
    "跨越两个大洲的父母的梦想。奥巴马用它论证一个命题——"
    "<b>「我的故事只有在这样一个美国才可能发生」</b>，"
    "再由个人故事推到国家叙事：<span class='refrain one'>we are one people</span>。"
    "<br><br>"
    "修辞上，全篇靠<b>排比（anaphora）</b>推进："
    "<span class='refrain gointo'>Go into…</span>、"
    "<span class='refrain thereis'>There's not a … America</span>、"
    "<span class='refrain hopeb'>the hope of …</span>、"
    "<span class='refrain ibelieve'>I believe we can …</span> 四组排比层层加压。"
    "结尾的 <b>the audacity of hope</b>（无畏的希望）借自他的牧师 Jeremiah Wright 的布道词，"
    "后来成了他一本书的书名。"
)

VOCAB = [
    ("①", "gratitude", "/ˈɡrætɪtjuːd/", "拉丁 <b>gratus</b>「令人愉快的、心存感激的」→ gratitudo", "感激——开场第一句就是谢意"),
    ("②", "crossroads", "/ˈkrɒsrəʊdz/", "cross（交叉）+ road（路）；字面「路交叉的地方」", "十字路口——把伊利诺伊定位成全国的枢纽"),
    ("③", "perseverance", "/ˌpɜːsɪˈvɪərəns/", "拉丁 <b>per-</b>「彻底」+ <b>severus</b>「严肃、严格」→ 坚持到底", "坚持不懈——祖父靠它把父亲送出肯尼亚"),
    ("④", "beacon", "/ˈbiːkən/", "古英语 <b>bēacen</b>「信号、记号」→ 灯塔、指路明灯", "灯塔——美国在移民心中的形象"),
    ("⑤", "improbable", "/ɪmˈprɒbəbl/", "拉丁 <b>in-</b>「不」+ <b>probabilis</b>「可证明的」（probare 检验）", "不太可能的——他说「我站在这里本身就不寻常」"),
    ("⑥", "abiding", "/əˈbaɪdɪŋ/", "古英语 <b>ābīdan</b>「停留、等待」（a- + bīdan 等待）", "持久的——父母对美国可能性的信念"),
    ("⑦", "tolerant", "/ˈtɒlərənt/", "拉丁 <b>tolerare</b>「忍受、承担」", "宽容的——「在宽容的美国，你的名字不是障碍」"),
    ("⑧", "barrier", "/ˈbæriə/", "古法语 <b>barriere</b>，源自 <b>barre</b>「横木、栅栏」", "障碍——名字不该成为成功的障碍"),
    ("⑨", "potential", "/pəˈtenʃl/", "拉丁 <b>potentia</b>「力量」，源自 <b>posse</b>「能够」", "潜力——「你不必富有也能实现潜力」"),
    ("⑩", "diversity", "/daɪˈvɜːsəti/", "拉丁 <b>diversitas</b>；<b>divertere</b>「转向不同方向」（dis- 分开 + vertere 转）", "多样性——他为自己的混血出身感恩"),
    ("⑪", "heritage", "/ˈherɪtɪdʒ/", "拉丁 <b>heres</b>「继承人」→ hereditare「继承」", "传承、血统——「我为我的血统感恩」"),
    ("⑫", "affirm", "/əˈfɜːm/", "拉丁 <b>affirmare</b>：ad-「朝向」+ <b>firmus</b>「坚固」→ 使坚固、断言", "确认、重申——今晚聚在一起要确认国家的伟大"),
    ("⑬", "premise", "/ˈpremɪs/", "拉丁 <b>praemissa</b>；<b>praemittere</b>「先送出」（prae- 前 + mittere 送）", "前提——「我们的自豪基于一个很简单的前提」"),
    ("⑭", "self-evident", "/ˌself ˈevɪdənt/", "拉丁 <b>evidens</b>：e-「向外」+ <b>videre</b>「看」→ 一看就明白", "不言自明的——《独立宣言》原话"),
    ("⑮", "inalienable", "/ɪnˈeɪliənəbl/", "拉丁 <b>in-</b>「不」+ <b>alienare</b>「转让」（alienus 他人的）", "不可剥夺的——「不可转让的权利」"),
    ("⑯", "insistence", "/ɪnˈsɪstəns/", "拉丁 <b>insistere</b>：in-「在上」+ <b>sistere</b>「站立」→ 站在上面不走", "坚持——「对微小奇迹的坚持」"),
    ("⑰", "forbearers", "/fɔːˈbeərəz/", "古英语 <b>forberan</b>「忍受」→ 先辈（承受过的人）", "祖先、先辈——「对照先辈留下的遗产」"),
    ("⑱", "retribution", "/ˌretrɪˈbjuːʃn/", "拉丁 <b>retribuere</b>：re-「回」+ <b>tribuere</b>「给予」→ 回报、报应", "报复——「不必害怕投票被报复」"),
    ("⑲", "eradicate", "/ɪˈrædɪkeɪt/", "拉丁 <b>eradicare</b>：e-「出」+ <b>radix</b>「根」→ 连根拔起", "根除——「根除『读书的黑人孩子在装白人』这种诽谤」"),
    ("⑳", "slander", "/ˈslɑːndə/", "古法语 <b>esclandre</b>，拉丁 <b>scandalum</b>「绊脚石、丑闻」", "诽谤、中伤——上文那个「读书=装白人」的偏见"),
    ("㉑", "solemn", "/ˈsɒləm/", "拉丁 <b>sollemnis</b>「每年举行的（宗教仪式）」→ 庄严的", "庄严的——「我们负有庄严的义务」"),
    ("㉒", "obligation", "/ˌɒblɪˈɡeɪʃn/", "拉丁 <b>obligatio</b>：ob-「朝向」+ <b>ligare</b>「绑」→ 被绑住的责任", "义务——对待参战军人的责任"),
    ("㉓", "allegiance", "/əˈliːdʒəns/", "古法语 <b>lige</b>「臣属的」→ ligeance「对领主的效忠」", "效忠——「我们都向星条旗宣誓效忠」"),
    ("㉔", "cynicism", "/ˈsɪnɪsɪzəm/", "希腊 <b>kynikos</b>「像狗的」，kynon「狗」——犬儒学派", "愤世嫉俗——「玩世不恭的政治 vs 希望的政治」"),
    ("㉕", "audacity", "/ɔːˈdæsəti/", "拉丁 <b>audacia</b>；<b>audere</b>「敢于」→ 大胆、无畏", "无畏、大胆——全篇的题眼 the audacity of hope"),
]

RHET = [
    ("1", "排比 Anaphora",
     "同一句式连续出现，是本篇最主要的推进器。四处最典型："
     "<br>① <span class='refrain gointo'>Go into</span> the collar counties… / "
     "<span class='refrain gointo'>Go into</span> any inner city neighborhood…"
     "<br>② <span class='refrain thereis'>There's not a</span> liberal America and a conservative America — "
     "there is the United States of America. / <span class='refrain thereis'>There's not a</span> black America and white America…"
     "<br>③ <span class='refrain hopeb'>the hope of</span> slaves… / immigrants… / a young naval lieutenant… / a mill worker's son… / a skinny kid…"
     "<br>④ <span class='refrain ibelieve'>I believe we can</span>… ×3"
     "<br>排比把「列举」变成「加压」：每重复一次，论点就重一分。",
     "朗读时把重复的那几个词<b>读得一样重、一样快</b>，只在每句的<b>新内容</b>上做重音，"
     "四组排比之间要换气、稍停，让听众意识到「又来了」。"),
    ("2", "对偶 Antithesis",
     "把两个对立项并排，用否定—肯定的结构一举否定对方的框架："
     "<br>· There's <b>not</b> a liberal America and a conservative America — "
     "<b>there is</b> the United States of America."
     "<br>· not because of the height of our skyscrapers, or the power of our military, or the size of our economy"
     "（三个「不是因为」，最后才给「而是因为」）"
     "<br>· war must be an option sometimes, but it should never be the first option"
     "<br>对偶的力量在于：它不给中间地带，逼听众选边。",
     "破折号 `—` 前要<b>降调收住</b>，破折号后换一口气、<b>提调起句</b>；"
     "「not…」那半句语速可稍快，「there is…」那半句放慢加重。"),
    ("3", "引喻 Allusion",
     "全篇嵌了三处美国人都认得的经典："
     "<br>· <b>We hold these truths to be self-evident…</b> —— 《独立宣言》原文，用来给「平等」找最高依据；"
     "<br>· <b>E pluribus unum</b>（Out of many, one）—— 国徽上的拉丁格言，正好承接「一个美国」的主题；"
     "<br>· <b>I am my brother's keeper</b> —— 《创世记》该隐的回答，把政治命题提到伦理/信仰层面。"
     "<br>引喻的作用是<b>借权威</b>：不用论证，听众自然接受。",
     "引文部分要读得<b>略慢、略庄重</b>，与前后口语化的句子拉开距离；"
     "`E pluribus unum` 是拉丁语，读完立刻自己翻译一遍（Out of many, one）。"),
    ("4", "隐喻 Metaphor",
     "全篇用一组「道路 / 光」的意象贯穿："
     "<br>· <b>crossroads of a nation</b>（十字路口）——开篇定调，暗示选择；"
     "<br>· a <b>beacon</b> of freedom（自由的灯塔）——移民眼中的美国；"
     "<br>· a <b>righteous wind at our backs</b>（背后有正义之风）——把历史趋势写成物理推力；"
     "<br>· out of this long political <b>darkness</b> a brighter <b>day</b> will come——结尾用光收束。"
     "<br>从「路口」到「灯塔」再到「天亮」，空间意象一路递进，情绪也一路往上。",
     "读意象词时不要停顿解释，让画面自己过去；结尾 darkness / brighter day 要形成"
     "<b>低—高</b>的语调对比。"),
    ("5", "重复 Repetition（情感锚点）",
     "`I stand here…`（两次）、`Let me be clear. Let me be clear.`（连说两次）、"
     "`it is that fundamental belief`（连说两次）——"
     "这类原地重复不是修辞技巧，而是<b>给掌声留时间、给情绪留台阶</b>。",
     "连说两次的地方，第二遍要比第一遍<b>更慢、更重</b>，中间留半拍；"
     "不要读成结巴，要读成果断。"),
]

TIPS_INTRO = (
    "这篇演讲的口语性很强，但排比段极密。跟读的关键不是模仿口音，"
    "而是<b>学会用排比换气</b>——把每一组排比当成一个呼吸单元，而不是一句一句读。"
)

TIPS = [
    ("① 先听再跟", "第一遍只听不动嘴，标出四组排比的位置（Go into / There's not a / the hope of / I believe）。"),
    ("② 排比读成「一组」", "同一组里的各句节奏要一致：重复词轻快带过，新内容加重。整组读完再停顿。"),
    ("③ 破折号是换气点", "`— there is the United States of America` 前深吸一口气，破折号后提调起句。"),
    ("④ 长句找主干", "`When we send our young men and women into harm's way, we have a solemn obligation not to fudge the numbers…` —— 先抓 has an obligation，其余都是往右挂的补充。"),
    ("⑤ 引文放慢", "读到《独立宣言》引语、E pluribus unum 时降速，与前后的口语句子拉开层次。"),
    ("⑥ 结尾三连降调", "`reclaim its promise` / `a brighter day will come` —— 结尾句用降调收，最后 Thank you 轻收。"),
]

QUOTES = [
    ("A", "There's not a liberal America and a conservative America — there is the United States of America.",
     "全篇最著名的一句。用<b>对偶</b>一次性否定「红州蓝州」的分类框架："
     "前半句连说两个「不是」，破折号后只给一个「是」。值得整句背下来，"
     "可以套用到任何「不要用标签把人分开」的场合。"),
    ("B", "We are one people, all of us pledging allegiance to the stars and stripes, all of us defending the United States of America.",
     "排比的收束句。`all of us…, all of us…` 两个并列短语把「one people」落到实处。"
     "注意 pledge allegiance to 是固定搭配（向…宣誓效忠），宾语常是 flag / country。"),
    ("C", "Hope in the face of difficulty, hope in the face of uncertainty, the audacity of hope.",
     "三连递进：前两个是「在…之中的希望」，第三个直接换成名词短语 <b>the audacity of hope</b>，"
     "把「希望」升级成「无畏」。in the face of 是高频搭配（面对…）。"),
    ("D", "I am my brother's keeper, I am my sister's keeper.",
     "引《创世记》该隐之问的回答，把「我们彼此相连」从政治命题提到伦理层面。"
     "连说两次（brother / sister）扩大覆盖面，念时要慢、要重。"),
    ("E", "Out of this long political darkness a brighter day will come.",
     "结尾句。`Out of …` 置于句首的介词短语制造悬念，darkness 与 brighter day 形成明暗对偶。"
     "适合背下来做「困难之后会好起来」的表达模板。"),
]

QUIZ_MATCH = [
    ("1. gratitude", "a. 忍受、承担（拉丁 tolerare）"),
    ("2. perseverance", "b. 根（拉丁 radix）"),
    ("3. tolerant", "c. 敢于（拉丁 audere）"),
    ("4. eradicate", "d. 令人愉快的、心存感激的（拉丁 gratus）"),
    ("5. audacity", "e. 彻底 + 严肃（拉丁 per- + severus）"),
    ("6. allegiance", "f. 他人的（拉丁 alienus）"),
    ("7. inalienable", "g. 臣属的（古法语 lige）"),
    ("8. slander", "h. 绊脚石、丑闻（拉丁 scandalum）"),
]

QUIZ_BANK = ("A. 排比 anaphora ｜ B. 对偶 antithesis ｜ C. 隐喻 metaphor ｜ "
             "D. 引喻 allusion ｜ E. 重复 repetition")

QUIZ_RHET = [
    "There's not a liberal America and a conservative America — there is the United States of America. —— <b>___</b>",
    "Go into the collar counties around Chicago… Go into any inner city neighborhood… —— <b>___</b>",
    "the hope of slaves sitting around a fire… the hope of immigrants setting out for distant shores… —— <b>___</b>",
    "We hold these truths to be self-evident, that all men are created equal. —— <b>___</b>",
    "a righteous wind at our backs；out of this long political darkness a brighter day will come —— <b>___</b>",
]

QUIZ_FILL = [
    "There's not a liberal America and a conservative America — there is the <b>___</b> of America.",
    "We are one people, all of us pledging <b>___</b> to the stars and stripes.",
    "Hope in the face of difficulty, hope in the face of uncertainty, the <b>___</b> of hope.",
    "I am my brother's <b>___</b>, I am my sister's keeper.",
    "Out of this long political darkness a <b>___</b> day will come.",
]

ANSWERS = (
    "<b>练习一 · 词源连线</b>　1-d　2-e　3-a　4-b　5-c　6-g　7-f　8-h<br>"
    "<b>练习二 · 修辞辨识</b>　1. B 对偶　2. A 排比　3. A 排比　4. D 引喻　5. C 隐喻<br>"
    "<b>练习三 · 名句填空</b>　1. United States　2. allegiance　"
    "3. audacity　4. keeper　5. brighter"
)

# 四个分文件拼成完整正文（段号在各自文件里连续）
PARAS = A.PARAS + B.PARAS + C.PARAS + D.PARAS

# 本篇新增的排比高亮配色（模板自带的 7 个不够用，这里补 5 个）
EXTRA_CSS = """
  .refrain.one { background: #fecaca; color: #7f1d1d; }
  .refrain.gointo { background: #fed7aa; color: #7c2d12; }
  .refrain.thereis { background: #ddd6fe; color: #4c1d95; }
  .refrain.hopeb { background: #bae6fd; color: #075985; }
  .refrain.ibelieve { background: #bbf7d0; color: #14532d; }
"""
