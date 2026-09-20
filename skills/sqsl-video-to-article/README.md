# 🎬 SQSL Video To Article (视频素材转图文文章生成引擎)

将本地视频录屏或讲解素材，极速转化为保留第一人称真实口吻、图文严密对齐的高水准 Markdown 文章初稿。

---

## 💡 设计理念：专一与解耦

传统视频转文章脚本常常将「转写」、「提炼」、「排版」和「平台推送」杂糅在一起。
`sqsl-video-to-article` 专注于做好**视频转文章**的核心工作：
1. **音频提取与转写**：本地 whisper-cli 硬件加速转写；
2. **ASR 词典纠错**：专有品牌、人名及黑话词典对齐；
3. **字幕时间戳锚定**：依据 SRT 精准截取高清视频帧并回看检验；
4. **创作者口吻写作**：保留第一人称、口播金句与生动节奏，输出纯净的图文 Markdown。

完成创作后，排版与公众号发布交给专门的排版引擎 [`sqsl-article-to-wechat`](../sqsl-article-to-wechat) 处理。

---

## 🚀 快速使用

### 1. 命令行直接处理视频
```bash
python3 scripts/video_to_article.py "/path/to/my_video.mp4" [output_dir]
```
生成带纠错的 `.srt` 和 `.txt` 字幕文件。

### 2. 精准截取时间戳关键帧
```bash
python3 scripts/video_to_article.py --frame "/path/to/my_video.mp4" 00:01:21 "assets/01_highlight.jpg"
```

### 3. Agent 交互模式
直接在 Agent 中输入：
```text
/sqsl-video-to-article 把这个录屏视频整理成一篇图文文章：demo.mp4
```
Agent 会自动完成字幕转写、词典纠错、逐个亮点抽帧、撰写 Markdown，并在完成后提示你使用 `/sqsl-article-to-wechat` 一键排版。
