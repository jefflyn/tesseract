
const DATA_MAP = {
  "1": {
    "title": "JVM\u8fd0\u884c\u65f6\u5185\u5b58\u7ed3\u6784",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "2": {
    "title": "Java\u5185\u5b58\u7ba1\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "3": {
    "title": "\u5783\u573e\u56de\u6536\u7b97\u6cd5\u4ecb\u7ecd",
    "style": "background-color: yellow;",
    "details": "\u6309\u201c\u603b\u7ed3 \u2192 \u6982\u5ff5\u539f\u7406 \u2192 \u4f18\u7f3a\u70b9/\u573a\u666f \u2192 \u5e38\u89c1\u5751&\u89e3\u6cd5\u201d\u8bb2 JVM \u5783\u573e\u56de\u6536\u7b97\u6cd5\u3002\n\n## 1\uff09\u603b\u7ed3\nGC\u7b97\u6cd5\u6838\u5fc3\u5c31\u4e24\u7c7b\u601d\u8def\uff1a  \n- **\u6807\u8bb0\u7c7b**\uff1a\u5148\u627e\u201c\u6d3b\u7684\u201d\uff0c\u5176\u4f59\u56de\u6536\uff08\u6807\u8bb0-\u6e05\u9664 / \u6807\u8bb0-\u6574\u7406 / \u6807\u8bb0-\u590d\u5236\uff09  \n- **\u5f15\u7528\u8ba1\u6570\u7c7b**\uff1a\u9760\u8ba1\u6570\u589e\u51cf\u5224\u65ad\uff08Java\u4e3b\u6d41\u4e0d\u7528\u505a\u4e3b\u7b97\u6cd5\uff09  \n\u518d\u7ed3\u5408**\u5206\u4ee3\u5047\u8bbe**\uff1a\u65b0\u751f\u4ee3\u201c\u671d\u751f\u5915\u6b7b\u201d\u7528\u590d\u5236\u66f4\u5212\u7b97\uff0c\u8001\u5e74\u4ee3\u201c\u5b58\u6d3b\u7387\u9ad8\u201d\u7528\u6807\u8bb0\u6574\u7406/\u6e05\u9664\u66f4\u5408\u9002\u3002\n\n---\n\n## 2\uff09\u6982\u5ff5\u539f\u7406\uff08\u7b97\u6cd5\u600e\u4e48\u505a\uff09\n### 2.1 \u53ef\u8fbe\u6027\u5206\u6790\uff08GC Roots\uff09\nJava\u5224\u65ad\u5bf9\u8c61\u662f\u5426\u201c\u5783\u573e\u201d\uff0c\u4e3b\u6d41\u7528**\u53ef\u8fbe\u6027\u5206\u6790**\uff1a\u4ece GC Roots \u51fa\u53d1\u80fd\u8d70\u5230\u7684\u5bf9\u8c61\u90fd\u7b97\u6d3b\u3002  \n\u5e38\u89c1 Roots\uff1a\u7ebf\u7a0b\u6808\u5f15\u7528\u3001\u9759\u6001\u53d8\u91cf\u5f15\u7528\u3001JNI\u5f15\u7528\u3001\u8fd0\u884c\u4e2d\u9501\u6301\u6709\u5bf9\u8c61\u7b49\u3002\n\n### 2.2 \u6807\u8bb0-\u6e05\u9664\uff08Mark-Sweep\uff09\n- **\u6b65\u9aa4**\uff1a\u6807\u8bb0\u5b58\u6d3b\u5bf9\u8c61 \u2192 \u6e05\u9664\u672a\u6807\u8bb0\u5bf9\u8c61\n- **\u7279\u70b9**\uff1a\u5b9e\u73b0\u7b80\u5355\uff1b\u4f46\u4f1a\u4ea7\u751f**\u5185\u5b58\u788e\u7247**\uff0c\u5206\u914d\u5927\u5bf9\u8c61\u53ef\u80fd\u5931\u8d25\u3002\n\n### 2.3 \u6807\u8bb0-\u6574\u7406\uff08Mark-Compact\uff09\n- **\u6b65\u9aa4**\uff1a\u6807\u8bb0\u5b58\u6d3b\u5bf9\u8c61 \u2192 \u628a\u5b58\u6d3b\u5bf9\u8c61\u5411\u4e00\u7aef\u201c\u6324\u538b\u201d \u2192 \u6e05\u7406\u8fb9\u754c\u5916\u5185\u5b58\n- **\u7279\u70b9**\uff1a\u89e3\u51b3\u788e\u7247\uff1b\u4ee3\u4ef7\u662f**\u6574\u7406\u79fb\u52a8\u5bf9\u8c61\u6210\u672c\u9ad8**\u3001\u505c\u987f\u53ef\u80fd\u66f4\u957f\u3002\u5e38\u7528\u4e8e\u8001\u5e74\u4ee3\u3002\n\n### 2.4 \u590d\u5236\u7b97\u6cd5\uff08Copying / Semi-space\uff09\n- **\u6b65\u9aa4**\uff1a\u628a\u5b58\u6d3b\u5bf9\u8c61\u4ece From \u590d\u5236\u5230 To \u2192 \u76f4\u63a5\u6e05\u7a7a From\n- **\u7279\u70b9**\uff1a\u5206\u914d\u5feb\u3001\u65e0\u788e\u7247\uff1b\u7f3a\u70b9\u662f\u9700\u8981**\u989d\u5916\u4e00\u5757\u540c\u7b49\u7a7a\u95f4**\u3002\u65b0\u751f\u4ee3\u5e38\u7528\uff08Eden + Survivor\uff09\u3002\n\n### 2.5 \u5206\u4ee3\u6536\u96c6\uff08Generational\uff09\n- \u65b0\u751f\u4ee3\uff1a\u590d\u5236 + \u5feb\u901f\u56de\u6536\uff08Minor GC / Young GC\uff09\n- \u8001\u5e74\u4ee3\uff1a\u6807\u8bb0-\u6e05\u9664/\u6574\u7406\uff08Major/Old GC\uff09\n- \u8de8\u4ee3\u5f15\u7528\u7528 **\u8bb0\u5fc6\u96c6/\u5361\u8868** \u964d\u4f4e\u626b\u63cf\u6210\u672c\uff08\u907f\u514d\u6bcf\u6b21\u90fd\u626b\u6574\u4e2a\u8001\u5e74\u4ee3\uff09\u3002\n\n### 2.6 \u5f15\u7528\u8ba1\u6570\uff08Reference Counting\uff0c\u4e3a\u4f55Java\u4e0d\u4e3b\u7528\uff09\n- **\u4f18\u70b9**\uff1a\u56de\u6536\u53ca\u65f6\u3001\u5b9e\u73b0\u76f4\u89c2\n- **\u81f4\u547d\u95ee\u9898**\uff1a\u65e0\u6cd5\u89e3\u51b3**\u5faa\u73af\u5f15\u7528**\uff08A\u5f15\u7528B\uff0cB\u5f15\u7528A\uff0c\u8ba1\u6570\u90fd\u4e0d\u4e3a0\uff09\u3002\n\n---\n\n## 3\uff09\u4f18\u7f3a\u70b9 & \u9002\u7528\u573a\u666f\uff08\u600e\u4e48\u9009\uff09\n- **\u590d\u5236**\uff1a\u9002\u5408\u5b58\u6d3b\u7387\u4f4e\u3001\u5bf9\u8c61\u5c0f\u4e14\u591a\u7684\u533a\u57df\uff08\u65b0\u751f\u4ee3\uff09\u3002\n- **\u6807\u8bb0-\u6574\u7406**\uff1a\u9002\u5408\u5b58\u6d3b\u7387\u9ad8\u3001\u5e0c\u671b\u65e0\u788e\u7247\u7684\u533a\u57df\uff08\u8001\u5e74\u4ee3\u3001\u9700\u8981\u8fde\u7eed\u7a7a\u95f4\u65f6\uff09\u3002\n- **\u6807\u8bb0-\u6e05\u9664**\uff1a\u9002\u5408\u5bf9\u505c\u987f\u66f4\u654f\u611f\u3001\u80fd\u5bb9\u5fcd\u788e\u7247\u6216\u6709\u914d\u5957\uff08\u5982\u7a7a\u95f2\u5217\u8868\uff09\u7684\u573a\u666f\uff08\u90e8\u5206\u8001\u5e74\u4ee3\u5b9e\u73b0\u4f1a\u7528\uff09\u3002\n\n> \u5b9e\u9645\u4e0a\u4f60\u7528 G1/ZGC \u8fd9\u7c7b\u6536\u96c6\u5668\u65f6\uff0c\u5e95\u5c42\u4ecd\u662f\u8fd9\u4e9b\u7b97\u6cd5\u7684\u7ec4\u5408\u4e0e\u5de5\u7a0b\u5316\u5b9e\u73b0\uff08\u5e76\u53d1\u6807\u8bb0\u3001\u5206\u533a\u3001\u8f6c\u79fb\u7b49\uff09\u3002\n\n---\n\n## 4\uff09\u5e38\u89c1\u5751 & \u89e3\u51b3\u65b9\u6848\n1) **\u8001\u5e74\u4ee3\u788e\u7247\u5bfc\u81f4 Full GC \u9891\u7e41/\u5206\u914d\u5931\u8d25**  \n- \u73b0\u8c61\uff1a\u8001\u5e74\u4ee3\u660e\u660e\u8fd8\u6709\u7a7a\u95f4\u4f46\u5206\u914d\u5927\u5bf9\u8c61\u5931\u8d25\u89e6\u53d1 Full GC  \n- \u89e3\u6cd5\uff1a\u503e\u5411\u4f7f\u7528\u5e26\u6574\u7406/\u538b\u7f29\u80fd\u529b\u7684\u7b56\u7565\uff08\u5982G1\u7684\u8f6c\u79fb/\u538b\u7f29\u7279\u6027\uff09\uff1b\u51cf\u5c11\u5927\u5bf9\u8c61\u76f4\u63a5\u8fdb\u8001\u5e74\u4ee3\uff1b\u5408\u7406\u8bbe\u7f6e\u5806\u4e0e\u664b\u5347\u9608\u503c\n\n2) **\u664b\u5347\u5931\u8d25\uff08promotion failed\uff09**\uff08\u65b0\u751f\u4ee3\u590d\u5236\u5230\u8001\u5e74\u4ee3\u653e\u4e0d\u4e0b\uff09  \n- \u89e3\u6cd5\uff1a\u589e\u5927\u8001\u5e74\u4ee3/\u5806\uff1b\u964d\u4f4e\u5bf9\u8c61\u5b58\u6d3b\u7387\uff08\u51cf\u5c11\u957f\u751f\u547d\u5468\u671f\u7f13\u5b58\uff09\uff1b\u8c03\u6574 Survivor \u6bd4\u4f8b\u4e0e\u664b\u5347\u7b56\u7565\n\n3) **Minor GC\u5f88\u9891\u7e41**\uff08\u5206\u914d\u8fc7\u5feb\u3001Eden\u592a\u5c0f\uff09  \n- \u89e3\u6cd5\uff1a\u589e\u5927\u65b0\u751f\u4ee3\u6216\u4f18\u5316\u5bf9\u8c61\u521b\u5efa\uff08\u590d\u7528\u3001\u6c60\u5316\u8981\u8c28\u614e\uff09\uff1b\u6392\u67e5\u77ed\u751f\u547d\u5468\u671f\u5927\u5bf9\u8c61\n\n4) **\u628a\u201c\u5f15\u7528\u7c7b\u578b\u201d\u5f53\u7b97\u6cd5**  \n- \u5f3a/\u8f6f/\u5f31/\u865a\u5f15\u7528\u662f\u201c\u5bf9\u8c61\u53ef\u8fbe\u6027\u5f3a\u5f31\u201d\uff0c\u4e0d\u662fGC\u7b97\u6cd5\uff1b\u5e38\u7528\u4e8e\u7f13\u5b58\uff08Soft\uff09\u3001\u89c4\u8303\u5316\u6620\u5c04/\u5f31\u952e\uff08Weak\uff09\u7b49\u3002\n\n\u5982\u679c\u4f60\u9762\u8bd5\u9700\u8981\u518d\u5f80\u4e0b\u63a5\uff0c\u6211\u53ef\u4ee5\u628a\u8fd9\u4e9b\u7b97\u6cd5\u600e\u4e48\u5bf9\u5e94\u5230 **Serial/Parallel/CMS/G1/ZGC** \u4ee5\u53ca\u5404\u81ea\u89e6\u53d1\u6761\u4ef6\u3001\u505c\u987f\u7279\u5f81\uff0c\u4e32\u6210\u4e00\u5957\u8bdd\u672f\u3002",
    "subItems": []
  },
  "5": {
    "title": "Java\u5783\u573e\u56de\u6536\u673a\u5236",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u54ea\u4e9b\u662f\u5927\u5bf9\u8c61\uff1f",
      "\u5783\u573e\u56de\u6536\u6709\u54ea\u4e9b\u7b97\u6cd5\uff1f",
      "JVM\u7684\u6c38\u4e45\u4ee3\u4e2d\u4f1a\u53d1\u751f\u5783\u573e\u56de\u6536\u4e48\uff1f"
    ]
  },
  "6": {
    "title": "Full GC\u548cMinor GC",
    "style": "",
    "details": "",
    "subItems": [
      "Minor GC\u4e0eFull GC\u5206\u522b\u5728\u4ec0\u4e48\u65f6\u5019\u53d1\u751f\uff1f",
      "\u600e\u4e48\u907f\u514d\u548c\u4f18\u5316\uff1f"
    ]
  },
  "7": {
    "title": "OOM\u7684\u7c7b\u578b\uff0c\u4e3b\u8981\u539f\u56e0\u548c\u6392\u67e5",
    "style": "",
    "details": "",
    "subItems": []
  },
  "8": {
    "title": "Java\u6027\u80fd\u4f18\u5316\u51cf\u5c11GC",
    "style": "",
    "details": "",
    "subItems": []
  },
  "9": {
    "title": "JVM\u7c7b\u52a0\u8f7d\u539f\u7406\u548c\u8fc7\u7a0b",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "10": {
    "title": "Java\u7ebf\u7a0b\u6a21\u578bJMM",
    "style": "",
    "details": "",
    "subItems": [
      "happens-before\u548c\u5185\u5b58\u5c4f\u969c\u662f\u4ec0\u4e48\uff1f"
    ]
  },
  "11": {
    "title": "JDK8\u7684\u65b0\u7279\u6027",
    "style": "",
    "details": "",
    "subItems": [
      "Jdk21\u7684\u65b0\u7279\u6027",
      "\u865a\u62df\u7ebf\u7a0b\u4ecb\u7ecd"
    ]
  },
  "17": {
    "title": "Java\u96c6\u5408",
    "style": "",
    "details": "",
    "subItems": [
      "ArrayList\u548cLinkedList\u4ecb\u7ecd",
      "HashSet TreeSet LinkHashSet",
      "\u7ebf\u7a0b\u5b89\u5168\u96c6\u5408\u6709\u54ea\u4e9b\uff1f"
    ]
  },
  "18": {
    "title": "HashMap\u4ecb\u7ecd",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "HashMap\u600e\u4e48\u89e3\u51b3hash\u51b2\u7a81\uff1f",
      "\u5e95\u5c42\u5982\u4f55\u6269\u5bb9\uff1f",
      "\u4ecb\u7ecdConcurrentHashMap",
      "HashTable"
    ]
  },
  "19": {
    "title": "Java\u7ebf\u7a0b\u548c\u751f\u547d\u5468\u671f",
    "style": "",
    "details": "",
    "subItems": [
      "\u5b88\u62a4\u7ebf\u7a0b\u548c\u540e\u53f0\u7ebf\u7a0b",
      "\u4ec0\u4e48\u662f\u7ebf\u7a0b\u5b89\u5168\uff1f\u600e\u4e48\u4fdd\u8bc1\uff1f"
    ]
  },
  "20": {
    "title": "\u7ec8\u6b62\u7ebf\u7a0b\u7684\u65b9\u5f0f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "21": {
    "title": "\u7ebf\u7a0b\u95f4\u600e\u4e48\u901a\u8baf",
    "style": "",
    "details": "",
    "subItems": [
      "sleep\u548cwait\u7684\u4f5c\u7528",
      "start\u548crun\u533a\u522b\u662f\u4ec0\u4e48\uff1f"
    ]
  },
  "22": {
    "title": "\u7ebf\u7a0b\u6c60\u539f\u7406\u4ee5\u53ca\u8c03\u4f18",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u5e38\u7528\u7684\u7ebf\u7a0b\u6c60\u6709\u54ea\u4e9b\uff1f\u600e\u4e48\u4f7f\u7528\uff1f",
      "\u7ebf\u7a0b\u6c60\u600e\u4e48\u8c03\u4f18\uff1f",
      "\u4f7f\u7528\u7ebf\u7a0b\u6c60\u6709\u4ec0\u4e48\u95ee\u9898\u8981\u6ce8\u610f\uff1f"
    ]
  },
  "23": {
    "title": "Java\u9501\u539f\u7406",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u504f\u5411\u9501\u3001\u8f7b\u91cf\u7ea7\u9501\u548c\u91cd\u91cf\u7ea7\u9501",
      "\u4ec0\u4e48\u662f\u81ea\u65cb\u9501\uff1f",
      "\u4ec0\u4e48\u662f\u6b7b\u9501\u4e0e\u6d3b\u9501\uff1f",
      "\u4ec0\u4e48\u662f\u53ef\u91cd\u5165\u9501\uff1f\u4e3a\u4ec0\u4e48\u8bf4synchronized\u662f\u53ef\u91cd\u5165\uff1f"
    ]
  },
  "24": {
    "title": "\u7ebf\u7a0b\u5171\u4eab\u548c\u5e76\u53d1\u5de5\u5177\u7c7b",
    "style": "",
    "details": "",
    "subItems": [
      "\u5e76\u53d1\u5bb9\u5668\u6216\u5de5\u5177\u7c7b\u6709\u54ea\u4e9b\uff1f"
    ]
  },
  "25": {
    "title": "ThreadLocal\u548cThreadLocalMap",
    "style": "",
    "details": "",
    "subItems": [
      "ThreadLocal\u6709\u4ec0\u4e48\u7f3a\u70b9\uff1f"
    ]
  },
  "26": {
    "title": "synchronized",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "synchronized\u548cReentrantLock\u7684\u533a\u522b"
    ]
  },
  "27": {
    "title": "CAS\u548cAQS\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": [
      "CAS\u600e\u4e48\u5b9e\u73b0\u539f\u5b50\u66f4\u65b0\uff1f",
      "Java\u963b\u585e\u961f\u5217\u539f\u7406"
    ]
  },
  "28": {
    "title": "volatile\u7684\u4f5c\u7528",
    "style": "",
    "details": "",
    "subItems": []
  },
  "29": {
    "title": "Java\u53cd\u5c04\u539f\u7406\u548c\u5e94\u7528",
    "style": "",
    "details": "",
    "subItems": []
  },
  "30": {
    "title": "Java\u5bf9\u8c61\u590d\u5236\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "31": {
    "title": "Spring IOC",
    "style": "",
    "details": "",
    "subItems": []
  },
  "32": {
    "title": "Spring AOP",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "33": {
    "title": "Spring\u751f\u547d\u5468\u671f\u7ba1\u7406",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "34": {
    "title": "Spring\u600e\u4e48\u89e3\u51b3\u5faa\u73af\u4f9d\u8d56",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u54ea\u4e9b\u5faa\u73af\u4f9d\u8d56\u65e0\u6cd5\u89e3\u51b3\uff1f",
      "\u4e3a\u4ec0\u4e48\u4e0d\u4f7f\u7528\u4e8c\u7ea7\u7f13\u5b58"
    ]
  },
  "35": {
    "title": "Spring\u4ee3\u7406\u6a21\u5f0f",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u6ce8\u89e3\u5931\u6548\u539f\u7406\u4ee5\u53ca\u89e3\u51b3"
    ]
  },
  "36": {
    "title": "Spring\u5e38\u89c1\u8bbe\u8ba1\u6a21\u5f0f",
    "style": "",
    "details": "",
    "subItems": [
      "\u5355\u4f8b\u6a21\u5f0f\u5b9e\u73b0"
    ]
  },
  "37": {
    "title": "Spring\u4e8b\u52a1\u7ba1\u7406",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "38": {
    "title": "BeanFactory\u548cFactoryBean",
    "style": "",
    "details": "",
    "subItems": []
  },
  "39": {
    "title": "SpringMVC\u5de5\u4f5c\u6d41\u7a0b",
    "style": "",
    "details": "",
    "subItems": []
  },
  "40": {
    "title": "\u6ce8\u89e3\u5931\u6548\u539f\u7406\u4ee5\u53ca\u89e3\u51b3",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "41": {
    "title": "SpringBoot\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "42": {
    "title": "MyBatis\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "43": {
    "title": "MyBatis\u7f13\u5b58\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "44": {
    "title": "MyBatis\u9047\u5230\u7684\u5751",
    "style": "",
    "details": "",
    "subItems": []
  },
  "45": {
    "title": "SpringBoot Starter\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "52": {
    "title": "\u6570\u636e\u5e93\u4e8b\u52a1\u4ecb\u7ecd",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u4e8b\u52a1\u9694\u79bb\u7ea7\u522b\u6709\u54ea\u4e9b?",
      "MySQL\u7684\u9ed8\u8ba4\u9694\u79bb\u7ea7\u522b\u662f?"
    ]
  },
  "53": {
    "title": "SQL\u6267\u884c\u8fc7\u7a0b",
    "style": "",
    "details": "",
    "subItems": []
  },
  "54": {
    "title": "\u6570\u636e\u5e93\u9501\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": [
      "MySQL\u7684\u884c\u9501\u548c\u8868\u9501\uff0c\u4ec0\u4e48\u60c5\u51b5\u9501\u884c\u548c\u9501\u8868\uff1f"
    ]
  },
  "55": {
    "title": "\u805a\u7c07\u7d22\u5f15\u4ecb\u7ecd",
    "style": "",
    "details": "",
    "subItems": []
  },
  "56": {
    "title": "MySQL\u7d22\u5f15\u539f\u7406",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u7d22\u5f15\u7ed3\u6784\u662fB\u6811\u8fd8\u662fB+\u6811\uff1f",
      "\u4ec0\u4e48\u662f\u56de\u8868\uff1f"
    ]
  },
  "57": {
    "title": "\u5199\u591a\u8bfb\u5c11\u65b9\u6848",
    "style": "",
    "details": "",
    "subItems": []
  },
  "58": {
    "title": "\u60b2\u89c2\u9501\u548c\u4e50\u89c2\u9501",
    "style": "",
    "details": "",
    "subItems": []
  },
  "59": {
    "title": "\u6b7b\u9501\u6392\u67e5\u548c\u89e3\u51b3",
    "style": "",
    "details": "",
    "subItems": []
  },
  "60": {
    "title": "\u6162SQL\u4f18\u5316",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u5982\u4f55\u5927\u8868\uff0c\u5982\u4f55\u4f18\u5316?"
    ]
  },
  "61": {
    "title": "\u6267\u884c\u8ba1\u5212\u600e\u4e48\u770b",
    "style": "",
    "details": "",
    "subItems": []
  },
  "62": {
    "title": "\u5206\u5e03\u5f0f\u4e8b\u52a1\u539f\u7406",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "63": {
    "title": "\u5206\u5e03\u5f0f\u4e8b\u52a1\u89e3\u51b3\u65b9\u6848",
    "style": "",
    "details": "",
    "subItems": [
      "\u4e24\u9636\u6bb5\u63d0\u4ea4\u7f3a\u70b9\u548c\u89e3\u51b3"
    ]
  },
  "64": {
    "title": "Redis\u4e3a\u4ec0\u4e48\u6027\u80fd\u9ad8",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "65": {
    "title": "Redis\u6301\u4e45\u5316\u7b56\u7565",
    "style": "",
    "details": "",
    "subItems": []
  },
  "66": {
    "title": "Redis\u9ad8\u53ef\u7528\u548c\u96c6\u7fa4\u65b9\u5f0f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "67": {
    "title": "\u7f13\u5b58\u600e\u4e48\u4fdd\u8bc1\u6570\u636e\u4e00\u81f4\u6027",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "89": {
    "title": "\u5fae\u670d\u52a1 \u80cc\u666f \u4f18\u7f3a\u70b9",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "90": {
    "title": "\u5fae\u670d\u52a1\u62c6\u5206\u539f\u5219",
    "style": "",
    "details": "",
    "subItems": [
      "\u5fae\u670d\u52a1\u600e\u4e48\u62c6\u5206\uff1f",
      "\u62c6\u5206\u540e\u5e26\u6765\u4ec0\u4e48\u65b0\u95ee\u9898\uff1f"
    ]
  },
  "91": {
    "title": "\u670d\u52a1\u6ce8\u518c\u4e0e\u53d1\u73b0 Eureka+Nacos",
    "style": "",
    "details": "",
    "subItems": []
  },
  "92": {
    "title": "\u9650\u6d41 \u7194\u65ad \u964d\u7ea7\u600e\u4e48\u505a",
    "style": "",
    "details": "",
    "subItems": []
  },
  "93": {
    "title": "\u5fae\u670d\u52a1\u8d1f\u8f7d\u5747\u8861\u600e\u4e48\u505a",
    "style": "",
    "details": "",
    "subItems": []
  },
  "94": {
    "title": "CAP\u548cBASE\u7406\u8bba",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u600e\u4e48\u7406\u89e3BASE\u7406\u8bba\uff1f\u6709\u4ec0\u4e48\u65b9\u6848\uff1f"
    ]
  },
  "95": {
    "title": "Nacos\u914d\u7f6e\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "96": {
    "title": "\u94fe\u8def \u670d\u52a1\u7f51\u5173\u8def\u7531\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "97": {
    "title": "RPC\u539f\u7406\u548c\u5b9e\u73b0\u6846\u67b6",
    "style": "",
    "details": "",
    "subItems": [
      "\u8fd8\u6709\u54ea\u4e9bRPC\u6846\u67b6\uff0c\u6709\u4ec0\u4e48\u5f02\u540c\uff1f"
    ]
  },
  "98": {
    "title": "Zookeeper\u539f\u7406",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "ZAP\u534f\u8bae\u4ecb\u7ecd",
      "ZAB\u548cPaxos\u7b97\u6cd5\u7684\u8054\u7cfb\u4e0e\u533a\u522b?",
      "Zookeeper\u7684\u9009\u4e3e\u673a\u5236",
      "Zookeeper\u662f\u5982\u4f55\u4fdd\u8bc1\u4e8b\u52a1\u7684\u987a\u5e8f\u4e00\u81f4\u6027\u7684?",
      "Zookeeper\u6709\u54ea\u51e0\u79cd\u51e0\u79cd\u90e8\u7f72\u6a21\u5f0f?"
    ]
  },
  "99": {
    "title": "\u4e00\u81f4\u6027\u7b97\u6cd5\u6709\u54ea\u4e9b",
    "style": "",
    "details": "",
    "subItems": []
  },
  "100": {
    "title": "\u5982\u4f55\u4fdd\u8bc1\u63a5\u53e3\u5e42\u7b49",
    "style": "",
    "details": "",
    "subItems": []
  },
  "101": {
    "title": "\u5206\u5e03\u5f0f\u7f13\u5b58\u8bbe\u8ba1",
    "style": "",
    "details": "",
    "subItems": [
      "\u7f13\u5b58\u600e\u4e48\u4fdd\u6301\u6570\u636e\u4e00\u81f4\u6027\uff1f",
      "\u7f13\u5b58\u7a7f\u900f\u3001\u7f13\u5b58\u96ea\u5d29\u548c\u7f13\u5b58\u5931\u6548\u600e\u4e48\u5904\u7406\uff1f",
      "\u70ed\u70b9\u6570\u636e\u7f13\u5b58\u600e\u4e48\u8bbe\u8ba1\uff1f"
    ]
  },
  "102": {
    "title": "\u5206\u5e03\u5f0fID\u751f\u6210",
    "style": "",
    "details": "",
    "subItems": []
  },
  "103": {
    "title": "\u5206\u5e03\u5f0f\u9501\u539f\u7406",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u5206\u5e03\u5f0f\u9501\u6709\u54ea\u4e9b\u5b9e\u73b0\uff1f",
      "Redis\u5206\u5e03\u5f0f\u9501\u7f3a\u70b9",
      "Redisson\u600e\u4e48\u89e3\u51b3\u5206\u5e03\u5f0f\u9501\u7684\u95ee\u9898\uff1f",
      "\u600e\u4e48\u89e3\u51b3\u4e86Redis\u5b9e\u73b0\u7684\u5206\u5e03\u5f0f\u9501\u95ee\u9898\uff1f",
      "\u9501\u7684value\u5b58\u7684\u662f\u4ec0\u4e48\uff1f",
      "\u5982\u679c\u9501\u8d85\u65f6\uff0c\u4e1a\u52a1\u8fd8\u6ca1\u5904\u7406\u5b8c\u600e\u4e48\u529e\uff1f",
      "\u4e3bredis\u6302\u4e86\uff0c\u9501\u672a\u540c\u6b65\u5230\u4ece\uff0c\u600e\u4e48\u529e\uff1f"
    ]
  },
  "104": {
    "title": "\u5206\u5e03\u5f0f\u4e8b\u52a1",
    "style": "",
    "details": "",
    "subItems": [
      "\u5206\u5e03\u5f0f\u4e8b\u52a1\u89e3\u51b3\u65b9\u6848\u6709\u54ea\u4e9b\uff1f",
      "\u4e24\u9636\u6bb5\u63d0\u4ea4\u7f3a\u70b9\u548c\u89e3\u51b3\u65b9\u6848",
      "\u5f3a\u4e00\u81f4\u6027\u7684\u89e3\u51b3\u65b9\u6848\uff0c\u4e3a\u4ec0\u4e48\u4e0d\u7528\u5206\u5e03\u5f0f\u4e8b\u52a1XA\uff1f",
      "\u6700\u7ec8\u4e00\u81f4\u6027\u7684\u89e3\u51b3\u65b9\u6848",
      "\u672c\u5730\u4e8b\u52a1+Outbox\u65b9\u6848\uff0c\u4e3a\u4ec0\u4e48\u5f15\u5165\u672c\u5730\u4e8b\u52a1\u65e5\u5fd7\u8868\uff1f",
      "\u4e8b\u52a1\u65e5\u5fd7\u8868 + \u72b6\u6001\u673a\u7b56\u7565",
      "\u4e8b\u52a1\u65e5\u5fd7\u8868\u7206\u70b8\u4e86\u600e\u4e48\u529e\uff1f",
      "\u4e3a\u4ec0\u4e48\u4e0d\u7528MQ\u7684\u4e8b\u52a1\u6d88\u606f\uff1f",
      "TCC\u548cSaga\u7684\u89e3\u51b3\u65b9\u6848",
      "Seata\u4e00\u7ad9\u5f0f\u7684\u5206\u5e03\u5f0f\u89e3\u51b3\u65b9\u6848\u4ecb\u7ecd"
    ]
  },
  "105": {
    "title": "\u6d88\u606f\u961f\u5217\u7684\u4f7f\u7528\u573a\u666f",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "106": {
    "title": "Kafka\u4e3a\u4ec0\u4e48\u9ad8\u6027\u80fd",
    "style": "",
    "details": "",
    "subItems": [
      "\u6d88\u8d39\u8005poll/pull\u8fd8\u662fpush",
      "\u600e\u4e48\u4fdd\u8bc1\u6d88\u606f\u53d1\u9001\u6d88\u8d39\u6210\u529f\uff1f",
      "\u600e\u4e48\u5904\u7406\u6d88\u606f\u4e22\u5931\uff1f",
      "\u600e\u4e48\u89e3\u51b3\u6d88\u606f\u91cd\u590d\u6d88\u8d39\u3001\u6d88\u606f\u987a\u5e8f\u6027\u3001\u5927\u89c4\u6a21\u6d88\u606f\u9650\u901f\u95ee\u9898",
      "\u6d88\u8d39\u8005\u6545\u969c\uff0c\u51fa\u73b0\u6d3b\u9501\u95ee\u9898\u5982\u4f55\u89e3\u51b3?"
    ]
  },
  "107": {
    "title": "RocketMQ\u7684\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": [
      "\u6d88\u8d39\u8005poll/pull\u8fd8\u662fpush",
      "\u600e\u4e48\u4fdd\u8bc1\u6d88\u606f\u53d1\u9001\u6d88\u8d39\u6210\u529f\uff1f",
      "\u600e\u4e48\u5904\u7406\u6d88\u606f\u4e22\u5931\uff1f",
      "\u600e\u4e48\u89e3\u51b3\u6d88\u606f\u91cd\u590d\u6d88\u8d39\u3001\u6d88\u606f\u987a\u5e8f\u6027\u3001\u5927\u89c4\u6a21\u6d88\u606f\u9650\u901f\u95ee\u9898",
      "\u51fa\u73b0\u6d88\u606f\u5806\u79ef\u600e\u4e48\u5904\u7406\uff1f",
      "\u5982\u4f55\u4fdd\u8bc1\u6d88\u606f\u7684\u53ef\u9760\u4f20\u8f93\uff1f\u5982\u679c\u6d88\u606f\u4e22\u4e86\u600e\u4e48\u529e\uff1f"
    ]
  },
  "108": {
    "title": "RocketMQ\u6d88\u606f\u4e8b\u52a1\u539f\u7406",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u4e3a\u4ec0\u4e48\u4e0d\u80fd\u76f4\u63a5\u7528MQ\u7684\u4e8b\u52a1\u6d88\u606f\uff1f"
    ]
  },
  "109": {
    "title": "RocketMQ\u548cKafka\u9009\u578b\u5bf9\u6bd4",
    "style": "",
    "details": "",
    "subItems": []
  },
  "110": {
    "title": "\u4ecb\u7ecd\u9879\u76ee \u5171\u4eab\u5145\u7535\u5b9d",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u4f60\u7684\u804c\u8d23\u548c\u5de5\u4f5c\u5185\u5bb9",
      "\u8be6\u7ec6\u8bb2\u4e00\u4e0b\u9879\u76ee\u7684\u6280\u672f\u67b6\u6784",
      "\u9879\u76ee\u600e\u4e48\u505a\u6280\u672f\u9009\u578b\uff1f\u4fdd\u8bc1\u9ad8\u6027\u80fd \u9ad8\u53ef\u7528",
      "\u9879\u76ee\u600e\u4e48\u505a\u5230\u53ef\u7528\u602799.9%+\u7684\uff1f",
      "\u4ea4\u6613\u94fe\u8def\u54cd\u5e94\u901f\u5ea6\u63d0\u534745%\uff0c\u600e\u4e48\u505a\u5230\u7684\uff1f",
      "\u9879\u76ee\u600e\u4e48\u505a\u7ebf\u7a0b\u6c60\u4f18\u5316\u7684\uff1f",
      "Flink\u5b9e\u65f6\u6570\u636e\u540c\u6b65\uff0c\u4e3a\u4ec0\u4e48\u4f7f\u7528\uff1f",
      "Flink\u76d1\u542cbinlog\uff0c\u6570\u636e\u54ea\u91cc\u6765\u7684\uff1f",
      "\u4e3a\u4ec0\u4e48\u8fd9\u6837\u8bbe\u8ba1\uff1f",
      "\u9879\u76ee\u54ea\u4e9b\u5730\u65b9\u53ef\u6539\u8fdb\uff1f",
      "\u63cf\u8ff0\u4e00\u4e2a\u8bbe\u5907\u51fa\u5165\u5e93\u53d8\u66f4\u8d44\u4ea7\u4f4d\u7f6e\u4e24\u4e2a\u670d\u52a1\u6700\u7ec8\u4e00\u81f4\u6027\u7684\u5b9e\u73b0\u8fc7\u7a0b",
      "\u5e93\u5b58\u7ba1\u7406\u600e\u4e48\u505a\u7684\uff1f\u600e\u4e48\u4fdd\u8bc1\u5e93\u5b58\u51c6\u786e\u6027\uff1f",
      "\u4efb\u52a1\u8c03\u5ea6\u4e2d\u5fc3\u7684\u4e1a\u52a1\u80cc\u666f\u662f\u4ec0\u4e48\uff1f",
      "\u63cf\u8ff0\u5b9a\u65f6\u4efb\u52a1\u5728\u9879\u76ee\u7528\u4f5c\u4e8b\u52a1\u8865\u507f\uff1f",
      "\u5728\u9879\u76ee\u4e2d\u5982\u4f55\u652f\u6301\u548c\u76d1\u63a7\u4e1a\u52a1\u9ad8\u654f\u573a\u666f\uff1f",
      "\u4f60\u5728\u865a\u62df\u56e2\u961f\u4e2d\u6709\u6ca1\u6709\u5e26\u9886\u56e2\u961f\u505a\u8fc7\u4e00\u4e9b\u4e8b\u60c5\uff1f",
      "\u5728\u56e2\u961f\u8d44\u6e90\u534f\u8c03\u65b9\u9762\u6709\u4ec0\u4e48\u7ecf\u9a8c\uff1f",
      "\u5728\u9879\u76ee\u4e2d\u6709\u6ca1\u6709\u4f7f\u7528\u4e00\u4e9b\u65b0\u5174\u7684\u5de5\u5177\u8fdb\u884c\u6280\u672f\u5b9e\u73b0\u7684\u9a8c\u8bc1\uff1f",
      "AI+\u9489\u9489\u5bf9\u8bdd\u5f0f\u8fd0\u8425\u5de5\u5177 \u600e\u4e48\u5b9e\u73b0\u7684 \u7528\u5230\u54ea\u4e9b\u6280\u672f\uff1f",
      "\u591a\u8f6e\u5bf9\u8bdd\u600e\u4e48\u5b9e\u73b0\uff1f",
      "AI\u5de5\u7a0b\u5316\u9879\u76ee\u4e3b\u8981\u662f\u89e3\u51b3\u4ec0\u4e48\u95ee\u9898\uff1f"
    ]
  },
  "111": {
    "title": "\u4ee3\u7801\u91cd\u6784\u600e\u4e48\u505a",
    "style": "",
    "details": "",
    "subItems": []
  },
  "112": {
    "title": "\u600e\u4e48\u505a\u6280\u672f\u9009\u578b",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "113": {
    "title": "\u7cfb\u7edf\u6027\u80fd\u4f18\u5316\u600e\u4e48\u505a",
    "style": "",
    "details": "",
    "subItems": []
  },
  "114": {
    "title": "\u7ebf\u4e0a\u95ee\u9898\u600e\u4e48\u89e3\u51b3",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "115": {
    "title": "code review\u548c\u8d28\u91cf\u7ba1\u7406",
    "style": "",
    "details": "",
    "subItems": [
      "\u5982\u4f55\u8bc4\u4f30\u4ee3\u7801\u7684\u597d\u4e0e\u574f\uff1f"
    ]
  },
  "116": {
    "title": "\u7814\u53d1\u89c4\u8303",
    "style": "",
    "details": "",
    "subItems": []
  },
  "117": {
    "title": "\u67b6\u6784\u8bc4\u5ba1\u600e\u4e48\u505a",
    "style": "",
    "details": "",
    "subItems": []
  },
  "118": {
    "title": "\u5fae\u670d\u52a1\u7cfb\u7edf\u76d1\u63a7",
    "style": "",
    "details": "",
    "subItems": []
  },
  "119": {
    "title": "\u6570\u636e\u5e93\u4f18\u5316\u6848\u4f8b",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u6d77\u91cf\u6570\u636e\u5e93\u8868\u5207\u6362\u65b9\u6848",
      "\u53cc\u5199+\u589e\u91cf\u8fc1\u79fb+\u7070\u5ea6\u5207\u6362\u65b9\u5f0f \u9879\u76ee\u5177\u4f53\u6d41\u7a0b",
      "TIDB\u4e3b\u952e\u7684\u751f\u6210\u539f\u7406\u4ee5\u53ca\u51fa\u73b0\u6027\u80fd\u95ee\u9898",
      "\u4e3a\u4ec0\u4e48\u9009\u62e9OceanBase\u66ff\u6362TiDB\uff1f",
      "\u4f55\u4e3a\u5927\u8868\u4ee5\u53ca\u4f18\u5316\u65b9\u6848\uff1f",
      "\u4e3a\u4ec0\u4e48OceanBase\u53ef\u4ee5\u5355\u8868\u652f\u6301\u5927\u8868\uff1f",
      "OceanBase\u7684\u4e3b\u952e\u751f\u6210\u7b56\u7565\u652f\u6301\u9ad8\u6027\u80fd\uff1f",
      "ES\u7684\u539f\u7406\uff0c\u4e3a\u4ec0\u4e48\u9ad8\u6027\u80fd\uff1f\u600e\u4e48\u5904\u7406\u6d77\u91cf\u6570\u636e\u7684",
      "MySQL\u548cOracle\u5bf9\u6bd4\uff0c\u91d1\u878d\u573a\u666f\u4f7f\u7528",
      "Flink\u51fa\u73b0\u6570\u636e\u5ef6\u8fdf\u539f\u56e0\u4ee5\u53ca\u89e3\u51b3\u65b9\u6848",
      "\u5199\u591a\u8bfb\u5c11\uff0c\u8bfb\u591a\u5199\u5c11\u6570\u636e\u5e93\u65b9\u6848"
    ]
  },
  "120": {
    "title": "\u5982\u4f55\u5e94\u5bf9\u7a81\u53d1\u6d41\u91cf",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u9879\u76ee\u51fa\u73b0\u7a81\u53d1\u6d41\u91cf\u5904\u7406"
    ]
  },
  "121": {
    "title": "\u9ad8\u5e76\u53d1\u7cfb\u7edf\u74f6\u9888",
    "style": "",
    "details": "",
    "subItems": []
  },
  "122": {
    "title": "\u5f3a\u4e00\u81f4\u6027\u65b9\u6848",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u4e24\u9636\u6bb5\u63d0\u4ea4\u7f3a\u70b9\u548c\u89e3\u51b3\u65b9\u6848",
      "\u5f3a\u4e00\u81f4\u6027\u7684\u89e3\u51b3\u65b9\u6848\uff0c\u4e3a\u4ec0\u4e48\u4e0d\u7528\u5206\u5e03\u5f0f\u4e8b\u52a1XA\uff1f",
      "TCC\u548cSaga\u7684\u89e3\u51b3\u65b9\u6848",
      "Seata\u4e00\u7ad9\u5f0f\u7684\u5206\u5e03\u5f0f\u89e3\u51b3\u65b9\u6848\u4ecb\u7ecd"
    ]
  },
  "123": {
    "title": "\u6700\u7ec8\u4e00\u81f4\u6027\u65b9\u6848",
    "style": "",
    "details": "",
    "subItems": [
      "\u672c\u5730\u4e8b\u52a1+Outbox\u65b9\u6848\uff0c\u4e3a\u4ec0\u4e48\u5f15\u5165\u672c\u5730\u4e8b\u52a1\u65e5\u5fd7\u8868\uff1f",
      "\u4e8b\u52a1\u65e5\u5fd7\u8868 + \u72b6\u6001\u673a\u7b56\u7565",
      "\u4e8b\u52a1\u65e5\u5fd7\u8868\u7206\u70b8\u4e86\u600e\u4e48\u529e\uff1f",
      "\u4e3a\u4ec0\u4e48\u4e0d\u7528MQ\u7684\u4e8b\u52a1\u6d88\u606f\uff1f",
      "TCC\u548cSaga\u7684\u89e3\u51b3\u65b9\u6848",
      "Seata\u4e00\u7ad9\u5f0f\u7684\u5206\u5e03\u5f0f\u89e3\u51b3\u65b9\u6848\u4ecb\u7ecd"
    ]
  },
  "124": {
    "title": "\u7cfb\u7edf\u96ea\u5d29\u5904\u7406\u65b9\u6848",
    "style": "",
    "details": "",
    "subItems": []
  },
  "125": {
    "title": "\u6392\u67e5\u4e00\u6b21\u8de8\u591a\u4e2a\u670d\u52a1\u7684\u6162\u8bf7\u6c42",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u9879\u76ee\u51fa\u73b0\u591a\u4e2a\u670d\u52a1\u6162\u8bf7\u6c42\uff0c\u5904\u7406\u65b9\u6848"
    ]
  },
  "126": {
    "title": "\u6d88\u606f\u79ef\u538b\u5982\u4f55\u5904\u7406",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u6d88\u606f\u5806\u79ef\u51fa\u73b0\u7684\u539f\u56e0\uff1f",
      "\u9879\u76ee\u51fa\u73b0\u6d88\u606f\u5806\u79ef\u5904\u7406\u65b9\u6848"
    ]
  },
  "127": {
    "title": "\u5982\u4f55\u4fdd\u8bc1\u6d88\u606f\u4e0d\u4e22\u3001\u4e0d\u91cd\u3001\u4e0d\u4e71",
    "style": "",
    "details": "",
    "subItems": []
  },
  "128": {
    "title": "\u591a\u7ea7\u7f13\u5b58\u8bbe\u8ba1",
    "style": "",
    "details": "",
    "subItems": [
      "\u63cf\u8ff0\u9879\u76ee\u7684\u591a\u7ea7\u7f13\u5b58\u8bbe\u8ba1"
    ]
  },
  "129": {
    "title": "\u7f13\u5b58\u95ee\u9898\u5904\u7406",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u7f13\u5b58\u600e\u4e48\u4fdd\u6301\u6570\u636e\u4e00\u81f4\u6027\uff1f",
      "\u7f13\u5b58\u7a7f\u900f\u3001\u7f13\u5b58\u96ea\u5d29\u548c\u7f13\u5b58\u5931\u6548\u600e\u4e48\u5904\u7406\uff1f",
      "\u70ed\u70b9\u6570\u636e\u7f13\u5b58\u600e\u4e48\u8bbe\u8ba1\uff1f\u600e\u4e48\u9884\u70ed\uff1f",
      "\u5206\u5e03\u5f0f\u7f13\u5b58\u95ee\u9898\u4ee5\u53ca\u89e3\u51b3\u65b9\u6848"
    ]
  },
  "130": {
    "title": "\u9ad8\u5e76\u53d1\u652f\u4ed8\u7cfb\u7edf\u8bbe\u8ba1",
    "style": "",
    "details": "",
    "subItems": []
  },
  "131": {
    "title": "\u79d2\u6740\u7cfb\u7edf\u8bbe\u8ba1",
    "style": "",
    "details": "",
    "subItems": [
      "\u9ad8\u5e76\u53d1\u652f\u4ed8\u95ee\u9898\u600e\u4e48\u5904\u7406\uff1f",
      "\u5982\u679c\u4fdd\u8bc1\u5e93\u5b58\u4e0d\u8d85\u5356\uff1f",
      "\u600e\u4e48\u505a\u6d41\u91cf\u524a\u5cf0\uff1f",
      "Redis\u6302\u4e86\u600e\u4e48\u529e\uff1f"
    ]
  },
  "132": {
    "title": "\u9ad8\u5e76\u53d1\u8ba2\u5355\u7cfb\u7edf\u8bbe\u8ba1",
    "style": "",
    "details": "",
    "subItems": [
      "\u5982\u679c\u4fdd\u8bc1\u5e93\u5b58\u4e0d\u8d85\u5356\uff1f"
    ]
  },
  "133": {
    "title": "\u5206\u5e93\u5206\u8868 \u573a\u666f\u548c\u65b9\u6848",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u5206\u5e93\u5206\u8868\u7684\u7c7b\u578b\u548c\u539f\u5219\u662f\u4ec0\u4e48\uff1f",
      "\u5728\u4ec0\u4e48\u60c5\u51b5\u4e0b\u4f7f\u7528\u5206\u5e93\u5206\u8868\u6bd4\u8f83\u5408\u7406\uff1f",
      "\u5206\u5e93\u5206\u8868 JDBC-shading\u65b9\u6848",
      "\u5931\u8d25\u4e86\u600e\u4e48\u67e5\u8be2\u9ed8\u8ba4\u8868\uff1f",
      "\u5206\u5e93\u5206\u8868\u600e\u4e48\u89e3\u51b3\u591a\u5b57\u6bb5\u67e5\u8be2\uff1f",
      "Oracle\u53ef\u4ee5\u505a\u5206\u5e93\u5206\u8868\u5417"
    ]
  },
  "134": {
    "title": "\u7cfb\u7edf\u8bbe\u8ba1\u539f\u5219\u548c\u8003\u91cf\u70b9",
    "style": "",
    "details": "",
    "subItems": []
  },
  "135": {
    "title": "DDD\u8bbe\u8ba1\u4ecb\u7ecd",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u4e3a\u4ec0\u4e48\u8981\u7528DDD\uff1f",
      "DDD\u548c\u4f20\u7edf\u4e09\u5c42\u67b6\u6784\u6709\u4ec0\u4e48\u533a\u522b\uff1f",
      "\u4ec0\u4e48\u662f\u5145\u8840\u6a21\u578b\uff1f\u4e3a\u4ec0\u4e48DDD\u4f7f\u7528\u8fd9\u79cd\u6a21\u578b\uff1f",
      "\u4ec0\u4e48\u662f\u9886\u57df\u6a21\u578b\uff1f\u7531\u54ea\u4e9b\u5143\u7d20\u7ec4\u6210\uff1f",
      "Entity\u548cValue Object\u7684\u533a\u522b\uff1f",
      "\u4ec0\u4e48\u662f\u805a\u5408\uff1f\u4e3a\u4ec0\u4e48\u9700\u8981\u805a\u5408\uff1f",
      "\u805a\u5408\u8bbe\u8ba1\u8fc7\u5927\u6216\u8fc7\u5c0f\u6709\u4ec0\u4e48\u95ee\u9898\uff1f",
      "\u4ec0\u4e48\u662f\u9650\u754c\u4e0a\u4e0b\u6587\uff1f\u4e3a\u4ec0\u4e48\u91cd\u8981\uff1f",
      "\u4f60\u662f\u5982\u4f55\u5212\u5206\u9650\u754c\u4e0a\u4e0b\u6587\u7684\uff1f",
      ">>>DDD\u7684\u5206\u5c42\u7ed3\u6784\u662f\u600e\u4e48\u6837\u7684\uff1f",
      "App Service\u548cDomain service\u7684\u533a\u522b\uff1f",
      "\u4ec0\u4e48\u662f\u9886\u57df\u4e8b\u4ef6\uff1f",
      "\u4f60\u7684\u9879\u76ee\u4e2d\u662f\u5982\u4f55\u843d\u5730DDD\u7684\uff1f",
      "DDD\u5b9e\u8df5\u4e2d\u9047\u5230\u7684\u6700\u5927\u56f0\u96be\uff1f",
      "\u4ec0\u4e48\u65f6\u5019\u4e0d\u9002\u5408DDD\uff1f",
      "DDD\u4f1a\u4e0d\u4f1a\u5f71\u54cd\u5f00\u53d1\u6548\u7387\uff1f",
      "DDD\u662f\u5426\u7b49\u4e8e\u5fae\u670d\u52a1\uff1f",
      "\u9886\u57df\u6a21\u578b\u548cORM\u5982\u4f55\u914d\u5408\uff1f"
    ]
  },
  "136": {
    "title": "\u600e\u4e48\u63d0\u9ad8\u7cfb\u7edf\u53ef\u6269\u5c55\u6027",
    "style": "",
    "details": "",
    "subItems": []
  },
  "137": {
    "title": "\u9ad8\u6027\u80fd\u9ad8\u5e76\u53d1\u7cfb\u7edf\u8bbe\u8ba1",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "138": {
    "title": "\u53d1\u5e03\u65b9\u5f0f\u548c\u90e8\u7f72\u5468\u671f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "139": {
    "title": "\u7cfb\u7edf\u600e\u4e48\u505a\u76d1\u63a7\u7684",
    "style": "",
    "details": "",
    "subItems": []
  },
  "140": {
    "title": "Docker\u548cK8S",
    "style": "",
    "details": "",
    "subItems": []
  },
  "141": {
    "title": "\u5fae\u670d\u52a1\u67b6\u6784\u8bbe\u8ba1",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u5fae\u670d\u52a1 \u80cc\u666f \u4f18\u7f3a\u70b9",
      "\u5fae\u670d\u52a1\u62c6\u5206\u539f\u5219",
      "\u670d\u52a1\u6ce8\u518c\u4e0e\u53d1\u73b0 Eureka+Nacos",
      "\u9650\u6d41 \u7194\u65ad \u964d\u7ea7\u600e\u4e48\u505a",
      "\u5fae\u670d\u52a1\u8d1f\u8f7d\u5747\u8861\u600e\u4e48\u505a",
      "Nacos\u914d\u7f6e\u539f\u7406",
      "\u94fe\u8def \u670d\u52a1\u7f51\u5173\u8def\u7531\u539f\u7406",
      "RPC\u539f\u7406\u548c\u5b9e\u73b0\u6846\u67b6",
      "\u5982\u4f55\u4fdd\u8bc1\u63a5\u53e3\u5e42\u7b49"
    ]
  },
  "142": {
    "title": "\u5982\u4f55\u7406\u89e3\u5927\u6a21\u578b",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u548c\u4f20\u7edf\u7a0b\u5e8f\u7684\u533a\u522b\uff1f",
      "\u89e3\u91ca\u53c2\u6570 \u53c2\u6570\u89c4\u6a21 Token",
      "GPT\u3001LLaMA\u5927\u6a21\u578b\u9002\u5408\u505a\u4ec0\u4e48\uff1f"
    ]
  },
  "143": {
    "title": "AI\u548c\u540e\u7aef\u7cfb\u7edf\u7684\u5173\u7cfb",
    "style": "",
    "details": "",
    "subItems": []
  },
  "144": {
    "title": "\u5982\u4f55\u8bbe\u8ba1\u4e00\u4e2a\u57fa\u4e8eLLM\u7684\u540e\u7aef\u7cfb\u7edf",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "146": {
    "title": "\u4ec0\u4e48\u662fAgent\u667a\u80fd\u4f53",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u548c\u666e\u901aChat\u7684\u533a\u522b\uff1f",
      "Agent\u67b6\u6784"
    ]
  },
  "147": {
    "title": "RAG\u548c\u5411\u91cf\u6570\u636e\u5e93",
    "style": "",
    "details": "",
    "subItems": [
      "\u4e3a\u4ec0\u4e48\u9700\u8981RAG\u548c\u5411\u91cf\u6570\u636e\u5e93\uff1f",
      "\u5982\u4f55\u9009\u62e9\u5411\u91cf\u6570\u636e\u5e93\uff1f"
    ]
  },
  "148": {
    "title": "\u63d0\u793a\u5de5\u7a0b \u6838\u5fc3\u539f\u5219",
    "style": "",
    "details": "",
    "subItems": []
  },
  "149": {
    "title": "LangChain\u6846\u67b6",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "150": {
    "title": "FastGPT\u6982\u8ff0\u4e0e\u6838\u5fc3\u4ef7\u503c",
    "style": "",
    "details": "",
    "subItems": []
  },
  "151": {
    "title": "LLM\u4ea7\u751f\u5e7b\u89c9\u600e\u4e48\u907f\u514d",
    "style": "",
    "details": "",
    "subItems": []
  },
  "152": {
    "title": "Java\u5982\u4f55\u9ad8\u5e76\u53d1\u5b89\u5168\u8c03\u7528LLM",
    "style": "",
    "details": "",
    "subItems": []
  },
  "153": {
    "title": "\u5982\u4f55\u5728AI\u5e94\u7528\u4e2d\u505a\u7f13\u5b58",
    "style": "",
    "details": "",
    "subItems": []
  },
  "154": {
    "title": "AI\u670d\u52a1\u600e\u4e48\u505a\u76d1\u63a7\u548c\u6210\u672c\u63a7\u5236",
    "style": "",
    "details": "",
    "subItems": []
  },
  "155": {
    "title": "AI\u8f93\u51fa\u9020\u6210\u4e1a\u52a1\u5f71\u54cd\uff0c\u8c01\u8d1f\u8d23\uff1f",
    "style": "",
    "details": "",
    "subItems": [
      "\u7cfb\u7edf\u5982\u4f55\u8bbe\u8ba1\uff1f"
    ]
  },
  "156": {
    "title": "AI\u8de8\u884c\u4e1a\u7ecf\u9a8c\u590d\u5236\u4e0e\u5e94\u7528",
    "style": "",
    "details": "",
    "subItems": []
  },
  "157": {
    "title": "\u600e\u4e48\u770b\u5f85AI\u53d6\u4ee3\u7a0b\u5e8f\u5458",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "158": {
    "title": "\u81ea\u6211\u4ecb\u7ecd",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "159": {
    "title": "\u82f1\u6587\u53e3\u8bed\u81ea\u6211\u4ecb\u7ecd",
    "style": "",
    "details": "",
    "subItems": []
  },
  "160": {
    "title": "\u4e3a\u4ec0\u4e48\u60f3\u52a0\u5165\u6211\u4eec\u516c\u53f8\uff1f",
    "style": "\u4e3a\u4ec0\u4e48\u60f3\u52a0\u5165\u6211\u4eec\u516c\u53f8\uff1f",
    "details": "",
    "subItems": []
  },
  "161": {
    "title": "\u80fd\u7ed9\u6211\u4eec\u5e26\u6765\u4ec0\u4e48\uff1f\n\u4e3a\u4ec0\u4e48\u96c7\u4f63\u4f60\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "162": {
    "title": "\u4e0a\u4efd\u5de5\u4f5c\u6700\u5927\u6536\u83b7\u662f\u4ec0\u4e48\uff1f",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "163": {
    "title": "\u65b0\u52a0\u5165\u5bf9\u4f60\u6709\u4ec0\u4e48\u6311\u6218\uff1f\n\u600e\u4e48\u5f00\u5c55\u5de5\u4f5c\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "164": {
    "title": "\u5982\u679c\u52a0\u5165\u6211\u4eec\uff0c\n\u4f60\u5e0c\u671b\u505a\u54ea\u4e9b\u6311\u6218\u6027\u7684\u4e8b\u60c5\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "165": {
    "title": "\u4f60\u66f4\u504f\u6280\u672f\u6df1\u8015\uff0c\u8fd8\u662f\u613f\u610f\u8f6c\u7ba1\u7406\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "166": {
    "title": "\u4f60\u672a\u67653/5\u5e74\u7684\u804c\u4e1a\u76ee\u6807\u662f\u4ec0\u4e48\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "167": {
    "title": "\u4f60\u662f\u5982\u4f55\u5b89\u6392\u4e2a\u4eba\u6210\u957f\u65f6\u95f4\u7684\uff1f",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "168": {
    "title": "\u4f60\u6700\u5927\u7684\u4f18\u70b9\u662f\u4ec0\u4e48\uff1f\n\u77ed\u677f\u6216\u5f85\u6539\u8fdb\u7684\u5730\u65b9\u662f\u4ec0\u4e48\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "169": {
    "title": "\u4f60\u5e26\u8fc7\u7684\u56e2\u961f\u89c4\u6a21\u662f\u591a\u5c11\uff1f\n\u5982\u4f55\u7ba1\u7406\u56e2\u961f\u7684\u6280\u672f\u6210\u957f\u548c\u4ea4\u4ed8\u8fdb\u5ea6\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "170": {
    "title": "\u5982\u4f55\u7ba1\u7406\u7814\u53d1\u56e2\u961f\uff1f",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u5bf9\u4e8e\u56e2\u961f\u7ba1\u7406\uff0c\u4f60\u6709\u4ec0\u4e48\u60f3\u6cd5\uff1f",
      "\u5982\u4f55\u8861\u91cf\u4e00\u4e2a\u4eba\u7684\u597d\u4e0e\u574f\uff1f",
      "\u5982\u4f55\u63d0\u5347\u56e2\u961f\u7684\u6574\u4f53\u80fd\u529b\uff1f"
    ]
  },
  "171": {
    "title": "\u56e2\u961f\u7ba1\u7406\u600e\u4e48\u5206\u5de5\u534f\u4f5c\uff1f",
    "style": "",
    "details": "",
    "subItems": [
      "\u600e\u4e48\u5206\u914d\u4efb\u52a1\u80fd\u4fdd\u8bc1\u65b0\u4eba\u6210\u957f\uff1f",
      "OKR\u600e\u4e48\u5236\u5b9a\uff1fOKR\u5b8c\u6210\u4e0d\u4e86\u600e\u4e48\u5904\u7406\uff1f"
    ]
  },
  "172": {
    "title": "\u600e\u4e48\u8861\u91cf\u5458\u5de5\u7684\u7ee9\u6548\uff1f\n\u5982\u679c\u4e0b\u5c5e\u7ee9\u6548\u4e0d\u8fbe\u6807\uff0c\u600e\u4e48\u505aPIP",
    "style": "",
    "details": "",
    "subItems": [
      "\u600e\u4e48\u9762\u8c08\u4e0d\u597d\u7684\u7ee9\u6548\uff1f"
    ]
  },
  "173": {
    "title": "\u5728\u4e00\u4e2a\u9879\u76ee\u4e2d\uff0c\u4f60\u662f\u5982\u4f55\u6743\u8861\n\u4e1a\u52a1\u9700\u6c42\u4e0e\u6280\u672f\u5b9e\u73b0\u7684\u590d\u6742\u5ea6\uff1f",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "174": {
    "title": "\u9879\u76ee\u5ef6\u671f\u65f6\uff0c\u4f60\u4f1a\u600e\u4e48\n\u5411\u4e0a\u6c47\u62a5\u5e76\u534f\u8c03\u8d44\u6e90\uff1f",
    "style": "",
    "details": "",
    "subItems": [
      "\u8d44\u6e90\u534f\u8c03\u6709\u4ec0\u4e48\u7ecf\u9a8c\uff1f"
    ]
  },
  "175": {
    "title": "\u4f60\u662f\u66f4\u559c\u6b22\u72ec\u7acb\u5b8c\u6210\u4efb\u52a1\uff0c\n\u8fd8\u662f\u548c\u56e2\u961f\u534f\u4f5c\uff1f\u4e3a\u4ec0\u4e48\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "176": {
    "title": "\u9047\u5230\u4ea7\u54c1\u7ecf\u7406\u63d0\u51fa\u4e0d\u5408\u7406\u9700\u6c42\u65f6\uff0c\n\u4f60\u600e\u4e48\u6c9f\u901a\uff1f",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "177": {
    "title": "\u6709\u6ca1\u6709\u9047\u5230\u8fc7\u7ebf\u4e0a\u4e8b\u6545\uff1f\n\u4f60\u662f\u600e\u4e48\u590d\u76d8\u548c\u63a8\u52a8\u6539\u8fdb\u7684\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "178": {
    "title": "\u8bf7\u8c08\u8c08\u4f60\u5728\u9879\u76ee\u4e2d\u662f\u5982\u4f55\n\u5f71\u54cd\u5176\u4ed6\u56e2\u961f\u7684\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "179": {
    "title": "\u4f60\u6709\u6ca1\u6709\u63a8\u52a8\u8fc7\u6280\u672f\u5347\u7ea7\uff1f\n\u662f\u5982\u4f55\u8bf4\u670d\u7ba1\u7406\u5c42\u7684\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "180": {
    "title": "\u5f53\u53d1\u73b0\u73b0\u6709\u7cfb\u7edf\u67b6\u6784\u9762\u4e34\u4e25\u91cd\u7684\n\u6280\u672f\u503a\uff0c\u4f46\u4e1a\u52a1\u4e0a\u7ebf\u538b\u529b\u5f88\u5927\uff0c\u4f60\u5982\u4f55\u9009",
    "style": "",
    "details": "",
    "subItems": []
  },
  "181": {
    "title": "\u4f60\u600e\u4e48\u770b\u5f85996\u6216\u9ad8\u5f3a\u5ea6\u5de5\u4f5c\uff1f\n\u600e\u6837\u5e73\u8861\u6548\u7387\u4e0e\u53ef\u6301\u7eed\u53d1\u5c55\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "182": {
    "title": "\u5783\u573e\u56de\u6536\u5668\u6709\u54ea\u4e9b",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u5206\u4ee3\u5206\u533a\u548c\u65b0\u8001\u751f\u4ee3\u7684\u56de\u6536\u5668",
      "CMS\u6536\u96c6\u5668\u548cG1\u6536\u96c6\u5668",
      "\u5b83\u4eec\u6709\u4ec0\u4e48\u4f18\u7f3a\u70b9\uff1f",
      "\u65b0\u4e00\u4ee3jdk\u4f7f\u7528\u4ec0\u4e48\u6536\u96c6\u5668\uff1f\u4e3a\u4ec0\u4e48\uff1f"
    ]
  },
  "183": {
    "title": "\u9879\u76ee\u4e2d\u89e3\u51b3\u670d\u52a1\u5316\u7684\u6280\u672f\u95ee\u9898",
    "style": "background-color: yellow;",
    "details": "\u5728\u670d\u52a1\u5316\u5de5\u4f5c\u6d41\u9879\u76ee\u4e2d\uff0c\u89e3\u51b3\u6280\u672f\u95ee\u9898\u9700\u8981\u4ece\u67b6\u6784\u8bbe\u8ba1\u3001\u6570\u636e\u4e00\u81f4\u6027\u3001\u6027\u80fd\u4f18\u5316\u3001\u5bb9\u9519\u5904\u7406\u3001\u76d1\u63a7\u544a\u8b66\u4e94\u4e2a\u7ef4\u5ea6\u8fdb\u884c\u7cfb\u7edf\u6027\u6cbb\u7406\u3002\n\n\u4e00\u3001\u67b6\u6784\u8bbe\u8ba1\u95ee\u9898\u4e0e\u89e3\u51b3\u65b9\u6848\n\u95ee\u98981\uff1a\u670d\u52a1\u62c6\u5206\u8fb9\u754c\u4e0d\u6e05\u6670\n\u2022 \u75c7\u72b6\uff1a\u670d\u52a1\u95f4\u8c03\u7528\u94fe\u8fc7\u957f\u3001\u5faa\u73af\u4f9d\u8d56\u3001\u670d\u52a1\u804c\u8d23\u6a21\u7cca\n\u2022 \u89e3\u51b3\u65b9\u6848\uff1a\u4e0b\u9762\n\n\u95ee\u98982\uff1a\u670d\u52a1\u6ce8\u518c\u4e0e\u53d1\u73b0\u5931\u6548\n\u2022 \u75c7\u72b6\uff1a\u670d\u52a1\u8c03\u7528\u5931\u8d25\u3001\u8d1f\u8f7d\u4e0d\u5747\u8861\n\u2022 \u89e3\u51b3\u65b9\u6848\uff1a\u4e0b\u9762\n\n\u4e8c\u3001\u6570\u636e\u4e00\u81f4\u6027\u95ee\u9898\u4e0e\u89e3\u51b3\u65b9\u6848\n\u95ee\u98983\uff1a\u5206\u5e03\u5f0f\u4e8b\u52a1\u6570\u636e\u4e0d\u4e00\u81f4\n\u2022 \u75c7\u72b6\uff1a\u8de8\u670d\u52a1\u4e8b\u52a1\u5931\u8d25\uff0c\u6570\u636e\u72b6\u6001\u4e0d\u4e00\u81f4\n\u2022 \u89e3\u51b3\u65b9\u6848\uff1a\u4e0b\u9762\n\n\u95ee\u98984\uff1a\u7f13\u5b58\u4e0e\u6570\u636e\u5e93\u4e0d\u4e00\u81f4\n\u2022 \u75c7\u72b6\uff1a\u7f13\u5b58\u6570\u636e\u8fc7\u671f\u6216\u810f\u6570\u636e\n\u2022 \u89e3\u51b3\u65b9\u6848\uff1a\u4e0b\u9762\n\n\u4e09\u3001\u6027\u80fd\u4f18\u5316\u95ee\u9898\u4e0e\u89e3\u51b3\u65b9\u6848\n\u95ee\u98985\uff1a\u670d\u52a1\u8c03\u7528\u94fe\u8fc7\u957f\u5bfc\u81f4\u54cd\u5e94\u6162\n\u2022 \u75c7\u72b6\uff1a\u63a5\u53e3\u54cd\u5e94\u65f6\u95f4\u8d85\u8fc7\u9608\u503c\uff0c\u7528\u6237\u4f53\u9a8c\u5dee\n\u2022 \u89e3\u51b3\u65b9\u6848\uff1a\u4e0b\u9762\n\n\u95ee\u98986\uff1a\u6570\u636e\u5e93\u6210\u4e3a\u74f6\u9888\n\u2022 \u75c7\u72b6\uff1a\u6570\u636e\u5e93\u8fde\u63a5\u6c60\u6ee1\u3001\u6162\u67e5\u8be2\u9891\u53d1\n\u2022 \u89e3\u51b3\u65b9\u6848\uff1a\u4e0b\u9762\n\n\u56db\u3001\u5bb9\u9519\u4e0e\u7a33\u5b9a\u6027\u95ee\u9898\n\u95ee\u98987\uff1a\u670d\u52a1\u96ea\u5d29\u6548\u5e94\n\u2022 \u75c7\u72b6\uff1a\u4e00\u4e2a\u670d\u52a1\u6545\u969c\u5bfc\u81f4\u6574\u4e2a\u7cfb\u7edf\u762b\u75ea\n\u2022 \u89e3\u51b3\u65b9\u6848\uff1a\u4e0b\u9762\n\n\u95ee\u98988\uff1a\u914d\u7f6e\u7ba1\u7406\u6df7\u4e71\n\u2022 \u75c7\u72b6\uff1a\u914d\u7f6e\u53d8\u66f4\u9700\u8981\u91cd\u542f\u670d\u52a1\uff0c\u914d\u7f6e\u7248\u672c\u4e0d\u4e00\u81f4\n\u2022 \u89e3\u51b3\u65b9\u6848\uff1a\u4e0b\u9762\n\n\u4e94\u3001\u76d1\u63a7\u4e0e\u8fd0\u7ef4\u95ee\u9898\n\u95ee\u98989\uff1a\u95ee\u9898\u5b9a\u4f4d\u56f0\u96be\n\u2022 \u75c7\u72b6\uff1a\u6545\u969c\u53d1\u751f\u65f6\u65e0\u6cd5\u5feb\u901f\u5b9a\u4f4d\u6839\u56e0\n\u2022 \u89e3\u51b3\u65b9\u6848\uff1a\u4e0b\u9762\n\n\u95ee\u989810\uff1a\u90e8\u7f72\u4e0e\u53d1\u5e03\u95ee\u9898\n\u2022 \u75c7\u72b6\uff1a\u53d1\u5e03\u5931\u8d25\u3001\u56de\u6eda\u56f0\u96be\n\u2022 \u89e3\u51b3\u65b9\u6848\uff1a\u4e0b\u9762\n\n\u516d\u3001\u6700\u4f73\u5b9e\u8df5\u603b\u7ed3\n1. \u8bbe\u8ba1\u9636\u6bb5\uff1a\u660e\u786e\u670d\u52a1\u8fb9\u754c\uff0c\u5b9a\u4e49\u6e05\u6670\u7684\u63a5\u53e3\u5951\u7ea6\n2. \u5f00\u53d1\u9636\u6bb5\uff1a\u5b9e\u73b0\u5e42\u7b49\u6027\u3001\u91cd\u8bd5\u673a\u5236\u3001\u7194\u65ad\u964d\u7ea7\n3. \u6d4b\u8bd5\u9636\u6bb5\uff1a\u8fdb\u884c\u538b\u529b\u6d4b\u8bd5\u3001\u6df7\u6c8c\u6d4b\u8bd5\uff0c\u9a8c\u8bc1\u5bb9\u9519\u80fd\u529b\n4. \u8fd0\u7ef4\u9636\u6bb5\uff1a\u5efa\u7acb\u5b8c\u5584\u7684\u76d1\u63a7\u544a\u8b66\u4f53\u7cfb\uff0c\u5feb\u901f\u54cd\u5e94\u95ee\u9898\n5. \u6301\u7eed\u4f18\u5316\uff1a\u5b9a\u671freview\u67b6\u6784\uff0c\u6839\u636e\u4e1a\u52a1\u53d1\u5c55\u8c03\u6574\u6280\u672f\u65b9\u6848\n\n\u901a\u8fc7\u4ee5\u4e0a\u7cfb\u7edf\u6027\u6cbb\u7406\uff0c\u53ef\u4ee5\u6709\u6548\u89e3\u51b3\u670d\u52a1\u5316\u5de5\u4f5c\u6d41\u4e2d\u7684\u5404\u7c7b\u6280\u672f\u95ee\u9898\uff0c\u6784\u5efa\u7a33\u5b9a\u3001\u9ad8\u6027\u80fd\u7684\u5206\u5e03\u5f0f\u7cfb\u7edf\u3002",
    "subItems": [
      "\u4e00\u3001\u67b6\u6784\u8bbe\u8ba1\u95ee\u9898\u4e0e\u89e3\u51b3\u65b9\u6848: \u670d\u52a1\u62c6\u5206\u8fb9\u754c\u4e0d\u6e05\u6670+\u670d\u52a1\u6ce8\u518c\u4e0e\u53d1\u73b0\u5931\u6548",
      "\u91c7\u7528\u9886\u57df\u9a71\u52a8\u8bbe\u8ba1\uff08DDD\uff09\uff0c\u6309\u4e1a\u52a1\u57df\u5212\u5206\u670d\u52a1\u8fb9\u754c",
      "\u5b9a\u4e49\u6e05\u6670\u7684\u670d\u52a1\u5951\u7ea6\uff0c\u4f7f\u7528OpenAPI\u89c4\u8303\u63a5\u53e3",
      "\u5efa\u7acb\u670d\u52a1\u6cbb\u7406\u5e73\u53f0\uff0c\u53ef\u89c6\u5316\u670d\u52a1\u4f9d\u8d56\u5173\u7cfb",
      "\u5b9e\u65bd\u670d\u52a1\u964d\u7ea7\u7b56\u7565\uff0c\u907f\u514d\u7ea7\u8054\u6545\u969c",
      "\u4f7f\u7528Nacos\u4f5c\u4e3a\u670d\u52a1\u6ce8\u518c\u4e2d\u5fc3\uff0c\u652f\u6301\u5065\u5eb7\u68c0\u67e5",
      "\u914d\u7f6e\u5ba2\u6237\u7aef\u8d1f\u8f7d\u5747\u8861\uff08\u5982Ribbon\uff09\u6216\u670d\u52a1\u7aef\u8d1f\u8f7d\u5747\u8861\uff08\u5982Istio\uff09",
      "\u5b9e\u73b0\u670d\u52a1\u7194\u65ad\uff08Hystrix/Sentinel\uff09\uff0c\u9632\u6b62\u96ea\u5d29\u6548\u5e94",
      "\u8bbe\u7f6e\u91cd\u8bd5\u673a\u5236\uff0c\u4f46\u9700\u914d\u5408\u5e42\u7b49\u6027\u8bbe\u8ba1",
      "\u4e8c\u3001\u6570\u636e\u4e00\u81f4\u6027\u95ee\u9898\u4e0e\u89e3\u51b3\u65b9\u6848: \u5206\u5e03\u5f0f\u4e8b\u52a1\u6570\u636e\u4e0d\u4e00\u81f4+\u7f13\u5b58\u4e0e\u6570\u636e\u5e93\u4e0d\u4e00\u81f4",
      "\u6700\u7ec8\u4e00\u81f4\u6027\u65b9\u6848\uff1a\u4f7f\u7528\u6d88\u606f\u961f\u5217\uff08Kafka/RocketMQ\uff09\u5b9e\u73b0\u5f02\u6b65\u8865\u507f",
      "TCC\u6a21\u5f0f\uff1aTry-Confirm-Cancel\u4e09\u9636\u6bb5\u63d0\u4ea4\uff0c\u9002\u7528\u4e8e\u5f3a\u4e00\u81f4\u6027\u573a\u666f",
      "Saga\u6a21\u5f0f\uff1a\u957f\u4e8b\u52a1\u62c6\u5206\uff0c\u6bcf\u4e2a\u6b65\u9aa4\u53ef\u8865\u507f\uff0c\u9002\u5408\u4e1a\u52a1\u6d41\u7a0b",
      "\u672c\u5730\u6d88\u606f\u8868\uff1a\u4e1a\u52a1\u4e0e\u6d88\u606f\u8868\u5728\u540c\u4e00\u4e2a\u4e8b\u52a1\uff0c\u901a\u8fc7\u5b9a\u65f6\u4efb\u52a1\u91cd\u8bd5",
      "Cache-Aside\u6a21\u5f0f\uff1a\u5148\u8bfb\u7f13\u5b58\uff0c\u672a\u547d\u4e2d\u8bfb\u6570\u636e\u5e93\u5e76\u56de\u5199\u7f13\u5b58",
      "Write-Through\u6a21\u5f0f\uff1a\u5199\u6570\u636e\u5e93\u540c\u65f6\u5199\u7f13\u5b58\uff0c\u4fdd\u8bc1\u5f3a\u4e00\u81f4\u6027",
      "\u5ef6\u8fdf\u53cc\u5220\uff1a\u66f4\u65b0\u6570\u636e\u5e93\u540e\u5220\u9664\u7f13\u5b58\uff0c\u5ef6\u8fdf\u518d\u6b21\u5220\u9664",
      "\u8bbe\u7f6e\u5408\u7406\u7684\u8fc7\u671f\u65f6\u95f4\uff0c\u7ed3\u5408\u4e3b\u52a8\u5237\u65b0\u7b56\u7565",
      "\u4e09\u3001\u6027\u80fd\u4f18\u5316\u95ee\u9898\u4e0e\u89e3\u51b3\u65b9\u6848: \u670d\u52a1\u8c03\u7528\u94fe\u8fc7\u957f\u5bfc\u81f4\u54cd\u5e94\u6162+\u6570\u636e\u5e93\u6210\u4e3a\u74f6\u9888",
      "\u5f02\u6b65\u5316\u6539\u9020\uff1a\u975e\u6838\u5fc3\u4e1a\u52a1\u5f02\u6b65\u5904\u7406\uff0c\u5982\u53d1\u9001\u77ed\u4fe1\u3001\u8bb0\u5f55\u65e5\u5fd7",
      "\u6279\u91cf\u5904\u7406\uff1a\u5408\u5e76\u591a\u4e2a\u8bf7\u6c42\uff0c\u51cf\u5c11\u7f51\u7edc\u5f00\u9500",
      "\u6570\u636e\u9884\u52a0\u8f7d\uff1a\u70ed\u70b9\u6570\u636e\u9884\u52a0\u8f7d\u5230\u7f13\u5b58",
      "\u670d\u52a1\u5408\u5e76\uff1a\u5bf9\u9ad8\u9891\u8c03\u7528\u7684\u670d\u52a1\u8fdb\u884c\u5408\u7406\u5408\u5e76",
      "\u8bfb\u5199\u5206\u79bb\uff1a\u4e3b\u5e93\u5199\uff0c\u4ece\u5e93\u8bfb\uff0c\u51cf\u8f7b\u4e3b\u5e93\u538b\u529b",
      "\u5206\u5e93\u5206\u8868\uff1a\u6309\u4e1a\u52a1\u7ef4\u5ea6\u62c6\u5206\uff0c\u5982\u6309\u7528\u6237ID\u5206\u7247",
      "\u7d22\u5f15\u4f18\u5316\uff1a\u5206\u6790\u6162\u67e5\u8be2\u65e5\u5fd7\uff0c\u6dfb\u52a0\u5408\u9002\u7d22\u5f15",
      "\u8fde\u63a5\u6c60\u4f18\u5316\uff1a\u5408\u7406\u914d\u7f6e\u8fde\u63a5\u6c60\u5927\u5c0f\u3001\u8d85\u65f6\u65f6\u95f4",
      "\u56db\u3001\u5bb9\u9519\u4e0e\u7a33\u5b9a\u6027\u95ee\u9898: \u670d\u52a1\u96ea\u5d29\u6548\u5e94+\u914d\u7f6e\u7ba1\u7406\u6df7\u4e71",
      "\u670d\u52a1\u7194\u65ad\uff1a\u5f53\u5931\u8d25\u7387\u8d85\u8fc7\u9608\u503c\uff0c\u81ea\u52a8\u7194\u65ad\uff0c\u5feb\u901f\u5931\u8d25",
      "\u670d\u52a1\u964d\u7ea7\uff1a\u8fd4\u56de\u515c\u5e95\u6570\u636e\u6216\u9ed8\u8ba4\u503c\uff0c\u4fdd\u8bc1\u6838\u5fc3\u529f\u80fd\u53ef\u7528",
      "\u9650\u6d41\u4fdd\u62a4\uff1a\u4f7f\u7528\u4ee4\u724c\u6876\u6216\u6f0f\u6876\u7b97\u6cd5\u9650\u5236\u8bf7\u6c42\u901f\u7387",
      "\u8d85\u65f6\u63a7\u5236\uff1a\u8bbe\u7f6e\u5408\u7406\u7684\u8c03\u7528\u8d85\u65f6\u65f6\u95f4\uff0c\u907f\u514d\u8d44\u6e90\u5360\u7528",
      "\u914d\u7f6e\u4e2d\u5fc3\uff1a\u4f7f\u7528Nacos\u7ba1\u7406\u914d\u7f6e\uff0c\u652f\u6301\u52a8\u6001\u5237\u65b0",
      "\u914d\u7f6e\u7248\u672c\u63a7\u5236\uff1aGit\u7ba1\u7406\u914d\u7f6e\uff0c\u652f\u6301\u56de\u6eda",
      "\u914d\u7f6e\u7070\u5ea6\u53d1\u5e03\uff1a\u5148\u5c0f\u8303\u56f4\u9a8c\u8bc1\uff0c\u518d\u5168\u91cf\u53d1\u5e03",
      "\u4e94\u3001\u76d1\u63a7\u4e0e\u8fd0\u7ef4\u95ee\u9898: \u95ee\u9898\u5b9a\u4f4d\u56f0\u96be+\u90e8\u7f72\u4e0e\u53d1\u5e03\u95ee\u9898",
      "\u5168\u94fe\u8def\u8ffd\u8e2a\uff1a\u96c6\u6210SkyWalking\uff0c\u8ffd\u8e2a\u8bf7\u6c42\u94fe\u8def",
      "\u4f7f\u7528\u963f\u91cc\u4e91\u65e5\u5fd7/ELK/EFK\u6536\u96c6\u548c\u5206\u6790\u65e5\u5fd7",
      "\u6307\u6807\u76d1\u63a7\uff1aPrometheus + Grafana\u76d1\u63a7\u5173\u952e\u6307\u6807",
      "\u544a\u8b66\u4f53\u7cfb\uff1a\u914d\u7f6e\u591a\u7ea7\u544a\u8b66\uff0c\u53ca\u65f6\u53d1\u73b0\u95ee\u9898",
      "\u84dd\u7eff\u90e8\u7f72\uff1a\u65b0\u65e7\u7248\u672c\u540c\u65f6\u8fd0\u884c\uff0c\u6d41\u91cf\u5207\u6362",
      "\u91d1\u4e1d\u96c0\u53d1\u5e03\uff1a\u5148\u5c0f\u6d41\u91cf\u9a8c\u8bc1\uff0c\u9010\u6b65\u6269\u5927",
      "\u6eda\u52a8\u66f4\u65b0\uff1a\u9010\u6b65\u66ff\u6362\u65e7\u5b9e\u4f8b\uff0c\u4fdd\u8bc1\u670d\u52a1\u53ef\u7528",
      "\u5065\u5eb7\u68c0\u67e5\uff1a\u914d\u7f6e\u5c31\u7eea\u63a2\u9488\u548c\u5b58\u6d3b\u63a2\u9488"
    ]
  },
  "184": {
    "title": "AI\u5de5\u7a0b\u5316\u9879\u76ee\u4e3b\u8981\u662f\u89e3\u51b3\u4ec0\u4e48\u95ee\u9898",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "185": {
    "title": "\u5982\u4f55\u7528\u5927\u6a21\u578b\u751f\u6210\u4ee3\u7801\uff1f",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": [
      "\u4e3e\u4e2a\u5177\u4f53\u4f8b\u5b50"
    ]
  },
  "186": {
    "title": "\u6570\u636e\u4e2d\u53f0\u4ecb\u7ecd",
    "style": "",
    "details": "",
    "subItems": [
      "\u6570\u636e\u4e2d\u53f0\u4f7f\u7528\u7684\u5e95\u5c42\u6280\u672f\u6846\u67b6\u662f\u4ec0\u4e48\uff1f",
      "\u6570\u636e\u67b6\u6784\u600e\u4e48\u8bbe\u8ba1\u7684"
    ]
  },
  "187": {
    "title": "\u5206\u5e03\u5f0f\u4e8b\u52a1",
    "style": "",
    "details": "",
    "subItems": [
      "\u5206\u5e03\u5f0f\u4e8b\u52a1\u89e3\u51b3\u65b9\u6848\u6709\u54ea\u4e9b\uff1f",
      "\u4e24\u9636\u6bb5\u63d0\u4ea4\u7f3a\u70b9\u548c\u89e3\u51b3\u65b9\u6848",
      "\u5f3a\u4e00\u81f4\u6027\u7684\u89e3\u51b3\u65b9\u6848\uff0c\u4e3a\u4ec0\u4e48\u4e0d\u7528\u5206\u5e03\u5f0f\u4e8b\u52a1XA\uff1f",
      "\u6700\u7ec8\u4e00\u81f4\u6027\u7684\u89e3\u51b3\u65b9\u6848",
      "\u672c\u5730\u4e8b\u52a1+Outbox\u65b9\u6848\uff0c\u4e3a\u4ec0\u4e48\u5f15\u5165\u672c\u5730\u4e8b\u52a1\u65e5\u5fd7\u8868\uff1f",
      "\u4e8b\u52a1\u65e5\u5fd7\u8868 + \u72b6\u6001\u673a\u7b56\u7565",
      "\u4e8b\u52a1\u65e5\u5fd7\u8868\u7206\u70b8\u4e86\u600e\u4e48\u529e\uff1f",
      "\u4e3a\u4ec0\u4e48\u4e0d\u7528MQ\u7684\u4e8b\u52a1\u6d88\u606f\uff1f",
      "TCC\u548cSaga\u7684\u89e3\u51b3\u65b9\u6848",
      "Seata\u4e00\u7ad9\u5f0f\u7684\u5206\u5e03\u5f0f\u89e3\u51b3\u65b9\u6848\u4ecb\u7ecd"
    ]
  },
  "188": {
    "title": "\u4efb\u52a1\u8c03\u5ea6\u4e2d\u5fc3\u7684\u4e1a\u52a1\u80cc\u666f\u662f\u4ec0\u4e48\uff1f",
    "style": "",
    "details": "",
    "subItems": [
      "\u5904\u7406\u672c\u5730\u4e8b\u52a1\u65e5\u5fd7\u8868\u7684\u91cd\u8bd5"
    ]
  },
  "189": {
    "title": "\u5728\u9879\u76ee\u4e2d\u5982\u4f55\u652f\u6301\u548c\u76d1\u63a7\u4e1a\u52a1\u9ad8\u654f\u573a\u666f\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "190": {
    "title": "\u5728\u865a\u62df\u56e2\u961f\u4e2d\u6709\u6ca1\u6709\u5e26\u9886\u56e2\u961f\u505a\u8fc7\u4e00\u4e9b\u4e8b\u60c5\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "191": {
    "title": "\u5728\u56e2\u961f\u8d44\u6e90\u534f\u8c03\u65b9\u9762\u6709\u4ec0\u4e48\u7ecf\u9a8c\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "192": {
    "title": "\u9650\u6d41 \u7194\u65ad \u964d\u7ea7",
    "style": "",
    "details": "",
    "subItems": [
      "\u9650\u6d41\u7b97\u6cd5\u4ecb\u7ecd",
      "\u7194\u65ad\u65b9\u6848 hystrix sentinel dubbo",
      "\u964d\u7ea7\u65b9\u5f0f \u5177\u4f53\u65b9\u6848"
    ]
  }
};
const DISPLAY_MAP = {
  "1": [
    [
      1,
      17,
      31,
      52,
      64,
      null
    ],
    [
      2,
      18,
      32,
      53,
      65,
      null
    ],
    [
      3,
      19,
      33,
      56,
      66,
      null
    ],
    [
      182,
      20,
      34,
      55,
      67,
      null
    ],
    [
      5,
      21,
      35,
      54,
      null,
      null
    ],
    [
      6,
      22,
      36,
      58,
      null,
      null
    ],
    [
      7,
      23,
      37,
      59,
      null,
      null
    ],
    [
      8,
      24,
      38,
      57,
      null,
      null
    ],
    [
      9,
      25,
      39,
      60,
      null,
      null
    ],
    [
      10,
      26,
      40,
      61,
      null,
      null
    ],
    [
      11,
      27,
      41,
      62,
      null,
      null
    ],
    [
      29,
      28,
      45,
      63,
      null,
      null
    ],
    [
      30,
      null,
      43,
      null,
      null,
      null
    ],
    [
      null,
      null,
      44,
      null,
      null,
      null
    ],
    [
      null,
      null,
      42,
      null,
      null,
      null
    ]
  ],
  "2": [
    [
      89,
      94,
      101,
      105,
      null,
      null
    ],
    [
      90,
      98,
      102,
      106,
      null,
      null
    ],
    [
      91,
      99,
      103,
      107,
      null,
      null
    ],
    [
      92,
      100,
      104,
      108,
      null,
      null
    ],
    [
      93,
      null,
      null,
      109,
      null,
      null
    ],
    [
      95,
      null,
      null,
      null,
      null,
      null
    ],
    [
      96,
      null,
      null,
      null,
      null,
      null
    ],
    [
      97,
      null,
      null,
      null,
      null,
      null
    ]
  ],
  "5": [
    [
      158,
      169,
      null,
      null,
      null,
      null
    ],
    [
      159,
      170,
      null,
      null,
      null,
      null
    ],
    [
      160,
      171,
      null,
      null,
      null,
      null
    ],
    [
      161,
      172,
      null,
      null,
      null,
      null
    ],
    [
      162,
      173,
      null,
      null,
      null,
      null
    ],
    [
      163,
      174,
      null,
      null,
      null,
      null
    ],
    [
      164,
      175,
      null,
      null,
      null,
      null
    ],
    [
      165,
      176,
      null,
      null,
      null,
      null
    ],
    [
      166,
      177,
      null,
      null,
      null,
      null
    ],
    [
      167,
      178,
      null,
      null,
      null,
      null
    ],
    [
      168,
      179,
      null,
      null,
      null,
      null
    ],
    [
      181,
      180,
      null,
      null,
      null,
      null
    ]
  ],
  "3": [
    [
      134,
      110,
      183,
      135,
      null,
      null
    ],
    [
      141,
      120,
      137,
      136,
      null,
      null
    ],
    [
      111,
      187,
      121,
      188,
      null,
      null
    ],
    [
      112,
      122,
      130,
      189,
      null,
      null
    ],
    [
      113,
      123,
      132,
      190,
      null,
      null
    ],
    [
      114,
      124,
      131,
      191,
      null,
      null
    ],
    [
      115,
      125,
      186,
      null,
      null,
      null
    ],
    [
      116,
      128,
      192,
      null,
      null,
      null
    ],
    [
      117,
      129,
      null,
      null,
      null,
      null
    ],
    [
      138,
      133,
      null,
      null,
      null,
      null
    ],
    [
      139,
      126,
      null,
      null,
      null,
      null
    ],
    [
      118,
      127,
      null,
      null,
      null,
      null
    ],
    [
      140,
      119,
      null,
      null,
      null,
      null
    ]
  ],
  "4": [
    [
      142,
      151,
      null,
      null,
      null,
      null
    ],
    [
      143,
      153,
      null,
      null,
      null,
      null
    ],
    [
      144,
      154,
      null,
      null,
      null,
      null
    ],
    [
      146,
      156,
      null,
      null,
      null,
      null
    ],
    [
      185,
      155,
      null,
      null,
      null,
      null
    ],
    [
      147,
      157,
      null,
      null,
      null,
      null
    ],
    [
      148,
      null,
      null,
      null,
      null,
      null
    ],
    [
      184,
      null,
      null,
      null,
      null,
      null
    ],
    [
      149,
      null,
      null,
      null,
      null,
      null
    ],
    [
      150,
      null,
      null,
      null,
      null,
      null
    ],
    [
      152,
      null,
      null,
      null,
      null,
      null
    ]
  ]
};
