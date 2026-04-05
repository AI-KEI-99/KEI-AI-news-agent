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
    """抓取新闻"""
    all_news = []
    
    for source in NEWS_SOURCES:
        try:
            feed = feedparser.parse(source['url'])
            print(f"正在抓取: {source['name']} ({len(feed.entries)}条)")
            
            for entry in feed.entries[:5]:  # 每个源取最新5条
                # 检查是否包含关键词
                title = entry.get('title', '')
                summary = entry.get('summary', '')
                content = f"{title} {summary}".lower()
                
                # 根据分类检查关键词
                keywords = KEYWORDS.get(source['category'], [])
                has_keyword = any(keyword.lower() in content for keyword in keywords)
                
                if has_keyword:
                    news_item = {
                        'title': title,
                        'link': entry.get('link', '#'),
                        'source': source['name'],
                        'category': source['category'],
                        'published': entry.get('published', '未知时间'),
                        'summary': summary[:200] + '...' if len(summary) > 200 else summary
                    }
                    all_news.append(news_item)
        except Exception as e:
            print(f"抓取失败 {source['name']}: {e}")
    
    return all_news
def fetch_news():
    """抓取新闻"""
    all_news = []
    
    for source in NEWS_SOURCES:
        try:
            print(f"\n🔍 开始抓取: {source['name']}")
            print(f"   URL: {source['url']}")
            
            feed = feedparser.parse(source['url'])
            
            # 打印RSS解析结果
            print(f"   解析结果: {len(feed.entries)} 条条目")
            print(f"   解析状态: {feed.get('status', '未知')}")
            
            if hasattr(feed, 'bozo_exception') and feed.bozo_exception:
                print(f"   ⚠️ 解析警告: {feed.bozo_exception}")
            
            for i, entry in enumerate(feed.entries[:3]):  # 只取前3条测试
                title = entry.get('title', '无标题')
                link = entry.get('link', '#')
                published = entry.get('published', '未知时间')
                
                print(f"   条目{i+1}: {title[:50]}...")
                
                # 检查是否包含关键词
                summary = entry.get('summary', '')
                content = f"{title} {summary}".lower()
                
                keywords = KEYWORDS.get(source['category'], [])
                has_keyword = any(keyword.lower() in content for keyword in keywords)
                
                if has_keyword:
                    news_item = {
                        'title': title,
                        'link': link,
                        'source': source['name'],
                        'category': source['category'],
                        'published': published,
                        'summary': summary[:150] + '...' if len(summary) > 150 else summary
                    }
                    all_news.append(news_item)
                    print(f"   ✅ 已添加: {title[:30]}...")
                else:
                    print(f"   ⏭️  跳过: 不包含关键词")
                    
        except Exception as e:
            print(f"❌ 抓取失败 {source['name']}: {type(e).__name__} - {str(e)}")
    
    return all_news
def create_email_content(news_list):
    """生成邮件内容"""
    if not news_list:
        return "今日未找到相关新闻。"
    
    # 按分类分组
    news_by_category = {}
    for news in news_list:
        category = news['category']
        if category not in news_by_category:
            news_by_category[category] = []
        news_by_category[category].append(news)
    
    # 生成HTML内容
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2>📰 AI与低空经济每日资讯 ({datetime.now().strftime('%Y-%m-%d')})</h2>
        <p>共收集到 {len(news_list)} 条相关新闻</p>
    """
    
    for category, items in news_by_category.items():
        html_content += f"""
        <h3>🔹 {category} ({len(items)}条)</h3>
        <ul>
        """
        for news in items:
            html_content += f"""
            <li style="margin-bottom: 15px;">
                <strong><a href="{news['link']}" style="color: #0066cc; text-decoration: none;">{news['title']}</a></strong><br/>
                <small style="color: #666;">
                    来源：{news['source']} | 发布时间：{news['published']}<br/>
                    {news['summary']}
                </small>
            </li>
            """
        html_content += "</ul>"
    
    html_content += """
        <hr/>
        <p style="color: #999; font-size: 12px;">
            本邮件由AI Agent自动生成，新闻来源均为公开RSS订阅。<br/>
            如需调整订阅源或频率，请修改GitHub仓库配置。
        </p>
    </body>
    </html>
    """
    
    return html_content

def send_email(subject, html_content):
    """发送邮件"""
    try:
        # 创建邮件
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        
        # 添加HTML内容
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        # 连接服务器并发送
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print("✅ 邮件发送成功！")
        return True
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("开始收集AI与低空经济资讯...")
    print("=" * 50)
    
    # 1. 抓取新闻
    news_list = fetch_news()
    
    print(f"\n📊 抓取总结: 共找到 {len(news_list)} 条相关新闻")
    
    # 2. 生成邮件内容
    if not news_list:
        print("⚠️ 今日未找到相关新闻，发送测试邮件验证邮件功能")
        email_subject = f"AI Agent测试邮件 ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
        email_content = """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2>📧 AI Agent测试邮件</h2>
            <p>这是一封测试邮件，用于验证AI Agent的邮件发送功能。</p>
            <p>发送时间: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
            <p>状态: 新闻抓取返回0条，但邮件发送功能正常。</p>
            <p>下一步: 请检查新闻源RSS地址是否有效。</p>
        </body>
        </html>
        """
    else:
        email_subject = f"AI与低空经济每日资讯 ({datetime.now().strftime('%m-%d')})"
        email_content = create_email_content(news_list)
    
    # 3. 发送邮件
    print(f"\n📤 准备发送邮件...")
    print(f"   主题: {email_subject}")
    print(f"   发件人: {EMAIL_SENDER}")
    print(f"   收件人: {EMAIL_RECEIVER}")
    
    if EMAIL_PASSWORD:
        try:
            success = send_email(email_subject, email_content)
            if success:
                print("✅ 邮件发送成功！请检查您的邮箱。")
            else:
                print("❌ 邮件发送失败")
        except Exception as e:
            print(f"❌ 邮件发送异常: {type(e).__name__} - {str(e)}")
    else:
        print("⚠️ 未设置邮箱密码，跳过发送邮件")
    
    print("=" * 50)
    print("任务完成")
    print("=" * 50)
