import os
import re


def normalize_millis(millis_str: str) -> int:
    """
    把 SRT 的毫秒部分（1~3位字符串）标准化为整数毫秒（0-999）。
    e.g. "7"->700? No: "7" means 7ms in SRT usually, but many SRTs use
    7 -> 007 ms or 70 -> 070 ms? Common practice: treat digit count as given:
    '7' -> 7 ms, '70' -> 70 ms, '701' -> 701 ms.
    We'll parse as int then keep as ms.
    """
    s = millis_str.strip()
    # 若为空或非数字，视为 0
    if not s.isdigit():
        return 0
    return int(s)

def time_str_to_centiseconds(time_str: str) -> int:
    """
    将 SRT 时间 'hh:mm:ss,ms' -> 返回总百秒 (centiseconds) （整数）
    使用四舍五入到最接近的百秒。
    """
    # 支持 hh:mm:ss,ms 其中 ms 1~3 位
    m = re.match(r'(\d{2}):(\d{2}):(\d{2}),(\d{1,3})$', time_str.strip())
    if not m:
        raise ValueError(f"Invalid time format: {time_str!r}")
    hh, mm, ss, ms = m.groups()
    h = int(hh); minute = int(mm); second = int(ss)
    ms_int = normalize_millis(ms)  # 0-999
    total_seconds = h * 3600 + minute * 60 + second + ms_int / 1000.0
    # 转为百秒并四舍五入为整数
    total_centis = int(round(total_seconds * 100))
    return total_centis

def centis_to_lrc_tag(total_centis: int) -> str:
    """
    将总百秒转为 LRC 时间标签 [mm:ss.xx]
    注意：LRC 通常使用 mm:ss.xx（分钟:秒.百秒）
    我们把分钟设计为不限位数，但格式化成两位分钟，两位秒和两位百秒。
    """
    minutes = total_centis // 6000  # 6000 centis = 60 seconds
    rem_centis = total_centis % 6000
    seconds = rem_centis // 100
    centis = rem_centis % 100
    return f"[{minutes:02d}:{seconds:02d}.{centis:02d}]"

def srt_block_to_lrc_line(block: str) -> str | None:
    """
    解析单个 SRT block，返回 LRC 行（字符串）或 None（若内容为空）
    block 示例:
      1
      00:00:03,403 --> 00:00:05,70
      Hello world
    """
    lines = [ln for ln in block.splitlines() if ln.strip() != ""]
    if len(lines) < 2:
        return None
    # lines[0] 可能是编号（忽略），lines[1] 是时间行
    time_line = lines[1].strip()
    # 匹配时间行，允许左右有空格以及毫秒1~3位
    m = re.match(r'(\d{2}:\d{2}:\d{2},\d{1,3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{1,3})', time_line)
    if not m:
        return None
    start_str, end_str = m.groups()
    # 组装文本（后续所有行合并为一行）
    text_lines = lines[2:]  # 可能为空
    text = " ".join([ln.strip() for ln in text_lines]).strip()
    if not text:
        return None  # 如果没有实际文本，跳过（不会产出空LRC行）
    # 将开始时间转为 LRC 标签（使用开始时间）
    try:
        start_centis = time_str_to_centiseconds(start_str)
    except ValueError:
        return None
    tag = centis_to_lrc_tag(start_centis)
    # 清理字幕文本中的多余换行符和 HTML 标记
    text = re.sub(r"<[^>]+>", "", text).replace("\n", " ").strip()
    # 返回标签 + 文本
    return f"{tag}{text}"

def srt_to_lrc_text(srt_text: str) -> str:
    """
    把整个 srt 文本转换为 lrc 文本（字符串）。
    """
    # 先统一换行符
    srt_text = srt_text.replace("\r\n", "\n").replace("\r", "\n")
    # 用两个及以上换行分割 block，支持多空行
    blocks = re.split(r'\n\s*\n+', srt_text.strip(), flags=re.MULTILINE)
    lrc_lines = []
    for blk in blocks:
        line = srt_block_to_lrc_line(blk)
        if line:
            lrc_lines.append(line)
    return "\n".join(lrc_lines)

def srt_file_to_lrc_file(srt_path: str, lrc_path: str):
    print(f"🚀 正在处理: {os.path.basename(srt_path)}")
    try:
        with open(srt_path, "r", encoding="utf-8") as f:
            srt_text = f.read()
        lrc_text = srt_to_lrc_text(srt_text)
        with open(lrc_path, "w", encoding="utf-8") as f:
            f.write(lrc_text)

        print(f"✅ 转换完成: {os.path.basename(srt_path)} → {os.path.basename(lrc_path)}")
    except Exception as e:
        #print(f"❌ 转换出错: {e}")
        print("")


def batch_convert_srt_to_lrc(input_dir: str, output_dir: str = None):
    """
    遍历目录批量转换 SRT 为 LRC
    """
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"目录不存在: {input_dir}")

    # 如果没指定输出路径，则保存在同目录下 lrc 文件夹
    if output_dir is None:
        output_dir = os.path.join(input_dir, "audios")

    os.makedirs(output_dir, exist_ok=True)

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(".srt"):
                srt_path = os.path.join(root, file)
                rel_path = os.path.relpath(srt_path, input_dir)
                lrc_path = os.path.join(output_dir, os.path.splitext(rel_path)[0] + ".lrc")

                # 确保输出子目录存在
                os.makedirs(os.path.dirname(lrc_path), exist_ok=True)

                srt_file_to_lrc_file(srt_path, lrc_path)

    print(f"\n🎉 全部转换完成，输出目录: {output_dir}")


if __name__ == "__main__":
    # srt_file_to_lrc_file('/Volumes/WD-4T/Movies/卡通/King of The Hill/S01/101 - Pilot.srt', 'test.lrc')
    # 修改这里为你的 SRT 文件目录
    input_folder = "/Volumes/WD-4T/Movies/卡通/King of The Hill/S05/"
    batch_convert_srt_to_lrc(input_folder)
