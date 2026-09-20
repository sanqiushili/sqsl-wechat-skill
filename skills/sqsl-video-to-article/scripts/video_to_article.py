#!/usr/bin/env python3
"""
video_to_article.py - 视频转写与台词对齐抽帧工具

功能：
1. 提取 16kHz mono WAV 音频
2. 本地 whisper-cli 极速转写（输出带时间戳的 .srt 与 .txt）
3. 依据 references/glossary.json 自动应用常用词与同音字词典纠错 (ASR Post-Processing)
4. 根据台词/时间戳精准提取视频截图帧
"""

import os
import sys
import json
import subprocess
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
GLOSSARY_PATH = SKILL_DIR / "references" / "glossary.json"

DEFAULT_WHISPER_MODELS = [
    os.path.expanduser("~/Library/Application Support/Screen Studio/models/ggml-small.bin"),
    os.path.expanduser("~/.cache/hyperframes/whisper/models/ggml-small.bin"),
    os.path.expanduser("~/whisper-cpp/models/ggml-small.bin"),
]

def load_glossary():
    if not GLOSSARY_PATH.exists():
        return {}
    with open(GLOSSARY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    mapping = {}
    for group, entries in data.items():
        if isinstance(entries, dict):
            mapping.update(entries)
    return mapping

def apply_glossary(text, mapping):
    for wrong, right in mapping.items():
        text = text.replace(wrong, right)
    return text

def extract_audio(video_path, out_wav_path):
    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
        str(out_wav_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def find_whisper_model():
    for p in DEFAULT_WHISPER_MODELS:
        if os.path.exists(p):
            return p
    return None

def transcribe(wav_path, out_prefix):
    model_path = find_whisper_model()
    if not model_path:
        raise FileNotFoundError(
            "未找到本地 ggml whisper 模型，请检查 Screen Studio (~/Library/Application Support/Screen Studio/models/ggml-small.bin) 或 whisper-cpp 路径。"
        )
    
    cmd = [
        "whisper-cli",
        "-m", model_path,
        "-f", str(wav_path),
        "-l", "zh",
        "-osrt", "-otxt",
        "-of", str(out_prefix)
    ]
    subprocess.run(cmd, check=True)
    
    # 词典纠错
    mapping = load_glossary()
    txt_file = f"{out_prefix}.txt"
    srt_file = f"{out_prefix}.srt"
    
    if os.path.exists(txt_file):
        with open(txt_file, "r", encoding="utf-8") as f:
            c = f.read()
        c = apply_glossary(c, mapping)
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(c)
            
    if os.path.exists(srt_file):
        with open(srt_file, "r", encoding="utf-8") as f:
            c = f.read()
        c = apply_glossary(c, mapping)
        with open(srt_file, "w", encoding="utf-8") as f:
            f.write(c)

def extract_frame(video_path, timestamp_str, out_img_path):
    out_img_path = Path(out_img_path)
    out_img_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-ss", timestamp_str,
        "-i", str(video_path),
        "-frames:v", "1", "-q:v", "2",
        str(out_img_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def print_help():
    print("""video_to_article.py - 视频转写与对齐抽帧工具

用法:
  1. 完整处理视频（提取音频 + Whisper转写 + 词典纠错）:
     python3 video_to_article.py <video_path> [output_dir]

  2. 精准截取单帧（依据 SRT 时间戳）:
     python3 video_to_article.py --frame <video_path> <timestamp> <output_image>
     示例: python3 video_to_article.py --frame demo.mp4 00:01:21 assets/feature1.jpg

  3. 仅对音频转写与纠错:
     python3 video_to_article.py --transcribe-only <wav_path> <out_prefix>
""")

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print_help()
        sys.exit(0)
    
    if sys.argv[1] == "--frame":
        if len(sys.argv) < 5:
            print("用法: python3 video_to_article.py --frame <video_path> <timestamp> <output_image>")
            sys.exit(1)
        video_file = Path(sys.argv[2]).resolve()
        timestamp = sys.argv[3]
        out_image = Path(sys.argv[4]).resolve()
        extract_frame(video_file, timestamp, out_image)
        print(f"已抽帧: {out_image} (时间戳: {timestamp})")
        sys.exit(0)
        
    if sys.argv[1] == "--transcribe-only":
        if len(sys.argv) < 4:
            print("用法: python3 video_to_article.py --transcribe-only <wav_path> <out_prefix>")
            sys.exit(1)
        wav_path = Path(sys.argv[2]).resolve()
        out_prefix = sys.argv[3]
        transcribe(wav_path, out_prefix)
        print(f"转写及纠错完成: {out_prefix}.srt / {out_prefix}.txt")
        sys.exit(0)
        
    video_file = Path(sys.argv[1]).resolve()
    if not video_file.exists():
        print(f"错误: 视频文件不存在: {video_file}")
        sys.exit(1)
        
    out_dir = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else video_file.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    
    tmp_wav = out_dir / "temp_audio.wav"
    out_prefix = out_dir / video_file.stem
    
    print(f"1. 提取音频: {tmp_wav}")
    extract_audio(video_file, tmp_wav)
    
    print(f"2. 本地 Whisper 极速转写与词典校正...")
    transcribe(tmp_wav, str(out_prefix))
    
    if tmp_wav.exists():
        tmp_wav.unlink()
        
    print(f"转写及纠错完成！已生成：\n- {out_prefix}.srt\n- {out_prefix}.txt")
