import streamlit as st
import yt_dlp
import os

st.title('YouTube视频下载器')

url = st.text_input('请输入YouTube视频链接:')

if url:
    try:
        # 配置yt-dlp选项
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'extract_info': True,
            'nocheckcertificate': True,
            # 添加cookies配置
            'cookiesfrombrowser': ('chrome',),  # 或者使用 'firefox', 'safari', 'edge' 等
        }
        
        # 获取视频信息
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                
                # 显示视频信息
                if 'thumbnail' in info:
                    st.image(info['thumbnail'])
                st.write(f'视频标题: {info.get("title", "未知")}')
                st.write(f'视频时长: {info.get("duration", "未知")} 秒')
                
                # 获取可用的格式
                formats = info.get('formats', [])
                # 过滤出视频格式
                video_formats = [f for f in formats if f.get('vcodec', 'none') != 'none']
                
                if video_formats:
                    # 选择最佳质量的视频
                    best_video = max(video_formats, key=lambda x: x.get('height', 0) or 0)
                    download_url = best_video['url']
                    
                    quality = best_video.get('height', 'unknown')
                    st.write(f'视频质量: {quality}p')
                    st.markdown(f'### [点击这里下载视频]({download_url})')
                    st.write('注意：链接有效期有限，请尽快下载')
                else:
                    st.error('无法获取下载链接')
                    
            except Exception as e:
                st.error(f'获取视频信息失败: {str(e)}')
                
    except Exception as e:
        st.error(f'发生错误: {str(e)}')