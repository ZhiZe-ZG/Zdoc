# Zdoc

Another markup language for note.

## 词汇定义

* `Zdoc` 表示该标记语言。
* `ZdocTool` 表示用于翻译和处理该标记语言的工具软件。

## 目的

用于为 ZhiZe 提供知识管理系统的文件格式基础。

* 表达能力
  * 可用于给自然语言纯文本标记增加格式和样式说明。
  * 可以结构化表达数据，用于内嵌图表和配置信息等。
  * 可以内嵌不经修改或经过简单修改的其他编程语言代码块。
* 语法复杂度
  * 比 XML 更简单。
  * 比 Markdown 更统一和方便扩展。
* 运行环境
  * 渲染后具有交互性和信息更新能力。
  * 代码自动整理。
  * 多文件结构和文件系统访问能力。
  * 内嵌代码块的设定环境运行能力。

## 原则

* 符合 Unicode 标准。
  * 尽量不使用 Unicode 的控制字符控制格式。

## Zdoc 语法

### 字符和编码

基础：

* 允许使用 Unicode 字符。
* 文件使用 UTF 编码。

推荐：

* 文档中不出现如下字符：
  * U+0000~U+0009
  * U+000B~U+001F
  * U+007F~U+009F
* 使用标准的 UTF-8 编码。

### 字符分类

* U+000A 换行
* U+0020 空格 ` `
* U+002E 句点 `.`
* U+0030~U+0039 数字
* U+0041~U+005A 大写字母
* U+005B 左方括号 `[`
* U+005C 反斜杠 `\`
* U+005D 右方括号 `]`
* U+005F 下划线 `_`
* U+0061~U+007A 小写字母
* U+007C 竖线 `|`
* 其他可用字符

### 标识符

* 标识符字母：由句点、数字、大写字母、下划线和小写字母组成。
* 标识符：由一个以上标识符字母组成的序列。

### 标签

标签格式为：

```text
[<标识符>|<内容>]
```

其中 `<标识符>` 可以为空。 `<内容>` 部分则为任意可用字符组成的字符串。但是出现语法字符有可能导致识别失效。需要使用转义字符表示

### 转义字符

转义序列：

* `\\` 表示 `\`
* `\[` 表示 `[`
* `\]` 表示 `]`
* `\|` 表示 `|`

### Zdoc 内容扫描策略

一个字符串中最大覆盖范围的标签模式识别为一个标签。一段字符串中可以有若干个不重叠的标签，其余部分识别为纯文本。

使用 `[|<内容>]` 表示强制纯文本。其他的隐式纯文本都可以视作自动加 `[|<内容>]` 标签。

包含在标签内容部分中的换行直接不处理，作为标签的内容（纯文本标签也算）。

剩余的隐式纯文本先分行，所有的换行识别为 `[br|]` 标签。转换剩下内容分断之后强制转换为强制纯文本。

所以严格的形式之下 `<内容>` 为一系列标签的顺序拼接。

标签的内容依照标签类型继续解析。可嵌套的标签的 `<内容>` 视作一个由纯文本和标签组成的字符串。

### 原子标签

原子标签是不在对 `<内容>` 进行递归分析的标签。包括 `[br|]` 和 `[|<内容>]` 等。

### 内容前后换行

在 `[<标识符>|` 后和 `]` 各有一个可选的换行属于 `<内容>`。这是为了方便源码排版，用统一的格式表示段内和段落格式。

### 换行问题

* 内容前后的换行属于代码格式换行。对于逻辑结构不影响，但是如果直接去除可能造成源码排版格式的缺失。
* 标签之间的换行（ `<内容>` 字符串内部的换行）属于内容换行，是内容的组成部分。

内容前后的换行属于排版用换行。但是纯文本中的换行属于

## 文件格式

* 自由式：可由人书写或阅读，包括一些代码的排版和语法糖
  * 包括 `[br|]` 或括换行符
  * 不包括 `[|]` 但是包括自由文本和 `[text|]` 强制文本
* 严格式：严格化到没有自由文本和换行符（除了一些特殊的原子标签中的换行符以及标签中冗余的内容前后换行）
  * 除了特殊原子标签中的原样换行符
  * 包括 `[br|]` ，不包括换行符
  * 包括 `[|]` 和 `[text|]` 但是不包括自由文本
* 逻辑式：仅仅包括逻辑样式，可以表示为 XML
  * 去除内容前后换行和 `[br|]` 标签
  * `[|]` 替换为 `[text|]`

不再保持 `[|]` 设计，而是所有内容视作一个带标签文段。可以在最外层增加一个 `[zdoc|]`。
但是实际上好像一回事，仍然能够将 `[|]` 引入

考虑使用 `[i|b|Hello world!]` 的语法表示多层嵌套：

```zdoc
[i|
[b|
Hello world!
]
]
```

## 语法糖

* 标签内容前后可以有至多一个换行。
* 自由式文本段。

## 后缀名

* 自由式： `zdoc`
* 严格式： `zdox`
* 逻辑式： `xml`

## To Do

* [ ] 考虑要不要