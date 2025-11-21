#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
尝试多个 PlantUML 在线服务器，包括支持更大图片的服务器
"""

import urllib.request
import urllib.parse
import zlib
import base64
import sys
from pathlib import Path

def encode_plantuml(plantuml_text):
    """PlantUML 标准编码"""
    plantuml_alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
    base64_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    
    zlibbed_str = zlib.compress(plantuml_text.encode('utf-8'))
    compressed = zlibbed_str[2:-4]
    b64 = base64.b64encode(compressed).decode('ascii')
    
    encoded = ''
    for char in b64:
        if char in base64_alphabet:
            idx = base64_alphabet.index(char)
            encoded += plantuml_alphabet[idx]
        else:
            encoded += char
    
    return encoded

def render_with_server(puml_file, output_file, server_config):
    """使用指定服务器渲染"""
    name = server_config['name']
    base_url = server_config['url']
    format_type = server_config.get('format', 'png')
    
    print(f"\n{'='*70}")
    print(f"尝试服务器: {name}")
    print(f"{'='*70}")
    print(f"URL: {base_url}")
    
    try:
        # 读取源文件
        with open(puml_file, 'r', encoding='utf-8') as f:
            plantuml_text = f.read()
        
        # 编码
        encoded = encode_plantuml(plantuml_text)
        
        # 构建完整 URL
        if '{encoded}' in base_url:
            url = base_url.replace('{encoded}', encoded)
        else:
            url = f'{base_url}/{format_type}/{encoded}'
        
        print(f"请求 URL: {url[:100]}...")
        
        # 设置请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'image/png,image/*;q=0.8,*/*;q=0.5'
        }
        
        req = urllib.request.Request(url, headers=headers)
        
        print("正在获取图片...")
        with urllib.request.urlopen(req, timeout=60) as response:
            if response.status == 200:
                content = response.read()
                
                # 保存文件
                with open(output_file, 'wb') as f:
                    f.write(content)
                
                file_size = len(content) / 1024
                print(f"\n✓ 渲染成功！")
                print(f"  服务器: {name}")
                print(f"  输出文件: {Path(output_file).absolute()}")
                print(f"  文件大小: {file_size:.2f} KB")
                
                # 检查图片尺寸
                try:
                    from PIL import Image
                    import io
                    img = Image.open(io.BytesIO(content))
                    print(f"  图片尺寸: {img.width} x {img.height} 像素")
                except:
                    pass
                
                return True
            else:
                print(f"✗ HTTP {response.status}")
                return False
                
    except urllib.error.HTTPError as e:
        print(f"✗ HTTP 错误: {e.code} - {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"✗ 网络错误: {e.reason}")
        return False
    except Exception as e:
        print(f"✗ 失败: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        puml_file = 'architecture_detailed.puml'
        output_file = 'architecture_detailed.png'
    else:
        puml_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else str(Path(puml_file).with_suffix('.png'))
    
    if not Path(puml_file).exists():
        print(f"✗ 文件不存在: {puml_file}")
        return False
    
    print("="*70)
    print("PlantUML 多服务器在线渲染工具")
    print("="*70)
    print(f"\n源文件: {puml_file}")
    print(f"输出: {output_file}")
    
    # 配置多个服务器（按优先级排序）
    servers = [
        {
            'name': 'PlantUML 官方服务器 (HTTPS)',
            'url': 'https://www.plantuml.com/plantuml',
            'format': 'png'
        },
        {
            'name': 'PlantUML 官方服务器 (HTTP)',
            'url': 'http://www.plantuml.com/plantuml',
            'format': 'png'
        },
        {
            'name': 'PlantUML.com (备用)',
            'url': 'https://plantuml.com/plantuml',
            'format': 'png'
        },
        {
            'name': 'PlantUML.com (HTTP备用)',
            'url': 'http://plantuml.com/plantuml',
            'format': 'png'
        },
        {
            'name': 'Kroki.io (支持更大图片)',
            'url': 'https://kroki.io/plantuml/{format}/{encoded}',
            'format': 'png'
        },
    ]
    
    # 尝试所有服务器
    for i, server in enumerate(servers, 1):
        print(f"\n进度: {i}/{len(servers)}")
        
        if render_with_server(puml_file, output_file, server):
            print("\n" + "="*70)
            print("✓ 渲染完成！")
            print("="*70)
            return True
    
    # 所有服务器都失败
    print("\n" + "="*70)
    print("✗ 所有服务器都失败了")
    print("="*70)
    print("\n建议:")
    print("1. 检查网络连接")
    print("2. 尝试简化 PlantUML 内容")
    print("3. 使用本地 Java 渲染: python render_with_java.py")
    
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
