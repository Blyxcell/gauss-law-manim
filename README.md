# 高斯定理：从电通量到电场计算

一部中文讲解高斯定理的 Manim Community Edition 视频项目，包含原创
ManimCE 动画、12 章中文讲稿、AI 配音生成器和连续配音合成脚本。

## 视频内容

电通量与面积矢量、高斯定理积分形式、点电荷与球对称、球壳、无限长
带电直线、无限带电平面、外部电荷的通量、导体静电平衡、散度定理与
微分形式、引力类比，以及如何按对称性选择高斯面。

视频使用真空中的 SI 制公式；特殊对称性假设和适用条件在讲解中说明。

## 项目文件

- `gauss_law.py`：12 章的 ManimCE 场景和示意图
- `narration.json`：章节标题与中文旁白原稿
- `generate_voice.py`：Edge TTS 普通话 AI 配音生成器
- `render_video.py`：以 1920×1080、30 fps 渲染，并把完整旁白连续合成为音轨
- `audio/`：12 个章节的配音文件
- `Gauss_Law_1080p.mp4`：渲染后的带配音视频

## 生成与渲染

需要 Python 3.10 或更新版本、FFmpeg、ManimCE 0.19 和 Microsoft YaHei、
Cambria Math 字体；不需要额外安装 LaTeX。

```powershell
py -3.10 -m pip install -r requirements.txt
py -3.10 generate_voice.py
py -3.10 render_video.py
```

配音使用 Microsoft Edge TTS 的 `zh-CN-XiaoxiaoNeural`，生成时需联网。
最终视频将 12 个章节音轨按章节顺序拼接成一条连续旁白音轨，避免
Manim 章节转场导致漏音或长时间静音。

## 许可

ManimCE 源码和生成脚本使用 MIT License；原创旁白文本和原创示意图使用
CC BY 4.0。Edge TTS 语音由 Microsoft Edge TTS 服务合成，不属于这两项
原创素材许可的涵盖范围。Manim Community Edition 本身为独立开源项目。
