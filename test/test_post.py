import sys
sys.path.append('/Users/lishoulong/Documents/toutiao/lib/openai/myGPTReader')
from utils import extract_text_from_content

# abc = {
#     'chat_id': 'oc_bd28371fcea7b1430b2604ec89baa6e1',
#     'chat_type': 'group',
#     'content': '{"title":"","content":[[{"tag":"at","user_id":"@_user_1","user_name":"chat-reader-bot-test2"},{"tag":"text","text":" 帮我写一个 preact 代码"}]]}',
#     'create_time': '1680133229293',
#     'mentions': [{
#         'id': {
#             'open_id': 'ou_6d7e374599da214ac91bdeccf4f5f70a',
#             'union_id': 'on_68a041cc1f1921eb514a2eced8239132',
#             'user_id': ''
#         },
#         'key': '@_user_1',
#         'name': 'chat-reader-bot-test2',
#         'tenant_key': '174402415083175d'
#     }],
#     'message_id': 'om_2b8f5046b27142997a84c254c3afa997',
#     'message_type': 'post'
# }
abc = {
	'chat_id': 'oc_bd28371fcea7b1430b2604ec89baa6e1',
	'chat_type': 'group',
	'content': '{"title":"","content":[[{"tag":"at","user_id":"@_user_1","user_name":"chat-reader-bot-test2"},{"tag":"text","text":" 介绍下 Signals 的主要原理是什么？"},{"tag":"a","href":"https://preactjs.com/blog/introducing-signals/","text":"https://preactjs.com/blog/introducing-signals/"}],[{"tag":"text","text":"以及介绍下 react 调度的原理？"},{"tag":"a","href":"https://react.iamkasong.com/state/priority.html#%E5%A6%82%E4%BD%95%E8%B0%83%E5%BA%A6%E4%BC%98%E5%85%88%E7%BA%A7","text":"https://react.iamkasong.com/state/priority.html#%E5%A6%82%E4%BD%95%E8%B0%83%E5%BA%A6%E4%BC%98%E5%85%88%E7%BA%A7"}]]}',
	'create_time': '1680134377596',
	'mentions': [{
		'id': {
			'open_id': 'ou_6d7e374599da214ac91bdeccf4f5f70a',
			'union_id': 'on_68a041cc1f1921eb514a2eced8239132',
			'user_id': ''
		},
		'key': '@_user_1',
		'name': 'chat-reader-bot-test2',
		'tenant_key': '174402415083175d'
	}],
	'message_id': 'om_dfdfbdfdf8c30d4d2bf7617901b9f690',
	'message_type': 'post'
}

result = extract_text_from_content(abc)
print(result)