### 自行搭建使用教程
1. 将 [token-api.js](https://github.com/xxtg666/alt_translator/blob/main/token-api.js) 上传至 [Cloudflare](https://dash.cloudflare.com/) Worker
2. 前往 [百度智能云控制台](https://console.bce.baidu.com/ai/#/ai/machinetranslation/overview/index) 创建应用并获得 **API Key** 与 **Secret Key**
3. 建立 KV 命名空间，预先配置三个键: `api_key` `secret_key` `uuids`
   - `uuids` 可以配置多个，用英文逗号 `,` 分隔，用于获取 token 时的鉴权
4. 修改 [主程序文件 此处](https://github.com/xxtg666/alt_translator/blob/main/alt_translate.py#L20) 的服务器地址
5. 在 [translateAPI.json](https://github.com/xxtg666/alt_translator/blob/main/translate_image_cache/translateAPI.json) 中填入你自己配置的 uuid，任意一个即可
### 安装依赖 
```
pip install -r requirements.txt
```
### 运行

建议管理员模式运行
```
python alt_translate.py
```

按住 Alt 并拖动鼠标可选区截图 自动上传并显示翻译

> [!TIP]
> 触发按键可以在 [此处](https://github.com/xxtg666/alt_translator/blob/main/alt_translate.py#L14) 修改

> [!WARNING]
> 仓库内自带的 uuid `8daa7b67-82a1-40a6-a095-9952d6a31c5f` 为测试数据，已不可使用，作为占位符引导修改
> 
> 不要多开 会出 bug
>
> 打开截屏界面后单击而不拖动会报错，等待修复
> 
> 不要删除 `translate_image_cache` 里的那个 `translateAPI.json`
>
> 建议在 Python 3.12 及以上版本运行
