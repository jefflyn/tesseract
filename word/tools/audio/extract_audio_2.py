import os
import subprocess


def extract_audio_ffmpeg(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in os.listdir(input_folder):
        if file.endswith(".mp4"):
            video_path = os.path.join(input_folder, file)
            audio_path = os.path.join(output_folder, file.replace(".mp4", ".mp3"))

            print(f"🎬 提取音频: {video_path} -> {audio_path}")
            try:
                # -q:a 0 表示最高音质，-map a 只取音频
                command = ["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path]
                subprocess.run(command, check=True)
            except Exception as e:
                print(f"⚠️ 处理 {file} 失败: {e}")

if __name__ == '__main__':
    folder_path = '/Volumes/WD-4T/Movies/卡通/Teenage Mutant Ninja Turtles 2003/TMNT2003-Season 4/'
    # 🔧 使用
    extract_audio_ffmpeg(folder_path, folder_path + "audios")
