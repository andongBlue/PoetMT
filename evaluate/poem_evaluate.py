import json
import os
import argparse
import openai
import time
import numpy as np
from tqdm import tqdm

# 设置OpenAI API密钥
# 请在运行前设置环境变量OPENAI_API_KEY或在此处直接设置
# openai.api_key = "your-api-key"

# 评估指标的prompt模板
PROMPTS = {
    "beauty_of_form": """/* Task prompt */Evaluate the translation of the given Chinese classical 
poem into English. Focus on whether the translation 
maintains consistency with the source poem's structure, 
including the alignment of line numbers and balanced 
phrasing. 
1 point: Poor translation, disregards the poem's 
structure, and fails to convey its aesthetic qualities. 
2 point: Some attempt to maintain structure but lack 
alignment and aesthetic consistency. 
3 point: Basic structural elements are maintained 
but with noticeable imperfections in alignment and 
phrasing. 
4 point: Good translation, with most structural 
elements preserved and minor issues in phrasing and 
alignment. 
5 point: Excellent translation, accurately preserving 
the structure, alignment, and aesthetic qualities of the 
original poem./* Input Data */: 
Original Chinese poem: {source} 
English translation: {translation} 
Evaluation (score only):/*Output Text */: 
{score}""",
    
    "beauty_of_meaning": """/* Task prompt */Evaluate the translation of Chinese classical poetry 
for the beauty of meaning, focusing on whether the 
translation effectively conveys the themes, emotions, 
and messages of the original. This includes the use of 
concise and precise language to create vivid imagery 
and a rich atmosphere. 
1 point: Poor translation, fails to convey the depth and 
richness of the original poetry. 
2 point: Basic translation with significant shortcomings 
in capturing themes, emotions, and messages. 
3 point: Satisfactory translation, conveys basic themes 
and emotions but lacks refinement or depth. 
4 point: Good translation, effectively captures 
most themes, emotions, and messages with minor 
imperfections. 
5 point: Excellent translation, accurately conveys the 
depth, richness, and atmosphere of the original poetry 
with full thematic and emotional resonance./* Input Data */: 
Original Chinese poem: {source} 
English translation: {translation} 
Evaluation (score only):/*Output Text */: 
{score}""",
    
    "beauty_of_sound": """/* Task prompt */Evaluate the beauty of sound in the given Chinese 
translation of classical poetry. Focus on whether the 
translation achieves harmonious sound, adherence to 
strict metrical rules, and a rhythm 
1 point: Poor translation, lacks harmony and adherence 
to metrical rules, and fails to capture the beauty of 
sound. 
2 point: Below average, some rhyme and meter present 
but with noticeable imperfections and awkwardness. 
3 point: Basic translation, captures some aspects of 
sound beauty but with several imperfections in rhyme, 
meter, or rhythm. 
4 point: Good translation, mostly harmonious with 
minor imperfections in sound quality or adherence to 
metrical rules. 
5 point: Excellent translation, achieves harmonious 
sound, precise wording, strict adherence to metrical 
rules, and a smooth, dynamic rhythm./* Input Data */: 
Original Chinese poem: {source} 
English translation: {translation} 
Evaluation (score only):/*Output Text */: 
{score}"""
}

def parse_args():
    parser = argparse.ArgumentParser(description='评估古诗词翻译质量')
    parser.add_argument('--input_file', type=str, required=True, help='输入的JSONL文件路径')
    parser.add_argument('--output_file', type=str, required=True, help='保存评估结果的文件路径')
    parser.add_argument('--model', type=str, default='gpt-4', help='用于评估的GPT模型')
    parser.add_argument('--metrics', nargs='+', default=['beauty_of_form', 'beauty_of_meaning', 'beauty_of_sound'], 
                        help='评估指标 (beauty_of_form, beauty_of_meaning, beauty_of_sound)')
    parser.add_argument('--batch_size', type=int, default=10, help='每批评估的诗词数量')
    parser.add_argument('--max_retries', type=int, default=3, help='API调用最大重试次数')
    return parser.parse_args()

