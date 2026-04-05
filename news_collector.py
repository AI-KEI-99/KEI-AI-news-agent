#!/usr/bin/env python3
"""
AI新闻收集脚本 - 调试版
"""
import sys
import traceback
import os
from datetime import datetime

print("=" * 60)
print(f"📅 脚本开始执行: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"🐍 Python版本: {sys.version}")
print("=" * 60)

# 打印环境变量
print("🔧 环境变量检查:")
print(f"   EMAIL_SENDER: {'✓ 已设置' if os.environ.get('EMAIL_SENDER') else '✗ 未设置'}")
print(f"   EMAIL_PASSWORD: {'✓ 已设置' if os.environ.get('EMAIL_PASSWORD') else '✗ 未设置'}")
print(f"   EMAIL_RECEIVER: {'✓ 已设置' if os.environ.get('EMAIL_RECEIVER') else '✗ 未设置'}")
print("-" * 40)

try:
    # 测试导入模块
    print("📦 导入模块...")
    import feedparser
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    print("✅ 所有模块导入成功")
    
    # 这里是您原有的新闻收集代码
    # 请确保这里不会因为条件判断而提前return或exit
    
    # 示例：简单的测试代码
    print("🧪 执行简单测试...")
    test_sources = [
        {'name': 'OpenAI官方博客', 'url': 'https://openai.com/blog/rss/', 'category': 'AI'},
    ]
    
    for source in test_sources:
        print(f"   🔍 尝试抓取: {source['name']}")
        feed = feedparser.parse(source['url'])
        print(f"     找到 {len(feed.entries)} 条条目")
    
    print("🎉 测试完成！")
    
except Exception as e:
    print(f"❌ 发生错误: {type(e).__name__}")
    print(f"   错误信息: {str(e)}")
    print("🔍 错误堆栈:")
    traceback.print_exc()
    sys.exit(1)

print("=" * 60)
print("✅ 脚本执行完成")
print("=" * 60)
import feedparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

# ========== 配置区域（您可以修改这里）==========
# 邮箱配置（使用QQ邮箱）
EMAIL_SENDER = os.environ.get('EMAIL_SENDER', '393924226@qq.com')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')  # 从GitHub Secrets读取
EMAIL_RECEIVER = os.environ.get('EMAIL_RECEIVER', '393924226@qq.com')
SMTP_SERVER = 'smtp.qq.com'
SMTP_PORT = 465

# 新闻源配置（AI和低空经济）
NEWS_SOURCES = [
    # AI领域
    {'name': 'OpenAI官方博客', 'url': 'https://openai.com/blog/rss/', 'category': 'AI'},
    {'name': '机器之心', 'url': 'https://www.jiqizhixin.com/rss', 'category': 'AI'},
    {'name': '36氪-人工智能', 'url': 'https://www.36kr.com/ai/rss', 'category': 'AI'},
    {'name': '新华网科技', 'url': 'http://www.xinhuanet.com/tech/rss.xml', 'category': 'AI'},
    
    # 低空经济领域
    {'name': '中国经济网-科技', 'url': 'http://rss.ce.cn/rss/keji.xml', 'category': '低空经济'},
    {'name': '无人机网新闻', 'url': 'https://www.youuav.com/feed', 'category': '低空经济'},
    {'name': '中国民航网', 'url': 'http://www.caacnews.com.cn/rss', 'category': '低空经济'},
]

# 关键词过滤（只收集包含这些关键词的新闻）
KEYWORDS = {
    'AI': ['AI', '人工智能', '大模型', '机器学习', '深度学习', 'GPT', '神经网络'],
    '低空经济': ['低空经济', '无人机', 'eVTOL', '航空物流', '空中交通', '垂直起降']
}
# ========== 配置结束 ==========

def fetch_news():
    """抓取新闻 - 增强版，包含错误处理和多个备用源"""
    all_news = []
    print("开始抓取新闻...")

    # 使用多个备用新闻源，提高成功率
    news_sources = [
        # 国际源，通常可访问性更好
        {'name': 'Ars Technica', 'url': 'http://feeds.arstechnica.com/arstechnica/index', 'category': '科技'},
        {'name': 'TechCrunch', 'url': 'https://techcrunch.com/feed/', 'category': '科技'},
        # 低空经济相关（通过科技新闻过滤）
        {'name': 'TechCrunch', 'url': 'https://techcrunch.com/feed/', 'category': '科技'},
        {'name': 'Drone Life', 'url': 'https://dronelife.com/feed/', 'category': '低空经济'},
    ]

    for source in news_sources:
        try:
            print(f"  尝试抓取: {source['name']} - {source['url']}")
            feed = feedparser.parse(source['url'])

            if feed.get('bozo', 0) == 1:  # 检查解析是否异常
                print(f"    ⚠️  RSS解析可能有问题: {feed.get('bozo_exception', '未知错误')}")
                # 即使解析有问题，也继续尝试读取条目
                print(f"    状态码: {feed.get('status', '未知')}")

            item_count = len(feed.entries) if hasattr(feed, 'entries') else 0
            print(f"    找到 {item_count} 条原始条目")

            # 放宽过滤条件，先确保有内容
            for entry in feed.entries[:5]:  # 每个源最多取5条
                title = entry.get('title', '无标题')
                # 简单的关键词过滤（您可以调整这里的关键词）
                ai_keywords = ['AI', 'artificial intelligence', 'Machine Learning', 'drone', '无人机', 'autonomous','LLM', 'GPT', '模型', '算法',  'eVTOL', '空中交通','智能']
                title_lower = title.lower()
                if any(keyword.lower() in title_lower for keyword in ai_keywords):
                    news_item = {
                        'title': title,
                        'link': entry.get('link', '#'),
                        'source': source['name'],
                        'category': source['category'],
                        'published': entry.get('published', entry.get('updated', '未知时间')),
                        'summary': entry.get('summary', entry.get('description', ''))[:150] + '...'
                    }
                    all_news.append(news_item)
                    print(f"    ✅ 添加: {title[:40]}...")

        except Exception as e:
            print(f"    ❌ 抓取失败: {type(e).__name__} - {str(e)}")
            continue  # 一个源失败，继续尝试下一个

    print(f"抓取完成，共找到 {len(all_news)} 条相关新闻。")
    return all_news

def send_test_email():
    """发送一封测试邮件，确认邮件功能正常"""
    try:
        print("准备发送测试邮件...")
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"✅ AI Agent 测试邮件 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER

        html_content = f"""
        <html><body style="font-family: Arial, sans-serif;">
            <h2>🎉 恭喜！您的AI Agent邮件功能测试成功</h2>
            <p>这封邮件证明您的AI Agent已经可以成功连接QQ邮箱并发送邮件。</p>
            <p><strong>发送时间：</strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>下一步：</strong>当前新闻抓取返回0条，请检查新闻源RSS地址，或添加更多新闻源。</p>
            <p>您的工作流运行成功，邮件功能正常，离完全成功只差最后一步！</p>
        </body></html>
        """

        msg.attach(MIMEText(html_content, 'html', 'utf-8'))

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        print("✅ 测试邮件发送成功！请检查您的QQ邮箱（包括垃圾邮件箱）。")
        return True
    except Exception as e:
        print(f"❌ 测试邮件发送失败: {type(e).__name__} - {str(e)}")
        return False
def create_email_content(news_list):
    """根据新闻列表生成HTML邮件内容"""
    if not news_list:
        return "<p>今日未抓取到相关新闻。</p>"

    # 按新闻来源简单分组
    from collections import defaultdict
    news_by_source = defaultdict(list)
    for news in news_list:
        news_by_source[news['source']].append(news)

    # 开始构建HTML
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 700px; margin: auto; padding: 20px; }}
            .header {{ background-color: #f0f8ff; padding: 20px; border-radius: 10px; margin-bottom: 25px; text-align: center; }}
            .news-item {{ border-left: 4px solid #4CAF50; padding: 15px; margin-bottom: 20px; background-color: #f9f9f9; border-radius: 0 8px 8px 0; }}
            .news-title {{ font-size: 18px; font-weight: bold; margin-bottom: 8px; }}
            .news-title a {{ color: #1a73e8; text-decoration: none; }}
            .news-title a:hover {{ text-decoration: underline; }}
            .news-meta {{ color: #666; font-size: 14px; margin-bottom: 10px; }}
            .news-summary {{ color: #444; }}
            .source-section {{ margin-top: 30px; padding-top: 20px; border-top: 1px dashed #ddd; }}
            .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; color: #777; font-size: 12px; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>🚀 AI与低空经济 每日资讯简报</h2>
            <p>📅 {datetime.now().strftime('%Y年%m月%d日')} | 📰 共 {len(news_list)} 条更新</p>
        </div>
    """

    # 为每个来源添加新闻
    for source, items in news_by_source.items():
        html_content += f'<div class="source-section"><h3>📋 来源：{source}</h3>'
        for i, news in enumerate(items, 1):
            html_content += f"""
            <div class="news-item">
                <div class="news-title">{i}. <a href="{news['link']}" target="_blank">{news['title']}</a></div>
                <div class="news-meta">⏰ {news.get('published', '时间未知')}</div>
                <div class="news-summary">{news.get('summary', '暂无摘要')}</div>
            </div>
            """
        html_content += '</div>'

    html_content += """
        <div class="footer">
            <p>本简报由 GitHub Actions 自动生成 | 资讯源自公开 RSS 订阅</p>
            <p>如需调整订阅源或反馈，请访问您的仓库设置。</p>
        </div>
    </body>
    </html>
    """
    return html_content

def send_news_email(subject, html_content):
    """发送正式的新闻邮件"""
    try:
        print(f"正在发送新闻邮件，主题: {subject}")
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print("✅ 新闻邮件发送成功！")
        return True
    except Exception as e:
        print(f"❌ 新闻邮件发送失败: {type(e).__name__} - {e}")
        return False
def main():
    print("=" * 60)
    print("开始执行AI新闻收集任务")
    print("=" * 60)

    # 1. 抓取新闻
    news_list = fetch_news()

    # 2. 根据有无新闻，发送不同类型的邮件
    if news_list and len(news_list) > 0:
        # 生成正式日报
        email_subject = f"AI与低空经济日报 ({datetime.now().strftime('%m-%d')}) - {len(news_list)}条"
        email_content = create_email_content(news_list)  # 现在这个函数已定义，可以调用了
        print(f"📨 准备发送包含 {len(news_list)} 条新闻的正式日报...")
        send_news_email(email_subject, email_content)    # 改为调用正式的发送函数
    else:
        # 如果确实没新闻，可以保留测试邮件或发送一个通知
        print("⚠️ 今日未抓取到相关新闻。")
        # 可以选择不发送邮件，或者发送一个简短通知
        # send_test_email() # 可以注释掉或保留

    print("=" * 60)
    print("任务执行完毕")
    print("=" * 60)

if __name__ == "__main__":
    main()
