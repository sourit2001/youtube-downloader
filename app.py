import streamlit as st
import yt_dlp
from pathlib import Path
import os

# 设置页面标题
st.title('YouTube视频下载器')

# 创建下载文件夹
if not os.path.exists('downloads'):
    os.makedirs('downloads')

# 创建输入框
url = st.text_input('请输入YouTube视频链接:')

if url:
    try:
        # 配置yt-dlp选项
        ydl_opts = {
            'format': 'bv*+ba/b',  # 最佳视频+音频质量
            'merge_output_format': 'mp4',  # 输出MP4格式
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'progress': False,
        }
        
        # 获取视频信息
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
        # 显示视频信息
        st.image(info['thumbnail'])
        st.write(f'视频标题: {info["title"]}')
        st.write(f'视频时长: {info["duration"]} 秒')
        
        # 获取可用的视频格式（确保包含音频）
        formats = []
        for f in info['formats']:
            # 只选择包含视频和���频的格式
            if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                formats.append(f)
        
        format_options = {
            f"{f.get('height', '???')}p ({f.get('ext', '???')}) - {f.get('filesize', 0)/1024/1024:.1f}MB": f 
            for f in formats if f.get('filesize')
        }
        
        if format_options:
            # 创建质量选择下拉框
            selected_format = st.selectbox('选择视频质量:', list(format_options.keys()))
            
            if st.button('开始下载'):
                # 显示进度条
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def progress_hook(d):
                    if d['status'] == 'downloading':
                        total_bytes = d.get('total_bytes')
                        downloaded_bytes = d.get('downloaded_bytes', 0)
                        if total_bytes:
                            percentage = (downloaded_bytes / total_bytes) * 100
                            progress_bar.progress(int(percentage))
                            status_text.text(f'下载进度: {percentage:.1f}%')
                    elif d['status'] == 'finished':
                        status_text.text('正在处理视频...')
                            
                # 设置下载选项
                selected_format_info = format_options[selected_format]
                ydl_opts.update({
                    'format': f"{selected_format_info['format_id']}+bestaudio/best",
                    'progress_hooks': [progress_hook],
                })
                
                # 开始下载
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # 下载完成后显示成功消息
                st.success('下载完成！')
                st.write(f'文件保存在 downloads 文件夹中')
        else:
            st.warning('未找到可用的完整视频格式（包含视频和音频）')
            
    except Exception as e:
        st.error(f'发生错误: {str(e)}') 