def load_data(input_file):
    """加载JSONL格式的诗词数据"""
    data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data

def evaluate_translation(source, translation, metric, model, max_retries=3):
    """使用GPT模型评估翻译质量"""
    prompt = PROMPTS[metric].format(source=source, translation=translation, score="")
    
    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that evaluates poetry translations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,  # 使用确定性输出
                max_tokens=10    # 只需要返回分数
            )
            
            # 提取分数
            score_text = response.choices[0].message.content.strip()
            try:
                # 尝试将分数转换为整数
                score = int(score_text)
                if 1 <= score <= 5:
                    return score
                else:
                    print(f"警告: 分数超出范围: {score_text}, 重试中...")
            except ValueError:
                print(f"警告: 无法解析分数: {score_text}, 重试中...")
                
        except Exception as e:
            print(f"API调用错误: {e}, 尝试 {attempt+1}/{max_retries}")
            if attempt < max_retries - 1:
                time.sleep(5)  # 等待5秒后重试
            else:
                print("达到最大重试次数，返回None")
                return None
    
    return None

def batch_evaluate(data, metrics, model, batch_size, max_retries):
    """批量评估诗词翻译"""
    results = []
    
    for i in tqdm(range(0, len(data), batch_size), desc="评估批次进度"):
        batch = data[i:i+batch_size]
        batch_results = []
        
        for item in tqdm(batch, desc="评估诗词进度", leave=False):
            source = item.get('src', '')
            translation = item.get('hyp', '')  # 使用hyp字段作为翻译结果
            
            item_result = {
                'source': source,
                'translation': translation,
                'scores': {}
            }
            
            # 对每个指标进行评估
            for metric in metrics:
                score = evaluate_translation(source, translation, metric, model, max_retries)
                item_result['scores'][metric] = score
                time.sleep(1)  # 避免API限制
            
            batch_results.append(item_result)
        
        results.extend(batch_results)
        
        # 每个批次后保存中间结果
        with open(f"temp_results_{i}.json", 'w', encoding='utf-8') as f:
            json.dump(batch_results, f, ensure_ascii=False, indent=2)
    
    return results

def calculate_statistics(results, metrics):
    """计算评估结果的统计数据"""
    stats = {}
    
    for metric in metrics:
        scores = [item['scores'][metric] for item in results if item['scores'][metric] is not None]
        
        if scores:
            stats[metric] = {
                'mean': np.mean(scores),
                'median': np.median(scores),
                'std': np.std(scores),
                'min': np.min(scores),
                'max': np.max(scores),
                'count': len(scores)
            }
        else:
            stats[metric] = {
                'mean': None,
                'median': None,
                'std': None,
                'min': None,
                'max': None,
                'count': 0
            }
    
    return stats

def main():
    args = parse_args()
    
    # 加载数据
    print(f"从 {args.input_file} 加载数据...")
    data = load_data(args.input_file)
    print(f"已加载 {len(data)} 首诗词")
    
    # 评估翻译
    print(f"使用 {args.model} 评估翻译...")
    results = batch_evaluate(data, args.metrics, args.model, args.batch_size, args.max_retries)
    
    # 计算统计数据
    stats = calculate_statistics(results, args.metrics)
    
    # 保存结果
    output = {
        'results': results,
        'statistics': stats,
        'config': vars(args)
    }
    
    with open(args.output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"评估完成。结果已保存到 {args.output_file}")
    
    # 打印统计结果
    print("\n评估统计:")
    for metric, metric_stats in stats.items():
        print(f"\n{metric}:")
        for stat_name, stat_value in metric_stats.items():
            if stat_value is not None:
                if stat_name in ['mean', 'median', 'std']:
                    print(f"  {stat_name}: {stat_value:.2f}")
                else:
                    print(f"  {stat_name}: {stat_value}")
            else:
                print(f"  {stat_name}: None")

if __name__ == "__main__":
    main()