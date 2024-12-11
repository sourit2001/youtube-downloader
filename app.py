import streamlit as st
import yt_dlp

def get_download_link(url):
    try:
        ydl_opts = {
            'format': 'best',  # 获取最佳质量
            'extract_info': True,  # 只提取信息
            'quiet': True,
            'no_warnings': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            download_url = info['url']
            return download_url
            
    except Exception as e:
        st.error(f'获取下载链接失败: {str(e)}')
        return None

# 设置页面标题
st.title('YouTube视频下载器')

# 创建输入框
url = st.text_input('请输入YouTube视频链接:')

if url:
    download_url = get_download_link(url)
    if download_url:
        st.markdown(f'[点击这里下载视频]({download_url})')