import sys
import json
import io

# 强制所有标准流使用 UTF-8
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


print("测试日志：插件被执行了！ - stderr", file=sys.stderr)
return_data = {
    "completed_output_lists": [],
    "popup": {
        "title": "测试小助手",
        "message": "这是一个测试消息！ - stdout"
    }
}
print(json.dumps(return_data, ensure_ascii=False), file=sys.stdout)
